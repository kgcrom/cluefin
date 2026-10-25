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
    "FRACTAL_N",
    "MIN_CANDLES",
    "IndexCloses",
    "IndexDateMismatch",
    "Pivot",
    "PriceArrays",
    "PriceFeatures",
    "Strength",
    "find_pivot",
    "fractal_highs",
    "price_features",
    "return_pct",
    "strength",
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
        volume_20_50=float(prices.volume[t - 19 :].mean() / prices.volume[t - 49 :].mean()),
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
