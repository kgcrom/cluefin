"""Trend-following setup features: trend template, 52-week range, fractal pivot, strength vs. index.

These are **ports, not re-derivations**, of the watchlist backtest (cluefin-factory
`scripts/watchlist/*.mjs` at `a5cfbcf`, archived 2026-10-18). Every threshold in the rules
only means something against these exact formulas, so two of them differ on purpose from
`indicators.py` and `cluefin-ta`:

- ATR is the plain 14-day mean of true range, not ta-lib's Wilder smoothing.
- The 52-week high/low leave out the day itself and use intraday highs/lows of the 250
  sessions before it.

That is why this module does not import `cluefin-ta`: its contract is ta-lib parity, and a
fractal pivot or a watchlist group has no ta-lib counterpart (the same reasoning keeps the
signal aggregation of `kis chart technical` in this CLI). Changing a formula here voids the
backtest evidence — rerun the backtest first.

Inputs are float arrays, oldest first (`PriceArrays`), so one stock from KIS and every stock
in the local cache go through the same code.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import date
from typing import Any

import numpy as np

from cluefin_openapi_cli.ohlcv import CandleSeries

__all__ = [
    "BASE_WINDOW",
    "CAVEATS",
    "RULES",
    "FRACTAL_N",
    "MIN_CANDLES",
    "IndexCloses",
    "IndexDateMismatch",
    "InsufficientHistory",
    "Pivot",
    "PriceArrays",
    "PriceFeatures",
    "Rules",
    "Strength",
    "analyze",
    "classify",
    "find_pivot",
    "floor_to_tick",
    "g2_score",
    "history",
    "levels",
    "fractal_highs",
    "price_features",
    "return_pct",
    "strength",
    "tick_size",
    "true_range",
    "weighted_return",
]

# 250 prior sessions for the 52-week range plus the day itself; also covers the 250-day return.
MIN_CANDLES = 251
FRACTAL_N = 3
# Contractions are counted from the highest high of this many sessions.
BASE_WINDOW = 60


def _day(value: Any) -> str:
    return value.strftime("%Y%m%d") if isinstance(value, date) else str(value)[:8]


def _array(values: Iterable[Any]) -> np.ndarray:
    return np.array([math.nan if value is None else value for value in values], dtype=np.float64)


@dataclass(frozen=True, slots=True)
class PriceArrays:
    """Daily bars of one stock, oldest first. ``value`` is traded value in won."""

    dates: tuple[str, ...]
    open: np.ndarray
    high: np.ndarray
    low: np.ndarray
    close: np.ndarray
    volume: np.ndarray
    value: np.ndarray

    def __len__(self) -> int:
        return len(self.dates)

    @classmethod
    def from_series(cls, series: CandleSeries) -> PriceArrays:
        arrays = series.arrays()
        return cls(
            dates=tuple(stamp[:8] for stamp in series.timestamps),
            open=arrays["open"],
            high=arrays["high"],
            low=arrays["low"],
            close=arrays["close"],
            volume=arrays["volume"],
            value=arrays["value"],
        )

    @classmethod
    def from_rows(cls, rows: Sequence[Sequence[Any]]) -> PriceArrays:
        """``(date, open, high, low, close, volume, value)`` rows, oldest first; ``None`` → NaN."""

        columns = list(zip(*rows, strict=True)) if rows else [()] * 7
        return cls(
            dates=tuple(_day(day) for day in columns[0]),
            open=_array(columns[1]),
            high=_array(columns[2]),
            low=_array(columns[3]),
            close=_array(columns[4]),
            volume=_array(columns[5]),
            value=_array(columns[6]),
        )

    def window(self, start: int | None = None, stop: int | None = None) -> PriceArrays:
        """Bars ``[start:stop]``, Python slice rules."""

        cut = slice(start, stop)
        return PriceArrays(
            dates=self.dates[cut],
            open=self.open[cut],
            high=self.high[cut],
            low=self.low[cut],
            close=self.close[cut],
            volume=self.volume[cut],
            value=self.value[cut],
        )


@dataclass(frozen=True, slots=True)
class IndexCloses:
    """Index closes, oldest first."""

    dates: tuple[str, ...]
    closes: np.ndarray

    @classmethod
    def from_pairs(cls, pairs: Iterable[tuple[Any, Any]]) -> IndexCloses:
        rows = sorted((_day(day), close) for day, close in pairs)
        return cls(dates=tuple(day for day, _ in rows), closes=_array(close for _, close in rows))


class IndexDateMismatch(LookupError):
    """The index has no close on the stock's last date — a data error, never filled from a nearby day."""

    def __init__(self, as_of: str) -> None:
        super().__init__(f"Index has no close on {as_of}.")
        self.as_of = as_of


# Like the original's reduce loops, max/min skip NaN (a missing bar) instead of propagating it.
def _max(values: np.ndarray) -> float:
    finite = values[~np.isnan(values)]
    return float(finite.max()) if finite.size else -math.inf


def _min(values: np.ndarray) -> float:
    finite = values[~np.isnan(values)]
    return float(finite.min()) if finite.size else math.inf


def _ratio(numerator: float, denominator: float) -> float:
    """NaN for a zero denominator (50 halted sessions have no volume) instead of a numpy warning."""

    return float(numerator / denominator) if denominator else math.nan


def _sma(values: np.ndarray, t: int, n: int) -> float:
    return float(values[t - n + 1 : t + 1].mean())


def true_range(high: np.ndarray, low: np.ndarray, close: np.ndarray, i: int) -> float:
    """max(high−low, |high−prevClose|, |low−prevClose|); the first bar has no previous close."""

    if i == 0:
        return float(high[0] - low[0])
    prev = close[i - 1]
    return float(max(high[i] - low[i], abs(high[i] - prev), abs(low[i] - prev)))


def weighted_return(closes: np.ndarray, t: int | None = None) -> float | None:
    """IBD-style weighted return, the last quarter counted twice. None before 251 bars.

    Comparing it between a stock and its index is the same comparison as their RS
    percentiles, because a percentile only ranks this number.
    """

    t = len(closes) - 1 if t is None else t
    if t < 250:
        return None
    c = closes[t]
    return float(2 * (c / closes[t - 63]) + c / closes[t - 126] + c / closes[t - 189] + c / closes[t - 250])


def return_pct(closes: np.ndarray, n: int, t: int | None = None) -> float | None:
    """Return over ``n`` sessions in %, or None when the series is shorter."""

    t = len(closes) - 1 if t is None else t
    return None if t < n else float((closes[t] / closes[t - n] - 1) * 100)


@dataclass(frozen=True, slots=True)
class PriceFeatures:
    date: str
    close: float
    sma_50: float
    sma_150: float
    sma_200: float
    sma_200_rising: bool
    high_52w: float
    low_52w: float
    gap_to_high_pct: float
    from_low_pct: float
    template: bool
    return_21d_pct: float
    weighted_return: float
    range_10d_pct: float
    atr14_pct: float
    volume_20_50: float
    traded_value_20d_eok: float
    dist_sma50_pct: float
    depth_60d_pct: float

    def template_checks(self) -> list[tuple[str, bool]]:
        """Minervini's trend template, one ``(rule, pass)`` per condition."""

        return _template_checks(
            self.close,
            self.sma_50,
            self.sma_150,
            self.sma_200,
            self.sma_200_rising,
            self.from_low_pct,
            self.gap_to_high_pct,
        )


def _template_checks(
    c: float, sma_50: float, sma_150: float, sma_200: float, rising: bool, from_low: float, gap: float
) -> list[tuple[str, bool]]:
    return [
        ("close > sma_150", c > sma_150),
        ("close > sma_200", c > sma_200),
        ("sma_150 > sma_200", sma_150 > sma_200),
        ("sma_200 rising (20 sessions)", rising),
        ("sma_50 > sma_150", sma_50 > sma_150),
        ("close > sma_50", c > sma_50),
        ("from 52w low >= 25%", from_low >= 25),
        ("52w high gap >= -25%", gap >= -25),
    ]


def price_features(prices: PriceArrays) -> PriceFeatures | None:
    """Features of the last bar, or None with fewer than ``MIN_CANDLES`` bars."""

    if len(prices) < MIN_CANDLES:
        return None
    t = len(prices) - 1
    close, high, low = prices.close, prices.high, prices.low
    c = float(close[t])
    sma_50, sma_150, sma_200 = _sma(close, t, 50), _sma(close, t, 150), _sma(close, t, 200)
    sma_200_rising = bool(sma_200 > _sma(close, t - 20, 200))
    high_52w = _max(high[t - 250 : t])
    low_52w = _min(low[t - 250 : t])
    gap = (c / high_52w - 1) * 100
    from_low = (c / low_52w - 1) * 100
    checks = _template_checks(c, sma_50, sma_150, sma_200, sma_200_rising, from_low, gap)
    high_10, high_60 = _max(high[t - 9 :]), _max(high[t - 59 :])
    atr14 = sum(true_range(high, low, close, i) for i in range(t - 13, t + 1)) / 14
    return PriceFeatures(
        date=prices.dates[t],
        close=c,
        sma_50=sma_50,
        sma_150=sma_150,
        sma_200=sma_200,
        sma_200_rising=sma_200_rising,
        high_52w=high_52w,
        low_52w=low_52w,
        gap_to_high_pct=gap,
        from_low_pct=from_low,
        template=all(bool(passed) for _, passed in checks),
        # t >= 250 here, so neither can be None.
        return_21d_pct=float(return_pct(close, 21) or 0.0),
        weighted_return=float(weighted_return(close) or math.nan),
        range_10d_pct=(high_10 - _min(low[t - 9 :])) / high_10 * 100,
        atr14_pct=atr14 / c * 100,
        volume_20_50=_ratio(prices.volume[t - 19 :].mean(), prices.volume[t - 49 :].mean()),
        traded_value_20d_eok=float(prices.value[t - 19 :].mean() / 1e8),
        dist_sma50_pct=(c / sma_50 - 1) * 100,
        depth_60d_pct=(1 - _min(low[t - 59 :]) / high_60) * 100,
    )


def fractal_highs(highs: np.ndarray, n: int = FRACTAL_N) -> list[int]:
    """Indices of confirmed fractal highs, oldest first.

    A high strictly above the ``n`` bars on its left and not below the ``n`` on its right
    (the asymmetry is the original's). The last ``n`` bars can never qualify, so nothing
    looks past the last bar.
    """

    out = []
    for i in range(n, len(highs) - n):
        h = highs[i]
        # Written as "fails if" so a NaN neighbour does not disqualify, as in the original.
        if not any(highs[i - k] >= h or highs[i + k] > h for k in range(1, n + 1)):
            out.append(i)
    return out


@dataclass(frozen=True, slots=True)
class Pivot:
    price: float
    date: str
    age: int
    last_contraction_pct: float
    legs: tuple[float, ...]

    @property
    def contractions(self) -> int:
        return len(self.legs)


def _depth(high: np.ndarray, low: np.ndarray, a: int, b: int) -> float:
    """Drop from the high at ``a`` to the lowest low strictly after it and before ``b``, in %."""

    return (1 - _min(low[a + 1 : b]) / high[a]) * 100


def find_pivot(prices: PriceArrays, n: int = FRACTAL_N, base_window: int = BASE_WINDOW) -> Pivot | None:
    """The most recent fractal high and the contractions of the base in front of it.

    ``last_contraction_pct`` leaves out the pivot bar's own low. ``legs`` has one depth per
    swing high since the highest high of the last ``base_window`` bars.
    """

    high, low = prices.high, prices.low
    t = len(high) - 1
    known = fractal_highs(high, n)
    if not known:
        return None
    p = known[-1]
    start = max(0, t + 1 - base_window)
    for i in range(start + 1, t + 1):
        if high[i] > high[start]:
            start = i
    swings = [start, *(i for i in known if i > start)]
    ends = [*swings[1:], t + 1]
    legs = tuple(_depth(high, low, a, b) for a, b in zip(swings, ends, strict=True) if b > a + 1)
    return Pivot(
        price=float(high[p]),
        date=prices.dates[p],
        age=t - p,
        last_contraction_pct=_depth(high, low, p, t + 1),
        legs=legs,
    )


@dataclass(frozen=True, slots=True)
class Strength:
    rel: float
    excess_21d_pp: float
    weighted_return: float
    index_weighted_return: float
    return_21d_pct: float
    index_return_21d_pct: float


def strength(prices: PriceArrays, index: IndexCloses) -> Strength | None:
    """Stock vs. its own market index: weighted-return ratio and 21-session excess return.

    The index is read on the stock's last date and cut there; each series counts its own
    positions (a halted stock with fewer bars is compared over a different span — as in the
    backtest). Raises ``IndexDateMismatch`` when the index lacks that date. None when either
    series has fewer than 251 values.
    """

    as_of = prices.dates[-1]
    try:
        at = index.dates.index(as_of)
    except ValueError:
        raise IndexDateMismatch(as_of) from None
    index_closes = index.closes[: at + 1]
    stock_raw = weighted_return(prices.close)
    index_raw = weighted_return(index_closes)
    if stock_raw is None or index_raw is None:
        return None
    # 251 values cover 21 sessions, so neither return is None.
    stock_21 = float(return_pct(prices.close, 21) or 0.0)
    index_21 = float(return_pct(index_closes, 21) or 0.0)
    return Strength(
        rel=stock_raw / index_raw,
        excess_21d_pp=stock_21 - index_21,
        weighted_return=stock_raw,
        index_weighted_return=index_raw,
        return_21d_pct=stock_21,
        index_return_21d_pct=index_21,
    )


# ---------------------------------------------------------------------------
# Groups, action and price levels (factory `classify.mjs`)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Rules:
    """Every number here was set by the backtest; § is the section of the README's trend-setup rules.

    The numbers live only here — the README explains them and does not keep a second copy.
    """

    # §2 공통: 20일 평균 거래대금(억원) 하한. 이보다 얇으면 체결·손절이 백테스트대로 안 된다.
    min_traded_value: float = 10
    # §4 지수 대비 강도: 지수보다 강해야 한다(원고의 "종목 RS > 지수 RS").
    rel_floor: float = 1.0
    # §4 백분위 RS 90 의 기간 중앙값. 넘으면 과열(1그룹) 쪽이다.
    rel_ceiling: float = 1.32
    # §2 1그룹: 52주 고점 대비 하한(%), 이만큼 출렁이거나(10일 고저폭 %) 50일선에서 떨어져 있으면(%) 과열.
    g1_max_gap: float = -20
    g1_range10: float = 15
    g1_dist_sma50: float = 25
    # §2 2그룹: 52주 저점 대비 상승률(%) 구간 — Stage 2 초입.
    g2_from_low_min: float = 30
    g2_from_low_max: float = 150
    # §3 3그룹(수축 완료).
    g3_min_contractions: int = 3
    g3_max_last_contraction: float = 10
    g3_max_range10: float = 12
    g3_max_gap: float = -20
    # §3 백테스트 셋업은 종가가 피봇 아래 8% 안일 때만 잡았다.
    g3_max_below_pivot: float = -8
    # §6 주문.
    alert_below_pivot: float = 0.03
    chase_limit: float = 0.05
    stop_loss: float = 0.08
    take_profit: float = 0.24
    # §5 2그룹 점수가 이 이상이면 3그룹 후보.
    g2_candidate_score: int = 6


RULES = Rules()

# KRX tick size, one table for KOSPI and KOSDAQ since 2023-01-25: (upper bound, tick).
_TICKS = ((2000, 1), (5000, 5), (20000, 10), (50000, 50), (200000, 100), (500000, 500))


def tick_size(price: float) -> int:
    return next((tick for bound, tick in _TICKS if price < bound), 1000)


def floor_to_tick(price: float) -> float:
    """Round down to a valid quote."""

    tick = tick_size(price)
    return float(math.floor(price / tick) * tick)


def levels(pivot_price: float) -> dict[str, float]:
    """§6: alert, buy stop, chase limit, stop loss and the 3R target, on valid ticks.

    The buy stop is the pivot itself, not floored — the pivot is a traded high, already a valid quote.
    """

    return {
        "alert": floor_to_tick(pivot_price * (1 - RULES.alert_below_pivot)),
        "buy_stop": pivot_price,
        "chase_limit": floor_to_tick(pivot_price * (1 + RULES.chase_limit)),
        "stop_loss": floor_to_tick(pivot_price * (1 - RULES.stop_loss)),
        "take_profit": floor_to_tick(pivot_price * (1 + RULES.take_profit)),
    }


def _check(check_id: str, rule: str, value: Any, passed: Any) -> dict[str, Any]:
    """``id`` is for agents to branch on; ``rule`` is the Korean line a person reads."""

    return {"id": check_id, "rule": rule, "value": value, "pass": bool(passed)}


def _all_pass(checks: list[dict[str, Any]]) -> bool:
    return all(check["pass"] for check in checks)


def g2_score(f: PriceFeatures, s: Strength) -> dict[str, Any]:
    """§5: seven conditions that made a group-2 stock more likely to become a group-3 breakout."""

    items = [
        _check("score.range10", "10일 고저폭 ≤ 12%", f.range_10d_pct, f.range_10d_pct <= 12),
        _check("score.atr14", "ATR14 ≤ 4.5%", f.atr14_pct, f.atr14_pct <= 4.5),
        _check("score.depth60", "60일 깊이 ≤ 30%", f.depth_60d_pct, f.depth_60d_pct <= 30),
        _check("score.dist_sma50", "50일선 이격 ≤ 10%", f.dist_sma50_pct, f.dist_sma50_pct <= 10),
        _check("score.excess_21d", "지수 대비 21일 초과수익 ≤ 5.5%p", s.excess_21d_pp, s.excess_21d_pp <= 5.5),
        _check("score.from_low", "52주 저점 대비 ≤ 100%", f.from_low_pct, f.from_low_pct <= 100),
        _check("score.gap", "52주 고점 −15% 이내", f.gap_to_high_pct, f.gap_to_high_pct >= -15),
    ]
    score = sum(1 for item in items if item["pass"])
    return {"score": score, "of": len(items), "candidate": score >= RULES.g2_candidate_score, "items": items}


def _group_checks(f: PriceFeatures, pv: Pivot | None, s: Strength) -> dict[str, Any]:
    r = RULES
    liquid = _check(
        "liquid",
        f"거래대금 ≥ {r.min_traded_value:g}억",
        f.traded_value_20d_eok,
        f.traded_value_20d_eok >= r.min_traded_value,
    )
    g1 = [
        _check("g1.rel_ceiling", f"지수 대비 ≥ {r.rel_ceiling:g}", s.rel, s.rel >= r.rel_ceiling),
        _check("g1.gap", f"52주 고점 {r.g1_max_gap:g}% 이내", f.gap_to_high_pct, f.gap_to_high_pct >= r.g1_max_gap),
        _check(
            "g1.overheat",
            f"10일 고저폭 > {r.g1_range10:g}% 또는 50일선 이격 > {r.g1_dist_sma50:g}%",
            {"range_10d_pct": f.range_10d_pct, "dist_sma50_pct": f.dist_sma50_pct},
            f.range_10d_pct > r.g1_range10 or f.dist_sma50_pct > r.g1_dist_sma50,
        ),
    ]
    lo, hi = r.g2_from_low_min, r.g2_from_low_max
    g2 = [
        _check("g2.template", "정배열(트렌드 템플릿)", f.template, f.template),
        _check("g2.from_low", f"52주 저점 대비 {lo:g}~{hi:g}%", f.from_low_pct, lo <= f.from_low_pct <= hi),
        _check("g2.rel_floor", f"지수 대비 > {r.rel_floor:g}", s.rel, s.rel > r.rel_floor),
    ]
    contractions = pv.contractions if pv else 0
    g3 = [
        {**liquid, "id": "g3.liquid"},
        _check(
            "g3.contractions", f"수축 ≥ {r.g3_min_contractions}회", contractions, contractions >= r.g3_min_contractions
        ),
        _check(
            "g3.last_contraction",
            f"마지막 수축 ≤ {r.g3_max_last_contraction:g}%",
            pv.last_contraction_pct if pv else None,
            pv is not None and pv.last_contraction_pct <= r.g3_max_last_contraction,
        ),
        _check(
            "g3.range10", f"10일 고저폭 ≤ {r.g3_max_range10:g}%", f.range_10d_pct, f.range_10d_pct <= r.g3_max_range10
        ),
        _check("g3.gap", f"52주 고점 {r.g3_max_gap:g}% 이내", f.gap_to_high_pct, f.gap_to_high_pct >= r.g3_max_gap),
        _check(
            "g3.rel_band",
            f"지수 대비 {r.rel_floor:g} 초과 {r.rel_ceiling:g} 미만",
            s.rel,
            r.rel_floor < s.rel < r.rel_ceiling,
        ),
    ]
    return {"liquid": liquid, "g1": g1, "g2": g2, "g3": g3}


def _decide(groups: dict[str, bool], liquid: bool, to_pivot: float | None, candidate: bool) -> tuple[str, str, str]:
    """``(action, status, reason)``, decided once in the original order."""

    if not liquid:
        return "exclude", "illiquid", "거래대금이 얇아 백테스트 대상 밖"
    if groups["g1"]:
        return "exclude", "overheated", "1그룹(과열) — 이 자리 돌파는 우위가 없었다"
    if groups["g3"] and to_pivot is not None:
        if to_pivot >= RULES.chase_limit * 100:
            return "watch", "extended", "피봇 +5% 초과 — 추격 금지"
        # A close exactly on the pivot has not broken out; the buy stop is still the next step.
        if to_pivot > 0:
            return "watch", "breaking_out", "이미 피봇 위(추격 한도 안) — 백테스트는 피봇 아래에서 셋업을 잡았다"
        if to_pivot < RULES.g3_max_below_pivot:
            return "watch", "far_below_pivot", "피봇에서 8% 넘게 아래"
        return "alert", "setup", "3그룹 — 피봇 아래 알림, 피봇에서 매수 스톱"
    if groups["g2"]:
        if candidate:
            return "watch", "g3_candidate", "2그룹 — 점수가 높아 3그룹 후보"
        return "watch", "g2", "2그룹 — 수축을 기다린다"
    return "exclude", "no_group", "어느 그룹 조건도 채우지 못함"


def classify(f: PriceFeatures, pv: Pivot | None, s: Strength) -> dict[str, Any]:
    """Groups (they can overlap), the per-rule checks behind them, and one action.

    The action is decided once: illiquid → exclude, group 1 → exclude, group 3 → alert/watch
    by distance to the pivot, group 2 → watch, nothing → exclude.
    """

    checks = _group_checks(f, pv, s)
    groups = {name: _all_pass(checks[name]) for name in ("g1", "g2", "g3")}
    score = g2_score(f, s)
    to_pivot = (f.close / pv.price - 1) * 100 if pv else None
    action, status, reason = _decide(groups, checks["liquid"]["pass"], to_pivot, score["candidate"])
    return {
        "groups": groups,
        "action": action,
        "status": status,
        "reason": reason,
        "checks": checks,
        "g2_score": score,
        "to_pivot_pct": to_pivot,
        "levels": levels(pv.price) if pv else None,
    }


# ---------------------------------------------------------------------------
# One stock's full reading (shared by `kis chart trend-setup` and `cache trend-setup`)
# ---------------------------------------------------------------------------

RULES_VERSION = "2026-10"
CAVEATS = (
    "규칙은 2021-10~2026-10 5년 백테스트(폐지 포함)에서 나왔다 — 3그룹 다음 날 피봇 돌파 1,512건 평균 +0.13R, "
    "1·2그룹 매수는 모든 규칙에서 마이너스였다.",
    "장중 트리거(돌파일 거래량, 업종 동반 상승)는 판정에 없다 — 매수 당일 직접 확인.",
    "폭락 뒤 V자 반등장의 짧은 베이스 돌파는 3그룹으로 잡지 않는다(10일 고저폭 ≤ 12%, 대부분 1그룹 과열).",
    "action 은 매수 추천이 아니다 — alert 는 피봇 아래 알림을 걸 자리라는 뜻이다.",
)


class InsufficientHistory(ValueError):
    """Fewer than ``MIN_CANDLES`` bars for the stock (``which="stock"``) or its index (``"index"``)."""

    def __init__(self, which: str, count: int) -> None:
        super().__init__(f"{which} has {count} bars; trend-setup needs {MIN_CANDLES}.")
        self.which = which
        self.count = count


def _clean(value: Any, digits: int = 4) -> Any:
    """Round floats for output; NaN/inf become None so JSON stays valid. Recurses into dicts/lists."""

    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, float | np.floating):
        return None if math.isnan(value) or math.isinf(value) else round(float(value), digits)
    if isinstance(value, dict):
        return {key: _clean(item, digits) for key, item in value.items()}
    if isinstance(value, list | tuple):
        return [_clean(item, digits) for item in value]
    return value


def analyze(prices: PriceArrays, index: IndexCloses) -> dict[str, Any]:
    """Every reading of the last bar plus the setup, as output-ready (rounded) values.

    Raises ``InsufficientHistory`` and ``IndexDateMismatch``; callers turn them into exit codes.
    """

    f = price_features(prices)
    if f is None:
        raise InsufficientHistory("stock", len(prices))
    s = strength(prices, index)
    if s is None:
        raise InsufficientHistory("index", index.dates.index(prices.dates[-1]) + 1)
    pv = find_pivot(prices)
    setup = classify(f, pv, s)
    return {
        "as_of": f.date,
        "candle_count": len(prices),
        "close": f.close,
        "trend": {
            "sma_50": _clean(f.sma_50, 2),
            "sma_150": _clean(f.sma_150, 2),
            "sma_200": _clean(f.sma_200, 2),
            "sma_200_rising": f.sma_200_rising,
            "template": f.template,
            "template_checks": [{"rule": rule, "pass": bool(passed)} for rule, passed in f.template_checks()],
        },
        "range_52w": _clean(
            {
                "high": f.high_52w,
                "low": f.low_52w,
                "gap_to_high_pct": f.gap_to_high_pct,
                "from_low_pct": f.from_low_pct,
            }
        ),
        "volatility": _clean(
            {
                "atr14_pct": f.atr14_pct,
                "range_10d_pct": f.range_10d_pct,
                "depth_60d_pct": f.depth_60d_pct,
                "dist_sma50_pct": f.dist_sma50_pct,
            }
        ),
        "volume": _clean({"volume_20_50": f.volume_20_50, "traded_value_20d_eok": f.traded_value_20d_eok}),
        "pivot": _clean(
            {
                "price": pv.price,
                "date": pv.date,
                "age": pv.age,
                "last_contraction_pct": pv.last_contraction_pct,
                "contractions": pv.contractions,
                "legs": list(pv.legs),
                "to_pivot_pct": setup["to_pivot_pct"],
            }
        )
        if pv
        else None,
        "strength": _clean(
            {
                "rel": s.rel,
                "excess_21d_pp": s.excess_21d_pp,
                "weighted_return": s.weighted_return,
                "index_weighted_return": s.index_weighted_return,
                "return_21d_pct": s.return_21d_pct,
                "index_return_21d_pct": s.index_return_21d_pct,
            }
        ),
        "setup": _clean({key: setup[key] for key in ("groups", "action", "status", "reason", "checks", "g2_score")}),
        "levels": setup["levels"],
        "rules": {"version": RULES_VERSION, "source": "apps/cluefin-openapi-cli/README.md#trend-setup"},
        "caveats": list(CAVEATS),
    }


# ---------------------------------------------------------------------------
# State history: the judgement keeps no state, so the past is recomputed from the bars
# ---------------------------------------------------------------------------

# Bars per judgement, as `kis chart trend-setup` fetches; history needs this many before each past day.
WINDOW = 260
HISTORY_DAYS = 20
G1_LOOKBACK = 60
# A state that lasted this many days or fewer is a flicker, skipped when looking for the previous one.
_FLICKER_DAYS = 2


def _state(setup: dict[str, Any]) -> str:
    """One state per day in the backtest's priority: illiquid → g1 → g3 → g2 → none."""

    if not setup["checks"]["liquid"]["pass"]:
        return "illiquid"
    groups = setup["groups"]
    return next((name for name in ("g1", "g3", "g2") if groups[name]), "none")


def _judge(prices: PriceArrays, index: IndexCloses, end: int) -> tuple[str, Pivot | None] | None:
    """State and pivot on bar ``end - 1`` from the ``WINDOW`` bars up to it; None when not computable."""

    window = prices.window(start=max(0, end - WINDOW), stop=end)
    f = price_features(window)
    if f is None:
        return None
    try:
        s = strength(window, index)
    except IndexDateMismatch:
        return None
    if s is None:
        return None
    pv = find_pivot(window)
    return _state(classify(f, pv, s)), pv


def _was_g1(prices: PriceArrays, index: IndexCloses, end: int) -> bool:
    """State g1 on bar ``end - 1`` — features and strength only, no pivot (g1 does not use it)."""

    window = prices.window(start=max(0, end - WINDOW), stop=end)
    f = price_features(window)
    if f is None:
        return False
    try:
        s = strength(window, index)
    except IndexDateMismatch:
        return False
    if s is None:
        return False
    r = RULES
    return bool(
        f.traded_value_20d_eok >= r.min_traded_value
        and s.rel >= r.rel_ceiling
        and f.gap_to_high_pct >= r.g1_max_gap
        and (f.range_10d_pct > r.g1_range10 or f.dist_sma50_pct > r.g1_dist_sma50)
    )


def _runs(states: list[str | None]) -> list[tuple[str | None, int, int]]:
    """``(state, first index, length)`` runs, oldest first."""

    runs: list[tuple[str | None, int, int]] = []
    for i, state in enumerate(states):
        if runs and runs[-1][0] == state:
            first = runs[-1][1]
            runs[-1] = (state, first, i - first + 1)
        else:
            runs.append((state, i, 1))
    return runs


def history(
    prices: PriceArrays, index: IndexCloses, *, days: int = HISTORY_DAYS, g1_lookback: int = G1_LOOKBACK
) -> dict[str, Any]:
    """Recent state history of the last bar (plan 4-9). Facts only; nothing here feeds the judgement.

    - ``status_days``: sessions the current state has lasted (today included), capped at ``days``.
    - ``prev_status``/``prev_status_date``: the state before it and its last day, skipping flickers
      (≤ 2 days) and runs of the current state; None when it lies beyond ``days``.
    - ``g1_within_60d``/``last_g1_date``: g1 in the ``g1_lookback`` sessions before today.
    - ``exit``: when yesterday was g3 and today is not — ``breakout`` (close ≥ yesterday's pivot),
      ``breakdown`` (close below the stop-loss line) or ``faded``.
    """

    n = len(prices)
    judged = [_judge(prices, index, end) for end in range(max(1, n - days + 1), n + 1)]
    dates = prices.dates[n - len(judged) :]
    states = [item[0] if item else None for item in judged]
    runs = _runs(states)
    current, first, length = runs[-1]
    prev_status = prev_date = None
    for state, start, run_length in reversed(runs[:-1]):
        if state is None or start == 0 and run_length <= _FLICKER_DAYS:
            break  # unknown, or a short run cut by the window: cannot tell a flicker from a state
        if state != current and run_length > _FLICKER_DAYS:
            prev_status, prev_date = state, dates[start + run_length - 1]
            break
    exit_kind = None
    if len(judged) >= 2 and judged[-2] and judged[-2][0] == "g3" and current != "g3" and judged[-2][1]:
        pivot_price, close = judged[-2][1].price, float(prices.close[-1])
        if close >= pivot_price:
            exit_kind = "breakout"
        elif close < pivot_price * (1 - RULES.stop_loss):
            exit_kind = "breakdown"
        else:
            exit_kind = "faded"
    last_g1 = next(
        (prices.dates[end - 1] for end in range(n - 1, max(0, n - 1 - g1_lookback), -1) if _was_g1(prices, index, end)),
        None,
    )
    return {
        "state": current,
        "status_days": length,
        "status_days_capped": first == 0 and length == days,
        "prev_status": prev_status,
        "prev_status_date": prev_date,
        "g1_within_60d": last_g1 is not None,
        "last_g1_date": last_g1,
        "exit": exit_kind,
    }
