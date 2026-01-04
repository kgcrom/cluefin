"""
Tests for candlestick pattern recognition.
"""

import numpy as np

from cluefin_ta import (
    CDLDARKCLOUDCOVER,
    CDLDOJI,
    CDLENGULFING,
    CDLEVENINGSTAR,
    CDLHAMMER,
    CDLHANGINGMAN,
    CDLHARAMI,
    CDLMORNINGSTAR,
    CDLPIERCING,
    CDLSHOOTINGSTAR,
    CUP_HANDLE,
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


class TestCDLMORNINGSTAR:
    """Tests for Morning Star pattern (3-bar bullish reversal)."""

    def test_cdlmorningstar_output_values(self, sample_ohlcv):
        """Verify CDLMORNINGSTAR returns valid values."""
        result = CDLMORNINGSTAR(
            sample_ohlcv["open"],
            sample_ohlcv["high"],
            sample_ohlcv["low"],
            sample_ohlcv["close"],
        )

        unique_values = np.unique(result)
        valid_values = {0, 100}
        assert set(unique_values).issubset(valid_values)

    def test_cdlmorningstar_perfect(self):
        """Test detection of perfect morning star pattern."""
        # Day 1: Large bearish candle
        # Day 2: Small body (star) that gaps down
        # Day 3: Large bullish candle that closes above day 1 midpoint
        open_arr = np.array([110.0, 98.0, 99.0])
        high = np.array([111.0, 99.0, 108.0])
        low = np.array([99.0, 97.0, 98.0])
        close = np.array([100.0, 98.5, 107.0])

        result = CDLMORNINGSTAR(open_arr, high, low, close)

        assert result[0] == 0  # No pattern on first day
        assert result[1] == 0  # No pattern on second day
        assert result[2] == 100  # Morning star detected on third day

    def test_cdlmorningstar_no_gap(self):
        """Test that pattern requires gap down for star."""
        # Day 2 doesn't gap down from day 1
        open_arr = np.array([110.0, 102.0, 99.0])  # Day 2 open too high
        high = np.array([111.0, 103.0, 108.0])
        low = np.array([99.0, 101.0, 98.0])
        close = np.array([100.0, 102.5, 107.0])

        result = CDLMORNINGSTAR(open_arr, high, low, close)

        assert result[2] == 0  # No pattern - star didn't gap down

    def test_cdlmorningstar_first_two_values(self):
        """Verify first two values are always 0 (needs 3 candles)."""
        open_arr = np.array([110.0, 98.0, 99.0])
        high = np.array([111.0, 99.0, 108.0])
        low = np.array([99.0, 97.0, 98.0])
        close = np.array([100.0, 98.5, 107.0])

        result = CDLMORNINGSTAR(open_arr, high, low, close)

        assert result[0] == 0
        assert result[1] == 0

    def test_cdlmorningstar_short_array(self):
        """Test with array shorter than 3 elements."""
        open_arr = np.array([100.0, 95.0])
        high = np.array([102.0, 96.0])
        low = np.array([99.0, 94.0])
        close = np.array([99.5, 95.5])

        result = CDLMORNINGSTAR(open_arr, high, low, close)

        assert len(result) == 2
        assert np.all(result == 0)


class TestCDLEVENINGSTAR:
    """Tests for Evening Star pattern (3-bar bearish reversal)."""

    def test_cdleveningstar_output_values(self, sample_ohlcv):
        """Verify CDLEVENINGSTAR returns valid values."""
        result = CDLEVENINGSTAR(
            sample_ohlcv["open"],
            sample_ohlcv["high"],
            sample_ohlcv["low"],
            sample_ohlcv["close"],
        )

        unique_values = np.unique(result)
        valid_values = {-100, 0}
        assert set(unique_values).issubset(valid_values)

    def test_cdleveningstar_perfect(self):
        """Test detection of perfect evening star pattern."""
        # Day 1: Large bullish candle
        # Day 2: Small body (star) that gaps up
        # Day 3: Large bearish candle that closes below day 1 midpoint
        open_arr = np.array([100.0, 112.0, 111.0])
        high = np.array([111.0, 113.0, 112.0])
        low = np.array([99.0, 111.0, 102.0])
        close = np.array([110.0, 112.5, 103.0])

        result = CDLEVENINGSTAR(open_arr, high, low, close)

        assert result[0] == 0  # No pattern on first day
        assert result[1] == 0  # No pattern on second day
        assert result[2] == -100  # Evening star detected on third day

    def test_cdleveningstar_no_gap(self):
        """Test that pattern requires gap up for star."""
        # Day 2 doesn't gap up from day 1
        open_arr = np.array([100.0, 108.0, 109.0])  # Day 2 open not above day 1 close
        high = np.array([111.0, 109.0, 110.0])
        low = np.array([99.0, 107.0, 102.0])
        close = np.array([110.0, 108.5, 103.0])

        result = CDLEVENINGSTAR(open_arr, high, low, close)

        assert result[2] == 0  # No pattern - star didn't gap up

    def test_cdleveningstar_first_two_values(self):
        """Verify first two values are always 0 (needs 3 candles)."""
        open_arr = np.array([100.0, 112.0, 111.0])
        high = np.array([111.0, 113.0, 112.0])
        low = np.array([99.0, 111.0, 102.0])
        close = np.array([110.0, 112.5, 103.0])

        result = CDLEVENINGSTAR(open_arr, high, low, close)

        assert result[0] == 0
        assert result[1] == 0


class TestCDLDARKCLOUDCOVER:
    """Tests for Dark Cloud Cover pattern (2-bar bearish reversal)."""

    def test_cdldarkcloudcover_output_values(self, sample_ohlcv):
        """Verify CDLDARKCLOUDCOVER returns valid values."""
        result = CDLDARKCLOUDCOVER(
            sample_ohlcv["open"],
            sample_ohlcv["high"],
            sample_ohlcv["low"],
            sample_ohlcv["close"],
        )

        unique_values = np.unique(result)
        valid_values = {-100, 0}
        assert set(unique_values).issubset(valid_values)

    def test_cdldarkcloudcover_perfect(self):
        """Test detection of perfect dark cloud cover pattern."""
        # Day 1: Large bullish candle
        # Day 2: Opens above day 1 high (gap up), closes below day 1 midpoint
        open_arr = np.array([100.0, 112.0])  # Day 2 opens above day 1 high (111)
        high = np.array([111.0, 113.0])
        low = np.array([99.0, 103.0])
        close = np.array([110.0, 104.0])  # Day 2 closes below midpoint (105) but above open (100)

        result = CDLDARKCLOUDCOVER(open_arr, high, low, close)

        assert result[0] == 0  # No pattern on first day
        assert result[1] == -100  # Dark cloud cover detected

    def test_cdldarkcloudcover_no_gap(self):
        """Test that pattern requires gap up opening."""
        # Day 2 doesn't open above day 1 high
        open_arr = np.array([100.0, 109.0])  # Day 2 opens below day 1 high (111)
        high = np.array([111.0, 110.0])
        low = np.array([99.0, 103.0])
        close = np.array([110.0, 104.0])

        result = CDLDARKCLOUDCOVER(open_arr, high, low, close)

        assert result[1] == 0  # No pattern - no gap up

    def test_cdldarkcloudcover_close_above_midpoint(self):
        """Test that pattern requires close below midpoint."""
        # Day 2 closes above day 1 midpoint
        open_arr = np.array([100.0, 112.0])
        high = np.array([111.0, 113.0])
        low = np.array([99.0, 106.0])
        close = np.array([110.0, 107.0])  # Closes above midpoint (105)

        result = CDLDARKCLOUDCOVER(open_arr, high, low, close)

        assert result[1] == 0  # No pattern - close too high

    def test_cdldarkcloudcover_first_value(self):
        """Verify first value is always 0."""
        open_arr = np.array([100.0, 112.0])
        high = np.array([111.0, 113.0])
        low = np.array([99.0, 103.0])
        close = np.array([110.0, 104.0])

        result = CDLDARKCLOUDCOVER(open_arr, high, low, close)
        assert result[0] == 0


class TestCUPHANDLE:
    """Tests for Cup & Handle pattern."""

    @staticmethod
    def _build_series():
        pre = np.linspace(95.0, 100.0, 6)
        down = np.linspace(99.0, 80.0, 10)
        up = np.linspace(82.0, 100.0, 12)
        handle_down = np.linspace(100.0, 95.0, 4)
        handle_flat = np.linspace(95.0, 96.0, 3)
        breakout = np.array([97.0, 101.0, 103.0])
        close = np.concatenate(
            [pre, down, up, handle_down, handle_flat, breakout]
        ).astype(np.float64)
        open_arr = close.copy()
        high = close * 1.01
        low = close * 0.99
        return open_arr, high, low, close

    @staticmethod
    def _build_volume(n: int) -> np.ndarray:
        volume = np.full(n, 100.0, dtype=np.float64)
        volume[5:8] = 140.0
        volume[8:16] = 110.0
        volume[16:28] = 90.0
        volume[28:32] = 70.0
        volume[32:35] = 65.0
        volume[36] = 200.0
        return volume

    def test_cup_handle_breakout_without_volume(self):
        open_arr, high, low, close = self._build_series()

        result = CUP_HANDLE(
            open_arr,
            high,
            low,
            close,
            cup_lookback=40,
            cup_min_len=12,
            cup_slope_max=0.12,
            handle_len=10,
            handle_depth_max=0.08,
            pivot_method="fractal",
            pivot_left=1,
            pivot_right=1,
        )

        signal_indices = np.where(result == 100)[0]
        assert signal_indices.size == 1
        assert signal_indices[0] == 36

    def test_cup_handle_breakout_with_volume(self):
        open_arr, high, low, close = self._build_series()
        volume = self._build_volume(len(close))

        result = CUP_HANDLE(
            open_arr,
            high,
            low,
            close,
            volume=volume,
            cup_lookback=40,
            cup_min_len=12,
            cup_slope_max=0.12,
            handle_len=10,
            handle_depth_max=0.08,
            pivot_method="fractal",
            pivot_left=1,
            pivot_right=1,
            vol_lookback=5,
            vol_cup_start_len=3,
            vol_cup_start_mult=1.3,
            vol_handle_max_mult=0.9,
            vol_breakout_mult=1.5,
            use_volume=True,
        )

        signal_indices = np.where(result == 100)[0]
        assert signal_indices.size == 1
        assert signal_indices[0] == 36

    def test_cup_handle_low_breakout_volume_fails(self):
        open_arr, high, low, close = self._build_series()
        volume = self._build_volume(len(close))
        volume[36] = 80.0

        result = CUP_HANDLE(
            open_arr,
            high,
            low,
            close,
            volume=volume,
            cup_lookback=40,
            cup_min_len=12,
            cup_slope_max=0.12,
            handle_len=10,
            handle_depth_max=0.08,
            pivot_method="fractal",
            pivot_left=1,
            pivot_right=1,
            vol_lookback=5,
            vol_cup_start_len=3,
            vol_cup_start_mult=1.3,
            vol_handle_max_mult=0.9,
            vol_breakout_mult=1.5,
            use_volume=True,
        )

        assert np.all(result == 0)
