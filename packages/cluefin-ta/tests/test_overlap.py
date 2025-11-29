"""
Tests for overlap indicators (SMA, EMA, BBANDS).
"""

import numpy as np
import pytest
import talib

from cluefin_ta import BBANDS, EMA, SMA


class TestSMA:
    """Tests for Simple Moving Average."""

    def test_sma_matches_talib(self, sample_close):
        """Verify SMA matches ta-lib output."""
        timeperiod = 20
        expected = talib.SMA(sample_close, timeperiod=timeperiod)
        actual = SMA(sample_close, timeperiod=timeperiod)

        # Compare non-NaN values
        mask = ~np.isnan(expected)
        np.testing.assert_allclose(actual[mask], expected[mask], rtol=1e-10)

    def test_sma_nan_prefix(self, sample_close):
        """Verify SMA has correct NaN prefix."""
        timeperiod = 20
        result = SMA(sample_close, timeperiod=timeperiod)

        # First (timeperiod - 1) values should be NaN
        assert np.all(np.isnan(result[: timeperiod - 1]))
        # Value at index (timeperiod - 1) should not be NaN
        assert not np.isnan(result[timeperiod - 1])

    def test_sma_short_array(self, short_data):
        """Test SMA with array shorter than timeperiod."""
        result = SMA(short_data, timeperiod=10)
        assert np.all(np.isnan(result))

    def test_sma_default_timeperiod(self, sample_close):
        """Test SMA with default timeperiod."""
        result = SMA(sample_close)
        expected = talib.SMA(sample_close, timeperiod=30)
        mask = ~np.isnan(expected)
        np.testing.assert_allclose(result[mask], expected[mask], rtol=1e-10)


class TestEMA:
    """Tests for Exponential Moving Average."""

    def test_ema_matches_talib(self, sample_close):
        """Verify EMA matches ta-lib output."""
        timeperiod = 12
        expected = talib.EMA(sample_close, timeperiod=timeperiod)
        actual = EMA(sample_close, timeperiod=timeperiod)

        # Compare non-NaN values
        mask = ~np.isnan(expected)
        np.testing.assert_allclose(actual[mask], expected[mask], rtol=1e-10)

    def test_ema_nan_prefix(self, sample_close):
        """Verify EMA has correct NaN prefix."""
        timeperiod = 12
        result = EMA(sample_close, timeperiod=timeperiod)

        # First (timeperiod - 1) values should be NaN
        assert np.all(np.isnan(result[: timeperiod - 1]))
        # Value at index (timeperiod - 1) should not be NaN
        assert not np.isnan(result[timeperiod - 1])

    def test_ema_short_array(self, short_data):
        """Test EMA with array shorter than timeperiod."""
        result = EMA(short_data, timeperiod=10)
        assert np.all(np.isnan(result))


class TestBBANDS:
    """Tests for Bollinger Bands."""

    def test_bbands_matches_talib(self, sample_close):
        """Verify BBANDS matches ta-lib output."""
        timeperiod = 20
        nbdevup = 2.0
        nbdevdn = 2.0

        expected_upper, expected_middle, expected_lower = talib.BBANDS(
            sample_close, timeperiod=timeperiod, nbdevup=nbdevup, nbdevdn=nbdevdn
        )
        actual_upper, actual_middle, actual_lower = BBANDS(
            sample_close, timeperiod=timeperiod, nbdevup=nbdevup, nbdevdn=nbdevdn
        )

        # Compare non-NaN values
        mask = ~np.isnan(expected_middle)
        np.testing.assert_allclose(actual_upper[mask], expected_upper[mask], rtol=1e-10)
        np.testing.assert_allclose(actual_middle[mask], expected_middle[mask], rtol=1e-10)
        np.testing.assert_allclose(actual_lower[mask], expected_lower[mask], rtol=1e-10)

    def test_bbands_symmetric_bands(self, sample_close):
        """Verify bands are symmetric when nbdevup == nbdevdn."""
        upper, middle, lower = BBANDS(sample_close, timeperiod=20, nbdevup=2.0, nbdevdn=2.0)

        mask = ~np.isnan(middle)
        upper_dist = upper[mask] - middle[mask]
        lower_dist = middle[mask] - lower[mask]

        np.testing.assert_allclose(upper_dist, lower_dist, rtol=1e-10)

    def test_bbands_short_array(self, short_data):
        """Test BBANDS with array shorter than timeperiod."""
        upper, middle, lower = BBANDS(short_data, timeperiod=10)
        assert np.all(np.isnan(upper))
        assert np.all(np.isnan(middle))
        assert np.all(np.isnan(lower))
