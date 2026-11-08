"""Read queries over the cache: one stock's bars, and the company universe as of a day."""

from __future__ import annotations

from datetime import date
from typing import Any

import duckdb

__all__ = ["read_company", "read_financials", "read_ohlcv"]

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


_COMPANY_SQL = """
SELECT code, name, market, kind, sector, industry, corp_code, settle_month, listed_on, delisted_on, list_count,
       is_admin, is_halted, seen_on
FROM company
WHERE (?::TEXT IS NULL OR code = ?)
  AND (?::TEXT IS NULL OR market = ?)
  AND (?::DATE IS NULL OR ((listed_on IS NULL OR listed_on <= ?) AND (delisted_on IS NULL OR delisted_on > ?)))
  AND (? OR delisted_on IS NULL)
ORDER BY code
"""


_FINANCIALS_NOTES = (
    "DART fnlttMultiAcnt(다중회사 주요계정)의 표준 12개 계정만 있다 — 현금흐름표 항목은 없다.",
    "지배/비지배 구분이 없는 연결 합계다(그 구분이 필요하면 `dart financial-summary`를 쓴다).",
    "연결(CFS)을 우선하고 없으면 별도(OFS)다 — 종목·연도별 `basis` 를 본다.",
    "사업보고서(reprt_code 11011) 한 해치만 있다 — 분기·반기는 없다.",
    "금액 단위는 원(DART 응답 그대로)이다 — `dart financial-summary`는 억원이다.",
)


def read_financials(
    conn: duckdb.DuckDBPyConnection, code: str, *, since_year: str | None = None, until_year: str | None = None
) -> dict[str, Any]:
    """One stock's cached annual major-account figures, newest year first.

    A preferred share has no rows of its own: DART answers its corp_code with the common share's
    stock code only, so its fetch is logged `empty`. It reads the common share's rows instead —
    the same company's statements — and says so in `financials_code`.
    """

    filer = _financials_filer(conn, code)
    rows = conn.execute(
        "SELECT year, reprt_code, basis, account_nm, amount, currency FROM financials "
        "WHERE code = ? AND (?::TEXT IS NULL OR year >= ?) AND (?::TEXT IS NULL OR year <= ?) "
        "ORDER BY year DESC, account_nm",
        [filer, since_year, since_year, until_year, until_year],
    ).fetchall()
    by_year: dict[str, dict[str, Any]] = {}
    for year, reprt_code, basis, account_nm, amount, currency in rows:
        entry = by_year.setdefault(
            year, {"year": year, "reprt_code": reprt_code, "basis": basis, "currency": currency, "accounts": {}}
        )
        entry["accounts"][account_nm] = amount
    years = sorted(by_year.values(), key=lambda row: row["year"], reverse=True)
    payload: dict[str, Any] = {"code": code, "count": len(years), "years": years, "notes": list(_FINANCIALS_NOTES)}
    if filer != code:
        payload["financials_code"] = filer
        payload["notes"].append(
            f"{code} 는 자체 재무 행이 없어 같은 회사(corp_code) 보통주 {filer} 의 재무를 보여준다."
        )
    return payload


def _financials_filer(conn: duckdb.DuckDBPyConnection, code: str) -> str:
    """``code`` itself if it has financials, else the other listed code sharing its corp_code that does."""

    if conn.execute("SELECT 1 FROM financials WHERE code = ? LIMIT 1", [code]).fetchone():
        return code
    row = conn.execute(
        "SELECT other.code FROM company me JOIN company other "
        "ON other.corp_code = me.corp_code AND other.code != me.code "
        "WHERE me.code = ? AND EXISTS (SELECT 1 FROM financials f WHERE f.code = other.code) "
        "ORDER BY other.code LIMIT 1",
        [code],
    ).fetchone()
    return row[0] if row else code


def read_company(
    conn: duckdb.DuckDBPyConnection,
    *,
    code: str | None = None,
    as_of: date | None = None,
    include_delisted: bool = False,
    market: str | None = None,
) -> dict[str, Any]:
    """Company rows. ``as_of`` gives the universe listed on that day (point in time)."""

    # A code lookup or an as-of universe includes delisted rows on its own terms.
    keep_delisted = include_delisted or code is not None or as_of is not None
    rows = conn.execute(_COMPANY_SQL, [code, code, market, market, as_of, as_of, as_of, keep_delisted]).fetchall()
    companies = [{name: _iso(value) for name, value in zip(_COMPANY_COLUMNS, row, strict=False)} for row in rows]
    payload: dict[str, Any] = {"count": len(companies), "companies": companies}
    if as_of is not None:
        payload["as_of"] = as_of.isoformat()
    return payload
