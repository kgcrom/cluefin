"""Read Claude Code transcripts: the CLI calls an agent run made, their exit codes and outputs, and its report.

A transcript is a JSONL file. Subagent runs live at `<projects>/<slug>/<session>/subagents/agent-<id>.jsonl`
next to `agent-<id>.meta.json` (`agentType`, `description`); a main conversation is `<projects>/<slug>/<session>.jsonl`.
Bash calls are `tool_use` blocks; their result is the `tool_result` with the same id, `is_error` true and text
starting `Exit code N` on a non-zero exit.
"""

from __future__ import annotations

import json
import os
import re
import shlex
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

__all__ = [
    "APP_TOKEN",
    "AgentRun",
    "CliCall",
    "collect_folder",
    "find_runs",
    "find_session",
    "load_run",
    "load_session",
    "parse_cli_calls",
    "projects_dirs",
]

APP_TOKEN = "cluefin-openapi-cli"
# Flags that change the rendering, not what was fetched — two calls differing only here are the same call.
_RENDER_FLAGS = frozenset({"json", "compact", "fields"})
_CONTROL = frozenset({"&&", "||", ";", "|", "&", "(", ")"})
_EXIT_RE = re.compile(r"^(?:Error: )?Exit code (\d+)")
# `2>&1`, `> out.json`, `>> log`, `< in` — dropped before tokenising so `2` is not read as a flag value.
_REDIRECT_RE = re.compile(r"\s\d*(?:>>?|<)(?:&\d+|\s*[^\s|;&]+)")
# stdout sent to a file: the data never reaches the transcript, so the report's numbers cannot be traced.
_TO_FILE_RE = re.compile(r"(?:^|\s)1?>>?\s*(?!&)(?!/dev/null)[^\s|;&]+")
# Commands that only reshape or move around a CLI call; any other segment makes the Bash call "mixed".
_PLUMBING = frozenset({"cd", "head", "tail", "jq", "python", "python3", "grep", "sed", "cat", "echo", "wc", "sort"})


@dataclass(frozen=True, slots=True)
class CliCall:
    index: int
    path: tuple[str, ...]
    args: dict[str, str]
    exit_code: int | None  # None: the Bash call never ran (denied) or held several CLI calls
    output: str
    timestamp: str
    shell: str = ""  # the whole Bash command this call came from
    to_file: bool = False  # stdout redirected to a file
    mixed: bool = False  # the Bash command also ran non-CLI work, so output/exit code may not be this call's
    via: str = ""  # run folder of the `review collect` call that made this call (read from its manifest)

    @property
    def command(self) -> str:
        return " ".join(self.path)

    @property
    def key(self) -> tuple[str, tuple[tuple[str, str], ...]]:
        kept = tuple(sorted((k, v) for k, v in self.args.items() if k not in _RENDER_FLAGS))
        return self.command, kept

    def codes(self) -> list[str]:
        found: list[str] = []
        for name in ("stock-code", "code"):
            raw = self.args.get(name)
            if raw:
                found.extend(part.strip() for part in raw.split(",") if part.strip())
        return found


@dataclass(frozen=True, slots=True)
class AgentRun:
    run_id: str
    agent: str
    description: str
    session: str
    path: Path
    prompt: str
    report: str
    started: str
    ended: str
    calls: tuple[CliCall, ...] = field(default=())
    shell: tuple[str, ...] = field(default=())  # every Bash command, CLI or not
    reads: tuple[str, ...] = field(default=())  # file paths opened with the Read tool


def projects_dirs(root: Path, base: Path | None = None) -> list[Path]:
    """Transcript folders for this repository, worktrees included (their slug extends the repo's)."""

    if base is None:
        config = os.environ.get("CLAUDE_CONFIG_DIR")
        base = (Path(config) if config else Path.home() / ".claude") / "projects"
    slug = re.sub(r"[^A-Za-z0-9]", "-", str(root.resolve()))
    if not base.is_dir():
        return []
    return sorted(p for p in base.iterdir() if p.is_dir() and p.name.startswith(slug))


def _segments(command: str) -> list[tuple[list[str], bool]]:
    """Command segments split on shell control operators, each with whether its line sends stdout to a file."""

    segments: list[tuple[list[str], bool]] = []
    for raw in command.splitlines():
        to_file = bool(_TO_FILE_RE.search(raw))
        line = _REDIRECT_RE.sub(" ", raw)
        try:
            lexer = shlex.shlex(line, posix=True, punctuation_chars=True)
            lexer.whitespace_split = True
            tokens = list(lexer)
        except ValueError:
            tokens = line.split()
        current: list[str] = []
        for token in tokens:
            if token in _CONTROL:
                if current:
                    segments.append((current, to_file))
                current = []
            else:
                current.append(token)
        if current:
            segments.append((current, to_file))
    return segments


def _parse_invocation(tokens: list[str]) -> tuple[tuple[str, ...], dict[str, str]] | None:
    start = next((i for i, tok in enumerate(tokens) if tok.endswith(APP_TOKEN)), None)
    if start is None:
        return None
    rest = tokens[start + 1 :]
    path: list[str] = []
    i = 0
    while i < len(rest) and not rest[i].startswith("-"):
        path.append(rest[i])
        i += 1
    args: dict[str, str] = {}
    while i < len(rest):
        token = rest[i]
        if token.startswith("--"):
            name, _, inline = token[2:].partition("=")
            name = name.replace("_", "-")
            if inline:
                args[name] = inline
            elif i + 1 < len(rest) and not rest[i + 1].startswith("--") and not rest[i + 1].startswith(">"):
                args[name] = rest[i + 1]
                i += 1
            else:
                args[name] = "true"
        i += 1
    if not path:
        return None
    return tuple(path), args


def parse_cli_calls(command: str) -> list[tuple[tuple[str, ...], dict[str, str]]]:
    return [(path, args) for path, args, _ in _parse_with_flags(command)[0]]


def _parse_with_flags(command: str) -> tuple[list[tuple[tuple[str, ...], dict[str, str], bool]], bool]:
    """CLI invocations with their to-file flag, and whether the command did other (non-plumbing) work."""

    calls = []
    mixed = False
    for tokens, to_file in _segments(command):
        parsed = _parse_invocation(tokens)
        if parsed is not None:
            calls.append((*parsed, to_file))
        elif tokens and tokens[0] not in _PLUMBING and tokens[0] not in {"uv", "do", "done", "for"}:
            mixed = True
    return calls, mixed


def _text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(part.get("text", "") for part in content if isinstance(part, dict))
    return ""


def _exit_code(result: dict[str, Any]) -> int | None:
    text = _text(result.get("content"))
    if not result.get("is_error"):
        return 0
    match = _EXIT_RE.match(text)
    return int(match.group(1)) if match else None


def _read_rows(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


@dataclass(frozen=True, slots=True)
class _Extracted:
    calls: list[CliCall]
    texts: list[tuple[str, str]]  # (timestamp, assistant text)
    shell: list[tuple[str, str]]  # (timestamp, Bash command)
    reads: list[tuple[str, str]]  # (timestamp, Read file path)


def _extract(rows: list[dict[str, Any]]) -> _Extracted:
    """CLI calls in order, every assistant text block, every Bash command and every Read path."""

    pending: dict[str, tuple[str, str]] = {}
    shell: dict[str, tuple[str, str]] = {}
    reads: dict[str, tuple[str, str]] = {}
    results: dict[str, dict[str, Any]] = {}
    texts: list[tuple[str, str]] = []
    order: list[str] = []
    for row in rows:
        content = row.get("message", {}).get("content")
        if not isinstance(content, list):
            continue
        stamp = str(row.get("timestamp", ""))
        for block in content:
            if not isinstance(block, dict):
                continue
            kind = block.get("type")
            if kind == "tool_use" and block.get("name") == "Read":
                reads.setdefault(str(block.get("id")), (stamp, str(block.get("input", {}).get("file_path", ""))))
            if kind == "tool_use" and block.get("name") == "Bash":
                command = str(block.get("input", {}).get("command", ""))
                shell.setdefault(str(block.get("id")), (stamp, command))
                # A streamed assistant turn can repeat the same tool_use block in several rows.
                if APP_TOKEN in command and block["id"] not in pending:
                    pending[block["id"]] = (command, stamp)
                    order.append(block["id"])
            elif kind == "tool_result":
                results[str(block.get("tool_use_id"))] = block
            elif kind == "text" and row.get("type") == "assistant":
                texts.append((stamp, str(block.get("text", ""))))
    calls: list[CliCall] = []
    for tool_id in order:
        command, stamp = pending[tool_id]
        result = results.get(tool_id)
        parsed, mixed = _parse_with_flags(command)
        exit_code = _exit_code(result) if result is not None else None
        output = _text(result.get("content")) if result is not None else ""
        for path, args, to_file in parsed:
            calls.append(
                CliCall(
                    index=len(calls),
                    path=path,
                    args=args,
                    exit_code=exit_code if len(parsed) == 1 else None,
                    output=output if len(parsed) == 1 else "",
                    timestamp=stamp,
                    shell=command,
                    to_file=to_file,
                    mixed=mixed,
                )
            )
    return _Extracted(_expand_collect(calls), texts, list(shell.values()), list(reads.values()))


_COLLECT = ("review", "collect")


def _json_object(text: str) -> Any:
    """The first JSON object in a tool result (stderr warnings can come before it)."""

    start = text.find("{")
    if start < 0:
        return None
    try:
        value, _ = json.JSONDecoder().raw_decode(text[start:])
    except ValueError:
        return None
    return value


def collect_folder(call: CliCall) -> Path | None:
    """The run folder a successful `review collect` call printed, if it still has a manifest."""

    if call.path != _COLLECT or call.exit_code != 0:
        return None
    payload = _json_object(call.output)
    out = payload.get("out") if isinstance(payload, dict) else None
    if not out or not (Path(out) / "manifest.jsonl").is_file():
        return None
    return Path(out)


def _manifest_calls(call: CliCall, folder: Path) -> list[CliCall]:
    calls: list[CliCall] = []
    for row in _read_rows(folder / "manifest.jsonl"):
        argv = row.get("argv")
        parsed = _parse_invocation([APP_TOKEN, *map(str, argv)]) if isinstance(argv, list) else None
        if parsed is None:
            continue
        raw = folder / str(row.get("file", ""))
        output = raw.read_text(encoding="utf-8") if raw.is_file() else ""
        exit_code = row.get("exit_code")
        calls.append(
            CliCall(
                index=0,
                path=parsed[0],
                args=parsed[1],
                exit_code=exit_code if isinstance(exit_code, int) else None,
                output=output,
                timestamp=str(row.get("started", call.timestamp)),
                shell=call.shell,
                via=str(folder),
            )
        )
    return calls


def _expand_collect(calls: list[CliCall]) -> list[CliCall]:
    """Each `review collect` call followed by the calls its manifest records, so checks see what it fetched."""

    out: list[CliCall] = []
    consumed: dict[Path, int] = {}  # `--into` appends to a folder: a later call adds only the new manifest lines
    for call in calls:
        out.append(call)
        folder = collect_folder(call)
        if folder is not None:
            rows = _manifest_calls(call, folder)
            out.extend(rows[consumed.get(folder, 0) :])
            consumed[folder] = len(rows)
    return [replace(c, index=i) for i, c in enumerate(out)]


def _first_prompt(rows: list[dict[str, Any]]) -> str:
    for row in rows:
        if row.get("type") == "user":
            text = _text(row.get("message", {}).get("content"))
            if text:
                return text
    return ""


def _folder_reports(calls: list[CliCall] | tuple[CliCall, ...]) -> str:
    """`report.md` of each review collect folder the calls came from — the agent writes its report there."""

    folders = dict.fromkeys(Path(c.via) for c in calls if c.via)
    parts = []
    for folder in folders:
        report = folder / "report.md"
        if report.is_file():
            parts.append(report.read_text(encoding="utf-8"))
    return "\n\n".join(parts)


def _join(*texts: str) -> str:
    return "\n\n".join(t for t in texts if t)


def load_run(jsonl: Path) -> AgentRun:
    meta_path = jsonl.with_suffix(".meta.json")
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    rows = _read_rows(jsonl)
    found = _extract(rows)
    texts = found.texts
    stamps = [str(r["timestamp"]) for r in rows if r.get("timestamp")]
    return AgentRun(
        run_id=jsonl.stem.removeprefix("agent-"),
        agent=str(meta.get("agentType", "")),
        description=str(meta.get("description", "")),
        session=jsonl.parent.parent.name,
        path=jsonl,
        prompt=_first_prompt(rows),
        report=_join(_folder_reports(found.calls), texts[-1][1] if texts else ""),
        started=stamps[0] if stamps else "",
        ended=stamps[-1] if stamps else "",
        calls=tuple(found.calls),
        shell=tuple(command for _, command in found.shell),
        reads=tuple(path for _, path in found.reads),
    )


def load_session(jsonl: Path, code: str) -> AgentRun:
    """A main-conversation analysis of one stock: calls and assistant text from the first call naming `code` on."""

    rows = _read_rows(jsonl)
    found = _extract(rows)
    calls, texts = found.calls, found.texts
    first = next((c for c in calls if code in c.codes()), None)
    if first is None:
        kept: list[CliCall] = []
        report = ""
        started = ""
    else:
        kept = [c for c in calls if c.index >= first.index]
        report = _join(_folder_reports(kept), "\n\n".join(text for stamp, text in texts if stamp >= first.timestamp))
        started = first.timestamp
    stamps = [str(r["timestamp"]) for r in rows if r.get("timestamp")]
    return AgentRun(
        run_id=jsonl.stem,
        agent="",
        description=f"main conversation, {code}",
        session=jsonl.stem,
        path=jsonl,
        prompt=code,
        report=report,
        started=started,
        ended=stamps[-1] if stamps else "",
        calls=tuple(replace(c, index=i) for i, c in enumerate(kept)),
        shell=tuple(cmd for stamp, cmd in found.shell if started and stamp >= started),
        reads=tuple(path for stamp, path in found.reads if started and stamp >= started),
    )


def find_runs(dirs: list[Path]) -> list[Path]:
    """Every subagent transcript under `dirs`, oldest first by file time."""

    found = [p for d in dirs for p in d.glob("*/subagents/agent-*.jsonl")]
    return sorted(found, key=lambda p: p.stat().st_mtime)


def find_session(dirs: list[Path], session: str) -> Path | None:
    for d in dirs:
        candidate = d / f"{session}.jsonl"
        if candidate.exists():
            return candidate
    return None
