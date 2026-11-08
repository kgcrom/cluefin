"""ML pipeline: diagnostics, target creation and class-imbalance handling.

These used to end in ``assert True`` and wrap SMOTE in ``try/except``, so they passed while
SMOTE could not even be imported (imbalanced-learn 0.14.0 vs scikit-learn 1.8, 2026-11-08).
SMOTE is gone; imbalance is handled by LightGBM ``class_weight="balanced"`` on the training split.
"""

import numpy as np
import pandas as pd
import pytest

from cluefin_desk.ml.diagnostics import MLDiagnostics
from cluefin_desk.ml.feature_engineering import FeatureEngineer
from cluefin_desk.ml.predictor import StockMLPredictor


def create_test_data(n_samples: int = 200):
    rng = np.random.default_rng(42)
    close = np.maximum(1000 + np.cumsum(rng.normal(0, 20, n_samples)), 100)
    high = close * (1 + np.abs(rng.normal(0, 0.02, n_samples)))
    low = close * (1 - np.abs(rng.normal(0, 0.02, n_samples)))
    open_ = np.roll(close, 1)
    open_[0] = 1000
    stock_data = pd.DataFrame(
        {
            "date": pd.date_range("2023-01-01", periods=n_samples, freq="D"),
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
            "volume": rng.integers(100_000, 1_000_000, n_samples),
        }
    )
    stock_data["sma_20"] = stock_data["close"].rolling(20).mean()
    stock_data["rsi"] = 50 + rng.normal(0, 15, n_samples)
    indicators = {"sma_20": stock_data["sma_20"].values, "rsi": stock_data["rsi"].values}
    return stock_data, indicators


class TestDiagnostics:
    def test_target_balance_flags(self):
        diagnostics = MLDiagnostics()
        balanced = diagnostics.analyze_target_distribution(pd.Series([0, 1] * 30), "balanced")
        imbalanced = diagnostics.analyze_target_distribution(pd.Series([0] * 55 + [1] * 5), "imbalanced")
        assert not balanced["is_severely_imbalanced"]
        assert balanced["imbalance_ratio"] == pytest.approx(1.0)
        assert imbalanced["is_severely_imbalanced"]
        assert imbalanced["imbalance_ratio"] == pytest.approx(11.0)

    def test_feature_quality_flags_constant_and_missing(self):
        rng = np.random.default_rng(0)
        X = pd.DataFrame(
            {
                "good": rng.normal(0, 1, 60),
                "constant": [1] * 60,
                "half_missing": [np.nan] * 30 + list(range(30)),
            }
        )
        quality = MLDiagnostics().analyze_feature_quality(X)
        assert quality["feature_quality"]["constant"]["constant_feature"]
        assert quality["feature_quality"]["half_missing"]["missing_ratio"] == pytest.approx(0.5)
        assert "constant" in quality["problematic_features"]
        assert "good" not in quality["problematic_features"]

    def test_recommendations_no_longer_suggest_oversampling(self):
        rng = np.random.default_rng(0)
        X = pd.DataFrame({"f": rng.normal(0, 1, 60)})
        diagnosis = MLDiagnostics().diagnose_training_data(X, pd.Series([0] * 55 + [1] * 5))
        assert diagnosis["target_analysis"]["is_severely_imbalanced"]
        assert not any("SMOTE" in item for item in diagnosis["recommendations"])


class TestTargetVariable:
    def test_binary_target_is_next_day_direction(self):
        stock_data, _ = create_test_data()
        df = FeatureEngineer().create_target_variable(stock_data.copy(), "binary")
        expected = (stock_data["close"].shift(-1) > stock_data["close"]).astype(int)
        # The last row has no next day and is dropped.
        assert len(df) == len(stock_data) - 1
        pd.testing.assert_series_equal(df["target"], expected.loc[df.index], check_names=False)

    def test_threshold_target_needs_a_large_enough_move(self):
        stock_data, _ = create_test_data()
        df = FeatureEngineer().create_target_variable(stock_data.copy(), "threshold", threshold_pct=0.02)
        change = stock_data["close"].shift(-1) / stock_data["close"] - 1
        up = change.loc[df.index] > 0.02
        assert up.any()
        assert (df["target"][up] == 1).all()
        assert (df["target"][~up] == 0).all()


class TestPipeline:
    def test_train_uses_balanced_class_weight_and_reports_validation_metrics(self):
        stock_data, indicators = create_test_data()
        predictor = StockMLPredictor(enable_diagnostics=True)
        prepared_df, _ = predictor.prepare_data(stock_data, indicators)

        metrics = predictor.train_model(prepared_df)

        assert predictor.model.model_params["class_weight"] == "balanced"
        assert predictor.model.model.get_params()["class_weight"] == "balanced"
        assert {"val_accuracy", "val_precision", "val_recall", "val_f1", "val_auc"} <= set(metrics)
        for key in ("val_accuracy", "val_precision", "val_recall", "val_f1", "val_auc"):
            assert 0.0 <= metrics[key] <= 1.0

    def test_class_weights_can_be_turned_off(self):
        stock_data, indicators = create_test_data()
        predictor = StockMLPredictor(enable_diagnostics=False)
        prepared_df, _ = predictor.prepare_data(stock_data, indicators)
        predictor.train_model(prepared_df, use_class_weights=False)
        assert predictor.model.model.get_params()["class_weight"] is None

    def test_predict_returns_a_signal_with_probabilities(self):
        stock_data, indicators = create_test_data()
        predictor = StockMLPredictor(enable_diagnostics=False)
        prepared_df, _ = predictor.prepare_data(stock_data, indicators)
        predictor.train_model(prepared_df)

        result = predictor.predict(stock_data, indicators)

        assert result["signal"] in {"BUY", "SELL"}
        assert result["probability_up"] + result["probability_down"] == pytest.approx(1.0)
        assert result["confidence"] == pytest.approx(max(result["probability_up"], result["probability_down"]))
