from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

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
                agent_notes="Follow with income-statement or ratio commands when deeper financial context is needed.",
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
        ),
        agent_notes="Use this recipe as a broad first pass, then narrow by domain/tag for detailed follow-up.",
    ),
    WorkflowRecipe(
        name="technical-analysis",
        title="Technical Analysis",
        description="Collect chart data for downstream technical indicator calculation.",
        domains=("chart", "technical-indicator"),
        tags=("ohlcv", "daily", "minute"),
        steps=(
            RecipeStep(
                title="Fetch daily OHLCV",
                command=("kis", "chart", "period"),
                purpose="Retrieve period chart data suitable for daily indicators.",
                agent_notes="Run `cluefin-cli ta <stock_code>` for the corresponding technical-indicator report (SMA/EMA/RSI/MACD/Bollinger/Stochastic/ADX/ATR/OBV plus risk metrics).",
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
        agent_notes="Recipes do not run TA indicators directly; use `cluefin-cli ta <stock_code>` after collecting OHLCV arrays.",
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
                title="Shareholder meeting",
                command=("kis", "schedule", "shareholder-meeting"),
                purpose="Find shareholder meeting schedules.",
                agent_notes="Useful for governance and event monitoring workflows.",
            ),
        ),
        agent_notes="Corporate-action APIs are event oriented; always include date windows where the schema supports them.",
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
