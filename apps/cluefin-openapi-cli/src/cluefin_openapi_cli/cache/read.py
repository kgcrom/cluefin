"""Read queries over the cache: one stock's bars, and the company universe as of a day."""

from __future__ import annotations

from datetime import date
from typing import Any

import duckdb

__all__ = ["read_company", "read_ohlcv"]

_PRICE_COLUMNS = ("open", "high", "low", "close")


def _iso(value: Any) -> Any:
    return value.isoformat() if isinstance(value, date) else value


def read_ohlcv(
    conn: duckdb.DuckDBPyConnection, code: str, *, since: date, until: date, adjusted: bool
) -> dict[str, Any]:
    """Bars oldest first. ``adjusted`` scales prices by adj_factor and volume by its inverse."""

    rows = conn.execute(
        "SELECT date, open, high, low, close, volume, value, adj_factor, lock_code, prtt_rate, reval_code "
        "FROM ohlcv WHERE code = ? AND date BETWEEN ? AND ? ORDER BY date",
        [code, since, until],
    ).fetchall()
    bars = []
    for day, *prices, volume, value, factor, lock_code, prtt_rate, reval_code in rows:
        scale = factor if adjusted and factor else 1.0
        bar = {"date": day.isoformat()}
        bar.update(
            {
                name: (price * scale if price is not None else None)
                for name, price in zip(_PRICE_COLUMNS, prices, strict=False)
            }
        )
        bar["volume"] = volume / scale if volume is not None else None
        bar["value"] = value
        bar["adj_factor"] = factor
        bar["lock_code"] = lock_code
        bar["prtt_rate"] = prtt_rate
        bar["reval_code"] = reval_code
        bars.append(bar)
    return {
        "code": code,
        "adjusted": adjusted,
        "since": since.isoformat(),
        "until": until.isoformat(),
        "count": len(bars),
        "bars": bars,
    }


_COMPANY_COLUMNS = (
    "code",
    "name",
    "market",
    "kind",
    "sector",
    "industry",
    "corp_code",
    "settle_month",
    "listed_on",
    "delisted_on",
    "list_count",
    "is_admin",
    "is_halted",
    "seen_on",
)


def read_company(
    conn: duckdb.DuckDBPyConnection,
    *,
    code: str | None = None,
    as_of: date | None = None,
    include_delisted: bool = False,
    market: str | None = None,
) -> dict[str, Any]:
    """Company rows. ``as_of`` gives the universe listed on that day (point in time)."""

    where: list[str] = []
    params: list[Any] = []
    if code is not None:
        where.append("code = ?")
        params.append(code)
    if market is not None:
        where.append("market = ?")
        params.append(market)
    if as_of is not None:
        where.append("(listed_on IS NULL OR listed_on <= ?) AND (delisted_on IS NULL OR delisted_on > ?)")
        params.extend([as_of, as_of])
    elif not include_delisted and code is None:
        where.append("delisted_on IS NULL")
    sql = f"SELECT {', '.join(_COMPANY_COLUMNS)} FROM company"
    if where:
        sql += " WHERE " + " AND ".join(where)
    rows = conn.execute(sql + " ORDER BY code", params).fetchall()
    companies = [{name: _iso(value) for name, value in zip(_COMPANY_COLUMNS, row, strict=False)} for row in rows]
    payload: dict[str, Any] = {"count": len(companies), "companies": companies}
    if as_of is not None:
        payload["as_of"] = as_of.isoformat()
    return payload
