"""Tests for Dow Theory trend classification."""

import numpy as np
import pytest

from cluefin_ta import DOW_THEORY


def _make_trending_series(
    n: int,
    slope: float,
    amplitude: float = 2.0,
    period: int = 10,
    base: float = 100.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = np.arange(n, dtype=np.float64)
    close = base + slope * x + amplitude * np.sin(2 * np.pi * x / period)
    high = close + 1.0
    low = close - 1.0
    return high, low, close


class TestDOW_THEORY:
    """Tests for Dow Theory trend classification."""

    def test_swing_uptrend_detection(self):
        """Uptrend with swings should be detected as Bull."""
        high, low, close = _make_trending_series(120, slope=0.2)
        trend, corr = DOW_THEORY(
            high,
            low,
            close,
            swing_window=3,
            primary_period=30,
            method="swing",
        )

        assert len(trend) == 120
        assert np.all(np.isnan(corr))
        assert np.all(trend[-20:] == 1)

    def test_swing_downtrend_detection(self):
        """Downtrend with swings should be detected as Bear."""
        high, low, close = _make_trending_series(120, slope=-0.2)
        trend, _ = DOW_THEORY(
            high,
            low,
            close,
            swing_window=3,
            primary_period=30,
            method="swing",
        )

        assert np.all(trend[-20:] == -1)

    def test_swing_sideways_detection(self):
        """No slope should result in Sideways trend."""
        high, low, close = _make_trending_series(120, slope=0.0)
        trend, _ = DOW_THEORY(
            high,
            low,
            close,
            swing_window=3,
            primary_period=30,
            method="swing",
        )

        assert np.all(trend[-20:] == 0)

    def test_volume_upgrade_strong_bull(self):
        """Increasing volume should upgrade Bull trend to Strong Bull."""
        n = 120
        close = np.linspace(100, 200, n)
        high = close + 1.0
        low = close - 1.0
        volume = np.linspace(1000, 2000, n)

        trend, _ = DOW_THEORY(
            high,
            low,
            close,
            volume=volume,
            method="ma_cross",
            minor_period=5,
            secondary_period=10,
            primary_period=20,
            volume_ma_period=5,
        )

        assert np.sum(trend[-20:] == 2) >= 10

    def test_volume_no_upgrade_when_decreasing(self):
        """Decreasing volume should not upgrade Bull trend."""
        n = 120
        close = np.linspace(100, 200, n)
        high = close + 1.0
        low = close - 1.0
        volume = np.linspace(2000, 1000, n)

        trend, _ = DOW_THEORY(
            high,
            low,
            close,
            volume=volume,
            method="ma_cross",
            minor_period=5,
            secondary_period=10,
            primary_period=20,
            volume_ma_period=5,
        )

        assert np.all(trend[-20:] <= 1)
        assert np.all(trend[-20:] >= -1)

    def test_index_confirmed(self):
        """Same direction trends should be confirmed (1.0)."""
        n = 120
        close = np.linspace(100, 200, n)
        high = close + 1.0
        low = close - 1.0
        index_close = np.linspace(1000, 1100, n)
        index_high = index_close + 1.0
        index_low = index_close - 1.0

        _, corr = DOW_THEORY(
            high,
            low,
            close,
            index_high=index_high,
            index_low=index_low,
            index_close=index_close,
            method="ma_cross",
            minor_period=5,
            secondary_period=10,
            primary_period=20,
        )

        assert np.all(corr[-10:] == 1.0)

    def test_index_diverging(self):
        """Opposite trends should be diverging (-1.0)."""
        n = 120
        close = np.linspace(100, 200, n)
        high = close + 1.0
        low = close - 1.0
        index_close = np.linspace(1100, 1000, n)
        index_high = index_close + 1.0
        index_low = index_close - 1.0

        _, corr = DOW_THEORY(
            high,
            low,
            close,
            index_high=index_high,
            index_low=index_low,
            index_close=index_close,
            method="ma_cross",
            minor_period=5,
            secondary_period=10,
            primary_period=20,
        )

        assert np.all(corr[-10:] == -1.0)

    def test_method_hybrid_consensus(self):
        """Hybrid should be Bull when both swing and MA agree."""
        high, low, close = _make_trending_series(120, slope=0.2)
        trend, _ = DOW_THEORY(
            high,
            low,
            close,
            method="hybrid",
            swing_window=3,
            minor_period=5,
            secondary_period=10,
            primary_period=30,
        )

        assert np.any(trend[-10:] == 1)
        assert np.all(trend[-10:] >= 0)

    def test_invalid_method(self):
        """Invalid method should raise ValueError."""
        high, low, close = _make_trending_series(50, slope=0.1)
        with pytest.raises(ValueError):
            DOW_THEORY(high, low, close, method="bad_method")

    def test_insufficient_data(self):
        """Insufficient data should return all NaN."""
        high, low, close = _make_trending_series(20, slope=0.1)
        trend, corr = DOW_THEORY(
            high,
            low,
            close,
            method="swing",
            swing_window=3,
            primary_period=30,
        )

        assert np.all(np.isnan(trend))
        assert np.all(np.isnan(corr))

    def test_volume_length_mismatch(self):
        """Volume length mismatch should raise ValueError."""
        high, low, close = _make_trending_series(50, slope=0.1)
        volume = np.linspace(1000, 1100, 49)
        with pytest.raises(ValueError):
            DOW_THEORY(high, low, close, volume=volume)

    def test_index_partial_input(self):
        """Partial index inputs should raise ValueError."""
        high, low, close = _make_trending_series(50, slope=0.1)
        with pytest.raises(ValueError):
            DOW_THEORY(high, low, close, index_close=close)

    def test_no_index_returns_nan_corr(self):
        """No index data should return NaN correlation."""
        high, low, close = _make_trending_series(120, slope=0.2)
        _, corr = DOW_THEORY(
            high,
            low,
            close,
            method="swing",
            swing_window=3,
            primary_period=30,
        )

        assert np.all(np.isnan(corr))

    def test_output_shapes(self):
        """Output arrays should match input length."""
        high, low, close = _make_trending_series(80, slope=0.1)
        trend, corr = DOW_THEORY(
            high,
            low,
            close,
            method="ma_cross",
            minor_period=5,
            secondary_period=10,
            primary_period=20,
        )

        assert len(trend) == 80
        assert len(corr) == 80

    def test_output_range(self):
        """Trend output should be within -2..2 or NaN."""
        high, low, close = _make_trending_series(120, slope=0.1)
        trend, _ = DOW_THEORY(
            high,
            low,
            close,
            method="ma_cross",
            minor_period=5,
            secondary_period=10,
            primary_period=20,
        )

        valid = trend[~np.isnan(trend)]
        assert np.all(np.isin(valid, [-2, -1, 0, 1, 2]))

    def test_correlation_range(self):
        """Correlation output should be -1, 0, 1 or NaN."""
        high, low, close = _make_trending_series(120, slope=0.1)
        index_high, index_low, index_close = _make_trending_series(120, slope=0.1)
        _, corr = DOW_THEORY(
            high,
            low,
            close,
            index_high=index_high,
            index_low=index_low,
            index_close=index_close,
            method="ma_cross",
            minor_period=5,
            secondary_period=10,
            primary_period=20,
        )

        valid = corr[~np.isnan(corr)]
        assert np.all(np.isin(valid, [-1.0, 0.0, 1.0]))

    def test_nan_handling_ma_cross(self):
        """NaN in close should propagate to trend in MA method."""
        n = 60
        close = np.linspace(100, 130, n)
        close[25] = np.nan
        high = close + 1.0
        low = close - 1.0

        trend, _ = DOW_THEORY(
            high,
            low,
            close,
            method="ma_cross",
            minor_period=5,
            secondary_period=10,
            primary_period=20,
        )

        assert np.any(np.isnan(trend))
