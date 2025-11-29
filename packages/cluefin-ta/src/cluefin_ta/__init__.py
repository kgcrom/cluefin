"""
cluefin-ta: Pure Python technical analysis library with ta-lib compatible API.

This library provides technical analysis functions that are compatible with ta-lib,
but implemented in pure Python using NumPy for easy installation across all platforms.

Usage:
    import cluefin_ta as talib  # Drop-in replacement for ta-lib

    # Or import specific functions
    from cluefin_ta import SMA, EMA, RSI, MACD
"""

# Overlap Studies (Moving Averages)
# Momentum Indicators
from cluefin_ta.momentum import MACD, RSI, STOCH, WILLR
from cluefin_ta.overlap import BBANDS, EMA, SMA

# Pattern Recognition (Candlestick)
from cluefin_ta.pattern import CDLDOJI, CDLENGULFING, CDLHAMMER

# Volatility Indicators
from cluefin_ta.volatility import ATR, NATR, TRANGE

# Volume Indicators
from cluefin_ta.volume import AD, OBV

__version__ = "0.1.0"

__all__ = [
    # Overlap
    "SMA",
    "EMA",
    "BBANDS",
    # Momentum
    "RSI",
    "MACD",
    "STOCH",
    "WILLR",
    # Volatility
    "TRANGE",
    "ATR",
    "NATR",
    # Volume
    "OBV",
    "AD",
    # Pattern
    "CDLDOJI",
    "CDLHAMMER",
    "CDLENGULFING",
]
