import asyncio
from typing import List

import click
from loguru import logger
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cluefin_cli.data.fundamentals import (
    AccountSnapshot,
    DividendSnapshot,
    DomesticFundamentalDataFetcher,
    IndicatorSnapshot,
    ShareholderSnapshot,
    default_business_year,
)
from cluefin_cli.utils.formatters import format_number

console = Console()

REPORT_CHOICES = {
    "annual": ("11011", "Annual report"),
    "q1": ("11013", "Quarter 1 report"),
    "half": ("11012", "Half-year report"),
    "q3": ("11014", "Quarter 3 report"),
}


@click.command(name="fa")
@click.argument("stock_code")
@click.option(
    "--year",
    default=default_business_year(),
    show_default=True,
    help="Business year (YYYY) to analyse.",
)
@click.option(
    "--report",
    type=click.Choice(list(REPORT_CHOICES.keys()), case_sensitive=False),
    default="annual",
    show_default=True,
    help="DART report period to query.",
)
@click.option(
    "--max-shareholders",
    type=click.IntRange(1, 20),
    default=5,
    show_default=True,
    help="Number of top shareholders to display.",
)
def fundamental_analysis(stock_code: str, year: str, report: str, max_shareholders: int) -> None:
    """Run fundamental analysis for a given stock code using DART OpenAPI data."""
    report_key = report.lower()
    report_code, report_description = REPORT_CHOICES[report_key]

    console.print(
        f"[bold blue]Running fundamental analysis for {stock_code} ({year}, {report_description})[/bold blue]"
    )

    try:
        asyncio.run(_perform_fundamental_analysis(stock_code, year, report_code, max_shareholders))
    except Exception as exc:
        console.print(f"[red]Error while analysing fundamentals: {exc}[/red]")
        logger.exception(f"Fundamental analysis failed for {stock_code}")


async def _perform_fundamental_analysis(stock_code: str, year: str, report_code: str, max_shareholders: int) -> None:
    fetcher = DomesticFundamentalDataFetcher()
    corp_code = await fetcher.get_corp_code(stock_code)
    overview = await fetcher.get_company_overview(corp_code)

    accounts = await fetcher.get_key_accounts(
        corp_code,
        business_year=year,
        report_code=report_code,
    )

    indicators = await fetcher.get_indicators(
        corp_code,
        business_year=year,
        report_code=report_code,
    )

    dividends = await fetcher.get_dividend_information(
        corp_code,
        business_year=year,
        report_code=report_code,
    )
    shareholders = await fetcher.get_major_shareholders(
        corp_code,
        business_year=year,
        report_code=report_code,
    )

    _display_overview(stock_code, corp_code, overview)
    _display_accounts(accounts)
    _display_indicators(indicators)
    _display_dividends(dividends)
    _display_shareholders(shareholders, max_shareholders)


def _display_overview(stock_code: str, corp_code: str, overview) -> None:
    """Render the company overview section."""
    table = Table(show_header=False, box=box.SIMPLE)
    table.add_row("Stock Code", stock_code)
    table.add_row("Corp Code", corp_code)
    table.add_row("Company", overview.corp_name)
    table.add_row("Industry", overview.induty_code or "-")
    table.add_row("CEO", overview.ceo_nm or "-")
    table.add_row("Listing Class", overview.corp_cls or "-")
    table.add_row("Founded", overview.est_dt or "-")
    table.add_row("Fiscal Month", overview.acc_mt or "-")
    table.add_row("Website", overview.hm_url or "-")
    table.add_row("IR Site", overview.ir_url or "-")
    table.add_row("Phone", overview.phn_no or "-")

    console.print("\n[bold green]Company Overview[/bold green]")
    console.print(Panel(table, expand=False))


def _display_accounts(accounts: List[AccountSnapshot]) -> None:
    console.print("\n[bold cyan]Key Financial Accounts[/bold cyan]")
    if not accounts:
        console.print("[yellow]No financial account data available for the selected period.[/yellow]")
        return

    table = Table(box=box.SIMPLE_HEAVY)
    table.add_column("Account")
    table.add_column("Current Period")
    table.add_column("Amount")
    table.add_column("Prior Period")
    table.add_column("Amount")

    for account in accounts:
        table.add_row(
            f"{account.name}\n({account.label})",
            account.current_label or "-",
            _format_amount(account.current_amount, account.currency),
            account.previous_label or "-",
            _format_amount(account.previous_amount, account.currency),
        )

    console.print(Panel(table, expand=False))


def _display_indicators(indicators: List[IndicatorSnapshot]) -> None:
    console.print("\n[bold cyan]Major Financial Indicators[/bold cyan]")

    if not indicators:
        console.print("[yellow]No indicator data available for the selected period.[/yellow]")
        return

    grouped: dict[str, list[IndicatorSnapshot]] = {}
    for indicator in indicators:
        grouped.setdefault(indicator.category, []).append(indicator)

    for category, items in grouped.items():
        table = Table(title=category, box=box.MINIMAL_DOUBLE_HEAD)
        table.add_column("Indicator")
        table.add_column("Value", justify="right")

        for item in items:
            table.add_row(item.name, _format_indicator(item))

        console.print(Panel(table, expand=False))


def _display_dividends(dividends: List[DividendSnapshot]) -> None:
    console.print("\n[bold cyan]Dividend Information[/bold cyan]")

    if not dividends:
        console.print("[yellow]No dividend history reported in the selected filing.[/yellow]")
        return

    table = Table(box=box.SIMPLE)
    table.add_column("Category")
    table.add_column("Current")
    table.add_column("Prior")
    table.add_column("Two Years Ago")
    table.add_column("Stock Type")

    for item in dividends:
        table.add_row(
            item.category,
            item.current or "-",
            item.previous or "-",
            item.two_years_ago or "-",
            item.stock_kind or "-",
        )

    console.print(Panel(table, expand=False))


def _display_shareholders(shareholders: List[ShareholderSnapshot], max_rows: int) -> None:
    console.print("\n[bold cyan]Major Shareholders[/bold cyan]")

    if not shareholders:
        console.print("[yellow]No shareholder disclosures were found for this report.[/yellow]")
        return

    table = Table(box=box.SIMPLE_HEAVY)
    table.add_column("Name")
    table.add_column("Relation")
    table.add_column("Prior Shares", justify="right")
    table.add_column("Prior %", justify="right")
    table.add_column("Current Shares", justify="right")
    table.add_column("Current %", justify="right")

    for item in shareholders[:max_rows]:
        table.add_row(
            item.name,
            item.relation or "-",
            _format_share_value(item.shares_previous),
            item.holding_ratio_previous or "-",
            _format_share_value(item.shares_current),
            item.holding_ratio_current or "-",
        )

    console.print(Panel(table, expand=False))


def _format_amount(value, currency: str | None) -> str:
    if value is None:
        return "-"
    if value == value.to_integral_value():
        formatted = format_number(int(value))
    else:
        formatted = f"{float(value):,.2f}"
    return f"{formatted} {currency}" if currency else formatted


def _format_indicator(item: IndicatorSnapshot) -> str:
    if item.value is None:
        return "-"
    value = float(item.value)
    if item.unit_hint == "%" and value < 1:
        value *= 100
    suffix = item.unit_hint or ""
    return f"{value:,.2f}{suffix}"


def _format_share_value(value: str | None) -> str:
    if value is None:
        return "-"
    normalised = value.replace(",", "").strip()
    if not normalised or not normalised.replace("-", "").isdigit():
        return value
    try:
        return format_number(int(normalised))
    except ValueError:
        return value
