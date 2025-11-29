"""
Pure NumPy implementations of low-level technical analysis computations.

These functions are used when Numba is not available.
All functions are designed to match Numba-accelerated versions exactly.
"""

import numpy as np


def ema_loop(close: np.ndarray, period: int, alpha: float, initial_sma: float) -> np.ndarray:
    """
    EMA calculation loop.

    Args:
        close: Array of closing prices
        period: EMA period
        alpha: Smoothing factor (2 / (period + 1))
        initial_sma: Initial SMA value for first EMA

    Returns:
        Array of EMA values with NaN for initial periods
    """
    n = len(close)
    result = np.full(n, np.nan)
    result[period - 1] = initial_sma

    for i in range(period, n):
        result[i] = alpha * close[i] + (1 - alpha) * result[i - 1]

    return result


def rolling_std(data: np.ndarray, period: int) -> np.ndarray:
    """
    Rolling standard deviation (population).

    Args:
        data: Input data array
        period: Window size

    Returns:
        Array of rolling std values with NaN for initial periods
    """
    n = len(data)
    result = np.full(n, np.nan)

    for i in range(period - 1, n):
        window = data[i - period + 1 : i + 1]
        result[i] = np.std(window, ddof=0)

    return result


def wilder_smooth(values: np.ndarray, period: int, initial_value: float, start_idx: int) -> np.ndarray:
    """
    Wilder's smoothing method.

    Used by RSI and ATR for smoothed averages.

    Args:
        values: Input values to smooth
        period: Smoothing period
        initial_value: Initial value (typically SMA of first period)
        start_idx: Starting index for smoothed values

    Returns:
        Array of smoothed values with NaN for initial periods
    """
    n = len(values)
    result = np.full(n, np.nan)
    result[start_idx] = initial_value

    for i in range(start_idx + 1, n):
        result[i] = (result[i - 1] * (period - 1) + values[i]) / period

    return result


def rolling_minmax(high: np.ndarray, low: np.ndarray, period: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Rolling highest high and lowest low.

    Args:
        high: Array of high prices
        low: Array of low prices
        period: Window size

    Returns:
        Tuple of (highest_high, lowest_low) arrays
    """
    n = len(high)
    highest = np.full(n, np.nan)
    lowest = np.full(n, np.nan)

    for i in range(period - 1, n):
        highest[i] = np.max(high[i - period + 1 : i + 1])
        lowest[i] = np.min(low[i - period + 1 : i + 1])

    return highest, lowest


def true_range_loop(high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
    """
    True Range calculation loop.

    Args:
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices

    Returns:
        Array of True Range values with NaN for first element
    """
    n = len(close)
    result = np.full(n, np.nan)

    for i in range(1, n):
        hl = high[i] - low[i]
        hc = abs(high[i] - close[i - 1])
        lc = abs(low[i] - close[i - 1])
        result[i] = max(hl, hc, lc)

    return result


def obv_loop(close: np.ndarray, volume: np.ndarray) -> np.ndarray:
    """
    On Balance Volume calculation loop.

    Args:
        close: Array of closing prices
        volume: Array of volume data

    Returns:
        Array of OBV values
    """
    n = len(close)
    result = np.zeros(n, dtype=np.float64)
    result[0] = volume[0]

    for i in range(1, n):
        if close[i] > close[i - 1]:
            result[i] = result[i - 1] + volume[i]
        elif close[i] < close[i - 1]:
            result[i] = result[i - 1] - volume[i]
        else:
            result[i] = result[i - 1]

    return result


def ad_loop(high: np.ndarray, low: np.ndarray, close: np.ndarray, volume: np.ndarray) -> np.ndarray:
    """
    Accumulation/Distribution calculation loop.

    Args:
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices
        volume: Array of volume data

    Returns:
        Array of A/D values
    """
    n = len(close)
    result = np.zeros(n, dtype=np.float64)

    for i in range(n):
        hl_range = high[i] - low[i]

        if hl_range != 0:
            mfm = ((close[i] - low[i]) - (high[i] - close[i])) / hl_range
        else:
            mfm = 0.0

        mfv = mfm * volume[i]

        if i == 0:
            result[i] = mfv
        else:
            result[i] = result[i - 1] + mfv

    return result


def kama_loop(
    close: np.ndarray,
    period: int,
    fast_sc: float,
    slow_sc: float,
) -> np.ndarray:
    """
    Kaufman Adaptive Moving Average calculation loop.

    Args:
        close: Array of closing prices
        period: Efficiency ratio period
        fast_sc: Fast smoothing constant (2 / (fast + 1))
        slow_sc: Slow smoothing constant (2 / (slow + 1))

    Returns:
        Array of KAMA values with NaN for initial periods
    """
    n = len(close)
    result = np.full(n, np.nan)

    if n < period:
        return result

    # First KAMA value is the first close price after enough data
    result[period - 1] = close[period - 1]

    for i in range(period, n):
        # Change = |close - close[period ago]|
        change = abs(close[i] - close[i - period])

        # Volatility = sum of |close - prev_close| over period
        volatility = 0.0
        for j in range(i - period + 1, i + 1):
            volatility += abs(close[j] - close[j - 1])

        # Efficiency Ratio
        if volatility != 0:
            er = change / volatility
        else:
            er = 0.0

        # Smoothing Constant: SC = (ER * (fast_sc - slow_sc) + slow_sc)^2
        sc = (er * (fast_sc - slow_sc) + slow_sc) ** 2

        # KAMA = prev_KAMA + SC * (close - prev_KAMA)
        result[i] = result[i - 1] + sc * (close[i] - result[i - 1])

    return result


def dx_loop(
    high: np.ndarray,
    low: np.ndarray,
    prev_close: np.ndarray,
    period: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Directional Index calculation loop for ADX.

    Calculates +DI, -DI, and DX using Wilder's smoothing.

    Args:
        high: Array of high prices
        low: Array of low prices
        prev_close: Array of previous close prices (close shifted by 1)
        period: Smoothing period

    Returns:
        Tuple of (+DI, -DI, DX) arrays
    """
    n = len(high)
    plus_di = np.full(n, np.nan)
    minus_di = np.full(n, np.nan)
    dx = np.full(n, np.nan)

    if n < period + 1:
        return plus_di, minus_di, dx

    # Calculate +DM, -DM, and TR
    plus_dm = np.zeros(n)
    minus_dm = np.zeros(n)
    tr = np.zeros(n)

    for i in range(1, n):
        up_move = high[i] - high[i - 1]
        down_move = low[i - 1] - low[i]

        if up_move > down_move and up_move > 0:
            plus_dm[i] = up_move
        if down_move > up_move and down_move > 0:
            minus_dm[i] = down_move

        # True Range
        hl = high[i] - low[i]
        hc = abs(high[i] - prev_close[i])
        lc = abs(low[i] - prev_close[i])
        tr[i] = max(hl, hc, lc)

    # Wilder smoothing for +DM, -DM, TR
    smooth_plus_dm = np.full(n, np.nan)
    smooth_minus_dm = np.full(n, np.nan)
    smooth_tr = np.full(n, np.nan)

    # Initialize with sum of first 'period' values
    smooth_plus_dm[period] = np.sum(plus_dm[1 : period + 1])
    smooth_minus_dm[period] = np.sum(minus_dm[1 : period + 1])
    smooth_tr[period] = np.sum(tr[1 : period + 1])

    # Wilder smoothing
    for i in range(period + 1, n):
        smooth_plus_dm[i] = smooth_plus_dm[i - 1] - (smooth_plus_dm[i - 1] / period) + plus_dm[i]
        smooth_minus_dm[i] = smooth_minus_dm[i - 1] - (smooth_minus_dm[i - 1] / period) + minus_dm[i]
        smooth_tr[i] = smooth_tr[i - 1] - (smooth_tr[i - 1] / period) + tr[i]

    # Calculate +DI, -DI
    for i in range(period, n):
        if smooth_tr[i] != 0:
            plus_di[i] = 100.0 * smooth_plus_dm[i] / smooth_tr[i]
            minus_di[i] = 100.0 * smooth_minus_dm[i] / smooth_tr[i]
        else:
            plus_di[i] = 0.0
            minus_di[i] = 0.0

        # Calculate DX
        di_sum = plus_di[i] + minus_di[i]
        if di_sum != 0:
            dx[i] = 100.0 * abs(plus_di[i] - minus_di[i]) / di_sum
        else:
            dx[i] = 0.0

    return plus_di, minus_di, dx


def mfi_loop(
    typical_price: np.ndarray,
    volume: np.ndarray,
    period: int,
) -> np.ndarray:
    """
    Money Flow Index calculation loop.

    Args:
        typical_price: Array of typical prices ((H+L+C)/3)
        volume: Array of volume data
        period: MFI period

    Returns:
        Array of MFI values (0-100) with NaN for initial periods
    """
    n = len(typical_price)
    result = np.full(n, np.nan)

    if n < period + 1:
        return result

    # Raw money flow
    raw_mf = typical_price * volume

    for i in range(period, n):
        pos_mf = 0.0
        neg_mf = 0.0

        for j in range(i - period + 1, i + 1):
            if typical_price[j] > typical_price[j - 1]:
                pos_mf += raw_mf[j]
            elif typical_price[j] < typical_price[j - 1]:
                neg_mf += raw_mf[j]

        if neg_mf != 0:
            mf_ratio = pos_mf / neg_mf
            result[i] = 100.0 - (100.0 / (1.0 + mf_ratio))
        else:
            result[i] = 100.0

    return result


__all__ = [
    "ema_loop",
    "rolling_std",
    "wilder_smooth",
    "rolling_minmax",
    "true_range_loop",
    "obv_loop",
    "ad_loop",
    "kama_loop",
    "dx_loop",
    "mfi_loop",
]
