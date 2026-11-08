"""Tests for TechnicalAnalyzer (apps/cluefin-desk/src/cluefin_desk/ml/indicators.py).

`TechnicalAnalyzer.calculate_all` previously had no test at all (see desk AGENTS.md,
"지표 -> ML 피처 경로"). Its output feeds `StockMLPredictor.prepare_data`/`predict` as the
`indicators` dict, and only 8 of its columns survive `create_talib_features` overwriting:
sma_50, sma_120, sma_240, rsi, macd_histogram, adx, resistance, support. This file:

1. Exercises `calculate_all` end to end (smoke test), including the resistance/support
   20-row threshold behavior called out in AGENTS.md.
2. Pins the pre-refactor reference values for every column with a frozen synthetic OHLCV
   fixture, so swapping in `cluefin_ta` functions can't silently change column names,
   column order, row counts, or the survivor feature values beyond a small tolerance.
"""

import numpy as np
import pandas as pd
import pytest

from cluefin_desk.ml.indicators import TechnicalAnalyzer

SURVIVOR_COLUMNS = [
    "sma_50",
    "sma_120",
    "sma_240",
    "rsi",
    "macd_histogram",
    "adx",
    "resistance",
    "support",
]


def _reference_calculate_all(data: pd.DataFrame) -> pd.DataFrame:
    """Pre-refactor implementation of TechnicalAnalyzer.calculate_all, frozen here as the
    baseline that the cluefin_ta-backed implementation must stay close to."""
    if data.empty:
        return pd.DataFrame()

    result = data.copy()

    def _sma(series: pd.Series, period: int) -> pd.Series:
        return series.rolling(window=period).mean()

    def _ema(series: pd.Series, period: int) -> pd.Series:
        return series.ewm(span=period).mean()

    def _rsi(series: pd.Series, period: int = 14) -> pd.Series:
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def _stochastic(high: pd.Series, low: pd.Series, close: pd.Series, k_period: int = 14, d_period: int = 3):
        lowest_low = low.rolling(window=k_period).min()
        highest_high = high.rolling(window=k_period).max()
        k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d_percent = k_percent.rolling(window=d_period).mean()
        return k_percent, d_percent

    result["sma_5"] = _sma(data["close"], 5)
    result["sma_20"] = _sma(data["close"], 20)
    result["sma_50"] = _sma(data["close"], 50)
    result["sma_120"] = _sma(data["close"], 120)
    result["sma_240"] = _sma(data["close"], 240)
    result["ema_12"] = _ema(data["close"], 12)
    result["ema_26"] = _ema(data["close"], 26)

    result["rsi"] = _rsi(data["close"], 14)

    macd_line = result["ema_12"] - result["ema_26"]
    macd_signal = _ema(macd_line, 9)
    result["macd"] = macd_line
    result["macd_signal"] = macd_signal
    result["macd_histogram"] = macd_line - macd_signal

    bb_middle = result["sma_20"]
    bb_std = data["close"].rolling(window=20).std()
    result["bb_middle"] = bb_middle
    result["bb_upper"] = bb_middle + (bb_std * 2)
    result["bb_lower"] = bb_middle - (bb_std * 2)

    stoch_k, stoch_d = _stochastic(data["high"], data["low"], data["close"])
    result["stoch_k"] = stoch_k
    result["stoch_d"] = stoch_d

    result["volume_sma"] = _sma(data["volume"], 20)
    import cluefin_ta as talib

    result["obv"] = talib.OBV(data["close"].values, data["volume"].values)
    result["adx"] = talib.ADX(data["high"].values, data["low"].values, data["close"].values, timeperiod=14)
    result["atr"] = talib.ATR(data["high"].values, data["low"].values, data["close"].values, timeperiod=14)

    if len(result) >= 20:
        high_rolling = result["high"].rolling(window=10).max()
        low_rolling = result["low"].rolling(window=10).min()
        result["resistance"] = high_rolling
        result["support"] = low_rolling

    return result


def _synthetic_ohlcv(n: int = 300, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    close = 100 + np.cumsum(rng.normal(0, 1, n))
    high = close + rng.uniform(0, 2, n)
    low = close - rng.uniform(0, 2, n)
    open_ = close + rng.uniform(-1, 1, n)
    volume = rng.uniform(1_000_000, 5_000_000, n)
    dates = pd.date_range("2024-01-01", periods=n, freq="D")
    return pd.DataFrame({"date": dates, "open": open_, "high": high, "low": low, "close": close, "volume": volume})


class TestCalculateAllSmoke:
    """calculate_all had no test before this file (desk AGENTS.md)."""

    def test_empty_input_returns_empty(self):
        result = TechnicalAnalyzer().calculate_all(pd.DataFrame())
        assert result.empty

    def test_calculate_all_runs_and_has_expected_columns(self):
        data = _synthetic_ohlcv(n=300)
        result = TechnicalAnalyzer().calculate_all(data)

        assert len(result) == len(data)
        for col in [
            "sma_5",
            "sma_20",
            "sma_50",
            "sma_120",
            "sma_240",
            "ema_12",
            "ema_26",
            "rsi",
            "macd",
            "macd_signal",
            "macd_histogram",
            "bb_middle",
            "bb_upper",
            "bb_lower",
            "stoch_k",
            "stoch_d",
            "volume_sma",
            "obv",
            "adx",
            "atr",
            "resistance",
            "support",
        ]:
            assert col in result.columns, f"missing column {col}"

        # sma_240 needs 240 valid closes; by the end of a 300-row series it must be populated.
        assert pd.notna(result["sma_240"].iloc[-1])

    def test_resistance_support_do_not_look_ahead(self):
        """A spike at bar 40 must not show up in resistance/support before bar 40."""
        data = _synthetic_ohlcv(n=60)
        spiked = data.copy()
        spiked.loc[40, "high"] = 10_000.0
        spiked.loc[40, "low"] = -10_000.0
        base = TechnicalAnalyzer().calculate_all(data)
        after = TechnicalAnalyzer().calculate_all(spiked)
        for column in ("resistance", "support"):
            np.testing.assert_array_equal(after[column].iloc[:40], base[column].iloc[:40])
        assert after["resistance"].iloc[40] == 10_000.0
        assert after["support"].iloc[40] == -10_000.0

    def test_resistance_support_need_20_rows(self):
        """AGENTS.md: resistance/support only appear once there are >= 20 rows."""
        short_data = _synthetic_ohlcv(n=19)
        short_result = TechnicalAnalyzer().calculate_all(short_data)
        assert "resistance" not in short_result.columns
        assert "support" not in short_result.columns

        long_data = _synthetic_ohlcv(n=20)
        long_result = TechnicalAnalyzer().calculate_all(long_data)
        assert "resistance" in long_result.columns
        assert "support" in long_result.columns


class TestCalculateAllMatchesReference:
    """Pins before/after equivalence for a cluefin_ta-backed TechnicalAnalyzer.

    Column names/order and row counts must match exactly. Survivor feature columns
    (the 8 that reach the ML model unchanged) must match within tolerance. Non-survivor
    columns that keep their original (non cluefin_ta) formula also match exactly; any
    column intentionally swapped to a cluefin_ta function with a different internal
    warm-up/definition is exempted here and called out in the implementation.
    """

    @staticmethod
    @pytest.fixture(scope="class")
    def data():
        return _synthetic_ohlcv(n=300)

    @staticmethod
    @pytest.fixture(scope="class")
    def reference(data):
        return _reference_calculate_all(data)

    @staticmethod
    @pytest.fixture(scope="class")
    def actual(data):
        return TechnicalAnalyzer().calculate_all(data)

    def test_same_columns_and_order(self, reference, actual):
        assert list(actual.columns) == list(reference.columns)

    def test_same_row_count(self, reference, actual):
        assert len(actual) == len(reference)

    @pytest.mark.parametrize("column", SURVIVOR_COLUMNS)
    def test_survivor_columns_match_within_tolerance(self, reference, actual, column):
        np.testing.assert_allclose(
            actual[column].to_numpy(dtype=float),
            reference[column].to_numpy(dtype=float),
            rtol=1e-3,
            atol=1e-3,
            equal_nan=True,
        )

    @pytest.mark.parametrize(
        "column",
        [
            "sma_5",
            "sma_20",
            "volume_sma",
            "obv",
            "atr",
            "ema_12",
            "ema_26",
            "macd",
            "macd_signal",
            "bb_middle",
            "bb_upper",
            "bb_lower",
            "stoch_k",
            "stoch_d",
        ],
    )
    def test_unchanged_columns_match_closely(self, reference, actual, column):
        np.testing.assert_allclose(
            actual[column].to_numpy(dtype=float),
            reference[column].to_numpy(dtype=float),
            rtol=1e-6,
            atol=1e-6,
            equal_nan=True,
        )
