"""Tests for TechnicalAnalyzer indicator calculations."""

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


def _make_ohlcv(n: int = 60) -> pd.DataFrame:
    """Build a deterministic OHLCV fixture with an upward-trending close."""
    rng = np.random.default_rng(42)
    close = 100 + np.cumsum(rng.normal(loc=0.3, scale=1.0, size=n))
    high = close + rng.uniform(0.5, 1.5, size=n)
    low = close - rng.uniform(0.5, 1.5, size=n)
    volume = rng.integers(1_000, 10_000, size=n).astype(float)
    return pd.DataFrame({"open": close, "high": high, "low": low, "close": close, "volume": volume})


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


class TestCalculateAll:
    def test_adx_column_present_and_bounded(self):
        result = TechnicalAnalyzer().calculate_all(_make_ohlcv())
        assert "adx" in result
        valid = result["adx"].dropna()
        assert not valid.empty
        assert valid.between(0, 100).all()

    def test_atr_column_present_and_non_negative(self):
        result = TechnicalAnalyzer().calculate_all(_make_ohlcv())
        assert "atr" in result
        valid = result["atr"].dropna()
        assert not valid.empty
        assert (valid >= 0).all()

    def test_obv_column_present_same_length_as_input(self):
        data = _make_ohlcv()
        result = TechnicalAnalyzer().calculate_all(data)
        assert "obv" in result
        assert len(result["obv"]) == len(data)
        assert result["obv"].notna().all()

    def test_empty_input_returns_empty_dataframe(self):
        result = TechnicalAnalyzer().calculate_all(pd.DataFrame())
        assert result.empty


class TestCalculateRiskMetrics:
    def test_returns_mdd_and_sharpe_for_sufficient_data(self):
        metrics = TechnicalAnalyzer().calculate_risk_metrics(_make_ohlcv())
        assert set(metrics) == {"mdd", "sharpe"}
        assert 0 <= metrics["mdd"] <= 1
        assert isinstance(metrics["sharpe"], float)

    def test_empty_dict_when_fewer_than_two_returns(self):
        data = _make_ohlcv(n=1)
        metrics = TechnicalAnalyzer().calculate_risk_metrics(data)
        assert metrics == {}

    def test_drops_leading_nan_from_pct_change(self):
        # 3 rows -> 2 non-null returns after dropna(), which is the minimum
        # for calculate_risk_metrics to compute. Proves the leading NaN from
        # pct_change() doesn't poison the result via an uncounted extra row.
        data = _make_ohlcv(n=3)
        metrics = TechnicalAnalyzer().calculate_risk_metrics(data)
        assert metrics != {}
        assert np.isfinite(metrics["mdd"])
        assert np.isfinite(metrics["sharpe"])
