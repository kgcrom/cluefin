"""Technical analysis handlers using cluefin-ta library.

All TA methods have requires_session=False since they operate on raw data arrays.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from cluefin_rpc.handlers._base import rpc_method

if TYPE_CHECKING:
    from cluefin_rpc.dispatcher import Dispatcher


def _to_array(data: list) -> np.ndarray:
    """Convert a list of numbers to a numpy float64 array."""
    return np.array(data, dtype=np.float64)


def _to_json(arr: np.ndarray) -> list:
    """Convert numpy array to JSON-safe list, replacing NaN/Inf with None."""
    return [None if (np.isnan(v) or np.isinf(v)) else round(float(v), 6) for v in arr]


# ---------------------------------------------------------------------------
# Overlap / Moving Averages
# ---------------------------------------------------------------------------


@rpc_method(
    name="ta.sma",
    description="Simple Moving Average.",
    parameters={
        "type": "object",
        "properties": {
            "close": {"type": "array", "items": {"type": "number"}, "description": "Close prices"},
            "timeperiod": {"type": "integer", "description": "Number of periods. Default 14."},
        },
        "required": ["close"],
    },
    returns={"type": "object", "properties": {"values": {"type": "array"}}},
    category="ta",
    requires_session=False,
)
def handle_sma(params: dict) -> dict:
    from cluefin_ta import SMA

    close = _to_array(params["close"])
    period = params.get("timeperiod", 14)
    result = SMA(close, timeperiod=period)
    return {"values": _to_json(result)}


@rpc_method(
    name="ta.ema",
    description="Exponential Moving Average.",
    parameters={
        "type": "object",
        "properties": {
            "close": {"type": "array", "items": {"type": "number"}, "description": "Close prices"},
            "timeperiod": {"type": "integer", "description": "Number of periods. Default 14."},
        },
        "required": ["close"],
    },
    returns={"type": "object", "properties": {"values": {"type": "array"}}},
    category="ta",
    requires_session=False,
)
def handle_ema(params: dict) -> dict:
    from cluefin_ta import EMA

    close = _to_array(params["close"])
    period = params.get("timeperiod", 14)
    result = EMA(close, timeperiod=period)
    return {"values": _to_json(result)}


# ---------------------------------------------------------------------------
# Momentum
# ---------------------------------------------------------------------------


@rpc_method(
    name="ta.rsi",
    description="Relative Strength Index.",
    parameters={
        "type": "object",
        "properties": {
            "close": {"type": "array", "items": {"type": "number"}, "description": "Close prices"},
            "timeperiod": {"type": "integer", "description": "Number of periods. Default 14."},
        },
        "required": ["close"],
    },
    returns={"type": "object", "properties": {"values": {"type": "array"}}},
    category="ta",
    requires_session=False,
)
def handle_rsi(params: dict) -> dict:
    from cluefin_ta import RSI

    close = _to_array(params["close"])
    period = params.get("timeperiod", 14)
    result = RSI(close, timeperiod=period)
    return {"values": _to_json(result)}


@rpc_method(
    name="ta.macd",
    description="Moving Average Convergence/Divergence.",
    parameters={
        "type": "object",
        "properties": {
            "close": {"type": "array", "items": {"type": "number"}, "description": "Close prices"},
            "fastperiod": {"type": "integer", "description": "Fast period. Default 12."},
            "slowperiod": {"type": "integer", "description": "Slow period. Default 26."},
            "signalperiod": {"type": "integer", "description": "Signal period. Default 9."},
        },
        "required": ["close"],
    },
    returns={
        "type": "object",
        "properties": {
            "macd": {"type": "array"},
            "signal": {"type": "array"},
            "histogram": {"type": "array"},
        },
    },
    category="ta",
    requires_session=False,
)
def handle_macd(params: dict) -> dict:
    from cluefin_ta import MACD

    close = _to_array(params["close"])
    fast = params.get("fastperiod", 12)
    slow = params.get("slowperiod", 26)
    signal = params.get("signalperiod", 9)
    macd, macd_signal, macd_hist = MACD(close, fastperiod=fast, slowperiod=slow, signalperiod=signal)
    return {
        "macd": _to_json(macd),
        "signal": _to_json(macd_signal),
        "histogram": _to_json(macd_hist),
    }


@rpc_method(
    name="ta.bbands",
    description="Bollinger Bands.",
    parameters={
        "type": "object",
        "properties": {
            "close": {"type": "array", "items": {"type": "number"}, "description": "Close prices"},
            "timeperiod": {"type": "integer", "description": "Number of periods. Default 20."},
            "nbdevup": {"type": "number", "description": "Upper band std dev. Default 2."},
            "nbdevdn": {"type": "number", "description": "Lower band std dev. Default 2."},
        },
        "required": ["close"],
    },
    returns={
        "type": "object",
        "properties": {
            "upper": {"type": "array"},
            "middle": {"type": "array"},
            "lower": {"type": "array"},
        },
    },
    category="ta",
    requires_session=False,
)
def handle_bbands(params: dict) -> dict:
    from cluefin_ta import BBANDS

    close = _to_array(params["close"])
    period = params.get("timeperiod", 20)
    nbdevup = params.get("nbdevup", 2.0)
    nbdevdn = params.get("nbdevdn", 2.0)
    upper, middle, lower = BBANDS(close, timeperiod=period, nbdevup=nbdevup, nbdevdn=nbdevdn)
    return {
        "upper": _to_json(upper),
        "middle": _to_json(middle),
        "lower": _to_json(lower),
    }


@rpc_method(
    name="ta.stoch",
    description="Stochastic Oscillator.",
    parameters={
        "type": "object",
        "properties": {
            "high": {"type": "array", "items": {"type": "number"}, "description": "High prices"},
            "low": {"type": "array", "items": {"type": "number"}, "description": "Low prices"},
            "close": {"type": "array", "items": {"type": "number"}, "description": "Close prices"},
            "fastk_period": {"type": "integer", "description": "Fast K period. Default 14."},
            "slowk_period": {"type": "integer", "description": "Slow K period. Default 3."},
            "slowd_period": {"type": "integer", "description": "Slow D period. Default 3."},
        },
        "required": ["high", "low", "close"],
    },
    returns={
        "type": "object",
        "properties": {
            "slowk": {"type": "array"},
            "slowd": {"type": "array"},
        },
    },
    category="ta",
    requires_session=False,
)
def handle_stoch(params: dict) -> dict:
    from cluefin_ta import STOCH

    high = _to_array(params["high"])
    low = _to_array(params["low"])
    close = _to_array(params["close"])
    fastk = params.get("fastk_period", 14)
    slowk = params.get("slowk_period", 3)
    slowd = params.get("slowd_period", 3)
    slowk_arr, slowd_arr = STOCH(high, low, close, fastk_period=fastk, slowk_period=slowk, slowd_period=slowd)
    return {
        "slowk": _to_json(slowk_arr),
        "slowd": _to_json(slowd_arr),
    }


@rpc_method(
    name="ta.adx",
    description="Average Directional Movement Index.",
    parameters={
        "type": "object",
        "properties": {
            "high": {"type": "array", "items": {"type": "number"}, "description": "High prices"},
            "low": {"type": "array", "items": {"type": "number"}, "description": "Low prices"},
            "close": {"type": "array", "items": {"type": "number"}, "description": "Close prices"},
            "timeperiod": {"type": "integer", "description": "Number of periods. Default 14."},
        },
        "required": ["high", "low", "close"],
    },
    returns={"type": "object", "properties": {"values": {"type": "array"}}},
    category="ta",
    requires_session=False,
)
def handle_adx(params: dict) -> dict:
    from cluefin_ta import ADX

    high = _to_array(params["high"])
    low = _to_array(params["low"])
    close = _to_array(params["close"])
    period = params.get("timeperiod", 14)
    result = ADX(high, low, close, timeperiod=period)
    return {"values": _to_json(result)}


# ---------------------------------------------------------------------------
# Volatility
# ---------------------------------------------------------------------------


@rpc_method(
    name="ta.atr",
    description="Average True Range.",
    parameters={
        "type": "object",
        "properties": {
            "high": {"type": "array", "items": {"type": "number"}, "description": "High prices"},
            "low": {"type": "array", "items": {"type": "number"}, "description": "Low prices"},
            "close": {"type": "array", "items": {"type": "number"}, "description": "Close prices"},
            "timeperiod": {"type": "integer", "description": "Number of periods. Default 14."},
        },
        "required": ["high", "low", "close"],
    },
    returns={"type": "object", "properties": {"values": {"type": "array"}}},
    category="ta",
    requires_session=False,
)
def handle_atr(params: dict) -> dict:
    from cluefin_ta import ATR

    high = _to_array(params["high"])
    low = _to_array(params["low"])
    close = _to_array(params["close"])
    period = params.get("timeperiod", 14)
    result = ATR(high, low, close, timeperiod=period)
    return {"values": _to_json(result)}


# ---------------------------------------------------------------------------
# Volume
# ---------------------------------------------------------------------------


@rpc_method(
    name="ta.obv",
    description="On Balance Volume.",
    parameters={
        "type": "object",
        "properties": {
            "close": {"type": "array", "items": {"type": "number"}, "description": "Close prices"},
            "volume": {"type": "array", "items": {"type": "number"}, "description": "Volume data"},
        },
        "required": ["close", "volume"],
    },
    returns={"type": "object", "properties": {"values": {"type": "array"}}},
    category="ta",
    requires_session=False,
)
def handle_obv(params: dict) -> dict:
    from cluefin_ta import OBV

    close = _to_array(params["close"])
    volume = _to_array(params["volume"])
    result = OBV(close, volume)
    return {"values": _to_json(result)}


# ---------------------------------------------------------------------------
# Portfolio
# ---------------------------------------------------------------------------


@rpc_method(
    name="ta.mdd",
    description="Maximum Drawdown. Returns a scalar value.",
    parameters={
        "type": "object",
        "properties": {
            "returns": {"type": "array", "items": {"type": "number"}, "description": "Return series"},
        },
        "required": ["returns"],
    },
    returns={"type": "object", "properties": {"value": {"type": "number"}}},
    category="ta",
    requires_session=False,
)
def handle_mdd(params: dict) -> dict:
    from cluefin_ta import MDD

    returns = _to_array(params["returns"])
    result = MDD(returns)
    val = float(result)
    if np.isnan(val) or np.isinf(val):
        val = None
    return {"value": val}


@rpc_method(
    name="ta.sharpe",
    description="Sharpe Ratio. Returns a scalar value.",
    parameters={
        "type": "object",
        "properties": {
            "returns": {"type": "array", "items": {"type": "number"}, "description": "Return series"},
            "risk_free_rate": {"type": "number", "description": "Risk-free rate. Default 0.0."},
            "periods_per_year": {"type": "integer", "description": "Trading periods per year. Default 252."},
        },
        "required": ["returns"],
    },
    returns={"type": "object", "properties": {"value": {"type": "number"}}},
    category="ta",
    requires_session=False,
)
def handle_sharpe(params: dict) -> dict:
    from cluefin_ta import SHARPE

    returns = _to_array(params["returns"])
    rfr = params.get("risk_free_rate", 0.0)
    periods = params.get("periods_per_year", 252)
    result = SHARPE(returns, risk_free_rate=rfr, periods_per_year=periods)
    val = float(result)
    if np.isnan(val) or np.isinf(val):
        val = None
    return {"value": val}


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

_ALL_HANDLERS = [
    handle_sma,
    handle_ema,
    handle_rsi,
    handle_macd,
    handle_bbands,
    handle_stoch,
    handle_adx,
    handle_atr,
    handle_obv,
    handle_mdd,
    handle_sharpe,
]


def register_ta_handlers(dispatcher: Dispatcher) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
