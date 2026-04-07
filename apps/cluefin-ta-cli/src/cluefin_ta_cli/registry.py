from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

import numpy as np


def _to_array(data: list[float]) -> np.ndarray:
    """Convert a list of numbers to a numpy float64 array."""

    return np.array(data, dtype=np.float64)


def _to_json(arr: np.ndarray) -> list[float | None]:
    """Convert numpy array to JSON-safe list, replacing NaN/Inf with None."""

    return [None if (np.isnan(v) or np.isinf(v)) else round(float(v), 6) for v in arr]


def _to_scalar(value: float) -> float | None:
    val = float(value)
    if np.isnan(val) or np.isinf(val):
        return None
    return val


@dataclass(frozen=True, slots=True)
class CommandSpec:
    """Metadata and executor wiring for one CLI command."""

    category: str
    name: str
    description: str
    path_segments: tuple[str, ...]
    parameters: dict[str, Any] = field(default_factory=dict)
    returns: dict[str, Any] = field(default_factory=dict)
    executor: Callable[[dict[str, Any]], Any] | None = None

    @property
    def path(self) -> tuple[str, ...]:
        return self.path_segments

    @property
    def qualified_name(self) -> str:
        return ".".join(self.path_segments)


class Registry:
    """TA CLI command registry."""

    def __init__(self) -> None:
        self._commands = build_registry()

    def list_commands(self, *, category: str | None = None) -> list[CommandSpec]:
        commands = list(self._commands.values())
        if category is not None:
            commands = [command for command in commands if command.category == category]
        return sorted(commands, key=lambda command: command.path_segments)

    def resolve_command(self, path_segments: tuple[str, ...]) -> CommandSpec | None:
        return self._commands.get(path_segments)

    def invoke_command(self, command: CommandSpec, params: dict[str, Any]) -> Any:
        if command.executor is None:
            raise RuntimeError(f"Command `{command.qualified_name}` has no executor.")
        return command.executor(params)


def _spec(name: str, description: str, parameters: dict[str, Any], returns: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": name,
        "description": description,
        "parameters": parameters,
        "returns": returns,
        "category": "ta",
        "path_segments": ("ta", name),
    }


def _handle_sma(params: dict[str, Any]) -> dict[str, Any]:
    from cluefin_ta import SMA

    close = _to_array(params["close"])
    period = params.get("timeperiod", 14)
    return {"values": _to_json(SMA(close, timeperiod=period))}


def _handle_ema(params: dict[str, Any]) -> dict[str, Any]:
    from cluefin_ta import EMA

    close = _to_array(params["close"])
    period = params.get("timeperiod", 14)
    return {"values": _to_json(EMA(close, timeperiod=period))}


def _handle_rsi(params: dict[str, Any]) -> dict[str, Any]:
    from cluefin_ta import RSI

    close = _to_array(params["close"])
    period = params.get("timeperiod", 14)
    return {"values": _to_json(RSI(close, timeperiod=period))}


def _handle_macd(params: dict[str, Any]) -> dict[str, Any]:
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


def _handle_bbands(params: dict[str, Any]) -> dict[str, Any]:
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


def _handle_stoch(params: dict[str, Any]) -> dict[str, Any]:
    from cluefin_ta import STOCH

    high = _to_array(params["high"])
    low = _to_array(params["low"])
    close = _to_array(params["close"])
    fastk = params.get("fastk_period", 14)
    slowk = params.get("slowk_period", 3)
    slowd = params.get("slowd_period", 3)
    slowk_arr, slowd_arr = STOCH(high, low, close, fastk_period=fastk, slowk_period=slowk, slowd_period=slowd)
    return {"slowk": _to_json(slowk_arr), "slowd": _to_json(slowd_arr)}


def _handle_adx(params: dict[str, Any]) -> dict[str, Any]:
    from cluefin_ta import ADX

    high = _to_array(params["high"])
    low = _to_array(params["low"])
    close = _to_array(params["close"])
    period = params.get("timeperiod", 14)
    return {"values": _to_json(ADX(high, low, close, timeperiod=period))}


def _handle_atr(params: dict[str, Any]) -> dict[str, Any]:
    from cluefin_ta import ATR

    high = _to_array(params["high"])
    low = _to_array(params["low"])
    close = _to_array(params["close"])
    period = params.get("timeperiod", 14)
    return {"values": _to_json(ATR(high, low, close, timeperiod=period))}


def _handle_obv(params: dict[str, Any]) -> dict[str, Any]:
    from cluefin_ta import OBV

    close = _to_array(params["close"])
    volume = _to_array(params["volume"])
    return {"values": _to_json(OBV(close, volume))}


def _handle_mdd(params: dict[str, Any]) -> dict[str, Any]:
    from cluefin_ta import MDD

    returns = _to_array(params["returns"])
    return {"value": _to_scalar(MDD(returns))}


def _handle_sharpe(params: dict[str, Any]) -> dict[str, Any]:
    from cluefin_ta import SHARPE

    returns = _to_array(params["returns"])
    risk_free_rate = params.get("risk_free_rate", 0.0)
    periods_per_year = params.get("periods_per_year", 252)
    return {"value": _to_scalar(SHARPE(returns, risk_free=risk_free_rate, periods_per_year=periods_per_year))}


def build_registry() -> dict[tuple[str, ...], CommandSpec]:
    command_definitions = [
        (
            _spec(
                "sma",
                "Simple Moving Average.",
                {
                    "type": "object",
                    "properties": {
                        "close": {"type": "array", "items": {"type": "number"}, "description": "Close prices"},
                        "timeperiod": {"type": "integer", "description": "Number of periods. Default 14."},
                    },
                    "required": ["close"],
                },
                {"type": "object", "properties": {"values": {"type": "array"}}},
            ),
            _handle_sma,
        ),
        (
            _spec(
                "ema",
                "Exponential Moving Average.",
                {
                    "type": "object",
                    "properties": {
                        "close": {"type": "array", "items": {"type": "number"}, "description": "Close prices"},
                        "timeperiod": {"type": "integer", "description": "Number of periods. Default 14."},
                    },
                    "required": ["close"],
                },
                {"type": "object", "properties": {"values": {"type": "array"}}},
            ),
            _handle_ema,
        ),
        (
            _spec(
                "rsi",
                "Relative Strength Index.",
                {
                    "type": "object",
                    "properties": {
                        "close": {"type": "array", "items": {"type": "number"}, "description": "Close prices"},
                        "timeperiod": {"type": "integer", "description": "Number of periods. Default 14."},
                    },
                    "required": ["close"],
                },
                {"type": "object", "properties": {"values": {"type": "array"}}},
            ),
            _handle_rsi,
        ),
        (
            _spec(
                "macd",
                "Moving Average Convergence/Divergence.",
                {
                    "type": "object",
                    "properties": {
                        "close": {"type": "array", "items": {"type": "number"}, "description": "Close prices"},
                        "fastperiod": {"type": "integer", "description": "Fast period. Default 12."},
                        "slowperiod": {"type": "integer", "description": "Slow period. Default 26."},
                        "signalperiod": {"type": "integer", "description": "Signal period. Default 9."},
                    },
                    "required": ["close"],
                },
                {
                    "type": "object",
                    "properties": {
                        "macd": {"type": "array"},
                        "signal": {"type": "array"},
                        "histogram": {"type": "array"},
                    },
                },
            ),
            _handle_macd,
        ),
        (
            _spec(
                "bbands",
                "Bollinger Bands.",
                {
                    "type": "object",
                    "properties": {
                        "close": {"type": "array", "items": {"type": "number"}, "description": "Close prices"},
                        "timeperiod": {"type": "integer", "description": "Number of periods. Default 20."},
                        "nbdevup": {"type": "number", "description": "Upper band std dev. Default 2."},
                        "nbdevdn": {"type": "number", "description": "Lower band std dev. Default 2."},
                    },
                    "required": ["close"],
                },
                {
                    "type": "object",
                    "properties": {
                        "upper": {"type": "array"},
                        "middle": {"type": "array"},
                        "lower": {"type": "array"},
                    },
                },
            ),
            _handle_bbands,
        ),
        (
            _spec(
                "stoch",
                "Stochastic Oscillator.",
                {
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
                {"type": "object", "properties": {"slowk": {"type": "array"}, "slowd": {"type": "array"}}},
            ),
            _handle_stoch,
        ),
        (
            _spec(
                "adx",
                "Average Directional Movement Index.",
                {
                    "type": "object",
                    "properties": {
                        "high": {"type": "array", "items": {"type": "number"}, "description": "High prices"},
                        "low": {"type": "array", "items": {"type": "number"}, "description": "Low prices"},
                        "close": {"type": "array", "items": {"type": "number"}, "description": "Close prices"},
                        "timeperiod": {"type": "integer", "description": "Number of periods. Default 14."},
                    },
                    "required": ["high", "low", "close"],
                },
                {"type": "object", "properties": {"values": {"type": "array"}}},
            ),
            _handle_adx,
        ),
        (
            _spec(
                "atr",
                "Average True Range.",
                {
                    "type": "object",
                    "properties": {
                        "high": {"type": "array", "items": {"type": "number"}, "description": "High prices"},
                        "low": {"type": "array", "items": {"type": "number"}, "description": "Low prices"},
                        "close": {"type": "array", "items": {"type": "number"}, "description": "Close prices"},
                        "timeperiod": {"type": "integer", "description": "Number of periods. Default 14."},
                    },
                    "required": ["high", "low", "close"],
                },
                {"type": "object", "properties": {"values": {"type": "array"}}},
            ),
            _handle_atr,
        ),
        (
            _spec(
                "obv",
                "On Balance Volume.",
                {
                    "type": "object",
                    "properties": {
                        "close": {"type": "array", "items": {"type": "number"}, "description": "Close prices"},
                        "volume": {"type": "array", "items": {"type": "number"}, "description": "Volume data"},
                    },
                    "required": ["close", "volume"],
                },
                {"type": "object", "properties": {"values": {"type": "array"}}},
            ),
            _handle_obv,
        ),
        (
            _spec(
                "mdd",
                "Maximum Drawdown. Returns a scalar value.",
                {
                    "type": "object",
                    "properties": {
                        "returns": {"type": "array", "items": {"type": "number"}, "description": "Return series"},
                    },
                    "required": ["returns"],
                },
                {"type": "object", "properties": {"value": {"type": "number"}}},
            ),
            _handle_mdd,
        ),
        (
            _spec(
                "sharpe",
                "Sharpe Ratio. Returns a scalar value.",
                {
                    "type": "object",
                    "properties": {
                        "returns": {"type": "array", "items": {"type": "number"}, "description": "Return series"},
                        "risk_free_rate": {"type": "number", "description": "Risk-free rate. Default 0.0."},
                        "periods_per_year": {
                            "type": "integer",
                            "description": "Trading periods per year. Default 252.",
                        },
                    },
                    "required": ["returns"],
                },
                {"type": "object", "properties": {"value": {"type": "number"}}},
            ),
            _handle_sharpe,
        ),
    ]

    registry: dict[tuple[str, ...], CommandSpec] = {}
    for definition, executor in command_definitions:
        spec = CommandSpec(
            category=definition["category"],
            name=definition["name"],
            description=definition["description"],
            path_segments=definition["path_segments"],
            parameters=definition["parameters"],
            returns=definition["returns"],
            executor=executor,
        )
        if spec.path_segments in registry:
            raise ValueError(f"Duplicate CLI path detected: {' '.join(spec.path_segments)}")
        registry[spec.path_segments] = spec
    return registry
