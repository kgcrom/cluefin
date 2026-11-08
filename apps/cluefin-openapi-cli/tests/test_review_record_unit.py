from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

import pytest

from cluefin_openapi_cli.errors import EXIT_USAGE, CliError
from cluefin_openapi_cli.review import paths
from cluefin_openapi_cli.review.cli import run_review
from cluefin_openapi_cli.review.record import record_verdict, validate

DAY = date(2026, 11, 8)


def _verdict(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "stock_code": "214320",
        "stock_name": "이노션",
        "verdict": "watch",
        "confidence": "medium",
        "horizon_days": 60,
        "reference_price": {"close": 17760, "date": "2026-11-06", "adjusted": False},
        "trigger": {"entry_above": 18510, "exit_below": 16730, "recheck_on": "2026-11-14"},
        "invalidation": ["주간 종가 17,020원 이탈"],
        "scenario": {"bull": 0.29},
    }
    base.update(overrides)
    return base


def _write(folder: Path, verdict: dict[str, Any]) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "verdict.json").write_text(json.dumps(verdict, ensure_ascii=False), encoding="utf-8")
    return folder


def _lines(root: Path) -> list[dict[str, Any]]:
    return [json.loads(x) for x in (root / "verdicts.jsonl").read_text(encoding="utf-8").splitlines()]


# --- research_root ---------------------------------------------------------------------------------------------


def test_research_root_env_wins(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(paths.RESEARCH_DIR_ENV, str(tmp_path / "elsewhere"))
    assert paths.research_root(tmp_path) == tmp_path / "elsewhere"


def test_research_root_is_main_checkout_from_subfolder(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(paths.RESEARCH_DIR_ENV, raising=False)
    (tmp_path / ".git").mkdir()
    sub = tmp_path / "apps" / "x"
    sub.mkdir(parents=True)
    assert paths.research_root(sub) == tmp_path / "research"


def test_research_root_from_worktree_points_at_main_checkout(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(paths.RESEARCH_DIR_ENV, raising=False)
    main = tmp_path / "repo"
    admin = main / ".git" / "worktrees" / "w1"
    admin.mkdir(parents=True)
    (admin / "commondir").write_text("../..\n", encoding="utf-8")
    worktree = main / ".claude" / "worktrees" / "w1"
    worktree.mkdir(parents=True)
    (worktree / ".git").write_text(f"gitdir: {admin}\n", encoding="utf-8")
    assert paths.research_root(worktree) == main.resolve() / "research"


def test_research_root_outside_git_is_usage_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(paths.RESEARCH_DIR_ENV, raising=False)
    monkeypatch.setattr(paths, "_common_git_dir", lambda start: None)
    with pytest.raises(CliError) as exc:
        paths.research_root(tmp_path)
    assert exc.value.exit_code == EXIT_USAGE


# --- validate --------------------------------------------------------------------------------------------------


def test_valid_watch_has_no_problems() -> None:
    assert validate(_verdict()) == []


def test_validate_lists_every_problem_at_once() -> None:
    problems = validate(
        _verdict(stock_code=30000, verdict="maybe", confidence="mid", horizon_days=0, reference_price={})
    )
    assert len(problems) == 5
    assert any("6-digit string" in p for p in problems)


def test_watch_needs_a_trigger_price() -> None:
    assert any("trigger" in p for p in validate(_verdict(trigger={"recheck_on": "2026-11-14"})))
    assert validate(_verdict(trigger={"exit_below": 16730})) == []


@pytest.mark.parametrize("label", ["buy", "sell"])
def test_buy_sell_need_target_and_stop(label: str) -> None:
    problems = validate(_verdict(verdict=label, trigger=None))
    assert problems == [f"{label} needs target (> 0)", f"{label} needs stop (> 0)"]
    assert validate(_verdict(verdict=label, trigger=None, target=21000, stop=16000)) == []


def test_bool_is_not_a_price() -> None:
    assert validate(_verdict(trigger={"entry_above": True}))


# --- record_verdict --------------------------------------------------------------------------------------------


def test_record_appends_normalized_line(tmp_path: Path) -> None:
    root = tmp_path / "research"
    done = record_verdict(
        _write(tmp_path / "run", _verdict()), root=root, source="company-review", report=None, today=DAY
    )
    assert done.file == root / "verdicts.jsonl"
    (line,) = _lines(root)
    assert line["id"] == "214320-20261106-1"
    assert line["recorded_at"] == "2026-11-08"
    assert line["trigger"] == {"entry_above": 18510, "exit_below": 16730, "recheck_on": "2026-11-14"}
    assert line["target"] is None
    assert "scenario" not in line


def test_same_stock_and_date_gets_next_id_and_keeps_earlier_line(tmp_path: Path) -> None:
    root = tmp_path / "research"
    src = _write(tmp_path / "run", _verdict())
    record_verdict(src, root=root, source="main", report=None, today=DAY)
    record_verdict(src, root=root, source="main", report=None, today=DAY)
    assert [x["id"] for x in _lines(root)] == ["214320-20261106-1", "214320-20261106-2"]


def test_report_stored_relative_to_research(tmp_path: Path) -> None:
    root = tmp_path / "research"
    html = root / "reports" / "innocean-214320-report-2026-11-08.html"
    html.parent.mkdir(parents=True)
    html.write_text("<html></html>", encoding="utf-8")
    src = _write(tmp_path / "run", _verdict()) / "verdict.json"
    record_verdict(src, root=root, source="main", report=html, today=DAY)
    assert _lines(root)[0]["report"] == "reports/innocean-214320-report-2026-11-08.html"


def test_report_outside_research_refused(tmp_path: Path) -> None:
    html = tmp_path / "docs" / "r.html"
    html.parent.mkdir()
    html.write_text("x", encoding="utf-8")
    with pytest.raises(CliError) as exc:
        record_verdict(
            _write(tmp_path / "run", _verdict()), root=tmp_path / "research", source="main", report=html, today=DAY
        )
    assert exc.value.exit_code == EXIT_USAGE
    assert not (tmp_path / "research" / "verdicts.jsonl").exists()


def test_invalid_verdict_writes_nothing(tmp_path: Path) -> None:
    root = tmp_path / "research"
    with pytest.raises(CliError) as exc:
        record_verdict(
            _write(tmp_path / "run", _verdict(trigger=None)), root=root, source="main", report=None, today=DAY
        )
    assert exc.value.data["problems"]
    assert not root.exists()


@pytest.mark.parametrize("content", ["{not json", "[1, 2]"])
def test_bad_file_is_usage_error(tmp_path: Path, content: str) -> None:
    src = tmp_path / "verdict.json"
    src.write_text(content, encoding="utf-8")
    with pytest.raises(CliError) as exc:
        record_verdict(src, root=tmp_path / "research", source="main", report=None, today=DAY)
    assert exc.value.exit_code == EXIT_USAGE


def test_unknown_source_refused(tmp_path: Path) -> None:
    with pytest.raises(CliError):
        record_verdict(_write(tmp_path / "run", _verdict()), root=tmp_path / "r", source="bot", report=None, today=DAY)


# --- CLI -------------------------------------------------------------------------------------------------------


def test_cli_record_uses_research_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv(paths.RESEARCH_DIR_ENV, str(tmp_path / "research"))
    run_review(["record", "--from", str(_write(tmp_path / "run", _verdict())), "--json"])
    out = json.loads(capsys.readouterr().out)
    assert out["record"]["id"] == "214320-20261106-1"
    assert len(_lines(tmp_path / "research")) == 1


def test_cli_record_needs_from() -> None:
    with pytest.raises(CliError) as exc:
        run_review(["record", "--json"])
    assert exc.value.exit_code == EXIT_USAGE
