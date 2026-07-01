from __future__ import annotations

import asyncio
from types import SimpleNamespace
from unittest.mock import MagicMock

import cluefin_ta
import numpy as np
import pandas as pd

from cluefin_cli.commands.technical_analysis import (
    _display_basic_feature_importance,
    _display_company_info,
    _display_ml_model_summary,
    _display_regime_analysis,
    _display_stock_info,
    _display_technical_indicators,
    _display_trading_trend,
    _perform_ml_analysis,
)


def _make_stock_data(n: int) -> pd.DataFrame:
    dates = pd.date_range("2024-01-01", periods=n, freq="D")
    close = [70000.0 + i * 10 for i in range(n)]
    return pd.DataFrame(
        {
            "open": [c - 10 for c in close],
            "high": [c + 50 for c in close],
            "low": [c - 50 for c in close],
            "close": close,
            "volume": [1000.0 + i for i in range(n)],
        },
        index=dates,
    )


def _make_ml_predictor(n_samples: int, feature_names=None) -> MagicMock:
    feature_names = feature_names or ["rsi", "macd", "sma_20"]
    predictor = MagicMock()
    predictor.prepare_data.return_value = (
        pd.DataFrame({"target": [0, 1] * (n_samples // 2) + [0] * (n_samples % 2)}),
        feature_names,
    )
    predictor.train_model.return_value = {
        "val_accuracy": 0.65,
        "val_precision": 0.6,
        "val_recall": 0.55,
        "val_f1": 0.57,
        "val_auc": 0.68,
    }
    predictor.predict.return_value = {"direction": "up", "confidence": 0.7}
    predictor.model.get_feature_importance.return_value = pd.Series({"rsi": 0.6, "macd": 0.4})
    return predictor


# ---------------------------------------------------------------------------
# _display_company_info
# ---------------------------------------------------------------------------


def test_display_company_info_empty() -> None:
    _display_company_info("005930", pd.DataFrame())


def test_display_company_info_full() -> None:
    data = pd.DataFrame(
        [
            {
                "stock_name": "삼성전자",
                "settlement_month": "12",
                "industry_name": "반도체",
                "registration_day": "19750611",
                "sector_name": "전기전자",
                "distribution_stock": "100000",
                "distribution_ratio": "10.5",
                "floating_stock": "900000",
                "company_size": "대형주",
                "market_cap": "4000000",
                "per": "15.2",
                "eps": "5000",
                "pbr": "1.5",
                "roe": "12.3",
                "bps": "45000",
                "revenue": "3000000",
                "operating_profit": "500000",
                "net_profit": "400000",
                "250_day_high": "80000",
                "250hgst_pric_pre_rt": "-5.2",
                "250_day_low": "60000",
                "250lwst_pric_pre_rt": "10.1",
                "foreign_exhaustion_rate": "45.0",
                "order_warning": "3",
            }
        ]
    )
    _display_company_info("005930", data)


# ---------------------------------------------------------------------------
# _display_stock_info
# ---------------------------------------------------------------------------


def test_display_stock_info_empty() -> None:
    _display_stock_info("005930", pd.DataFrame())


def test_display_stock_info_single_row() -> None:
    data = pd.DataFrame({"close": [70000.0], "volume": [1000.0]})
    _display_stock_info("005930", data)


def test_display_stock_info_multi_row_negative_change() -> None:
    data = pd.DataFrame({"close": [71000.0, 70000.0], "volume": [1000.0, 1200.0]})
    _display_stock_info("005930", data)


# ---------------------------------------------------------------------------
# _display_trading_trend
# ---------------------------------------------------------------------------


def test_display_trading_trend_empty() -> None:
    _display_trading_trend(None)
    _display_trading_trend({})


def test_display_trading_trend_with_data() -> None:
    _display_trading_trend({"개인": "-1000", "외국인": "1500", "기관": "N/A"})


# ---------------------------------------------------------------------------
# _display_technical_indicators
# ---------------------------------------------------------------------------


def test_display_technical_indicators_full() -> None:
    indicators = pd.DataFrame(
        {
            "close": [70000.0],
            "rsi": [75.0],
            "macd": [1.5],
            "macd_signal": [1.0],
            "sma_20": [69000.0],
            "sma_50": [68000.0],
            "sma_120": [67000.0],
            "sma_240": [66000.0],
        }
    )
    _display_technical_indicators(indicators)


# ---------------------------------------------------------------------------
# _display_basic_feature_importance
# ---------------------------------------------------------------------------


def test_display_basic_feature_importance_success() -> None:
    importance = pd.Series({"rsi": 0.5, "macd": 0.3, "sma_20": 0.2})
    predictor = SimpleNamespace(model=SimpleNamespace(get_feature_importance=lambda top_n=15: importance))
    _display_basic_feature_importance(predictor, ["rsi", "macd", "sma_20"])


def test_display_basic_feature_importance_error() -> None:
    def _boom(top_n=15):
        raise RuntimeError("model not fitted")

    predictor = SimpleNamespace(model=SimpleNamespace(get_feature_importance=_boom))
    _display_basic_feature_importance(predictor, ["rsi"])


# ---------------------------------------------------------------------------
# _display_ml_model_summary
# ---------------------------------------------------------------------------


def test_display_ml_model_summary_good_and_excellent() -> None:
    metrics = {
        "val_accuracy": 0.72,
        "val_precision": 0.65,
        "val_recall": 0.60,
        "val_f1": 0.62,
        "val_auc": 0.75,
    }
    _display_ml_model_summary(metrics, n_features=42)


def test_display_ml_model_summary_fair_and_good() -> None:
    metrics = {
        "val_accuracy": 0.58,
        "val_precision": 0.55,
        "val_recall": 0.50,
        "val_f1": 0.52,
        "val_auc": 0.65,
    }
    _display_ml_model_summary(metrics, n_features=20)


def test_display_ml_model_summary_poor_and_fair() -> None:
    metrics = {
        "val_accuracy": 0.50,
        "val_precision": 0.40,
        "val_recall": 0.35,
        "val_f1": 0.37,
        "val_auc": 0.50,
    }
    _display_ml_model_summary(metrics, n_features=10)


def test_display_ml_model_summary_error() -> None:
    _display_ml_model_summary(None, n_features=0)


# ---------------------------------------------------------------------------
# _perform_ml_analysis
# ---------------------------------------------------------------------------


def test_perform_ml_analysis_basic_flow() -> None:
    predictor = _make_ml_predictor(n_samples=80)
    stock_data = _make_stock_data(80)
    asyncio.run(
        _perform_ml_analysis(
            predictor, "005930", stock_data, {}, show_feature_importance=False, show_shap_analysis=False
        )
    )
    predictor.train_model.assert_called_once()
    predictor.display_prediction_results.assert_called_once()
    predictor.model.get_feature_importance.assert_not_called()
    predictor.display_feature_importance.assert_not_called()


def test_perform_ml_analysis_with_feature_importance_and_shap() -> None:
    predictor = _make_ml_predictor(n_samples=80)
    stock_data = _make_stock_data(80)
    asyncio.run(
        _perform_ml_analysis(predictor, "005930", stock_data, {}, show_feature_importance=True, show_shap_analysis=True)
    )
    predictor.model.get_feature_importance.assert_called_once()
    predictor.display_feature_importance.assert_called_once()


def test_perform_ml_analysis_limited_samples_warning() -> None:
    predictor = _make_ml_predictor(n_samples=30)
    predictor.prepare_data.return_value = (pd.DataFrame({"target": [0, 1] * 15}), ["rsi"])
    stock_data = _make_stock_data(30)
    asyncio.run(
        _perform_ml_analysis(
            predictor, "005930", stock_data, {}, show_feature_importance=False, show_shap_analysis=False
        )
    )
    predictor.train_model.assert_called_once()


def test_perform_ml_analysis_handles_errors() -> None:
    predictor = MagicMock()
    predictor.prepare_data.side_effect = RuntimeError("feature engineering failed")
    stock_data = _make_stock_data(60)
    asyncio.run(
        _perform_ml_analysis(
            predictor, "005930", stock_data, {}, show_feature_importance=False, show_shap_analysis=False
        )
    )
    predictor.train_model.assert_not_called()


# ---------------------------------------------------------------------------
# _display_regime_analysis
# ---------------------------------------------------------------------------


def _fake_regime_hmm_success(returns, n_states=3, random_state=42):
    hmm_states = np.array([2.0] * len(returns))
    transition_probs = np.array(
        [
            [0.7, 0.2, 0.1],
            [0.2, 0.6, 0.2],
            [0.1, 0.2, 0.7],
        ]
    )
    state_means = np.array([-0.01, 0.0, 0.02])
    return hmm_states, transition_probs, state_means


def test_display_regime_analysis_full_with_hmm_success(monkeypatch) -> None:
    stock_data = _make_stock_data(300)
    monkeypatch.setattr(cluefin_ta, "REGIME_HMM", _fake_regime_hmm_success)
    _display_regime_analysis(stock_data, {})


def test_display_regime_analysis_hmm_import_error(monkeypatch) -> None:
    stock_data = _make_stock_data(300)

    def _boom(*args, **kwargs):
        raise ImportError("hmmlearn not installed")

    monkeypatch.setattr(cluefin_ta, "REGIME_HMM", _boom)
    _display_regime_analysis(stock_data, {})


def test_display_regime_analysis_hmm_generic_error(monkeypatch) -> None:
    stock_data = _make_stock_data(300)

    def _boom(*args, **kwargs):
        raise RuntimeError("HMM fit failed")

    monkeypatch.setattr(cluefin_ta, "REGIME_HMM", _boom)
    _display_regime_analysis(stock_data, {})


def test_display_regime_analysis_outer_exception_on_missing_column() -> None:
    stock_data = pd.DataFrame({"low": [1.0, 2.0], "close": [1.5, 2.5]})
    _display_regime_analysis(stock_data, {})
