"""`cache perf`: one stock's buy-and-hold performance against an index, from cached bars."""

from __future__ import annotations

import math
from datetime import date
from typing import Any

import duckdb
import numpy as np
from cluefin_ta import PERFORMANCE, PERIODIC_RATE

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
    risk_free: float,
) -> dict[str, Any]:
    """``PERFORMANCE`` of the stock's adjusted close against the benchmark's, on shared dates.

    ``risk_free`` is an annual rate (0.035 for 3.5%); CAGR uses calendar years between the
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
    rate = PERIODIC_RATE(risk_free)
    payload["first"] = days[0].isoformat()
    payload["last"] = days[-1].isoformat()
    payload["performance"] = _clean(PERFORMANCE(stock, benchmark=index, risk_free=rate, years=years))
    payload["benchmark_performance"] = _clean(PERFORMANCE(index, risk_free=rate, years=years))
    return payload
