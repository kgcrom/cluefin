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

    def create_target_variable(self, df: pd.DataFrame, target_type: str = "binary") -> pd.DataFrame:
        """
        Create target variable for ML prediction.

        Args:
            df: DataFrame with stock data
            target_type: Type of target ("binary" for up/down, "regression" for price change)

        Returns:
            DataFrame with target variable
        """
        try:
            if target_type == "binary":
                # Binary classification: 1 if next day close > today close, 0 otherwise
                df["target"] = (df["close"].shift(-1) > df["close"]).astype(int)
            elif target_type == "regression":
                # Regression: next day percentage change
                df["target"] = df["close"].shift(-1).pct_change()
            else:
                raise ValueError(f"Unknown target_type: {target_type}")

            # Remove last row as it doesn't have target
            df = df[:-1].copy()

            logger.info(f"Created {target_type} target variable")
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
            non_feature_cols = ["open", "high", "low", "close", "volume", "target"]
            feature_cols = [col for col in df.columns if col not in non_feature_cols]

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
