"""
Overlap Studies (Moving Averages) - ta-lib compatible implementations.

Functions:
    SMA: Simple Moving Average
    EMA: Exponential Moving Average
    BBANDS: Bollinger Bands
"""

import numpy as np

from cluefin_ta._core import get_impl


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

    # Use cumsum for efficient calculation (already vectorized, no Numba needed)
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

    if n < timeperiod:
        return np.full(n, np.nan)

    # Calculate multiplier (smoothing factor)
    alpha = 2.0 / (timeperiod + 1)

    # Initialize with SMA for the first EMA value
    initial_sma = np.mean(close[:timeperiod])

    # Use optimized implementation
    impl = get_impl()
    return impl.ema_loop(close, timeperiod, alpha, initial_sma)


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

    if n < timeperiod:
        nan_arr = np.full(n, np.nan)
        return nan_arr, nan_arr.copy(), nan_arr.copy()

    # Calculate middle band (SMA)
    middle = SMA(close, timeperiod)

    # Use optimized rolling std
    impl = get_impl()
    std = impl.rolling_std(close, timeperiod)

    upper = middle + nbdevup * std
    lower = middle - nbdevdn * std

    return upper, middle, lower


__all__ = ["SMA", "EMA", "BBANDS"]
