from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from cluefin_openapi_cli.registry import RegistryProtocol


@dataclass(frozen=True, slots=True)
class RecipeStep:
    title: str
    command: tuple[str, ...]
    purpose: str
    agent_notes: str


@dataclass(frozen=True, slots=True)
class WorkflowRecipe:
    name: str
    title: str
    description: str
    domains: tuple[str, ...]
    tags: tuple[str, ...]
    steps: tuple[RecipeStep, ...]
    agent_notes: str


_RECIPES: tuple[WorkflowRecipe, ...] = (
    WorkflowRecipe(
        name="stock-research",
        title="Stock Research",
        description="Collect quote, company, financial, disclosure, and flow context for one Korean stock.",
        domains=("quote", "statements", "news", "trading-flow"),
        tags=("current-price", "financial-statement", "disclosure", "foreign", "institution"),
        steps=(
            RecipeStep(
                title="Get current quote",
                command=("kis", "stock", "current-price"),
                purpose="Start with the latest KIS current-price snapshot.",
                agent_notes="Use the target stock code as a required parameter.",
            ),
            RecipeStep(
                title="Get company basics",
                command=("kis", "stock", "basic-info"),
                purpose="Resolve basic stock identity and listing context.",
                agent_notes="Compare with DART corp-code lookup when a DART workflow needs corp_code.",
            ),
            RecipeStep(
                title="Summarize financials",
                command=("dart", "financial-summary"),
                purpose="Fetch quarters, fiscal years and ratios before valuation notes.",
                agent_notes="Needs the 8-digit DART corp_code (dart corp-code-lookup). It costs 8 DART calls; call "
                "it once and reuse the output.",
            ),
            RecipeStep(
                title="Search disclosures",
                command=("dart", "disclosure-search"),
                purpose="Find recent DART disclosures for the issuer.",
                agent_notes="Use corp_code or date filters to reduce result size.",
            ),
            RecipeStep(
                title="Check investor flow",
                command=("kis", "analysis", "institutional-foreign"),
                purpose="Add foreign and institutional trading-flow context.",
                agent_notes="Check date fields before comparing with price movement.",
            ),
            RecipeStep(
                title="Summarize broker targets",
                command=("kis", "stock", "opinion-summary"),
                purpose="Each broker's latest rating and target price in the window, with mean/median/max/min.",
                agent_notes="Default window is 90 days. This is the cross-broker view; kis stock estimated-earnings is one "
                "brokerage's estimate, not a consensus.",
            ),
            RecipeStep(
                title="Value at the current price",
                command=("kis", "stock", "valuation"),
                purpose="Market cap, TTM PER, PBR and PER on the KIS estimate years from the close, DART share count "
                "and DART statements.",
                agent_notes="Needs corp_code as well as stock_code (resolve with dart corp-code-lookup once). Costs ~11 "
                "calls; call once and reuse. Do not recompute its multiples from other sources.",
            ),
        ),
        agent_notes="Use this recipe as a broad first pass, then narrow by domain/tag for detailed follow-up.",
    ),
    WorkflowRecipe(
        name="technical-analysis",
        title="Technical Analysis",
        description="Read technical indicator signals for one stock, or collect the raw chart data behind them.",
        domains=("chart",),
        tags=("technical-indicator", "trend-template", "ohlcv", "daily", "minute"),
        steps=(
            RecipeStep(
                title="Read the indicators",
                command=("kis", "chart", "technical"),
                purpose="Get indicator readings and signal rules for one stock in a single call.",
                agent_notes=(
                    "Start here. The CLI fetches the candles and computes in-process, so the reply is a few dozen "
                    "numbers rather than a few hundred rows. Only fall through to the chart commands below when the "
                    "rows themselves are the deliverable. `stop_sizing` gives the per-horizon stop-width floor "
                    "(1.5 × ATR14 × √(h/30)) with buy/sell stop prices and `verdict_cap: watch` past 20% — use "
                    "it instead of computing the stop; pass `--horizon-days 20,40,60` to choose horizons."
                ),
            ),
            RecipeStep(
                title="Judge the breakout setup",
                command=("kis", "chart", "trend-setup"),
                purpose="Trend template, 52-week range, fractal pivot, strength vs. index and watchlist group 1/2/3.",
                agent_notes=(
                    "Use for 'is this stock waiting at a breakout' questions. The rules are a backtest's, not "
                    "ta-lib's: its atr14_pct is a plain mean and differs from `technical`'s Wilder ATR. For every "
                    "stock on a day, `cache trend-setup` reads the local cache instead of calling KIS."
                ),
            ),
            RecipeStep(
                title="Fetch daily OHLCV",
                command=("kis", "chart", "period"),
                purpose="Retrieve period chart data suitable for daily indicators.",
                agent_notes="Use this when the candle rows themselves are needed. For indicator readings alone, `kis chart technical` fetches and computes in one call and returns no rows.",
            ),
            RecipeStep(
                title="Fetch intraday OHLCV",
                command=("kis", "chart", "minute"),
                purpose="Retrieve minute chart data when intraday analysis is needed.",
                agent_notes="Keep interval and date window consistent before comparing to daily signals.",
            ),
            RecipeStep(
                title="Fallback chart source",
                command=("kiwoom", "chart", "tick"),
                purpose="Use Kiwoom chart data when KIS coverage or parameters are insufficient.",
                agent_notes="Normalize provider response shape before TA calculation.",
            ),
        ),
        agent_notes="Start with `kis chart technical`: it returns SMA/RSI/MACD/Bollinger/Stochastic/ADX/ATR/OBV readings plus signal rules without putting a candle series in context. Fall back to these chart commands when the rows themselves are needed.",
    ),
    WorkflowRecipe(
        name="market-scan",
        title="Market Scan",
        description="Screen ranking, sector, theme, and volume signals for market-wide ideas.",
        domains=("market", "sector", "theme"),
        tags=("ranking", "volume-rank", "sector-index", "theme-group"),
        steps=(
            RecipeStep(
                title="Volume ranking",
                command=("kis", "ranking", "volume"),
                purpose="Find high-volume stocks from KIS ranking data.",
                agent_notes="Use market and ranking parameters to keep scans comparable.",
            ),
            RecipeStep(
                title="Sector index",
                command=("kis", "sector", "current-index"),
                purpose="Add sector-level market context.",
                agent_notes="Combine with sector daily or period commands for trend context.",
            ),
            RecipeStep(
                title="Theme groups",
                command=("kiwoom", "theme", "group"),
                purpose="Discover Kiwoom theme groups for thematic scans.",
                agent_notes="Follow with theme group-stocks for constituents.",
            ),
        ),
        agent_notes="Use ranking outputs as candidates; verify with quote/chart commands before drawing conclusions.",
    ),
    WorkflowRecipe(
        name="corporate-actions",
        title="Corporate Actions",
        description="Discover dividend, issuance, split, merger, listing, and meeting events.",
        domains=("corporate-actions", "market-calendar"),
        tags=("dividend", "capital-increase", "capital-reduction", "merger-split", "shareholder-meeting"),
        steps=(
            RecipeStep(
                title="Dividend decisions",
                command=("kis", "schedule", "dividend"),
                purpose="Find cash dividend decision events.",
                agent_notes="Use date ranges to scope event searches.",
            ),
            RecipeStep(
                title="Capital increase",
                command=("kis", "schedule", "capital-increase"),
                purpose="Find paid-in capital increase schedules.",
                agent_notes="Cross-check with disclosure search for issuer filings.",
            ),
            RecipeStep(
                title="Merger or split",
                command=("kis", "schedule", "merger-split"),
                purpose="Find merger and split decision schedules.",
                agent_notes="Use DART disclosures for original filings when material.",
            ),
            RecipeStep(
                title="Decision filing body",
                command=("dart", "major-event"),
                purpose="Read the structured body of one company's decision filings: amount, conversion or issue "
                "price, counterparty, purpose of funds.",
                agent_notes="One event type per call (convertible-bond, rights-offering, merger ...). Schedules above "
                "list events market-wide; this reads one issuer's filing as filed.",
            ),
            RecipeStep(
                title="Shareholder meeting",
                command=("kis", "schedule", "shareholder-meeting"),
                purpose="Find shareholder meeting schedules.",
                agent_notes="Useful for governance and event monitoring workflows.",
            ),
        ),
        agent_notes="Corporate-action APIs are event oriented; always include date windows where the schema supports them.",
    ),
    WorkflowRecipe(
        name="latest-earnings",
        title="Latest Earnings",
        description="Read the newest reported half-year or quarterly results of one stock from the DART filing itself.",
        domains=("statements", "news"),
        tags=("financial-statement", "disclosure"),
        steps=(
            RecipeStep(
                title="Resolve corp_code",
                command=("dart", "corp-code-lookup"),
                purpose="Map the 6-digit stock code to the 8-digit DART corp_code.",
                agent_notes="Pass --stock-code; every DART report command needs corp_code, not the stock code.",
            ),
            RecipeStep(
                title="Find the newest periodic report",
                command=("dart", "disclosure-search"),
                purpose="See which business year and report type (annual, H1, Q1, Q3) was filed most recently.",
                agent_notes="Use --pblntf-ty A with --corp-code and a recent --bgn-de; the report name tells you the reprt_code to use next.",
            ),
            RecipeStep(
                title="Read major accounts",
                command=("dart", "financial-major-accounts"),
                purpose="Get revenue, operating income and net income straight from that report.",
                agent_notes="In quarterly reports thstrm_amount is the single quarter and thstrm_add_amount the year-to-date "
                "sum; compare year-to-date against frmtrm_add_amount, never against the annual row.",
            ),
            RecipeStep(
                title="Summarize quarters, years and ratios",
                command=("dart", "financial-summary"),
                purpose="Get the last 8 single quarters with YoY, three fiscal years with ratios, the latest "
                "year-to-date period and TTM sums computed from the full statements, in 억원.",
                agent_notes="One call replaces reading several reports and deriving quarters by hand; do not recompute "
                "its figures. It costs 8 DART calls, so call it once per company and reuse the output.",
            ),
        ),
        agent_notes="DART is the only source for statements and ratios; KIS retired its 종목분석 financial APIs "
        "on 2026-11-11.",
    ),
    WorkflowRecipe(
        name="filing-text",
        title="Read a Periodic Report's Text",
        description="Read what the numbers do not say from the filing itself: business description (segments, "
        "products, orders, raw materials) and financial statement notes (borrowings, related parties, contingencies).",
        domains=("statements",),
        tags=("filing-text", "disclosure"),
        steps=(
            RecipeStep(
                title="Find the periodic report",
                command=("dart", "disclosure-search"),
                purpose="Get the rcept_no of the newest 사업·반기·분기보고서.",
                agent_notes="Use --corp-code with --pblntf-ty A and a recent --bgn-de. Filings before 2017 are not "
                "supported by the text commands.",
            ),
            RecipeStep(
                title="Outline the filing",
                command=("dart", "document-outline"),
                purpose="See every section of the report and its attached audit reports, with sizes.",
                agent_notes="Pass the same --corp-code: a wrong rcept_no returns another company's filing, which the "
                "command rejects with exit 4. `chars` tells you whether a section fits in one call.",
            ),
            RecipeStep(
                title="Read the business description",
                command=("dart", "document-section"),
                purpose="Read II. 사업의 내용 or one of its subsections as paragraphs and tables.",
                agent_notes="Start with --section business-overview; the whole business section of a large cap is "
                "~40k characters, so pick subsections by --index from the outline instead of raising --max-chars.",
            ),
            RecipeStep(
                title="Read financial statement notes",
                command=("dart", "financial-notes"),
                purpose="List the notes, then read only the ones you need.",
                agent_notes="Call once without filters for the table of contents and its warnings, then pass "
                "--title-contains 차입금,특수관계자,우발 or --notes with numbers from that list.",
            ),
        ),
        agent_notes="Every step downloads the filing again; keep the rcept_no and corp_code from the first steps. "
        "Table amounts are strings as filed and the table's `unit` is not applied.",
    ),
    WorkflowRecipe(
        name="us-peer-filings",
        title="Read a US Customer's or Competitor's Filings",
        description="Read the SEC filings of a US company that bears on a Korean stock: risk factors and MD&A "
        "(demand, capex, inventory guidance) from the 10-K/10-Q, and the latest quarter from the 8-K earnings release.",
        domains=("statements",),
        tags=("us-filing", "risk-factors", "earnings-release"),
        steps=(
            RecipeStep(
                title="Resolve the ticker",
                command=("sec", "company-lookup"),
                purpose="Get the company's CIK from its US ticker.",
                agent_notes="Pass --ticker (BRK.B and BRK-B both work). Korean companies' own filings are in dart.",
            ),
            RecipeStep(
                title="List recent filings",
                command=("sec", "filings"),
                purpose="Pick the newest 10-K or 10-Q, or the newest 8-K with item 2.02 (results).",
                agent_notes="Use --forms 10-K or --forms 10-Q, or --forms 8-K --items 2.02. If the hint lists only "
                "20-F/6-K, the company is a foreign private issuer and sec filing-items cannot read it.",
            ),
            RecipeStep(
                title="Outline the report",
                command=("sec", "filing-items"),
                purpose="See which Items the filing has, their sizes and whether any boundary is uncertain.",
                agent_notes="Call without --items first. Distrust an Item with `uncertain: true` or warnings; "
                "an `incorporated_by_reference` Item holds only a pointer to another document.",
            ),
            RecipeStep(
                title="Read the Items",
                command=("sec", "filing-items"),
                purpose="Read 1A (risk factors) and 7 (MD&A) of a 10-K, or II:1A and I:2 of a 10-Q.",
                agent_notes="Pass --items 1A,7. Text is cut at --max-chars (default 40000); continue one Item at a "
                "time with --items <key> --offset-chars <next_offset>.",
            ),
            RecipeStep(
                title="Read the earnings release",
                command=("sec", "filing-exhibit"),
                purpose="Read the 8-K's EX-99.1 press release: revenue, margins and next-quarter guidance tables.",
                agent_notes="Use the accession_number of the 8-K with item 2.02; the 8-K body itself only points "
                "to the exhibit. --include-tables true adds column-aligned grids.",
            ),
        ),
        agent_notes="Each command downloads the filing again; keep the cik and accession_number from the first "
        "steps. Amounts are strings as filed and table units are not applied.",
    ),
    WorkflowRecipe(
        name="disclosure-monitoring",
        title="Disclosure Monitoring",
        description="Monitor market announcements and DART disclosures.",
        domains=("news", "market"),
        tags=("announcement", "disclosure"),
        steps=(
            RecipeStep(
                title="Market announcements",
                command=("kis", "market", "announcement"),
                purpose="Fetch KIS market news and announcement titles.",
                agent_notes="Use as a quick title-level monitor.",
            ),
            RecipeStep(
                title="DART disclosure search",
                command=("dart", "disclosure-search"),
                purpose="Search formal DART disclosures.",
                agent_notes="Use corp_code and date filters when monitoring a specific issuer.",
            ),
            RecipeStep(
                title="Major-event report body",
                command=("dart", "major-event"),
                purpose="Read a major-event report (pblntf_ty B) found by the search as structured fields.",
                agent_notes="Map report_nm to an event type (전환사채권발행결정 → convertible-bond) and pass the "
                "rcept_dt as both bgn_de and end_de.",
            ),
            RecipeStep(
                title="DART company overview",
                command=("dart", "company-overview"),
                purpose="Resolve issuer context for DART results.",
                agent_notes="Requires corp_code from lookup or known issuer mapping.",
            ),
        ),
        agent_notes="Use KIS for title-level discovery and DART for formal disclosure records.",
    ),
    WorkflowRecipe(
        name="macro-context",
        title="Macro Context",
        description="Read the Korean macro backdrop (rates, credit, KRW, prices, cycle, sentiment, growth, exports) "
        "and dig into any indicator a call depends on.",
        domains=("macro", "market"),
        tags=("macro-indicator", "economic-series", "statistic-catalog"),
        steps=(
            RecipeStep(
                title="Macro snapshot",
                command=("ecos", "macro-snapshot"),
                purpose="Every headline indicator and spread with its latest value, 1m/3m/1y change and 10-year "
                "percentile, in one call.",
                agent_notes="Needs ECOS_AUTH_KEY. Read each row's as_of: monthly data lags weeks. There is no regime "
                "label on purpose — name the readings your call rests on (e.g. leading_cycle falling for 3 months, "
                "credit_spread_aa at a high percentile) instead of a one-word regime.",
            ),
            RecipeStep(
                title="Find a table",
                command=("ecos", "table-search"),
                purpose="Locate the ECOS table for an indicator the snapshot does not carry (e.g. 업종별 BSI, "
                "생산자물가, 주택가격).",
                agent_notes="Every query term must match the table name. The list is downloaded on every call.",
            ),
            RecipeStep(
                title="Pick item codes",
                command=("ecos", "items"),
                purpose="Get the item codes and the latest period on file (end_time) for that table.",
                agent_notes="A table with a Group2 needs a code from each group, in group order; otherwise rows for "
                "every sub-item come back mixed.",
            ),
            RecipeStep(
                title="Read the series",
                command=("ecos", "series"),
                purpose="The indicator's history in the cycle's period format.",
                agent_notes="Periods: D 20240101, M 202401, Q 2024Q1, A 2024. max_rows keeps the most recent rows.",
            ),
        ),
        agent_notes="Macro explains the backdrop, not a single stock: say which reading matters for this company and "
        "through which channel (KRW for exporters, rates for lenders and growth multiples, credit spreads for leveraged "
        "issuers). Do not substitute web search for these numbers.",
    ),
    WorkflowRecipe(
        name="outlook",
        title="Outlook Scenarios",
        description="Build bear/base/bull probability-weighted price scenarios for one stock from the industry "
        "backdrop, what the market price already implies, and value-investor quality metrics.",
        domains=("statements", "macro"),
        tags=("valuation", "implied-expectations", "macro-indicator", "investor-quality", "financial-ratio"),
        steps=(
            RecipeStep(
                title="Read the industry outlook",
                command=("ecos", "industry-outlook"),
                purpose="BSI outlook/actual, production/shipment/inventory yoy and the inventory cycle, plus a "
                "representative product's export and producer prices, for one manufacturing KSIC division.",
                agent_notes="Needs --induty-code (a KSIC manufacturing division C10-C33, e.g. 26 for "
                "전자부품,컴퓨터,영상음향및통신장비). Needs ECOS_AUTH_KEY; if it is invalid, skip this step and say "
                "so instead of filling the industry reading from elsewhere.",
            ),
            RecipeStep(
                title="Read market-implied expectations",
                command=("kis", "stock", "implied-expectations"),
                purpose="Reverse-engineer today's price into an implied permanent ROE (RIM) and an implied revenue "
                "growth rate (reverse DCF), against DART's own 3-year ROE/growth and the KIS research estimate.",
                agent_notes="Needs stock_code and corp_code; ~14 calls, call once and reuse. Numbers and "
                "assumptions only — it gives no cheap/expensive label.",
            ),
            RecipeStep(
                title="Read the valuation band",
                command=("kis", "stock", "valuation-band"),
                purpose="5-year PER/PBR percentile band (min/p25/median/p75/max) and the current multiple's "
                "percentile in that band.",
                agent_notes="Needs `cache load` to have filled the local price cache first. `current` divides by "
                "the prior fiscal year's EPS/BPS, so it differs from `kis stock valuation`'s TTM PER/PBR — "
                "never mix the two in one scenario note.",
            ),
            RecipeStep(
                title="Read investor-quality metrics",
                command=("kis", "stock", "investor-metrics"),
                purpose="FCF yield, owner earnings, EV/EBIT and earnings yield, PEG (DART and KIS), shareholder "
                "yield and Altman Z at the current close.",
                agent_notes="Missing figures come back as `null` with a `reason`. Owner earnings is often null at "
                "large filers that omit D&A. Shareholder yield treats a missing cash-flow line as zero and flags "
                "it in `assumed_zero` instead of dropping it.",
            ),
            RecipeStep(
                title="Read the quality block",
                command=("dart", "financial-summary"),
                purpose="ROIC, DuPont decomposition, accruals and F-Score/Altman Z'' from the same call's "
                "`quality` block.",
                agent_notes="Reuse the latest-earnings recipe's call instead of calling this again in the same "
                "session — it costs 8 DART calls.",
            ),
        ),
        agent_notes="This recipe covers the RPC-backed steps only. The historical base rate (`cache base-rate`, "
        "percentile of similar past setups) and the macro-beta check (`cache macro-beta`, discard a factor when "
        "its t-value is small) are local cache subcommands outside this registry — call them directly alongside "
        "these steps, starting scenario probabilities from the base-rate percentiles and adjusting them by the "
        "gap between the industry outlook/implied expectations and that base rate.",
    ),
)


def list_recipes() -> list[WorkflowRecipe]:
    return sorted(_RECIPES, key=lambda recipe: recipe.name)


def get_recipe(name: str) -> WorkflowRecipe | None:
    for recipe in _RECIPES:
        if recipe.name == name:
            return recipe
    return None


def recipe_summaries() -> list[dict[str, object]]:
    return [
        {
            "name": recipe.name,
            "title": recipe.title,
            "description": recipe.description,
            "domains": list(recipe.domains),
            "tags": list(recipe.tags),
            "step_count": len(recipe.steps),
        }
        for recipe in list_recipes()
    ]


def iter_recipe_command_paths() -> Iterable[tuple[str, ...]]:
    for recipe in _RECIPES:
        for step in recipe.steps:
            yield step.command


def validate_recipe_commands(registry: RegistryProtocol) -> list[tuple[str, ...]]:
    return [path for path in iter_recipe_command_paths() if registry.resolve_command(path) is None]
