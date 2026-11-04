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
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

__all__ = [
    "APP_TOKEN",
    "AgentRun",
    "CliCall",
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


@dataclass(frozen=True, slots=True)
class CliCall:
    index: int
    path: tuple[str, ...]
    args: dict[str, str]
    exit_code: int | None  # None: the Bash call never ran (denied) or held several CLI calls
    output: str
    timestamp: str

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


def projects_dirs(root: Path, base: Path | None = None) -> list[Path]:
    """Transcript folders for this repository, worktrees included (their slug extends the repo's)."""

    if base is None:
        config = os.environ.get("CLAUDE_CONFIG_DIR")
        base = (Path(config) if config else Path.home() / ".claude") / "projects"
    slug = re.sub(r"[^A-Za-z0-9]", "-", str(root.resolve()))
    if not base.is_dir():
        return []
    return sorted(p for p in base.iterdir() if p.is_dir() and p.name.startswith(slug))


def _segments(command: str) -> list[list[str]]:
    segments: list[list[str]] = []
    for raw in command.splitlines():
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
                    segments.append(current)
                current = []
            else:
                current.append(token)
        if current:
            segments.append(current)
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
    calls = []
    for segment in _segments(command):
        parsed = _parse_invocation(segment)
        if parsed is not None:
            calls.append(parsed)
    return calls


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


def _extract(rows: list[dict[str, Any]]) -> tuple[list[CliCall], list[tuple[str, str]]]:
    """CLI calls in order, and every assistant text block as (timestamp, text)."""

    pending: dict[str, tuple[str, str]] = {}
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
            if kind == "tool_use" and block.get("name") == "Bash":
                command = str(block.get("input", {}).get("command", ""))
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
        parsed = parse_cli_calls(command)
        exit_code = _exit_code(result) if result is not None else None
        output = _text(result.get("content")) if result is not None else ""
        for path, args in parsed:
            calls.append(
                CliCall(
                    index=len(calls),
                    path=path,
                    args=args,
                    exit_code=exit_code if len(parsed) == 1 else None,
                    output=output if len(parsed) == 1 else "",
                    timestamp=stamp,
                )
            )
    return calls, texts


def _first_prompt(rows: list[dict[str, Any]]) -> str:
    for row in rows:
        if row.get("type") == "user":
            text = _text(row.get("message", {}).get("content"))
            if text:
                return text
    return ""


def load_run(jsonl: Path) -> AgentRun:
    meta_path = jsonl.with_suffix(".meta.json")
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    rows = _read_rows(jsonl)
    calls, texts = _extract(rows)
    stamps = [str(r["timestamp"]) for r in rows if r.get("timestamp")]
    return AgentRun(
        run_id=jsonl.stem.removeprefix("agent-"),
        agent=str(meta.get("agentType", "")),
        description=str(meta.get("description", "")),
        session=jsonl.parent.parent.name,
        path=jsonl,
        prompt=_first_prompt(rows),
        report=texts[-1][1] if texts else "",
        started=stamps[0] if stamps else "",
        ended=stamps[-1] if stamps else "",
        calls=tuple(calls),
    )


def load_session(jsonl: Path, code: str) -> AgentRun:
    """A main-conversation analysis of one stock: calls and assistant text from the first call naming `code` on."""

    rows = _read_rows(jsonl)
    calls, texts = _extract(rows)
    first = next((c for c in calls if code in c.codes()), None)
    if first is None:
        kept: list[CliCall] = []
        report = ""
        started = ""
    else:
        kept = [c for c in calls if c.index >= first.index]
        report = "\n\n".join(text for stamp, text in texts if stamp >= first.timestamp)
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
        calls=tuple(CliCall(i, c.path, c.args, c.exit_code, c.output, c.timestamp) for i, c in enumerate(kept)),
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
