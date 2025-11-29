"""
Tests to verify NumPy and Numba implementations produce identical results.

These tests ensure that the optimized Numba implementations match
the reference NumPy implementations exactly.
"""

import numpy as np
import pytest

from cluefin_ta._core import HAS_NUMBA, numpy_impl

if HAS_NUMBA:
    from cluefin_ta._core import numba_impl


@pytest.mark.skipif(not HAS_NUMBA, reason="Numba not installed")
class TestEmaLoopParity:
    """Verify EMA loop implementations match."""

    def test_ema_loop_basic(self, sample_close):
        """Test basic EMA calculation parity."""
        period = 12
        alpha = 2.0 / (period + 1)
        initial_sma = np.mean(sample_close[:period])

        numpy_result = numpy_impl.ema_loop(sample_close, period, alpha, initial_sma)
        numba_result = numba_impl.ema_loop(sample_close, period, alpha, initial_sma)

        # Check non-NaN values match
        mask = ~np.isnan(numpy_result)
        np.testing.assert_allclose(numba_result[mask], numpy_result[mask], rtol=1e-14)

    def test_ema_loop_nan_positions(self, sample_close):
        """Verify NaN positions are identical."""
        period = 20
        alpha = 2.0 / (period + 1)
        initial_sma = np.mean(sample_close[:period])

        numpy_result = numpy_impl.ema_loop(sample_close, period, alpha, initial_sma)
        numba_result = numba_impl.ema_loop(sample_close, period, alpha, initial_sma)

        np.testing.assert_array_equal(np.isnan(numpy_result), np.isnan(numba_result))


@pytest.mark.skipif(not HAS_NUMBA, reason="Numba not installed")
class TestRollingStdParity:
    """Verify rolling standard deviation implementations match."""

    def test_rolling_std_basic(self, sample_close):
        """Test basic rolling std parity."""
        period = 20

        numpy_result = numpy_impl.rolling_std(sample_close, period)
        numba_result = numba_impl.rolling_std(sample_close, period)

        mask = ~np.isnan(numpy_result)
        np.testing.assert_allclose(numba_result[mask], numpy_result[mask], rtol=1e-14)

    def test_rolling_std_small_period(self, sample_close):
        """Test with small period."""
        period = 5

        numpy_result = numpy_impl.rolling_std(sample_close, period)
        numba_result = numba_impl.rolling_std(sample_close, period)

        mask = ~np.isnan(numpy_result)
        np.testing.assert_allclose(numba_result[mask], numpy_result[mask], rtol=1e-14)


@pytest.mark.skipif(not HAS_NUMBA, reason="Numba not installed")
class TestWilderSmoothParity:
    """Verify Wilder smoothing implementations match."""

    def test_wilder_smooth_basic(self, sample_close):
        """Test basic Wilder smoothing parity."""
        period = 14
        values = np.abs(np.diff(sample_close))
        initial_value = np.mean(values[:period])
        start_idx = period - 1

        numpy_result = numpy_impl.wilder_smooth(values, period, initial_value, start_idx)
        numba_result = numba_impl.wilder_smooth(values, period, initial_value, start_idx)

        mask = ~np.isnan(numpy_result)
        np.testing.assert_allclose(numba_result[mask], numpy_result[mask], rtol=1e-14)


@pytest.mark.skipif(not HAS_NUMBA, reason="Numba not installed")
class TestRollingMinMaxParity:
    """Verify rolling min/max implementations match."""

    def test_rolling_minmax_basic(self, sample_ohlcv):
        """Test basic rolling min/max parity."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        period = 14

        numpy_highest, numpy_lowest = numpy_impl.rolling_minmax(high, low, period)
        numba_highest, numba_lowest = numba_impl.rolling_minmax(high, low, period)

        mask_h = ~np.isnan(numpy_highest)
        mask_l = ~np.isnan(numpy_lowest)

        np.testing.assert_allclose(numba_highest[mask_h], numpy_highest[mask_h], rtol=1e-14)
        np.testing.assert_allclose(numba_lowest[mask_l], numpy_lowest[mask_l], rtol=1e-14)

    def test_rolling_minmax_small_period(self, sample_ohlcv):
        """Test with small period."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        period = 5

        numpy_highest, numpy_lowest = numpy_impl.rolling_minmax(high, low, period)
        numba_highest, numba_lowest = numba_impl.rolling_minmax(high, low, period)

        mask_h = ~np.isnan(numpy_highest)
        np.testing.assert_allclose(numba_highest[mask_h], numpy_highest[mask_h], rtol=1e-14)


@pytest.mark.skipif(not HAS_NUMBA, reason="Numba not installed")
class TestTrueRangeParity:
    """Verify True Range implementations match."""

    def test_true_range_basic(self, sample_ohlcv):
        """Test basic True Range parity."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]

        numpy_result = numpy_impl.true_range_loop(high, low, close)
        numba_result = numba_impl.true_range_loop(high, low, close)

        mask = ~np.isnan(numpy_result)
        np.testing.assert_allclose(numba_result[mask], numpy_result[mask], rtol=1e-14)


@pytest.mark.skipif(not HAS_NUMBA, reason="Numba not installed")
class TestOBVParity:
    """Verify OBV implementations match."""

    def test_obv_basic(self, sample_ohlcv):
        """Test basic OBV parity."""
        close = sample_ohlcv["close"]
        volume = sample_ohlcv["volume"]

        numpy_result = numpy_impl.obv_loop(close, volume)
        numba_result = numba_impl.obv_loop(close, volume)

        np.testing.assert_allclose(numba_result, numpy_result, rtol=1e-14)


@pytest.mark.skipif(not HAS_NUMBA, reason="Numba not installed")
class TestADParity:
    """Verify A/D implementations match."""

    def test_ad_basic(self, sample_ohlcv):
        """Test basic A/D parity."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]
        volume = sample_ohlcv["volume"]

        numpy_result = numpy_impl.ad_loop(high, low, close, volume)
        numba_result = numba_impl.ad_loop(high, low, close, volume)

        np.testing.assert_allclose(numba_result, numpy_result, rtol=1e-14)


class TestBackendDetection:
    """Test backend detection and switching."""

    def test_get_backend_returns_string(self):
        """Verify get_backend returns expected string."""
        from cluefin_ta._core import get_backend

        backend = get_backend()
        assert backend in ("numpy", "numba")

    def test_has_numba_is_boolean(self):
        """Verify HAS_NUMBA is boolean."""
        assert isinstance(HAS_NUMBA, bool)

    def test_get_impl_returns_module(self):
        """Verify get_impl returns a module with required functions."""
        from cluefin_ta._core import get_impl

        impl = get_impl()

        # Verify required functions exist
        assert hasattr(impl, "ema_loop")
        assert hasattr(impl, "rolling_std")
        assert hasattr(impl, "wilder_smooth")
        assert hasattr(impl, "rolling_minmax")
        assert hasattr(impl, "true_range_loop")
        assert hasattr(impl, "obv_loop")
        assert hasattr(impl, "ad_loop")

    def test_consistent_backend(self):
        """Verify backend is consistent across calls."""
        from cluefin_ta._core import get_backend, get_impl

        backend1 = get_backend()
        impl1 = get_impl()
        backend2 = get_backend()
        impl2 = get_impl()

        assert backend1 == backend2
        assert impl1 is impl2  # Same cached instance
