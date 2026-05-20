from __future__ import annotations

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
