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

        # Moving Averages: cluefin_ta.SMA matches a plain rolling mean (desk previously
        # hand-rolled this), so it's a drop-in swap. EMA stays hand-rolled (see below).
        result["sma_5"] = talib.SMA(data["close"].values, timeperiod=5)
        result["sma_20"] = talib.SMA(data["close"].values, timeperiod=20)
        result["sma_50"] = talib.SMA(data["close"].values, timeperiod=50)
        result["sma_120"] = talib.SMA(data["close"].values, timeperiod=120)
        result["sma_240"] = talib.SMA(data["close"].values, timeperiod=240)
        result["ema_12"] = self._ema(data["close"], 12)
        result["ema_26"] = self._ema(data["close"], 26)

        # RSI: cluefin_ta.RSI uses Wilder smoothing (ta-lib's definition); this desk RSI
        # uses a plain rolling mean of gains/losses and is a survivor ML feature
        # (desk AGENTS.md), so it is kept as-is rather than switched to a different
        # indicator definition. See refactor report for the measured difference.
        result["rsi"] = self._rsi(data["close"], 14)

        # MACD: derived from the hand-rolled ema_12/26 above, so macd_histogram (a
        # survivor ML feature) keeps its current values instead of adopting
        # cluefin_ta.MACD's ta-lib-style EMA warm-up (seeded by an SMA, which differs
        # noticeably from the ewm() EMA for roughly the first 2x the slow period).
        macd_line = result["ema_12"] - result["ema_26"]
        macd_signal = self._ema(macd_line, 9)
        result["macd"] = macd_line
        result["macd_signal"] = macd_signal
        result["macd_histogram"] = macd_line - macd_signal

        # Bollinger Bands: not a survivor feature (create_talib_features overwrites
        # bb_upper/middle/lower). Kept hand-rolled because cluefin_ta.BBANDS uses a
        # population stddev (ta-lib convention) vs this rolling().std() sample stddev —
        # a real definition difference, not just floating-point noise.
        bb_middle = result["sma_20"]
        bb_std = data["close"].rolling(window=20).std()
        result["bb_middle"] = bb_middle
        result["bb_upper"] = bb_middle + (bb_std * 2)
        result["bb_lower"] = bb_middle - (bb_std * 2)

        # Stochastic Oscillator: not a survivor feature either. cluefin_ta has no plain
        # unsmoothed-%K variant with this desk's (period=14, no slow-%K smoothing)
        # shape without changing the NaN warm-up window, so kept hand-rolled.
        stoch_k, stoch_d = self._stochastic(data["high"], data["low"], data["close"])
        result["stoch_k"] = stoch_k
        result["stoch_d"] = stoch_d

        # Volume indicators
        result["volume_sma"] = talib.SMA(data["volume"].values.astype(float), timeperiod=20)
        result["obv"] = talib.OBV(data["close"].values, data["volume"].values)

        # Trend strength and volatility
        result["adx"] = talib.ADX(data["high"].values, data["low"].values, data["close"].values, timeperiod=14)
        result["atr"] = talib.ATR(data["high"].values, data["low"].values, data["close"].values, timeperiod=14)

        # Support and Resistance levels
        result = self._calculate_support_resistance(result)

        return result

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

        # Trailing 10-bar extremes. A centered window would read the next five bars — future
        # data the model never has when it predicts.
        high_rolling = data["high"].rolling(window=10).max()
        low_rolling = data["low"].rolling(window=10).min()

        data["resistance"] = high_rolling
        data["support"] = low_rolling

        return data
