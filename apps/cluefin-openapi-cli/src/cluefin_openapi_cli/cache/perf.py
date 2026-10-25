"""`cache perf`: one stock's buy-and-hold performance against an index, from cached bars."""

from __future__ import annotations

import math
from datetime import date, timedelta
from typing import Any

import duckdb
import numpy as np
from cluefin_ta import PERFORMANCE, PERIODIC_RATE

from cluefin_openapi_cli.errors import EXIT_USAGE, CliError

__all__ = ["read_perf"]

# Adjusted closes on the days both codes have a bar; a missing or zero factor counts as 1.
_PAIRED_SQL = """
SELECT s.date,
       s.close * COALESCE(NULLIF(s.adj_factor, 0), 1),
       b.close * COALESCE(NULLIF(b.adj_factor, 0), 1)
FROM ohlcv s
JOIN ohlcv b ON b.date = s.date AND b.code = ?
WHERE s.code = ? AND s.date BETWEEN ? AND ? AND s.close IS NOT NULL AND b.close IS NOT NULL
ORDER BY s.date
"""

# The latest published rate on or before each day (holidays and ECOS's one-day lag carry the last value).
_RATE_SQL = """
SELECT d.day, r.date, r.value
FROM (SELECT unnest(?::DATE[]) AS day) d
ASOF LEFT JOIN (SELECT date, value FROM rates WHERE series = ?) r ON d.day >= r.date
ORDER BY d.day
"""
# A rate older than this is a cache that stopped loading rates, not a long holiday.
_STALE_DAYS = 10


def _rates(conn: duckdb.DuckDBPyConnection, series: str, days: list[date]) -> np.ndarray:
    """Annual decimal rate per day from `rates`, or exit 2 when the cache does not cover the span."""

    rows = conn.execute(_RATE_SQL, [days, series]).fetchall()
    gaps = [day for day, published, _ in rows if published is None or day - published > timedelta(days=_STALE_DAYS)]
    if gaps:
        raise CliError(
            f"No `{series}` rate within {_STALE_DAYS} days of {gaps[0].isoformat()} in the cache.",
            exit_code=EXIT_USAGE,
            error_type="RatesMissing",
            hint="Run `cache load --only rates` (needs ECOS_AUTH_KEY), or pass an annual decimal like 0.03.",
            data={"series": series, "first_gap": gaps[0].isoformat(), "gaps": len(gaps)},
        )
    return np.array([value for _, _, value in rows], dtype=np.float64) / 100


def _clean(stats: dict[str, float]) -> dict[str, float | None]:
    """Round for output; NaN/inf (no volatility, no drawdown) become None so JSON stays valid."""

    return {name: None if math.isnan(value) or math.isinf(value) else round(value, 4) for name, value in stats.items()}


def read_perf(
    conn: duckdb.DuckDBPyConnection,
    code: str,
    *,
    benchmark: str,
    since: date,
    until: date,
    risk_free: float | str,
) -> dict[str, Any]:
    """``PERFORMANCE`` of the stock's adjusted close against the benchmark's, on shared dates.

    ``risk_free`` is an annual rate (0.035 for 3.5%) or a `rates` series slug (``ktb3y``), whose
    rate on the first day of each period applies to that period's return; CAGR uses calendar years between the
    first and last shared bar, since KRX has ~245 trading days rather than 252.
    """

    rows = conn.execute(_PAIRED_SQL, [benchmark, code, since, until]).fetchall()
    payload: dict[str, Any] = {
        "code": code,
        "benchmark": benchmark,
        "since": since.isoformat(),
        "until": until.isoformat(),
        "risk_free": risk_free,
        "count": len(rows),
    }
    if len(rows) < 2:
        payload["performance"] = None
        payload["benchmark_performance"] = None
        return payload
    days = [row[0] for row in rows]
    stock = np.array([row[1] for row in rows], dtype=np.float64)
    index = np.array([row[2] for row in rows], dtype=np.float64)
    years = (days[-1] - days[0]).days / 365.25
    if isinstance(risk_free, str):
        annual = _rates(conn, risk_free, days[:-1])
        payload["risk_free_mean"] = round(float(annual.mean()), 4)
        rate = PERIODIC_RATE(annual)
    else:
        rate = PERIODIC_RATE(risk_free)
    payload["first"] = days[0].isoformat()
    payload["last"] = days[-1].isoformat()
    payload["performance"] = _clean(PERFORMANCE(stock, benchmark=index, risk_free=rate, years=years))
    payload["benchmark_performance"] = _clean(PERFORMANCE(index, risk_free=rate, years=years))
    return payload
