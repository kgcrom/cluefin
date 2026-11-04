"""`band.py` — pure PER/PBR band math, no DART/KIS/cache I/O."""

from __future__ import annotations

import pytest

from cluefin_openapi_cli import band


def test_eps_bps_divides_by_shares() -> None:
    eps, bps = band.eps_bps(net_income_owners=100.0, equity_owners=1000.0, shares=10.0)
    assert eps == pytest.approx(10.0)
    assert bps == pytest.approx(100.0)


def test_eps_bps_propagates_none_without_zero_filling() -> None:
    assert band.eps_bps(None, 1000.0, 10.0) == (None, 100.0)
    assert band.eps_bps(100.0, None, 10.0) == (10.0, None)


@pytest.mark.parametrize("shares", [None, 0, -5])
def test_eps_bps_is_none_without_a_positive_share_count(shares) -> None:
    assert band.eps_bps(100.0, 1000.0, shares) == (None, None)


def test_quantiles_of_empty_series_is_none() -> None:
    assert band.quantiles([]) is None


def test_quantiles_matches_numpy_linear_interpolation() -> None:
    out = band.quantiles([0.9, 1.1, 1.5, 2.0])
    assert out == {"min": 0.9, "p25": 1.05, "median": 1.3, "p75": 1.625, "max": 2.0}


@pytest.mark.parametrize(
    ("day", "year"),
    [("2025-03-31", 2023), ("2025-04-01", 2024), ("20251231", 2024), ("2026-01-02", 2024)],
)
def test_trailing_fiscal_year_switches_on_april_first(day, year) -> None:
    assert band.trailing_fiscal_year(day) == year


def test_multiple_series_drops_years_with_no_per_share_value() -> None:
    bars = [("2025-06-01", 15000.0), ("2026-06-01", 18000.0), ("2027-06-01", 22000.0)]
    per_share = {2024: 10000.0, 2025: None}  # 2026 missing entirely, 2025 explicitly None

    rows = band.multiple_series(bars, per_share)

    assert [row["year"] for row in rows] == [2024]
    assert rows[0]["multiple"] == pytest.approx(1.5)


def test_multiple_series_drops_non_positive_close_or_per_share() -> None:
    bars = [("2024-05-01", 0.0), ("2024-06-01", -5.0), ("2024-07-01", 10.0)]
    per_share = {2023: -1.0}
    assert band.multiple_series(bars, per_share) == []

    per_share_ok = {2023: 5.0}
    rows = band.multiple_series(bars, per_share_ok)
    assert [row["date"] for row in rows] == ["2024-07-01"]


def test_band_reports_current_multiple_and_percentile_within_history() -> None:
    bars = [
        ("2024-06-01", 15000.0),
        ("2024-12-01", 20000.0),
        ("2025-06-01", 18000.0),
        ("2025-10-01", 22000.0),
    ]
    per_share_by_year = {2023: 10000.0, 2024: 20000.0}

    out = band.band(bars, per_share_by_year, current_close=22000.0, current_per_share=20000.0)

    assert out["n"] == 4
    assert out["quantiles"] == {"min": 0.9, "p25": 1.05, "median": 1.3, "p75": 1.625, "max": 2.0}
    assert out["current"] == pytest.approx(1.1)
    assert out["current_percentile"] == pytest.approx(50.0)


def test_band_with_no_current_inputs_is_null_without_an_error() -> None:
    out = band.band([("2024-06-01", 15000.0)], {2023: 10000.0}, current_close=None, current_per_share=None)
    assert out["current"] is None
    assert out["current_percentile"] is None
    assert out["n"] == 1


def test_band_with_no_history_still_computes_current() -> None:
    out = band.band([], {}, current_close=22000.0, current_per_share=20000.0)
    assert out["n"] == 0
    assert out["quantiles"] is None
    assert out["current"] == pytest.approx(1.1)
    assert out["current_percentile"] is None  # no series to rank against
