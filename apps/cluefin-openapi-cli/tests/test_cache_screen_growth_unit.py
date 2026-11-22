"""`cache screen` growth factors (cache/screen_growth.py)."""

from __future__ import annotations

from cluefin_openapi_cli.cache.screen_growth import growth_factors


def _years(values: dict[str, float], account: str = "당기순이익") -> dict[str, dict[str, float]]:
    return {year: {account: amount} for year, amount in values.items()}


def _panel(rows: dict[tuple[int, int], dict[str, tuple[float | None, float | None]]], latest: tuple[int, int]):
    return {"period": latest, "panel": rows}


def test_up_years_counts_back_until_a_drop_or_gap() -> None:
    years = _years({"2021": 10, "2022": 12, "2023": 11, "2024": 13, "2025": 20})
    assert growth_factors(years, None)["ni_up_years"] == 2

    rising = _years({"2021": 1, "2022": 2, "2023": 3, "2024": 4, "2025": 5})
    assert growth_factors(rising, None)["ni_up_years"] == 4

    gap = _years({"2022": 1, "2024": 4, "2025": 5})
    assert growth_factors(gap, None)["ni_up_years"] == 1


def test_cagr_needs_positive_ends() -> None:
    assert growth_factors(_years({"2022": 100, "2025": 133.1}), None)["ni_cagr_3y"] == 10.0
    assert growth_factors(_years({"2022": -5, "2025": 133.1}), None)["ni_cagr_3y"] is None
    assert growth_factors(_years({"2025": 133.1}), None)["ni_cagr_3y"] is None


def test_quarter_streak_ttm_change_turnaround_and_margin() -> None:
    panel = {
        (2026, 3): {"영업이익": (30.0, 100.0), "매출액": (200.0, 700.0)},
        (2026, 2): {"영업이익": (25.0, 80.0)},
        (2026, 1): {"영업이익": (5.0, 60.0)},
        (2025, 3): {"영업이익": (-10.0, 50.0), "매출액": (150.0, 600.0)},
        (2025, 2): {"영업이익": (20.0, 40.0)},
        (2025, 1): {"영업이익": (8.0, 30.0)},
    }

    factors = growth_factors({}, _panel(panel, (2026, 3)))

    assert factors["op_up_quarters"] == 2  # 2026Q3 > 2025Q3, 2026Q2 > 2025Q2, 2026Q1 < 2025Q1
    assert factors["op_yoy_ttm"] == 100.0
    assert factors["rev_yoy_ttm"] == round((700 / 600 - 1) * 100, 2)
    assert factors["op_turnaround_q"] == 1
    assert factors["opm_change_q"] == round(30 / 200 * 100 - (-10 / 150 * 100), 2)
    assert factors["ni_up_quarters"] == 0
    assert factors["ni_yoy_ttm"] is None


def test_no_data_gives_nulls() -> None:
    factors = growth_factors({}, None)
    assert set(factors.values()) == {None}
