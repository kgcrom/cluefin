"""
Main ML prediction pipeline for stock analysis.

This module provides the main StockMLPredictor class that integrates
feature engineering, model training, and SHAP explanation into a
unified pipeline for stock prediction.
"""

from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
from loguru import logger
from rich.console import Console
from rich.panel import Panel

from .diagnostics import MLDiagnostics
from .explainer import SHAPExplainer
from .feature_engineering import FeatureEngineer
from .models import StockPredictor


class StockMLPredictor:
    """
    Main ML prediction pipeline for stock analysis.

    Integrates feature engineering, model training, and SHAP explanations
    into a unified pipeline for stock price movement prediction.
    """

    def __init__(self, model_params: Optional[Dict] = None, enable_diagnostics: bool = True):
        """
        Initialize the ML prediction pipeline.

        Args:
            model_params: Optional parameters for the ML model
            enable_diagnostics: Enable diagnostic features
        """
        self.feature_engineer = FeatureEngineer()
        self.model = StockPredictor(model_params)
        self.explainer: Optional[SHAPExplainer] = None
        self.diagnostics = MLDiagnostics() if enable_diagnostics else None
        self.console = Console()

        # Pipeline state
        self.is_fitted = False
        self.feature_names: List[str] = []
        self.training_metrics: Dict[str, float] = {}

        # Configuration
        self.enable_diagnostics = enable_diagnostics

    def prepare_data(self, stock_data: pd.DataFrame, indicators: Dict) -> Tuple[pd.DataFrame, List[str]]:
        """
        Prepare data for ML training using feature engineering.

        Args:
            stock_data: Raw stock OHLCV data
            indicators: Dictionary of existing technical indicators

        Returns:
            Tuple of (prepared_dataframe, feature_names)
        """
        try:
            logger.info("Starting data preparation...")

            # Prepare features using feature engineer
            prepared_df, feature_names = self.feature_engineer.prepare_features(stock_data, indicators)

            self.feature_names = feature_names
            logger.info(f"Data preparation completed. {len(feature_names)} features created.")

            return prepared_df, feature_names

        except Exception as e:
            logger.error(f"Error preparing data: {e}")
            raise

    def train_model(
        self,
        prepared_df: pd.DataFrame,
        validation_split: float = 0.2,
        use_smote: bool = True,
        use_class_weights: bool = True,
    ) -> Dict[str, float]:
        """
        Train the ML model on prepared data with improved handling for class imbalance.

        Args:
            prepared_df: DataFrame with features and target
            validation_split: Fraction of data for validation
            use_smote: Whether to apply SMOTE oversampling
            use_class_weights: Whether to use balanced class weights

        Returns:
            Dictionary of training metrics
        """
        try:
            logger.info("🏋️ Starting enhanced model training...")

            # Split features and target
            X = prepared_df[self.feature_names]
            y = prepared_df["target"]

            logger.info(f"📊 Training data shape: {X.shape}")
            logger.info(f"🎯 Original target distribution: {y.value_counts().to_dict()}")

            # Run diagnostics if enabled
            if self.enable_diagnostics and self.diagnostics:
                logger.info("🔍 Running pre-training diagnostics...")
                diagnosis = self.diagnostics.diagnose_training_data(X, y, self.feature_names)

                # Apply recommendations
                if diagnosis["target_analysis"]["is_severely_imbalanced"] and use_smote:
                    logger.info("⚖️ Applying SMOTE to handle severe class imbalance...")
                    X, y = self.feature_engineer.apply_smote_oversampling(X, y)
                    logger.info(f"📈 After SMOTE - Data shape: {X.shape}, Distribution: {y.value_counts().to_dict()}")

            # Calculate class weights if requested
            class_weights = None
            if use_class_weights:
                class_weights = self.feature_engineer.calculate_class_weights(y)
                if class_weights:
                    # Update model params with class weights
                    self.model.model_params["class_weight"] = class_weights

            # Train model
            self.training_metrics = self.model.train(X, y, validation_split)

            # Log detailed training results
            logger.info("✅ Model training completed successfully")
            logger.info(f"📈 Validation accuracy: {self.training_metrics.get('val_accuracy', 0):.4f}")
            logger.info(f"📈 Validation precision: {self.training_metrics.get('val_precision', 0):.4f}")
            logger.info(f"📈 Validation recall: {self.training_metrics.get('val_recall', 0):.4f}")
            logger.info(f"📈 Validation F1-score: {self.training_metrics.get('val_f1', 0):.4f}")

            # Initialize SHAP explainer
            try:
                self.explainer = SHAPExplainer(self.model.model, model_type="tree")
                # Use a sample of training data as background for SHAP
                background_size = min(100, len(X))
                background_data = X.sample(background_size, random_state=42)
                self.explainer.initialize_explainer(background_data)
                logger.info("🔍 SHAP explainer initialized successfully")
            except Exception as e:
                logger.warning(f"⚠️ SHAP explainer initialization failed: {e}")
                self.explainer = None

            self.is_fitted = True

            return self.training_metrics

        except Exception as e:
            logger.error(f"❌ Error training model: {e}")
            raise

    def predict(self, stock_data: pd.DataFrame, indicators: Dict) -> Dict[str, Any]:
        """
        Make predictions on new stock data.

        Args:
            stock_data: Raw stock OHLCV data
            indicators: Dictionary of technical indicators

        Returns:
            Dictionary with prediction results
        """
        if not self.is_fitted:
            raise ValueError("Model must be trained before making predictions")

        try:
            logger.info("Making predictions...")

            # Prepare data (without target variable creation for prediction)
            df = stock_data.copy()

            # Add existing indicators
            for name, values in indicators.items():
                if len(values) == len(df):
                    df[name] = values

            # Create TA-Lib and custom features
            df = self.feature_engineer.create_talib_features(df)
            df = self.feature_engineer.create_custom_features(df)

            # Handle missing values for feature columns only
            feature_df = df[self.feature_names].ffill().bfill().infer_objects(copy=False)
            feature_df = feature_df.dropna()

            if len(feature_df) == 0:
                raise ValueError("No valid data available for prediction after preprocessing")

            # Make predictions
            predictions, probabilities = self.model.predict(feature_df)

            # Get latest prediction
            latest_prediction = predictions[-1]
            latest_probability = probabilities[-1]

            # Calculate SHAP values for explanation
            shap_values = None
            if self.explainer is not None:
                try:
                    shap_values = self.explainer.calculate_shap_values(feature_df.tail(1))
                except Exception as e:
                    logger.warning(f"Could not calculate SHAP values: {e}")

            result = {
                "prediction": int(latest_prediction),
                "probability_down": float(latest_probability[0]),
                "probability_up": float(latest_probability[1]),
                "confidence": float(max(latest_probability)),
                "signal": "BUY" if latest_prediction == 1 else "SELL",
                "shap_available": shap_values is not None,
                "feature_data": feature_df.tail(1),
            }

            logger.info(f"Prediction completed. Signal: {result['signal']}, Confidence: {result['confidence']:.4f}")

            return result

        except Exception as e:
            logger.error(f"Error making predictions: {e}")
            raise

    def display_prediction_results(self, prediction_result: Dict[str, Any]) -> None:
        """
        Display prediction results in a rich format.

        Args:
            prediction_result: Results from predict() method
        """
        try:
            # Main prediction panel
            prob_up = prediction_result["probability_up"]
            prob_down = prediction_result["probability_down"]
            confidence = prediction_result["confidence"]
            signal = prediction_result["signal"]

            if signal == "BUY":
                signal_text = f"[green]📈 {signal} ({prob_up:.1%})[/green]"
                panel_style = "green"
            else:
                signal_text = f"[red]📉 {signal} ({prob_down:.1%})[/red]"
                panel_style = "red"

            prediction_text = f"""
Signal: {signal_text}
Confidence: {confidence:.1%}
Up Probability: {prob_up:.1%}
Down Probability: {prob_down:.1%}
            """

            self.console.print("\n")
            self.console.print(
                Panel(prediction_text.strip(), title="🎯 ML Prediction Results", border_style=panel_style)
            )

            # Model performance panel
            if self.training_metrics:
                metrics_text = f"""
Validation Accuracy: {self.training_metrics.get("val_accuracy", 0):.1%}
Validation F1-Score: {self.training_metrics.get("val_f1", 0):.3f}
Validation AUC: {self.training_metrics.get("val_auc", 0):.3f}
                """

                self.console.print(Panel(metrics_text.strip(), title="📊 Model Performance", border_style="blue"))

        except Exception as e:
            logger.error(f"Error displaying prediction results: {e}")

    def display_feature_importance(self, prediction_result: Dict[str, Any], top_n: int = 10) -> None:
        """
        Display feature importance using SHAP values.

        Args:
            prediction_result: Results from predict() method
            top_n: Number of top features to display
        """
        if not prediction_result["shap_available"] or self.explainer is None:
            self.console.print("[yellow]⚠️  SHAP analysis not available[/yellow]")
            return

        try:
            # Display global feature importance
            feature_data = prediction_result["feature_data"]
            self.explainer.display_feature_importance(feature_data, top_n)

            # Display prediction explanation for the latest sample
            self.console.print("\n")
            self.explainer.display_prediction_explanation(feature_data, 0)

        except Exception as e:
            logger.error(f"Error displaying feature importance: {e}")

    def get_model_summary(self) -> Dict[str, Any]:
        """
        Get summary information about the trained model.

        Returns:
            Dictionary with model summary
        """
        if not self.is_fitted:
            return {"status": "not_trained"}

        try:
            # Get feature importance from model
            model_importance = self.model.get_feature_importance(10)

            summary = {
                "status": "trained",
                "n_features": len(self.feature_names),
                "training_metrics": self.training_metrics,
                "top_features": model_importance.to_dict(),
                "model_type": "LightGBM",
                "shap_available": self.explainer is not None,
            }

            return summary

        except Exception as e:
            logger.error(f"Error getting model summary: {e}")
            return {"status": "error", "error": str(e)}

    def cross_validate_model(self, prepared_df: pd.DataFrame, cv_folds: int = 5) -> Dict[str, float]:
        """
        Perform cross-validation on the prepared data.

        Args:
            prepared_df: DataFrame with features and target
            cv_folds: Number of cross-validation folds

        Returns:
            Dictionary of cross-validation metrics
        """
        try:
            logger.info(f"Starting {cv_folds}-fold cross-validation...")

            # Split features and target
            X = prepared_df[self.feature_names]
            y = prepared_df["target"]

            # Perform cross-validation
            cv_metrics = self.model.cross_validate(X, y, cv_folds)

            logger.info(f"Cross-validation completed. Mean accuracy: {cv_metrics['cv_accuracy_mean']:.4f}")

            return cv_metrics

        except Exception as e:
            logger.error(f"Error performing cross-validation: {e}")
            raise
