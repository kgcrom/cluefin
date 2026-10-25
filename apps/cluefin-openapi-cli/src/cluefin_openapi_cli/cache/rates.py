"""`rates` table: ECOS daily market rates (annual %, as published), the risk-free side of `cache perf`.

One `StatisticSearch` per series covers any span with a real key (no row cap; paged by 1000 anyway).
Holidays have no row. A daily run re-reads the last week so a late or revised value replaces the old one.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Any

import duckdb
from cluefin_openapi.ecos import CD_91D, KTB_1Y, KTB_3Y, KTB_10Y

__all__ = ["RATE_SERIES", "RateLoadStats", "load_rates"]

# Slug used by `cache perf --risk-free` → ECOS series.
RATE_SERIES = {"ktb1y": KTB_1Y, "ktb3y": KTB_3Y, "ktb10y": KTB_10Y, "cd91d": CD_91D}
_REREAD_DAYS = 7


@dataclass(slots=True)
class RateLoadStats:
    series: int = 0
    rows: int = 0
    calls: int = 0
    errors: list[dict[str, str]] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "series": self.series,
            "rows": self.rows,
            "calls": self.calls,
            "errors": len(self.errors),
            "error_samples": self.errors[:10],
        }


def _observations(page: Any) -> list[tuple[date, float]]:
    rows = []
    for row in page.rows:
        value = row.value
        if value is not None:
            rows.append((datetime.strptime(row.time, "%Y%m%d").date(), float(value)))
    return rows


def load_rates(
    conn: duckdb.DuckDBPyConnection,
    *,
    ecos: Any,
    since: date,
    last_day: date,
    progress: Callable[[str], None] = lambda _message: None,
) -> RateLoadStats:
    stats = RateLoadStats(series=len(RATE_SERIES))
    if ecos.is_sample:
        # The public `sample` key pages 10 rows a call: ~250 calls a series for ten years.
        stats.errors.append({"code": "ecos", "error": "ECOS_AUTH_KEY is not set in .env; rates skipped."})
        return stats
    for slug, series in RATE_SERIES.items():
        row = conn.execute("SELECT max(date) FROM rates WHERE series = ?", [slug]).fetchone()
        stored = row[0] if row else None
        start = max(since, stored - timedelta(days=_REREAD_DAYS)) if stored else since
        try:
            stats.calls += 1
            page = ecos.statistic_search.search_series(series, f"{start:%Y%m%d}", f"{last_day:%Y%m%d}")
            observations = _observations(page)
            now = datetime.now()
            conn.executemany(
                "INSERT OR REPLACE INTO rates VALUES (?, ?, ?, ?)",
                [(slug, day, value, now) for day, value in observations],
            )
            stats.rows += len(observations)
        except Exception as exc:  # noqa: BLE001 - one bad series must not stop the others
            stats.errors.append({"code": slug, "error": f"{type(exc).__name__}: {str(exc)[:200]}"})
        progress(f"rates: {slug} {start:%Y-%m-%d}..{last_day:%Y-%m-%d}")
    return stats
