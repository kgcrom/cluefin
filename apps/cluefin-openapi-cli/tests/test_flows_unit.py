"""Pure-function tests for `flows.py` — synthetic rows, no KIS calls.

Rows are passed **newest first**, matching every KIS endpoint behind `kis stock flow-summary`
(measured on three stocks, 2026-11-11 — see the module docstring).
"""

from __future__ import annotations

import pytest

from cluefin_openapi_cli import flows


def _row(date: str, pbmn: str | None, turnover: str = "1000") -> dict:
    return {"date": date, "pbmn": pbmn, "turnover": turnover}


def test_to_number_treats_blank_and_none_as_missing() -> None:
    assert flows.to_number(None) is None
    assert flows.to_number("") is None
    assert flows.to_number("   ") is None
    assert flows.to_number("0") == 0.0
    assert flows.to_number("1234.5") == pytest.approx(1234.5)


def test_window_flow_stats_sums_net_buy_and_scales_pbmn() -> None:
    rows = [_row("3", "10"), _row("2", "20"), _row("1", "-5")]
    result = flows.window_flow_stats(
        rows, pbmn_field="pbmn", pbmn_scale=2, turnover_field="turnover", turnover_scale=1, window=3
    )
    # (10+20-5) * 2 = 50
    assert result["net_buy_amount"] == pytest.approx(50.0)
    assert result["window_turnover"] == pytest.approx(3000.0)
    assert result["pct_of_window_turnover"] == pytest.approx(50.0 / 3000.0 * 100)
    assert result["net_buy_day_ratio"] == pytest.approx(2 / 3 * 100)
    assert result["rows_used"] == 3
    assert result["rows_requested"] == 3


def test_window_flow_stats_only_uses_the_first_window_rows() -> None:
    rows = [_row(str(i), "10") for i in range(10)]
    result = flows.window_flow_stats(
        rows, pbmn_field="pbmn", pbmn_scale=1, turnover_field="turnover", turnover_scale=1, window=3
    )
    assert result["rows_used"] == 3
    assert result["net_buy_amount"] == pytest.approx(30.0)


def test_window_flow_stats_skips_missing_rows_without_substituting_zero() -> None:
    rows = [_row("3", None), _row("2", "20"), _row("1", "10")]
    result = flows.window_flow_stats(
        rows, pbmn_field="pbmn", pbmn_scale=1, turnover_field="turnover", turnover_scale=1, window=3
    )
    assert result["net_buy_amount"] == pytest.approx(30.0)
    assert result["rows_used"] == 2


def test_window_flow_stats_is_null_when_nothing_usable() -> None:
    rows = [_row("1", None)]
    result = flows.window_flow_stats(
        rows, pbmn_field="pbmn", pbmn_scale=1, turnover_field="turnover", turnover_scale=1, window=1
    )
    assert result["net_buy_amount"] is None
    assert result["net_buy_day_ratio"] is None
    assert result["rows_used"] == 0


def test_current_streak_counts_consecutive_same_sign_days_from_the_most_recent_row() -> None:
    # newest first: +, +, +, -, -
    rows = [_row("5", "10"), _row("4", "5"), _row("3", "1"), _row("2", "-3"), _row("1", "-1")]
    assert flows.current_streak(rows, "pbmn") == 3


def test_current_streak_is_negative_for_a_net_sell_run() -> None:
    rows = [_row("2", "-10"), _row("1", "-5")]
    assert flows.current_streak(rows, "pbmn") == -2


def test_current_streak_stops_at_a_missing_row() -> None:
    rows = [_row("3", "10"), _row("2", None), _row("1", "10")]
    assert flows.current_streak(rows, "pbmn") == 1


def test_current_streak_is_none_when_most_recent_row_is_missing_or_empty() -> None:
    assert flows.current_streak([], "pbmn") is None
    assert flows.current_streak([_row("1", None)], "pbmn") is None


def test_level_window_stats_reports_latest_and_change_from_window_start() -> None:
    rows = [{"date": "3", "v": "120"}, {"date": "2", "v": "110"}, {"date": "1", "v": "100"}]
    result = flows.level_window_stats(rows, value_field="v", scale=1, window=3)
    assert result["latest"] == pytest.approx(120.0)
    assert result["window_start"] == pytest.approx(100.0)
    assert result["change_pct"] == pytest.approx(20.0)
    assert result["rows_used"] == 3


def test_level_window_stats_applies_scale_to_latest_and_window_start_only() -> None:
    rows = [{"date": "2", "v": "20"}, {"date": "1", "v": "10"}]
    result = flows.level_window_stats(rows, value_field="v", scale=100, window=2)
    assert result["latest"] == pytest.approx(2000.0)
    assert result["window_start"] == pytest.approx(1000.0)
    assert result["change_pct"] == pytest.approx(100.0)  # unaffected by scale


def test_level_window_stats_empty_rows_is_all_null() -> None:
    result = flows.level_window_stats([], value_field="v", scale=1, window=5)
    assert result == {"latest": None, "window_start": None, "change_pct": None, "rows_used": 0, "rows_requested": 5}


def test_short_selling_stats_latest_window_avg_and_percentile() -> None:
    # newest first, values 10..1
    rows = [{"ratio": str(v)} for v in range(10, 0, -1)]
    result = flows.short_selling_stats(rows, ratio_field="ratio", window=5)
    assert result["latest"] == pytest.approx(10.0)
    assert result["window_avg"] == pytest.approx((10 + 9 + 8 + 7 + 6) / 5)
    # latest (10) is the max of the full population -> top percentile
    assert result["percentile"] == pytest.approx(90.0)
    assert result["rows_used"] == 5


def test_short_selling_stats_is_null_when_every_row_is_missing() -> None:
    result = flows.short_selling_stats([{"ratio": None}], ratio_field="ratio", window=5)
    assert result["latest"] is None
    assert result["percentile"] is None


def test_program_window_stats_sums_and_scales() -> None:
    rows = [{"pbmn": "10"}, {"pbmn": "-4"}, {"pbmn": "2"}]
    result = flows.program_window_stats(rows, pbmn_field="pbmn", scale=10, window=3)
    assert result["net_buy_amount"] == pytest.approx(80.0)
    assert result["rows_used"] == 3


def test_program_window_stats_only_uses_requested_window() -> None:
    rows = [{"pbmn": "10"}, {"pbmn": "10"}, {"pbmn": "10"}]
    result = flows.program_window_stats(rows, pbmn_field="pbmn", scale=1, window=2)
    assert result["net_buy_amount"] == pytest.approx(20.0)
    assert result["rows_used"] == 2
