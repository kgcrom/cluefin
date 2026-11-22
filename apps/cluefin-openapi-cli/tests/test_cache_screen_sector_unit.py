"""`cache screen` within-sector percentiles (cache/screen_sector.py)."""

from __future__ import annotations

from cluefin_openapi_cli.cache.screen_sector import add_sector_percentiles


def _row(code: str, sector: str, per: float | None) -> dict:
    return {"code": code, "sector": sector, "per_ttm": per, "pbr_mrq": None, "psr_ttm": None, "roe_ttm": None}


def test_percentile_within_sector_and_small_sector_is_null() -> None:
    rows = [_row(f"A{i}", "화학", per) for i, per in enumerate([5.0, 10.0, 15.0, 20.0, 25.0])]
    rows += [_row("B0", "건설", 3.0), _row("B1", "건설", 4.0)]
    rows.append(_row("A9", "화학", None))

    add_sector_percentiles(rows)

    by_code = {row["code"]: row for row in rows}
    assert by_code["A0"]["per_ttm_sector_pct"] == 0
    assert by_code["A4"]["per_ttm_sector_pct"] == 99
    assert 0 < by_code["A2"]["per_ttm_sector_pct"] < 99
    assert by_code["B0"]["per_ttm_sector_pct"] is None
    assert by_code["A9"]["per_ttm_sector_pct"] is None
    assert by_code["A0"]["pbr_mrq_sector_pct"] is None
