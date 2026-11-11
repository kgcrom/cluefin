from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import pytest

from cluefin_openapi_cli.cache import store
from cluefin_openapi_cli.errors import CliError
from cluefin_openapi_cli.review import due as rd
from cluefin_openapi_cli.review import paths
from cluefin_openapi_cli.review.cli import run_review

TODAY = date(2026, 11, 11)


def _record(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "id": "214320-20261102-1",
        "stock_code": "214320",
        "stock_name": "이노션",
        "recorded_at": "2026-11-02",
        "verdict": "watch",
        "horizon_days": 20,
        "reference_price": {"close": 100, "date": "2026-11-02", "adjusted": False},
        "trigger": {"entry_above": 105, "exit_below": 95, "recheck_on": None},
        "target": None,
        "stop": None,
    }
    base.update(overrides)
    return base


def _days(start: date, n: int) -> list[date]:
    return [start + timedelta(days=i) for i in range(n)]


def _store(code: str, closes: list[float], *, start: date = date(2026, 11, 2), settle_month: int | None = 12) -> Any:
    conn = store.open_store(":memory:")
    conn.execute(
        "INSERT INTO company (code, name, market, corp_code, settle_month) VALUES (?, ?, 'KOSPI', ?, ?)",
        [code, code, f"00{code}", settle_month],
    )
    for day, close in zip(_days(start, len(closes)), closes, strict=True):
        conn.execute("INSERT INTO ohlcv (code, date, close, adj_factor) VALUES (?, ?, ?, 1.0)", [code, day, close])
    return conn


# --- latest_per_stock ----------------------------------------------------------------------------------------


def test_latest_per_stock_keeps_the_newest_record() -> None:
    records = [
        _record(id="214320-20261001-1", recorded_at="2026-10-01", verdict="watch"),
        _record(id="214320-20261102-1", recorded_at="2026-11-02", verdict="buy"),
        _record(stock_code="030000", id="030000-20261101-1", recorded_at="2026-11-01"),
    ]
    latest = rd.latest_per_stock(records)
    assert {r["stock_code"]: r["verdict"] for r in latest} == {"214320": "buy", "030000": "watch"}


# --- due() reasons --------------------------------------------------------------------------------------------


def test_crossed_is_a_reason() -> None:
    conn = _store("214320", [100, 103, 106, 110])
    rows, as_of = rd.tracked_rows(conn, [_record()], codes=[])
    payload = rd.due(rows, as_of, days=14, today=TODAY)
    assert payload["due_count"] == 1
    assert payload["due"][0]["due_reasons"][0]["type"] == "crossed"
    assert payload["by_reason"] == {"crossed": 1}


def test_recheck_passed_and_recheck_within() -> None:
    conn = _store("214320", [100, 101])
    passed = _record(trigger={"entry_above": 999, "exit_below": 1, "recheck_on": "2026-11-10"})
    within = _record(
        stock_code="030000",
        id="030000-20261102-1",
        trigger={"entry_above": 999, "exit_below": 1, "recheck_on": "2026-11-20"},
    )
    conn.execute("INSERT INTO company (code, name, market, corp_code) VALUES ('030000', '030000', 'KOSPI', '00030000')")
    for day, close in zip(_days(date(2026, 11, 2), 2), [100, 101], strict=True):
        conn.execute("INSERT INTO ohlcv (code, date, close, adj_factor) VALUES ('030000', ?, ?, 1.0)", [day, close])
    rows, as_of = rd.tracked_rows(conn, [passed, within], codes=[])
    payload = rd.due(rows, as_of, days=14, today=TODAY)
    reasons_by_code = {row["stock_code"]: [r["type"] for r in row["due_reasons"]] for row in payload["due"]}
    assert "recheck_passed" in reasons_by_code["214320"]
    assert "recheck_within" in reasons_by_code["030000"]


def test_horizon_ending_within_days() -> None:
    conn = _store("214320", [100, 101, 102], start=date(2026, 10, 20))
    record = _record(
        recorded_at="2026-10-20",
        reference_price={"close": 100, "date": "2026-10-20", "adjusted": False},
        horizon_days=4,
    )
    rows, as_of = rd.tracked_rows(conn, [record], codes=[])
    payload = rd.due(rows, as_of, days=14, today=TODAY)
    assert payload["due"][0]["due_reasons"][0]["type"] == "horizon_ending"


def test_no_reason_is_only_counted() -> None:
    conn = _store("214320", [100, 100, 100])
    record = _record(
        horizon_days=60,
        trigger={"entry_above": 999999, "exit_below": 1, "recheck_on": "2027-06-01"},
    )
    rows, as_of = rd.tracked_rows(conn, [record], codes=[])
    payload = rd.due(rows, as_of, days=14, today=TODAY)
    assert payload["due_count"] == 0
    assert payload["watched"] == 1


def test_codes_filter() -> None:
    conn = _store("214320", [100, 101])
    rows, _ = rd.tracked_rows(conn, [_record()], codes=["030000"])
    assert rows == []


# --- next_periodic_deadline ------------------------------------------------------------------------------------


def test_next_periodic_deadline_calendar_year_filer() -> None:
    result = rd.next_periodic_deadline(12, TODAY)
    # 2026-09-30 + 45 days is Saturday 2026-11-14, so the report is due the Monday.
    assert result == {"kind": "분기보고서", "period_end": "2026-09-30", "deadline": "2026-11-16", "days_left": 5}


def test_next_periodic_deadline_on_a_weekday_is_not_moved() -> None:
    # FY2026 ends Thursday 2026-12-31; 90 days later is Wednesday 2027-03-31.
    result = rd.next_periodic_deadline(12, date(2027, 1, 4))
    assert result["kind"] == "사업보고서"
    assert result["deadline"] == "2027-03-31"


def test_next_periodic_deadline_is_the_soonest_future_one() -> None:
    # The day right after a deadline: the next one should be picked, never a past one.
    result = rd.next_periodic_deadline(12, date(2026, 11, 15))
    assert date.fromisoformat(result["deadline"]) >= date(2026, 11, 15)


@pytest.mark.parametrize("month", list(range(1, 13)))
def test_next_periodic_deadline_always_returns_a_future_deadline(month: int) -> None:
    result = rd.next_periodic_deadline(month, TODAY)
    assert date.fromisoformat(result["deadline"]) >= TODAY
    assert result["kind"] in {"분기보고서", "반기보고서", "사업보고서"}


def test_next_periodic_deadline_rejects_bad_month() -> None:
    with pytest.raises(ValueError, match="settle_month"):
        rd.next_periodic_deadline(13, TODAY)


# --- gather_events ----------------------------------------------------------------------------------------------


class _FakeRunner:
    def __init__(
        self, schedule_rows: dict[str, list[dict[str, Any]]], disclosures: dict[str, list[dict[str, Any]]]
    ) -> None:
        self.calls: list[list[str]] = []
        self._schedule_rows = schedule_rows
        self._disclosures = disclosures

    def __call__(self, argv: list[str]) -> tuple[int, str, str]:
        self.calls.append(argv)
        if argv[:2] == ["kis", "schedule"]:
            rows = self._schedule_rows.get(argv[2], [])
            if "--stock-code" in argv:
                rows = [r for r in rows if r["sht_cd"] == argv[argv.index("--stock-code") + 1]]
            return 0, json.dumps({"data": rows}), ""
        if argv[:2] == ["dart", "disclosure-search"]:
            corp = argv[argv.index("--corp-code") + 1]
            return 0, json.dumps({"result": {"list": self._disclosures.get(corp, [])}}), ""
        return 1, "{}", "unexpected call"


def test_gather_events_filters_schedule_rows_by_code_and_flags_truncation() -> None:
    conn = _store("214320", [100, 101])
    rows, _ = rd.tracked_rows(conn, [_record()], codes=[])
    schedule_rows = {
        "dividend": [{"sht_cd": "214320", "record_date": "20261112"}, {"sht_cd": "999999", "record_date": "20261112"}],
        "listing": [{"sht_cd": c, "record_date": "20261112"} for c in [f"{i:06d}" for i in range(100)]],
    }
    runner = _FakeRunner(schedule_rows, disclosures={"00214320": [{"report_nm": "분기보고서", "rcept_no": "1"}]})
    events = rd.gather_events(runner, conn, rows, days=14, today=TODAY)
    assert events["schedule"]["by_code"]["214320"] == [
        {"command": "dividend", "sht_cd": "214320", "record_date": "20261112"}
    ]
    # `listing` came back at the 100-row cap, so it is asked again for the one open stock instead of being trusted.
    assert events["schedule"]["refetched_per_stock"] == ["listing"]
    assert events["schedule"]["possibly_truncated"] == []
    assert events["schedule"]["failed"] == []
    assert len(runner.calls) == len(rd.SCHEDULE_COMMANDS) + 1 + 1  # + per-stock listing + disclosure-search
    assert events["disclosures"]["214320"]["count"] == 1
    assert events["disclosures"]["214320"]["recent_titles"] == ["분기보고서"]
    assert events["next_periodic_deadline"]["214320"]["kind"] == "분기보고서"


def test_gather_events_dart_status_013_is_zero_not_a_failure() -> None:
    # DART answers an empty window with status 013 and `list: null`, not an empty list (confirmed 2026-11-11 real call).
    conn = _store("214320", [100, 101])
    rows, _ = rd.tracked_rows(conn, [_record()], codes=[])

    def runner(argv: list[str]) -> tuple[int, str, str]:
        if argv[:2] == ["kis", "schedule"]:
            return 0, json.dumps({"data": []}), ""
        if argv[:2] == ["dart", "disclosure-search"]:
            return (
                0,
                json.dumps({"result": {"status": "013", "message": "조회된 데이타가 없습니다.", "list": None}}),
                "",
            )
        return 1, "{}", "unexpected call"

    events = rd.gather_events(runner, conn, rows, days=14, today=TODAY)
    assert events["disclosures"]["214320"] == {"count": 0, "recent_titles": [], "since": "20261102"}


def test_gather_events_only_covers_open_rows() -> None:
    conn = _store("214320", [100, 200, 200, 200, 200])  # crosses entry_above immediately then runs past horizon
    record = _record(horizon_days=2)
    rows, _ = rd.tracked_rows(conn, [record], codes=[])
    assert rows[0]["status"] == "closed"
    runner = _FakeRunner({}, {})
    events = rd.gather_events(runner, conn, rows, days=14, today=TODAY)
    assert events["open_codes"] == []
    assert runner.calls == []


def test_gather_events_missing_corp_code_is_a_reason() -> None:
    conn = store.open_store(":memory:")
    conn.execute("INSERT INTO company (code, name, market) VALUES ('214320', '이노션', 'KOSPI')")
    for day, close in zip(_days(date(2026, 11, 2), 2), [100, 101], strict=True):
        conn.execute("INSERT INTO ohlcv (code, date, close, adj_factor) VALUES ('214320', ?, ?, 1.0)", [day, close])
    rows, _ = rd.tracked_rows(conn, [_record()], codes=[])
    runner = _FakeRunner({}, {})
    events = rd.gather_events(runner, conn, rows, days=14, today=TODAY)
    assert events["disclosures"]["214320"]["reason"]
    assert events["next_periodic_deadline"]["214320"] is None


# --- CLI -----------------------------------------------------------------------------------------------------


def test_cli_due_dry_run_touches_nothing(capsys: pytest.CaptureFixture[str]) -> None:
    run_review(["due", "--days", "7", "--events", "true", "--dry-run", "--json"])
    out = json.loads(capsys.readouterr().out)
    assert out["dry_run"] is True


def test_cli_due_rejects_bad_days(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(paths.RESEARCH_DIR_ENV, str(tmp_path / "research"))
    with pytest.raises(CliError):
        run_review(["due", "--days", "nope", "--json"])


def test_cli_due_end_to_end(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "research"
    root.mkdir()
    (root / "verdicts.jsonl").write_text(json.dumps(_record()) + "\n", encoding="utf-8")
    db = tmp_path / "market.duckdb"
    conn = store.open_store(db)
    conn.execute("INSERT INTO company (code, name, market, corp_code) VALUES ('214320', '이노션', 'KOSPI', '00214320')")
    for day, close in zip(_days(date(2026, 11, 2), 4), [100, 103, 106, 110], strict=True):
        conn.execute("INSERT INTO ohlcv (code, date, close, adj_factor) VALUES ('214320', ?, ?, 1.0)", [day, close])
    conn.close()
    monkeypatch.setenv(paths.RESEARCH_DIR_ENV, str(root))
    monkeypatch.setenv(store.CACHE_DIR_ENV, str(tmp_path))
    run_review(["due", "--days", "14", "--json"])
    out = json.loads(capsys.readouterr().out)
    assert out["due_count"] == 1
    assert out["due"][0]["stock_code"] == "214320"


def test_a_full_market_wide_page_is_refetched_per_stock_and_finds_the_cut_row() -> None:
    conn = _store("214320", [100, 101])
    rows, _ = rd.tracked_rows(conn, [_record()], codes=[])
    others = [{"sht_cd": f"{i:06d}", "record_date": "20261112"} for i in range(100)]
    mine = {"sht_cd": "214320", "record_date": "20261120"}

    def runner(argv: list[str]) -> tuple[int, str, str]:
        if argv[:3] == ["kis", "schedule", "listing"]:
            # The market-wide reply stops at 100 rows and this stock's row is past the cut.
            return 0, json.dumps({"data": [mine] if "--stock-code" in argv else others}), ""
        if argv[:2] == ["kis", "schedule"]:
            return 0, json.dumps({"data": []}), ""
        return 0, json.dumps({"result": {"status": "013", "list": None}}), ""

    events = rd.gather_events(runner, conn, rows, days=14, today=TODAY)
    assert events["schedule"]["by_code"]["214320"] == [{"command": "listing", **mine}]


def test_a_failed_schedule_call_is_listed_not_read_as_no_events() -> None:
    conn = _store("214320", [100, 101])
    rows, _ = rd.tracked_rows(conn, [_record()], codes=[])

    def runner(argv: list[str]) -> tuple[int, str, str]:
        if argv[:3] == ["kis", "schedule", "dividend"]:
            return 3, json.dumps({"error": {"type": "CredentialsMissing"}}), ""
        if argv[:2] == ["kis", "schedule"]:
            return 0, json.dumps({"data": []}), ""
        return 4, "{}", ""

    events = rd.gather_events(runner, conn, rows, days=14, today=TODAY)
    assert events["schedule"]["failed"] == [{"command": "dividend", "exit_code": 3}]
    assert events["disclosures"]["214320"]["reason"] == "disclosure-search failed (exit 4)"


def test_disclosure_count_is_the_window_total_not_the_page_length() -> None:
    conn = _store("214320", [100, 101])
    rows, _ = rd.tracked_rows(conn, [_record()], codes=[])
    page = [{"report_nm": f"공시 {i}"} for i in range(100)]

    def runner(argv: list[str]) -> tuple[int, str, str]:
        if argv[:2] == ["kis", "schedule"]:
            return 0, json.dumps({"data": []}), ""
        return 0, json.dumps({"result": {"status": "000", "total_count": 240, "list": page}}), ""

    events = rd.gather_events(runner, conn, rows, days=14, today=TODAY)
    assert events["disclosures"]["214320"]["count"] == 240
    assert len(events["disclosures"]["214320"]["recent_titles"]) == 5


def test_a_verdict_the_cache_cannot_check_is_due_with_no_data() -> None:
    conn = _store("214320", [100, 101], start=date(2026, 11, 3))  # no bar on the 2026-11-02 reference date
    rows, cache_as_of = rd.tracked_rows(conn, [_record()], codes=[])
    payload = rd.due(rows, cache_as_of, days=14, today=TODAY)
    assert payload["by_reason"] == {"no_data": 1}


def test_blank_padding_rows_do_not_count_toward_the_page_cap() -> None:
    # `listing` pads a short reply to 100 rows with blank ones — that is not a cut-off page.
    conn = _store("214320", [100, 101])
    rows, _ = rd.tracked_rows(conn, [_record()], codes=[])
    padded = [{"sht_cd": "214320", "list_dt": "20261116"}] + [{"sht_cd": "", "list_dt": ""}] * 99
    runner = _FakeRunner({"listing": padded}, disclosures={})
    events = rd.gather_events(runner, conn, rows, days=14, today=TODAY)
    assert events["schedule"]["refetched_per_stock"] == []
    assert events["schedule"]["by_code"]["214320"] == [
        {"command": "listing", "sht_cd": "214320", "list_dt": "20261116"}
    ]
