"""`cache trend-setup`: the trend-setup judgement for every stock in the cache on one day.

No rule lives here — each stock goes through `trend_setup.analyze`, the same function
`kis chart trend-setup` calls, and a contract test holds the two to the same answer. This
module only reads the cache, picks the universe and summarizes rows.
"""

from __future__ import annotations

from collections import Counter
from datetime import date, timedelta
from typing import Any

import duckdb
import numpy as np

from cluefin_openapi_cli import trend_setup
from cluefin_openapi_cli.cache.read import read_company

__all__ = ["latest_index_date", "scan"]

# Matches `kis chart trend-setup` (260 bars); ~380 calendar days, read with slack.
_BARS = 260
_LOOKBACK_DAYS = 500
_INDEX_FOR = {"KOSPI": "U0001", "KOSDAQ": "U1001"}

# Adjusted like `read_ohlcv(adjusted=True)`; NULL prices (KIS 0) drop the bar, as in the backtest.
_BARS_SQL = """
SELECT code, date,
       open * f, high * f, low * f, close * f, volume / f, value
FROM (
  SELECT *, COALESCE(NULLIF(adj_factor, 0), 1) AS f FROM ohlcv
  WHERE code IN (SELECT unnest(?::TEXT[])) AND date BETWEEN ? AND ?
)
WHERE high > 0 AND low > 0 AND close > 0
ORDER BY code, date
"""
_INDEX_SQL = "SELECT code, date, close FROM ohlcv WHERE code IN ('U0001', 'U1001') AND date <= ? ORDER BY code, date"

# Row order: actionable first, then by distance to the pivot (closest above first).
_STATUS_ORDER = (
    "alert/setup",
    "watch/breaking_out",
    "watch/g3_candidate",
    "watch/g2",
    "watch/extended",
    "watch/far_below_pivot",
    "exclude/overheated",
    "exclude/no_group",
    "exclude/illiquid",
)
_NOTES = (
    "가격은 캐시의 KIS 원주가 × adj_factor(수정주가)다 — kis chart trend-setup 과 같은 기준.",
    "company.market 은 현재 값이다 — 시장을 옮긴 종목은 과거 날짜에서 비교 지수가 틀릴 수 있다.",
)


def latest_index_date(conn: duckdb.DuckDBPyConnection) -> date | None:
    row = conn.execute("SELECT max(date) FROM ohlcv WHERE code = 'U0001'").fetchone()
    return row[0] if row else None


def _universe(
    conn: duckdb.DuckDBPyConnection, as_of: date, market: str | None, codes: list[str] | None
) -> list[dict[str, Any]]:
    """Listed on ``as_of`` (later delistings included), common shares only, no SPACs — as the backtest."""

    companies = read_company(conn, as_of=as_of, market=market)["companies"]
    wanted = set(codes) if codes else None
    return [
        row
        for row in companies
        if row["code"].endswith("0")
        and "스팩" not in (row["name"] or "")
        and row["market"] in _INDEX_FOR
        and (wanted is None or row["code"] in wanted)
    ]


def _indices(conn: duckdb.DuckDBPyConnection, as_of: date) -> dict[str, trend_setup.IndexCloses]:
    by_code: dict[str, list[tuple[date, float]]] = {}
    for code, day, close in conn.execute(_INDEX_SQL, [as_of]).fetchall():
        by_code.setdefault(code, []).append((day, close))
    return {code: trend_setup.IndexCloses.from_pairs(pairs) for code, pairs in by_code.items()}


def _series(conn: duckdb.DuckDBPyConnection, codes: list[str], as_of: date) -> dict[str, trend_setup.PriceArrays]:
    """Each code's last ``_BARS`` bars up to ``as_of``, split from one columnar read."""

    cols = conn.execute(_BARS_SQL, [codes, as_of - timedelta(days=_LOOKBACK_DAYS), as_of]).fetchnumpy()
    names = list(cols)
    if len(cols[names[0]]) == 0:
        return {}
    code_col = np.asarray(cols[names[0]])
    dates = np.char.replace(np.datetime_as_string(np.asarray(cols[names[1]]), unit="D"), "-", "")
    prices = [np.asarray(cols[name], dtype=np.float64) for name in names[2:8]]
    bounds = np.flatnonzero(code_col[1:] != code_col[:-1]) + 1
    out = {}
    for start, stop in zip(np.r_[0, bounds], np.r_[bounds, len(code_col)], strict=True):
        cut = slice(max(start, stop - _BARS), stop)
        out[str(code_col[start])] = trend_setup.PriceArrays(
            dates=tuple(dates[cut].tolist()),
            open=prices[0][cut],
            high=prices[1][cut],
            low=prices[2][cut],
            close=prices[3][cut],
            volume=prices[4][cut],
            value=prices[5][cut],
        )
    return out


def _failed(setup: dict[str, Any]) -> list[str]:
    """Check ids that kept the stock out of groups 2 and 3 — why it is not a setup, from the row alone."""

    checks = setup["checks"]
    return [check["id"] for check in (*checks["g2"], *checks["g3"]) if not check["pass"]]


def _row(company: dict[str, Any], reading: dict[str, Any]) -> dict[str, Any]:
    setup, pivot, strength = reading["setup"], reading["pivot"], reading["strength"]
    return {
        "code": company["code"],
        "name": company["name"],
        "market": company["market"],
        "close": reading["close"],
        "action": setup["action"],
        "status": setup["status"],
        "groups": setup["groups"],
        "reason": setup["reason"],
        "pivot": pivot["price"] if pivot else None,
        "to_pivot_pct": pivot["to_pivot_pct"] if pivot else None,
        "rel": strength["rel"],
        "contractions": pivot["contractions"] if pivot else 0,
        "last_contraction_pct": pivot["last_contraction_pct"] if pivot else None,
        "range_10d_pct": reading["volatility"]["range_10d_pct"],
        "gap_to_high_pct": reading["range_52w"]["gap_to_high_pct"],
        "g2_score": setup["g2_score"]["score"],
        "traded_value_20d_eok": reading["volume"]["traded_value_20d_eok"],
        "levels": reading["levels"],
        "failed": _failed(setup),
    }


def _sort_key(row: dict[str, Any]) -> tuple[int, float]:
    key = f"{row['action']}/{row['status']}"
    rank = _STATUS_ORDER.index(key) if key in _STATUS_ORDER else len(_STATUS_ORDER)
    to_pivot = row["to_pivot_pct"]
    return rank, -to_pivot if to_pivot is not None else float("inf")


def _wanted(row: dict[str, Any], statuses: list[str] | None, include_excluded: bool) -> bool:
    if statuses:
        return row["action"] in statuses or f"{row['action']}/{row['status']}" in statuses
    return include_excluded or row["action"] != "exclude"


def scan(
    conn: duckdb.DuckDBPyConnection,
    as_of: date,
    *,
    market: str | None = None,
    codes: list[str] | None = None,
    statuses: list[str] | None = None,
    include_excluded: bool = False,
) -> dict[str, Any]:
    """Judge every stock in the universe on ``as_of``; rows for the wanted statuses, counts for all."""

    universe = _universe(conn, as_of, market, codes)
    indices = _indices(conn, as_of)
    series = _series(conn, [row["code"] for row in universe], as_of)
    day = as_of.strftime("%Y%m%d")
    counts: Counter[str] = Counter()
    skipped: Counter[str] = Counter()
    rows = []
    for company in universe:
        prices = series.get(company["code"])
        if prices is None or prices.dates[-1] != day:
            skipped["no_bar"] += 1
            continue
        try:
            reading = trend_setup.analyze(prices, indices[_INDEX_FOR[company["market"]]])
        except trend_setup.InsufficientHistory:
            skipped["insufficient_history"] += 1
            continue
        row = _row(company, reading)
        counts[f"{row['action']}/{row['status']}"] += 1
        if _wanted(row, statuses, include_excluded):
            rows.append(row)
    rows.sort(key=_sort_key)
    summary: dict[str, Any] = {key: counts[key] for key in _STATUS_ORDER if counts[key]}
    summary["skipped"] = {"no_bar": skipped["no_bar"], "insufficient_history": skipped["insufficient_history"]}
    return {
        "as_of": day,
        "universe": len(universe),
        "summary": summary,
        "count": len(rows),
        "rows": rows,
        "notes": list(_NOTES),
        "caveats": list(trend_setup.CAVEATS),
    }
