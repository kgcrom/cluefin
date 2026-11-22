"""TTM and latest-quarter factors for `cache screen`, read from `financials_ttm` (decided 2026-11-22).

The annual factors (`per`, `roe`, …) stay on the latest 사업보고서; these sit beside them so a
screen can use the latest quarter instead of a fiscal year that may be nine months old.

- Period: each stock's latest (year, quarter) in `financials_ttm` whose filing deadline
  (`financials_quarterly.quarter_due`, December year-end) is on or before ``as_of`` — no look-ahead.
  A stock whose own latest period is older (late filer, delisted) uses that older period;
  `ttm_period` says which.
- Flows (매출액·영업이익·당기순이익) are TTM; equity (자본총계) is the period-end balance (MRQ).
- `revenue_yoy_q`/`op_yoy_q` compare that quarter's three months with the same quarter a year
  earlier; a missing or non-positive base is `null`.
"""

from __future__ import annotations

from datetime import date
from typing import Any

import duckdb

from cluefin_openapi_cli.cache.financials_quarterly import quarter_due

__all__ = ["TTM_FACTORS", "latest_due_period", "ttm_by_code", "ttm_factors"]

TTM_FACTORS: tuple[tuple[str, str], ...] = (
    ("per_ttm", "시총 / TTM 당기순이익(최근 4개 분기 합). 당기순이익<=0 이면 null."),
    ("psr_ttm", "시총 / TTM 매출액. 매출액<=0 이면 null."),
    ("pbr_mrq", "시총 / 최근 분기말 자본총계. 자본총계<=0 이면 null."),
    ("roe_ttm", "TTM 당기순이익 / 최근 분기말 자본총계 * 100 (%). 자본총계<=0 이면 null."),
    ("opm_ttm", "TTM 영업이익 / TTM 매출액 * 100 (%). 매출액<=0 이면 null."),
    ("revenue_yoy_q", "최근 분기 3개월 매출액의 전년 같은 분기 대비 증감률(%). 전년 분기가 없거나 0 이하면 null."),
    ("op_yoy_q", "최근 분기 3개월 영업이익의 전년 같은 분기 대비 증감률(%). 전년 분기가 없거나 0 이하면 null."),
)
_FIELDS = ("ttm_period", *(name for name, _ in TTM_FACTORS))
_ACCOUNTS = ["매출액", "영업이익", "당기순이익", "자본총계"]

_SQL = """
SELECT code, year, quarter, account_nm, quarter_amount, ttm_amount
FROM financials_ttm
WHERE code IN (SELECT unnest(?::TEXT[])) AND account_nm IN (SELECT unnest(?::TEXT[]))
  AND CAST(year AS INTEGER) * 10 + quarter <= ?
"""


def latest_due_period(as_of: date) -> tuple[int, int]:
    """The latest (fiscal year, quarter) whose filing deadline is on or before ``as_of``."""

    year = as_of.year
    while True:
        for quarter in (4, 3, 2, 1):
            if quarter_due(year, quarter) <= as_of:
                return year, quarter
        year -= 1


def ttm_by_code(conn: duckdb.DuckDBPyConnection, codes: list[str], as_of: date) -> dict[str, dict[str, Any]]:
    """``{code: {"period": (year, quarter), "ttm": {...}, "quarter": {...}, "prior_quarter": {...}}}``."""

    if not codes:
        return {}
    cap_year, cap_quarter = latest_due_period(as_of)
    rows = conn.execute(_SQL, [codes, _ACCOUNTS, cap_year * 10 + cap_quarter]).fetchall()
    periods: dict[str, dict[tuple[int, int], dict[str, tuple[Any, Any]]]] = {}
    for code, year, quarter, account_nm, quarter_amount, ttm_amount in rows:
        periods.setdefault(code, {}).setdefault((int(year), quarter), {})[account_nm] = (quarter_amount, ttm_amount)
    out: dict[str, dict[str, Any]] = {}
    for code, by_period in periods.items():
        latest = max(by_period)
        prior = by_period.get((latest[0] - 1, latest[1]), {})
        out[code] = {
            "period": latest,
            "ttm": {name: values[1] for name, values in by_period[latest].items()},
            "quarter": {name: values[0] for name, values in by_period[latest].items()},
            "prior_quarter": {name: values[0] for name, values in prior.items()},
        }
    return out


def _ratio(numerator: float | None, denominator: float | None, scale: float = 1.0) -> float | None:
    if numerator is None or denominator is None or denominator <= 0:
        return None
    return round(numerator / denominator * scale, 2)


def _yoy(now: float | None, before: float | None) -> float | None:
    if now is None or before is None or before <= 0:
        return None
    return round((now / before - 1) * 100, 2)


def ttm_factors(entry: dict[str, Any] | None, mcap: float | None) -> dict[str, Any]:
    """The `TTM_FACTORS` values (plus `ttm_period`) for one stock; all `null` without cached quarters."""

    out: dict[str, Any] = dict.fromkeys(_FIELDS, None)
    if not entry:
        return out
    year, quarter = entry["period"]
    ttm, current, prior = entry["ttm"], entry["quarter"], entry["prior_quarter"]
    revenue, ebit, net_income, equity = (ttm.get(name) for name in _ACCOUNTS)
    out["ttm_period"] = f"{year}Q{quarter}"
    out["roe_ttm"] = _ratio(net_income, equity, 100)
    out["opm_ttm"] = _ratio(ebit, revenue, 100)
    out["revenue_yoy_q"] = _yoy(current.get("매출액"), prior.get("매출액"))
    out["op_yoy_q"] = _yoy(current.get("영업이익"), prior.get("영업이익"))
    if mcap is not None:
        out["per_ttm"] = _ratio(mcap, net_income)
        out["psr_ttm"] = _ratio(mcap, revenue)
        out["pbr_mrq"] = _ratio(mcap, equity)
    return out
