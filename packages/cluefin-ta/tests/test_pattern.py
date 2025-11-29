"""
Tests for candlestick pattern recognition.
"""

import numpy as np
import pytest
import talib

from cluefin_ta import (
    CDLDOJI,
    CDLENGULFING,
    CDLHAMMER,
    CDLHANGINGMAN,
    CDLHARAMI,
    CDLPIERCING,
    CDLSHOOTINGSTAR,
)


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


class TestCDLSHOOTINGSTAR:
    """Tests for Shooting Star pattern."""

    def test_cdlshootingstar_output_values(self, sample_ohlcv):
        """Verify CDLSHOOTINGSTAR returns valid values."""
        result = CDLSHOOTINGSTAR(
            sample_ohlcv["open"],
            sample_ohlcv["high"],
            sample_ohlcv["low"],
            sample_ohlcv["close"],
        )

        unique_values = np.unique(result)
        valid_values = {-100, 0}
        assert set(unique_values).issubset(valid_values)

    def test_cdlshootingstar_perfect(self):
        """Test detection of perfect shooting star pattern."""
        # Shooting star: small body at bottom, long upper shadow, no lower shadow
        open_arr = np.array([100.0])
        high = np.array([110.0])  # Long upper shadow
        low = np.array([99.5])  # Small lower shadow
        close = np.array([100.5])  # Small body

        result = CDLSHOOTINGSTAR(open_arr, high, low, close)

        # Should detect shooting star
        assert result[0] == -100

    def test_cdlshootingstar_no_pattern(self):
        """Test non-shooting-star candle."""
        # Regular bullish candle
        open_arr = np.array([100.0])
        high = np.array([105.0])
        low = np.array([95.0])
        close = np.array([104.0])

        result = CDLSHOOTINGSTAR(open_arr, high, low, close)

        assert result[0] == 0


class TestCDLHANGINGMAN:
    """Tests for Hanging Man pattern."""

    def test_cdlhangingman_output_values(self, sample_ohlcv):
        """Verify CDLHANGINGMAN returns valid values."""
        result = CDLHANGINGMAN(
            sample_ohlcv["open"],
            sample_ohlcv["high"],
            sample_ohlcv["low"],
            sample_ohlcv["close"],
        )

        unique_values = np.unique(result)
        valid_values = {-100, 0}
        assert set(unique_values).issubset(valid_values)

    def test_cdlhangingman_perfect(self):
        """Test detection of hanging man pattern (same shape as hammer)."""
        # Hanging man: small body at top, long lower shadow, no upper shadow
        open_arr = np.array([100.0])
        high = np.array([101.0])  # Small upper shadow
        low = np.array([90.0])  # Long lower shadow
        close = np.array([100.5])  # Small body

        result = CDLHANGINGMAN(open_arr, high, low, close)

        # Should detect hanging man (bearish signal)
        assert result[0] == -100


class TestCDLHARAMI:
    """Tests for Harami pattern."""

    def test_cdlharami_output_values(self, sample_ohlcv):
        """Verify CDLHARAMI returns valid values."""
        result = CDLHARAMI(
            sample_ohlcv["open"],
            sample_ohlcv["high"],
            sample_ohlcv["low"],
            sample_ohlcv["close"],
        )

        unique_values = np.unique(result)
        valid_values = {-100, 0, 100}
        assert set(unique_values).issubset(valid_values)

    def test_cdlharami_bullish(self):
        """Test detection of bullish harami pattern."""
        # Day 1: Large bearish candle, Day 2: Small bullish candle inside
        open_arr = np.array([105.0, 101.0])
        high = np.array([106.0, 102.0])
        low = np.array([99.0, 100.0])
        close = np.array([100.0, 101.5])  # Day 1: bearish, Day 2: bullish inside

        result = CDLHARAMI(open_arr, high, low, close)

        assert result[0] == 0  # No pattern on first day
        assert result[1] == 100  # Bullish harami

    def test_cdlharami_bearish(self):
        """Test detection of bearish harami pattern."""
        # Day 1: Large bullish candle, Day 2: Small bearish candle inside
        open_arr = np.array([100.0, 104.0])
        high = np.array([106.0, 104.5])
        low = np.array([99.0, 101.0])
        close = np.array([105.0, 101.5])  # Day 1: bullish, Day 2: bearish inside

        result = CDLHARAMI(open_arr, high, low, close)

        assert result[0] == 0
        assert result[1] == -100  # Bearish harami

    def test_cdlharami_first_value(self):
        """Verify first value is always 0."""
        open_arr = np.array([100.0, 101.0])
        high = np.array([102.0, 103.0])
        low = np.array([99.0, 100.0])
        close = np.array([101.0, 100.5])

        result = CDLHARAMI(open_arr, high, low, close)
        assert result[0] == 0


class TestCDLPIERCING:
    """Tests for Piercing Line pattern."""

    def test_cdlpiercing_output_values(self, sample_ohlcv):
        """Verify CDLPIERCING returns valid values."""
        result = CDLPIERCING(
            sample_ohlcv["open"],
            sample_ohlcv["high"],
            sample_ohlcv["low"],
            sample_ohlcv["close"],
        )

        unique_values = np.unique(result)
        valid_values = {0, 100}
        assert set(unique_values).issubset(valid_values)

    def test_cdlpiercing_perfect(self):
        """Test detection of piercing line pattern."""
        # Day 1: Bearish candle, Day 2: Opens below day 1 low, closes above midpoint
        open_arr = np.array([105.0, 98.0])  # Day 2 opens below day 1's low (99)
        high = np.array([106.0, 104.0])
        low = np.array([99.0, 97.0])
        close = np.array([100.0, 103.5])  # Day 1: bearish (105->100), Day 2: bullish, closes above 102.5 midpoint

        result = CDLPIERCING(open_arr, high, low, close)

        assert result[0] == 0  # No pattern on first day
        assert result[1] == 100  # Piercing line

    def test_cdlpiercing_first_value(self):
        """Verify first value is always 0."""
        open_arr = np.array([100.0, 95.0])
        high = np.array([102.0, 105.0])
        low = np.array([99.0, 94.0])
        close = np.array([99.5, 104.0])

        result = CDLPIERCING(open_arr, high, low, close)
        assert result[0] == 0
