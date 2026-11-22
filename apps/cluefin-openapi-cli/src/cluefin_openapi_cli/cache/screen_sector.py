"""Within-sector percentiles for `cache screen` (decided 2026-11-22).

`<factor>_sector_pct` ranks a stock's factor against every stock of the same `company.sector` in the
full screen universe (0 = lowest value, 99 = highest), before `--market`/`--sector`/`--code` narrow
the output — same rule as `rs_1m`, so narrowing never moves a percentile. A sector with fewer than
`MIN_SECTOR_SIZE` non-null values gives `null`. Low `per_ttm_sector_pct` = cheap for its sector.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from cluefin_openapi_cli.cache.breadth import _percentile_rank, _round_half_up

__all__ = ["MIN_SECTOR_SIZE", "SECTOR_FACTORS", "add_sector_percentiles"]

MIN_SECTOR_SIZE = 5
_BASES = ("per_ttm", "pbr_mrq", "psr_ttm", "roe_ttm")
SECTOR_FACTORS: tuple[tuple[str, str], ...] = tuple(
    (
        f"{base}_sector_pct",
        f"같은 업종(company.sector) 안 {base} 백분위(0=가장 낮음, 99=가장 높음). 업종 값 5개 미만이면 null.",
    )
    for base in _BASES
)


def add_sector_percentiles(rows: list[dict[str, Any]]) -> None:
    """Set every `SECTOR_FACTORS` field on ``rows`` in place."""

    for base in _BASES:
        field = f"{base}_sector_pct"
        by_sector: dict[Any, list[dict[str, Any]]] = {}
        for row in rows:
            row[field] = None
            if row.get(base) is not None:
                by_sector.setdefault(row.get("sector"), []).append(row)
        for members in by_sector.values():
            if len(members) < MIN_SECTOR_SIZE:
                continue
            ranks = _percentile_rank(np.array([row[base] for row in members], dtype=np.float64))
            for row, rank in zip(members, ranks, strict=True):
                row[field] = _round_half_up(rank)
