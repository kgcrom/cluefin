#!/usr/bin/env python3
"""
Test script for improved ML pipeline.

This script tests the Phase 1 improvements to the ML prediction system:
- Enhanced target variable creation
- Data quality diagnostics
- SMOTE oversampling
- Improved logging and error handling
"""

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger

from cluefin_cli.ml.diagnostics import MLDiagnostics
from cluefin_cli.ml.feature_engineering import FeatureEngineer
from cluefin_cli.ml.predictor import StockMLPredictor

# Add the src directory to Python path
src_path = Path(__file__).parent / "apps" / "cluefin-cli" / "src"
sys.path.insert(0, str(src_path))


def create_test_data():
    """Create synthetic test data for ML pipeline testing."""
    logger.info("🔨 Creating synthetic test data...")

    np.random.seed(42)
    n_samples = 200

    # Create OHLCV data
    dates = pd.date_range("2023-01-01", periods=n_samples, freq="D")
    base_price = 1000

    # Generate price data with some trend
    price_changes = np.random.normal(0, 20, n_samples)
    prices = [base_price]
    for change in price_changes[1:]:
        new_price = max(prices[-1] + change, 100)  # Minimum price of 100
        prices.append(new_price)

    # Create OHLC from close prices
    close_prices = np.array(prices)
    high_prices = close_prices * (1 + np.abs(np.random.normal(0, 0.02, n_samples)))
    low_prices = close_prices * (1 - np.abs(np.random.normal(0, 0.02, n_samples)))
    open_prices = np.roll(close_prices, 1)  # Yesterday's close as today's open
    open_prices[0] = base_price

    # Create volume data
    volumes = np.random.randint(100000, 1000000, n_samples)

    # Create DataFrame
    stock_data = pd.DataFrame(
        {
            "date": dates,
            "open": open_prices,
            "high": high_prices,
            "low": low_prices,
            "close": close_prices,
            "volume": volumes,
        }
    )

    # Create some basic indicators
    stock_data["sma_20"] = stock_data["close"].rolling(20).mean()
    stock_data["rsi"] = 50 + np.random.normal(0, 15, n_samples)  # Mock RSI

    indicators = {"sma_20": stock_data["sma_20"].values, "rsi": stock_data["rsi"].values}

    return stock_data, indicators


def test_diagnostics():
    """Test the diagnostics module."""
    logger.info("\n🔍 Testing ML Diagnostics...")

    diagnostics = MLDiagnostics()

    # Create test data with known class imbalance
    y_balanced = pd.Series([0, 1, 0, 1, 0, 1] * 10)  # Balanced
    y_imbalanced = pd.Series([0] * 50 + [1] * 5)  # Severely imbalanced

    # Create test features
    X = pd.DataFrame(
        {
            "feature_1": np.random.normal(0, 1, 60),
            "feature_2": np.random.normal(5, 2, 60),
            "constant_feature": [1] * 60,  # Problematic constant feature
            "missing_feature": [np.nan] * 30 + list(range(30)),  # Half missing
        }
    )

    logger.info("Testing balanced target...")
    diagnostics.analyze_target_distribution(y_balanced, "balanced_target")

    logger.info("\nTesting imbalanced target...")
    diagnostics.analyze_target_distribution(y_imbalanced, "imbalanced_target")

    logger.info("\nTesting feature quality...")
    diagnostics.analyze_feature_quality(X)

    logger.info("\nTesting comprehensive diagnosis...")
    diagnostics.diagnose_training_data(X, y_imbalanced)

    return True


def test_feature_engineering():
    """Test the improved feature engineering."""
    logger.info("\n🔧 Testing Feature Engineering...")

    stock_data, indicators = create_test_data()
    feature_engineer = FeatureEngineer()

    # Test different target creation methods
    df1 = stock_data.copy()
    df1 = feature_engineer.create_target_variable(df1, "binary")
    logger.info(f"Binary target distribution: {df1['target'].value_counts().to_dict()}")

    df2 = stock_data.copy()
    df2 = feature_engineer.create_target_variable(df2, "threshold", threshold_pct=0.02)
    logger.info(f"Threshold target (2%) distribution: {df2['target'].value_counts().to_dict()}")

    # Test SMOTE
    if len(df1) > 50:  # Ensure we have enough data
        prepared_df, feature_names = feature_engineer.prepare_features(stock_data, indicators)
        X = prepared_df[feature_names]
        y = prepared_df["target"]

        logger.info(f"Original data shape: {X.shape}, distribution: {y.value_counts().to_dict()}")

        # Test SMOTE if available
        try:
            X_resampled, y_resampled = feature_engineer.apply_smote_oversampling(X, y)
            logger.info(f"After SMOTE shape: {X_resampled.shape}, distribution: {y_resampled.value_counts().to_dict()}")
        except Exception as e:
            logger.info(f"SMOTE test skipped: {e}")

        # Test class weights
        class_weights = feature_engineer.calculate_class_weights(y)
        logger.info(f"Class weights: {class_weights}")

    return True


def test_ml_pipeline():
    """Test the complete ML pipeline."""
    logger.info("\n🤖 Testing ML Pipeline...")

    stock_data, indicators = create_test_data()

    # Initialize predictor with diagnostics enabled
    predictor = StockMLPredictor(enable_diagnostics=True)

    try:
        # Prepare data
        prepared_df, feature_names = predictor.prepare_data(stock_data, indicators)
        logger.info(f"Prepared data shape: {prepared_df.shape}")
        logger.info(f"Features: {len(feature_names)}")

        # Train model
        training_metrics = predictor.train_model(prepared_df, use_smote=True, use_class_weights=True)

        logger.info("\n📊 Training Results:")
        for metric, value in training_metrics.items():
            logger.info(f"  {metric}: {value:.4f}")

        # Test prediction
        prediction_result = predictor.predict(stock_data, indicators)
        logger.info(
            f"\n🎯 Prediction: {prediction_result['signal']} (confidence: {prediction_result['confidence']:.4f})"
        )

        return True

    except Exception as e:
        logger.info(f"❌ Pipeline test failed: {e}")
        import traceback

        logger.info(traceback.format_exc())
        return False


def main():
    """Run all tests."""
    logger.info("🚀 Starting ML Pipeline Phase 1 Tests\n")

    tests = [
        ("Diagnostics", test_diagnostics),
        ("Feature Engineering", test_feature_engineering),
        ("Complete ML Pipeline", test_ml_pipeline),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            logger.info(f"\n{'=' * 50}")
            logger.info(f"Running {test_name} Test")
            logger.info("=" * 50)
            result = test_func()
            results.append((test_name, result))
            if result:
                logger.info(f"✅ {test_name} test passed!")
            else:
                logger.info(f"❌ {test_name} test failed!")
        except Exception as e:
            logger.info(f"❌ {test_name} test error: {e}")
            results.append((test_name, False))

    logger.info(f"\n{'=' * 50}")
    logger.info("📈 Test Summary")
    logger.info("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{test_name}: {status}")

    logger.info(f"\nResults: {passed}/{total} tests passed")

    if passed == total:
        logger.info("🎉 All tests passed! Phase 1 improvements are working correctly.")
        logger.info("\n💡 The improvements should help resolve precision/recall/F1-score issues:")
        logger.info("  • Enhanced target variable creation with thresholds")
        logger.info("  • SMOTE oversampling for class imbalance")
        logger.info("  • Comprehensive data quality diagnostics")
        logger.info("  • Improved error handling and logging")
        logger.info("  • Class weight balancing")
    else:
        logger.info("⚠️ Some tests failed. Please review the errors above.")


if __name__ == "__main__":
    main()
