"""
Momentum Indicators - ta-lib compatible implementations.

Functions:
    RSI: Relative Strength Index
    MACD: Moving Average Convergence/Divergence
    STOCH: Stochastic Oscillator
    WILLR: Williams' %R
"""

import numpy as np

from cluefin_ta.overlap import EMA, SMA


def RSI(close: np.ndarray, timeperiod: int = 14) -> np.ndarray:
    """
    Relative Strength Index.

    Args:
        close: Array of closing prices
        timeperiod: Number of periods (default: 14)

    Returns:
        Array of RSI values (0-100) with NaN for initial periods
    """
    close = np.asarray(close, dtype=np.float64)
    n = len(close)
    result = np.full(n, np.nan)

    if n < timeperiod + 1:
        return result

    # Calculate price changes
    deltas = np.diff(close)

    # Separate gains and losses
    gains = np.where(deltas > 0, deltas, 0.0)
    losses = np.where(deltas < 0, -deltas, 0.0)

    # Calculate initial average gain and loss using SMA
    avg_gain = np.mean(gains[:timeperiod])
    avg_loss = np.mean(losses[:timeperiod])

    # Calculate RSI using Wilder's smoothing method (EMA with alpha=1/timeperiod)
    if avg_loss == 0:
        result[timeperiod] = 100.0
    else:
        rs = avg_gain / avg_loss
        result[timeperiod] = 100.0 - (100.0 / (1.0 + rs))

    # Continue with smoothed averages
    for i in range(timeperiod, n - 1):
        avg_gain = (avg_gain * (timeperiod - 1) + gains[i]) / timeperiod
        avg_loss = (avg_loss * (timeperiod - 1) + losses[i]) / timeperiod

        if avg_loss == 0:
            result[i + 1] = 100.0
        else:
            rs = avg_gain / avg_loss
            result[i + 1] = 100.0 - (100.0 / (1.0 + rs))

    return result


def MACD(
    close: np.ndarray,
    fastperiod: int = 12,
    slowperiod: int = 26,
    signalperiod: int = 9,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Moving Average Convergence/Divergence.

    Args:
        close: Array of closing prices
        fastperiod: Fast EMA period (default: 12)
        slowperiod: Slow EMA period (default: 26)
        signalperiod: Signal line EMA period (default: 9)

    Returns:
        Tuple of (macd, signal, histogram)
    """
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    macd = np.full(n, np.nan)
    signal = np.full(n, np.nan)
    hist = np.full(n, np.nan)

    if n < slowperiod:
        return macd, signal, hist

    # Calculate fast and slow EMAs
    fast_ema = EMA(close, fastperiod)
    slow_ema = EMA(close, slowperiod)

    # MACD line = Fast EMA - Slow EMA
    macd = fast_ema - slow_ema

    # Calculate signal line (EMA of MACD)
    # Need to handle NaN values in MACD for signal calculation
    valid_start = slowperiod - 1
    if n >= valid_start + signalperiod:
        # Calculate EMA of valid MACD values
        macd_valid = macd[valid_start:]
        signal_ema = EMA(macd_valid, signalperiod)
        signal[valid_start:] = signal_ema

    # Histogram = MACD - Signal
    hist = macd - signal

    return macd, signal, hist


def _sma_ignore_nan(arr: np.ndarray, period: int) -> np.ndarray:
    """Simple Moving Average that handles NaN values by ignoring them in the window."""
    n = len(arr)
    result = np.full(n, np.nan)

    for i in range(period - 1, n):
        window = arr[i - period + 1 : i + 1]
        valid = window[~np.isnan(window)]
        if len(valid) >= period:
            result[i] = np.mean(valid)

    return result


def STOCH(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    fastk_period: int = 5,
    slowk_period: int = 3,
    slowk_matype: int = 0,
    slowd_period: int = 3,
    slowd_matype: int = 0,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Stochastic Oscillator.

    Args:
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices
        fastk_period: Fast %K period (default: 5)
        slowk_period: Slow %K smoothing period (default: 3)
        slowk_matype: Slow %K MA type (0=SMA) - only SMA supported
        slowd_period: Slow %D period (default: 3)
        slowd_matype: Slow %D MA type (0=SMA) - only SMA supported

    Returns:
        Tuple of (slowk, slowd)
    """
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    slowk = np.full(n, np.nan)
    slowd = np.full(n, np.nan)

    if n < fastk_period:
        return slowk, slowd

    # Calculate Fast %K
    fastk = np.full(n, np.nan)
    for i in range(fastk_period - 1, n):
        highest_high = np.max(high[i - fastk_period + 1 : i + 1])
        lowest_low = np.min(low[i - fastk_period + 1 : i + 1])

        if highest_high != lowest_low:
            fastk[i] = 100.0 * (close[i] - lowest_low) / (highest_high - lowest_low)
        else:
            fastk[i] = 50.0  # Neutral when no range

    # Calculate Slow %K (SMA of Fast %K) - ta-lib starts from first valid fastk
    valid_start = fastk_period - 1
    for i in range(valid_start + slowk_period - 1, n):
        window = fastk[i - slowk_period + 1 : i + 1]
        slowk[i] = np.mean(window)

    # Calculate Slow %D (SMA of Slow %K)
    slowk_start = valid_start + slowk_period - 1
    for i in range(slowk_start + slowd_period - 1, n):
        window = slowk[i - slowd_period + 1 : i + 1]
        slowd[i] = np.mean(window)

    return slowk, slowd


def WILLR(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    timeperiod: int = 14,
) -> np.ndarray:
    """
    Williams' %R.

    Args:
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices
        timeperiod: Number of periods (default: 14)

    Returns:
        Array of Williams %R values (-100 to 0)
    """
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    result = np.full(n, np.nan)

    if n < timeperiod:
        return result

    for i in range(timeperiod - 1, n):
        highest_high = np.max(high[i - timeperiod + 1 : i + 1])
        lowest_low = np.min(low[i - timeperiod + 1 : i + 1])

        if highest_high != lowest_low:
            result[i] = -100.0 * (highest_high - close[i]) / (highest_high - lowest_low)
        else:
            result[i] = -50.0  # Neutral when no range

    return result


__all__ = ["RSI", "MACD", "STOCH", "WILLR"]
