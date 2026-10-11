"""
Momentum Indicators - ta-lib compatible implementations.

Functions:
    RSI: Relative Strength Index
    MACD: Moving Average Convergence/Divergence
    STOCH: Stochastic Oscillator
    STOCHF: Fast Stochastic Oscillator
    WILLR: Williams' %R
    MOM: Momentum
    ROC: Rate of Change
    CCI: Commodity Channel Index
    MFI: Money Flow Index
    ADX: Average Directional Index
"""

import numpy as np

from cluefin_ta._core import adx_loop, mfi_loop, rolling_minmax, wilder_smooth
from cluefin_ta.overlap import SMA, _ema_from, _require_sma


def _fast_k(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int) -> np.ndarray:
    """Stochastic Fast %K, shared by STOCH and STOCHF. 50 (neutral) when the window has no range."""
    highest_high, lowest_low = rolling_minmax(high, low, period)
    span = highest_high - lowest_low
    with np.errstate(divide="ignore", invalid="ignore"):
        fastk = np.where(span != 0, 100.0 * (close - lowest_low) / span, 50.0)
    fastk[: period - 1] = np.nan
    return fastk


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

    # Calculate first RSI value (ta-lib returns 0 when there is no movement at all)
    if avg_gain == 0 and avg_loss == 0:
        result[timeperiod] = 0.0
    elif avg_loss == 0:
        result[timeperiod] = 100.0
    else:
        rs = avg_gain / avg_loss
        result[timeperiod] = 100.0 - (100.0 / (1.0 + rs))

    # Use Wilder's smoothing for gains and losses
    smoothed_gains = wilder_smooth(gains, timeperiod, avg_gain, timeperiod - 1)
    smoothed_losses = wilder_smooth(losses, timeperiod, avg_loss, timeperiod - 1)

    # Calculate RSI from smoothed values (starting from timeperiod+1)
    for i in range(timeperiod + 1, n):
        if smoothed_gains[i - 1] == 0 and smoothed_losses[i - 1] == 0:
            result[i] = 0.0
        elif smoothed_losses[i - 1] == 0:
            result[i] = 100.0
        else:
            rs = smoothed_gains[i - 1] / smoothed_losses[i - 1]
            result[i] = 100.0 - (100.0 / (1.0 + rs))

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

    # ta-lib swaps the periods rather than producing a negated MACD
    if slowperiod < fastperiod:
        fastperiod, slowperiod = slowperiod, fastperiod

    # Both EMAs start at the slow EMA's first bar (ta-lib seeds the fast one there too,
    # from the fastperiod bars ending at that index), and all three outputs start once
    # the signal EMA has its first value.
    start = slowperiod - 1
    first = start + signalperiod - 1
    if n <= first:
        nan_arr = np.full(n, np.nan)
        return nan_arr, nan_arr.copy(), nan_arr.copy()

    macd = _ema_from(close, fastperiod, start) - _ema_from(close, slowperiod, start)
    signal = np.full(n, np.nan)
    signal[start:] = _ema_from(macd[start:], signalperiod, signalperiod - 1)
    macd[:first] = np.nan
    hist = macd - signal

    return macd, signal, hist


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
        slowk_matype: Slow %K MA type - only 0 (SMA) is supported
        slowd_period: Slow %D period (default: 3)
        slowd_matype: Slow %D MA type - only 0 (SMA) is supported

    Returns:
        Tuple of (slowk, slowd)

    Raises:
        ValueError: If slowk_matype or slowd_matype is not 0
    """
    _require_sma("slowk_matype", slowk_matype)
    _require_sma("slowd_matype", slowd_matype)
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    slowk = np.full(n, np.nan)
    slowd = np.full(n, np.nan)

    if n < fastk_period:
        return slowk, slowd

    fastk = _fast_k(high, low, close, fastk_period)

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

    highest_high, lowest_low = rolling_minmax(high, low, timeperiod)
    span = highest_high - lowest_low
    with np.errstate(divide="ignore", invalid="ignore"):
        # -50 (neutral) when the window has no range
        result = np.where(span != 0, -100.0 * (highest_high - close) / span, -50.0)
    result[: timeperiod - 1] = np.nan

    return result


def STOCHF(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    fastk_period: int = 5,
    fastd_period: int = 3,
    fastd_matype: int = 0,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Fast Stochastic Oscillator.

    Args:
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices
        fastk_period: Fast %K period (default: 5)
        fastd_period: Fast %D period (default: 3)
        fastd_matype: Fast %D MA type - only 0 (SMA) is supported

    Returns:
        Tuple of (fastk, fastd)

    Raises:
        ValueError: If fastd_matype is not 0
    """
    _require_sma("fastd_matype", fastd_matype)
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    fastk = np.full(n, np.nan)
    fastd = np.full(n, np.nan)

    if n < fastk_period:
        return fastk, fastd

    fastk = _fast_k(high, low, close, fastk_period)

    # Calculate Fast %D (SMA of Fast %K)
    valid_start = fastk_period - 1
    for i in range(valid_start + fastd_period - 1, n):
        window = fastk[i - fastd_period + 1 : i + 1]
        fastd[i] = np.mean(window)

    return fastk, fastd


def MOM(close: np.ndarray, timeperiod: int = 10) -> np.ndarray:
    """
    Momentum.

    MOM = close - close[timeperiod ago]

    Args:
        close: Array of closing prices
        timeperiod: Number of periods (default: 10)

    Returns:
        Array of Momentum values with NaN for initial periods
    """
    close = np.asarray(close, dtype=np.float64)
    n = len(close)
    result = np.full(n, np.nan)

    if n <= timeperiod:
        return result

    # Momentum = current price - price n periods ago
    result[timeperiod:] = close[timeperiod:] - close[:-timeperiod]

    return result


def ROC(close: np.ndarray, timeperiod: int = 10) -> np.ndarray:
    """
    Rate of Change.

    ROC = ((close - close[timeperiod ago]) / close[timeperiod ago]) * 100

    Args:
        close: Array of closing prices
        timeperiod: Number of periods (default: 10)

    Returns:
        Array of ROC values (percentage) with NaN for initial periods
    """
    close = np.asarray(close, dtype=np.float64)
    n = len(close)
    result = np.full(n, np.nan)

    if n <= timeperiod:
        return result

    # ROC = ((current - past) / past) * 100
    past_prices = close[:-timeperiod]
    current_prices = close[timeperiod:]

    # Avoid division by zero
    with np.errstate(divide="ignore", invalid="ignore"):
        result[timeperiod:] = ((current_prices - past_prices) / past_prices) * 100.0

    return result


def CCI(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    timeperiod: int = 14,
) -> np.ndarray:
    """
    Commodity Channel Index.

    CCI = (TP - SMA(TP)) / (0.015 * Mean Deviation)

    Args:
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices
        timeperiod: Number of periods (default: 14)

    Returns:
        Array of CCI values with NaN for initial periods
    """
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    result = np.full(n, np.nan)

    if n < timeperiod:
        return result

    # Typical Price
    tp = (high + low + close) / 3.0

    # SMA of Typical Price
    tp_sma = SMA(tp, timeperiod)

    # Mean Deviation (average of |TP - SMA(TP)|)
    for i in range(timeperiod - 1, n):
        window = tp[i - timeperiod + 1 : i + 1]
        mean_tp = tp_sma[i]
        mean_dev = np.mean(np.abs(window - mean_tp))

        if mean_dev != 0:
            result[i] = (tp[i] - mean_tp) / (0.015 * mean_dev)
        else:
            result[i] = 0.0

    return result


def MFI(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    timeperiod: int = 14,
) -> np.ndarray:
    """
    Money Flow Index.

    Volume-weighted RSI.

    Args:
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices
        volume: Array of volume data
        timeperiod: Number of periods (default: 14)

    Returns:
        Array of MFI values (0-100) with NaN for initial periods
    """
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    close = np.asarray(close, dtype=np.float64)
    volume = np.asarray(volume, dtype=np.float64)
    n = len(close)

    if n < timeperiod + 1:
        return np.full(n, np.nan)

    # Typical Price
    tp = (high + low + close) / 3.0

    return mfi_loop(tp, volume, timeperiod)


def ADX(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    timeperiod: int = 14,
) -> np.ndarray:
    """
    Average Directional Index.

    Measures trend strength (0-100), not trend direction.

    Args:
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices
        timeperiod: Number of periods (default: 14)

    Returns:
        Array of ADX values (0-100) with NaN for initial periods
    """
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    close = np.asarray(close, dtype=np.float64)

    return adx_loop(high, low, close, timeperiod)


__all__ = ["RSI", "MACD", "STOCH", "STOCHF", "WILLR", "MOM", "ROC", "CCI", "MFI", "ADX"]
