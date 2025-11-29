"""
Tests for volatility indicators (TRANGE, ATR, NATR).
"""

import numpy as np
import talib

from cluefin_ta import ATR, NATR, TRANGE


class TestTRANGE:
    """Tests for True Range."""

    def test_trange_matches_talib(self, sample_ohlcv):
        """Verify TRANGE matches ta-lib output."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]

        expected = talib.TRANGE(high, low, close)
        actual = TRANGE(high, low, close)

        # Compare non-NaN values
        mask = ~np.isnan(expected)
        np.testing.assert_allclose(actual[mask], expected[mask], rtol=1e-10)

    def test_trange_positive(self, sample_ohlcv):
        """Verify True Range is always positive."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]

        result = TRANGE(high, low, close)
        valid = result[~np.isnan(result)]

        assert np.all(valid >= 0)

    def test_trange_first_nan(self, sample_ohlcv):
        """Verify first value is NaN (no previous close)."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]

        result = TRANGE(high, low, close)
        assert np.isnan(result[0])


class TestATR:
    """Tests for Average True Range."""

    def test_atr_matches_talib(self, sample_ohlcv):
        """Verify ATR matches ta-lib output."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]

        expected = talib.ATR(high, low, close, timeperiod=14)
        actual = ATR(high, low, close, timeperiod=14)

        # Compare non-NaN values
        mask = ~np.isnan(expected)
        np.testing.assert_allclose(actual[mask], expected[mask], rtol=1e-10)

    def test_atr_positive(self, sample_ohlcv):
        """Verify ATR is always positive."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]

        result = ATR(high, low, close, timeperiod=14)
        valid = result[~np.isnan(result)]

        assert np.all(valid >= 0)

    def test_atr_nan_prefix(self, sample_ohlcv):
        """Verify ATR has correct NaN prefix."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]
        timeperiod = 14

        result = ATR(high, low, close, timeperiod=timeperiod)

        # First timeperiod values should be NaN
        assert np.all(np.isnan(result[:timeperiod]))
        # Value at timeperiod should not be NaN
        assert not np.isnan(result[timeperiod])


class TestNATR:
    """Tests for Normalized Average True Range."""

    def test_natr_matches_talib(self, sample_ohlcv):
        """Verify NATR matches ta-lib output."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]

        expected = talib.NATR(high, low, close, timeperiod=14)
        actual = NATR(high, low, close, timeperiod=14)

        # Compare non-NaN values
        mask = ~np.isnan(expected)
        np.testing.assert_allclose(actual[mask], expected[mask], rtol=1e-10)

    def test_natr_percentage(self, sample_ohlcv):
        """Verify NATR is expressed as percentage."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]

        atr = ATR(high, low, close, timeperiod=14)
        natr = NATR(high, low, close, timeperiod=14)

        # NATR = (ATR / Close) * 100
        mask = ~np.isnan(natr)
        expected_natr = (atr[mask] / close[mask]) * 100
        np.testing.assert_allclose(natr[mask], expected_natr, rtol=1e-10)
