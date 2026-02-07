"""XBRL financial statement analysis command."""

import asyncio

import click
from loguru import logger
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cluefin_cli.data.fundamentals import DomesticFundamentalDataFetcher, default_business_year
from cluefin_cli.data.xbrl import REPORT_CODE_MAP, XbrlStatementFetcher
from cluefin_cli.utils.formatters import format_number

console = Console()

STATEMENT_TYPE_LABELS: dict[str, str] = {
    "BS": "Statement of Financial Position (재무상태표)",
    "IS": "Income Statement (손익계산서)",
    "CIS": "Comprehensive Income Statement (포괄손익계산서)",
    "CF": "Cash Flow Statement (현금흐름표)",
    "SCE": "Statement of Changes in Equity (자본변동표)",
}


@click.command(name="xbrl")
@click.argument("stock_code")
@click.option(
    "--year",
    default=default_business_year(),
    show_default=True,
    help="Business year (YYYY) to analyse.",
)
@click.option(
    "--report",
    type=click.Choice(list(REPORT_CODE_MAP.keys()), case_sensitive=False),
    default="annual",
    show_default=True,
    help="DART report period.",
)
@click.option(
    "--statement-type",
    type=click.Choice(["BS", "IS", "CIS", "CF", "SCE"], case_sensitive=False),
    default=None,
    help="Filter to a specific statement type. Show all if not set.",
)
def xbrl_analysis(stock_code: str, year: str, report: str, statement_type: str | None) -> None:
    """Analyse XBRL financial statements for a given stock code."""
    reprt_code = REPORT_CODE_MAP[report.lower()]

    console.print(f"[bold blue]XBRL Analysis for {stock_code} ({year}, {report})[/bold blue]")

    try:
        asyncio.run(_perform_xbrl_analysis(stock_code, year, reprt_code, statement_type))
    except Exception as exc:
        console.print(f"[red]Error during XBRL analysis: {exc}[/red]")
        logger.exception(f"XBRL analysis failed for {stock_code}")


async def _perform_xbrl_analysis(
    stock_code: str,
    year: str,
    reprt_code: str,
    statement_type: str | None,
) -> None:
    fundamental_fetcher = DomesticFundamentalDataFetcher()
    corp_code = await fundamental_fetcher.get_corp_code(stock_code)

    xbrl_fetcher = XbrlStatementFetcher()

    console.print("[dim]Searching for report filing...[/dim]")
    rcept_no = xbrl_fetcher.find_rcept_no(corp_code, year, reprt_code)
    if rcept_no is None:
        console.print(f"[red]No report filing found for {stock_code} ({year}).[/red]")
        return

    console.print(f"[dim]Downloading XBRL (rcept_no={rcept_no})...[/dim]")
    result = xbrl_fetcher.fetch_statements(corp_code, rcept_no, reprt_code)

    if not result.statements:
        console.print("[yellow]No financial statements found in the XBRL data.[/yellow]")
        return

    target_type = statement_type.upper() if statement_type else None
    displayed = False

    for stmt_key, stmt in result.statements.items():
        if target_type and stmt_key != target_type:
            continue
        _display_statement(stmt_key, stmt)
        displayed = True

    if not displayed and target_type:
        available = ", ".join(result.statements.keys())
        console.print(f"[yellow]Statement type '{target_type}' not found. Available: {available}[/yellow]")


def _display_statement(stmt_key: str, stmt) -> None:
    """Render a single financial statement as a Rich table."""
    title = STATEMENT_TYPE_LABELS.get(stmt_key, stmt_key)
    console.print(f"\n[bold cyan]{title}[/bold cyan]")

    table = Table(box=box.SIMPLE_HEAVY)
    table.add_column("Account", min_width=30)
    table.add_column("Label (KO)", min_width=20)
    table.add_column("Value", justify="right", min_width=15)
    table.add_column("Unit", min_width=6)
    table.add_column("Period", min_width=12)

    for item in stmt.line_items:
        indent = "  " * item.depth
        concept = f"{indent}{item.concept_local_name}"

        label_ko = item.label_ko or ""
        if item.is_abstract:
            concept = f"[bold]{concept}[/bold]"
            label_ko = f"[bold]{label_ko}[/bold]" if label_ko else ""

        value_str = "-"
        if item.value is not None:
            try:
                value_str = format_number(int(item.value))
            except (ValueError, OverflowError):
                value_str = str(item.value)

        unit_str = item.unit or ""
        period_str = _format_period(item.period)

        table.add_row(concept, label_ko, value_str, unit_str, period_str)

    console.print(Panel(table, expand=False))


def _format_period(period) -> str:
    """Format an XbrlPeriod for display."""
    if period is None:
        return "-"
    if period.instant is not None:
        return str(period.instant)
    if period.start_date is not None and period.end_date is not None:
        return f"{period.start_date}~{period.end_date}"
    return "-"
