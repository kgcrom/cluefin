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

from cluefin_ta._core import get_impl
from cluefin_ta.overlap import EMA


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

    # Calculate first RSI value
    if avg_loss == 0:
        result[timeperiod] = 100.0
    else:
        rs = avg_gain / avg_loss
        result[timeperiod] = 100.0 - (100.0 / (1.0 + rs))

    # Use Wilder's smoothing for gains and losses
    impl = get_impl()
    smoothed_gains = impl.wilder_smooth(gains, timeperiod, avg_gain, timeperiod - 1)
    smoothed_losses = impl.wilder_smooth(losses, timeperiod, avg_loss, timeperiod - 1)

    # Calculate RSI from smoothed values (starting from timeperiod+1)
    for i in range(timeperiod + 1, n):
        if smoothed_losses[i - 1] == 0:
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

    # Get optimized rolling min/max
    impl = get_impl()
    highest_high, lowest_low = impl.rolling_minmax(high, low, fastk_period)

    # Calculate Fast %K
    fastk = np.full(n, np.nan)
    for i in range(fastk_period - 1, n):
        hh = highest_high[i]
        ll = lowest_low[i]

        if hh != ll:
            fastk[i] = 100.0 * (close[i] - ll) / (hh - ll)
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

    # Get optimized rolling min/max
    impl = get_impl()
    highest_high, lowest_low = impl.rolling_minmax(high, low, timeperiod)

    for i in range(timeperiod - 1, n):
        hh = highest_high[i]
        ll = lowest_low[i]

        if hh != ll:
            result[i] = -100.0 * (hh - close[i]) / (hh - ll)
        else:
            result[i] = -50.0  # Neutral when no range

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
        fastd_matype: Fast %D MA type (0=SMA) - only SMA supported

    Returns:
        Tuple of (fastk, fastd)
    """
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    fastk = np.full(n, np.nan)
    fastd = np.full(n, np.nan)

    if n < fastk_period:
        return fastk, fastd

    # Get optimized rolling min/max
    impl = get_impl()
    highest_high, lowest_low = impl.rolling_minmax(high, low, fastk_period)

    # Calculate Fast %K
    for i in range(fastk_period - 1, n):
        hh = highest_high[i]
        ll = lowest_low[i]

        if hh != ll:
            fastk[i] = 100.0 * (close[i] - ll) / (hh - ll)
        else:
            fastk[i] = 50.0  # Neutral when no range

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
    from cluefin_ta.overlap import SMA

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

    impl = get_impl()
    return impl.mfi_loop(tp, volume, timeperiod)


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
    n = len(close)

    result = np.full(n, np.nan)

    if n < timeperiod * 2:
        return result

    # Create prev_close array (close shifted by 1)
    prev_close = np.empty(n, dtype=np.float64)
    prev_close[0] = np.nan
    prev_close[1:] = close[:-1]

    # Get +DI, -DI, DX
    impl = get_impl()
    plus_di, minus_di, dx = impl.dx_loop(high, low, prev_close, timeperiod)

    # ADX = Wilder smoothed average of DX
    # First ADX is the average of first 'period' DX values
    first_adx_idx = timeperiod * 2 - 1
    if first_adx_idx < n:
        # Average of DX values from index 'period' to '2*period-1'
        dx_values = dx[timeperiod : first_adx_idx + 1]
        valid_dx = dx_values[~np.isnan(dx_values)]
        if len(valid_dx) > 0:
            result[first_adx_idx] = np.mean(valid_dx)

            # Wilder smoothing for subsequent ADX values
            for i in range(first_adx_idx + 1, n):
                if not np.isnan(dx[i]):
                    result[i] = (result[i - 1] * (timeperiod - 1) + dx[i]) / timeperiod

    return result


__all__ = ["RSI", "MACD", "STOCH", "STOCHF", "WILLR", "MOM", "ROC", "CCI", "MFI", "ADX"]
