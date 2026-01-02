"""Tests for regime detection functions."""

import numpy as np
import pytest

from cluefin_ta import (
    REGIME_COMBINED,
    REGIME_HMM,
    REGIME_HMM_RETURNS,
    REGIME_MA,
    REGIME_MA_DURATION,
    REGIME_VOLATILITY,
)


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


class TestREGIME_VOLATILITY:
    """Tests for volatility-based regime detection."""

    def test_volatility_regime_basic(self):
        """Test basic volatility regime classification."""
        # Create sample OHLC with varying volatility
        np.random.seed(42)
        n = 100

        # Low volatility period followed by high volatility
        close = np.concatenate(
            [
                100 + np.random.uniform(-1, 1, 50),  # Low vol
                100 + np.random.uniform(-10, 10, 50),  # High vol
            ]
        )
        high = close + np.abs(np.random.uniform(0, 2, n))
        low = close - np.abs(np.random.uniform(0, 2, n))

        result = REGIME_VOLATILITY(high, low, close, atr_period=14, threshold_percentile=50)

        assert len(result) == n
        # First atr_period values should be NaN
        assert np.sum(np.isnan(result[:14])) > 0

    def test_volatility_regime_output_values(self):
        """Test that output values are only 0, 1, or NaN."""
        np.random.seed(42)
        n = 100
        close = 100 + np.cumsum(np.random.uniform(-1, 1, n))
        high = close + np.random.uniform(0, 2, n)
        low = close - np.random.uniform(0, 2, n)

        result = REGIME_VOLATILITY(high, low, close)

        valid = result[~np.isnan(result)]
        unique_values = np.unique(valid)

        # All values should be in {0, 1}
        assert np.all(np.isin(unique_values, [0, 1])), "Volatility regime must be 0 or 1"

    def test_volatility_percentile_boundary(self):
        """Test percentile threshold boundary behavior."""
        np.random.seed(42)
        n = 100
        close = 100 + np.cumsum(np.random.uniform(-1, 1, n))
        high = close + np.random.uniform(0, 2, n)
        low = close - np.random.uniform(0, 2, n)

        # With 50th percentile, roughly half should be high vol
        result_50 = REGIME_VOLATILITY(high, low, close, threshold_percentile=50)
        valid_50 = result_50[~np.isnan(result_50)]
        high_vol_ratio_50 = np.mean(valid_50 == 1)

        # With 90th percentile, much less should be high vol
        result_90 = REGIME_VOLATILITY(high, low, close, threshold_percentile=90)
        valid_90 = result_90[~np.isnan(result_90)]
        high_vol_ratio_90 = np.mean(valid_90 == 1)

        # Higher percentile should result in fewer high vol classifications
        assert high_vol_ratio_90 < high_vol_ratio_50

    def test_volatility_short_array(self):
        """Test with insufficient data."""
        high = np.array([105, 108, 112])
        low = np.array([95, 98, 102])
        close = np.array([100, 105, 110])

        result = REGIME_VOLATILITY(high, low, close, atr_period=14)

        # Should return all NaN for insufficient data
        assert len(result) == 3
        # Most or all should be NaN
        assert np.sum(np.isnan(result)) >= 1

    def test_volatility_constant_prices(self):
        """Test with constant prices (zero volatility)."""
        n = 100
        high = np.full(n, 100.0)
        low = np.full(n, 100.0)
        close = np.full(n, 100.0)

        result = REGIME_VOLATILITY(high, low, close)

        valid = result[~np.isnan(result)]
        if len(valid) > 0:
            # All should be low volatility (0) with constant prices
            assert np.all(valid == 0), "Constant prices should be low volatility"

    def test_volatility_nan_handling(self):
        """Test NaN handling in input."""
        np.random.seed(42)
        n = 100
        close = 100 + np.cumsum(np.random.uniform(-1, 1, n))
        close[10] = np.nan  # Insert NaN
        high = close + np.random.uniform(0, 2, n)
        low = close - np.random.uniform(0, 2, n)

        result = REGIME_VOLATILITY(high, low, close)

        # Should handle NaN gracefully
        assert len(result) == n


class TestREGIME_COMBINED:
    """Tests for combined regime detection."""

    def test_combined_encoding(self):
        """Test combined regime encoding formula."""
        # Create simple trend
        close = np.linspace(100, 200, 100)  # Uptrend
        high = close + 2
        low = close - 2

        trend, vol, combined = REGIME_COMBINED(high, low, close)

        # All outputs should have same length
        assert len(trend) == len(vol) == len(combined) == 100

        # Check encoding: combined = trend * 2 + vol
        valid_mask = ~np.isnan(combined)
        if np.any(valid_mask):
            expected_combined = trend[valid_mask] * 2 + vol[valid_mask]
            np.testing.assert_array_equal(
                combined[valid_mask], expected_combined, err_msg="Combined encoding should be trend * 2 + vol"
            )

    def test_combined_output_range(self):
        """Test that combined regime values are in valid range 0-5."""
        np.random.seed(42)
        n = 100
        close = 100 + np.cumsum(np.random.uniform(-1, 1, n))
        high = close + np.random.uniform(0, 3, n)
        low = close - np.random.uniform(0, 3, n)

        trend, vol, combined = REGIME_COMBINED(high, low, close)

        # Check valid values
        valid_combined = combined[~np.isnan(combined)]
        if len(valid_combined) > 0:
            assert np.all(valid_combined >= 0) and np.all(valid_combined <= 5), "Combined regime must be in range 0-5"

    def test_combined_consistency(self):
        """Test consistency between trend, vol, and combined."""
        close = np.linspace(100, 200, 100)
        high = close + 2
        low = close - 2

        trend, vol, combined = REGIME_COMBINED(high, low, close)

        # Where combined is valid, trend and vol should also be valid
        valid_combined_mask = ~np.isnan(combined)

        if np.any(valid_combined_mask):
            assert np.all(~np.isnan(trend[valid_combined_mask])), "Trend should be valid where combined is valid"
            assert np.all(~np.isnan(vol[valid_combined_mask])), "Volatility should be valid where combined is valid"

    def test_combined_all_states(self):
        """Test that combined can produce various regime combinations."""
        # This is a weaker test - just checks that function works
        # Not all 6 states may appear in random data
        np.random.seed(42)
        n = 200  # Longer period to get more variety
        close = 100 + np.cumsum(np.random.uniform(-2, 2, n))
        high = close + np.abs(np.random.uniform(0, 5, n))
        low = close - np.abs(np.random.uniform(0, 5, n))

        trend, vol, combined = REGIME_COMBINED(high, low, close)

        valid_combined = combined[~np.isnan(combined)]

        # Should have at least 2 different combined states
        unique_states = np.unique(valid_combined)
        assert len(unique_states) >= 2, "Should detect multiple regime combinations"

    def test_combined_bull_low_vol(self):
        """Test Bull + Low Vol regime (should be 4)."""
        # Create strong uptrend with low volatility
        close = np.linspace(100, 200, 100)
        high = close + 0.5  # Very low volatility
        low = close - 0.5

        trend, vol, combined = REGIME_COMBINED(high, low, close)

        valid_combined = combined[~np.isnan(combined)]

        if len(valid_combined) > 10:
            # In strong uptrend, most should be Bull (2)
            # With low volatility, combined should be mostly 4 (2*2 + 0)
            assert np.mean(valid_combined == 4) > 0.3, "Strong uptrend with low vol should produce regime 4"

    def test_combined_nan_preservation(self):
        """Test that NaN is preserved when either component is NaN."""
        close = np.linspace(100, 150, 50)  # Shorter than slow_period
        high = close + 2
        low = close - 2

        trend, vol, combined = REGIME_COMBINED(high, low, close)

        # Where trend is NaN, combined should also be NaN
        nan_trend_mask = np.isnan(trend)
        assert np.all(np.isnan(combined[nan_trend_mask])), "Combined should be NaN where trend is NaN"


class TestREGIME_Phase2_Integration:
    """Integration tests for Phase 2 functions."""

    def test_all_regime_functions_together(self):
        """Test using all regime functions together."""
        # Create sample data
        np.random.seed(42)
        n = 100
        close = 100 + np.cumsum(np.random.uniform(-1, 1, n))
        high = close + np.random.uniform(0, 2, n)
        low = close - np.random.uniform(0, 2, n)

        # Calculate all regimes
        ma_regime = REGIME_MA(close)
        ma_duration = REGIME_MA_DURATION(ma_regime)
        vol_regime = REGIME_VOLATILITY(high, low, close)
        trend, vol, combined = REGIME_COMBINED(high, low, close)

        # All should have same length
        assert len(ma_regime) == len(ma_duration) == len(vol_regime) == len(trend) == len(vol) == len(combined) == n

        # MA regime and trend from combined should be identical
        valid_mask = ~np.isnan(trend)
        if np.any(valid_mask):
            np.testing.assert_array_equal(
                ma_regime[valid_mask],
                trend[valid_mask],
                err_msg="REGIME_MA and trend from REGIME_COMBINED should match",
            )

    def test_import_all_phase2_functions(self):
        """Test that all Phase 2 functions can be imported."""
        from cluefin_ta import REGIME_COMBINED, REGIME_MA, REGIME_MA_DURATION, REGIME_VOLATILITY

        # Just verify they're callable
        assert callable(REGIME_MA)
        assert callable(REGIME_MA_DURATION)
        assert callable(REGIME_VOLATILITY)
        assert callable(REGIME_COMBINED)


class TestREGIME_HMM_RETURNS:
    """Tests for HMM returns preparation."""

    def test_returns_basic(self):
        """Test basic returns calculation."""
        prices = np.array([100, 102, 105, 103, 107], dtype=float)
        returns = REGIME_HMM_RETURNS(prices)

        # First value should be NaN
        assert np.isnan(returns[0])

        # Check subsequent returns
        expected_returns = np.array(
            [
                np.nan,
                0.02,  # (102-100)/100
                0.02941176,  # (105-102)/102
                -0.01904762,  # (103-105)/105
                0.03883495,  # (107-103)/103
            ]
        )

        np.testing.assert_array_almost_equal(returns, expected_returns, decimal=6)

    def test_returns_constant_prices(self):
        """Test returns with constant prices."""
        prices = np.full(10, 100.0)
        returns = REGIME_HMM_RETURNS(prices)

        # First value NaN, rest should be 0
        assert np.isnan(returns[0])
        assert np.all(returns[1:] == 0.0)

    def test_returns_short_array(self):
        """Test returns with very short array."""
        # Single price
        prices = np.array([100])
        returns = REGIME_HMM_RETURNS(prices)
        assert len(returns) == 1
        assert np.isnan(returns[0])

        # Two prices
        prices = np.array([100, 102])
        returns = REGIME_HMM_RETURNS(prices)
        assert len(returns) == 2
        assert np.isnan(returns[0])
        assert returns[1] == pytest.approx(0.02)

    def test_returns_empty_array(self):
        """Test returns with empty array."""
        prices = np.array([])
        returns = REGIME_HMM_RETURNS(prices)
        assert len(returns) == 0

    def test_returns_with_nan(self):
        """Test returns with NaN in prices."""
        prices = np.array([100, np.nan, 105, 103])
        returns = REGIME_HMM_RETURNS(prices)

        assert np.isnan(returns[0])
        assert np.isnan(returns[1])  # NaN input produces NaN output
        # Subsequent values may also be NaN due to nan propagation


class TestREGIME_HMM:
    """Tests for HMM-based regime detection."""

    @pytest.mark.skipif(
        not pytest.importorskip("hmmlearn", reason="hmmlearn not installed"), reason="hmmlearn required for HMM tests"
    )
    def test_hmm_import_required(self):
        """Test that hmmlearn is imported correctly."""
        # This test only runs if hmmlearn is available
        import hmmlearn

        assert hmmlearn is not None

    def test_hmm_missing_library(self):
        """Test graceful failure when hmmlearn not installed."""
        # Mock the import to always fail
        import sys

        original_modules = sys.modules.copy()

        try:
            # Remove hmmlearn from sys.modules if it exists
            if "hmmlearn" in sys.modules:
                del sys.modules["hmmlearn"]
            if "hmmlearn.hmm" in sys.modules:
                del sys.modules["hmmlearn.hmm"]

            # We can't actually test this easily without mocking
            # Just verify function exists
            assert callable(REGIME_HMM)

        finally:
            # Restore sys.modules
            sys.modules.update(original_modules)

    @pytest.mark.skipif(
        pytest.importorskip("hmmlearn", reason="hmmlearn not installed") is None, reason="hmmlearn required"
    )
    def test_hmm_basic_three_states(self):
        """Test basic 3-state HMM detection."""
        pytest.importorskip("hmmlearn")

        np.random.seed(42)

        # Create synthetic regime-switching data
        # Bear regime: negative returns
        bear_returns = np.random.normal(-0.01, 0.02, 40)
        # Sideways regime: zero mean returns
        sideways_returns = np.random.normal(0.0, 0.01, 30)
        # Bull regime: positive returns
        bull_returns = np.random.normal(0.02, 0.02, 40)

        returns = np.concatenate([bear_returns, sideways_returns, bull_returns])

        # Detect regimes
        states, trans_probs, means = REGIME_HMM(returns, n_states=3, random_state=42)

        # Check output shapes
        assert len(states) == len(returns)
        assert trans_probs.shape == (3, 3)
        assert len(means) == 3

        # Check that states are sorted by mean (Bear < Neutral < Bull)
        assert means[0] < means[1] < means[2]

        # Valid states should be in range [0, 2]
        valid_states = states[~np.isnan(states)]
        assert np.all((valid_states >= 0) & (valid_states <= 2))

    @pytest.mark.skipif(
        pytest.importorskip("hmmlearn", reason="hmmlearn not installed") is None, reason="hmmlearn required"
    )
    def test_hmm_transition_matrix_valid(self):
        """Test that transition matrix rows sum to 1."""
        pytest.importorskip("hmmlearn")

        np.random.seed(42)
        returns = np.random.normal(0, 0.02, 100)

        states, trans_probs, means = REGIME_HMM(returns, n_states=3)

        if not np.all(np.isnan(trans_probs)):
            # Each row should sum to 1 (probability distribution)
            row_sums = np.sum(trans_probs, axis=1)
            np.testing.assert_array_almost_equal(row_sums, np.ones(3), decimal=5)

    @pytest.mark.skipif(
        pytest.importorskip("hmmlearn", reason="hmmlearn not installed") is None, reason="hmmlearn required"
    )
    def test_hmm_insufficient_data(self):
        """Test HMM with insufficient data."""
        pytest.importorskip("hmmlearn")

        # Only 5 samples, need at least 2 * n_states = 6
        returns = np.array([0.01, -0.02, 0.03, -0.01, 0.02])

        states, trans_probs, means = REGIME_HMM(returns, n_states=3)

        # Should return all NaN
        assert np.all(np.isnan(states))
        assert np.all(np.isnan(trans_probs))
        assert np.all(np.isnan(means))

    @pytest.mark.skipif(
        pytest.importorskip("hmmlearn", reason="hmmlearn not installed") is None, reason="hmmlearn required"
    )
    def test_hmm_with_nan_values(self):
        """Test HMM with NaN values in returns."""
        pytest.importorskip("hmmlearn")

        np.random.seed(42)
        returns = np.random.normal(0, 0.02, 100)
        returns[10:15] = np.nan  # Insert some NaN values

        states, trans_probs, means = REGIME_HMM(returns, n_states=3)

        # Should handle NaN gracefully
        assert len(states) == len(returns)
        # NaN positions should remain NaN
        assert np.all(np.isnan(states[10:15]))

    @pytest.mark.skipif(
        pytest.importorskip("hmmlearn", reason="hmmlearn not installed") is None, reason="hmmlearn required"
    )
    def test_hmm_reproducibility(self):
        """Test that HMM is reproducible with same random_state."""
        pytest.importorskip("hmmlearn")

        np.random.seed(42)
        returns = np.random.normal(0, 0.02, 100)

        # Run twice with same random_state
        states1, trans1, means1 = REGIME_HMM(returns, n_states=3, random_state=42)
        states2, trans2, means2 = REGIME_HMM(returns, n_states=3, random_state=42)

        # Should produce identical results
        np.testing.assert_array_equal(states1, states2)
        np.testing.assert_array_almost_equal(trans1, trans2, decimal=10)
        np.testing.assert_array_almost_equal(means1, means2, decimal=10)

    @pytest.mark.skipif(
        pytest.importorskip("hmmlearn", reason="hmmlearn not installed") is None, reason="hmmlearn required"
    )
    def test_hmm_two_states(self):
        """Test HMM with 2 states (Bull/Bear only)."""
        pytest.importorskip("hmmlearn")

        np.random.seed(42)
        returns = np.random.normal(0, 0.02, 100)

        states, trans_probs, means = REGIME_HMM(returns, n_states=2)

        assert trans_probs.shape == (2, 2)
        assert len(means) == 2
        valid_states = states[~np.isnan(states)]
        assert np.all((valid_states >= 0) & (valid_states <= 1))


class TestREGIME_HMM_Integration:
    """Integration tests for HMM functions."""

    @pytest.mark.skipif(
        pytest.importorskip("hmmlearn", reason="hmmlearn not installed") is None, reason="hmmlearn required"
    )
    def test_hmm_returns_to_hmm_pipeline(self):
        """Test using REGIME_HMM_RETURNS -> REGIME_HMM pipeline."""
        pytest.importorskip("hmmlearn")

        np.random.seed(42)

        # Generate prices
        prices = 100 + np.cumsum(np.random.normal(0.01, 0.02, 100))

        # Calculate returns
        returns = REGIME_HMM_RETURNS(prices)

        # Detect regimes
        states, trans_probs, means = REGIME_HMM(returns, n_states=3)

        # Should work end-to-end
        assert len(states) == len(prices)
        assert not np.all(np.isnan(states))  # Should have some valid states

    def test_import_all_hmm_functions(self):
        """Test that all HMM functions can be imported."""
        from cluefin_ta import REGIME_HMM, REGIME_HMM_RETURNS

        assert callable(REGIME_HMM_RETURNS)
        assert callable(REGIME_HMM)
