"""Indicator composition and signal aggregation over `cluefin-ta`.

This is the layer that earns the command: it turns a few hundred candles into a few
dozen numbers, so an agent never has to pull an OHLCV table through its context just to
learn what RSI is doing.

Raw indicator math is **not** reimplemented here — `cluefin-ta` owns that and holds a
bit-for-bit TA-Lib parity contract. This module only composes those primitives and
aggregates them. The aggregation deliberately stays here rather than moving into
`cluefin-ta`: a signal score has no TA-Lib counterpart, so it could never be
parity-tested, and adding it there would break that package's one contract.

Note for anyone comparing numbers against `cluefin-desk`: they will not match. desk
computes EMAs through pandas `ewm(span=N)`, which starts at the first sample with no
warm-up gap, while `cluefin-ta` follows TA-Lib's convention of seeding from an SMA and
emitting `N-1` leading NaNs. `cluefin-ta`'s definition is the reference here.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Callable

import numpy as np
from cluefin_ta import ADX, ATR, BBANDS, MACD, MDD, OBV, RSI, SHARPE, SMA, STOCH

from cluefin_openapi_cli.ohlcv import CandleSeries

__all__ = [
    "IndicatorSet",
    "MIN_CANDLES",
    "SignalRule",
    "analyze",
    "compute_indicators",
    "score_signals",
]

# The longest warm-up any configured indicator needs is SMA(60); below that the slow MA
# is all NaN and the trend rules silently stop voting. Refuse instead, so a short series
# is an explicit error rather than a quietly half-blind answer.
MIN_CANDLES = 60

# Aggregation thresholds. These are heuristics chosen for legibility, not a backtested
# strategy — the per-rule votes are the substance, and the scores are only a summary of
# how many rules agree. A caller that wants a different sensitivity should read the
# votes rather than asking for the threshold to be tuned.
_STRONG = 0.4

_TRADING_DAYS_PER_YEAR = 252


def _last(values: np.ndarray) -> float:
    """Return the final element, or NaN for an empty array."""

    if values.size == 0:
        return math.nan
    return float(values[-1])


def _clean(value: float, digits: int = 4) -> float | None:
    """Round for compact output; NaN/inf become None so JSON stays valid."""

    if value is None or math.isnan(value) or math.isinf(value):
        return None
    return round(value, digits)


@dataclass(frozen=True, slots=True)
class SignalRule:
    """One named vote in ``[-1, 0, 1]``, with the reading that produced it.

    ``vote`` is ``None`` when the rule could not be evaluated (its indicator was still
    in its NaN warm-up). Such rules are excluded from the score rather than counted as
    neutral, so a short series weakens confidence instead of biasing it toward HOLD.
    """

    name: str
    vote: int | None
    reason: str


@dataclass(frozen=True, slots=True)
class IndicatorSet:
    """Final values of every configured indicator, plus the series context."""

    as_of: str
    candle_count: int
    missing_count: int
    close: float
    values: dict[str, Any]


def compute_indicators(series: CandleSeries) -> IndicatorSet:
    """Compute every configured indicator and keep only the final reading of each.

    Only the last value of each series is retained on purpose: the full curve is exactly
    the bulk this command exists to avoid sending back.
    """

    if len(series) < MIN_CANDLES:
        raise ValueError(f"Need at least {MIN_CANDLES} candles for indicators; got {len(series)}.")

    arrays = series.arrays()
    close, high, low, volume = arrays["close"], arrays["high"], arrays["low"], arrays["volume"]

    macd_line, macd_signal, macd_hist = MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    upper, middle, lower = BBANDS(close, timeperiod=20, nbdevup=2.0, nbdevdn=2.0)
    slow_k, slow_d = STOCH(high, low, close)

    last_close = _last(close)
    bb_upper, bb_lower = _last(upper), _last(lower)
    band_width = bb_upper - bb_lower

    values: dict[str, Any] = {
        "sma_5": _clean(_last(SMA(close, timeperiod=5)), 2),
        "sma_20": _clean(_last(SMA(close, timeperiod=20)), 2),
        "sma_60": _clean(_last(SMA(close, timeperiod=60)), 2),
        "rsi_14": _clean(_last(RSI(close, timeperiod=14)), 2),
        "macd": {
            "macd": _clean(_last(macd_line)),
            "signal": _clean(_last(macd_signal)),
            "histogram": _clean(_last(macd_hist)),
        },
        "bbands_20": {
            "upper": _clean(bb_upper, 2),
            "middle": _clean(_last(middle), 2),
            "lower": _clean(bb_lower, 2),
            # Where the close sits inside the band: 0 at the lower band, 1 at the upper.
            # Degenerate (zero-width) bands would divide by zero, so they stay None.
            "percent_b": _clean((last_close - bb_lower) / band_width) if band_width > 0 else None,
        },
        "stoch": {"slow_k": _clean(_last(slow_k), 2), "slow_d": _clean(_last(slow_d), 2)},
        "adx_14": _clean(_last(ADX(high, low, close, timeperiod=14)), 2),
        "atr_14": _clean(_last(ATR(high, low, close, timeperiod=14)), 2),
        "obv": _clean(_last(OBV(close, volume)), 0),
    }

    returns = np.diff(close) / close[:-1] if close.size > 1 else np.array([], dtype=np.float64)
    finite_returns = returns[np.isfinite(returns)]
    if finite_returns.size > 1:
        values["mdd"] = _clean(float(MDD(finite_returns)))
        values["sharpe"] = _clean(float(SHARPE(finite_returns, periods_per_year=_TRADING_DAYS_PER_YEAR)))
    else:
        values["mdd"] = None
        values["sharpe"] = None

    return IndicatorSet(
        as_of=series.candles[-1].timestamp,
        candle_count=len(series),
        missing_count=series.missing_count,
        close=last_close,
        values=values,
    )


# ---------------------------------------------------------------------------
# Signal rules
# ---------------------------------------------------------------------------


def _rule_rsi(indicators: IndicatorSet) -> SignalRule:
    rsi = indicators.values["rsi_14"]
    if rsi is None:
        return SignalRule("rsi", None, "RSI unavailable")
    if rsi < 30:
        return SignalRule("rsi", 1, f"RSI {rsi} below 30 (oversold)")
    if rsi > 70:
        return SignalRule("rsi", -1, f"RSI {rsi} above 70 (overbought)")
    return SignalRule("rsi", 0, f"RSI {rsi} in the 30-70 band")


def _rule_macd(indicators: IndicatorSet) -> SignalRule:
    histogram = indicators.values["macd"]["histogram"]
    if histogram is None:
        return SignalRule("macd", None, "MACD unavailable")
    if histogram > 0:
        return SignalRule("macd", 1, f"MACD histogram {histogram} above zero")
    if histogram < 0:
        return SignalRule("macd", -1, f"MACD histogram {histogram} below zero")
    return SignalRule("macd", 0, "MACD histogram flat at zero")


def _rule_ma_stack(indicators: IndicatorSet) -> SignalRule:
    values = indicators.values
    fast, mid, slow = values["sma_5"], values["sma_20"], values["sma_60"]
    if None in (fast, mid, slow):
        return SignalRule("ma_stack", None, "Moving averages unavailable")
    close = indicators.close
    if close > fast > mid > slow:
        return SignalRule("ma_stack", 1, "Close above a rising 5 > 20 > 60 stack")
    if close < fast < mid < slow:
        return SignalRule("ma_stack", -1, "Close below a falling 5 < 20 < 60 stack")
    return SignalRule("ma_stack", 0, "Moving averages are not stacked in either direction")


def _rule_bbands(indicators: IndicatorSet) -> SignalRule:
    bands = indicators.values["bbands_20"]
    upper, lower = bands["upper"], bands["lower"]
    if upper is None or lower is None:
        return SignalRule("bbands", None, "Bollinger bands unavailable")
    close = indicators.close
    if close <= lower:
        return SignalRule("bbands", 1, f"Close {close} at or below the lower band {lower}")
    if close >= upper:
        return SignalRule("bbands", -1, f"Close {close} at or above the upper band {upper}")
    return SignalRule("bbands", 0, "Close inside the bands")


def _rule_stoch(indicators: IndicatorSet) -> SignalRule:
    slow_k = indicators.values["stoch"]["slow_k"]
    if slow_k is None:
        return SignalRule("stoch", None, "Stochastic unavailable")
    if slow_k < 20:
        return SignalRule("stoch", 1, f"Stochastic %K {slow_k} below 20 (oversold)")
    if slow_k > 80:
        return SignalRule("stoch", -1, f"Stochastic %K {slow_k} above 80 (overbought)")
    return SignalRule("stoch", 0, f"Stochastic %K {slow_k} in the 20-80 band")


_TREND_RULES: tuple[Callable[[IndicatorSet], SignalRule], ...] = (_rule_macd, _rule_ma_stack)
_MEAN_REVERSION_RULES: tuple[Callable[[IndicatorSet], SignalRule], ...] = (_rule_rsi, _rule_bbands, _rule_stoch)


def _family_score(rules: list[SignalRule], labels: tuple[str, str, str]) -> dict[str, Any]:
    """Mean of the evaluable votes in one family, plus its label.

    The mean — not the sum — so a warm-up NaN that silences one rule weakens the
    family's confidence instead of dragging its score toward the neutral label.
    """

    votes = [rule.vote for rule in rules if rule.vote is not None]
    score = sum(votes) / len(votes) if votes else 0.0
    positive, neutral, negative = labels
    if score >= _STRONG:
        label = positive
    elif score <= -_STRONG:
        label = negative
    else:
        label = neutral
    return {"label": label, "score": round(score, 4), "evaluated_rules": len(votes)}


def score_signals(indicators: IndicatorSet) -> dict[str, Any]:
    """Aggregate the rule votes into two scores — deliberately not one.

    The five rules split into two families that answer different questions: `macd` and
    `ma_stack` follow trend, while `rsi`, `bbands` and `stoch` look for exhaustion. On a
    clean trend they take opposite sides *by construction* — an overbought RSI inside a
    healthy uptrend is the normal case, not a contradiction.

    Averaging all five together therefore cancels out exactly when the reading is
    strongest: a sustained rise and a sustained collapse both come out at 0.0. Reporting
    the families separately keeps that information instead of destroying it, and leaves
    the trade-off to the caller, which has context this module does not. A single
    BUY/SELL label from unvalidated thresholds would be false precision.
    """

    trend = [rule(indicators) for rule in _TREND_RULES]
    mean_reversion = [rule(indicators) for rule in _MEAN_REVERSION_RULES]

    return {
        "trend": _family_score(trend, ("BULLISH", "FLAT", "BEARISH")),
        "mean_reversion": _family_score(mean_reversion, ("OVERSOLD", "NEUTRAL", "OVERBOUGHT")),
        "rules": [
            {"name": rule.name, "family": family, "vote": rule.vote, "reason": rule.reason}
            for family, rules in (("trend", trend), ("mean_reversion", mean_reversion))
            for rule in rules
        ],
    }


def analyze(series: CandleSeries) -> dict[str, Any]:
    """Run the whole layer and return the JSON-safe payload the command emits."""

    indicators = compute_indicators(series)
    return {
        "stock_code": series.stock_code,
        "source": series.source,
        "as_of": indicators.as_of,
        "candle_count": indicators.candle_count,
        "missing_candles": indicators.missing_count,
        "close": _clean(indicators.close, 2),
        "indicators": indicators.values,
        "signal": score_signals(indicators),
    }
