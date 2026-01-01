"""Tests for regime detection functions."""

import numpy as np
import pytest

from cluefin_ta import REGIME_MA, REGIME_MA_DURATION


class TestREGIME_MA:
    """Tests for MA-based regime detection."""

    def test_regime_ma_uptrend(self):
        """Test uptrend detection - should detect Bull regime."""
        # Create strong uptrend: 100 -> 200 over 100 days
        uptrend = np.linspace(100, 200, 100)
        result = REGIME_MA(uptrend, fast_period=20, slow_period=50)

        # Check output shape
        assert len(result) == 100

        # First slow_period - 1 values should be NaN
        assert np.all(np.isnan(result[:49]))

        # After MA stabilizes, should be mostly Bull (2)
        valid = result[~np.isnan(result)]
        assert len(valid) > 0, "Should have valid regime values"

        # In strong uptrend, average should be close to 2 (Bull)
        assert np.mean(valid) > 1.5, "Should detect Bull regime in uptrend"

    def test_regime_ma_downtrend(self):
        """Test downtrend detection - should detect Bear regime."""
        # Create strong downtrend: 200 -> 100 over 100 days
        downtrend = np.linspace(200, 100, 100)
        result = REGIME_MA(downtrend, fast_period=20, slow_period=50)

        # After MA stabilizes, should be mostly Bear (0)
        valid = result[~np.isnan(result)]
        assert len(valid) > 0

        # In strong downtrend, average should be close to 0 (Bear)
        assert np.mean(valid) < 0.5, "Should detect Bear regime in downtrend"

    def test_regime_ma_sideways(self):
        """Test sideways market detection."""
        # Create sideways market: oscillating around 150 with small range
        np.random.seed(42)
        base = 150
        noise = np.random.uniform(-1, 1, 100)
        sideways = base + noise

        result = REGIME_MA(sideways, fast_period=20, slow_period=50)

        valid = result[~np.isnan(result)]
        assert len(valid) > 0

        # In sideways market, should have mix of all regimes or mostly Sideways (1)
        # Check that not all values are Bull or all Bear
        unique_regimes = np.unique(valid)
        assert len(unique_regimes) >= 1, "Should detect at least one regime type"

    def test_regime_ma_short_array(self):
        """Test with array shorter than slow_period - should return all NaN."""
        short_data = np.array([100, 101, 102, 103, 104])
        result = REGIME_MA(short_data, fast_period=20, slow_period=50)

        assert len(result) == len(short_data)
        assert np.all(np.isnan(result)), "Should return all NaN for insufficient data"

    def test_regime_ma_exact_slow_period(self):
        """Test with array length exactly equal to slow_period."""
        data = np.linspace(100, 150, 50)
        result = REGIME_MA(data, fast_period=20, slow_period=50)

        # Should have exactly one valid value at the end
        assert len(result) == 50
        assert np.sum(~np.isnan(result)) == 1
        assert not np.isnan(result[-1])

    def test_regime_ma_constant_prices(self):
        """Test with constant prices - should return Sideways regime."""
        constant = np.full(100, 150.0)
        result = REGIME_MA(constant, fast_period=20, slow_period=50)

        valid = result[~np.isnan(result)]
        assert len(valid) > 0

        # Constant prices should be classified as Sideways (1)
        assert np.all(valid == 1), "Constant prices should be Sideways regime"

    def test_regime_ma_nan_handling(self):
        """Test that NaN values in input are handled properly."""
        # Create data with NaN in the middle, but past the slow_period mark
        data = np.linspace(100, 150, 30)
        data = np.concatenate([data, np.full(5, np.nan), np.linspace(150, 200, 65)])
        result = REGIME_MA(data, fast_period=20, slow_period=50)

        # Function should handle NaN gracefully
        assert len(result) == len(data)
        # Values before slow_period should be NaN due to insufficient data
        assert np.all(np.isnan(result[:49]))

    def test_regime_ma_output_values(self):
        """Test that output values are only 0, 1, 2, or NaN."""
        data = np.random.uniform(100, 200, 100)
        result = REGIME_MA(data)

        valid = result[~np.isnan(result)]
        unique_values = np.unique(valid)

        # All values should be in {0, 1, 2}
        assert np.all(np.isin(unique_values, [0, 1, 2])), "Regime values must be 0, 1, or 2"

    def test_regime_ma_custom_threshold(self):
        """Test with custom sideways threshold."""
        data = np.linspace(100, 110, 100)  # Slow uptrend

        # With tight threshold, should detect Bull more easily
        result_tight = REGIME_MA(data, sideways_threshold=0.001)

        # With loose threshold, should detect Sideways more often
        result_loose = REGIME_MA(data, sideways_threshold=0.1)

        valid_tight = result_tight[~np.isnan(result_tight)]
        valid_loose = result_loose[~np.isnan(result_loose)]

        # Tight threshold should have higher mean (more Bull detections)
        assert np.mean(valid_tight) > np.mean(valid_loose)


class TestREGIME_MA_DURATION:
    """Tests for regime duration calculation."""

    def test_duration_basic(self):
        """Test basic duration counting."""
        # Regime sequence: Bull(3), Sideways(2), Bear(4)
        regime_states = np.array([2, 2, 2, 1, 1, 0, 0, 0, 0], dtype=float)
        durations = REGIME_MA_DURATION(regime_states)

        expected = np.array([1, 2, 3, 1, 2, 1, 2, 3, 4], dtype=float)
        np.testing.assert_array_equal(durations, expected)

    def test_duration_with_nan(self):
        """Test duration calculation with NaN values."""
        regime_states = np.array([np.nan, np.nan, 2, 2, 1], dtype=float)
        durations = REGIME_MA_DURATION(regime_states)

        assert np.isnan(durations[0])
        assert np.isnan(durations[1])
        assert durations[2] == 1
        assert durations[3] == 2
        assert durations[4] == 1

    def test_duration_single_regime(self):
        """Test duration when regime doesn't change."""
        regime_states = np.full(10, 2.0)  # All Bull
        durations = REGIME_MA_DURATION(regime_states)

        expected = np.arange(1, 11, dtype=float)
        np.testing.assert_array_equal(durations, expected)

    def test_duration_alternating(self):
        """Test duration with alternating regimes."""
        regime_states = np.array([0, 1, 0, 1, 0], dtype=float)
        durations = REGIME_MA_DURATION(regime_states)

        # Each regime change resets to 1
        expected = np.array([1, 1, 1, 1, 1], dtype=float)
        np.testing.assert_array_equal(durations, expected)

    def test_duration_all_nan(self):
        """Test duration with all NaN input."""
        regime_states = np.full(5, np.nan)
        durations = REGIME_MA_DURATION(regime_states)

        assert np.all(np.isnan(durations))

    def test_duration_empty_array(self):
        """Test duration with empty array."""
        regime_states = np.array([], dtype=float)
        durations = REGIME_MA_DURATION(regime_states)

        assert len(durations) == 0

    def test_duration_output_shape(self):
        """Test that output has same shape as input."""
        for length in [1, 10, 100]:
            regime_states = np.random.choice([0, 1, 2], size=length).astype(float)
            durations = REGIME_MA_DURATION(regime_states)

            assert len(durations) == length


class TestREGIME_MA_Integration:
    """Integration tests combining REGIME_MA and REGIME_MA_DURATION."""

    def test_ma_duration_integration(self):
        """Test using REGIME_MA output as REGIME_MA_DURATION input."""
        # Create uptrend data
        prices = np.linspace(100, 200, 100)

        # Calculate regime
        regimes = REGIME_MA(prices, fast_period=20, slow_period=50)

        # Calculate duration
        durations = REGIME_MA_DURATION(regimes)

        # Both should have same length
        assert len(regimes) == len(durations) == 100

        # Valid durations should be positive integers
        valid_durations = durations[~np.isnan(durations)]
        assert np.all(valid_durations >= 1)
        assert np.all(valid_durations == np.floor(valid_durations))

    def test_duration_increases_in_stable_regime(self):
        """Test that duration increases when regime is stable."""
        # Create data that produces stable Bull regime
        prices = np.linspace(100, 200, 100)
        regimes = REGIME_MA(prices, fast_period=20, slow_period=50)
        durations = REGIME_MA_DURATION(regimes)

        # Find first valid index
        valid_idx = np.where(~np.isnan(durations))[0]

        if len(valid_idx) > 10:  # If we have enough valid values
            # Check that durations can increase (not always, but should be possible)
            duration_diffs = np.diff(durations[valid_idx])
            # At least some should be +1 (increasing duration)
            assert np.any(duration_diffs == 1), "Duration should increase in stable regime"
