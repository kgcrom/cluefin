"""
Market Regime Detection - Statistical methods for identifying market states.

Functions:
    REGIME_MA: Moving Average-based regime detection
    REGIME_MA_DURATION: Calculate regime duration
    REGIME_VOLATILITY: Volatility-based regime detection
    REGIME_COMBINED: Combined trend and volatility regime detection

Regime States:
    0: Bear Market (Fast MA < Slow MA and diverging)
    1: Sideways Market (Fast MA ≈ Slow MA)
    2: Bull Market (Fast MA > Slow MA and diverging)
"""

import numpy as np

from cluefin_ta.overlap import SMA
from cluefin_ta.volatility import NATR

__all__ = [
    "REGIME_MA",
    "REGIME_MA_DURATION",
    "REGIME_VOLATILITY",
    "REGIME_COMBINED",
    "REGIME_HMM",
    "REGIME_HMM_RETURNS",
]


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


def REGIME_VOLATILITY(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    atr_period: int = 14,
    threshold_percentile: int = 66,
) -> np.ndarray:
    """
    Volatility-based Market Regime Detection.

    Classifies market into low/high volatility regimes based on NATR:
    - 0 (Low Volatility): NATR below threshold percentile
    - 1 (High Volatility): NATR above threshold percentile

    Uses Normalized ATR (NATR) to measure volatility as a percentage of price,
    making it comparable across different price levels.

    Args:
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices
        atr_period: ATR calculation period (default: 14)
        threshold_percentile: Percentile for high/low volatility split (default: 66)
                            66 means top 34% is high volatility

    Returns:
        Array of volatility regime (0/1) with NaN for initial periods

    Examples:
        >>> import numpy as np
        >>> from cluefin_ta import REGIME_VOLATILITY
        >>>
        >>> # Sample OHLC data
        >>> high = np.array([105, 108, 112, 110, 115])
        >>> low = np.array([95, 98, 102, 100, 105])
        >>> close = np.array([100, 105, 110, 108, 112])
        >>>
        >>> regime = REGIME_VOLATILITY(high, low, close, atr_period=3, threshold_percentile=50)
        >>> # Returns 0 or 1 for low/high volatility

    Notes:
        - First valid value appears at index (atr_period)
        - Higher threshold_percentile means more restrictive high volatility classification
        - NATR is used instead of ATR to normalize across different price levels
    """
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    # Calculate NATR (Normalized ATR as percentage)
    natr = NATR(high, low, close, timeperiod=atr_period)

    # Get valid NATR values (non-NaN)
    valid_natr = natr[~np.isnan(natr)]

    if len(valid_natr) == 0:
        # No valid data, return all NaN
        return np.full(n, np.nan)

    # Calculate threshold based on percentile
    threshold = np.percentile(valid_natr, threshold_percentile)

    # Classify regime: High volatility (1) if above threshold, Low volatility (0) otherwise
    regime = np.where(natr > threshold, 1, 0)

    # Preserve NaN values from NATR calculation
    regime = np.where(np.isnan(natr), np.nan, regime)

    return regime


def REGIME_COMBINED(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    fast_period: int = 20,
    slow_period: int = 50,
    atr_period: int = 14,
    sideways_threshold: float = 0.02,
    vol_percentile: int = 66,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Combined Trend and Volatility Regime Detection.

    Combines MA-based trend regime with volatility regime to create
    a comprehensive market state classification.

    Args:
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices
        fast_period: Fast MA period for trend detection (default: 20)
        slow_period: Slow MA period for trend detection (default: 50)
        atr_period: ATR period for volatility detection (default: 14)
        sideways_threshold: Threshold for sideways trend (default: 0.02)
        vol_percentile: Percentile for volatility classification (default: 66)

    Returns:
        Tuple of (trend_regime, volatility_regime, combined_regime)

        trend_regime: 0=Bear, 1=Sideways, 2=Bull
        volatility_regime: 0=Low Vol, 1=High Vol
        combined_regime: Combined encoding (0-5):
            0: Bear + Low Vol
            1: Bear + High Vol
            2: Sideways + Low Vol
            3: Sideways + High Vol
            4: Bull + Low Vol
            5: Bull + High Vol

    Examples:
        >>> import numpy as np
        >>> from cluefin_ta import REGIME_COMBINED
        >>>
        >>> # Uptrend with increasing volatility
        >>> high = np.linspace(105, 205, 100)
        >>> low = np.linspace(95, 195, 100)
        >>> close = np.linspace(100, 200, 100)
        >>>
        >>> trend, vol, combined = REGIME_COMBINED(high, low, close)
        >>> # trend: mostly 2 (Bull)
        >>> # vol: 0 or 1 based on volatility
        >>> # combined: 4 or 5 (Bull + Low/High Vol)

    Notes:
        - Combined regime provides 6 distinct market states
        - Encoding: combined = trend * 2 + volatility
        - NaN values are preserved where either component is NaN
    """
    # Calculate trend regime using MA crossover
    trend_regime = REGIME_MA(
        close, fast_period=fast_period, slow_period=slow_period, sideways_threshold=sideways_threshold
    )

    # Calculate volatility regime using NATR
    vol_regime = REGIME_VOLATILITY(high, low, close, atr_period=atr_period, threshold_percentile=vol_percentile)

    # Combine regimes: trend * 2 + volatility
    # This creates 6 possible states (0-5)
    combined = trend_regime * 2 + vol_regime

    # Preserve NaN if either component is NaN
    combined = np.where(np.isnan(trend_regime) | np.isnan(vol_regime), np.nan, combined)

    return trend_regime, vol_regime, combined


def REGIME_HMM_RETURNS(close: np.ndarray) -> np.ndarray:
    """
    Prepare returns for HMM regime detection.

    Calculates percentage returns from closing prices.
    Returns are used as input for HMM-based regime detection.

    Args:
        close: Array of closing prices

    Returns:
        Array of percentage returns with NaN for first value

    Examples:
        >>> import numpy as np
        >>> from cluefin_ta import REGIME_HMM_RETURNS
        >>>
        >>> prices = np.array([100, 102, 105, 103, 107])
        >>> returns = REGIME_HMM_RETURNS(prices)
        >>> print(returns)
        [nan 0.02 0.02941176 -0.01904762 0.03883495]
        >>>
        >>> # First value is always NaN (no previous price for return calculation)

    Notes:
        - Returns are calculated as: (price[i] - price[i-1]) / price[i-1]
        - First element is always NaN (no previous price available)
        - Handles division by zero gracefully
    """
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    if n < 2:
        return np.full(n, np.nan)

    # Initialize returns array with NaN
    returns = np.full(n, np.nan)

    # Calculate percentage returns: (close[i] - close[i-1]) / close[i-1]
    # Equivalent to: close[i] / close[i-1] - 1
    with np.errstate(divide="ignore", invalid="ignore"):
        returns[1:] = np.diff(close) / close[:-1]

    return returns


def REGIME_HMM(
    returns: np.ndarray,
    n_states: int = 3,
    covariance_type: str = "full",
    n_iter: int = 100,
    random_state: int = 42,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Hidden Markov Model-based Regime Detection.

    Uses Gaussian HMM to identify hidden market regimes from returns data.
    The model automatically learns regime characteristics (means, variances, transitions)
    from historical data without manual threshold setting.

    Args:
        returns: Array of price returns (use REGIME_HMM_RETURNS to prepare)
        n_states: Number of hidden states/regimes (default: 3)
                 Typically 3 for Bull/Neutral/Bear
        covariance_type: HMM covariance type (default: "full")
                        Options: "full", "diag", "spherical", "tied"
        n_iter: Maximum HMM training iterations (default: 100)
        random_state: Random seed for reproducibility (default: 42)

    Returns:
        Tuple of (regime_states, transition_probs, state_means)

        regime_states: Array of regime states (0 to n_states-1)
                      Sorted by mean return: 0=Bear (lowest), 1=Neutral, 2=Bull (highest)
        transition_probs: State transition probability matrix (n_states x n_states)
                         Element [i,j] = P(state j at t+1 | state i at t)
        state_means: Mean return for each state, sorted ascending
                    Useful for interpreting what each state represents

    Examples:
        >>> import numpy as np
        >>> from cluefin_ta import REGIME_HMM, REGIME_HMM_RETURNS
        >>>
        >>> # Create price data with regime changes
        >>> prices = np.concatenate(
        ...     [
        ...         100 + np.cumsum(np.random.normal(-0.01, 0.02, 50)),  # Bear
        ...         100 + np.cumsum(np.random.normal(0.02, 0.02, 50)),  # Bull
        ...     ]
        ... )
        >>>
        >>> # Prepare returns
        >>> returns = REGIME_HMM_RETURNS(prices)
        >>>
        >>> # Detect regimes
        >>> states, trans_probs, means = REGIME_HMM(returns, n_states=3)
        >>>
        >>> print(f"State means: {means}")  # Shows avg return for each regime
        >>> print(f"Current regime: {states[-1]}")  # Last detected regime
        >>> print(f"Transition probs shape: {trans_probs.shape}")  # (3, 3)

    Raises:
        ImportError: If hmmlearn is not installed

    Notes:
        - Requires hmmlearn library: `uv add --optional hmm hmmlearn`
        - Minimum data requirement: 2 * n_states samples
        - States are automatically sorted by mean return for interpretability
        - NaN values in returns are handled by fitting on valid data only
        - Returns NaN arrays if insufficient valid data
        - Transition probabilities can be used to predict regime persistence
    """
    # Check if hmmlearn is available
    try:
        from hmmlearn import hmm
    except ImportError as e:
        raise ImportError(
            "hmmlearn is required for HMM regime detection. "
            "Install with: uv add --optional hmm hmmlearn\n"
            "Or for development: uv sync --group dev"
        ) from e

    returns = np.asarray(returns, dtype=np.float64)
    n = len(returns)

    # Handle insufficient data
    if n < 2 * n_states:
        # Not enough data for reliable HMM
        return (np.full(n, np.nan), np.full((n_states, n_states), np.nan), np.full(n_states, np.nan))

    # Remove NaN values for HMM fitting
    valid_mask = ~np.isnan(returns)
    valid_returns = returns[valid_mask]

    if len(valid_returns) < 2 * n_states:
        # Not enough valid data
        return (np.full(n, np.nan), np.full((n_states, n_states), np.nan), np.full(n_states, np.nan))

    # Reshape for hmmlearn (expects 2D array: [n_samples, n_features])
    valid_returns_2d = valid_returns.reshape(-1, 1)

    # Fit Gaussian HMM
    try:
        model = hmm.GaussianHMM(
            n_components=n_states,
            covariance_type=covariance_type,
            n_iter=n_iter,
            random_state=random_state,
        )

        model.fit(valid_returns_2d)

        # Predict hidden states
        hidden_states = model.predict(valid_returns_2d)

    except Exception as e:
        # HMM fitting failed (convergence issues, etc.)
        import warnings

        warnings.warn(f"HMM fitting failed: {e}. Returning NaN.", UserWarning, stacklevel=2)
        return (np.full(n, np.nan), np.full((n_states, n_states), np.nan), np.full(n_states, np.nan))

    # Map hidden states back to original array (with NaN preserved)
    regime_states = np.full(n, np.nan)
    regime_states[valid_mask] = hidden_states

    # Extract transition probabilities and state means
    transition_probs = model.transmat_
    state_means = model.means_.flatten()

    # Sort states by mean return (Bear=0, Neutral=1, Bull=2)
    # This makes interpretation easier and consistent
    sorted_indices = np.argsort(state_means)

    # Create mapping from old states to new sorted states
    state_mapping = np.empty(n_states, dtype=int)
    state_mapping[sorted_indices] = np.arange(n_states)

    # Remap regime states to sorted order
    regime_states_valid = regime_states[valid_mask]
    regime_states[valid_mask] = state_mapping[regime_states_valid.astype(int)]

    # Rearrange transition matrix and means to match sorted states
    transition_probs = transition_probs[sorted_indices][:, sorted_indices]
    state_means = state_means[sorted_indices]

    return regime_states, transition_probs, state_means
