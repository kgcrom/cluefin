from __future__ import annotations

import math

import pytest

from cluefin_ta_cli.registry import Registry

# Enough data points for TA-Lib lookback windows to produce values.
_CLOSE = [float(100 + (i % 7) - 3) for i in range(60)]
_HIGH = [c + 2.0 for c in _CLOSE]
_LOW = [c - 2.0 for c in _CLOSE]
_VOLUME = [1000.0 + i * 10 for i in range(60)]
_RETURNS = [0.01, -0.02, 0.015, 0.0, -0.01, 0.03, -0.005, 0.02, -0.015, 0.01]


def _invoke(name: str, params: dict) -> dict:
    registry = Registry()
    command = registry.resolve_command(("ta", name))
    assert command is not None
    return registry.invoke_command(command, params)


@pytest.mark.parametrize(
    ("name", "params", "expected_keys"),
    [
        ("sma", {"close": _CLOSE}, {"values"}),
        ("ema", {"close": _CLOSE}, {"values"}),
        ("rsi", {"close": _CLOSE}, {"values"}),
        ("macd", {"close": _CLOSE}, {"macd", "signal", "histogram"}),
        ("bbands", {"close": _CLOSE}, {"upper", "middle", "lower"}),
        ("stoch", {"high": _HIGH, "low": _LOW, "close": _CLOSE}, {"slowk", "slowd"}),
        ("adx", {"high": _HIGH, "low": _LOW, "close": _CLOSE}, {"values"}),
        ("atr", {"high": _HIGH, "low": _LOW, "close": _CLOSE}, {"values"}),
        ("obv", {"close": _CLOSE, "volume": _VOLUME}, {"values"}),
        ("mdd", {"returns": _RETURNS}, {"value"}),
        ("sharpe", {"returns": _RETURNS}, {"value"}),
    ],
)
def test_indicator_handlers_return_expected_keys(name, params, expected_keys) -> None:
    result = _invoke(name, params)
    assert set(result) == expected_keys


def test_handlers_honor_custom_periods() -> None:
    sma = _invoke("sma", {"close": _CLOSE, "timeperiod": 5})
    assert any(value is not None for value in sma["values"])

    macd = _invoke(
        "macd",
        {"close": _CLOSE, "fastperiod": 5, "slowperiod": 10, "signalperiod": 3},
    )
    assert len(macd["macd"]) == len(_CLOSE)


def test_scalar_handlers_return_finite_numbers() -> None:
    mdd = _invoke("mdd", {"returns": _RETURNS})
    assert mdd["value"] is not None and math.isfinite(mdd["value"])

    sharpe = _invoke("sharpe", {"returns": _RETURNS, "risk_free_rate": 0.01, "periods_per_year": 252})
    assert sharpe["value"] is None or math.isfinite(sharpe["value"])
