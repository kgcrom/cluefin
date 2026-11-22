"""`cache screen` value and balance-sheet factors (cache/screen_quality.py)."""

from __future__ import annotations

from cluefin_openapi_cli.cache.screen_quality import quality_factors


def _entry():
    def both(value: float) -> tuple[float, float]:
        return (value, value)

    latest = {
        "당기순이익": (30.0, 100.0),
        "매출액": (300.0, 1000.0),
        "영업이익": (40.0, 80.0),
        "자산총계": both(1200.0),
        "자본총계": both(600.0),
        "자본금": both(50.0),
        "이익잉여금(결손금)": both(400.0),
        "유동자산": both(500.0),
        "유동부채": both(250.0),
        "부채총계": both(600.0),
        "비유동자산": both(700.0),
    }
    year_ago = {"자산총계": both(800.0), "자본총계": both(500.0), "비유동자산": both(560.0)}
    return {"period": (2026, 3), "panel": {(2026, 3): latest, (2025, 3): year_ago}}


def test_ratios_from_ttm_and_balances() -> None:
    factors = quality_factors(_entry(), 2000.0, per_ttm=20.0, growth=25.0, sector="전기전자")

    assert factors["roa_ttm"] == 10.0  # 100 / avg(1200, 800)
    assert factors["npm_ttm"] == 10.0
    assert factors["asset_turnover_ttm"] == 1.0
    assert factors["peg_ttm"] == 0.8
    assert factors["earnings_yield_ttm"] == round(80 / 2600 * 100, 2)
    assert factors["current_ratio"] == 200.0
    assert factors["debt_ratio_mrq"] == 100.0
    assert factors["ncav_ratio"] == round((500 - 600) / 2000, 2)
    assert factors["retained_ratio"] == 800.0
    assert factors["capital_impairment"] == 0
    assert factors["equity_yoy"] == 20.0
    assert factors["noncurrent_asset_yoy"] == 25.0
    assert factors["ni_to_op_ttm"] == 1.25


def test_excluded_sector_negative_growth_and_missing_year_ago() -> None:
    entry = _entry()
    del entry["panel"][(2025, 3)]

    factors = quality_factors(entry, 2000.0, per_ttm=20.0, growth=-5.0, sector="금융")

    assert factors["roa_ttm"] is None
    assert factors["peg_ttm"] is None
    assert factors["earnings_yield_ttm"] is None
    assert factors["equity_yoy"] is None


def test_capital_impairment_and_no_entry() -> None:
    entry = _entry()
    entry["panel"][(2026, 3)]["자본총계"] = (40.0, 40.0)
    assert quality_factors(entry, None, per_ttm=None, growth=None, sector=None)["capital_impairment"] == 1
    assert set(quality_factors(None, 1.0, per_ttm=None, growth=None, sector=None).values()) == {None}
