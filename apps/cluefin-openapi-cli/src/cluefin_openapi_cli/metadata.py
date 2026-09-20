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
        avoid_when="Skip when the question is what the indicators say rather than what the prices were — `kis chart technical` computes them and returns readings instead of rows.",
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
    "reference": TaxonomyMetadata(
        name="reference",
        description="Static registries: instrument identity, product master, member firms, industry codes, and eligibility lists.",
        when_to_use="Use to resolve a code, confirm an instrument exists, or list what is tradable/loanable before a real query.",
        avoid_when="Use quote for live price state; these lists describe what exists, not what it is doing now.",
        related_tags=("reference-list", "broker-flow", "short-selling", "credit"),
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
    "screening": TaxonomyMetadata(
        name="screening",
        description="Commands that return a filtered or ranked slice of the market rather than one known stock.",
        when_to_use="Use when the task starts from a condition ('stocks that ...') instead of a stock code.",
        avoid_when="Use ranking when you want a standard top-N list by a single criterion.",
        related_domains=("market",),
    ),
    "condition-search": TaxonomyMetadata(
        name="condition-search",
        description="Saved HTS condition-search definitions and their results.",
        when_to_use="Use to run a user's pre-saved screening condition; requires a user id.",
        related_domains=("market",),
    ),
    "watchlist": TaxonomyMetadata(
        name="watchlist",
        description="Watchlist (관심종목) group membership and multi-stock quote lookup.",
        when_to_use="Use to read a user's watchlist groups or quote many stocks in one call.",
        related_domains=("quote", "market"),
    ),
    "broker-flow": TaxonomyMetadata(
        name="broker-flow",
        description="Trading by securities firm / member company (거래원·회원사).",
        when_to_use="Use when the question is which brokerage is buying or selling, not which investor type.",
        avoid_when="Use foreign or institution for investor-type flow.",
        related_domains=("trading-flow", "market"),
    ),
    "analyst-opinion": TaxonomyMetadata(
        name="analyst-opinion",
        description="Sell-side investment opinions and target prices.",
        when_to_use="Use for analyst ratings on a stock, optionally broken down by brokerage.",
        related_domains=("statements",),
    ),
    "earnings-estimate": TaxonomyMetadata(
        name="earnings-estimate",
        description="Forward earnings and foreign/institutional estimates.",
        when_to_use="Use for forward-looking figures rather than reported statements.",
        avoid_when="Use financial-statement for reported results.",
        related_domains=("statements", "trading-flow"),
    ),
    "valuation": TaxonomyMetadata(
        name="valuation",
        description="PER, PBR, PCR, PSR, EPS and ROE based screens.",
        when_to_use="Use to rank or screen by valuation multiples.",
        related_domains=("market", "statements"),
    ),
    "nav": TaxonomyMetadata(
        name="nav",
        description="ETF/ETN net asset value and NAV-vs-price tracking.",
        when_to_use="Use for ETF NAV levels, premium/discount, and return tracking.",
        related_domains=("etf",),
    ),
    "etf-holdings": TaxonomyMetadata(
        name="etf-holdings",
        description="ETF component stocks (PDF) and their weights.",
        when_to_use="Use to see what an ETF actually holds.",
        related_domains=("etf",),
    ),
    "reference-list": TaxonomyMetadata(
        name="reference-list",
        description="Static master lists: instruments, member firms, industry codes, eligibility.",
        when_to_use="Use to resolve or enumerate codes before a data query.",
        avoid_when="Use current-price for live state.",
        related_domains=("reference", "market"),
    ),
    "volatility": TaxonomyMetadata(
        name="volatility",
        description="Rapid price movement, VI triggers, and upper/lower limit states.",
        when_to_use="Use to find stocks moving abnormally fast or halted for volatility.",
        related_domains=("market", "quote"),
    ),
    "expected-price": TaxonomyMetadata(
        name="expected-price",
        description="Pre-open, closing-auction, and after-hours expected execution prices.",
        when_to_use="Use for indicative prices outside continuous trading.",
        avoid_when="Use current-price during continuous session hours.",
        related_domains=("quote", "market"),
    ),
    "investor-interest": TaxonomyMetadata(
        name="investor-interest",
        description="Retail attention proxies: HTS inquiry counts, watchlist registrations, sentiment.",
        when_to_use="Use to gauge how much attention a stock is getting, independent of price.",
        related_domains=("market",),
    ),
    "price-level": TaxonomyMetadata(
        name="price-level",
        description="Support/resistance, disparity, new high/low, and supply-concentration price zones.",
        when_to_use="Use to locate meaningful price levels for a stock.",
        related_domains=("quote", "market"),
    ),
    "execution-strength": TaxonomyMetadata(
        name="execution-strength",
        description="Execution strength (체결강도) and trading weight by execution amount.",
        when_to_use="Use to judge buying vs selling pressure inside executions.",
        related_domains=("quote",),
    ),
    "market-breadth": TaxonomyMetadata(
        name="market-breadth",
        description="Market-wide fund flow and interest-rate summary context.",
        when_to_use="Use for macro/market-level context rather than a single stock.",
        related_domains=("market",),
    ),
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
        avoid_when="Skip when only indicator readings are needed; `kis chart technical` computes them in-process, so no candle series has to be read at all.",
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
    "technical-indicator": TaxonomyMetadata(
        name="technical-indicator",
        description="Computed indicator readings and signal rules rather than raw price rows.",
        when_to_use=(
            "Use when the question is what the indicators say. The CLI computes them in-process and "
            "returns final values only, so no OHLCV table has to be read into context."
        ),
        avoid_when="Use the ohlcv tag when the raw candle series itself is the deliverable.",
        related_domains=("chart",),
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


@dataclass(frozen=True, slots=True)
class CommandTaxonomy:
    """Hand-authored discovery taxonomy for one command.

    Keyed by qualified name — the same identity recipes, `kis_alternatives`, and the
    tests already use. Authored per command rather than derived from the category,
    because a category default is wrong for every command in the category that is not
    the category's typical case, and there is no rule that can remove a wrong default.
    """

    domains: tuple[str, ...]
    tags: tuple[str, ...]
    keywords: tuple[str, ...] = ()


COMMAND_TAXONOMY: dict[str, CommandTaxonomy] = {
    "kis.analysis.after-hours-expected": CommandTaxonomy(
        ("market", "quote"), ("expected-price", "overtime", "screening")
    ),
    "kis.analysis.buy-sell-volume-daily": CommandTaxonomy(("trading-flow",), ("foreign", "institution", "daily")),
    "kis.analysis.condition-search-list": CommandTaxonomy(("market",), ("screening", "condition-search")),
    "kis.analysis.condition-search-result": CommandTaxonomy(("market",), ("screening", "condition-search")),
    "kis.analysis.expected-price-trend": CommandTaxonomy(("quote",), ("expected-price",)),
    "kis.analysis.foreign-brokerage": CommandTaxonomy(
        ("trading-flow", "market"), ("foreign", "broker-flow", "ranking")
    ),
    "kis.analysis.foreign-institutional-estimate": CommandTaxonomy(
        ("trading-flow",), ("foreign", "institution", "earnings-estimate")
    ),
    "kis.analysis.institutional-foreign": CommandTaxonomy(("trading-flow",), ("foreign", "institution")),
    "kis.analysis.investor-by-market-daily": CommandTaxonomy(
        ("trading-flow", "market"), ("foreign", "institution", "daily")
    ),
    "kis.analysis.investor-by-market-intraday": CommandTaxonomy(
        ("trading-flow", "market"), ("foreign", "institution", "minute")
    ),
    "kis.analysis.limit-price-stocks": CommandTaxonomy(("market",), ("screening", "volatility")),
    "kis.analysis.market-fund-summary": CommandTaxonomy(("market",), ("market-breadth",)),
    "kis.analysis.member-trend-tick": CommandTaxonomy(("trading-flow",), ("broker-flow", "tick")),
    "kis.analysis.resistance-level": CommandTaxonomy(("quote",), ("price-level", "execution-strength")),
    "kis.analysis.short-selling-trend": CommandTaxonomy(("trading-flow",), ("short-selling", "daily")),
    "kis.analysis.stock-loan-trend": CommandTaxonomy(("trading-flow",), ("short-selling", "daily")),
    "kis.analysis.trading-weight": CommandTaxonomy(("quote",), ("price-level", "execution-strength")),
    "kis.analysis.watchlist-groups": CommandTaxonomy(("quote",), ("watchlist",)),
    "kis.analysis.watchlist-multi-quote": CommandTaxonomy(("quote",), ("watchlist", "current-price")),
    "kis.analysis.watchlist-stocks": CommandTaxonomy(("quote",), ("watchlist",)),
    "kis.chart.daily": CommandTaxonomy(("chart",), ("ohlcv", "daily")),
    "kis.chart.daily-minute": CommandTaxonomy(("chart",), ("ohlcv", "minute", "daily")),
    "kis.chart.minute": CommandTaxonomy(("chart",), ("ohlcv", "minute")),
    "kis.chart.period": CommandTaxonomy(("chart",), ("ohlcv", "daily")),
    "kis.chart.technical": CommandTaxonomy(("chart",), ("technical-indicator", "daily")),
    "kis.etf.component-stocks": CommandTaxonomy(("etf",), ("etf-holdings",)),
    "kis.etf.current-price": CommandTaxonomy(("etf", "quote"), ("current-price", "nav")),
    "kis.etf.daily": CommandTaxonomy(("etf", "chart"), ("nav", "daily")),
    "kis.etf.nav-trend": CommandTaxonomy(("etf",), ("nav",)),
    "kis.financial.balance-sheet": CommandTaxonomy(("statements",), ("financial-statement",)),
    "kis.financial.growth": CommandTaxonomy(("statements",), ("financial-ratio",)),
    "kis.financial.income-statement": CommandTaxonomy(("statements",), ("financial-statement",)),
    "kis.financial.other-key": CommandTaxonomy(("statements",), ("financial-ratio",)),
    "kis.financial.profitability": CommandTaxonomy(("statements",), ("financial-ratio",)),
    "kis.financial.ratio": CommandTaxonomy(("statements",), ("financial-ratio",)),
    "kis.financial.stability": CommandTaxonomy(("statements",), ("financial-ratio",)),
    "kis.market.announcement": CommandTaxonomy(("news", "market"), ("announcement", "disclosure")),
    "kis.market.futures-business-day": CommandTaxonomy(("market-calendar", "market"), ("market-calendar",)),
    "kis.market.holiday": CommandTaxonomy(("market-calendar", "market"), ("market-calendar",)),
    "kis.market.interest-rate": CommandTaxonomy(("market",), ("market-breadth",)),
    "kis.program.investor-trend": CommandTaxonomy(("trading-flow", "market"), ("program-trading",)),
    "kis.ranking.after-hours-volume": CommandTaxonomy(("market",), ("ranking", "volume-rank", "overtime")),
    "kis.ranking.credit": CommandTaxonomy(("market",), ("ranking", "credit")),
    "kis.ranking.disparity": CommandTaxonomy(("market",), ("ranking", "price-level")),
    "kis.ranking.dividend-yield": CommandTaxonomy(("market", "corporate-actions"), ("ranking", "dividend")),
    "kis.ranking.execution-strength": CommandTaxonomy(("market",), ("ranking", "execution-strength")),
    "kis.ranking.expected-execution": CommandTaxonomy(("market",), ("ranking", "expected-price")),
    "kis.ranking.finance-ratio": CommandTaxonomy(("market", "statements"), ("ranking", "financial-ratio")),
    "kis.ranking.hoga-quantity": CommandTaxonomy(("market",), ("ranking", "order-book")),
    "kis.ranking.hts-inquiry": CommandTaxonomy(("market",), ("ranking", "investor-interest")),
    "kis.ranking.large-execution": CommandTaxonomy(("market",), ("ranking", "conclusion")),
    "kis.ranking.market-cap": CommandTaxonomy(("market",), ("ranking", "market-cap")),
    "kis.ranking.market-value": CommandTaxonomy(("market", "statements"), ("ranking", "valuation")),
    "kis.ranking.new-high-low": CommandTaxonomy(("market",), ("ranking", "price-level")),
    "kis.ranking.preferred-stock": CommandTaxonomy(("market",), ("ranking", "price-level")),
    "kis.ranking.profitability": CommandTaxonomy(("market", "statements"), ("ranking", "financial-ratio")),
    "kis.ranking.proprietary": CommandTaxonomy(("market", "trading-flow"), ("ranking", "institution")),
    "kis.ranking.short-selling": CommandTaxonomy(("market", "trading-flow"), ("ranking", "short-selling")),
    "kis.ranking.time-hoga": CommandTaxonomy(("market",), ("ranking", "order-book", "overtime")),
    "kis.ranking.volume": CommandTaxonomy(("market",), ("ranking", "volume-rank")),
    "kis.ranking.watchlist": CommandTaxonomy(("market",), ("ranking", "investor-interest", "watchlist")),
    "kis.schedule.bonus-issue": CommandTaxonomy(("corporate-actions", "market-calendar"), ("dividend", "announcement")),
    "kis.schedule.capital-increase": CommandTaxonomy(
        ("corporate-actions", "market-calendar"), ("capital-increase", "announcement")
    ),
    "kis.schedule.capital-reduction": CommandTaxonomy(
        ("corporate-actions", "market-calendar"), ("capital-reduction", "announcement")
    ),
    "kis.schedule.deposit": CommandTaxonomy(("corporate-actions", "market-calendar"), ("announcement",)),
    "kis.schedule.dividend": CommandTaxonomy(("corporate-actions", "market-calendar"), ("dividend", "announcement")),
    "kis.schedule.forfeited-share": CommandTaxonomy(
        ("corporate-actions", "market-calendar"), ("capital-increase", "announcement")
    ),
    "kis.schedule.ipo-subscription": CommandTaxonomy(("corporate-actions", "market-calendar"), ("ipo", "announcement")),
    "kis.schedule.listing": CommandTaxonomy(("corporate-actions", "market-calendar"), ("ipo", "announcement")),
    "kis.schedule.merger-split": CommandTaxonomy(
        ("corporate-actions", "market-calendar"), ("merger-split", "announcement")
    ),
    "kis.schedule.par-value-change": CommandTaxonomy(
        ("corporate-actions", "market-calendar"), ("merger-split", "announcement")
    ),
    "kis.schedule.shareholder-meeting": CommandTaxonomy(
        ("corporate-actions", "market-calendar"), ("shareholder-meeting", "announcement")
    ),
    "kis.schedule.stock-dividend": CommandTaxonomy(
        ("corporate-actions", "market-calendar"), ("dividend", "announcement")
    ),
    "kis.sector.current-index": CommandTaxonomy(("sector",), ("sector-index", "current-price")),
    "kis.sector.daily": CommandTaxonomy(("sector", "chart"), ("sector-index", "daily", "ohlcv")),
    "kis.sector.expected-index-all": CommandTaxonomy(("sector",), ("sector-index", "expected-price")),
    "kis.sector.expected-index-trend": CommandTaxonomy(("sector",), ("sector-index", "expected-price")),
    "kis.sector.minute": CommandTaxonomy(("sector", "chart"), ("sector-index", "minute", "ohlcv")),
    "kis.sector.period": CommandTaxonomy(("sector", "chart"), ("sector-index", "daily", "ohlcv")),
    "kis.sector.time-minute": CommandTaxonomy(("sector",), ("sector-index", "minute")),
    "kis.sector.time-second": CommandTaxonomy(("sector",), ("sector-index", "tick")),
    "kis.stock.basic-info": CommandTaxonomy(("reference", "quote"), ("reference-list",)),
    "kis.stock.closing-expected": CommandTaxonomy(("market",), ("screening", "expected-price", "ranking")),
    "kis.stock.conclusion": CommandTaxonomy(("quote",), ("conclusion", "tick")),
    "kis.stock.current-price": CommandTaxonomy(("quote",), ("current-price",)),
    "kis.stock.current-price-extended": CommandTaxonomy(("quote",), ("current-price", "volatility", "credit")),
    "kis.stock.estimated-earnings": CommandTaxonomy(("statements",), ("earnings-estimate",)),
    "kis.stock.investment-opinion": CommandTaxonomy(("statements",), ("analyst-opinion",)),
    "kis.stock.investment-opinion-by-brokerage": CommandTaxonomy(("statements",), ("analyst-opinion", "broker-flow")),
    "kis.stock.loanable": CommandTaxonomy(("reference", "trading-flow"), ("reference-list", "short-selling")),
    "kis.stock.margin-tradable": CommandTaxonomy(("reference", "trading-flow"), ("reference-list", "credit")),
    "kis.stock.order-book": CommandTaxonomy(("quote",), ("order-book", "expected-price")),
    "kis.stock.overtime-conclusion": CommandTaxonomy(("quote",), ("conclusion", "overtime")),
    "kis.stock.overtime-daily": CommandTaxonomy(("quote", "chart"), ("overtime", "daily")),
    "kis.stock.overtime-order-book": CommandTaxonomy(("quote",), ("order-book", "overtime")),
    "kis.stock.product-info": CommandTaxonomy(("reference",), ("reference-list",)),
    "kis.stock.time-conclusion": CommandTaxonomy(("quote",), ("conclusion", "minute")),
    "kiwoom.analysis.after-market-investor": CommandTaxonomy(
        ("trading-flow", "market"), ("foreign", "institution", "overtime")
    ),
    "kiwoom.analysis.daily-institutional": CommandTaxonomy(("trading-flow",), ("institution", "daily")),
    "kiwoom.analysis.foreign-consecutive": CommandTaxonomy(
        ("trading-flow", "market"), ("foreign", "institution", "ranking")
    ),
    "kiwoom.analysis.foreign-institution": CommandTaxonomy(("trading-flow",), ("foreign", "institution")),
    "kiwoom.analysis.foreign-net-buy": CommandTaxonomy(("trading-flow",), ("foreign",)),
    "kiwoom.analysis.institutional": CommandTaxonomy(("trading-flow",), ("institution", "daily")),
    "kiwoom.analysis.institutional-trend": CommandTaxonomy(("trading-flow",), ("institution", "foreign", "daily")),
    "kiwoom.analysis.intraday-investor": CommandTaxonomy(
        ("trading-flow", "market"), ("foreign", "institution", "minute")
    ),
    "kiwoom.analysis.member-trend": CommandTaxonomy(("trading-flow",), ("broker-flow",)),
    "kiwoom.chart.industry-tick": CommandTaxonomy(("chart", "sector"), ("ohlcv", "tick", "sector-index")),
    "kiwoom.chart.institutional": CommandTaxonomy(("chart", "trading-flow"), ("institution", "daily")),
    "kiwoom.chart.intraday-investor": CommandTaxonomy(("chart", "trading-flow"), ("foreign", "institution", "minute")),
    "kiwoom.chart.tick": CommandTaxonomy(("chart",), ("ohlcv", "tick")),
    "kiwoom.etf.daily-execution": CommandTaxonomy(("etf",), ("conclusion", "daily")),
    "kiwoom.etf.full-price": CommandTaxonomy(("etf", "market"), ("current-price", "screening")),
    "kiwoom.etf.hourly": CommandTaxonomy(("etf",), ("nav", "minute")),
    "kiwoom.etf.hourly-execution": CommandTaxonomy(("etf",), ("conclusion", "minute")),
    "kiwoom.etf.hourly-execution-v2": CommandTaxonomy(("etf",), ("conclusion", "minute")),
    "kiwoom.etf.hourly-v2": CommandTaxonomy(("etf",), ("nav", "minute")),
    "kiwoom.etf.return-rate": CommandTaxonomy(("etf",), ("nav",)),
    "kiwoom.market.warrant-price": CommandTaxonomy(
        ("corporate-actions", "quote"), ("capital-increase", "current-price")
    ),
    "kiwoom.program.arbitrage-balance": CommandTaxonomy(("trading-flow", "market"), ("program-trading",)),
    "kiwoom.program.by-stock-daily": CommandTaxonomy(("trading-flow",), ("program-trading", "daily")),
    "kiwoom.program.by-stock-intraday": CommandTaxonomy(("trading-flow",), ("program-trading", "minute")),
    "kiwoom.program.cumulative": CommandTaxonomy(("trading-flow", "market"), ("program-trading",)),
    "kiwoom.program.summary-daily": CommandTaxonomy(("trading-flow", "market"), ("program-trading", "daily")),
    "kiwoom.program.summary-intraday": CommandTaxonomy(("trading-flow", "market"), ("program-trading", "minute")),
    "kiwoom.ranking.after-hours": CommandTaxonomy(("market",), ("ranking", "overtime")),
    "kiwoom.ranking.consecutive-foreign": CommandTaxonomy(("market", "trading-flow"), ("ranking", "foreign")),
    "kiwoom.ranking.deviation-sources": CommandTaxonomy(("market", "trading-flow"), ("ranking", "broker-flow")),
    "kiwoom.ranking.expected-conclusion": CommandTaxonomy(("market",), ("ranking", "expected-price")),
    "kiwoom.ranking.fluctuation": CommandTaxonomy(("market",), ("ranking", "volatility")),
    "kiwoom.ranking.foreign-account": CommandTaxonomy(("market", "trading-flow"), ("ranking", "foreign")),
    "kiwoom.ranking.foreign-limit": CommandTaxonomy(("market", "trading-flow"), ("ranking", "foreign")),
    "kiwoom.ranking.foreigner-period": CommandTaxonomy(("market", "trading-flow"), ("ranking", "foreign")),
    "kiwoom.ranking.increasing-order": CommandTaxonomy(("market",), ("ranking", "order-book")),
    "kiwoom.ranking.increasing-sell": CommandTaxonomy(("market",), ("ranking", "order-book")),
    "kiwoom.ranking.increasing-volume": CommandTaxonomy(("market",), ("ranking", "volume-rank")),
    "kiwoom.ranking.intraday-investor": CommandTaxonomy(
        ("market", "trading-flow"), ("ranking", "foreign", "institution")
    ),
    "kiwoom.ranking.major-traders": CommandTaxonomy(("market", "trading-flow"), ("ranking", "broker-flow")),
    "kiwoom.ranking.net-buy-trader": CommandTaxonomy(("market", "trading-flow"), ("ranking", "broker-flow")),
    "kiwoom.ranking.prev-day-volume": CommandTaxonomy(("market",), ("ranking", "volume-rank")),
    "kiwoom.ranking.remaining-order": CommandTaxonomy(("market",), ("ranking", "order-book")),
    "kiwoom.ranking.same-net-buy-sell": CommandTaxonomy(
        ("market", "trading-flow"), ("ranking", "foreign", "institution")
    ),
    "kiwoom.ranking.securities-firm": CommandTaxonomy(("market", "trading-flow"), ("ranking", "broker-flow")),
    "kiwoom.ranking.securities-firm-by-stock": CommandTaxonomy(("market", "trading-flow"), ("ranking", "broker-flow")),
    "kiwoom.ranking.transaction-value": CommandTaxonomy(("market",), ("ranking", "volume-rank")),
    "kiwoom.sector.all-index": CommandTaxonomy(("sector",), ("sector-index",)),
    "kiwoom.sector.investor-net-buy": CommandTaxonomy(
        ("sector", "trading-flow"), ("sector-index", "foreign", "institution")
    ),
    "kiwoom.sector.program": CommandTaxonomy(("sector", "trading-flow"), ("sector-index", "program-trading")),
    "kiwoom.sector.stocks": CommandTaxonomy(("sector", "market"), ("sector-index", "screening")),
    "kiwoom.stock.basic-v1": CommandTaxonomy(("quote", "reference"), ("current-price", "reference-list")),
    "kiwoom.stock.change-from-open": CommandTaxonomy(("market",), ("screening", "ranking", "volatility")),
    "kiwoom.stock.credit-trend": CommandTaxonomy(("trading-flow",), ("credit", "daily")),
    "kiwoom.stock.daily-details": CommandTaxonomy(("quote", "chart"), ("daily", "conclusion")),
    "kiwoom.stock.daily-price": CommandTaxonomy(("chart", "quote"), ("ohlcv", "daily")),
    "kiwoom.stock.execution-intensity-date": CommandTaxonomy(("quote",), ("execution-strength", "daily")),
    "kiwoom.stock.execution-intensity-time": CommandTaxonomy(("quote",), ("execution-strength", "minute")),
    "kiwoom.stock.high-per": CommandTaxonomy(("market", "statements"), ("ranking", "valuation")),
    "kiwoom.stock.industry-code": CommandTaxonomy(("reference", "sector"), ("reference-list", "sector-index")),
    "kiwoom.stock.interest-indicator": CommandTaxonomy(("quote",), ("watchlist", "current-price")),
    "kiwoom.stock.investor": CommandTaxonomy(("market", "trading-flow"), ("ranking", "foreign", "institution")),
    "kiwoom.stock.member": CommandTaxonomy(("trading-flow",), ("broker-flow",)),
    "kiwoom.stock.member-company": CommandTaxonomy(("reference",), ("reference-list", "broker-flow")),
    "kiwoom.stock.member-instant-volume": CommandTaxonomy(("trading-flow",), ("broker-flow", "minute")),
    "kiwoom.stock.member-supply-demand": CommandTaxonomy(("trading-flow",), ("broker-flow",)),
    "kiwoom.stock.order-book-by-date": CommandTaxonomy(("quote",), ("order-book", "daily")),
    "kiwoom.stock.overtime-price": CommandTaxonomy(("quote",), ("overtime", "current-price")),
    "kiwoom.stock.prev-day-conclusion": CommandTaxonomy(("quote",), ("conclusion", "daily")),
    "kiwoom.stock.prev-day-volume": CommandTaxonomy(("quote",), ("conclusion", "volume-rank", "daily")),
    "kiwoom.stock.price-volatility": CommandTaxonomy(("market",), ("screening", "volatility")),
    "kiwoom.stock.program-net-buy-top50": CommandTaxonomy(("market", "trading-flow"), ("ranking", "program-trading")),
    "kiwoom.stock.program-trading": CommandTaxonomy(("trading-flow", "market"), ("program-trading",)),
    "kiwoom.stock.sentiment": CommandTaxonomy(("quote", "market"), ("investor-interest",)),
    "kiwoom.stock.summary": CommandTaxonomy(("reference", "market"), ("reference-list", "screening")),
    "kiwoom.stock.supply-demand": CommandTaxonomy(("market", "trading-flow"), ("screening", "price-level")),
    "kiwoom.stock.total-institutional": CommandTaxonomy(("trading-flow",), ("institution",)),
    "kiwoom.stock.upper-lower-limit": CommandTaxonomy(("market",), ("screening", "volatility")),
    "kiwoom.stock.vi-status": CommandTaxonomy(("market",), ("screening", "volatility")),
    "kiwoom.stock.volume-renewal": CommandTaxonomy(("market",), ("screening", "volume-rank")),
    "kiwoom.theme.group": CommandTaxonomy(("theme", "market"), ("theme-group",)),
    "kiwoom.theme.group-stocks": CommandTaxonomy(("theme", "market"), ("theme-group", "screening")),
    "dart.company-overview": CommandTaxonomy(("statements", "reference"), ("disclosure", "shareholder")),
    "dart.corp-code-lookup": CommandTaxonomy(("reference",), ("reference-list", "disclosure")),
    "dart.disclosure-search": CommandTaxonomy(("news", "statements"), ("disclosure",)),
    "dart.executive-ownership-report": CommandTaxonomy(("statements",), ("shareholder", "disclosure")),
    "dart.large-holding-report": CommandTaxonomy(("statements",), ("shareholder", "disclosure")),
    "dart.major-shareholder": CommandTaxonomy(("statements",), ("shareholder", "disclosure")),
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


@dataclass(frozen=True, slots=True)
class CategoryInfo:
    """Agent-facing explanation for one provider SDK category.

    `domains`/`tags` here are the category *seed* values; the authoritative per-command
    taxonomy lives in `COMMAND_TAXONOMY`. Broker help computes its domain/tag union from
    the real commands so it reflects the authored truth, not this seed.
    """

    name: str
    description: str
    when_to_use: str
    domains: tuple[str, ...]
    tags: tuple[str, ...]


CATEGORY_INFO: dict[str, CategoryInfo] = {
    "analysis": CategoryInfo(
        name="analysis",
        description="Investor supply/demand, screening, watchlists, and market-state analysis.",
        when_to_use="Use when the question is who is trading, or to screen the market by a condition.",
        domains=_CATEGORY_DEFAULTS["analysis"][0],
        tags=_CATEGORY_DEFAULTS["analysis"][1],
    ),
    "chart": CategoryInfo(
        name="chart",
        description="Historical OHLCV time series at tick, minute, daily, and period granularity.",
        when_to_use="Use when the raw price/volume rows are the deliverable. For indicator readings, `kis chart technical` computes them and returns values only.",
        domains=_CATEGORY_DEFAULTS["chart"][0],
        tags=_CATEGORY_DEFAULTS["chart"][1],
    ),
    "dart": CategoryInfo(
        name="dart",
        description="Regulatory disclosure filings, corporate codes, and shareholder records.",
        when_to_use="Use for the filed source document or to resolve a corp_code; not a price source.",
        domains=_CATEGORY_DEFAULTS["dart"][0],
        tags=_CATEGORY_DEFAULTS["dart"][1],
    ),
    "etf": CategoryInfo(
        name="etf",
        description="ETF and ETN pricing, NAV tracking, returns, and component holdings.",
        when_to_use="Use for ETF-specific state; a plain equity quote belongs in stock.",
        domains=_CATEGORY_DEFAULTS["etf"][0],
        tags=_CATEGORY_DEFAULTS["etf"][1],
    ),
    "financial": CategoryInfo(
        name="financial",
        description="Reported financial statements and derived ratios.",
        when_to_use="Use for balance sheet, income statement, and profitability/stability/growth ratios.",
        domains=_CATEGORY_DEFAULTS["financial"][0],
        tags=_CATEGORY_DEFAULTS["financial"][1],
    ),
    "market": CategoryInfo(
        name="market",
        description="Market-wide context: announcements, holidays, business days, and rates.",
        when_to_use="Use for calendar checks and market-level background, not per-stock data.",
        domains=_CATEGORY_DEFAULTS["market"][0],
        tags=_CATEGORY_DEFAULTS["market"][1],
    ),
    "program": CategoryInfo(
        name="program",
        description="Program (basket/arbitrage) trading flow.",
        when_to_use="Use when the question is specifically about program trading rather than investor type.",
        domains=_CATEGORY_DEFAULTS["program"][0],
        tags=_CATEGORY_DEFAULTS["program"][1],
    ),
    "ranking": CategoryInfo(
        name="ranking",
        description="Top-N market screens ordered by a single criterion.",
        when_to_use="Use to find candidates across the market; each command pairs ranking with its criterion tag.",
        domains=_CATEGORY_DEFAULTS["ranking"][0],
        tags=_CATEGORY_DEFAULTS["ranking"][1],
    ),
    "schedule": CategoryInfo(
        name="schedule",
        description="Corporate action calendars from KSD: dividends, issuance, listings, meetings.",
        when_to_use="Use for dated corporate events over a start/end date range.",
        domains=_CATEGORY_DEFAULTS["schedule"][0],
        tags=_CATEGORY_DEFAULTS["schedule"][1],
    ),
    "sector": CategoryInfo(
        name="sector",
        description="Sector and industry index levels, history, and constituents.",
        when_to_use="Use for sector context or to group a market scan by industry.",
        domains=_CATEGORY_DEFAULTS["sector"][0],
        tags=_CATEGORY_DEFAULTS["sector"][1],
    ),
    "stock": CategoryInfo(
        name="stock",
        description="Single-stock quotes, order book, executions, identity, and eligibility lists.",
        when_to_use="Use when you already know the stock code and want its current state or reference data.",
        domains=_CATEGORY_DEFAULTS["stock"][0],
        tags=_CATEGORY_DEFAULTS["stock"][1],
    ),
    "theme": CategoryInfo(
        name="theme",
        description="Theme groups and their member stocks.",
        when_to_use="Use to explore thematic baskets; Kiwoom-only, KIS has no theme command.",
        domains=_CATEGORY_DEFAULTS["theme"][0],
        tags=_CATEGORY_DEFAULTS["theme"][1],
    ),
}


def category_info(category: str) -> CategoryInfo | None:
    """Return the agent-facing description for a category, if one is authored."""

    return CATEGORY_INFO.get(category)


#: Query-expansion aliases for `search`. Key = a surface form an agent actually types
#: (Korean, or English jargon that appears nowhere in the command text); value = tokens
#: that really occur in the indexed corpus. Scanned longest-key-first so `순매수` wins
#: over `매수`. Every command description is English, so Korean queries reach the index
#: only through this table.
QUERY_ALIASES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("외국인", ("foreign", "foreigner")),
    ("기관", ("institution", "institutional")),
    ("수급", ("investor", "trend", "institution", "foreign")),
    ("순매수", ("net", "buy")),
    ("순매도", ("net", "sell")),
    ("매매동향", ("trading", "trend", "investor")),
    ("프로그램매매", ("program", "trading")),
    ("재무제표", ("financial", "statement", "balance", "sheet", "income")),
    ("재무비율", ("financial", "ratio", "profitability", "stability", "growth")),
    ("손익계산서", ("income", "statement")),
    ("대차대조표", ("balance", "sheet")),
    ("배당", ("dividend", "yield")),
    ("차트", ("chart", "ohlcv", "price", "history")),
    ("분봉", ("minute", "chart")),
    ("일봉", ("daily", "chart")),
    ("주봉", ("weekly", "period", "chart")),
    ("월봉", ("monthly", "period", "chart")),
    ("틱", ("tick", "chart")),
    ("시세", ("current", "price", "quote")),
    ("현재가", ("current", "price")),
    ("호가", ("order", "book", "bid", "ask")),
    ("체결", ("conclusion", "execution")),
    ("거래량", ("volume",)),
    ("거래대금", ("transaction", "value", "amount")),
    ("순위", ("ranking", "rank", "top")),
    ("상위", ("top", "ranking")),
    ("테마", ("theme", "group")),
    ("업종", ("sector", "industry", "index")),
    ("지수", ("index", "sector")),
    ("공시", ("disclosure", "dart", "announcement")),
    ("공매도", ("short", "selling")),
    ("신용", ("credit", "margin", "loan")),
    ("대출", ("loan", "loanable")),
    ("시가총액", ("market", "cap", "value")),
    ("증자", ("capital", "increase")),
    ("감자", ("capital", "reduction")),
    ("합병", ("merger", "split")),
    ("상장", ("listing", "ipo", "subscription")),
    ("주주총회", ("shareholder", "meeting")),
    ("최대주주", ("major", "shareholder")),
    ("휴장일", ("holiday", "calendar", "business", "day")),
    ("종목", ("stock",)),
    ("종목정보", ("stock", "basic", "info")),
    ("회원사", ("member", "securities", "firm", "brokerage")),
    ("거래원", ("member", "securities", "firm")),
    ("상한가", ("upper", "limit")),
    ("하한가", ("lower", "limit")),
    ("etf", ("etf", "nav")),
    ("관심종목", ("watchlist", "interest")),
    ("조건검색", ("condition", "search")),
    ("구성종목", ("component", "stock", "holdings")),
    ("체결강도", ("execution", "strength", "intensity")),
    ("투자의견", ("investment", "opinion", "analyst")),
    ("목표주가", ("investment", "opinion", "estimate")),
    ("실적", ("earnings", "estimate", "income")),
    ("지지선", ("resistance", "level")),
    ("저항선", ("resistance", "level")),
    ("변동성", ("volatility", "fluctuation")),
    ("급등", ("rapid", "rise", "fluctuation")),
    ("급락", ("rapid", "fall", "fluctuation")),
    ("예상체결", ("expected", "conclusion", "price")),
    # English jargon with no literal match anywhere in the corpus.
    ("moving average", ("chart", "daily", "ohlcv", "period")),
    ("rsi", ("chart", "daily", "ohlcv")),
    ("macd", ("chart", "daily", "ohlcv")),
    ("bollinger", ("chart", "daily", "ohlcv")),
    ("candlestick", ("chart", "daily", "ohlcv")),
    ("technical", ("chart", "daily", "ohlcv")),
    ("valuation", ("per", "pbr", "market", "value", "ratio")),
    ("supply demand", ("investor", "institution", "foreign", "trend")),
    ("screener", ("condition", "search", "ranking")),
    ("screening", ("condition", "search", "ranking")),
)


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


def category_defaults(category: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Seed domains/tags for a category. Fallback only — see `COMMAND_TAXONOMY`."""

    return _CATEGORY_DEFAULTS.get(category, (("market",), ("ranking",)))


def get_command_metadata(*, broker: str, category: str, name: str, qualified_name: str) -> CommandMetadata:
    """Return domain/tag metadata for a generated CLI command."""

    entry = COMMAND_TAXONOMY.get(qualified_name)
    if entry is None:
        default_domains, default_tags = category_defaults(category)
        entry = CommandTaxonomy(default_domains, default_tags)

    return CommandMetadata(
        domains=entry.domains,
        tags=entry.tags,
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

    if category == "chart" and name == "technical":
        return (
            f"{base} This command computes rather than passing a response through: it fetches the daily candles "
            "itself and returns final indicator values and signal rule votes, never the candle series. Prefer it "
            "over fetching OHLCV and reasoning over the rows. The two signal families (trend, mean_reversion) are "
            "reported separately and routinely disagree on a strong trend — read both, plus the per-rule reasons."
        )
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
