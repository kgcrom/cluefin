"""`ecos macro-snapshot`: the headline macro set, each reading against its own history.

Values, changes and percentiles only — no regime label (expansion/slowdown …). A label is a forecast rule, and this
repo only ships rules that passed an out-of-sample check (README §9). Every series keeps its own `as_of`: monthly
and quarterly statistics are published weeks after the period, so aligning them would hide the lag.
"""

from __future__ import annotations

from calendar import monthrange
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import date
from typing import Any

from cluefin_openapi.ecos import EcosAPIError, EcosAuthenticationError, EcosRateLimitError

__all__ = ["DERIVED", "SERIES", "Derived", "MacroSeries", "Point", "fetch_window", "summarize", "snapshot"]

Point = tuple[str, float]  # (ECOS TIME, value)


@dataclass(frozen=True, slots=True)
class MacroSeries:
    key: str
    name: str
    group: str
    stat_code: str
    cycle: str
    item_codes: tuple[str, ...]
    unit: str
    # "level": the published value. "yoy": % change from the same month a year earlier (CPI, exports).
    transform: str = "level"


# Codes checked against the live API on 2026-11-01 (docs/plans/ecos-forecast-plan.md).
SERIES: tuple[MacroSeries, ...] = (
    MacroSeries("base_rate", "한국은행 기준금리", "policy", "722Y001", "D", ("0101000",), "연%"),
    MacroSeries("ktb_3y", "국고채(3년)", "rates", "817Y002", "D", ("010200000",), "연%"),
    MacroSeries("ktb_10y", "국고채(10년)", "rates", "817Y002", "D", ("010210000",), "연%"),
    MacroSeries("corp_aa_3y", "회사채(3년, AA-)", "rates", "817Y002", "D", ("010300000",), "연%"),
    MacroSeries("corp_bbb_3y", "회사채(3년, BBB-)", "rates", "817Y002", "D", ("010320000",), "연%"),
    MacroSeries("usd_krw", "원/미국달러(매매기준율)", "fx", "731Y001", "D", ("0000001",), "원"),
    MacroSeries("cpi_yoy", "소비자물가 상승률(전년동월비)", "prices", "901Y009", "M", ("0",), "%", "yoy"),
    MacroSeries("leading_cycle", "선행지수 순환변동치", "cycle", "901Y067", "M", ("I16E",), "2020=100"),
    MacroSeries("coincident_cycle", "동행지수 순환변동치", "cycle", "901Y067", "M", ("I16D",), "2020=100"),
    MacroSeries("esi", "경제심리지수(순환변동치)", "sentiment", "513Y001", "M", ("E2000",), "지수"),
    MacroSeries("bsi_outlook", "기업경기 업황전망BSI(전산업)", "sentiment", "512Y014", "M", ("99988", "BA"), "지수"),
    MacroSeries("ccsi", "소비자심리지수(CCSI, 전체)", "sentiment", "511Y002", "M", ("FME", "99988"), "지수"),
    MacroSeries("news_sentiment", "뉴스심리지수(실험적 통계)", "sentiment", "523Y001", "D", ("A001",), "지수"),
    MacroSeries("gdp_qoq", "실질 GDP 성장률(계절조정, 전기비)", "growth", "200Y102", "Q", ("10111",), "%"),
    MacroSeries("exports_yoy", "수출금액 증가율(전년동월비)", "trade", "901Y118", "M", ("T002",), "%", "yoy"),
)


@dataclass(frozen=True, slots=True)
class Derived:
    key: str
    name: str
    group: str
    left: str
    right: str
    unit: str = "%p"

    @property
    def formula(self) -> str:
        return f"{self.left} - {self.right}"


DERIVED: tuple[Derived, ...] = (
    Derived("term_spread", "장단기 금리차(국고 10년 - 3년)", "rates", "ktb_10y", "ktb_3y"),
    Derived("credit_spread_aa", "신용스프레드(회사채 AA- - 국고 3년)", "rates", "corp_aa_3y", "ktb_3y"),
    Derived("credit_spread_bbb", "신용스프레드(회사채 BBB- - AA-)", "rates", "corp_bbb_3y", "corp_aa_3y"),
)

# Lookbacks for `change`, in months. A daily series compares with its last value on or before that day.
_CHANGES = {"Q": (("1q", 3), ("1y", 12))}
_DEFAULT_CHANGES = (("1m", 1), ("3m", 3), ("1y", 12))


def period_date(time: str) -> date:
    """ECOS TIME → the period's first day: 20261030, 202609, 2026Q3, 2026."""
    if len(time) == 8:
        return date(int(time[:4]), int(time[4:6]), int(time[6:]))
    if len(time) == 6 and time[4] == "Q":
        return date(int(time[:4]), (int(time[5]) - 1) * 3 + 1, 1)
    if len(time) == 6:
        return date(int(time[:4]), int(time[4:]), 1)
    return date(int(time[:4]), 1, 1)


def months_before(day: date, months: int) -> date:
    """`day` moved back by whole months, the day clamped to the month's end (Mar 31 − 1 month → Feb 28/29)."""
    year, month = divmod(day.year * 12 + day.month - 1 - months, 12)
    month += 1
    return date(year, month, min(day.day, monthrange(year, month)[1]))


def period_start(cycle: str, day: date) -> str:
    """The ECOS period string for `day` in `cycle` (D/M/Q)."""
    if cycle == "D":
        return f"{day:%Y%m%d}"
    if cycle == "Q":
        return f"{day.year}Q{(day.month - 1) // 3 + 1}"
    return f"{day:%Y%m}"


def year_over_year(points: Sequence[Point]) -> list[Point]:
    """Monthly level → % change from the same month a year earlier. Months without that base are dropped."""
    by_time = dict(points)
    out = []
    for time, value in points:
        base = by_time.get(f"{int(time[:4]) - 1}{time[4:]}")
        if base:
            out.append((time, (value / base - 1) * 100))
    return out


def _value_on_or_before(points: Sequence[Point], day: date) -> float | None:
    found = None
    for time, value in points:
        if period_date(time) > day:
            break
        found = value
    return found


def summarize(points: Sequence[Point], *, window_years: int, cycle: str = "D") -> dict[str, Any] | None:
    """Latest value, changes, and its percentile within the trailing window. Points must be in time order."""
    if not points:
        return None
    as_of, latest = points[-1]
    last_day = period_date(as_of)
    change = {}
    for label, months in _CHANGES.get(cycle, _DEFAULT_CHANGES):
        earlier = _value_on_or_before(points, months_before(last_day, months))
        change[label] = None if earlier is None else _round(latest - earlier)
    window_start = months_before(last_day, window_years * 12)
    window = [value for time, value in points if period_date(time) > window_start]
    below_or_equal = sum(1 for value in window if value <= latest)
    return {
        "value": _round(latest),
        "as_of": as_of,
        "change": change,
        "percentile": _round(below_or_equal / len(window) * 100, 1),
        "min": _round(min(window)),
        "max": _round(max(window)),
        "observations": len(window),
    }


def _round(value: float, digits: int = 3) -> float:
    return round(value, digits)


def align(left: Sequence[Point], right: Sequence[Point]) -> list[Point]:
    """`left - right` on the periods both have (holidays and late days drop out, never filled)."""
    right_by_time = dict(right)
    return [(time, value - right_by_time[time]) for time, value in left if time in right_by_time]


def fetch_window(series: MacroSeries, today: date, window_years: int) -> tuple[str, str]:
    """Start/end periods: the window plus one extra year for the 1y change and the year-over-year base."""
    start = months_before(today, (window_years + 1) * 12 + (12 if series.transform == "yoy" else 0))
    return period_start(series.cycle, start), period_start(series.cycle, today)


def snapshot(
    fetch: Callable[[MacroSeries], list[Point]],
    *,
    window_years: int,
) -> dict[str, Any]:
    """Run every series through `fetch` (which may raise) and summarize. Failures land in `missing`."""
    points: dict[str, list[Point]] = {}
    indicators = []
    missing = []
    for series in SERIES:
        try:
            raw = fetch(series)
        except (EcosAuthenticationError, EcosRateLimitError):
            # Every other series would fail the same way: let it become exit 3 / 5.
            raise
        except EcosAPIError as exc:
            missing.append({"key": series.key, "error": f"{type(exc).__name__}: {str(exc)[:200]}"})
            continue
        if len({time for time, _ in raw}) != len(raw):
            # The item codes do not pin one series (a table with a second item group): never average or pick.
            missing.append({"key": series.key, "error": "several rows per period; item_codes do not pin one series"})
            continue
        values = year_over_year(raw) if series.transform == "yoy" else raw
        summary = summarize(values, window_years=window_years, cycle=series.cycle)
        if summary is None:
            missing.append({"key": series.key, "error": "no data in the window"})
            continue
        points[series.key] = values
        indicators.append(
            {
                "key": series.key,
                "name": series.name,
                "group": series.group,
                "unit": series.unit,
                "transform": series.transform,
                "source": {"stat_code": series.stat_code, "cycle": series.cycle, "item_codes": list(series.item_codes)},
                **summary,
            }
        )
    derived = []
    for spec in DERIVED:
        if spec.left not in points or spec.right not in points:
            continue
        summary = summarize(align(points[spec.left], points[spec.right]), window_years=window_years)
        if summary is not None:
            derived.append(
                {"key": spec.key, "name": spec.name, "group": spec.group, "unit": spec.unit, "formula": spec.formula}
                | summary
            )
    return {"indicators": indicators, "derived": derived, "missing": missing}
