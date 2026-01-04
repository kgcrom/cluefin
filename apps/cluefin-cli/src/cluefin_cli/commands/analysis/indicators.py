from typing import Any, Dict

import numpy as np
import pandas as pd
from loguru import logger


class TechnicalAnalyzer:
    """Calculates technical indicators for stock analysis."""

    def calculate_all(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate all technical indicators for the given stock data.

        Args:
            data: DataFrame with OHLCV data

        Returns:
            DataFrame with all calculated indicators
        """
        if data.empty:
            return pd.DataFrame()

        result = data.copy()

        # Moving Averages
        result["sma_5"] = self._sma(data["close"], 5)
        result["sma_20"] = self._sma(data["close"], 20)
        result["sma_50"] = self._sma(data["close"], 50)
        result["sma_120"] = self._sma(data["close"], 120)
        result["sma_240"] = self._sma(data["close"], 240)
        result["ema_12"] = self._ema(data["close"], 12)
        result["ema_26"] = self._ema(data["close"], 26)

        # RSI
        result["rsi"] = self._rsi(data["close"], 14)

        # MACD
        macd_line = result["ema_12"] - result["ema_26"]
        macd_signal = self._ema(macd_line, 9)
        result["macd"] = macd_line
        result["macd_signal"] = macd_signal
        result["macd_histogram"] = macd_line - macd_signal

        # Bollinger Bands
        bb_middle = result["sma_20"]
        bb_std = data["close"].rolling(window=20).std()
        result["bb_middle"] = bb_middle
        result["bb_upper"] = bb_middle + (bb_std * 2)
        result["bb_lower"] = bb_middle - (bb_std * 2)

        # Stochastic Oscillator
        stoch_k, stoch_d = self._stochastic(data["high"], data["low"], data["close"])
        result["stoch_k"] = stoch_k
        result["stoch_d"] = stoch_d

        # Volume indicators
        result["volume_sma"] = self._sma(data["volume"], 20)

        # Support and Resistance levels
        result = self._calculate_support_resistance(result)

        # Pattern Recognition: Cup & Handle
        if len(data) >= 120:
            try:
                import cluefin_ta as talib

                open_arr = data["open"].values
                high = data["high"].values
                low = data["low"].values
                close = data["close"].values
                volume = data["volume"].values if "volume" in data.columns else None

                cup_pattern = talib.CUP_HANDLE(
                    open_arr=open_arr,
                    high=high,
                    low=low,
                    close=close,
                    volume=volume,
                    cup_lookback=120,
                    handle_len=30,
                    pivot_method="zigzag",
                    pivot_pct=0.04,
                    use_volume=volume is not None,
                )
                result["cup_pattern"] = cup_pattern
                result["cup_has_volume"] = volume is not None

            except Exception as e:
                logger.warning(f"Cup pattern calculation failed: {e}")
                result["cup_pattern"] = 0
                result["cup_has_volume"] = False
        else:
            result["cup_pattern"] = 0
            result["cup_has_volume"] = False

        # Pattern Recognition: Dow Theory Trend Analysis
        if len(data) >= 200:
            try:
                import cluefin_ta as talib

                high = data["high"].values
                low = data["low"].values
                close = data["close"].values
                volume = data["volume"].values if "volume" in data.columns else None

                trend_state, correlation_state = talib.DOW_THEORY(
                    high=high,
                    low=low,
                    close=close,
                    volume=volume,
                    swing_window=5,
                    method="swing",
                )
                result["dow_trend"] = trend_state
                result["dow_correlation"] = correlation_state
                result["dow_has_volume"] = volume is not None

            except Exception as e:
                logger.warning(f"Dow Theory calculation failed: {e}")
                result["dow_trend"] = np.nan
                result["dow_correlation"] = np.nan
                result["dow_has_volume"] = False
        else:
            result["dow_trend"] = np.nan
            result["dow_correlation"] = np.nan
            result["dow_has_volume"] = False

        return result

    def _sma(self, series: pd.Series, period: int) -> pd.Series:
        """Calculate Simple Moving Average."""
        return series.rolling(window=period).mean()

    def _ema(self, series: pd.Series, period: int) -> pd.Series:
        """Calculate Exponential Moving Average."""
        return series.ewm(span=period).mean()

    def _rsi(self, series: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index."""
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def _stochastic(
        self, high: pd.Series, low: pd.Series, close: pd.Series, k_period: int = 14, d_period: int = 3
    ) -> tuple:
        """Calculate Stochastic Oscillator."""
        lowest_low = low.rolling(window=k_period).min()
        highest_high = high.rolling(window=k_period).max()

        k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d_percent = k_percent.rolling(window=d_period).mean()

        return k_percent, d_percent

    def _calculate_support_resistance(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate support and resistance levels."""
        if len(data) < 20:
            return data

        # Simple support/resistance based on local extremes
        high_rolling = data["high"].rolling(window=10, center=True).max()
        low_rolling = data["low"].rolling(window=10, center=True).min()

        data["resistance"] = high_rolling
        data["support"] = low_rolling

        return data

    def get_signals(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate trading signals based on technical indicators.

        Args:
            data: DataFrame with calculated indicators

        Returns:
            Dict with trading signals and recommendations
        """
        if data.empty or len(data) < 2:
            return {}

        latest = data.iloc[-1]
        previous = data.iloc[-2]

        signals = {"overall_signal": "NEUTRAL", "strength": 0.0, "signals": []}

        score = 0
        max_score = 0

        # RSI signals
        if not pd.isna(latest["rsi"]):
            max_score += 1
            if latest["rsi"] < 30:
                signals["signals"].append("RSI oversold - potential buy signal")
                score += 1
            elif latest["rsi"] > 70:
                signals["signals"].append("RSI overbought - potential sell signal")
                score -= 1
            elif 30 <= latest["rsi"] <= 70:
                score += 0.5

        # MACD signals
        if not pd.isna(latest["macd"]) and not pd.isna(latest["macd_signal"]):
            max_score += 1
            if latest["macd"] > latest["macd_signal"] and previous["macd"] <= previous["macd_signal"]:
                signals["signals"].append("MACD bullish crossover")
                score += 1
            elif latest["macd"] < latest["macd_signal"] and previous["macd"] >= previous["macd_signal"]:
                signals["signals"].append("MACD bearish crossover")
                score -= 1
            elif latest["macd"] > latest["macd_signal"]:
                score += 0.5

        # Moving Average signals
        if not pd.isna(latest["sma_20"]) and not pd.isna(latest["sma_50"]):
            max_score += 1
            if latest["close"] > latest["sma_20"] > latest["sma_50"]:
                signals["signals"].append("Price above moving averages - bullish trend")
                score += 1
            elif latest["close"] < latest["sma_20"] < latest["sma_50"]:
                signals["signals"].append("Price below moving averages - bearish trend")
                score -= 1

        # Bollinger Bands signals
        if not pd.isna(latest["bb_lower"]) and not pd.isna(latest["bb_upper"]):
            max_score += 1
            if latest["close"] <= latest["bb_lower"]:
                signals["signals"].append("Price at lower Bollinger Band - potential bounce")
                score += 0.5
            elif latest["close"] >= latest["bb_upper"]:
                signals["signals"].append("Price at upper Bollinger Band - potential pullback")
                score -= 0.5

        # Calculate overall signal
        if max_score > 0:
            signals["strength"] = score / max_score

            if signals["strength"] > 0.6:
                signals["overall_signal"] = "BUY"
            elif signals["strength"] < -0.6:
                signals["overall_signal"] = "SELL"
            else:
                signals["overall_signal"] = "NEUTRAL"

        return signals
