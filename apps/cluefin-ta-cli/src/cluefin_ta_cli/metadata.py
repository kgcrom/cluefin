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


@dataclass(frozen=True, slots=True)
class TaxonomyMetadata:
    """Agent-facing explanation for one domain or tag."""

    name: str
    description: str
    when_to_use: str
    avoid_when: str | None = None
    related_domains: tuple[str, ...] = ()
    related_tags: tuple[str, ...] = ()


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

_DOMAIN_TAXONOMY: dict[str, TaxonomyMetadata] = {
    "portfolio-metric": TaxonomyMetadata(
        name="portfolio-metric",
        description="Portfolio-level performance metrics calculated from periodic returns.",
        when_to_use="Use when the input is a return series and the task needs performance-adjusted portfolio evaluation.",
        avoid_when="Use technical-indicator when the input is OHLCV price data rather than periodic returns.",
        related_tags=("portfolio-risk",),
    ),
    "risk-metric": TaxonomyMetadata(
        name="risk-metric",
        description="Risk metrics calculated from returns or drawdown series.",
        when_to_use="Use when the task asks about downside risk, drawdown, or loss magnitude.",
        avoid_when="Use volatility tag under technical-indicator when the task needs price-range volatility from OHLCV.",
        related_tags=("portfolio-risk",),
    ),
    "technical-indicator": TaxonomyMetadata(
        name="technical-indicator",
        description="Technical analysis indicators calculated from price, volume, or OHLCV arrays.",
        when_to_use="Use after collecting chart data from cluefin-openapi-cli and extracting arrays for indicator calculation.",
        avoid_when="Use portfolio-metric or risk-metric when the input is a return series rather than market price arrays.",
        related_tags=("moving-average", "momentum", "trend", "volatility", "volume-indicator"),
    ),
}

_TAG_TAXONOMY: dict[str, TaxonomyMetadata] = {
    "momentum": TaxonomyMetadata(
        name="momentum",
        description="Indicators that measure price momentum or overbought/oversold conditions.",
        when_to_use="Use for RSI, MACD, STOCH, and ADX-style signal generation after OHLCV collection.",
        avoid_when="Use moving-average for smoothing and trend-following averages.",
        related_domains=("technical-indicator",),
    ),
    "moving-average": TaxonomyMetadata(
        name="moving-average",
        description="Indicators that smooth close prices or derive trend signals from averages.",
        when_to_use="Use for SMA, EMA, Bollinger middle band, and MACD average components.",
        avoid_when="Use momentum when the task asks for oscillator-style overbought or oversold signals.",
        related_domains=("technical-indicator",),
    ),
    "portfolio-risk": TaxonomyMetadata(
        name="portfolio-risk",
        description="Portfolio risk or performance metrics calculated from periodic returns.",
        when_to_use="Use for MDD and Sharpe ratio workflows where the input is returns, not prices.",
        avoid_when="Use volatility when the input is OHLCV high/low/close arrays.",
        related_domains=("risk-metric", "portfolio-metric"),
    ),
    "trend": TaxonomyMetadata(
        name="trend",
        description="Indicators that help identify trend direction or trend strength.",
        when_to_use="Use for moving averages, MACD, and ADX-style trend analysis from price arrays.",
        avoid_when="Use volume-indicator when the task is primarily about price-volume confirmation.",
        related_domains=("technical-indicator",),
    ),
    "volatility": TaxonomyMetadata(
        name="volatility",
        description="Indicators that measure price range or band-based volatility from OHLCV data.",
        when_to_use="Use for ATR, Bollinger Bands, or ADX contexts when high/low/close arrays are available.",
        avoid_when="Use portfolio-risk when the task is about return-series drawdown or Sharpe ratio.",
        related_domains=("technical-indicator",),
    ),
    "volume-indicator": TaxonomyMetadata(
        name="volume-indicator",
        description="Indicators that combine price movement and volume data.",
        when_to_use="Use when the task asks whether volume confirms price movement, such as OBV analysis.",
        avoid_when="Use momentum or moving-average when volume is not part of the input data.",
        related_domains=("technical-indicator",),
    ),
}

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


def _generic_taxonomy(kind: str, name: str) -> TaxonomyMetadata:
    label = "domain" if kind == "domains" else "tag"
    return TaxonomyMetadata(
        name=name,
        description=f"Agent discovery {label} for `{name}` commands.",
        when_to_use=f"Use when a task needs commands classified by `{name}`.",
    )


def build_taxonomy_entry(*, kind: str, name: str, command_count: int, app_name: str) -> dict[str, Any]:
    """Build a JSON-safe taxonomy discovery entry."""

    catalog = _DOMAIN_TAXONOMY if kind == "domains" else _TAG_TAXONOMY
    item = catalog.get(name, _generic_taxonomy(kind, name))
    filter_name = "domain" if kind == "domains" else "tag"
    return {
        "name": item.name,
        "description": item.description,
        "when_to_use": item.when_to_use,
        "avoid_when": item.avoid_when,
        "related_domains": list(item.related_domains),
        "related_tags": list(item.related_tags),
        "example_filter": f"uv run {app_name} list --{filter_name} {name} --json",
        "command_count": command_count,
    }


def missing_taxonomy_names(*, kind: str, names: set[str]) -> set[str]:
    """Return taxonomy names that do not have explicit metadata."""

    catalog = _DOMAIN_TAXONOMY if kind == "domains" else _TAG_TAXONOMY
    return names - set(catalog)
