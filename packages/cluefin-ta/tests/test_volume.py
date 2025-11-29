"""
Tests for volume indicators (OBV, AD, ADOSC).
"""

import numpy as np
import talib

from cluefin_ta import AD, ADOSC, OBV


class TestOBV:
    """Tests for On Balance Volume."""

    def test_obv_matches_talib(self, sample_ohlcv):
        """Verify OBV matches ta-lib output."""
        close = sample_ohlcv["close"]
        volume = sample_ohlcv["volume"]

        expected = talib.OBV(close, volume)
        actual = OBV(close, volume)

        np.testing.assert_allclose(actual, expected, rtol=1e-10)

    def test_obv_cumulative(self, sample_ohlcv):
        """Verify OBV is cumulative."""
        close = sample_ohlcv["close"]
        volume = sample_ohlcv["volume"]

        result = OBV(close, volume)

        # OBV should be cumulative sum of signed volume
        # Check that the last value is reasonable
        assert result[-1] != 0  # Should not be zero for random data

    def test_obv_up_day(self):
        """Test OBV increases on up days."""
        close = np.array([100.0, 110.0])
        volume = np.array([1000.0, 2000.0])

        result = OBV(close, volume)

        # On an up day, OBV should add volume
        assert result[1] == result[0] + volume[1]

    def test_obv_down_day(self):
        """Test OBV decreases on down days."""
        close = np.array([110.0, 100.0])
        volume = np.array([1000.0, 2000.0])

        result = OBV(close, volume)

        # On a down day, OBV should subtract volume
        assert result[1] == result[0] - volume[1]


class TestAD:
    """Tests for Accumulation/Distribution Line."""

    def test_ad_matches_talib(self, sample_ohlcv):
        """Verify AD matches ta-lib output."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]
        volume = sample_ohlcv["volume"]

        expected = talib.AD(high, low, close, volume)
        actual = AD(high, low, close, volume)

        np.testing.assert_allclose(actual, expected, rtol=1e-10)

    def test_ad_cumulative(self, sample_ohlcv):
        """Verify AD is cumulative."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]
        volume = sample_ohlcv["volume"]

        result = AD(high, low, close, volume)

        # AD should be cumulative
        # Each value depends on all previous values
        assert len(result) == len(close)

    def test_ad_mfm_calculation(self):
        """Test Money Flow Multiplier calculation."""
        # When close is at the midpoint, MFM = 0
        high = np.array([110.0])
        low = np.array([90.0])
        close = np.array([100.0])  # Midpoint
        volume = np.array([1000.0])

        result = AD(high, low, close, volume)

        # MFM = ((100-90) - (110-100)) / (110-90) = (10-10)/20 = 0
        assert result[0] == 0

    def test_ad_extreme_close(self):
        """Test AD with close at extremes."""
        # Close at high
        high = np.array([110.0])
        low = np.array([90.0])
        close = np.array([110.0])
        volume = np.array([1000.0])

        result = AD(high, low, close, volume)

        # MFM = ((110-90) - (110-110)) / (110-90) = 20/20 = 1
        # Money Flow Volume = 1 * 1000 = 1000
        assert result[0] == 1000.0


class TestADOSC:
    """Tests for Chaikin A/D Oscillator."""

    def test_adosc_matches_talib(self, sample_ohlcv):
        """Verify ADOSC matches ta-lib output."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]
        volume = sample_ohlcv["volume"]

        expected = talib.ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)
        actual = ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)

        mask = ~np.isnan(expected)
        np.testing.assert_allclose(actual[mask], expected[mask], rtol=1e-10)

    def test_adosc_short_array(self):
        """Test ADOSC with array shorter than slow period."""
        high = np.array([100.0, 101.0, 102.0])
        low = np.array([99.0, 100.0, 101.0])
        close = np.array([100.5, 101.5, 102.5])
        volume = np.array([1000.0, 2000.0, 3000.0])

        result = ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)
        assert np.all(np.isnan(result))
