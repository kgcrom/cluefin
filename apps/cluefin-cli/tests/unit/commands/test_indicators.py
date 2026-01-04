"""Unit tests for technical analysis indicators including pattern recognition."""

import numpy as np
import pandas as pd
import pytest

from cluefin_cli.commands.analysis.indicators import TechnicalAnalyzer


class TestPatternRecognition:
    """Test suite for pattern recognition features (Cup & Handle, Dow Theory)."""

    def test_cup_pattern_with_sufficient_data(self):
        """Test Cup & Handle calculation with sufficient data (150 days)."""
        analyzer = TechnicalAnalyzer()

        # Create 150 days of synthetic OHLCV data
        np.random.seed(42)
        data = pd.DataFrame(
            {
                "date": pd.date_range("2024-01-01", periods=150),
                "open": np.random.uniform(90, 110, 150),
                "high": np.random.uniform(95, 115, 150),
                "low": np.random.uniform(85, 105, 150),
                "close": np.random.uniform(90, 110, 150),
                "volume": np.random.randint(1000000, 10000000, 150),
            }
        )

        indicators = analyzer.calculate_all(data)

        # Verify cup_pattern column exists and has valid values
        assert "cup_pattern" in indicators.columns
        assert "cup_has_volume" in indicators.columns
        assert indicators["cup_pattern"].dtype in [np.int32, np.int64, np.float64]
        # Cup pattern should return 0 or 100
        assert all(indicators["cup_pattern"].isin([0, 100]))

    def test_cup_pattern_insufficient_data(self):
        """Test Cup & Handle with insufficient data (< 120 days)."""
        analyzer = TechnicalAnalyzer()

        # Create only 100 days of data
        np.random.seed(42)
        data = pd.DataFrame(
            {
                "date": pd.date_range("2024-01-01", periods=100),
                "open": np.random.uniform(90, 110, 100),
                "high": np.random.uniform(95, 115, 100),
                "low": np.random.uniform(85, 105, 100),
                "close": np.random.uniform(90, 110, 100),
                "volume": np.random.randint(1000000, 10000000, 100),
            }
        )

        indicators = analyzer.calculate_all(data)

        # Should still calculate, but return all 0s (no pattern)
        assert "cup_pattern" in indicators.columns
        assert all(indicators["cup_pattern"] == 0)
        assert all(indicators["cup_has_volume"] == False)

    def test_dow_theory_with_sufficient_data(self):
        """Test Dow Theory calculation with sufficient data (250 days)."""
        analyzer = TechnicalAnalyzer()

        # Create 250 days of synthetic data with trend
        np.random.seed(42)
        days = 250
        base_price = 100
        close = np.cumsum(np.random.randn(days) * 0.5) + base_price  # Add drift for trend

        data = pd.DataFrame(
            {
                "date": pd.date_range("2024-01-01", periods=days),
                "open": close + np.random.uniform(-1, 1, days),
                "high": close + np.random.uniform(1, 3, days),
                "low": close + np.random.uniform(-3, -1, days),
                "close": close,
                "volume": np.random.randint(1000000, 10000000, days),
            }
        )

        indicators = analyzer.calculate_all(data)

        # Verify Dow Theory columns exist
        assert "dow_trend" in indicators.columns
        assert "dow_correlation" in indicators.columns
        assert "dow_has_volume" in indicators.columns

        # Trend should be in valid range or NaN (accounting for startup period)
        valid_trends = {-2, -1, 0, 1, 2}
        for val in indicators["dow_trend"]:
            if not pd.isna(val):
                assert int(val) in valid_trends

    def test_dow_theory_insufficient_data(self):
        """Test Dow Theory with insufficient data (< 200 days)."""
        analyzer = TechnicalAnalyzer()

        # Create only 150 days of data
        np.random.seed(42)
        data = pd.DataFrame(
            {
                "date": pd.date_range("2024-01-01", periods=150),
                "open": np.random.uniform(90, 110, 150),
                "high": np.random.uniform(95, 115, 150),
                "low": np.random.uniform(85, 105, 150),
                "close": np.random.uniform(90, 110, 150),
                "volume": np.random.randint(1000000, 10000000, 150),
            }
        )

        indicators = analyzer.calculate_all(data)

        # Should return NaN for insufficient data
        assert "dow_trend" in indicators.columns
        assert all(pd.isna(indicators["dow_trend"]))
        assert all(pd.isna(indicators["dow_correlation"]))

    def test_patterns_with_volume_in_data(self):
        """Test pattern volume confirmation tracking."""
        analyzer = TechnicalAnalyzer()

        # Create data with volume column
        np.random.seed(42)
        data = pd.DataFrame(
            {
                "date": pd.date_range("2024-01-01", periods=250),
                "open": np.random.uniform(90, 110, 250),
                "high": np.random.uniform(95, 115, 250),
                "low": np.random.uniform(85, 105, 250),
                "close": np.random.uniform(90, 110, 250),
                "volume": np.random.randint(1000000, 10000000, 250),
            }
        )

        # Should not raise exception
        indicators = analyzer.calculate_all(data)

        # Should have pattern columns with volume
        assert "cup_pattern" in indicators.columns
        assert "dow_trend" in indicators.columns
        # Volume flag should be True since volume column exists
        assert indicators["cup_has_volume"].iloc[0]
        assert indicators["dow_has_volume"].iloc[0]

    def test_empty_dataframe(self):
        """Test handling of empty DataFrame."""
        analyzer = TechnicalAnalyzer()

        data = pd.DataFrame()
        indicators = analyzer.calculate_all(data)

        # Should return empty DataFrame without error
        assert indicators.empty

    def test_pattern_values_are_numeric(self):
        """Test that pattern values are numeric and not NaN for sufficient data."""
        analyzer = TechnicalAnalyzer()

        np.random.seed(42)
        data = pd.DataFrame(
            {
                "date": pd.date_range("2024-01-01", periods=250),
                "open": np.random.uniform(90, 110, 250),
                "high": np.random.uniform(95, 115, 250),
                "low": np.random.uniform(85, 105, 250),
                "close": np.random.uniform(90, 110, 250),
                "volume": np.random.randint(1000000, 10000000, 250),
            }
        )

        indicators = analyzer.calculate_all(data)

        # Cup pattern should always be numeric (0 or 100)
        assert not indicators["cup_pattern"].isna().all()
        assert indicators["cup_pattern"].dtype != object

        # Dow trend might have NaNs during startup period but should have some valid values
        valid_trends = indicators["dow_trend"].dropna()
        if len(valid_trends) > 0:
            # If we have any valid trend values, they should be numeric
            assert all(isinstance(v, (int, np.integer)) or np.issubdtype(type(v), np.integer) for v in valid_trends)
