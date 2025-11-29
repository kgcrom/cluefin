"""
Volume Indicators - ta-lib compatible implementations.

Functions:
    OBV: On Balance Volume
    AD: Accumulation/Distribution Line
"""

import numpy as np

from cluefin_ta._core import get_impl


def OBV(close: np.ndarray, volume: np.ndarray) -> np.ndarray:
    """
    On Balance Volume.

    OBV is a cumulative indicator that adds volume on up days
    and subtracts volume on down days.

    Args:
        close: Array of closing prices
        volume: Array of volume data

    Returns:
        Array of OBV values
    """
    close = np.asarray(close, dtype=np.float64)
    volume = np.asarray(volume, dtype=np.float64)
    n = len(close)

    if n < 2:
        result = np.zeros(n, dtype=np.float64)
        if n >= 1:
            result[0] = volume[0]
        return result

    # Use optimized implementation
    impl = get_impl()
    return impl.obv_loop(close, volume)


def AD(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
) -> np.ndarray:
    """
    Accumulation/Distribution Line (Chaikin A/D Line).

    AD = Previous AD + Money Flow Volume
    where Money Flow Volume = Money Flow Multiplier * Volume
    and Money Flow Multiplier = ((Close - Low) - (High - Close)) / (High - Low)

    Args:
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices
        volume: Array of volume data

    Returns:
        Array of A/D values
    """
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    close = np.asarray(close, dtype=np.float64)
    volume = np.asarray(volume, dtype=np.float64)
    n = len(close)

    if n < 1:
        return np.zeros(n, dtype=np.float64)

    # Use optimized implementation
    impl = get_impl()
    return impl.ad_loop(high, low, close, volume)


__all__ = ["OBV", "AD"]
