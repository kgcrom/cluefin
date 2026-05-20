from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class CommandMetadata:
    """Agent discovery metadata for one broker command."""

    domains: tuple[str, ...]
    tags: tuple[str, ...]
    use_cases: tuple[str, ...] = ()
    examples: tuple[dict[str, Any], ...] = ()
    agent_notes: str | None = None
    required_credentials: tuple[str, ...] = ()
    side_effect: str = "read"


_BROKER_CREDENTIALS: dict[str, tuple[str, ...]] = {
    "dart": ("DART_AUTH_KEY",),
    "kis": ("KIS_APP_KEY", "KIS_SECRET_KEY"),
    "kiwoom": ("KIWOOM_APP_KEY", "KIWOOM_SECRET_KEY"),
}

_CATEGORY_DEFAULTS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "analysis": (("trading-flow", "market"), ("foreign", "institution")),
    "chart": (("chart",), ("ohlcv",)),
    "dart": (("news", "statements"), ("disclosure",)),
    "etf": (("etf", "market"), ("current-price",)),
    "financial": (("statements",), ("financial-statement", "financial-ratio")),
    "market": (("market",), ("market-calendar",)),
    "program": (("trading-flow", "market"), ("program-trading",)),
    "ranking": (("market",), ("ranking",)),
    "schedule": (("corporate-actions", "market-calendar"), ("announcement",)),
    "sector": (("sector", "market"), ("sector-index",)),
    "stock": (("quote", "market"), ("current-price",)),
    "theme": (("theme", "market"), ("theme-group",)),
}

_COMMAND_OVERRIDES: dict[tuple[str, str, str], tuple[tuple[str, ...], tuple[str, ...]]] = {
    ("dart", "dart", "disclosure-search"): (("news", "statements"), ("disclosure",)),
    ("dart", "dart", "company-overview"): (("statements",), ("disclosure", "shareholder")),
    ("dart", "dart", "corp-code-lookup"): (("market",), ("disclosure",)),
    ("dart", "dart", "major-shareholder"): (("statements",), ("shareholder", "disclosure")),
    ("kis", "market", "announcement"): (("news", "market"), ("announcement", "disclosure")),
    ("kis", "market", "holiday"): (("market-calendar", "market"), ("market-calendar",)),
    ("kis", "market", "futures-business-day"): (("market-calendar", "market"), ("market-calendar",)),
    ("kis", "schedule", "dividend"): (("corporate-actions",), ("dividend", "announcement")),
    ("kiwoom", "theme", "group"): (("theme", "market"), ("theme-group",)),
}

_TAG_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("daily", ("daily",)),
    ("minute", ("minute",)),
    ("tick", ("tick",)),
    ("current-price", ("current-price",)),
    ("order-book", ("order-book",)),
    ("conclusion", ("conclusion",)),
    ("overtime", ("overtime",)),
    ("balance-sheet", ("financial-statement",)),
    ("income-statement", ("financial-statement",)),
    ("ratio", ("financial-ratio",)),
    ("profitability", ("financial-ratio",)),
    ("stability", ("financial-ratio",)),
    ("growth", ("financial-ratio",)),
    ("dividend", ("dividend",)),
    ("shareholder", ("shareholder",)),
    ("foreign", ("foreign",)),
    ("foreigner", ("foreign",)),
    ("institution", ("institution",)),
    ("investor", ("foreign", "institution")),
    ("program", ("program-trading",)),
    ("volume", ("volume-rank",)),
    ("market-cap", ("market-cap",)),
    ("market-value", ("market-cap",)),
    ("short-selling", ("short-selling",)),
    ("loan", ("short-selling",)),
    ("credit", ("credit",)),
    ("sector", ("sector-index",)),
    ("industry", ("sector-index",)),
    ("theme", ("theme-group",)),
    ("ipo", ("ipo",)),
    ("capital-increase", ("capital-increase",)),
    ("capital-reduction", ("capital-reduction",)),
    ("merger-split", ("merger-split",)),
    ("shareholder-meeting", ("shareholder-meeting",)),
)

_DOMAIN_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("announcement", ("news",)),
    ("disclosure", ("news",)),
    ("financial", ("statements",)),
    ("balance-sheet", ("statements",)),
    ("income-statement", ("statements",)),
    ("ratio", ("statements",)),
    ("dividend", ("corporate-actions",)),
    ("shareholder", ("statements",)),
    ("foreign", ("trading-flow",)),
    ("foreigner", ("trading-flow",)),
    ("institution", ("trading-flow",)),
    ("investor", ("trading-flow",)),
    ("program", ("trading-flow",)),
    ("sector", ("sector",)),
    ("industry", ("sector",)),
    ("theme", ("theme",)),
    ("ipo", ("corporate-actions",)),
    ("capital", ("corporate-actions",)),
    ("merger", ("corporate-actions",)),
    ("split", ("corporate-actions",)),
    ("meeting", ("corporate-actions",)),
)


def _append_unique(values: list[str], new_values: tuple[str, ...]) -> None:
    for value in new_values:
        if value not in values:
            values.append(value)


def get_command_metadata(*, broker: str, category: str, name: str) -> CommandMetadata:
    """Return domain/tag metadata for a generated CLI command."""

    domains: list[str] = []
    tags: list[str] = []

    default_domains, default_tags = _CATEGORY_DEFAULTS.get(category, (("market",), ("ranking",)))
    _append_unique(domains, default_domains)
    _append_unique(tags, default_tags)

    override = _COMMAND_OVERRIDES.get((broker, category, name))
    if override is not None:
        override_domains, override_tags = override
        domains = []
        tags = []
        _append_unique(domains, override_domains)
        _append_unique(tags, override_tags)

    haystack = f"{broker}.{category}.{name}"
    for keyword, keyword_domains in _DOMAIN_KEYWORDS:
        if keyword in haystack:
            _append_unique(domains, keyword_domains)
    for keyword, keyword_tags in _TAG_KEYWORDS:
        if keyword in haystack:
            _append_unique(tags, keyword_tags)

    return CommandMetadata(
        domains=tuple(domains),
        tags=tuple(tags),
        required_credentials=_BROKER_CREDENTIALS.get(broker, ()),
    )


def _sample_value(field_name: str, schema: dict[str, Any]) -> Any:
    if "default" in schema:
        return schema["default"]
    if "enum" in schema and schema["enum"]:
        return schema["enum"][0]

    schema_type = schema.get("type", "string")
    if schema_type == "integer":
        return 1
    if schema_type == "number":
        return 1.0
    if schema_type == "boolean":
        return False
    if schema_type == "array":
        return []

    lowered = field_name.lower()
    if "date" in lowered or lowered.endswith("_dt") or lowered.endswith("ymd"):
        return "20250101"
    if "corp_code" in lowered:
        return "00126380"
    if "stock_code" in lowered or "code" in lowered or "iscd" in lowered:
        return "005930"
    if "market" in lowered:
        return "J"
    return "value"


def build_command_examples(path_segments: tuple[str, ...], parameters: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    """Build one JSON-first executable command skeleton from a command schema."""

    command = " ".join(("uv run cluefin-openapi-cli", *path_segments))
    properties = parameters.get("properties", {})
    required = parameters.get("required", [])
    sample_params = {field: _sample_value(field, properties.get(field, {})) for field in required}

    if sample_params:
        params_json = json.dumps(sample_params, ensure_ascii=False, separators=(",", ":"))
        command = f"{command} --params-json '{params_json}' --json"
    else:
        command = f"{command} --json"

    return (
        {
            "description": "Run this command with JSON output.",
            "command": command,
        },
    )


def build_agent_notes(*, broker: str, category: str, name: str, required_credentials: tuple[str, ...]) -> str:
    """Build concise command-use guidance for agents."""

    credential_note = ", ".join(required_credentials) if required_credentials else "configured broker credentials"
    base = f"Read-only {broker.upper()} command. Use --json for machine-readable output. Requires {credential_note}."

    if category == "chart":
        return f"{base} Use chart output as provider-normalized market data before calculating technical indicators."
    if category == "financial":
        return f"{base} Use for statements and financial ratios; confirm fiscal period fields in the response."
    if category == "schedule":
        return f"{base} Use for corporate-action and market-calendar event discovery."
    if category in {"analysis", "program"} or "investor" in name:
        return f"{base} Use for trading-flow analysis; check date and market parameters before comparing providers."
    if category == "ranking":
        return f"{base} Use for market screening; ranking criteria are provider-specific."
    if category == "market" and name == "announcement":
        return f"{base} Use with DART disclosure search when a disclosure/news workflow needs cross-provider context."
    return base
