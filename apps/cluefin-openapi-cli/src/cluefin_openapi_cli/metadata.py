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


@dataclass(frozen=True, slots=True)
class TaxonomyMetadata:
    """Agent-facing explanation for one domain or tag."""

    name: str
    description: str
    when_to_use: str
    avoid_when: str | None = None
    related_domains: tuple[str, ...] = ()
    related_tags: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class BrokerRole:
    """Which role a broker plays in the agent-facing surface."""

    name: str
    role: str
    rank: int
    description: str
    when_to_use: str
    credentials: tuple[str, ...]
    env_var: str | None = None


_BROKER_CREDENTIALS: dict[str, tuple[str, ...]] = {
    "dart": ("DART_AUTH_KEY",),
    "kis": ("KIS_APP_KEY", "KIS_SECRET_KEY"),
    "kiwoom": ("KIWOOM_APP_KEY", "KIWOOM_SECRET_KEY"),
}

BROKER_ROLES: dict[str, BrokerRole] = {
    "kis": BrokerRole(
        name="kis",
        role="primary",
        rank=0,
        description="Korea Investment & Securities. Default source for quotes, charts, rankings, financials, "
        "sector indices, ETF data, corporate-action schedules, and the market calendar.",
        when_to_use="Start here for every task. Only fall back to another broker when `list --broker kis` "
        "has no command for the data you need.",
        credentials=_BROKER_CREDENTIALS["kis"],
        env_var="KIS_ENV",
    ),
    "kiwoom": BrokerRole(
        name="kiwoom",
        role="auxiliary",
        rank=1,
        description="Kiwoom Securities. Fills KIS gaps: theme groups, sector constituents, tick charts, "
        "program-trading detail, member (brokerage) flow, ETF intraday, and screening lists KIS lacks.",
        when_to_use="Use when a kiwoom command has an empty `kis_alternatives` list, or when the KIS "
        "equivalent returned no usable data. When `kis_alternatives` is non-empty, call the KIS command first.",
        credentials=_BROKER_CREDENTIALS["kiwoom"],
        env_var="KIWOOM_ENV",
    ),
    "dart": BrokerRole(
        name="dart",
        role="reference",
        rank=2,
        description="DART (FSS disclosure system). Formal filings, corp-code lookup, company overview, "
        "and major-shareholder data. Not a market-data source.",
        when_to_use="Use for disclosure text, filing search, and issuer registry data that no broker provides.",
        credentials=_BROKER_CREDENTIALS["dart"],
    ),
}

BROKER_ORDER: tuple[str, ...] = tuple(sorted(BROKER_ROLES, key=lambda name: BROKER_ROLES[name].rank))


def broker_rank(broker: str) -> int:
    role = BROKER_ROLES.get(broker)
    return role.rank if role is not None else len(BROKER_ROLES)


def broker_role_name(broker: str) -> str:
    role = BROKER_ROLES.get(broker)
    return role.role if role is not None else "unknown"


# Kiwoom command → KIS commands that cover the same question. An auxiliary command with
# an empty tuple here is Kiwoom-only and is the intended reason to call Kiwoom at all.
# Validated against the live registry by tests/test_agent_surface.py.
KIWOOM_KIS_ALTERNATIVES: dict[str, tuple[str, ...]] = {
    "kiwoom.analysis.daily-institutional": ("kis.analysis.investor-by-market-daily",),
    "kiwoom.analysis.foreign-institution": ("kis.analysis.institutional-foreign",),
    "kiwoom.analysis.foreign-net-buy": ("kis.analysis.institutional-foreign",),
    "kiwoom.analysis.institutional": ("kis.analysis.institutional-foreign",),
    "kiwoom.analysis.institutional-trend": ("kis.analysis.institutional-foreign",),
    "kiwoom.analysis.intraday-investor": ("kis.analysis.investor-by-market-intraday",),
    "kiwoom.analysis.member-trend": ("kis.analysis.member-trend-tick",),
    "kiwoom.etf.daily-execution": ("kis.etf.daily",),
    "kiwoom.etf.full-price": ("kis.etf.current-price",),
    "kiwoom.etf.hourly": ("kis.etf.nav-trend",),
    "kiwoom.etf.hourly-v2": ("kis.etf.nav-trend",),
    "kiwoom.etf.return-rate": ("kis.etf.daily",),
    "kiwoom.program.by-stock-daily": ("kis.program.investor-trend",),
    "kiwoom.program.by-stock-intraday": ("kis.program.investor-trend",),
    "kiwoom.program.cumulative": ("kis.program.investor-trend",),
    "kiwoom.program.summary-daily": ("kis.program.investor-trend",),
    "kiwoom.program.summary-intraday": ("kis.program.investor-trend",),
    "kiwoom.ranking.after-hours": ("kis.ranking.after-hours-volume",),
    "kiwoom.ranking.expected-conclusion": ("kis.ranking.expected-execution",),
    "kiwoom.ranking.foreigner-period": ("kis.analysis.foreign-brokerage",),
    "kiwoom.ranking.increasing-order": ("kis.ranking.hoga-quantity",),
    "kiwoom.ranking.increasing-volume": ("kis.ranking.volume",),
    "kiwoom.ranking.prev-day-volume": ("kis.ranking.volume",),
    "kiwoom.ranking.remaining-order": ("kis.ranking.hoga-quantity",),
    "kiwoom.ranking.transaction-value": ("kis.ranking.volume",),
    "kiwoom.sector.all-index": ("kis.sector.current-index",),
    "kiwoom.stock.basic-v1": ("kis.stock.basic-info", "kis.stock.current-price"),
    "kiwoom.stock.credit-trend": ("kis.ranking.credit",),
    "kiwoom.stock.daily-price": ("kis.chart.daily",),
    "kiwoom.stock.execution-intensity-date": ("kis.ranking.execution-strength",),
    "kiwoom.stock.execution-intensity-time": ("kis.ranking.execution-strength",),
    "kiwoom.stock.high-per": ("kis.ranking.market-value",),
    "kiwoom.stock.interest-indicator": ("kis.analysis.watchlist-multi-quote",),
    "kiwoom.stock.investor": ("kis.analysis.investor-by-market-daily",),
    "kiwoom.stock.member": ("kis.analysis.member-trend-tick",),
    "kiwoom.stock.order-book-by-date": ("kis.stock.order-book",),
    "kiwoom.stock.overtime-price": ("kis.stock.overtime-daily",),
    "kiwoom.stock.prev-day-conclusion": ("kis.stock.conclusion",),
    "kiwoom.stock.total-institutional": ("kis.analysis.institutional-foreign",),
    "kiwoom.stock.upper-lower-limit": ("kis.analysis.limit-price-stocks",),
    "kiwoom.stock.volume-renewal": ("kis.ranking.volume",),
}


def kis_alternatives_for(qualified_name: str) -> tuple[str, ...]:
    return KIWOOM_KIS_ALTERNATIVES.get(qualified_name, ())


_DOMAIN_TAXONOMY: dict[str, TaxonomyMetadata] = {
    "chart": TaxonomyMetadata(
        name="chart",
        description="Price, volume, and OHLCV time-series lookup commands.",
        when_to_use="Use before technical analysis, price trend review, or volume analysis.",
        avoid_when="Skip when OHLCV arrays are already in hand; compute indicators from them with the cluefin-ta package.",
        related_tags=("ohlcv", "daily", "minute", "tick"),
    ),
    "corporate-actions": TaxonomyMetadata(
        name="corporate-actions",
        description="Dividend, capital change, merger, split, IPO, listing, and meeting event commands.",
        when_to_use="Use when an agent needs issuer event schedules or corporate-action monitoring.",
        avoid_when="Use news or statements domains when the task needs disclosure text or financial statement values.",
        related_tags=(
            "dividend",
            "ipo",
            "capital-increase",
            "capital-reduction",
            "merger-split",
            "shareholder-meeting",
        ),
    ),
    "etf": TaxonomyMetadata(
        name="etf",
        description="ETF quote, holdings, NAV, and execution data commands.",
        when_to_use="Use for ETF research, ETF market scans, or component stock lookups.",
        avoid_when="Use quote or chart domains for regular stock quote and OHLCV tasks.",
        related_tags=("current-price", "daily"),
    ),
    "market": TaxonomyMetadata(
        name="market",
        description="Market-wide scan, ranking, schedule, and summary commands.",
        when_to_use="Use when the task starts from a market universe rather than one known stock.",
        avoid_when="Use quote or statements domains when the task is already focused on one issuer.",
        related_tags=("ranking", "volume-rank", "market-cap", "market-calendar"),
    ),
    "market-calendar": TaxonomyMetadata(
        name="market-calendar",
        description="Trading calendar, business day, holiday, and dated market-event commands.",
        when_to_use="Use to validate trading dates or discover dated market and issuer events.",
        avoid_when="Use corporate-actions for issuer action details and market for broad scans.",
        related_tags=("market-calendar", "announcement"),
    ),
    "news": TaxonomyMetadata(
        name="news",
        description="Market announcement and DART disclosure discovery commands.",
        when_to_use="Use for title-level news, formal disclosures, and disclosure monitoring workflows.",
        avoid_when="Use statements when the task needs normalized financial values rather than filing discovery.",
        related_tags=("announcement", "disclosure"),
    ),
    "quote": TaxonomyMetadata(
        name="quote",
        description="Current price, order book, execution, and stock identity lookup commands.",
        when_to_use="Use for latest stock state, quote snapshots, and immediate market microstructure context.",
        avoid_when="Use chart when historical OHLCV series are required.",
        related_tags=("current-price", "order-book", "conclusion", "overtime"),
    ),
    "sector": TaxonomyMetadata(
        name="sector",
        description="Sector and industry index commands.",
        when_to_use="Use for sector context, sector trend checks, or market scan grouping.",
        avoid_when="Use theme when the grouping is thematic rather than exchange sector based.",
        related_tags=("sector-index", "daily", "minute"),
    ),
    "statements": TaxonomyMetadata(
        name="statements",
        description="Financial statement, financial ratio, company overview, and shareholder commands.",
        when_to_use="Use for fundamental analysis, issuer financials, ratios, and ownership context.",
        avoid_when="Use news for disclosure search or quote for current market pricing.",
        related_tags=("financial-statement", "financial-ratio", "shareholder", "disclosure"),
    ),
    "theme": TaxonomyMetadata(
        name="theme",
        description="Theme group and theme constituent commands.",
        when_to_use="Use for thematic market scans and group membership discovery.",
        avoid_when="Use sector for exchange sector or industry index analysis.",
        related_tags=("theme-group",),
    ),
    "trading-flow": TaxonomyMetadata(
        name="trading-flow",
        description="Investor, foreigner, institution, brokerage, short-selling, and program trading commands.",
        when_to_use="Use when a task asks who is buying or selling, or needs supply/demand context.",
        avoid_when="Use chart for price series or quote for current price snapshots.",
        related_tags=("foreign", "institution", "program-trading", "short-selling", "credit"),
    ),
}

_TAG_TAXONOMY: dict[str, TaxonomyMetadata] = {
    "announcement": TaxonomyMetadata(
        name="announcement",
        description="Market announcement and event title data.",
        when_to_use="Use to discover recent market notices or schedule announcements.",
        related_domains=("news", "market-calendar", "corporate-actions"),
    ),
    "capital-increase": TaxonomyMetadata(
        name="capital-increase",
        description="Paid-in capital increase schedule or decision data.",
        when_to_use="Use when tracking equity issuance or capital raise events.",
        related_domains=("corporate-actions",),
    ),
    "capital-reduction": TaxonomyMetadata(
        name="capital-reduction",
        description="Capital reduction and reverse split schedule data.",
        when_to_use="Use when tracking capital structure reductions or reverse split events.",
        related_domains=("corporate-actions",),
    ),
    "conclusion": TaxonomyMetadata(
        name="conclusion",
        description="Execution or trade conclusion data.",
        when_to_use="Use for recent executed trade details and microstructure checks.",
        related_domains=("quote",),
    ),
    "credit": TaxonomyMetadata(
        name="credit",
        description="Margin, credit, or loan-related market data.",
        when_to_use="Use when supply/demand analysis needs credit balance or margin-tradable context.",
        related_domains=("trading-flow", "market"),
    ),
    "current-price": TaxonomyMetadata(
        name="current-price",
        description="Latest quote or current price snapshot.",
        when_to_use="Use as the first lookup for current market state of a stock or ETF.",
        related_domains=("quote", "etf"),
    ),
    "daily": TaxonomyMetadata(
        name="daily",
        description="Daily interval series or daily event data.",
        when_to_use="Use for day-level chart, sector, ETF, and trading-flow analysis.",
        related_domains=("chart", "sector", "etf"),
    ),
    "disclosure": TaxonomyMetadata(
        name="disclosure",
        description="Formal DART disclosure or disclosure-linked company data.",
        when_to_use="Use to find filings, issuer details, and disclosure-backed records.",
        related_domains=("news", "statements"),
    ),
    "dividend": TaxonomyMetadata(
        name="dividend",
        description="Cash dividend or stock dividend schedule and decision data.",
        when_to_use="Use for income, payout, corporate-action, and event monitoring tasks.",
        related_domains=("corporate-actions",),
    ),
    "financial-ratio": TaxonomyMetadata(
        name="financial-ratio",
        description="Profitability, stability, growth, valuation, and other financial ratios.",
        when_to_use="Use after statement lookup when comparing issuer fundamentals.",
        related_domains=("statements",),
    ),
    "financial-statement": TaxonomyMetadata(
        name="financial-statement",
        description="Balance sheet, income statement, and related financial statement data.",
        when_to_use="Use for fundamental analysis and statement-driven research.",
        related_domains=("statements",),
    ),
    "foreign": TaxonomyMetadata(
        name="foreign",
        description="Foreign investor or foreign brokerage trading data.",
        when_to_use="Use when analyzing foreign buying, selling, ownership, or flow.",
        related_domains=("trading-flow", "market"),
    ),
    "institution": TaxonomyMetadata(
        name="institution",
        description="Institutional investor trading data.",
        when_to_use="Use when analyzing institution-driven supply and demand.",
        related_domains=("trading-flow", "market"),
    ),
    "ipo": TaxonomyMetadata(
        name="ipo",
        description="IPO subscription and listing schedule data.",
        when_to_use="Use for new listing and public offering event workflows.",
        related_domains=("corporate-actions", "market-calendar"),
    ),
    "market-calendar": TaxonomyMetadata(
        name="market-calendar",
        description="Holiday, business day, and date-based market schedule data.",
        when_to_use="Use to validate tradable dates or discover market calendar events.",
        related_domains=("market-calendar", "market"),
    ),
    "market-cap": TaxonomyMetadata(
        name="market-cap",
        description="Market capitalization or market value ranking data.",
        when_to_use="Use for size-based market screening and ranking tasks.",
        related_domains=("market",),
    ),
    "merger-split": TaxonomyMetadata(
        name="merger-split",
        description="Merger, split, and par value change event data.",
        when_to_use="Use for issuer restructuring and corporate-action monitoring.",
        related_domains=("corporate-actions",),
    ),
    "minute": TaxonomyMetadata(
        name="minute",
        description="Minute interval price or index data.",
        when_to_use="Use for intraday chart analysis and short-horizon market context.",
        related_domains=("chart", "sector"),
    ),
    "ohlcv": TaxonomyMetadata(
        name="ohlcv",
        description="Open, high, low, close, and volume price series data.",
        when_to_use="Use to collect source arrays for technical indicators and price/volume analysis.",
        avoid_when="Skip when OHLCV arrays are already available; compute indicators with the cluefin-ta package instead of re-fetching.",
        related_domains=("chart",),
    ),
    "order-book": TaxonomyMetadata(
        name="order-book",
        description="Bid/ask order book and quote depth data.",
        when_to_use="Use for current liquidity and market microstructure context.",
        related_domains=("quote",),
    ),
    "overtime": TaxonomyMetadata(
        name="overtime",
        description="After-hours or overtime trading data.",
        when_to_use="Use when the task specifically involves off-regular-session prices or execution.",
        related_domains=("quote",),
    ),
    "program-trading": TaxonomyMetadata(
        name="program-trading",
        description="Program trading summary, cumulative, arbitrage, or by-stock flow data.",
        when_to_use="Use when supply/demand analysis needs program trading context.",
        related_domains=("trading-flow", "market"),
    ),
    "ranking": TaxonomyMetadata(
        name="ranking",
        description="Provider ranking outputs for market screening.",
        when_to_use="Use to find candidate stocks by a provider-defined ranking criterion.",
        related_domains=("market",),
    ),
    "sector-index": TaxonomyMetadata(
        name="sector-index",
        description="Sector or industry index price and time-series data.",
        when_to_use="Use when comparing a stock against sector-level movement.",
        related_domains=("sector", "market"),
    ),
    "shareholder": TaxonomyMetadata(
        name="shareholder",
        description="Major shareholder or ownership-related issuer data.",
        when_to_use="Use for ownership, governance, and shareholder context.",
        related_domains=("statements",),
    ),
    "shareholder-meeting": TaxonomyMetadata(
        name="shareholder-meeting",
        description="Shareholder meeting schedule data.",
        when_to_use="Use for governance event monitoring and calendar workflows.",
        related_domains=("corporate-actions", "market-calendar"),
    ),
    "short-selling": TaxonomyMetadata(
        name="short-selling",
        description="Short selling, stock loan, or loanable stock data.",
        when_to_use="Use when bearish positioning or lending context is relevant.",
        related_domains=("trading-flow", "market"),
    ),
    "theme-group": TaxonomyMetadata(
        name="theme-group",
        description="Theme group list or theme constituent data.",
        when_to_use="Use for thematic screening and theme membership discovery.",
        related_domains=("theme", "market"),
    ),
    "tick": TaxonomyMetadata(
        name="tick",
        description="Tick interval price or index data.",
        when_to_use="Use for high-frequency or execution-level chart analysis.",
        related_domains=("chart",),
    ),
    "volume-rank": TaxonomyMetadata(
        name="volume-rank",
        description="Trading volume ranking or volume renewal data.",
        when_to_use="Use for liquidity, unusual volume, and market scan workflows.",
        related_domains=("market",),
    ),
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


def build_agent_notes(
    *,
    broker: str,
    category: str,
    name: str,
    required_credentials: tuple[str, ...],
    kis_alternatives: tuple[str, ...] = (),
) -> str:
    """Build concise command-use guidance for agents."""

    credential_note = ", ".join(required_credentials) if required_credentials else "configured broker credentials"
    base = f"Read-only {broker.upper()} command. Use --json for machine-readable output. Requires {credential_note}."
    if broker_role_name(broker) == "auxiliary":
        if kis_alternatives:
            preferred = ", ".join(kis_alternatives)
            base = f"Auxiliary-broker command. Prefer the primary KIS command first: {preferred}. {base}"
        else:
            base = f"Auxiliary-broker command with no KIS equivalent; this is the intended use of Kiwoom. {base}"

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
