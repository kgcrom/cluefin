from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import pytest

from cluefin_openapi_cli.cache import store
from cluefin_openapi_cli.errors import CliError
from cluefin_openapi_cli.review import paths
from cluefin_openapi_cli.review.cli import run_review
from cluefin_openapi_cli.review.track import load_records, summarize, track

REF = date(2026, 11, 2)


def _days(n: int) -> list[date]:
    return [REF + timedelta(days=i) for i in range(n)]


def _record(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "id": "214320-20261102-1",
        "stock_code": "214320",
        "stock_name": "이노션",
        "verdict": "watch",
        "horizon_days": 3,
        "reference_price": {"close": 100, "date": REF.isoformat(), "adjusted": False},
        "trigger": {"entry_above": 105, "exit_below": 95, "recheck_on": None},
        "target": None,
        "stop": None,
    }
    base.update(overrides)
    return base


def _store(closes: list[float], *, index: list[float] | None = None, factors: list[float] | None = None) -> Any:
    conn = store.open_store(":memory:")
    conn.execute("INSERT INTO company (code, name, market) VALUES ('214320', '이노션', 'KOSPI')")
    for i, day in enumerate(_days(len(closes))):
        factor = factors[i] if factors else 1.0
        conn.execute(
            "INSERT INTO ohlcv (code, date, close, adj_factor) VALUES ('214320', ?, ?, ?)", [day, closes[i], factor]
        )
    for day, close in zip(_days(len(index or [])), index or [], strict=True):
        conn.execute("INSERT INTO ohlcv (code, date, close, adj_factor) VALUES ('U0001', ?, ?, 1.0)", [day, close])
    return conn


def test_entry_crossed_first_then_closed_with_excess() -> None:
    conn = _store([100, 103, 106, 110], index=[1000, 1010, 1020, 1050])
    (row,) = track(conn, [_record()])["verdicts"]
    assert row["status"] == "closed"
    assert row["first_cross"] == {"level": "entry_above", "on": "2026-11-04", "close": 106.0, "return_after_pct": 3.77}
    assert row["return_pct"] == 10.0
    assert row["index_return_pct"] == 5.0
    assert row["excess_pct"] == 5.0
    assert (row["max_up_pct"], row["max_down_pct"]) == (10.0, 3.0)


def test_exit_crossed_first() -> None:
    conn = _store([100, 94, 107, 100], index=[1, 1, 1, 1])
    (row,) = track(conn, [_record()])["verdicts"]
    assert row["first_cross"]["level"] == "exit_below"


def test_bars_past_horizon_are_ignored_and_short_history_is_open() -> None:
    conn = _store([100, 101, 102, 103, 200])
    (row,) = track(conn, [_record()])["verdicts"]
    assert row["as_of"] == "2026-11-05"
    assert row["first_cross"] is None
    (short,) = track(_store([100, 101]), [_record()])["verdicts"]
    assert (short["status"], short["days_seen"]) == ("open", 1)


def test_levels_scale_with_reference_day_factor() -> None:
    # A 2:1 split after the reference date halves the earlier factors; 105 on the reference scale is 52.5 adjusted.
    conn = _store([100, 102, 53, 54], factors=[0.5, 0.5, 1.0, 1.0])
    (row,) = track(conn, [_record()])["verdicts"]
    assert row["first_cross"]["level"] == "entry_above"
    assert row["first_cross"]["on"] == "2026-11-04"


def test_buy_uses_target_and_stop_and_sell_flips_direction() -> None:
    buy = _record(verdict="buy", trigger={}, target=110, stop=90)
    sell = _record(verdict="sell", trigger={}, target=90, stop=110)
    conn = _store([100, 111, 100, 100])
    rows = track(conn, [buy, sell])["verdicts"]
    assert [r["first_cross"]["level"] for r in rows] == ["target", "stop"]


def test_missing_reference_bar_is_no_data() -> None:
    conn = _store([100, 101], index=[1, 1])
    (row,) = track(conn, [_record(reference_price={"close": 100, "date": "2026-11-20", "adjusted": False})])["verdicts"]
    assert row["status"] == "no_data"
    assert row["cache_as_of"] == "2026-11-03"


def test_summary_groups_by_label() -> None:
    rows = [
        {"verdict": "watch", "status": "closed", "first_cross": {"level": "entry_above"}, "excess_pct": 4.0},
        {"verdict": "watch", "status": "closed", "first_cross": None, "excess_pct": -2.0},
        {"verdict": "watch", "status": "open", "first_cross": None},
        {"verdict": "buy", "status": "no_data"},
    ]
    out = summarize(rows)
    assert out["watch"] == {
        "count": 3,
        "closed": 2,
        "open": 1,
        "no_data": 0,
        "first_cross": {"entry_above": 1},
        "mean_excess_pct_closed": 1.0,
    }
    assert out["buy"]["mean_excess_pct_closed"] is None


def test_load_records_missing_file(tmp_path: Path) -> None:
    with pytest.raises(CliError):
        load_records(tmp_path / "verdicts.jsonl")


def test_cli_track_filters_by_code(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "research"
    root.mkdir()
    lines = [_record(), _record(id="030000-20261102-1", stock_code="030000")]
    (root / "verdicts.jsonl").write_text("".join(json.dumps(x) + "\n" for x in lines), encoding="utf-8")
    db = tmp_path / "market.duckdb"
    seed = _store([100, 101, 102, 103], index=[1, 1, 1, 1])
    seed.execute(f"ATTACH '{db}' AS f")
    seed.execute("COPY FROM DATABASE memory TO f")
    seed.close()
    monkeypatch.setenv(paths.RESEARCH_DIR_ENV, str(root))
    monkeypatch.setenv(store.CACHE_DIR_ENV, str(tmp_path))
    run_review(["track", "--code", "214320", "--json"])
    out = json.loads(capsys.readouterr().out)
    assert [r["id"] for r in out["verdicts"]] == ["214320-20261102-1"]
    assert out["summary"]["watch"]["closed"] == 1
