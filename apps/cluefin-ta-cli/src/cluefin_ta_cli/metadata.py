from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class CommandMetadata:
    """Agent discovery metadata for one TA command."""

    domains: tuple[str, ...]
    tags: tuple[str, ...]
    use_cases: tuple[str, ...]
    examples: tuple[dict[str, Any], ...]
    agent_notes: str


def _example(name: str, params_json: str) -> tuple[dict[str, Any], ...]:
    return (
        {
            "description": f"Run {name} with inline JSON input.",
            "command": f"uv run cluefin-ta-cli ta {name} --params-json '{params_json}' --json",
        },
    )


_COMMON_PRICE_NOTE = (
    "Supply price arrays through --params-json. Indicator warm-up periods can return null values in JSON output."
)

_METADATA: dict[str, CommandMetadata] = {
    "adx": CommandMetadata(
        domains=("technical-indicator",),
        tags=("momentum", "trend", "volatility"),
        use_cases=("Measure trend strength from high/low/close OHLCV data.",),
        examples=_example("adx", '{"high":[3,4,5],"low":[1,2,3],"close":[2,3,4],"timeperiod":14}'),
        agent_notes=_COMMON_PRICE_NOTE + " Requires high, low, and close arrays of the same length.",
    ),
    "atr": CommandMetadata(
        domains=("technical-indicator",),
        tags=("volatility",),
        use_cases=("Measure price range volatility from high/low/close OHLCV data.",),
        examples=_example("atr", '{"high":[3,4,5],"low":[1,2,3],"close":[2,3,4],"timeperiod":14}'),
        agent_notes=_COMMON_PRICE_NOTE + " Requires high, low, and close arrays of the same length.",
    ),
    "bbands": CommandMetadata(
        domains=("technical-indicator",),
        tags=("volatility", "moving-average"),
        use_cases=("Calculate Bollinger Bands around a close-price series.",),
        examples=_example("bbands", '{"close":[1,2,3,4,5],"timeperiod":20,"nbdevup":2,"nbdevdn":2}'),
        agent_notes=_COMMON_PRICE_NOTE + " Use close prices ordered oldest to newest.",
    ),
    "ema": CommandMetadata(
        domains=("technical-indicator",),
        tags=("moving-average", "trend"),
        use_cases=("Smooth close prices with an exponential moving average.",),
        examples=_example("ema", '{"close":[1,2,3,4,5],"timeperiod":14}'),
        agent_notes=_COMMON_PRICE_NOTE + " Use close prices ordered oldest to newest.",
    ),
    "macd": CommandMetadata(
        domains=("technical-indicator",),
        tags=("momentum", "trend", "moving-average"),
        use_cases=("Calculate MACD, signal, and histogram values from close prices.",),
        examples=_example("macd", '{"close":[1,2,3,4,5,6],"fastperiod":12,"slowperiod":26,"signalperiod":9}'),
        agent_notes=_COMMON_PRICE_NOTE + " Use close prices ordered oldest to newest.",
    ),
    "mdd": CommandMetadata(
        domains=("risk-metric",),
        tags=("portfolio-risk",),
        use_cases=("Calculate maximum drawdown from a return series.",),
        examples=_example("mdd", '{"returns":[0.1,-0.2,0.05,-0.1]}'),
        agent_notes="Supply periodic returns through --params-json, not prices. Returns a scalar value.",
    ),
    "obv": CommandMetadata(
        domains=("technical-indicator",),
        tags=("volume-indicator",),
        use_cases=("Calculate On Balance Volume from close and volume series.",),
        examples=_example("obv", '{"close":[1,2,1.5,3],"volume":[100,120,90,150]}'),
        agent_notes=_COMMON_PRICE_NOTE + " Requires close and volume arrays of the same length.",
    ),
    "rsi": CommandMetadata(
        domains=("technical-indicator",),
        tags=("momentum",),
        use_cases=("Measure overbought or oversold momentum from close prices.",),
        examples=_example("rsi", '{"close":[1,2,3,2,4,5],"timeperiod":14}'),
        agent_notes=_COMMON_PRICE_NOTE + " Use close prices ordered oldest to newest.",
    ),
    "sharpe": CommandMetadata(
        domains=("portfolio-metric",),
        tags=("portfolio-risk",),
        use_cases=("Calculate annualized Sharpe ratio from periodic returns.",),
        examples=_example("sharpe", '{"returns":[0.01,-0.02,0.015],"risk_free_rate":0,"periods_per_year":252}'),
        agent_notes="Supply periodic returns through --params-json, not prices. Returns a scalar value.",
    ),
    "sma": CommandMetadata(
        domains=("technical-indicator",),
        tags=("moving-average", "trend"),
        use_cases=("Smooth close prices with a simple moving average.",),
        examples=_example("sma", '{"close":[1,2,3,4,5],"timeperiod":14}'),
        agent_notes=_COMMON_PRICE_NOTE + " Use close prices ordered oldest to newest.",
    ),
    "stoch": CommandMetadata(
        domains=("technical-indicator",),
        tags=("momentum",),
        use_cases=("Calculate stochastic oscillator values from high/low/close OHLCV data.",),
        examples=_example(
            "stoch",
            '{"high":[3,4,5],"low":[1,2,3],"close":[2,3,4],"fastk_period":14,"slowk_period":3,"slowd_period":3}',
        ),
        agent_notes=_COMMON_PRICE_NOTE + " Requires high, low, and close arrays of the same length.",
    ),
}


def get_command_metadata(name: str) -> CommandMetadata:
    """Return discovery metadata for a TA command name."""

    return _METADATA[name]
