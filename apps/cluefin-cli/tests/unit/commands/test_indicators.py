from __future__ import annotations

import numpy as np
import pandas as pd

from cluefin_cli.commands.analysis.indicators import TechnicalAnalyzer


def _ohlcv(n: int) -> pd.DataFrame:
    rng = np.linspace(100, 200, n)
    return pd.DataFrame(
        {
            "open": rng,
            "high": rng + 3,
            "low": rng - 3,
            "close": rng + 1,
            "volume": np.arange(n) * 100 + 1000,
        }
    )


def _two_rows(previous: dict, latest: dict) -> pd.DataFrame:
    return pd.DataFrame([previous, latest])


def test_calculate_all_empty_returns_empty() -> None:
    assert TechnicalAnalyzer().calculate_all(pd.DataFrame()).empty


def test_calculate_all_produces_indicator_columns() -> None:
    result = TechnicalAnalyzer().calculate_all(_ohlcv(260))
    for column in ["sma_5", "sma_240", "rsi", "macd", "macd_signal", "bb_upper", "stoch_k", "resistance"]:
        assert column in result.columns
    assert len(result) == 260


def test_calculate_all_short_series_skips_support_resistance() -> None:
    result = TechnicalAnalyzer().calculate_all(_ohlcv(10))
    assert "resistance" not in result.columns  # _calculate_support_resistance early-returns


def test_get_signals_empty_or_too_short_returns_empty() -> None:
    assert TechnicalAnalyzer().get_signals(pd.DataFrame()) == {}
    assert TechnicalAnalyzer().get_signals(_ohlcv(1)) == {}


def test_get_signals_buy_scenario() -> None:
    previous = {
        "rsi": 28,
        "macd": 0.2,
        "macd_signal": 0.5,
        "close": 110,
        "sma_20": 100,
        "sma_50": 90,
        "bb_lower": 120,
        "bb_upper": 200,
    }
    latest = {
        "rsi": 25,
        "macd": 1.0,
        "macd_signal": 0.5,
        "close": 110,
        "sma_20": 100,
        "sma_50": 90,
        "bb_lower": 120,
        "bb_upper": 200,
    }
    signals = TechnicalAnalyzer().get_signals(_two_rows(previous, latest))
    assert signals["overall_signal"] == "BUY"
    assert any("RSI oversold" in s for s in signals["signals"])
    assert any("bullish crossover" in s for s in signals["signals"])


def test_get_signals_sell_scenario() -> None:
    previous = {
        "rsi": 75,
        "macd": 2.0,
        "macd_signal": 1.0,
        "close": 80,
        "sma_20": 100,
        "sma_50": 110,
        "bb_lower": 10,
        "bb_upper": 70,
    }
    latest = {
        "rsi": 75,
        "macd": 0.0,
        "macd_signal": 1.0,
        "close": 80,
        "sma_20": 100,
        "sma_50": 110,
        "bb_lower": 10,
        "bb_upper": 70,
    }
    signals = TechnicalAnalyzer().get_signals(_two_rows(previous, latest))
    assert signals["overall_signal"] == "SELL"
    assert any("overbought" in s for s in signals["signals"])
    assert any("bearish crossover" in s for s in signals["signals"])


def test_get_signals_neutral_scenario() -> None:
    # RSI mid-band, MACD above signal without a crossover, price between MAs and bands.
    row = {
        "rsi": 50,
        "macd": 1.0,
        "macd_signal": 0.5,
        "close": 105,
        "sma_20": 100,
        "sma_50": 110,
        "bb_lower": 50,
        "bb_upper": 200,
    }
    signals = TechnicalAnalyzer().get_signals(_two_rows(row, row))
    assert signals["overall_signal"] == "NEUTRAL"
    assert -0.6 <= signals["strength"] <= 0.6
