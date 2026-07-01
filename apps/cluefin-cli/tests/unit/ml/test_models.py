from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from cluefin_cli.ml.models import StockPredictor


def _dataset(n: int = 160, *, seed: int = 0):
    rng = np.random.default_rng(seed)
    X = pd.DataFrame(rng.normal(size=(n, 6)), columns=[f"f{i}" for i in range(6)])
    # Signal that LightGBM can latch onto, so both classes are predicted.
    y = pd.Series((X["f0"] + rng.normal(scale=0.3, size=n) > 0).astype(int))
    # Guarantee both classes regardless of noise.
    y.iloc[::2] = 1
    y.iloc[1::2] = 0
    return X, y


def test_default_params_are_binary() -> None:
    predictor = StockPredictor()
    assert predictor.model_params["objective"] == "binary"
    assert predictor.is_trained is False


def test_custom_params_override_defaults() -> None:
    predictor = StockPredictor({"objective": "binary", "n_estimators": 10})
    assert predictor.model_params["n_estimators"] == 10


def test_train_returns_metrics_and_sets_state() -> None:
    X, y = _dataset()
    predictor = StockPredictor({"n_estimators": 20, "verbose": -1, "random_state": 42})
    metrics = predictor.train(X, y, validation_split=0.2)
    assert predictor.is_trained is True
    assert {"train_accuracy", "val_accuracy", "val_precision", "val_auc"}.issubset(metrics)


def test_train_raises_when_training_single_class() -> None:
    X, _ = _dataset(100)
    y = pd.Series([0] * 80 + [1] * 20)  # train slice (first 80) is single-class
    with pytest.raises(ValueError, match="at least 2 classes"):
        StockPredictor({"n_estimators": 10}).train(X, y, validation_split=0.2)


def test_train_handles_single_class_validation() -> None:
    X, _ = _dataset(100)
    y = pd.Series(([0, 1] * 40) + [0] * 20)  # train both classes, val all one class
    metrics = StockPredictor({"n_estimators": 10}).train(X, y, validation_split=0.2)
    assert metrics["val_auc"] == 0.0  # AUC skipped for single-class validation


def test_predict_requires_training() -> None:
    with pytest.raises(ValueError, match="must be trained"):
        StockPredictor().predict(pd.DataFrame({"f0": [1.0]}))


def test_predict_after_training_returns_arrays() -> None:
    X, y = _dataset()
    predictor = StockPredictor({"n_estimators": 20})
    predictor.train(X, y)
    preds, probs = predictor.predict(X.head(5))
    assert len(preds) == 5
    assert probs.shape[0] == 5


def test_cross_validate_returns_aggregate_metrics() -> None:
    X, y = _dataset(160)
    metrics = StockPredictor({"n_estimators": 10}).cross_validate(X, y, cv_folds=3)
    assert {"cv_accuracy_mean", "cv_f1_std"}.issubset(metrics)


def test_get_feature_importance_requires_training() -> None:
    with pytest.raises(ValueError, match="must be trained"):
        StockPredictor().get_feature_importance()


def test_get_feature_importance_after_training() -> None:
    X, y = _dataset()
    predictor = StockPredictor({"n_estimators": 20})
    predictor.train(X, y)
    importance = predictor.get_feature_importance(top_n=3)
    assert len(importance) == 3


def test_evaluate_model_requires_training() -> None:
    X, _ = _dataset(20)
    with pytest.raises(ValueError, match="must be trained"):
        StockPredictor().evaluate_model(X, pd.Series([0] * 20))


def test_evaluate_model_after_training() -> None:
    X, y = _dataset()
    predictor = StockPredictor({"n_estimators": 20})
    predictor.train(X, y)
    metrics = predictor.evaluate_model(X, y)
    assert {"test_accuracy", "test_auc"}.issubset(metrics)


def test_save_requires_training(tmp_path) -> None:
    with pytest.raises(ValueError, match="must be trained"):
        StockPredictor().save_model(str(tmp_path / "m.txt"))


def test_save_model_writes_file(tmp_path) -> None:
    X, y = _dataset()
    predictor = StockPredictor({"n_estimators": 20})
    predictor.train(X, y)
    path = tmp_path / "model.txt"
    predictor.save_model(str(path))
    assert path.exists() and path.stat().st_size > 0


def test_save_and_load_round_trip_preserves_predictions(tmp_path) -> None:
    X, y = _dataset()
    predictor = StockPredictor({"n_estimators": 20})
    predictor.train(X, y)
    path = str(tmp_path / "model.joblib")
    predictor.save_model(path)

    loaded = StockPredictor()
    loaded.load_model(path)
    assert loaded.is_trained is True

    # Reloaded model reproduces the original predictions and exposes importances.
    original_preds, _ = predictor.predict(X.head(10))
    reloaded_preds, reloaded_probs = loaded.predict(X.head(10))
    np.testing.assert_array_equal(original_preds, reloaded_preds)
    assert reloaded_probs.shape == (10, 2)
    assert loaded.get_feature_importance(top_n=3).shape[0] == 3


def test_load_model_raises_on_missing_file(tmp_path) -> None:
    with pytest.raises(FileNotFoundError):
        StockPredictor().load_model(str(tmp_path / "does-not-exist.joblib"))
