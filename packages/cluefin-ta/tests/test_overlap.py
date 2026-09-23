"""
Tests for overlap indicators (SMA, EMA, WMA, DEMA, TEMA, KAMA, BBANDS).
"""

import numpy as np
import pytest
import talib

from cluefin_ta import BBANDS, DEMA, EMA, KAMA, SMA, TEMA, WMA

# (name, our func, timeperiod) for indicators whose NaN warm-up prefix is
# exactly (timeperiod - 1) values, matching ta-lib's simple lookback convention.
NAN_PREFIX_CASES = [
    ("SMA", SMA, 20),
    ("EMA", EMA, 12),
    ("WMA", WMA, 20),
    ("KAMA", KAMA, 30),
]

# (name, our func, timeperiod) for single-output overlap indicators, used to
# verify they return an all-NaN result when the input is shorter than the lookback.
SHORT_ARRAY_CASES = [
    ("SMA", SMA, 10),
    ("EMA", EMA, 10),
    ("WMA", WMA, 10),
    ("DEMA", DEMA, 10),
    ("TEMA", TEMA, 10),
    ("KAMA", KAMA, 10),
]


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

    def test_sma_default_timeperiod(self, sample_close):
        """Test SMA with default timeperiod."""
        result = SMA(sample_close)
        expected = talib.SMA(sample_close, timeperiod=30)
        mask = ~np.isnan(expected)
        np.testing.assert_allclose(result[mask], expected[mask], rtol=1e-10)

    def test_sma_empty_array(self):
        """Empty input: ta-lib returns an empty array, lock down the same behavior."""
        empty = np.array([], dtype=np.float64)
        expected = talib.SMA(empty, timeperiod=20)
        actual = SMA(empty, timeperiod=20)
        assert len(actual) == len(expected) == 0


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

    def test_bbands_length_one_matches_talib(self):
        """Verify BBANDS parity on a single-bar array (all-NaN, per ta-lib)."""
        close = np.array([100.5])

        expected_upper, expected_middle, expected_lower = talib.BBANDS(close, timeperiod=20)
        actual_upper, actual_middle, actual_lower = BBANDS(close, timeperiod=20)

        np.testing.assert_array_equal(actual_upper, expected_upper)
        np.testing.assert_array_equal(actual_middle, expected_middle)
        np.testing.assert_array_equal(actual_lower, expected_lower)


class TestWMA:
    """Tests for Weighted Moving Average."""

    def test_wma_matches_talib(self, sample_close):
        """Verify WMA matches ta-lib output."""
        timeperiod = 20
        expected = talib.WMA(sample_close, timeperiod=timeperiod)
        actual = WMA(sample_close, timeperiod=timeperiod)

        mask = ~np.isnan(expected)
        np.testing.assert_allclose(actual[mask], expected[mask], rtol=1e-10)


class TestDEMA:
    """Tests for Double Exponential Moving Average."""

    def test_dema_matches_talib(self, sample_close):
        """Verify DEMA matches ta-lib output."""
        timeperiod = 20
        expected = talib.DEMA(sample_close, timeperiod=timeperiod)
        actual = DEMA(sample_close, timeperiod=timeperiod)

        mask = ~np.isnan(expected)
        np.testing.assert_allclose(actual[mask], expected[mask], rtol=1e-10)


class TestTEMA:
    """Tests for Triple Exponential Moving Average."""

    def test_tema_matches_talib(self, sample_close):
        """Verify TEMA matches ta-lib output."""
        timeperiod = 20
        expected = talib.TEMA(sample_close, timeperiod=timeperiod)
        actual = TEMA(sample_close, timeperiod=timeperiod)

        mask = ~np.isnan(expected)
        np.testing.assert_allclose(actual[mask], expected[mask], rtol=1e-10)


class TestKAMA:
    """Tests for Kaufman Adaptive Moving Average."""

    def test_kama_matches_talib(self, sample_close):
        """Verify KAMA matches ta-lib output."""
        timeperiod = 30
        expected = talib.KAMA(sample_close, timeperiod=timeperiod)
        actual = KAMA(sample_close, timeperiod=timeperiod)

        mask = ~np.isnan(expected)
        np.testing.assert_allclose(actual[mask], expected[mask], rtol=1e-6)


@pytest.mark.parametrize("name,func,timeperiod", NAN_PREFIX_CASES, ids=[c[0] for c in NAN_PREFIX_CASES])
def test_nan_prefix(name, func, timeperiod, sample_close):
    """Verify each indicator's NaN warm-up prefix is exactly (timeperiod - 1) values."""
    result = func(sample_close, timeperiod=timeperiod)

    assert np.all(np.isnan(result[: timeperiod - 1]))
    assert not np.isnan(result[timeperiod - 1])


@pytest.mark.parametrize("name,func,timeperiod", SHORT_ARRAY_CASES, ids=[c[0] for c in SHORT_ARRAY_CASES])
def test_short_array(name, func, timeperiod, short_data):
    """Test each indicator returns all-NaN when input is shorter than timeperiod."""
    result = func(short_data, timeperiod=timeperiod)
    assert np.all(np.isnan(result))
