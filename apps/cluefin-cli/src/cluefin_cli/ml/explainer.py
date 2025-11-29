"""
SHAP-based model explainer for stock prediction models.

This module provides model interpretability using SHAP (SHapley Additive exPlanations)
for understanding feature importance and individual prediction explanations.
"""

from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import shap
from scipy.special import expit as sigmoid
from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class SHAPExplainer:
    """
    SHAP-based explainer for stock prediction models.

    Provides model interpretability using SHAP values to explain
    feature importance and individual predictions.
    """

    def __init__(self, model, model_type: str = "tree"):
        """
        Initialize SHAP explainer with trained model.

        Args:
            model: Trained ML model (LightGBM, sklearn, etc.)
            model_type: Type of SHAP explainer ("tree", "kernel", "linear")
        """
        self.model = model
        self.model_type = model_type
        self.explainer: Optional[shap.Explainer] = None
        self.shap_values: Optional[np.ndarray] = None
        self.feature_names: List[str] = []
        self.console = Console()

    def initialize_explainer(self, X_background: pd.DataFrame) -> None:
        """
        Initialize SHAP explainer with background data.

        Args:
            X_background: Background dataset for SHAP explainer
        """
        try:
            self.feature_names = list(X_background.columns)

            if self.model_type == "tree":
                # TreeExplainer for tree-based models (LightGBM, XGBoost, etc.)
                self.explainer = shap.TreeExplainer(self.model)
            elif self.model_type == "kernel":
                # KernelExplainer for model-agnostic explanations
                self.explainer = shap.KernelExplainer(
                    self.model.predict_proba,
                    X_background.sample(min(100, len(X_background))),  # Sample for efficiency
                )
            elif self.model_type == "linear":
                # LinearExplainer for linear models
                self.explainer = shap.LinearExplainer(self.model, X_background)
            else:
                raise ValueError(f"Unknown model_type: {self.model_type}")

            logger.info(f"SHAP {self.model_type}Explainer initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing SHAP explainer: {e}")
            raise

    def calculate_shap_values(self, X: pd.DataFrame) -> np.ndarray:
        """
        Calculate SHAP values for given data.

        Args:
            X: Feature dataframe

        Returns:
            SHAP values array
        """
        if self.explainer is None:
            raise ValueError("SHAP explainer must be initialized first")

        try:
            # Calculate SHAP values
            if self.model_type == "tree":
                # For tree models, get SHAP values for positive class
                shap_values = self.explainer.shap_values(X)
                if isinstance(shap_values, list):
                    # Binary classification returns list of arrays
                    self.shap_values = shap_values[1]  # Positive class
                else:
                    self.shap_values = shap_values
            else:
                self.shap_values = self.explainer.shap_values(X)

            logger.info(f"SHAP values calculated for {len(X)} samples")
            return self.shap_values

        except Exception as e:
            logger.error(f"Error calculating SHAP values: {e}")
            raise

    def get_feature_importance(self, X: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
        """
        Get global feature importance from SHAP values.

        Args:
            X: Feature dataframe
            top_n: Number of top features to return

        Returns:
            DataFrame with feature importance
        """
        if self.shap_values is None:
            self.calculate_shap_values(X)

        try:
            # Calculate mean absolute SHAP values for each feature
            feature_importance = pd.DataFrame(
                {
                    "feature": self.feature_names,
                    "importance": np.abs(self.shap_values).mean(axis=0),
                    "mean_shap": self.shap_values.mean(axis=0),
                }
            )

            # Sort by importance
            feature_importance = feature_importance.sort_values("importance", ascending=False)

            return feature_importance.head(top_n)

        except Exception as e:
            logger.error(f"Error calculating feature importance: {e}")
            raise

    def explain_prediction(self, X_sample: pd.DataFrame, sample_idx: int = 0) -> Dict[str, Any]:
        """
        Explain individual prediction using SHAP values.

        Args:
            X_sample: Sample data
            sample_idx: Index of sample to explain

        Returns:
            Dictionary with explanation details
        """
        if self.shap_values is None:
            self.calculate_shap_values(X_sample)

        try:
            sample_shap = self.shap_values[sample_idx]
            sample_features = X_sample.iloc[sample_idx]

            # Get prediction and base value
            if hasattr(self.explainer, "expected_value"):
                if isinstance(self.explainer.expected_value, list):
                    base_value = self.explainer.expected_value[1]  # Positive class
                else:
                    base_value = self.explainer.expected_value
            else:
                base_value = 0.0

            # Create explanation DataFrame
            explanation = pd.DataFrame(
                {
                    "feature": self.feature_names,
                    "value": sample_features.values,
                    "shap_value": sample_shap,
                    "abs_shap": np.abs(sample_shap),
                }
            ).sort_values("abs_shap", ascending=False)

            total_prediction = base_value + sample_shap.sum()
            # Convert log-odds to probability using sigmoid function
            probability = float(sigmoid(total_prediction))

            return {
                "base_value": base_value,
                "prediction_impact": sample_shap.sum(),
                "total_prediction": total_prediction,
                "probability": probability,
                "feature_contributions": explanation,
                "top_positive": explanation[explanation["shap_value"] > 0].head(5),
                "top_negative": explanation[explanation["shap_value"] < 0].head(5),
            }

        except Exception as e:
            logger.error(f"Error explaining prediction: {e}")
            raise

    def display_feature_importance(self, X: pd.DataFrame, top_n: int = 15) -> None:
        """
        Display feature importance in a rich table format.

        Args:
            X: Feature dataframe
            top_n: Number of top features to display
        """
        try:
            importance_df = self.get_feature_importance(X, top_n)

            # Create rich table
            table = Table(title=f"🔍 Top {top_n} Feature Importance (SHAP)")
            table.add_column("Rank", style="dim", width=6)
            table.add_column("Feature", style="bold blue", min_width=20)
            table.add_column("Importance", justify="right", style="green")
            table.add_column("Mean SHAP", justify="right", style="yellow")
            table.add_column("Impact", justify="center", width=10)

            for idx, row in importance_df.iterrows():
                rank = str(len(importance_df) - len(importance_df[importance_df.index >= idx]) + 1)
                feature = row["feature"]
                importance = f"{row['importance']:.4f}"
                mean_shap = f"{row['mean_shap']:+.4f}"

                # Determine impact direction
                if row["mean_shap"] > 0:
                    impact = "📈 UP"
                    impact_style = "green"
                elif row["mean_shap"] < 0:
                    impact = "📉 DOWN"
                    impact_style = "red"
                else:
                    impact = "➖ NEUTRAL"
                    impact_style = "dim"

                table.add_row(rank, feature, importance, mean_shap, f"[{impact_style}]{impact}[/{impact_style}]")

            self.console.print("\n")
            self.console.print(table)

        except Exception as e:
            logger.error(f"Error displaying feature importance: {e}")
            raise

    def display_prediction_explanation(self, X_sample: pd.DataFrame, sample_idx: int = 0) -> None:
        """
        Display explanation for individual prediction.

        Args:
            X_sample: Sample data
            sample_idx: Index of sample to explain
        """
        try:
            explanation = self.explain_prediction(X_sample, sample_idx)

            # Create summary panel
            probability = explanation["probability"]
            if probability > 0.5:
                prediction_text = f"[green]📈 UP ({probability:.1%})[/green]"
            else:
                prediction_text = f"[red]📉 DOWN ({1 - probability:.1%})[/red]"

            summary_text = f"""
Base Value (log-odds): {explanation["base_value"]:.4f}
Prediction Impact: {explanation["prediction_impact"]:+.4f}
Final Prediction: {prediction_text}
            """

            self.console.print(Panel(summary_text.strip(), title="🎯 Prediction Summary", border_style="blue"))

            # Top positive contributions
            if not explanation["top_positive"].empty:
                pos_table = Table(title="📈 Top Positive Contributors", border_style="green")
                pos_table.add_column("Feature", style="bold")
                pos_table.add_column("Value", justify="right")
                pos_table.add_column("SHAP", justify="right", style="green")

                for _, row in explanation["top_positive"].iterrows():
                    pos_table.add_row(row["feature"], f"{row['value']:.4f}", f"+{row['shap_value']:.4f}")

                self.console.print(pos_table)

            # Top negative contributions
            if not explanation["top_negative"].empty:
                neg_table = Table(title="📉 Top Negative Contributors", border_style="red")
                neg_table.add_column("Feature", style="bold")
                neg_table.add_column("Value", justify="right")
                neg_table.add_column("SHAP", justify="right", style="red")

                for _, row in explanation["top_negative"].iterrows():
                    neg_table.add_row(row["feature"], f"{row['value']:.4f}", f"{row['shap_value']:.4f}")

                self.console.print(neg_table)

        except Exception as e:
            logger.error(f"Error displaying prediction explanation: {e}")
            raise

    def get_summary_statistics(self, X: pd.DataFrame) -> Dict[str, Any]:
        """
        Get summary statistics about SHAP values.

        Args:
            X: Feature dataframe

        Returns:
            Dictionary with summary statistics
        """
        if self.shap_values is None:
            self.calculate_shap_values(X)

        try:
            stats = {
                "n_samples": len(self.shap_values),
                "n_features": len(self.feature_names),
                "mean_prediction_impact": np.abs(self.shap_values).sum(axis=1).mean(),
                "std_prediction_impact": np.abs(self.shap_values).sum(axis=1).std(),
                "most_important_feature": self.feature_names[np.abs(self.shap_values).mean(axis=0).argmax()],
                "least_important_feature": self.feature_names[np.abs(self.shap_values).mean(axis=0).argmin()],
            }

            return stats

        except Exception as e:
            logger.error(f"Error calculating summary statistics: {e}")
            raise
