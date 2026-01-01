"""
Market Regime Detection - Statistical methods for identifying market states.

Functions:
    REGIME_MA: Moving Average-based regime detection
    REGIME_MA_DURATION: Calculate regime duration

Regime States:
    0: Bear Market (Fast MA < Slow MA and diverging)
    1: Sideways Market (Fast MA ≈ Slow MA)
    2: Bull Market (Fast MA > Slow MA and diverging)
"""

import numpy as np

from cluefin_ta.overlap import SMA

__all__ = ["REGIME_MA", "REGIME_MA_DURATION"]


def REGIME_MA(
    close: np.ndarray,
    fast_period: int = 20,
    slow_period: int = 50,
    sideways_threshold: float = 0.02,
) -> np.ndarray:
    """
    Moving Average-based Market Regime Detection.

    Detects three regime states based on MA crossover:
    - 0 (Bear): Fast MA < Slow MA and diverging (pct_diff < -threshold)
    - 1 (Sideways): Fast MA ≈ Slow MA (|pct_diff| <= threshold)
    - 2 (Bull): Fast MA > Slow MA and diverging (pct_diff > threshold)

    Args:
        close: Array of closing prices
        fast_period: Fast moving average period (default: 20)
        slow_period: Slow moving average period (default: 50)
        sideways_threshold: Threshold for sideways regime as percentage difference (default: 0.02 = 2%)

    Returns:
        Array of regime states (0/1/2) with NaN for initial periods

    Examples:
        >>> import numpy as np
        >>> from cluefin_ta import REGIME_MA
        >>>
        >>> # Uptrend data
        >>> prices = np.linspace(100, 200, 100)
        >>> regimes = REGIME_MA(prices, fast_period=20, slow_period=50)
        >>> # Most values should be 2 (Bull) after initial NaN period
        >>>
        >>> # Constant prices
        >>> prices = np.full(100, 150.0)
        >>> regimes = REGIME_MA(prices)
        >>> # Should be 1 (Sideways) after initial NaN period

    Notes:
        - First valid value appears at index (slow_period - 1)
        - Initial values before slow_period are NaN
        - Handles division by zero (constant prices) by defaulting to Sideways (1)
    """
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    # Return all NaN if insufficient data
    if n < slow_period:
        return np.full(n, np.nan)

    # Calculate moving averages
    fast_ma = SMA(close, timeperiod=fast_period)
    slow_ma = SMA(close, timeperiod=slow_period)

    # Calculate percentage difference: (fast - slow) / slow
    # Use errstate to suppress divide-by-zero and invalid warnings
    with np.errstate(divide="ignore", invalid="ignore"):
        pct_diff = (fast_ma - slow_ma) / slow_ma

    # Initialize regime array with NaN
    regime = np.full(n, np.nan)

    # Classify regimes based on percentage difference
    # Bull: pct_diff > threshold
    regime = np.where(pct_diff > sideways_threshold, 2, regime)

    # Bear: pct_diff < -threshold
    regime = np.where(pct_diff < -sideways_threshold, 0, regime)

    # Sideways: |pct_diff| <= threshold
    regime = np.where(np.abs(pct_diff) <= sideways_threshold, 1, regime)

    # Handle edge case: constant prices (slow_ma = 0 causes division by zero)
    # Default to Sideways regime
    regime = np.where(slow_ma == 0, 1, regime)

    return regime


def REGIME_MA_DURATION(regime_states: np.ndarray) -> np.ndarray:
    """
    Calculate duration (number of consecutive days) in current regime.

    Counts how many consecutive days the market has been in the current regime state.
    Resets to 1 when regime changes.

    Args:
        regime_states: Array of regime states from REGIME_MA (values: 0, 1, 2, or NaN)

    Returns:
        Array of regime duration counts with same length as input

    Examples:
        >>> import numpy as np
        >>> from cluefin_ta import REGIME_MA_DURATION
        >>>
        >>> # Example regime sequence: Bull(3 days), Sideways(2 days), Bear(4 days)
        >>> regimes = np.array([2, 2, 2, 1, 1, 0, 0, 0, 0], dtype=float)
        >>> durations = REGIME_MA_DURATION(regimes)
        >>> print(durations)
        [1. 2. 3. 1. 2. 1. 2. 3. 4.]
        >>>
        >>> # With NaN values
        >>> regimes = np.array([np.nan, np.nan, 2, 2, 1], dtype=float)
        >>> durations = REGIME_MA_DURATION(regimes)
        >>> print(durations)
        [nan nan 1. 2. 1.]

    Notes:
        - Duration resets to 1 when regime changes
        - NaN values in input produce NaN in output at same position
        - First occurrence of any regime has duration = 1
    """
    regime_states = np.asarray(regime_states, dtype=np.float64)
    n = len(regime_states)
    durations = np.full(n, np.nan)

    current_regime = np.nan
    counter = 0

    for i in range(n):
        if np.isnan(regime_states[i]):
            # Preserve NaN in output
            durations[i] = np.nan
        elif np.isnan(current_regime) or regime_states[i] != current_regime:
            # Regime changed or first valid value
            current_regime = regime_states[i]
            counter = 1
            durations[i] = counter
        else:
            # Same regime continues
            counter += 1
            durations[i] = counter

    return durations
