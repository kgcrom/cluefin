"""`audit runs|check|trace|report` end to end over a fake repository and transcript folder (pinned agent history, no cache)."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

import pytest

from cluefin_openapi_cli.audit import cli as audit_cli
from cluefin_openapi_cli.audit.cli import run_audit
from cluefin_openapi_cli.errors import EXIT_USAGE, CliError
from tests.test_audit_unit import APP, SPEC, _bash, _result

RUN_ID = "abc123"
SESSION_ID = "11111111-2222-3333-4444-555555555555"


def _rows() -> list[dict]:
    return [
        {"type": "user", "timestamp": "2026-11-08T01:00:00Z", "message": {"content": "삼성전자(005930) 검토"}},
        _bash("1", f"{APP} ecos macro-snapshot --json", "2026-11-08T01:00:01Z"),
        _result("1", "{}"),
        _bash("2", f"{APP} kis stock current-price \\\n  --stock-code 005930 --json", "2026-11-08T01:00:02Z"),
        _result("2", '{"stock_code": "005930", "price": "' + "9" * 50 + '"}'),
        _bash("3", f"{APP} kis stock current-price --stock-code 005930 --json", "2026-11-08T01:00:03Z"),
        _result("3", "{}"),
        {
            "type": "assistant",
            "timestamp": "2026-11-08T01:00:04Z",
            "message": {"content": [{"type": "text", "text": "# 리포트\n삼성전자(005930)"}]},
        },
    ]


def _write(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows), encoding="utf-8")


@pytest.fixture
def repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    root = tmp_path / "repo"
    (root / ".claude" / "agents").mkdir(parents=True)
    (root / ".claude" / "agents" / "company-review.md").write_text(SPEC, encoding="utf-8")
    config = tmp_path / "config"
    slug = re.sub(r"[^A-Za-z0-9]", "-", str(root.resolve()))
    project = config / "projects" / slug
    run_dir = project / "session-1" / "subagents"
    _write(run_dir / f"agent-{RUN_ID}.jsonl", _rows())
    (run_dir / f"agent-{RUN_ID}.meta.json").write_text(json.dumps({"agentType": "company-review", "description": "t"}))
    _write(project / f"{SESSION_ID}.jsonl", _rows())
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(config))
    monkeypatch.setenv("CLUEFIN_CACHE_DIR", str(tmp_path / "no-cache"))
    monkeypatch.chdir(root)
    # `git log` reads whatever repository GIT_DIR points at (a pre-push hook sets it): pin the history.
    history = (
        ("bbb2222", datetime.fromisoformat("2026-11-09T00:00:00+00:00"), frozenset({"company-review.md"})),
        ("aaa1111", datetime.fromisoformat("2026-11-07T00:00:00+00:00"), frozenset({"company-review.md"})),
    )
    monkeypatch.setattr(audit_cli, "_agents_history", lambda _root: history)
    return root


def _json(capsys: pytest.CaptureFixture[str]) -> dict:
    return json.loads(capsys.readouterr().out)


def test_runs_lists_the_subagent_run(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    run_audit(["runs", "--json"])
    payload = _json(capsys)
    assert payload["count"] == 1
    row = payload["runs"][0]
    assert (row["run"], row["agent"], row["cli_calls"]) == (RUN_ID, "company-review", 3)
    # The agent file as of the run's start, not the commit made after it.
    assert row["agent_commit"] == "aaa1111"


def test_runs_filters_by_agent(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    run_audit(["runs", "--agent", "market-scan", "--json"])
    assert _json(capsys)["count"] == 0


def test_check_finds_missing_required_and_duplicate(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    run_audit(["check", "--run", RUN_ID, "--json"])
    payload = _json(capsys)
    assert payload["main"] == "005930"
    types = {(f["type"], f.get("command")) for f in payload["findings"]}
    assert ("missing_main", "kis stock opinion-summary") in types
    assert ("missing_each", "dart financial-summary") in types
    assert any(t == "duplicate" for t, _ in types)
    # The continued call kept its flags, so it is not reported as missing.
    assert ("missing_each", "kis stock current-price") not in types


def test_check_session_slice_needs_a_code(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(CliError) as excinfo:
        run_audit(["check", "--session", SESSION_ID])
    assert excinfo.value.exit_code == EXIT_USAGE
    run_audit(["check", "--session", SESSION_ID, "--code", "005930", "--json"])
    assert _json(capsys)["main"] == "005930"


def test_trace_cuts_each_output(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    run_audit(["trace", "--run", RUN_ID, "--max-chars", "10", "--json"])
    payload = _json(capsys)
    call = payload["calls"][1]
    assert call["args"] == {"stock-code": "005930", "json": "true"}
    assert len(call["output"]) == 10
    assert call["output_chars"] > 10


def test_report_groups_runs_by_agent_and_version(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    run_audit(["report", "--json"])
    groups = _json(capsys)["groups"]
    assert [(g["agent"], g["agent_commit"], len(g["runs"])) for g in groups] == [("company-review", "aaa1111", 1)]
    assert any(key.startswith("missing_main") for key in groups[0]["findings"])


@pytest.mark.parametrize(
    "argv",
    [[], ["nope"], ["check"], ["check", "--run", "missing"], ["check", "--session", "missing", "--code", "005930"]],
)
def test_usage_errors(repo: Path, argv: list[str]) -> None:
    with pytest.raises(CliError) as excinfo:
        run_audit(argv)
    assert excinfo.value.exit_code == EXIT_USAGE


def test_outside_the_repository_is_a_usage_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    with pytest.raises(CliError, match=r"\.claude/agents"):
        run_audit(["runs"])
