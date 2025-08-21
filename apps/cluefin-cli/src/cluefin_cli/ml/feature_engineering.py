"""
Feature engineering module for ML-based stock prediction.

This module handles the conversion of stock data and technical indicators
into ML-ready features, including TA-Lib indicators and target variable creation.
"""

from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import talib
from loguru import logger
from sklearn.preprocessing import LabelEncoder, StandardScaler

try:
    from imblearn.over_sampling import SMOTE

    SMOTE_AVAILABLE = True
except ImportError:
    SMOTE_AVAILABLE = False
    logger.warning("imbalanced-learn not available. SMOTE oversampling will be disabled.")


class FeatureEngineer:
    """
    Feature engineering class for stock prediction ML pipeline.

    Converts raw stock data and technical indicators into ML-ready features
    using TA-Lib and custom feature engineering techniques.
    """

    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_names: List[str] = []

    def create_talib_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create technical indicators using TA-Lib library.

        Args:
            df: DataFrame with OHLCV data

        Returns:
            DataFrame with additional TA-Lib features
        """
        try:
            # Extract OHLCV arrays
            high = df["high"].values
            low = df["low"].values
            close = df["close"].values
            volume = df["volume"].values

            # Trend indicators
            df["sma_5"] = talib.SMA(close, timeperiod=5)
            df["sma_10"] = talib.SMA(close, timeperiod=10)
            df["sma_20"] = talib.SMA(close, timeperiod=20)
            df["ema_12"] = talib.EMA(close, timeperiod=12)
            df["ema_26"] = talib.EMA(close, timeperiod=26)

            # MACD
            df["macd"], df["macd_signal"], df["macd_hist"] = talib.MACD(close)

            # Bollinger Bands
            df["bb_upper"], df["bb_middle"], df["bb_lower"] = talib.BBANDS(close)
            df["bb_width"] = (df["bb_upper"] - df["bb_lower"]) / df["bb_middle"]
            df["bb_position"] = (close - df["bb_lower"]) / (df["bb_upper"] - df["bb_lower"])

            # Momentum indicators
            df["rsi_14"] = talib.RSI(close, timeperiod=14)
            df["stoch_k"], df["stoch_d"] = talib.STOCH(high, low, close)
            df["williams_r"] = talib.WILLR(high, low, close)

            # Volume indicators
            df["obv"] = talib.OBV(close, volume)
            df["ad_line"] = talib.AD(high, low, close, volume)
            df["volume_sma"] = talib.SMA(volume.astype(float), timeperiod=20)
            df["volume_ratio"] = volume / df["volume_sma"]

            # Volatility indicators
            df["atr"] = talib.ATR(high, low, close, timeperiod=14)
            df["natr"] = talib.NATR(high, low, close, timeperiod=14)

            # Pattern recognition (a few key patterns)
            df["cdl_doji"] = talib.CDLDOJI(df["open"], high, low, close)
            df["cdl_hammer"] = talib.CDLHAMMER(df["open"], high, low, close)
            df["cdl_engulfing"] = talib.CDLENGULFING(df["open"], high, low, close)

            logger.info("Successfully created TA-Lib features")
            return df

        except Exception as e:
            logger.error(f"Error creating TA-Lib features: {e}")
            return df

    def create_custom_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create custom technical analysis features.

        Args:
            df: DataFrame with stock data

        Returns:
            DataFrame with additional custom features
        """
        try:
            # Price-based features
            df["price_change"] = df["close"].pct_change()
            df["high_low_ratio"] = df["high"] / df["low"]
            df["close_open_ratio"] = df["close"] / df["open"]

            # Rolling statistics
            for period in [5, 10, 20]:
                df[f"price_volatility_{period}"] = df["close"].rolling(period).std()
                df[f"volume_volatility_{period}"] = df["volume"].rolling(period).std()
                df[f"high_low_avg_{period}"] = ((df["high"] + df["low"]) / 2).rolling(period).mean()

            # Lag features
            for lag in [1, 2, 3, 5]:
                df[f"close_lag_{lag}"] = df["close"].shift(lag)
                df[f"volume_lag_{lag}"] = df["volume"].shift(lag)
                df[f"rsi_lag_{lag}"] = df.get("rsi_14", pd.Series()).shift(lag)

            logger.info("Successfully created custom features")
            return df

        except Exception as e:
            logger.error(f"Error creating custom features: {e}")
            return df

    def create_target_variable(
        self, df: pd.DataFrame, target_type: str = "binary", threshold_pct: float = 0.0, prediction_days: int = 1
    ) -> pd.DataFrame:
        """
        Create target variable for ML prediction with improved methods.

        Args:
            df: DataFrame with stock data
            target_type: Type of target ("binary", "threshold", "regression")
            threshold_pct: Percentage threshold for classification (e.g., 0.02 for 2%)
            prediction_days: Number of days ahead to predict

        Returns:
            DataFrame with target variable
        """
        try:
            logger.info(
                f"Creating {target_type} target variable with threshold {threshold_pct:.2%}, {prediction_days} days ahead"
            )

            # Calculate future price change
            future_close = df["close"].shift(-prediction_days)
            current_close = df["close"]
            price_change_pct = (future_close - current_close) / current_close

            if target_type == "binary":
                # Simple binary: 1 if price goes up, 0 if down
                df["target"] = (price_change_pct > 0).astype(int)

            elif target_type == "threshold":
                # Threshold-based binary: 1 if change > threshold, 0 if change < -threshold
                # Ignore small changes (neutral class becomes 0)
                df["target"] = 0  # Default neutral
                df.loc[price_change_pct > threshold_pct, "target"] = 1  # Significant up
                df.loc[price_change_pct < -threshold_pct, "target"] = 0  # Significant down or neutral

            elif target_type == "regression":
                # Regression: future percentage change
                df["target"] = price_change_pct

            else:
                raise ValueError(f"Unknown target_type: {target_type}")

            # Remove rows without target (last N rows)
            df = df[:-prediction_days].copy()

            # Log target distribution for debugging
            if target_type in ["binary", "threshold"]:
                target_dist = df["target"].value_counts()
                logger.info(f"Target distribution: {target_dist.to_dict()}")

                # Check for severe imbalance
                if len(target_dist) == 2:
                    ratio = max(target_dist) / min(target_dist)
                    if ratio > 10:
                        logger.warning(f"Severe class imbalance detected: {ratio:.2f}:1")
                    elif ratio > 3:
                        logger.warning(f"Moderate class imbalance detected: {ratio:.2f}:1")

            logger.info(f"Created {target_type} target variable: {len(df)} samples")
            return df

        except Exception as e:
            logger.error(f"Error creating target variable: {e}")
            return df

    def prepare_features(self, stock_data: pd.DataFrame, indicators: Dict) -> Tuple[pd.DataFrame, List[str]]:
        """
        Prepare all features for ML training.

        Args:
            stock_data: Raw stock OHLCV data
            indicators: Dictionary of existing technical indicators

        Returns:
            Tuple of (feature_df, feature_names)
        """
        try:
            # Ensure required columns exist
            required_cols = ["open", "high", "low", "close", "volume"]
            if not all(col in stock_data.columns for col in required_cols):
                raise ValueError(f"Missing required columns: {required_cols}")

            df = stock_data.copy()

            # Add existing indicators to DataFrame
            for name, values in indicators.items():
                if len(values) == len(df):
                    df[name] = values

            # Create TA-Lib features
            df = self.create_talib_features(df)

            # Create custom features
            df = self.create_custom_features(df)

            # Create target variable
            df = self.create_target_variable(df)

            # Remove non-feature columns and identify feature columns
            non_feature_cols = ["open", "high", "low", "close", "volume", "target", "date", "datetime"]
            feature_cols = [col for col in df.columns if col not in non_feature_cols]

            # Also remove any columns with datetime-like dtypes
            datetime_cols = [col for col in feature_cols if pd.api.types.is_datetime64_any_dtype(df[col])]
            feature_cols = [col for col in feature_cols if col not in datetime_cols]

            if datetime_cols:
                logger.info(f"Removed datetime columns from features: {datetime_cols}")

            # Handle missing values
            df = self._handle_missing_values(df, feature_cols)

            self.feature_names = feature_cols
            logger.info(f"Prepared {len(feature_cols)} features for ML training")

            return df, feature_cols

        except Exception as e:
            logger.error(f"Error preparing features: {e}")
            raise

    def _handle_missing_values(self, df: pd.DataFrame, feature_cols: List[str]) -> pd.DataFrame:
        """
        Handle missing values in feature columns.

        Args:
            df: DataFrame with features
            feature_cols: List of feature column names

        Returns:
            DataFrame with handled missing values
        """
        # Forward fill then backward fill (using new pandas methods)
        df[feature_cols] = df[feature_cols].ffill().bfill().infer_objects(copy=False)

        # Drop rows with remaining NaN values
        initial_rows = len(df)
        df = df.dropna()
        final_rows = len(df)

        if initial_rows != final_rows:
            logger.warning(f"Dropped {initial_rows - final_rows} rows due to missing values")

        return df

    def normalize_features(
        self, train_features: pd.DataFrame, test_features: pd.DataFrame = None
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Normalize features using StandardScaler.

        Args:
            train_features: Training features
            test_features: Testing features (optional)

        Returns:
            Tuple of normalized (train_features, test_features)
        """
        # Fit scaler on training data
        train_normalized = pd.DataFrame(
            self.scaler.fit_transform(train_features), columns=train_features.columns, index=train_features.index
        )

        if test_features is not None:
            test_normalized = pd.DataFrame(
                self.scaler.transform(test_features), columns=test_features.columns, index=test_features.index
            )
            return train_normalized, test_normalized

        return train_normalized, None

    def apply_smote_oversampling(
        self, X: pd.DataFrame, y: pd.Series, sampling_strategy: str = "auto", random_state: int = 42
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Apply SMOTE oversampling to handle class imbalance.

        Args:
            X: Feature dataframe
            y: Target series
            sampling_strategy: SMOTE sampling strategy ('auto', 'minority', float)
            random_state: Random state for reproducibility

        Returns:
            Tuple of (resampled_X, resampled_y)
        """
        if not SMOTE_AVAILABLE:
            logger.warning("SMOTE not available. Returning original data.")
            return X, y

        try:
            logger.info("Applying SMOTE oversampling...")

            # Check class distribution before SMOTE
            original_dist = y.value_counts()
            logger.info(f"Original class distribution: {original_dist.to_dict()}")

            # Apply SMOTE
            smote = SMOTE(sampling_strategy=sampling_strategy, random_state=random_state)
            X_resampled, y_resampled = smote.fit_resample(X, y)

            # Convert back to DataFrame/Series with original column names
            X_resampled = pd.DataFrame(X_resampled, columns=X.columns)
            y_resampled = pd.Series(y_resampled, name=y.name)

            # Check class distribution after SMOTE
            new_dist = y_resampled.value_counts()
            logger.info(f"After SMOTE class distribution: {new_dist.to_dict()}")
            logger.info(f"Data size increased from {len(X)} to {len(X_resampled)} samples")

            return X_resampled, y_resampled

        except Exception as e:
            logger.error(f"Error applying SMOTE: {e}")
            return X, y

    def calculate_class_weights(self, y: pd.Series) -> Dict[int, float]:
        """
        Calculate class weights for handling imbalanced data.

        Args:
            y: Target series

        Returns:
            Dictionary of class weights
        """
        try:
            from sklearn.utils.class_weight import compute_class_weight

            classes = np.unique(y)
            class_weights = compute_class_weight("balanced", classes=classes, y=y)
            weight_dict = {cls: weight for cls, weight in zip(classes, class_weights, strict=False)}

            logger.info(f"Calculated class weights: {weight_dict}")
            return weight_dict

        except Exception as e:
            logger.error(f"Error calculating class weights: {e}")
            return {}
