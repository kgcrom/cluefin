from __future__ import annotations

from datetime import date
from types import SimpleNamespace

import pytest
from cluefin_openapi.ecos import EcosAuthenticationError, EcosPage, EcosQueryTimeoutError, StatisticObservation

from cluefin_openapi_cli import macro
from cluefin_openapi_cli.errors import EXIT_BROKER, EXIT_CREDENTIALS, CliError
from cluefin_openapi_cli.handlers import ecos as handlers


def test_period_date_reads_every_cycle() -> None:
    assert macro.period_date("20261030") == date(2026, 10, 30)
    assert macro.period_date("202609") == date(2026, 9, 1)
    assert macro.period_date("2026Q3") == date(2026, 7, 1)
    assert macro.period_date("2026") == date(2026, 1, 1)


def test_months_before_clamps_to_month_end() -> None:
    assert macro.months_before(date(2026, 3, 31), 1) == date(2026, 2, 28)
    assert macro.months_before(date(2024, 3, 31), 1) == date(2024, 2, 29)
    assert macro.months_before(date(2026, 1, 15), 12) == date(2025, 1, 15)


def test_fetch_window_adds_a_year_and_another_for_yoy() -> None:
    today = date(2026, 11, 1)
    rates = next(s for s in macro.SERIES if s.key == "ktb_3y")
    cpi = next(s for s in macro.SERIES if s.key == "cpi_yoy")
    gdp = next(s for s in macro.SERIES if s.key == "gdp_qoq")
    assert macro.fetch_window(rates, today, 10) == ("20151101", "20261101")
    assert macro.fetch_window(cpi, today, 10) == ("201411", "202611")
    assert macro.fetch_window(gdp, today, 10) == ("2015Q4", "2026Q4")


def test_year_over_year_needs_the_same_month_a_year_earlier() -> None:
    points = [("202501", 100.0), ("202502", 100.0), ("202601", 103.0), ("202602", 99.0), ("202603", 101.0)]
    assert macro.year_over_year(points) == [("202601", pytest.approx(3.0)), ("202602", pytest.approx(-1.0))]


def test_summarize_changes_and_percentile() -> None:
    # 13 monthly points 1..13: latest 13 is the maximum of the 1-year window.
    points = [(f"{2025 + (m - 1) // 12}{(m - 1) % 12 + 1:02d}", float(m)) for m in range(1, 14)]
    summary = macro.summarize(points, window_years=1, cycle="M")
    assert summary is not None
    assert (summary["value"], summary["as_of"]) == (13.0, "202601")
    assert summary["change"] == {"1m": 1.0, "3m": 3.0, "1y": 12.0}
    # Window: after 2025-01-01 → 202502..202601 = 12 points, all ≤ 13.
    assert (summary["observations"], summary["percentile"], summary["min"], summary["max"]) == (12, 100.0, 2.0, 13.0)


def test_summarize_daily_uses_last_value_on_or_before_and_quarterly_labels() -> None:
    daily = [("20260828", 3.0), ("20260929", 3.2), ("20260930", 3.4), ("20261030", 3.5)]
    summary = macro.summarize(daily, window_years=10)
    assert summary is not None
    # 1m before 2026-10-30 is 2026-09-30; 3m is 2026-07-30 — nothing on or before it.
    assert summary["change"] == {"1m": pytest.approx(0.1), "3m": None, "1y": None}

    quarterly = [("2025Q3", 1.4), ("2026Q2", 0.6), ("2026Q3", 1.0)]
    q_summary = macro.summarize(quarterly, window_years=10, cycle="Q")
    assert q_summary is not None
    assert q_summary["change"] == {"1q": pytest.approx(0.4), "1y": pytest.approx(-0.4)}


def test_align_subtracts_only_shared_periods() -> None:
    left = [("20261028", 4.0), ("20261029", 4.1), ("20261030", 4.2)]
    right = [("20261028", 3.5), ("20261030", 3.6)]
    assert macro.align(left, right) == [("20261028", 0.5), ("20261030", pytest.approx(0.6))]


def _points_for(series: macro.MacroSeries) -> list[macro.Point]:
    if series.cycle == "D":
        return [("20261029", 3.0), ("20261030", 3.1)]
    if series.cycle == "Q":
        return [("2026Q2", 0.6), ("2026Q3", 1.0)]
    return [("202509", 100.0), ("202609", 102.0)]


def test_snapshot_reports_every_series_and_spreads() -> None:
    result = macro.snapshot(_points_for, window_years=10)

    keys = [row["key"] for row in result["indicators"]]
    assert keys == [series.key for series in macro.SERIES]
    cpi = next(row for row in result["indicators"] if row["key"] == "cpi_yoy")
    assert (cpi["value"], cpi["as_of"], cpi["transform"]) == (2.0, "202609", "yoy")
    assert [row["key"] for row in result["derived"]] == ["term_spread", "credit_spread_aa", "credit_spread_bbb"]
    assert result["derived"][0]["value"] == 0.0
    assert result["missing"] == []


def test_snapshot_records_a_failed_or_ambiguous_series_and_keeps_going() -> None:
    def fetch(series: macro.MacroSeries) -> list[macro.Point]:
        if series.key == "ktb_10y":
            raise EcosQueryTimeoutError("60초", code="ERROR-400")
        if series.key == "ccsi":
            return [("202609", 100.0), ("202609", 90.0)]
        return _points_for(series)

    result = macro.snapshot(fetch, window_years=10)
    missing = {row["key"]: row["error"] for row in result["missing"]}
    assert set(missing) == {"ktb_10y", "ccsi"}
    assert "EcosQueryTimeoutError" in missing["ktb_10y"]
    assert "several rows" in missing["ccsi"]
    # The term spread needs the 10y leg, so it is left out rather than computed from one side.
    assert "term_spread" not in [row["key"] for row in result["derived"]]


def test_snapshot_lets_a_key_error_through() -> None:
    def fetch(series: macro.MacroSeries) -> list[macro.Point]:
        raise EcosAuthenticationError("인증키", code="INFO-100")

    with pytest.raises(EcosAuthenticationError):
        macro.snapshot(fetch, window_years=10)


class _Session:
    def __init__(self, *, sample: bool = False, empty: bool = False) -> None:
        self.calls: list[tuple] = []

        def search(stat_code, cycle, start, end, item_codes):
            self.calls.append((stat_code, cycle, start, end, item_codes))
            if empty:
                rows = []
            else:
                series = next(s for s in macro.SERIES if (s.stat_code, s.item_codes) == (stat_code, item_codes))
                rows = [
                    {"STAT_CODE": stat_code, "STAT_NAME": "x", "TIME": time, "DATA_VALUE": str(value)}
                    for time, value in _points_for(series)
                ]
                rows.append(
                    {"STAT_CODE": stat_code, "STAT_NAME": "x", "TIME": rows[-1]["TIME"] + "9", "DATA_VALUE": ""}
                )
            return EcosPage[StatisticObservation].model_validate({"list_total_count": len(rows), "row": rows})

        self._client = SimpleNamespace(is_sample=sample, statistic_search=SimpleNamespace(search=search))

    def get_ecos(self):
        return self._client


def test_handler_calls_each_series_once_and_drops_blank_values(monkeypatch) -> None:
    monkeypatch.setattr(handlers, "_today", lambda: date(2026, 11, 1))
    session = _Session()

    result = handlers.handle_macro_snapshot({}, session)

    assert len(session.calls) == len(macro.SERIES)
    assert ("817Y002", "D", "20151101", "20261101", ("010200000",)) in session.calls
    assert result["run_date"] == "2026-11-01"
    assert result["window_years"] == 10
    assert result["missing"] == []
    assert any("as_of" in note for note in result["notes"])


def test_handler_refuses_the_sample_key() -> None:
    session = _Session(sample=True)
    with pytest.raises(CliError) as caught:
        handlers.handle_macro_snapshot({}, session)
    assert caught.value.exit_code == EXIT_CREDENTIALS
    assert session.calls == []


def test_handler_fails_when_nothing_came_back(monkeypatch) -> None:
    monkeypatch.setattr(handlers, "_today", lambda: date(2026, 11, 1))
    with pytest.raises(CliError) as caught:
        handlers.handle_macro_snapshot({}, _Session(empty=True))
    assert caught.value.exit_code == EXIT_BROKER
    assert len(caught.value.data["missing"]) == len(macro.SERIES)
