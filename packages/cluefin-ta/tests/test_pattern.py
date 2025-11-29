"""
Tests for candlestick pattern recognition (CDLDOJI, CDLHAMMER, CDLENGULFING).
"""

import numpy as np
import pytest
import talib

from cluefin_ta import CDLDOJI, CDLENGULFING, CDLHAMMER


class TestCDLDOJI:
    """Tests for Doji pattern."""

    def test_cdldoji_output_values(self, sample_ohlcv):
        """Verify CDLDOJI returns valid values (-100, 0, or 100)."""
        result = CDLDOJI(
            sample_ohlcv["open"],
            sample_ohlcv["high"],
            sample_ohlcv["low"],
            sample_ohlcv["close"],
        )

        unique_values = np.unique(result)
        valid_values = {-100, 0, 100}
        assert set(unique_values).issubset(valid_values)

    def test_cdldoji_perfect_doji(self):
        """Test detection of perfect doji (open == close)."""
        # Create a perfect doji: open equals close
        open_arr = np.array([100.0])
        high = np.array([105.0])
        low = np.array([95.0])
        close = np.array([100.0])  # Same as open

        result = CDLDOJI(open_arr, high, low, close)

        # Should detect doji
        assert result[0] == 100

    def test_cdldoji_no_doji(self):
        """Test non-doji candle."""
        # Create a candle with significant body
        open_arr = np.array([100.0])
        high = np.array([105.0])
        low = np.array([95.0])
        close = np.array([104.0])  # Big body

        result = CDLDOJI(open_arr, high, low, close)

        # Should not detect doji
        assert result[0] == 0


class TestCDLHAMMER:
    """Tests for Hammer pattern."""

    def test_cdlhammer_output_values(self, sample_ohlcv):
        """Verify CDLHAMMER returns valid values (0 or 100)."""
        result = CDLHAMMER(
            sample_ohlcv["open"],
            sample_ohlcv["high"],
            sample_ohlcv["low"],
            sample_ohlcv["close"],
        )

        unique_values = np.unique(result)
        # Hammer is bullish pattern, should return 0 or 100
        valid_values = {0, 100}
        assert set(unique_values).issubset(valid_values)

    def test_cdlhammer_perfect_hammer(self):
        """Test detection of perfect hammer pattern."""
        # Hammer: small body at top, long lower shadow, no upper shadow
        open_arr = np.array([100.0])
        high = np.array([101.0])  # Small upper shadow
        low = np.array([90.0])  # Long lower shadow
        close = np.array([100.5])  # Small body

        result = CDLHAMMER(open_arr, high, low, close)

        # Should detect hammer
        assert result[0] == 100

    def test_cdlhammer_no_hammer(self):
        """Test non-hammer candle."""
        # Regular candle with balanced shadows
        open_arr = np.array([100.0])
        high = np.array([105.0])
        low = np.array([95.0])
        close = np.array([103.0])

        result = CDLHAMMER(open_arr, high, low, close)

        # Should not detect hammer
        assert result[0] == 0


class TestCDLENGULFING:
    """Tests for Engulfing pattern."""

    def test_cdlengulfing_output_values(self, sample_ohlcv):
        """Verify CDLENGULFING returns valid values (-100, 0, or 100)."""
        result = CDLENGULFING(
            sample_ohlcv["open"],
            sample_ohlcv["high"],
            sample_ohlcv["low"],
            sample_ohlcv["close"],
        )

        unique_values = np.unique(result)
        valid_values = {-100, 0, 100}
        assert set(unique_values).issubset(valid_values)

    def test_cdlengulfing_bullish(self):
        """Test detection of bullish engulfing pattern."""
        # Day 1: Bearish candle, Day 2: Bullish candle that engulfs
        open_arr = np.array([102.0, 98.0])
        high = np.array([103.0, 104.0])
        low = np.array([99.0, 97.0])
        close = np.array([100.0, 103.0])  # Day 1: bearish, Day 2: bullish engulfing

        result = CDLENGULFING(open_arr, high, low, close)

        # Should detect bullish engulfing on day 2
        assert result[0] == 0  # No pattern on first day
        assert result[1] == 100  # Bullish engulfing

    def test_cdlengulfing_bearish(self):
        """Test detection of bearish engulfing pattern."""
        # Day 1: Bullish candle, Day 2: Bearish candle that engulfs
        open_arr = np.array([98.0, 104.0])
        high = np.array([103.0, 105.0])
        low = np.array([97.0, 96.0])
        close = np.array([102.0, 97.0])  # Day 1: bullish, Day 2: bearish engulfing

        result = CDLENGULFING(open_arr, high, low, close)

        # Should detect bearish engulfing on day 2
        assert result[0] == 0  # No pattern on first day
        assert result[1] == -100  # Bearish engulfing

    def test_cdlengulfing_no_engulf(self):
        """Test non-engulfing pattern."""
        # Two bullish candles, second doesn't engulf
        open_arr = np.array([100.0, 102.0])
        high = np.array([103.0, 104.0])
        low = np.array([99.0, 101.0])
        close = np.array([102.0, 103.0])

        result = CDLENGULFING(open_arr, high, low, close)

        # No engulfing pattern
        assert result[0] == 0
        assert result[1] == 0

    def test_cdlengulfing_first_value(self, sample_ohlcv):
        """Verify first value is always 0 (needs previous candle)."""
        result = CDLENGULFING(
            sample_ohlcv["open"],
            sample_ohlcv["high"],
            sample_ohlcv["low"],
            sample_ohlcv["close"],
        )

        assert result[0] == 0
