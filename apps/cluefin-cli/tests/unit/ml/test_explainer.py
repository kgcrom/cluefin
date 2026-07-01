from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from cluefin_cli.ml.explainer import SHAPExplainer
from cluefin_cli.ml.models import StockPredictor


@pytest.fixture(scope="module")
def trained_model_and_data():
    rng = np.random.default_rng(1)
    n = 120
    X = pd.DataFrame(rng.normal(size=(n, 5)), columns=[f"f{i}" for i in range(5)])
    y = pd.Series((X["f0"] + X["f1"] + rng.normal(scale=0.2, size=n) > 0).astype(int))
    y.iloc[::2] = 1
    y.iloc[1::2] = 0
    predictor = StockPredictor({"n_estimators": 25, "verbose": -1})
    predictor.train(X, y)
    return predictor.model, X


@pytest.fixture
def explainer(trained_model_and_data) -> SHAPExplainer:
    model, X = trained_model_and_data
    exp = SHAPExplainer(model, model_type="tree")
    exp.initialize_explainer(X.head(50))
    return exp


def test_calculate_shap_values_requires_initialization(trained_model_and_data) -> None:
    model, X = trained_model_and_data
    exp = SHAPExplainer(model, model_type="tree")
    with pytest.raises(ValueError, match="must be initialized"):
        exp.calculate_shap_values(X.head(5))


def test_initialize_explainer_rejects_unknown_type(trained_model_and_data) -> None:
    model, X = trained_model_and_data
    exp = SHAPExplainer(model, model_type="bogus")
    with pytest.raises(ValueError, match="Unknown model_type"):
        exp.initialize_explainer(X.head(10))


def test_calculate_shap_values_returns_2d(explainer, trained_model_and_data) -> None:
    _, X = trained_model_and_data
    values = explainer.calculate_shap_values(X.head(20))
    assert values.shape[0] == 20
    assert values.shape[1] == 5


def test_get_feature_importance(explainer, trained_model_and_data) -> None:
    _, X = trained_model_and_data
    importance = explainer.get_feature_importance(X.head(20), top_n=3)
    assert list(importance.columns) == ["feature", "importance", "mean_shap"]
    assert len(importance) == 3


def test_explain_prediction_returns_breakdown(explainer, trained_model_and_data) -> None:
    _, X = trained_model_and_data
    result = explainer.explain_prediction(X.head(10), sample_idx=0)
    assert {"base_value", "probability", "feature_contributions", "top_positive", "top_negative"} <= set(result)
    assert 0.0 <= result["probability"] <= 1.0


def test_display_feature_importance_renders(explainer, trained_model_and_data) -> None:
    _, X = trained_model_and_data
    explainer.display_feature_importance(X.head(20), top_n=5)  # should not raise


def test_display_prediction_explanation_renders(explainer, trained_model_and_data) -> None:
    _, X = trained_model_and_data
    explainer.display_prediction_explanation(X.head(10), sample_idx=0)  # should not raise


def test_get_summary_statistics(explainer, trained_model_and_data) -> None:
    _, X = trained_model_and_data
    stats = explainer.get_summary_statistics(X.head(20))
    assert stats["n_samples"] == 20
    assert stats["n_features"] == 5
    assert stats["most_important_feature"] in [f"f{i}" for i in range(5)]
