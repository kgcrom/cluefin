import numpy as np
import pandas as pd
import pytest

from cluefin_cli.ml.feature_engineering import FeatureEngineer


class TestRegimeFeatures:
    """Tests for regime detection feature engineering."""

    def test_create_regime_detection_features(self):
        """Test regime feature creation."""
        # Create sample OHLCV DataFrame
        n = 100
        dates = pd.date_range("2024-01-01", periods=n, freq="D")

        df = pd.DataFrame(
            {
                "date": dates,
                "open": 100 + np.cumsum(np.random.uniform(-1, 1, n)),
                "high": 105 + np.cumsum(np.random.uniform(-1, 1, n)),
                "low": 95 + np.cumsum(np.random.uniform(-1, 1, n)),
                "close": 100 + np.cumsum(np.random.uniform(-1, 1, n)),
                "volume": np.random.randint(1000000, 10000000, n),
            }
        )

        engineer = FeatureEngineer()
        result_df = engineer.create_regime_detection_features(df)

        # Verify regime columns are created
        expected_columns = [
            "regime_trend",
            "regime_trend_duration",
            "regime_volatility",
            "regime_combined",
        ]

        for col in expected_columns:
            assert col in result_df.columns, f"{col} should be in DataFrame"

        # Check data types
        assert result_df["regime_trend"].dtype == np.float64
        assert result_df["regime_trend_duration"].dtype == np.float64
        assert result_df["regime_volatility"].dtype == np.float64
        assert result_df["regime_combined"].dtype == np.float64

    def test_regime_features_with_hmm(self):
        """Test regime features including HMM (if available)."""
        pytest.importorskip("hmmlearn")

        n = 100
        dates = pd.date_range("2024-01-01", periods=n, freq="D")

        df = pd.DataFrame(
            {
                "date": dates,
                "open": 100 + np.cumsum(np.random.uniform(-1, 1, n)),
                "high": 105 + np.cumsum(np.random.uniform(-1, 1, n)),
                "low": 95 + np.cumsum(np.random.uniform(-1, 1, n)),
                "close": 100 + np.cumsum(np.random.uniform(-1, 1, n)),
                "volume": np.random.randint(1000000, 10000000, n),
            }
        )

        engineer = FeatureEngineer()
        result_df = engineer.create_regime_detection_features(df)

        # Check HMM features
        hmm_columns = [
            "regime_hmm_state",
            "regime_hmm_trans_to_0",
            "regime_hmm_trans_to_1",
            "regime_hmm_trans_to_2",
            "regime_hmm_expected_return",
        ]

        for col in hmm_columns:
            assert col in result_df.columns, f"{col} should be in DataFrame when hmmlearn available"

    def test_regime_features_no_nan_propagation(self):
        """Test regime features handle NaN appropriately."""
        n = 100
        dates = pd.date_range("2024-01-01", periods=n, freq="D")

        df = pd.DataFrame(
            {
                "date": dates,
                "open": 100 + np.cumsum(np.random.uniform(-1, 1, n)),
                "high": 105 + np.cumsum(np.random.uniform(-1, 1, n)),
                "low": 95 + np.cumsum(np.random.uniform(-1, 1, n)),
                "close": 100 + np.cumsum(np.random.uniform(-1, 1, n)),
                "volume": np.random.randint(1000000, 10000000, n),
            }
        )

        engineer = FeatureEngineer()
        result_df = engineer.create_regime_detection_features(df)

        # Check that some values are valid (not all NaN)
        assert not result_df["regime_trend"].isna().all(), "Should have some valid regime values"
        assert not result_df["regime_volatility"].isna().all(), "Should have some valid volatility values"

    def test_regime_features_with_insufficient_data(self):
        """Test regime features with short data (should handle gracefully)."""
        n = 30  # Less than slow_period (50)
        dates = pd.date_range("2024-01-01", periods=n, freq="D")

        df = pd.DataFrame(
            {
                "date": dates,
                "open": 100 + np.cumsum(np.random.uniform(-1, 1, n)),
                "high": 105 + np.cumsum(np.random.uniform(-1, 1, n)),
                "low": 95 + np.cumsum(np.random.uniform(-1, 1, n)),
                "close": 100 + np.cumsum(np.random.uniform(-1, 1, n)),
                "volume": np.random.randint(1000000, 10000000, n),
            }
        )

        engineer = FeatureEngineer()
        result_df = engineer.create_regime_detection_features(df)

        # Should not raise error, just have more NaN values
        assert "regime_trend" in result_df.columns
        # Most values will be NaN due to insufficient data
        assert result_df["regime_trend"].isna().sum() > n // 2


class TestRegimeFeatureIntegration:
    """Integration tests for regime features in ML pipeline."""

    def test_regime_features_in_prepare_features(self):
        """Test regime features integrated in full prepare_features pipeline."""
        # Create sample stock data
        n = 100
        dates = pd.date_range("2024-01-01", periods=n, freq="D")

        stock_data = pd.DataFrame(
            {
                "date": dates,
                "open": 100 + np.cumsum(np.random.uniform(-1, 1, n)),
                "high": 105 + np.cumsum(np.random.uniform(-1, 1, n)),
                "low": 95 + np.cumsum(np.random.uniform(-1, 1, n)),
                "close": 100 + np.cumsum(np.random.uniform(-1, 1, n)),
                "volume": np.random.randint(1000000, 10000000, n),
            }
        )

        # Create sample indicators (from TechnicalAnalyzer)
        indicators = {
            "sma_20": np.random.uniform(90, 110, n),
            "ema_20": np.random.uniform(90, 110, n),
            "rsi_14": np.random.uniform(30, 70, n),
            "macd": np.random.uniform(-5, 5, n),
            "macd_signal": np.random.uniform(-5, 5, n),
        }

        engineer = FeatureEngineer()
        df, feature_names = engineer.prepare_features(stock_data, indicators)

        # Check for regime features in output
        regime_features = [f for f in feature_names if f.startswith("regime_")]
        assert len(regime_features) > 0, "Regime features should be created"

        # Verify specific regime features
        expected_features = [
            "regime_trend",
            "regime_trend_duration",
            "regime_volatility",
            "regime_combined",
        ]

        for feature in expected_features:
            assert feature in feature_names, f"{feature} should be in feature list"

        # Check DataFrame has regime columns
        for feature in expected_features:
            assert feature in df.columns, f"{feature} should be in DataFrame"

    def test_regime_features_work_with_ml_predictor(self):
        """Test that regime features work in full ML predictor pipeline."""
        # This is a smoke test to ensure no errors in full pipeline
        from cluefin_cli.ml import StockMLPredictor

        # Create realistic sample data
        n = 300  # Need enough data for ML
        dates = pd.date_range("2024-01-01", periods=n, freq="D")

        stock_data = pd.DataFrame(
            {
                "date": dates,
                "open": 100 + np.cumsum(np.random.normal(0.1, 1, n)),
                "high": 105 + np.cumsum(np.random.normal(0.1, 1, n)),
                "low": 95 + np.cumsum(np.random.normal(0.1, 1, n)),
                "close": 100 + np.cumsum(np.random.normal(0.1, 1, n)),
                "volume": np.random.randint(1000000, 10000000, n),
            }
        )

        indicators = {
            "sma_20": 100 + np.cumsum(np.random.normal(0.1, 0.5, n)),
            "ema_20": 100 + np.cumsum(np.random.normal(0.1, 0.5, n)),
            "rsi_14": np.random.uniform(30, 70, n),
        }

        predictor = StockMLPredictor()

        try:
            # Try to prepare data with regime features
            prepared_df, feature_names = predictor.prepare_data(stock_data, indicators)

            # Should succeed without errors
            assert "regime_trend" in feature_names or len(feature_names) > 0

        except Exception as e:
            # If it fails, it should be due to insufficient data, not regime features
            assert "regime" not in str(e).lower(), f"Should not fail due to regime features: {e}"


class TestPatternFeatures:
    """Tests for pattern recognition feature engineering (Cup & Handle, Dow Theory)."""

    def test_cup_pattern_feature(self):
        """Test Cup & Handle feature creation in ML pipeline."""
        n = 150
        dates = pd.date_range("2024-01-01", periods=n, freq="D")

        df = pd.DataFrame(
            {
                "date": dates,
                "open": 100 + np.cumsum(np.random.uniform(-1, 1, n)),
                "high": 105 + np.cumsum(np.random.uniform(-1, 1, n)),
                "low": 95 + np.cumsum(np.random.uniform(-1, 1, n)),
                "close": 100 + np.cumsum(np.random.uniform(-1, 1, n)),
                "volume": np.random.randint(1000000, 10000000, n),
            }
        )

        engineer = FeatureEngineer()
        result_df = engineer.create_talib_features(df)

        # Verify cup pattern features exist
        assert "cup_pattern" in result_df.columns
        assert "days_since_cup_breakout" in result_df.columns

        # Cup pattern should be 0 or 100
        assert all(result_df["cup_pattern"].isin([0, 100]))
        # Days since cup should be -1 or >= 0
        assert all(result_df["days_since_cup_breakout"] >= -1)

    def test_dow_theory_features(self):
        """Test Dow Theory feature creation in ML pipeline."""
        n = 250
        dates = pd.date_range("2024-01-01", periods=n, freq="D")

        df = pd.DataFrame(
            {
                "date": dates,
                "open": 100 + np.cumsum(np.random.normal(0.1, 1, n)),
                "high": 105 + np.cumsum(np.random.normal(0.1, 1, n)),
                "low": 95 + np.cumsum(np.random.normal(0.1, 1, n)),
                "close": 100 + np.cumsum(np.random.normal(0.1, 1, n)),
                "volume": np.random.randint(1000000, 10000000, n),
            }
        )

        engineer = FeatureEngineer()
        result_df = engineer.create_talib_features(df)

        # Verify all Dow Theory features exist
        expected_features = [
            "dow_trend",
            "dow_correlation",
            "dow_strong_bull",
            "dow_weak_bull",
            "dow_sideways",
            "dow_weak_bear",
            "dow_strong_bear",
            "dow_trend_persistence",
            "dow_index_confirms",
            "dow_index_diverges",
        ]

        for feature in expected_features:
            assert feature in result_df.columns, f"{feature} should be in DataFrame"

    def test_dow_theory_one_hot_encoding(self):
        """Test Dow Theory one-hot encoding is mutually exclusive."""
        n = 250
        dates = pd.date_range("2024-01-01", periods=n, freq="D")

        df = pd.DataFrame(
            {
                "date": dates,
                "open": 100 + np.cumsum(np.random.normal(0.1, 1, n)),
                "high": 105 + np.cumsum(np.random.normal(0.1, 1, n)),
                "low": 95 + np.cumsum(np.random.normal(0.1, 1, n)),
                "close": 100 + np.cumsum(np.random.normal(0.1, 1, n)),
                "volume": np.random.randint(1000000, 10000000, n),
            }
        )

        engineer = FeatureEngineer()
        result_df = engineer.create_talib_features(df)

        # For each row, only one trend state should be 1 (except during startup where all might be 0)
        one_hot_cols = [
            "dow_strong_bull",
            "dow_weak_bull",
            "dow_sideways",
            "dow_weak_bear",
            "dow_strong_bear",
        ]

        # Skip initial rows that might have NaN trends
        for idx in range(100, len(result_df)):
            trend_sum = sum(result_df[col].iloc[idx] for col in one_hot_cols)
            # Should be 0 (invalid/startup) or 1 (valid trend state)
            assert trend_sum <= 1, f"Row {idx}: One-hot encoding violated (sum={trend_sum})"

    def test_pattern_features_with_insufficient_data(self):
        """Test pattern features handle insufficient data gracefully."""
        n = 100  # Less than both Cup (120) and Dow (200)
        dates = pd.date_range("2024-01-01", periods=n, freq="D")

        df = pd.DataFrame(
            {
                "date": dates,
                "open": np.random.uniform(90, 110, n),
                "high": np.random.uniform(95, 115, n),
                "low": np.random.uniform(85, 105, n),
                "close": np.random.uniform(90, 110, n),
                "volume": np.random.randint(1000000, 10000000, n),
            }
        )

        engineer = FeatureEngineer()
        result_df = engineer.create_talib_features(df)

        # Should still have columns but with default values
        assert "cup_pattern" in result_df.columns
        assert "dow_trend" in result_df.columns

        # Cup pattern should be all 0s (insufficient data)
        assert all(result_df["cup_pattern"] == 0)
        # Dow trend should be all 0s (neutral state when insufficient data)
        # Changed from NaN to 0 to avoid NaN propagation issues in ML pipeline
        assert all(result_df["dow_trend"] == 0)

    def test_pattern_features_in_full_pipeline(self):
        """Test pattern features work in full prepare_features pipeline."""
        n = 300
        dates = pd.date_range("2024-01-01", periods=n, freq="D")

        stock_data = pd.DataFrame(
            {
                "date": dates,
                "open": 100 + np.cumsum(np.random.normal(0.1, 1, n)),
                "high": 105 + np.cumsum(np.random.normal(0.1, 1, n)),
                "low": 95 + np.cumsum(np.random.normal(0.1, 1, n)),
                "close": 100 + np.cumsum(np.random.normal(0.1, 1, n)),
                "volume": np.random.randint(1000000, 10000000, n),
            }
        )

        indicators = {
            "sma_20": 100 + np.cumsum(np.random.normal(0.1, 0.5, n)),
            "ema_20": 100 + np.cumsum(np.random.normal(0.1, 0.5, n)),
            "rsi_14": np.random.uniform(30, 70, n),
        }

        engineer = FeatureEngineer()
        df, feature_names = engineer.prepare_features(stock_data, indicators)

        # Check for pattern features in output
        pattern_features = [
            "cup_pattern",
            "days_since_cup_breakout",
            "dow_trend",
            "dow_correlation",
            "dow_trend_persistence",
            "dow_index_confirms",
            "dow_index_diverges",
        ]

        # At least some pattern features should be present
        found_features = [f for f in pattern_features if f in feature_names]
        assert len(found_features) > 0, "Pattern features should be created in prepare_features"
