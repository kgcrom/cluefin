import cluefin_ta as talib
import pandas as pd


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
        result["obv"] = talib.OBV(data["close"].values, data["volume"].values)

        # Trend strength and volatility
        result["adx"] = talib.ADX(data["high"].values, data["low"].values, data["close"].values, timeperiod=14)
        result["atr"] = talib.ATR(data["high"].values, data["low"].values, data["close"].values, timeperiod=14)

        # Support and Resistance levels
        result = self._calculate_support_resistance(result)

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
