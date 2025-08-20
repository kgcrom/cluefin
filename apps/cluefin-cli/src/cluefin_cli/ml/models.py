"""
ML models module for stock prediction.

This module contains ML model implementations using LightGBM and scikit-learn
for stock price prediction and classification.
"""

from typing import Any, Dict, List, Optional, Tuple

import lightgbm as lgb
import numpy as np
import pandas as pd
from loguru import logger
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import TimeSeriesSplit, cross_val_score


class StockPredictor:
    """
    Stock prediction model using LightGBM with time series considerations.

    This class handles model training, prediction, and evaluation for stock
    price movement prediction using LightGBM classifier.
    """

    def __init__(self, model_params: Optional[Dict] = None):
        """
        Initialize StockPredictor with model parameters.

        Args:
            model_params: Optional dictionary of LightGBM parameters
        """
        self.model_params = model_params or self._get_default_params()
        self.model: Optional[lgb.LGBMClassifier] = None
        self.feature_importance: Optional[pd.Series] = None
        self.is_trained = False

    def _get_default_params(self) -> Dict[str, Any]:
        """
        Get default LightGBM parameters optimized for stock prediction.

        Returns:
            Dictionary of default parameters
        """
        return {
            "objective": "binary",
            "metric": "binary_logloss",
            "boosting_type": "gbdt",
            "num_leaves": 31,
            "learning_rate": 0.05,
            "feature_fraction": 0.9,
            "bagging_fraction": 0.8,
            "bagging_freq": 5,
            "verbose": -1,
            "random_state": 42,
            "n_estimators": 100,
        }

    def train(self, X: pd.DataFrame, y: pd.Series, validation_split: float = 0.2) -> Dict[str, float]:
        """
        Train the LightGBM model with time series split.

        Args:
            X: Feature dataframe
            y: Target series
            validation_split: Fraction of data to use for validation

        Returns:
            Dictionary of training metrics
        """
        try:
            # Time series split to maintain temporal order
            split_idx = int(len(X) * (1 - validation_split))
            X_train, X_val = X.iloc[:split_idx], X.iloc[split_idx:]
            y_train, y_val = y.iloc[:split_idx], y.iloc[split_idx:]

            logger.info(f"Training with {len(X_train)} samples, validating with {len(X_val)} samples")

            # Initialize and train model
            self.model = lgb.LGBMClassifier(**self.model_params)

            # Train with early stopping
            self.model.fit(
                X_train,
                y_train,
                eval_set=[(X_val, y_val)],
                callbacks=[lgb.early_stopping(stopping_rounds=10), lgb.log_evaluation(0)],
            )

            # Get feature importance
            self.feature_importance = pd.Series(self.model.feature_importances_, index=X.columns).sort_values(
                ascending=False
            )

            # Calculate training metrics
            train_pred = self.model.predict(X_train)
            val_pred = self.model.predict(X_val)
            val_pred_proba = self.model.predict_proba(X_val)[:, 1]

            metrics = {
                "train_accuracy": accuracy_score(y_train, train_pred),
                "val_accuracy": accuracy_score(y_val, val_pred),
                "val_precision": precision_score(y_val, val_pred),
                "val_recall": recall_score(y_val, val_pred),
                "val_f1": f1_score(y_val, val_pred),
                "val_auc": roc_auc_score(y_val, val_pred_proba),
            }

            self.is_trained = True
            logger.info(f"Model training completed. Validation accuracy: {metrics['val_accuracy']:.4f}")

            return metrics

        except Exception as e:
            logger.error(f"Error training model: {e}")
            raise

    def predict(self, X: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Make predictions using the trained model.

        Args:
            X: Feature dataframe

        Returns:
            Tuple of (predictions, probabilities)
        """
        if not self.is_trained or self.model is None:
            raise ValueError("Model must be trained before making predictions")

        try:
            predictions = self.model.predict(X)
            probabilities = self.model.predict_proba(X)

            return predictions, probabilities

        except Exception as e:
            logger.error(f"Error making predictions: {e}")
            raise

    def cross_validate(self, X: pd.DataFrame, y: pd.Series, cv_folds: int = 5) -> Dict[str, float]:
        """
        Perform time series cross-validation.

        Args:
            X: Feature dataframe
            y: Target series
            cv_folds: Number of cross-validation folds

        Returns:
            Dictionary of cross-validation metrics
        """
        try:
            # Use TimeSeriesSplit to respect temporal order
            tscv = TimeSeriesSplit(n_splits=cv_folds)

            # Create model for cross-validation
            model = lgb.LGBMClassifier(**self.model_params)

            # Perform cross-validation
            cv_scores = cross_val_score(model, X, y, cv=tscv, scoring="accuracy")
            cv_precision = cross_val_score(model, X, y, cv=tscv, scoring="precision")
            cv_recall = cross_val_score(model, X, y, cv=tscv, scoring="recall")
            cv_f1 = cross_val_score(model, X, y, cv=tscv, scoring="f1")

            metrics = {
                "cv_accuracy_mean": cv_scores.mean(),
                "cv_accuracy_std": cv_scores.std(),
                "cv_precision_mean": cv_precision.mean(),
                "cv_precision_std": cv_precision.std(),
                "cv_recall_mean": cv_recall.mean(),
                "cv_recall_std": cv_recall.std(),
                "cv_f1_mean": cv_f1.mean(),
                "cv_f1_std": cv_f1.std(),
            }

            logger.info(
                f"Cross-validation completed. Mean accuracy: {metrics['cv_accuracy_mean']:.4f} ± {metrics['cv_accuracy_std']:.4f}"
            )

            return metrics

        except Exception as e:
            logger.error(f"Error performing cross-validation: {e}")
            raise

    def get_feature_importance(self, top_n: int = 20) -> pd.Series:
        """
        Get top N most important features.

        Args:
            top_n: Number of top features to return

        Returns:
            Series with feature importance scores
        """
        if self.feature_importance is None:
            raise ValueError("Model must be trained before getting feature importance")

        return self.feature_importance.head(top_n)

    def evaluate_model(self, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
        """
        Evaluate model performance on test data.

        Args:
            X_test: Test feature dataframe
            y_test: Test target series

        Returns:
            Dictionary of evaluation metrics
        """
        if not self.is_trained or self.model is None:
            raise ValueError("Model must be trained before evaluation")

        try:
            predictions, probabilities = self.predict(X_test)

            metrics = {
                "test_accuracy": accuracy_score(y_test, predictions),
                "test_precision": precision_score(y_test, predictions),
                "test_recall": recall_score(y_test, predictions),
                "test_f1": f1_score(y_test, predictions),
                "test_auc": roc_auc_score(y_test, probabilities[:, 1]),
            }

            logger.info(f"Model evaluation completed. Test accuracy: {metrics['test_accuracy']:.4f}")

            return metrics

        except Exception as e:
            logger.error(f"Error evaluating model: {e}")
            raise

    def save_model(self, filepath: str) -> None:
        """
        Save the trained model to disk.

        Args:
            filepath: Path to save the model
        """
        if not self.is_trained or self.model is None:
            raise ValueError("Model must be trained before saving")

        try:
            self.model.booster_.save_model(filepath)
            logger.info(f"Model saved to {filepath}")

        except Exception as e:
            logger.error(f"Error saving model: {e}")
            raise

    def load_model(self, filepath: str) -> None:
        """
        Load a trained model from disk.

        Args:
            filepath: Path to load the model from
        """
        try:
            self.model = lgb.LGBMClassifier(**self.model_params)
            self.model.booster_ = lgb.Booster(model_file=filepath)
            self.is_trained = True
            logger.info(f"Model loaded from {filepath}")

        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
