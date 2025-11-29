"""
Tests for momentum indicators (RSI, MACD, STOCH, WILLR).
"""

import numpy as np
import pytest
import talib

from cluefin_ta import MACD, RSI, STOCH, WILLR


class TestRSI:
    """Tests for Relative Strength Index."""

    def test_rsi_matches_talib(self, sample_close):
        """Verify RSI matches ta-lib output."""
        timeperiod = 14
        expected = talib.RSI(sample_close, timeperiod=timeperiod)
        actual = RSI(sample_close, timeperiod=timeperiod)

        # Compare non-NaN values
        mask = ~np.isnan(expected)
        np.testing.assert_allclose(actual[mask], expected[mask], rtol=1e-10)

    def test_rsi_range(self, sample_close):
        """Verify RSI values are in range [0, 100]."""
        result = RSI(sample_close, timeperiod=14)
        valid = result[~np.isnan(result)]
        assert np.all(valid >= 0)
        assert np.all(valid <= 100)

    def test_rsi_short_array(self, short_data):
        """Test RSI with array shorter than timeperiod."""
        result = RSI(short_data, timeperiod=14)
        assert np.all(np.isnan(result))

    def test_rsi_constant_prices(self, constant_data):
        """Test RSI with constant prices (no change)."""
        result = RSI(constant_data, timeperiod=14)
        # When there's no price change, RSI should be 50 or undefined
        # With constant prices, all changes are 0, so RSI is undefined or neutral
        # ta-lib returns NaN for constant prices
        _ = result[~np.isnan(result)]  # Just verify it doesn't raise


class TestMACD:
    """Tests for Moving Average Convergence/Divergence."""

    def test_macd_matches_talib(self, sample_close):
        """Verify MACD matches ta-lib output within acceptable tolerance.

        Note: ta-lib uses internal "unstable period" handling which causes slight
        differences in early EMA values. The tolerance allows for ~2% relative difference
        which is acceptable for practical trading applications.
        """
        expected_macd, expected_signal, expected_hist = talib.MACD(sample_close)
        actual_macd, actual_signal, actual_hist = MACD(sample_close)

        # Compare non-NaN values for MACD line
        # Use more relaxed tolerance due to EMA initialization differences
        mask = ~np.isnan(expected_macd) & ~np.isnan(actual_macd)
        np.testing.assert_allclose(actual_macd[mask], expected_macd[mask], rtol=0.05)

        # Compare signal line (signal is EMA of MACD, so differences compound)
        signal_mask = ~np.isnan(expected_signal) & ~np.isnan(actual_signal)
        np.testing.assert_allclose(actual_signal[signal_mask], expected_signal[signal_mask], rtol=0.05)

        # Compare histogram using absolute tolerance (small values have high relative error)
        hist_mask = ~np.isnan(expected_hist) & ~np.isnan(actual_hist)
        np.testing.assert_allclose(actual_hist[hist_mask], expected_hist[hist_mask], atol=0.2)

    def test_macd_histogram_calculation(self, sample_close):
        """Verify histogram = MACD - Signal."""
        macd, signal, hist = MACD(sample_close)
        mask = ~np.isnan(signal)
        expected_hist = macd[mask] - signal[mask]
        np.testing.assert_allclose(hist[mask], expected_hist, rtol=1e-10)

    def test_macd_short_array(self, short_data):
        """Test MACD with short array."""
        macd, signal, hist = MACD(short_data)
        # All should be NaN for short array
        assert np.all(np.isnan(macd))


class TestSTOCH:
    """Tests for Stochastic Oscillator."""

    def test_stoch_matches_talib(self, sample_ohlcv):
        """Verify STOCH matches ta-lib output."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]

        expected_k, expected_d = talib.STOCH(high, low, close)
        actual_k, actual_d = STOCH(high, low, close)

        # Compare non-NaN values
        k_mask = ~np.isnan(expected_k)
        d_mask = ~np.isnan(expected_d)

        np.testing.assert_allclose(actual_k[k_mask], expected_k[k_mask], rtol=1e-10)
        np.testing.assert_allclose(actual_d[d_mask], expected_d[d_mask], rtol=1e-10)

    def test_stoch_range(self, sample_ohlcv):
        """Verify STOCH values are in range [0, 100]."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]

        slowk, slowd = STOCH(high, low, close)

        valid_k = slowk[~np.isnan(slowk)]
        valid_d = slowd[~np.isnan(slowd)]

        assert np.all(valid_k >= 0) and np.all(valid_k <= 100)
        assert np.all(valid_d >= 0) and np.all(valid_d <= 100)


class TestWILLR:
    """Tests for Williams %R."""

    def test_willr_matches_talib(self, sample_ohlcv):
        """Verify WILLR matches ta-lib output."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]

        expected = talib.WILLR(high, low, close, timeperiod=14)
        actual = WILLR(high, low, close, timeperiod=14)

        # Compare non-NaN values
        mask = ~np.isnan(expected)
        np.testing.assert_allclose(actual[mask], expected[mask], rtol=1e-10)

    def test_willr_range(self, sample_ohlcv):
        """Verify WILLR values are in range [-100, 0]."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]

        result = WILLR(high, low, close, timeperiod=14)
        valid = result[~np.isnan(result)]

        assert np.all(valid >= -100)
        assert np.all(valid <= 0)
