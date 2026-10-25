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
                title="Get financial statement",
                command=("kis", "financial", "balance-sheet"),
                purpose="Fetch statement context before ratios or valuation notes.",
                agent_notes="Follow with income-statement or ratio commands when deeper financial context is needed. "
                "KIS rows may stop at last year's annual report; use the latest-earnings recipe for the newest period.",
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
        tags=("technical-indicator", "ohlcv", "daily", "minute"),
        steps=(
            RecipeStep(
                title="Read the indicators",
                command=("kis", "chart", "technical"),
                purpose="Get indicator readings and signal rules for one stock in a single call.",
                agent_notes=(
                    "Start here. The CLI fetches the candles and computes in-process, so the reply is a few dozen "
                    "numbers rather than a few hundred rows. Only fall through to the chart commands below when the "
                    "rows themselves are the deliverable."
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
        agent_notes="Prefer this over kis financial commands whenever the question is about the most recent period; "
        "KIS returns annual rows for many small caps and lags the filing.",
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
