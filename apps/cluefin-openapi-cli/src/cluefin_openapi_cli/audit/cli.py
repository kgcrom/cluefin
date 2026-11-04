"""`audit <sub>` meta command: check agent runs from Claude Code transcripts. Reads files only, no broker."""

from __future__ import annotations

import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from cluefin_openapi_cli.audit.check import ALIASES, check_run, load_spec
from cluefin_openapi_cli.audit.transcript import (
    AgentRun,
    find_runs,
    find_session,
    load_run,
    load_session,
    projects_dirs,
)
from cluefin_openapi_cli.cliargs import _parse_named_options, _str_option
from cluefin_openapi_cli.errors import EXIT_USAGE, CliError
from cluefin_openapi_cli.output import render_output

__all__ = ["SUBCOMMANDS", "run_audit"]

_AGENTS_DIR = Path(".claude") / "agents"
_DEFAULT_MAX_CHARS = 4000


def _repo_root() -> Path:
    here = Path.cwd().resolve()
    for candidate in (here, *here.parents):
        if (candidate / _AGENTS_DIR).is_dir():
            return candidate
    raise CliError(
        "No `.claude/agents` folder above the current directory.",
        exit_code=EXIT_USAGE,
        hint="Run `audit` from the cluefin repository root.",
    )


def _agent_commit(root: Path, agent: str, started: str) -> str | None:
    """The last commit of the agent file at the run's start — the prompt version the run used."""

    name = ALIASES.get(agent, agent)
    # Old names are listed as paths instead of `--follow`, which finds nothing when combined with `--before`.
    names = [name, *(old for old, new in ALIASES.items() if new == name)]
    command = ["git", "log", "-1", "--format=%h"]
    if started:
        command.append(f"--before={started}")
    command += ["--", *(str(_AGENTS_DIR / f"{n}.md") for n in names)]
    try:
        out = subprocess.run(command, cwd=root, capture_output=True, text=True, check=False, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return out.stdout.strip() or None


def _valid_codes() -> frozenset[str] | None:
    """Known stock codes from the local cache, or None when there is no cache (then every 6-digit number counts)."""

    try:
        from cluefin_openapi_cli.cache import store

        path = store.cache_path()
        if not path.exists():
            return None
        conn = store.open_store(path, read_only=True)
        try:
            rows = conn.execute("SELECT code FROM company").fetchall()
        finally:
            conn.close()
    except Exception:  # noqa: BLE001 - an unreadable cache only loosens the filter, it never fails the audit
        return None
    return frozenset(str(row[0]) for row in rows)


def _run_summary(run: AgentRun, root: Path) -> dict[str, Any]:
    return {
        "run": run.run_id,
        "agent": ALIASES.get(run.agent, run.agent),
        "agent_at_run": run.agent,
        "description": run.description,
        "session": run.session,
        "started": run.started,
        "ended": run.ended,
        "agent_commit": _agent_commit(root, run.agent or "company-review", run.started),
        "cli_calls": len(run.calls),
    }


def _all_runs(root: Path, agent: str | None) -> list[AgentRun]:
    runs = [load_run(path) for path in find_runs(projects_dirs(root))]
    known = {p.stem for p in (root / _AGENTS_DIR).glob("*.md")} | set(ALIASES)
    runs = [r for r in runs if r.agent in known]
    if agent:
        runs = [r for r in runs if ALIASES.get(r.agent, r.agent) == agent]
    return runs


def _resolve(root: Path, options: dict[str, Any]) -> tuple[AgentRun, str, str | None]:
    """The run to look at, its agent name, and the main stock when it is a main-conversation slice."""

    run_id = _str_option(options, "run")
    session = _str_option(options, "session")
    agent = _str_option(options, "agent")
    dirs = projects_dirs(root)
    if run_id:
        match = next((p for p in find_runs(dirs) if p.stem == f"agent-{run_id}"), None)
        if match is None:
            raise CliError(f"No subagent run `{run_id}`.", exit_code=EXIT_USAGE, hint="List runs with `audit runs`.")
        run = load_run(match)
        return run, agent or ALIASES.get(run.agent, run.agent), None
    if session:
        code = _str_option(options, "code")
        if not code:
            raise CliError("`--session` needs `--code <stock code>`.", exit_code=EXIT_USAGE)
        path = find_session(dirs, session)
        if path is None:
            raise CliError(f"No session `{session}`.", exit_code=EXIT_USAGE)
        return load_session(path, code), agent or "company-review", code
    raise CliError("Give `--run <agent id>` or `--session <id> --code <code>`.", exit_code=EXIT_USAGE)


def _spec(root: Path, agent: str) -> Any:
    try:
        return load_spec(root / _AGENTS_DIR, agent)
    except FileNotFoundError:
        raise CliError(f"No agent file for `{agent}`.", exit_code=EXIT_USAGE) from None
    except ValueError as exc:
        raise CliError(str(exc), exit_code=EXIT_USAGE) from None


def _render(payload: Any, options: dict[str, Any]) -> None:
    render_output(payload, force_json=bool(options.get("json", False)), compact=bool(options.get("compact", False)))


def _run_runs(argv: list[str]) -> None:
    _, options = _parse_named_options(argv)
    root = _repo_root()
    runs = _all_runs(root, _str_option(options, "agent"))
    limit = int(_str_option(options, "limit") or 20)
    rows = [_run_summary(r, root) for r in runs[-limit:]]
    _render({"count": len(rows), "runs": rows}, options)


def _run_check(argv: list[str]) -> None:
    _, options = _parse_named_options(argv)
    root = _repo_root()
    run, agent, main_code = _resolve(root, options)
    result = check_run(_spec(root, agent), run, main_code, _valid_codes())
    summary = _run_summary(run, root)
    notes = []
    current = _agent_commit(root, agent, "")
    if summary["agent_commit"] != current:
        notes.append(
            f"Checked against the current agent file ({current}), not the version the run used "
            f"({summary['agent_commit']}): a command added since then shows as missing."
        )
    _render({**summary, "spec_commit": current, **result, "notes": notes}, options)


def _run_trace(argv: list[str]) -> None:
    _, options = _parse_named_options(argv)
    root = _repo_root()
    run, _agent, _main = _resolve(root, options)
    max_chars = int(_str_option(options, "max_chars") or _DEFAULT_MAX_CHARS)
    calls = [
        {
            "i": c.index,
            "command": c.command,
            "args": c.args,
            "exit_code": c.exit_code,
            "to_file": c.to_file,
            "mixed_shell": c.mixed,
            "shell": c.shell[:500],
            "output_chars": len(c.output),
            "output": c.output[:max_chars],
        }
        for c in run.calls
    ]
    payload = {
        **_run_summary(run, root),
        "prompt": run.prompt[:max_chars],
        "calls": calls,
        "report": run.report,
        "notes": [
            f"Each call output is cut at {max_chars} characters (`output_chars` is the full length).",
            "`to_file`: stdout went to a file — the data is not in the output. `mixed_shell`: the Bash command did "
            "other work too, so `output`/`exit_code` may belong to that work (see `shell`).",
        ],
    }
    _render(payload, options)


def _run_report(argv: list[str]) -> None:
    """Every run of every agent checked, findings counted per agent and per prompt version."""

    _, options = _parse_named_options(argv)
    root = _repo_root()
    valid = _valid_codes()
    groups: dict[tuple[str, str], dict[str, Any]] = {}
    tally: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for run in _all_runs(root, _str_option(options, "agent")):
        agent = ALIASES.get(run.agent, run.agent)
        commit = _agent_commit(root, run.agent, run.started) or "unknown"
        result = check_run(_spec(root, agent), run, None, valid)
        group = groups.setdefault((agent, commit), {"agent": agent, "agent_commit": commit, "runs": []})
        group["runs"].append({"run": run.run_id, "started": run.started, "counts": result["counts"]})
        for finding in result["findings"]:
            tally[(agent, commit)][f"{finding['type']}: {finding.get('command', finding.get('stopped_by', ''))}"] += 1
    rows = []
    for key, group in groups.items():
        group["findings"] = dict(tally[key].most_common())
        rows.append(group)
    _render(
        {"groups": rows, "notes": ["Main-conversation analyses are not listed; check them with --session."]}, options
    )


SUBCOMMANDS = {"runs": _run_runs, "check": _run_check, "trace": _run_trace, "report": _run_report}


def run_audit(argv: list[str]) -> None:
    if not argv or argv[0] not in SUBCOMMANDS:
        raise CliError(
            f"`audit` takes one of: {', '.join(SUBCOMMANDS)}.",
            exit_code=EXIT_USAGE,
            data={"subcommands": list(SUBCOMMANDS)},
        )
    SUBCOMMANDS[argv[0]](argv[1:])
