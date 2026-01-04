"""
Dow Theory Implementation - Classical technical analysis trend detection.

This module provides helper functions for Dow Theory trend analysis based on
swing high/low patterns, volume confirmation, and index correlation.

Internal Functions (not exported):
    _detect_swing_points: Identify swing highs and lows
    _classify_trend_from_swings: Classify trend from swing patterns
    _check_volume_confirmation: Check volume confirmation
    _apply_volume_upgrade: Upgrade trend strength with volume
    _calculate_index_correlation: Calculate index correlation
    _trend_ma_cross: Moving average crossover trend detection
"""

import numpy as np

from cluefin_ta.overlap import SMA

__all__ = ["DOW_THEORY"]


def _detect_swing_points(
    high: np.ndarray,
    low: np.ndarray,
    window: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Detect swing highs and lows using configurable window.

    A swing high occurs when high[i] is greater than all highs within
    'window' bars before and after. Similarly for swing lows.

    Args:
        high: Array of high prices
        low: Array of low prices
        window: Number of bars before/after to compare (must be >= 1)

    Returns:
        Tuple of (swing_high_mask, swing_high_values, swing_low_mask, swing_low_values)
        - swing_high_mask: Boolean array marking swing high locations
        - swing_high_values: High values at swing points (NaN elsewhere)
        - swing_low_mask: Boolean array marking swing low locations
        - swing_low_values: Low values at swing points (NaN elsewhere)

    Notes:
        - Swing points can only be detected from index window to n-window-1
        - Edge bars (first/last 'window' bars) will have False masks and NaN values
        - If array length < 2*window+1, all values will be False/NaN
    """
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    n = len(high)

    # Initialize output arrays
    swing_high_mask = np.full(n, False)
    swing_high_values = np.full(n, np.nan)
    swing_low_mask = np.full(n, False)
    swing_low_values = np.full(n, np.nan)

    # Check if we have enough data
    if n < 2 * window + 1:
        return swing_high_mask, swing_high_values, swing_low_mask, swing_low_values

    # Detect swing points using sliding window
    for i in range(window, n - window):
        # Get left and right windows
        left_highs = high[i - window : i]
        right_highs = high[i + 1 : i + window + 1]
        left_lows = low[i - window : i]
        right_lows = low[i + 1 : i + window + 1]

        # Check for swing high: current high > all highs in window
        if high[i] > np.max(left_highs) and high[i] > np.max(right_highs):
            swing_high_mask[i] = True
            swing_high_values[i] = high[i]

        # Check for swing low: current low < all lows in window
        if low[i] < np.min(left_lows) and low[i] < np.min(right_lows):
            swing_low_mask[i] = True
            swing_low_values[i] = low[i]

    return swing_high_mask, swing_high_values, swing_low_mask, swing_low_values


def _classify_trend_from_swings(
    swing_high_mask: np.ndarray,
    swing_high_values: np.ndarray,
    swing_low_mask: np.ndarray,
    swing_low_values: np.ndarray,
    lookback: int,
) -> np.ndarray:
    """
    Classify trend based on swing point patterns.

    Analyzes recent swing highs and lows to determine trend direction:
    - Uptrend: Both swing highs and lows have positive slopes (higher highs, higher lows)
    - Downtrend: Both swing highs and lows have negative slopes (lower highs, lower lows)
    - Sideways: Mixed slopes or insufficient swing points

    Args:
        swing_high_mask: Boolean array marking swing high locations
        swing_high_values: High values at swing points
        swing_low_mask: Boolean array marking swing low locations
        swing_low_values: Low values at swing points
        lookback: Number of bars to look back for swing analysis

    Returns:
        Array of base trend states (-1=Bear, 0=Sideways, +1=Bull)

    Notes:
        - Requires at least 2 swing highs AND 2 swing lows within lookback
        - Uses linear regression to determine swing point slopes
        - Defaults to Sideways (0) when insufficient data
    """
    n = len(swing_high_mask)
    trend = np.full(n, 0)  # Default to sideways

    # Need at least lookback bars to start analysis
    for i in range(lookback, n):
        # Get indices of recent swing points within lookback window
        window_start = max(0, i - lookback)

        # Find swing high indices and values in window
        high_indices = np.where(swing_high_mask[window_start : i + 1])[0]
        if len(high_indices) >= 2:
            # Adjust indices to absolute position
            high_indices_abs = high_indices + window_start
            high_values = swing_high_values[high_indices_abs]

            # Remove NaN values (shouldn't happen, but be safe)
            valid_highs = ~np.isnan(high_values)
            high_indices_abs = high_indices_abs[valid_highs]
            high_values = high_values[valid_highs]
        else:
            high_indices_abs = np.array([])
            high_values = np.array([])

        # Find swing low indices and values in window
        low_indices = np.where(swing_low_mask[window_start : i + 1])[0]
        if len(low_indices) >= 2:
            # Adjust indices to absolute position
            low_indices_abs = low_indices + window_start
            low_values = swing_low_values[low_indices_abs]

            # Remove NaN values
            valid_lows = ~np.isnan(low_values)
            low_indices_abs = low_indices_abs[valid_lows]
            low_values = low_values[valid_lows]
        else:
            low_indices_abs = np.array([])
            low_values = np.array([])

        # Need at least 2 swing highs AND 2 swing lows to determine trend
        if len(high_indices_abs) >= 2 and len(low_indices_abs) >= 2:
            # Calculate slopes using linear regression
            # polyfit returns [slope, intercept], we only need slope
            high_slope = np.polyfit(high_indices_abs, high_values, 1)[0]
            low_slope = np.polyfit(low_indices_abs, low_values, 1)[0]

            # Classify trend based on slopes
            # Use small threshold to avoid noise (0.001 per bar)
            slope_threshold = 0.001

            if high_slope > slope_threshold and low_slope > slope_threshold:
                # Both slopes positive: Uptrend
                trend[i] = 1
            elif high_slope < -slope_threshold and low_slope < -slope_threshold:
                # Both slopes negative: Downtrend
                trend[i] = -1
            else:
                # Mixed or flat slopes: Sideways
                trend[i] = 0
        else:
            # Insufficient swing points: Sideways
            trend[i] = 0

    return trend


def _check_volume_confirmation(
    volume: np.ndarray | None,
    volume_ma_period: int,
) -> np.ndarray:
    """
    Check volume confirmation at each bar.

    Volume confirms a trend when current volume exceeds its moving average,
    indicating increased participation in the price movement.

    Args:
        volume: Array of volume data (or None if not available)
        volume_ma_period: Period for volume moving average

    Returns:
        Boolean array: True where volume confirms trend (volume > MA)
        Returns all False if volume is None or all NaN

    Notes:
        - Volume confirmation strengthens trend signals
        - No volume data results in no confirmation (all False)
    """
    if volume is None:
        # No volume data available
        return np.full(1, False)  # Will be broadcast to correct size by caller

    volume = np.asarray(volume, dtype=np.float64)
    n = len(volume)

    # Check if all volume is NaN
    if np.all(np.isnan(volume)):
        return np.full(n, False)

    # Calculate volume moving average
    volume_ma = SMA(volume, timeperiod=volume_ma_period)

    # Volume confirms when current volume > average volume
    with np.errstate(invalid="ignore"):
        confirmation = volume > volume_ma

    # Handle NaN: no confirmation where data is invalid
    confirmation = np.where(np.isnan(volume) | np.isnan(volume_ma), False, confirmation)

    return confirmation


def _apply_volume_upgrade(
    base_trend: np.ndarray,
    volume_confirmation: np.ndarray,
) -> np.ndarray:
    """
    Upgrade trend strength based on volume confirmation.

    Upgrades base trend from weak (±1) to strong (±2) when volume confirms.
    Sideways trends (0) are not affected by volume.

    Args:
        base_trend: Array of base trend states (-1, 0, +1)
        volume_confirmation: Boolean array indicating volume confirmation

    Returns:
        Array with upgraded trend states (-2, -1, 0, +1, +2)
        - +2: Strong Bull (bull trend with volume confirmation)
        - +1: Weak Bull (bull trend without volume confirmation)
        -  0: Sideways (unchanged)
        - -1: Weak Bear (bear trend without volume confirmation)
        - -2: Strong Bear (bear trend with volume confirmation)

    Notes:
        - Only ±1 trends can be upgraded to ±2
        - Sideways (0) trends remain unchanged
    """
    upgraded = base_trend.copy()

    # Upgrade Bull trend (+1 → +2) where volume confirms
    upgraded = np.where((base_trend == 1) & volume_confirmation, 2, upgraded)

    # Upgrade Bear trend (-1 → -2) where volume confirms
    upgraded = np.where((base_trend == -1) & volume_confirmation, -2, upgraded)

    return upgraded


def _calculate_index_correlation(
    stock_trend: np.ndarray,
    index_trend: np.ndarray,
) -> np.ndarray:
    """
    Calculate correlation between stock and index trends.

    Classical Dow Theory principle: Markets should confirm each other.
    Originally used Industrials + Transports; this implementation supports
    any stock vs reference index comparison.

    Args:
        stock_trend: Array of stock trend states (-1, 0, +1)
        index_trend: Array of index trend states (-1, 0, +1)

    Returns:
        Array of correlation states:
        - +1.0: Confirmed (both in same non-zero trend)
        - -1.0: Diverging (in opposite trends)
        -  0.0: Neutral (one or both sideways)
        -  NaN: Invalid data (NaN in either input)

    Notes:
        - Arrays must have same length
        - NaN in either input produces NaN in output
        - Sideways (0) in either produces neutral (0.0)
    """
    stock_trend = np.asarray(stock_trend, dtype=np.float64)
    index_trend = np.asarray(index_trend, dtype=np.float64)
    n = len(stock_trend)

    # Initialize with NaN
    correlation = np.full(n, np.nan)

    # Valid data mask: both trends are not NaN
    valid_mask = ~np.isnan(stock_trend) & ~np.isnan(index_trend)

    # Same non-zero direction: confirmed (+1.0)
    same_bull = (stock_trend == 1) & (index_trend == 1)
    same_bear = (stock_trend == -1) & (index_trend == -1)
    correlation = np.where(valid_mask & (same_bull | same_bear), 1.0, correlation)

    # Opposite direction: diverging (-1.0)
    bull_vs_bear = (stock_trend == 1) & (index_trend == -1)
    bear_vs_bull = (stock_trend == -1) & (index_trend == 1)
    correlation = np.where(valid_mask & (bull_vs_bear | bear_vs_bull), -1.0, correlation)

    # Either sideways: neutral (0.0)
    either_sideways = (stock_trend == 0) | (index_trend == 0)
    correlation = np.where(valid_mask & either_sideways, 0.0, correlation)

    return correlation


def _trend_ma_cross(
    close: np.ndarray,
    minor_period: int,
    secondary_period: int,
    primary_period: int,
) -> np.ndarray:
    """
    Moving average crossover trend detection.

    Alternative to swing-based trend detection using three moving averages
    representing minor, secondary, and primary trends.

    Args:
        close: Array of closing prices
        minor_period: Fast MA period (e.g., 20 for minor trend)
        secondary_period: Medium MA period (e.g., 60 for secondary trend)
        primary_period: Slow MA period (e.g., 200 for primary trend)

    Returns:
        Array of trend states (-1=Bear, 0=Sideways, +1=Bull)
        - +1: Bull (fast > medium > slow)
        - -1: Bear (fast < medium < slow)
        -  0: Sideways (any other configuration)

    Notes:
        - First valid value appears at index (primary_period - 1)
        - Requires all three MAs to be in strict order for trend signal
        - More conservative than swing-based method
    """
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    # Early return for insufficient data
    if n < primary_period:
        return np.full(n, np.nan)

    # Calculate three moving averages
    fast_ma = SMA(close, timeperiod=minor_period)
    medium_ma = SMA(close, timeperiod=secondary_period)
    slow_ma = SMA(close, timeperiod=primary_period)

    # Initialize trend array with NaN
    trend = np.full(n, np.nan)

    # Bull: fast > medium > slow
    bull_condition = (fast_ma > medium_ma) & (medium_ma > slow_ma)
    trend = np.where(bull_condition, 1, trend)

    # Bear: fast < medium < slow
    bear_condition = (fast_ma < medium_ma) & (medium_ma < slow_ma)
    trend = np.where(bear_condition, -1, trend)

    # Sideways: any other configuration (including equal values)
    # Where not bull and not bear, set to 0
    valid_mask = ~np.isnan(fast_ma) & ~np.isnan(medium_ma) & ~np.isnan(slow_ma)
    sideways_condition = valid_mask & ~bull_condition & ~bear_condition
    trend = np.where(sideways_condition, 0, trend)

    return trend


def DOW_THEORY(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray | None = None,
    index_high: np.ndarray | None = None,
    index_low: np.ndarray | None = None,
    index_close: np.ndarray | None = None,
    swing_window: int = 5,
    minor_period: int = 20,
    secondary_period: int = 60,
    primary_period: int = 200,
    volume_ma_period: int = 20,
    method: str = "swing",
) -> tuple[np.ndarray, np.ndarray]:
    """
    Dow Theory Trend Classification with Volume Confirmation.

    Classifies market trends using classical Dow Theory principles with swing
    high/low analysis, optional volume confirmation for trend strength, and
    optional index correlation for market confirmation.

    Classical Dow Theory identifies three types of trends through the analysis
    of swing points (peaks and troughs):
    - Uptrend: Higher highs and higher lows
    - Downtrend: Lower highs and lower lows
    - Sideways: Mixed or unclear pattern

    Volume confirmation validates trend strength (expanding volume in trend
    direction suggests strong trend). Index correlation checks if stock and
    market index move together (a key Dow Theory confirmation principle).

    Args:
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices
        volume: Array of volume data (optional, for trend strength confirmation)
        index_high: Reference index high prices (optional, for correlation)
        index_low: Reference index low prices (optional, for correlation)
        index_close: Reference index close prices (optional, for correlation)
        swing_window: Window size for swing point detection (default: 5)
                      Larger values detect more significant swings
        minor_period: Fast MA period for minor trend (default: 20)
        secondary_period: Medium MA period for secondary trend (default: 60)
        primary_period: Slow MA period for primary trend (default: 200)
        volume_ma_period: Period for volume moving average (default: 20)
        method: Trend detection method (default: 'swing')
                - 'swing': Classical swing high/low analysis (Dow Theory)
                - 'ma_cross': Moving average crossover (fast > med > slow)
                - 'hybrid': Consensus of both methods (both must agree)

    Returns:
        Tuple of (trend_state, correlation_state)

        trend_state: Array of trend strength states (-2 to +2)
            -2: Strong Bear (bear trend + volume confirmation)
            -1: Weak Bear (bear trend without volume confirmation)
             0: Sideways/Uncertain (no clear trend pattern)
            +1: Weak Bull (bull trend without volume confirmation)
            +2: Strong Bull (bull trend + volume confirmation)

        correlation_state: Array of stock-index correlation states
            -1.0: Diverging (stock and index in opposite trends)
             0.0: Neutral (one or both in sideways trend)
             1.0: Confirmed (stock and index in same trend direction)
             NaN: No index data provided or insufficient data

    Raises:
        ValueError: If method is not 'swing', 'ma_cross', or 'hybrid'
        ValueError: If array lengths don't match
        ValueError: If only some index arrays provided (need all or none)
        ValueError: If volume length doesn't match close length

    Examples:
        >>> import numpy as np
        >>> from cluefin_ta import DOW_THEORY
        >>>
        >>> # Example 1: Basic uptrend detection with volume
        >>> high = np.linspace(105, 205, 100)
        >>> low = np.linspace(95, 195, 100)
        >>> close = np.linspace(100, 200, 100)
        >>> volume = np.linspace(1000, 2000, 100)  # Increasing volume
        >>>
        >>> trend, corr = DOW_THEORY(high, low, close, volume=volume)
        >>> # trend: Should be +2 (Strong Bull) where volume confirms
        >>> # corr: All NaN (no index provided)
        >>>
        >>> # Example 2: With index correlation
        >>> index_high = np.linspace(1050, 1150, 100)
        >>> index_low = np.linspace(950, 1050, 100)
        >>> index_close = np.linspace(1000, 1100, 100)
        >>>
        >>> trend, corr = DOW_THEORY(
        ...     high, low, close, index_high=index_high, index_low=index_low, index_close=index_close
        ... )
        >>> # trend: +1 (Weak Bull without volume)
        >>> # corr: 1.0 (Confirmed - both stock and index trending up)
        >>>
        >>> # Example 3: Divergence detection
        >>> # Stock uptrend, index downtrend
        >>> stock_high = np.linspace(105, 205, 100)
        >>> index_high_down = np.linspace(1150, 1050, 100)
        >>> index_low_down = np.linspace(1050, 950, 100)
        >>> index_close_down = np.linspace(1100, 1000, 100)
        >>>
        >>> trend, corr = DOW_THEORY(
        ...     stock_high,
        ...     low,
        ...     close,
        ...     index_high=index_high_down,
        ...     index_low=index_low_down,
        ...     index_close=index_close_down,
        ... )
        >>> # corr: -1.0 (Diverging - stock up, index down)
        >>>
        >>> # Example 4: Using MA crossover method
        >>> trend, corr = DOW_THEORY(
        ...     high, low, close, method="ma_cross", minor_period=20, secondary_period=60, primary_period=200
        ... )
        >>> # Uses MA crossover instead of swing analysis

    Notes:
        - First valid value appears at index determined by method and parameters
        - For 'swing': requires (primary_period + swing_window * 2 + 1) bars
        - For 'ma_cross': requires primary_period bars
        - Initial values before sufficient data are NaN
        - Without volume data: returns base trends (±1, 0) without strength upgrade
        - Without index data: returns NaN for entire correlation array
        - Hybrid method defaults to sideways (0) when swing and MA disagree
        - Volume confirmation only upgrades ±1 to ±2, sideways (0) stays 0
        - Index correlation uses base trend (before volume upgrade) for comparison

    See Also:
        REGIME_MA: Moving average regime detection
        REGIME_COMBINED: Combined trend and volatility regime detection
    """
    # PHASE 1: INPUT VALIDATION
    # Convert required inputs to NumPy arrays
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    # Validate array lengths match
    if len(high) != n or len(low) != n:
        raise ValueError("high, low, and close must have same length")

    # Validate method parameter
    valid_methods = {"swing", "ma_cross", "hybrid"}
    if method not in valid_methods:
        raise ValueError(f"Invalid method '{method}'. Must be one of: {valid_methods}")

    # Handle optional volume
    if volume is not None:
        volume = np.asarray(volume, dtype=np.float64)
        if len(volume) != n:
            raise ValueError("volume length must match close length")

    # Handle optional index data (all-or-nothing)
    index_provided = False
    if index_high is not None or index_low is not None or index_close is not None:
        if not all(x is not None for x in [index_high, index_low, index_close]):
            raise ValueError("If providing index data, must provide all of: index_high, index_low, index_close")

        index_high = np.asarray(index_high, dtype=np.float64)
        index_low = np.asarray(index_low, dtype=np.float64)
        index_close = np.asarray(index_close, dtype=np.float64)

        if len(index_high) != n or len(index_low) != n or len(index_close) != n:
            raise ValueError("index arrays must have same length as stock arrays")

        index_provided = True

    # Early return for insufficient data
    if method == "swing":
        min_required = primary_period + swing_window * 2 + 1
    elif method == "ma_cross":
        min_required = primary_period
    else:  # hybrid
        min_required = max(primary_period, primary_period + swing_window * 2 + 1)

    if n < min_required:
        return np.full(n, np.nan), np.full(n, np.nan)

    # PHASE 2: CALCULATE BASE TREND (method-dependent)
    if method == "swing":
        # Swing-based detection (classical Dow Theory)
        swing_high_mask, swing_high_values, swing_low_mask, swing_low_values = _detect_swing_points(
            high, low, swing_window
        )
        base_trend = _classify_trend_from_swings(
            swing_high_mask,
            swing_high_values,
            swing_low_mask,
            swing_low_values,
            lookback=primary_period,
        )

    elif method == "ma_cross":
        # MA crossover detection
        base_trend = _trend_ma_cross(close, minor_period, secondary_period, primary_period)

    else:  # method == "hybrid"
        # Both methods with consensus logic
        swing_high_mask, swing_high_values, swing_low_mask, swing_low_values = _detect_swing_points(
            high, low, swing_window
        )
        swing_trend = _classify_trend_from_swings(
            swing_high_mask,
            swing_high_values,
            swing_low_mask,
            swing_low_values,
            lookback=primary_period,
        )
        ma_trend = _trend_ma_cross(close, minor_period, secondary_period, primary_period)

        # Consensus: both must agree, else sideways (0)
        base_trend = np.full(n, 0)
        base_trend = np.where((swing_trend == 1) & (ma_trend == 1), 1, base_trend)
        base_trend = np.where((swing_trend == -1) & (ma_trend == -1), -1, base_trend)

        # Preserve NaN where either method has NaN
        base_trend = np.where(np.isnan(swing_trend) | np.isnan(ma_trend), np.nan, base_trend)

    # PHASE 3: APPLY VOLUME CONFIRMATION
    volume_confirmation = _check_volume_confirmation(volume, volume_ma_period)

    # Handle broadcast case (when volume is None, returns single False)
    if len(volume_confirmation) == 1:
        volume_confirmation = np.full(n, False)

    # Upgrade trend strength based on volume
    trend_state = _apply_volume_upgrade(base_trend, volume_confirmation)

    # PHASE 4: CALCULATE INDEX CORRELATION
    if index_provided:
        # Calculate index trend using same method as stock
        if method == "swing":
            idx_high_mask, idx_high_vals, idx_low_mask, idx_low_vals = _detect_swing_points(
                index_high, index_low, swing_window
            )
            index_trend = _classify_trend_from_swings(
                idx_high_mask,
                idx_high_vals,
                idx_low_mask,
                idx_low_vals,
                lookback=primary_period,
            )

        elif method == "ma_cross":
            index_trend = _trend_ma_cross(index_close, minor_period, secondary_period, primary_period)

        else:  # hybrid
            # Calculate both methods for index
            idx_high_mask, idx_high_vals, idx_low_mask, idx_low_vals = _detect_swing_points(
                index_high, index_low, swing_window
            )
            idx_swing = _classify_trend_from_swings(
                idx_high_mask, idx_high_vals, idx_low_mask, idx_low_vals, lookback=primary_period
            )
            idx_ma = _trend_ma_cross(index_close, minor_period, secondary_period, primary_period)

            # Apply same consensus logic
            index_trend = np.full(n, 0)
            index_trend = np.where((idx_swing == 1) & (idx_ma == 1), 1, index_trend)
            index_trend = np.where((idx_swing == -1) & (idx_ma == -1), -1, index_trend)
            index_trend = np.where(np.isnan(idx_swing) | np.isnan(idx_ma), np.nan, index_trend)

        # Calculate correlation using base trends (before volume upgrade)
        correlation_state = _calculate_index_correlation(base_trend, index_trend)

    else:
        # No index data provided - return all NaN
        correlation_state = np.full(n, np.nan)

    # PHASE 5: RETURN RESULTS
    return trend_state, correlation_state
