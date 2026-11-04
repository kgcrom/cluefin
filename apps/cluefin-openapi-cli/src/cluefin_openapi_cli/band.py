"""PER/PBR band: quantiles of a daily multiple series, and where today sits in it.

Pure functions only — no DART/KIS calls, no local `cache` file access. The `stock.valuation_band`
handler (`handlers/kis/domestic_stock_info.py`) does the I/O: daily closes come from the local
`cache` DuckDB (read-only, `cache.read.read_ohlcv`), and each fiscal year's EPS/BPS inputs
(net income attributable to owners, equity attributable to owners, common shares outstanding)
come from DART's per-stock full statements and share count, fetched one fiscal year at a time —
not `cache financials` (`fnlttMultiAcnt`), which has no 지배/비지배 split (decision 2026-11-04,
docs/plans/today-bundles-plan.md B-7).

A day's multiple is that day's close divided by the EPS/BPS of the latest fiscal year whose
사업보고서 was due by that day (`trailing_fiscal_year`: the prior year from April 1, two years back
before it — 결산월 12월 가정). That is what an investor could see on the day, and the same basis
the `current` multiple uses, so the current percentile compares like with like. A fiscal year
with no computable EPS/BPS (missing statements or share count) contributes no rows — never
zero-filled.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

import numpy as np

__all__ = ["band", "eps_bps", "multiple_series", "quantiles", "trailing_fiscal_year"]

_QUANTILE_LEVELS = (0.0, 0.25, 0.50, 0.75, 1.00)
_QUANTILE_LABELS = ("min", "p25", "median", "p75", "max")


def _as_date(day: str | date) -> date:
    if isinstance(day, date):
        return day
    text = str(day).replace("-", "")
    return datetime.strptime(text[:8], "%Y%m%d").date()


def trailing_fiscal_year(day: str | date) -> int:
    """Latest fiscal year whose annual report was due by ``day`` (filed within 90 days: by March 31)."""
    d = _as_date(day)
    return d.year - 1 if (d.month, d.day) >= (4, 1) else d.year - 2


def eps_bps(
    net_income_owners: float | None, equity_owners: float | None, shares: float | None
) -> tuple[float | None, float | None]:
    """EPS = 지배주주순이익 ÷ 발행주식수, BPS = 지배기업지분 ÷ 발행주식수.

    None propagates (missing input, not zero); a non-positive share count makes both None.
    """
    if shares is None or shares <= 0:
        return None, None
    eps = None if net_income_owners is None else net_income_owners / shares
    bps = None if equity_owners is None else equity_owners / shares
    return eps, bps


def quantiles(values: list[float]) -> dict[str, float] | None:
    """min/p25/median/p75/max of `values`, or None when there is nothing to summarize."""
    if not values:
        return None
    array = np.array(values, dtype=np.float64)
    q = np.quantile(array, _QUANTILE_LEVELS)
    return {label: round(float(v), 4) for label, v in zip(_QUANTILE_LABELS, q, strict=True)}


def _percentile_of(value: float, values: list[float]) -> float:
    """Share of `values` at or below `value`, 0-100. A value outside the range reads 0 or 100."""
    array = np.array(values, dtype=np.float64)
    return round(float((array <= value).mean() * 100), 1)


def multiple_series(bars: list[tuple[str, float]], per_share_by_year: dict[int, float | None]) -> list[dict[str, Any]]:
    """`(date "YYYY-MM-DD"/"YYYYMMDD", close)` bars → one row per bar whose trailing fiscal year has a value.

    Each bar is paired with `trailing_fiscal_year(date)`. Rows whose fiscal year is missing from
    `per_share_by_year`, or whose per-share value or close is None/non-positive, are dropped.
    """
    out = []
    for day, close in bars:
        if close is None or close <= 0:
            continue
        year = trailing_fiscal_year(day)
        value = per_share_by_year.get(year)
        if value is None or value <= 0:
            continue
        out.append({"date": day, "year": year, "close": close, "multiple": close / value})
    return out


def band(
    bars: list[tuple[str, float]],
    per_share_by_year: dict[int, float | None],
    *,
    current_close: float | None,
    current_per_share: float | None,
) -> dict[str, Any]:
    """Quantiles of `close / per_share_by_year[year]` over `bars`, plus today's multiple and percentile.

    `current_close`/`current_per_share` are given separately rather than derived from `bars`'
    last row: the current multiple compares today's price against the *latest computable*
    fiscal year's EPS/BPS, which need not be the calendar year the last bar falls in (this
    year's annual report is usually not filed yet).
    """
    rows = multiple_series(bars, per_share_by_year)
    series = [row["multiple"] for row in rows]
    current_multiple = (
        None
        if current_close is None or current_per_share is None or current_per_share <= 0
        else current_close / current_per_share
    )
    return {
        "n": len(series),
        "quantiles": quantiles(series),
        "current": None if current_multiple is None else round(current_multiple, 4),
        "current_percentile": None
        if current_multiple is None or not series
        else _percentile_of(current_multiple, series),
    }
