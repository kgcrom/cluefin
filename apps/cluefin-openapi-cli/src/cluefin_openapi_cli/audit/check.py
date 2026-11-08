"""Deterministic audit of one agent run against the `audit` block of its agent file.

It finds what can be found without reading the report for meaning: commands the agent file requires but the run
never called (for the stock under review and for each peer), calls repeated with the same arguments after a
success, calls made after an exit 3 that should have stopped the run, and failed calls never retried. Whether the
report used what it fetched is judged by the `agent-audit` agent from `audit trace`, not here.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from cluefin_openapi_cli.audit.transcript import AgentRun, CliCall, collect_folder

__all__ = ["AuditSpec", "check_run", "corp_map", "load_spec", "parse_spec", "subjects"]

_BLOCK_RE = re.compile(r"```audit\n(.*?)```", re.DOTALL)
_CODE_RE = re.compile(r"(?<![0-9A-Za-z])(\d{6})(?![0-9])")
_KINDS = frozenset({"subjects", "required", "main", "each", "stop-on-exit3", "report-has", "report-lacks"})
# Ways to reach a broker or a secret without the CLI. The CLI is read-only (every registered command has
# side_effect "read"), so these are the only paths to an order, a printed key, or data the audit cannot trace.
_SECRET_RE = re.compile(
    r"(?:cat|less|head|tail|grep|source)\s+[^|;&]*\.env\b|\bprintenv\b|\$\{?(?:KIS|KIWOOM|DART|ECOS|NH)_\w*"
)
_SHELL_API_RE = re.compile(r"\bcurl\b|\bwget\b|(?:from|import)\s+(?:cluefin_openapi|requests|httpx)\b")
_CODE_API_RE = re.compile(r"^\s*(?:from|import)\s+(?:cluefin_openapi|requests|httpx)\b", re.MULTILINE)
_ORDER_RE = re.compile(r"order|주문", re.IGNORECASE)
_HEREDOC_RE = re.compile(r"<<-?\s*['\"]?(\w+)['\"]?")
_INTERPRETERS = ("python", "python3", "uv run python", "bash", "sh", "node")


def _split_shell(command: str) -> tuple[str, str]:
    """(shell lines, code that runs). A heredoc body runs only when fed to an interpreter; written to a file
    (`cat > x <<EOF`) it is just text and is dropped. Lines that call the CLI are left out of the shell part."""

    shell: list[str] = []
    code: list[str] = []
    lines = command.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        match = _HEREDOC_RE.search(line)
        if "cluefin-openapi-cli" not in line:
            shell.append(line)
        if match:
            tag = match.group(1)
            body: list[str] = []
            i += 1
            while i < len(lines) and lines[i].strip() != tag:
                body.append(lines[i])
                i += 1
            head = line.split("<<")[0].strip().split("&&")[-1].strip()
            if head.split()[:1] in (["bash"], ["sh"], ["zsh"]):
                # A shell heredoc is shell: `bash <<EOF` + `curl ...` is a direct API call.
                shell.extend(row for row in body if "cluefin-openapi-cli" not in row)
            elif head.startswith(_INTERPRETERS):
                code.extend(body)
        i += 1
    return "\n".join(shell), "\n".join(code)


# Discovery commands (cheap, local) are not counted as duplicate data calls.
_DISCOVERY = frozenset({"search", "schema", "describe", "list", "domains", "tags", "brokers", "recipes", "recipe"})
# Agent names that were renamed: their old runs are checked against the new file.
ALIASES = {"market-review": "company-review"}


@dataclass(frozen=True, slots=True)
class AuditSpec:
    agent: str
    subjects: tuple[str, ...] = ("prompt",)
    required: tuple[str, ...] = ()
    main: tuple[str, ...] = ()
    each: tuple[str, ...] = ()
    stop_brokers: tuple[str, ...] = field(default=())
    report_has: tuple[str, ...] = ()
    report_lacks: tuple[str, ...] = ()


def parse_spec(agent: str, text: str) -> AuditSpec:
    match = _BLOCK_RE.search(text)
    if match is None:
        raise ValueError(f"no ```audit block in the `{agent}` agent file")
    values: dict[str, list[str]] = {kind: [] for kind in _KINDS}
    for raw in match.group(1).splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        kind, sep, rest = line.partition(":")
        kind = kind.strip()
        if not sep or kind not in _KINDS:
            raise ValueError(f"unknown audit line `{line}` in `{agent}`")
        if kind in {"subjects", "stop-on-exit3"}:
            values[kind].extend(part for part in re.split(r"[,\s]+", rest) if part)
        elif kind in {"report-has", "report-lacks"}:
            if rest.strip():
                values[kind].append(rest.strip())
        elif rest.strip():
            values[kind].append(" ".join(rest.split()))
    return AuditSpec(
        agent=agent,
        subjects=tuple(values["subjects"]) or ("prompt",),
        required=tuple(values["required"]),
        main=tuple(values["main"]),
        each=tuple(values["each"]),
        stop_brokers=tuple(values["stop-on-exit3"]),
        report_has=tuple(values["report-has"]),
        report_lacks=tuple(values["report-lacks"]),
    )


def load_spec(agents_dir: Path, agent: str) -> AuditSpec:
    name = ALIASES.get(agent, agent)
    path = agents_dir / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(path)
    return parse_spec(name, path.read_text(encoding="utf-8"))


def _walk(node: Any, pairs: dict[str, str]) -> None:
    if isinstance(node, dict):
        stock, corp = node.get("stock_code"), node.get("corp_code")
        if isinstance(stock, str) and isinstance(corp, str) and stock.strip() and corp.strip():
            pairs.setdefault(stock.strip(), corp.strip())
        for value in node.values():
            _walk(value, pairs)
    elif isinstance(node, list):
        for value in node:
            _walk(value, pairs)


def corp_map(calls: tuple[CliCall, ...]) -> dict[str, str]:
    """stock code → DART corp code, read from any CLI output that carries both."""

    pairs: dict[str, str] = {}
    for call in calls:
        body = _json_body(call.output)
        if body is None:
            continue
        try:
            _walk(json.loads(body), pairs)
        except json.JSONDecodeError:
            continue
    return pairs


def _json_body(output: str) -> str | None:
    """The JSON part of a call output; log lines (retry warnings) can come first on the same stream."""

    if output.lstrip().startswith(("{", "[")):
        return output
    for marker in ("\n{", "\n["):
        at = output.find(marker)
        if at >= 0:
            return output[at + 1 :]
    return None


def _codes_in(text: str, valid: frozenset[str] | None) -> list[str]:
    seen: list[str] = []
    for code in _CODE_RE.findall(text):
        if code not in seen and (valid is None or code in valid):
            seen.append(code)
    return seen


def subjects(
    spec: AuditSpec, run: AgentRun, main_code: str | None = None, valid: frozenset[str] | None = None
) -> tuple[str | None, list[str]]:
    """The stock under review and every stock the run should have covered (peers, candidates, watchlist).

    ``valid`` is the set of known stock codes (the cache's company table); a six-digit number in prose that is
    not one (an amount, a corp code) is then not taken for a stock.
    """

    found: list[str] = []
    if main_code:
        found.append(main_code)
    if main_code is None:
        if "prompt" in spec.subjects:
            found.extend(_codes_in(run.prompt, valid))
        if "report" in spec.subjects:
            found.extend(_codes_in(run.report, valid))
    else:
        # A main-conversation slice: its text mixes other work, so peers come from what the CLI was asked about.
        each = set(spec.each)
        for call in run.calls:
            if call.command in each:
                found.extend(call.codes())
    unique = list(dict.fromkeys(found))
    main = main_code or (unique[0] if unique else next((c for call in run.calls for c in call.codes()), None))
    if main and main not in unique:
        unique.insert(0, main)
    return main, unique


def _covers(call: CliCall, code: str, corp: str | None) -> bool:
    if code in call.codes():
        return True
    return corp is not None and call.args.get("corp-code") == corp


def _off_cli(run: AgentRun) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    for command in run.shell:
        shell, code = _split_shell(command)
        secret = _SECRET_RE.search(shell)
        if secret:
            found.append({"type": "off_cli_secret", "match": secret.group(0), "shell": command[:300]})
        api = _SHELL_API_RE.search(shell) or _CODE_API_RE.search(code)
        if api:
            found.append({"type": "off_cli_direct_api", "match": api.group(0).strip(), "shell": command[:300]})
            order = _ORDER_RE.search(shell + "\n" + code)
            if order:
                found.append({"type": "off_cli_order", "match": order.group(0), "shell": command[:300]})
    for path in run.reads:
        if path.endswith(".env") or "/.env" in path:
            found.append({"type": "off_cli_secret", "match": "Read", "shell": path})
    return found


def _report_contract(spec: AuditSpec, run: AgentRun) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if not run.report.strip():
        return [{"type": "report_missing"}] if spec.report_has else []
    for needle in spec.report_has:
        if needle not in run.report:
            found.append({"type": "report_lacks_required", "text": needle})
    for pattern in spec.report_lacks:
        match = re.search(pattern, run.report)
        if match:
            found.append({"type": "report_has_forbidden", "pattern": pattern, "match": match.group(0)})
    return found


def check_run(
    spec: AuditSpec, run: AgentRun, main_code: str | None = None, valid: frozenset[str] | None = None
) -> dict[str, Any]:
    calls = run.calls
    corps = corp_map(calls)
    main, covered = subjects(spec, run, main_code, valid)
    findings: list[dict[str, Any]] = []

    called = {call.command for call in calls}
    for command in spec.required:
        if command not in called:
            findings.append({"type": "missing_required", "command": command})

    def missing_for(command: str, code: str) -> bool:
        return not any(call.command == command and _covers(call, code, corps.get(code)) for call in calls)

    if main:
        for command in spec.main:
            if missing_for(command, main):
                findings.append({"type": "missing_main", "command": command, "code": main})
    for code in covered:
        for command in spec.each:
            if missing_for(command, code):
                finding: dict[str, Any] = {"type": "missing_each", "command": command, "code": code}
                if code != main:
                    finding["role"] = "peer_or_candidate"
                if command.startswith("dart ") and code not in corps:
                    finding["note"] = "no corp code seen for this stock, so a call by corp code could not be matched"
                findings.append(finding)

    shell = [c for c in calls if any("$" in v for v in c.args.values())]
    if shell:
        findings.append(
            {
                "type": "shell_expansion",
                "commands": sorted({c.command for c in shell}),
                "count": len(shell),
                "note": "arguments built by a shell loop or $(...) — the agent file asks for one literal call each",
            }
        )

    lost = [c for c in calls if c.path == ("review", "collect") and c.exit_code == 0 and collect_folder(c) is None]
    if lost:
        findings.append(
            {
                "type": "collect_manifest_missing",
                "calls": [c.index for c in lost],
                "note": "review collect ran but its folder or manifest.jsonl is gone (/tmp cleared?), so what it "
                "fetched cannot be checked",
            }
        )

    to_file = [c for c in calls if c.to_file]
    if to_file:
        findings.append(
            {
                "type": "output_to_file",
                "calls": [c.index for c in to_file],
                "commands": sorted({c.command for c in to_file}),
                "note": "stdout went to a file, so numbers taken from it cannot be traced to a CLI response",
            }
        )

    seen: dict[tuple[str, tuple[tuple[str, str], ...]], list[CliCall]] = {}
    for call in calls:
        if call.exit_code == 0 and call.path[0] not in _DISCOVERY and call not in shell:
            seen.setdefault(call.key, []).append(call)
    for (command, args), group in seen.items():
        if len(group) > 1:
            findings.append(
                {
                    "type": "duplicate",
                    "command": command,
                    "args": dict(args),
                    "count": len(group),
                    "calls": [c.index for c in group],
                    # Same arguments, different answers: a paged or unstable response, not plain waste.
                    "same_output": len({c.output for c in group}) == 1,
                }
            )

    if spec.stop_brokers:
        stop = next((c for c in calls if c.exit_code == 3 and c.path[0] in spec.stop_brokers), None)
        if stop is not None:
            later = [c.command for c in calls if c.index > stop.index]
            if later:
                findings.append(
                    {"type": "continued_after_exit3", "stopped_by": stop.command, "later_calls": later[:10]}
                )

    for call in calls:
        if call.exit_code in (None, 0, 3):
            continue
        retried = any(c.index > call.index and c.key == call.key and c.exit_code == 0 for c in calls)
        if not retried:
            findings.append(
                {"type": "failed_not_retried", "command": call.command, "args": call.args, "exit_code": call.exit_code}
            )

    findings.extend(_off_cli(run))
    findings.extend(_report_contract(spec, run))

    counts = Counter(f["type"] for f in findings)
    return {
        "agent": spec.agent,
        "main": main,
        "subjects": covered,
        "calls": len(calls),
        "distinct_calls": len({c.key for c in calls}),
        "counts": dict(counts),
        "findings": findings,
    }
