"""
cluefin-ta: Pure Python technical analysis library with ta-lib compatible API.

This library provides technical analysis functions that are compatible with ta-lib,
but implemented in pure Python using NumPy for easy installation across all platforms.

Usage:
    import cluefin_ta as talib  # Drop-in replacement for ta-lib

    # Or import specific functions
    from cluefin_ta import SMA, EMA, RSI, MACD
"""

from importlib.metadata import PackageNotFoundError, version

# Overlap Studies (Moving Averages)
# Momentum Indicators
from cluefin_ta.momentum import ADX, CCI, MACD, MFI, MOM, ROC, RSI, STOCH, STOCHF, WILLR
from cluefin_ta.overlap import BBANDS, DEMA, EMA, KAMA, SMA, TEMA, WMA

# Pattern Recognition (Candlestick)
from cluefin_ta.pattern import (
    CDLDARKCLOUDCOVER,
    CDLDOJI,
    CDLENGULFING,
    CDLEVENINGSTAR,
    CDLHAMMER,
    CDLHANGINGMAN,
    CDLHARAMI,
    CDLMORNINGSTAR,
    CDLPIERCING,
    CDLSHOOTINGSTAR,
)

# Portfolio Metrics
from cluefin_ta.portfolio import CAGR, CALMAR, MDD, SHARPE, SORTINO, VOLATILITY

# Regime Detection
from cluefin_ta.regime import (
    REGIME_COMBINED,
    REGIME_HMM,
    REGIME_HMM_RETURNS,
    REGIME_MA,
    REGIME_MA_DURATION,
    REGIME_VOLATILITY,
)

# Volatility Indicators
from cluefin_ta.volatility import ATR, NATR, TRANGE

# Volume Indicators
from cluefin_ta.volume import AD, ADOSC, OBV

try:
    __version__ = version("cluefin-ta")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = [
    # Overlap
    "SMA",
    "EMA",
    "WMA",
    "DEMA",
    "TEMA",
    "KAMA",
    "BBANDS",
    # Momentum
    "RSI",
    "MACD",
    "STOCH",
    "STOCHF",
    "WILLR",
    "MOM",
    "ROC",
    "CCI",
    "MFI",
    "ADX",
    # Volatility
    "TRANGE",
    "ATR",
    "NATR",
    # Volume
    "OBV",
    "AD",
    "ADOSC",
    # Pattern
    "CDLDOJI",
    "CDLHAMMER",
    "CDLENGULFING",
    "CDLSHOOTINGSTAR",
    "CDLHANGINGMAN",
    "CDLHARAMI",
    "CDLPIERCING",
    "CDLMORNINGSTAR",
    "CDLEVENINGSTAR",
    "CDLDARKCLOUDCOVER",
    # Portfolio
    "MDD",
    "CAGR",
    "VOLATILITY",
    "SHARPE",
    "SORTINO",
    "CALMAR",
    # Regime Detection
    "REGIME_MA",
    "REGIME_MA_DURATION",
    "REGIME_VOLATILITY",
    "REGIME_COMBINED",
    "REGIME_HMM",
    "REGIME_HMM_RETURNS",
]
