"""
Overlap Studies (Moving Averages) - ta-lib compatible implementations.

Functions:
    SMA: Simple Moving Average
    EMA: Exponential Moving Average
    BBANDS: Bollinger Bands
"""

import numpy as np


def SMA(close: np.ndarray, timeperiod: int = 30) -> np.ndarray:
    """
    Simple Moving Average.

    Args:
        close: Array of closing prices
        timeperiod: Number of periods for the moving average (default: 30)

    Returns:
        Array of SMA values with NaN for initial periods
    """
    close = np.asarray(close, dtype=np.float64)
    n = len(close)
    result = np.full(n, np.nan)

    if n < timeperiod:
        return result

    # Use cumsum for efficient calculation
    cumsum = np.cumsum(np.insert(close, 0, 0))
    result[timeperiod - 1 :] = (cumsum[timeperiod:] - cumsum[:-timeperiod]) / timeperiod

    return result


def EMA(close: np.ndarray, timeperiod: int = 30) -> np.ndarray:
    """
    Exponential Moving Average.

    Args:
        close: Array of closing prices
        timeperiod: Number of periods for the moving average (default: 30)

    Returns:
        Array of EMA values with NaN for initial periods
    """
    close = np.asarray(close, dtype=np.float64)
    n = len(close)
    result = np.full(n, np.nan)

    if n < timeperiod:
        return result

    # Calculate multiplier (smoothing factor)
    alpha = 2.0 / (timeperiod + 1)

    # Initialize with SMA for the first EMA value
    result[timeperiod - 1] = np.mean(close[:timeperiod])

    # Calculate EMA iteratively
    for i in range(timeperiod, n):
        result[i] = alpha * close[i] + (1 - alpha) * result[i - 1]

    return result


def BBANDS(
    close: np.ndarray,
    timeperiod: int = 5,
    nbdevup: float = 2.0,
    nbdevdn: float = 2.0,
    matype: int = 0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Bollinger Bands.

    Args:
        close: Array of closing prices
        timeperiod: Number of periods for the moving average (default: 5)
        nbdevup: Number of standard deviations for upper band (default: 2.0)
        nbdevdn: Number of standard deviations for lower band (default: 2.0)
        matype: Moving average type (0=SMA, 1=EMA) - currently only SMA supported

    Returns:
        Tuple of (upper_band, middle_band, lower_band)
    """
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    upper = np.full(n, np.nan)
    middle = np.full(n, np.nan)
    lower = np.full(n, np.nan)

    if n < timeperiod:
        return upper, middle, lower

    # Calculate middle band (SMA)
    middle = SMA(close, timeperiod)

    # Calculate rolling standard deviation
    for i in range(timeperiod - 1, n):
        window = close[i - timeperiod + 1 : i + 1]
        std = np.std(window, ddof=0)  # Population std (ta-lib uses ddof=0)
        upper[i] = middle[i] + nbdevup * std
        lower[i] = middle[i] - nbdevdn * std

    return upper, middle, lower


__all__ = ["SMA", "EMA", "BBANDS"]
