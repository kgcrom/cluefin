"""Growth factors for `cache screen`: streaks, CAGR and TTM change (decided 2026-11-22).

"EPS 3년 성장, 3년이 길면 최근 4개 분기 성장" — the cache has no historical share count, so net income
stands in for EPS (same company, same share count assumption as `mcap`).

- Annual (`financials`, fiscal years already due by ``as_of``): `*_up_years` counts back from the latest
  fiscal year while each year is above the one before (a missing year ends the streak; five cached years
  give at most 4). `*_cagr_3y` needs both ends positive.
- Quarterly (`financials_ttm` panel from `screen_ttm.ttm_by_code`): `*_up_quarters` counts back from the
  latest due quarter while that quarter's three months beat the same quarter a year earlier.
  `*_yoy_ttm` compares the latest TTM with the TTM four quarters earlier (base must be positive).
- "Up" is a plain numeric increase, so a shrinking loss counts — combine with `*>0` style conditions
  (`per_ttm`, `roe_ttm`) when only profitable growth is wanted.
"""

from __future__ import annotations

from typing import Any

from cluefin_openapi_cli.cache.screen_ttm import Panel

__all__ = ["GROWTH_FACTORS", "growth_factors"]

_SERIES = (("ni", "당기순이익"), ("op", "영업이익"), ("rev", "매출액"))

GROWTH_FACTORS: tuple[tuple[str, str], ...] = (
    ("ni_up_years", "최신 사업연도부터 당기순이익이 전년보다 늘어난 해의 연속 수(최대 4). EPS 성장 대용."),
    ("op_up_years", "최신 사업연도부터 영업이익이 전년보다 늘어난 해의 연속 수(최대 4)."),
    ("rev_up_years", "최신 사업연도부터 매출액이 전년보다 늘어난 해의 연속 수(최대 4)."),
    ("ni_cagr_3y", "당기순이익 3년 연평균 성장률(%). 양 끝이 양수일 때만."),
    ("op_cagr_3y", "영업이익 3년 연평균 성장률(%). 양 끝이 양수일 때만."),
    ("ni_up_quarters", "최근 분기부터 3개월 당기순이익이 전년 같은 분기보다 늘어난 분기의 연속 수."),
    ("op_up_quarters", "최근 분기부터 3개월 영업이익이 전년 같은 분기보다 늘어난 분기의 연속 수."),
    ("rev_up_quarters", "최근 분기부터 3개월 매출액이 전년 같은 분기보다 늘어난 분기의 연속 수."),
    ("ni_yoy_ttm", "TTM 당기순이익의 4개 분기 전 TTM 대비 증감률(%). 기준이 0 이하면 null."),
    ("op_yoy_ttm", "TTM 영업이익의 4개 분기 전 TTM 대비 증감률(%). 기준이 0 이하면 null."),
    ("rev_yoy_ttm", "TTM 매출액의 4개 분기 전 TTM 대비 증감률(%). 기준이 0 이하면 null."),
    ("op_turnaround_q", "최근 분기 3개월 영업이익이 흑자이고 전년 같은 분기가 적자면 1, 아니면 0."),
    ("opm_change_q", "최근 분기 영업이익률 − 전년 같은 분기 영업이익률(%p). 매출액이 0 이하면 null."),
)
_FIELDS = tuple(name for name, _ in GROWTH_FACTORS)
_CAGR_YEARS = 3
# Five cached fiscal years give four year-over-year comparisons.
_MAX_YEARS = 4


def _up_years(years: dict[str, dict[str, float]], account: str) -> int | None:
    if not years:
        return None
    year = int(max(years))
    streak = 0
    while streak < _MAX_YEARS:
        now = years.get(str(year), {}).get(account)
        before = years.get(str(year - 1), {}).get(account)
        if now is None or before is None or now <= before:
            break
        streak += 1
        year -= 1
    return streak


def _cagr(years: dict[str, dict[str, float]], account: str) -> float | None:
    if not years:
        return None
    latest = int(max(years))
    now = years[str(latest)].get(account)
    before = years.get(str(latest - _CAGR_YEARS), {}).get(account)
    if now is None or before is None or now <= 0 or before <= 0:
        return None
    return round(((now / before) ** (1 / _CAGR_YEARS) - 1) * 100, 2)


def _previous(period: tuple[int, int]) -> tuple[int, int]:
    year, quarter = period
    return (year, quarter - 1) if quarter > 1 else (year - 1, 4)


def _value(panel: Panel, period: tuple[int, int], account: str, index: int) -> float | None:
    values = panel.get(period, {}).get(account)
    return values[index] if values else None


def _up_quarters(panel: Panel, latest: tuple[int, int], account: str) -> int:
    streak = 0
    period = latest
    while True:
        now = _value(panel, period, account, 0)
        before = _value(panel, (period[0] - 1, period[1]), account, 0)
        if now is None or before is None or now <= before:
            return streak
        streak += 1
        period = _previous(period)


def _pct_change(now: float | None, before: float | None) -> float | None:
    if now is None or before is None or before <= 0:
        return None
    return round((now / before - 1) * 100, 2)


def _margin(op: float | None, revenue: float | None) -> float | None:
    if op is None or revenue is None or revenue <= 0:
        return None
    return op / revenue * 100


def _quarter_factors(panel: Panel, latest: tuple[int, int]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    year_ago = (latest[0] - 1, latest[1])
    for prefix, account in _SERIES:
        out[f"{prefix}_up_quarters"] = _up_quarters(panel, latest, account)
        out[f"{prefix}_yoy_ttm"] = _pct_change(_value(panel, latest, account, 1), _value(panel, year_ago, account, 1))
    op_now, op_before = _value(panel, latest, "영업이익", 0), _value(panel, year_ago, "영업이익", 0)
    if op_now is not None and op_before is not None:
        out["op_turnaround_q"] = int(op_now > 0 and op_before < 0)
    margin_now = _margin(op_now, _value(panel, latest, "매출액", 0))
    margin_before = _margin(op_before, _value(panel, year_ago, "매출액", 0))
    if margin_now is not None and margin_before is not None:
        out["opm_change_q"] = round(margin_now - margin_before, 2)
    return out


def growth_factors(years: dict[str, dict[str, float]], quarterly: dict[str, Any] | None) -> dict[str, Any]:
    """`GROWTH_FACTORS` for one stock from its annual ``{year: {account: amount}}`` and quarter entry."""

    out: dict[str, Any] = dict.fromkeys(_FIELDS, None)
    for prefix, account in _SERIES:
        out[f"{prefix}_up_years"] = _up_years(years, account)
    out["ni_cagr_3y"] = _cagr(years, "당기순이익")
    out["op_cagr_3y"] = _cagr(years, "영업이익")
    if quarterly:
        out.update(_quarter_factors(quarterly["panel"], quarterly["period"]))
    return out
