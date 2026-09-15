from __future__ import annotations

import math

import pytest

from cluefin_openapi_cli.indicators import (
    MIN_CANDLES,
    IndicatorSet,
    analyze,
    compute_indicators,
    score_signals,
)
from cluefin_openapi_cli.ohlcv import Candle, CandleSeries


def _series(closes: list[float], *, volume: float = 1000.0) -> CandleSeries:
    """Build a series from a close path, with a plausible bar drawn around each close."""

    candles = tuple(
        Candle(
            timestamp=f"2026{(index // 28) + 1:02d}{(index % 28) + 1:02d}",
            open=close,
            high=close * 1.01,
            low=close * 0.99,
            close=close,
            volume=volume,
        )
        for index, close in enumerate(closes)
    )
    return CandleSeries(stock_code="005930", source="test", candles=candles)


def _flat(count: int = 120, price: float = 1000.0) -> list[float]:
    return [price] * count


def _uptrend(count: int = 120, start: float = 1000.0, rate: float = 0.01) -> list[float]:
    """A compounding rise.

    Deliberately not a straight line: on a perfectly linear path the MACD line is
    constant, its signal EMA converges onto it, and the histogram sits at exactly 0 —
    so a linear fixture would test the MACD rule against a degenerate case it never
    meets on real prices.
    """

    return [start * (1.0 + rate) ** index for index in range(count)]


def _downtrend(count: int = 120, start: float = 2200.0, step: float = 10.0) -> list[float]:
    return [start - step * index for index in range(count)]


def _reversal(count: int = 120, start: float = 1000.0, step: float = 10.0) -> list[float]:
    """A rise that rolls over halfway — what a SELL reading actually looks like."""

    half = count // 2
    peak = start + step * half
    return [start + step * index for index in range(half)] + [
        peak - step * index for index in range(1, count - half + 1)
    ]


# ---------------------------------------------------------------------------
# Warm-up guard
# ---------------------------------------------------------------------------


def test_short_series_is_refused_rather_than_answered_half_blind() -> None:
    """Below SMA(60)'s warm-up the trend rules would silently stop voting."""

    with pytest.raises(ValueError, match="at least 60 candles"):
        compute_indicators(_series(_flat(MIN_CANDLES - 1)))


def test_exactly_the_minimum_is_accepted() -> None:
    indicators = compute_indicators(_series(_uptrend(MIN_CANDLES)))

    assert indicators.candle_count == MIN_CANDLES


# ---------------------------------------------------------------------------
# compute_indicators
# ---------------------------------------------------------------------------


def test_only_the_final_reading_of_each_indicator_is_kept() -> None:
    """The whole point of the layer is that the curve does not travel back to the agent."""

    indicators = compute_indicators(_series(_uptrend()))

    assert isinstance(indicators.values["rsi_14"], float)
    assert set(indicators.values["macd"]) == {"macd", "signal", "histogram"}
    assert set(indicators.values["bbands_20"]) == {"upper", "middle", "lower", "percent_b"}


def test_series_context_is_reported() -> None:
    series = _series(_uptrend(80))
    indicators = compute_indicators(series)

    assert indicators.as_of == series.candles[-1].timestamp
    assert indicators.candle_count == 80
    assert indicators.missing_count == 0
    assert indicators.close == series.candles[-1].close


def test_moving_averages_lag_a_rising_close() -> None:
    indicators = compute_indicators(_series(_uptrend()))
    values = indicators.values

    assert indicators.close > values["sma_5"] > values["sma_20"] > values["sma_60"]


def test_nan_indicator_values_serialize_as_none_not_nan() -> None:
    """`float('nan')` is not valid JSON; an agent would get a parse error."""

    # A flat price path gives Bollinger bands zero width, so percent_b is undefined.
    indicators = compute_indicators(_series(_flat()))

    assert indicators.values["bbands_20"]["percent_b"] is None


def test_missing_candles_are_counted_and_surfaced() -> None:
    closes = _uptrend()
    series = _series(closes)
    broken = CandleSeries(
        stock_code=series.stock_code,
        source=series.source,
        candles=series.candles[:-1]
        + (Candle(series.candles[-1].timestamp, math.nan, math.nan, math.nan, math.nan, math.nan),),
    )

    payload = analyze(broken)

    assert payload["missing_candles"] == 1


def test_flat_series_has_no_drawdown() -> None:
    indicators = compute_indicators(_series(_flat()))

    assert indicators.values["mdd"] == 0.0


def test_downtrend_produces_a_drawdown() -> None:
    indicators = compute_indicators(_series(_downtrend()))

    assert indicators.values["mdd"] > 0


# ---------------------------------------------------------------------------
# Signal aggregation
# ---------------------------------------------------------------------------


def _votes(payload: dict) -> dict[str, int | None]:
    return {rule["name"]: rule["vote"] for rule in payload["signal"]["rules"]}


def test_every_rule_reports_its_family_vote_and_reason() -> None:
    signal = score_signals(compute_indicators(_series(_uptrend())))

    assert [rule["name"] for rule in signal["rules"]] == ["macd", "ma_stack", "rsi", "bbands", "stoch"]
    assert [rule["family"] for rule in signal["rules"]] == ["trend"] * 2 + ["mean_reversion"] * 3
    assert all(rule["reason"] for rule in signal["rules"])


def test_sustained_uptrend_reads_bullish_on_trend_and_overbought_on_exhaustion() -> None:
    payload = analyze(_series(_uptrend()))

    assert payload["signal"]["trend"]["label"] == "BULLISH"
    assert payload["signal"]["mean_reversion"]["label"] == "OVERBOUGHT"


def test_rolled_over_trend_reads_bearish_on_trend_and_oversold_on_exhaustion() -> None:
    payload = analyze(_series(_reversal()))

    assert payload["signal"]["trend"]["label"] == "BEARISH"
    assert payload["signal"]["mean_reversion"]["label"] == "OVERSOLD"


def test_the_two_families_are_not_averaged_together() -> None:
    """Averaging all five cancels exactly when the reading is strongest.

    A sustained rise and a sustained collapse would both come out at 0.0 — the families
    are reported separately so that information survives.
    """

    rising = analyze(_series(_uptrend()))["signal"]
    falling = analyze(_series(_reversal()))["signal"]

    assert rising["trend"]["score"] > 0 > rising["mean_reversion"]["score"]
    assert falling["trend"]["score"] < 0 < falling["mean_reversion"]["score"]
    assert rising["trend"]["score"] != falling["trend"]["score"]


def test_score_is_the_mean_of_evaluated_rules_not_their_sum() -> None:
    indicators = IndicatorSet(
        as_of="20260101",
        candle_count=120,
        missing_count=0,
        close=1000.0,
        values={
            "sma_5": 900.0,
            "sma_20": 800.0,
            "sma_60": 700.0,
            "rsi_14": 20.0,
            "macd": {"macd": 1.0, "signal": 0.5, "histogram": 0.5},
            "bbands_20": {"upper": 1100.0, "middle": 1000.0, "lower": 900.0, "percent_b": 0.5},
            "stoch": {"slow_k": 50.0, "slow_d": 50.0},
        },
    )

    signal = score_signals(indicators)

    # trend: macd +1, ma_stack +1 -> 1.0; mean_reversion: rsi +1, bbands 0, stoch 0 -> 1/3
    assert signal["trend"] == {"label": "BULLISH", "score": 1.0, "evaluated_rules": 2}
    assert signal["mean_reversion"]["score"] == pytest.approx(0.3333, abs=1e-4)
    assert signal["mean_reversion"]["label"] == "NEUTRAL"


def test_unavailable_rules_are_excluded_rather_than_counted_as_neutral() -> None:
    """Counting a warm-up NaN as a 0 vote would bias a short series toward NEUTRAL."""

    indicators = IndicatorSet(
        as_of="20260101",
        candle_count=120,
        missing_count=0,
        close=1000.0,
        values={
            "sma_5": None,
            "sma_20": None,
            "sma_60": None,
            "rsi_14": 20.0,
            "macd": {"macd": None, "signal": None, "histogram": None},
            "bbands_20": {"upper": None, "middle": None, "lower": None, "percent_b": None},
            "stoch": {"slow_k": None, "slow_d": None},
        },
    )

    signal = score_signals(indicators)

    assert signal["mean_reversion"] == {"label": "OVERSOLD", "score": 1.0, "evaluated_rules": 1}
    assert signal["trend"] == {"label": "FLAT", "score": 0.0, "evaluated_rules": 0}
    assert _votes({"signal": signal})["ma_stack"] is None


def test_no_evaluable_rule_scores_zero_instead_of_dividing_by_zero() -> None:
    indicators = IndicatorSet(
        as_of="20260101",
        candle_count=120,
        missing_count=0,
        close=1000.0,
        values={
            "sma_5": None,
            "sma_20": None,
            "sma_60": None,
            "rsi_14": None,
            "macd": {"macd": None, "signal": None, "histogram": None},
            "bbands_20": {"upper": None, "middle": None, "lower": None, "percent_b": None},
            "stoch": {"slow_k": None, "slow_d": None},
        },
    )

    signal = score_signals(indicators)

    assert signal["trend"] == {"label": "FLAT", "score": 0.0, "evaluated_rules": 0}
    assert signal["mean_reversion"] == {"label": "NEUTRAL", "score": 0.0, "evaluated_rules": 0}


@pytest.mark.parametrize(
    ("rsi", "expected"),
    [(10.0, 1), (29.9, 1), (30.0, 0), (50.0, 0), (70.0, 0), (70.1, -1), (95.0, -1)],
)
def test_rsi_rule_boundaries(rsi: float, expected: int) -> None:
    indicators = IndicatorSet(
        as_of="20260101",
        candle_count=120,
        missing_count=0,
        close=1000.0,
        values={
            "sma_5": None,
            "sma_20": None,
            "sma_60": None,
            "rsi_14": rsi,
            "macd": {"macd": None, "signal": None, "histogram": None},
            "bbands_20": {"upper": None, "middle": None, "lower": None, "percent_b": None},
            "stoch": {"slow_k": None, "slow_d": None},
        },
    )

    assert _votes({"signal": score_signals(indicators)})["rsi"] == expected


def test_close_at_the_band_edge_counts_as_a_touch() -> None:
    indicators = IndicatorSet(
        as_of="20260101",
        candle_count=120,
        missing_count=0,
        close=900.0,
        values={
            "sma_5": None,
            "sma_20": None,
            "sma_60": None,
            "rsi_14": None,
            "macd": {"macd": None, "signal": None, "histogram": None},
            "bbands_20": {"upper": 1100.0, "middle": 1000.0, "lower": 900.0, "percent_b": 0.0},
            "stoch": {"slow_k": None, "slow_d": None},
        },
    )

    assert _votes({"signal": score_signals(indicators)})["bbands"] == 1


# ---------------------------------------------------------------------------
# analyze payload
# ---------------------------------------------------------------------------


def test_analyze_payload_is_json_safe_and_small() -> None:
    import json

    payload = analyze(_series(_uptrend()))

    text = json.dumps(payload, allow_nan=False)
    assert len(text) < 2000
    assert set(payload) == {
        "stock_code",
        "source",
        "as_of",
        "candle_count",
        "missing_candles",
        "close",
        "indicators",
        "signal",
    }


def test_analyze_carries_the_series_provenance() -> None:
    payload = analyze(_series(_uptrend()))

    assert payload["stock_code"] == "005930"
    assert payload["source"] == "test"
