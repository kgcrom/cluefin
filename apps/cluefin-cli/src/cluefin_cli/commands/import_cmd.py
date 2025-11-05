"""Import command for stock chart data."""

import sys
from datetime import datetime
from typing import Optional

import click
from cluefin_openapi.kiwoom._auth import Auth as KiwoomAuth
from cluefin_openapi.kiwoom._client import Client as KiwoomClient
from loguru import logger
from pydantic import SecretStr
from rich.console import Console
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TextColumn
from rich.table import Table

from cluefin_cli.config.settings import settings
from cluefin_cli.data.duckdb_manager import DuckDBManager
from cluefin_cli.data.importer import StockChartImporter
from cluefin_cli.data.industry_chart_importer import IndustryChartImporter
from cluefin_cli.data.industry_importer import IndustryCodeImporter
from cluefin_cli.data.stock_fetcher import StockListFetcher

console = Console()
stderr_console = Console(stderr=True)


@click.command(name="import")
@click.argument("stock_codes", nargs=-1, default=None)
@click.option(
    "--from-stdin",
    is_flag=True,
    help="Read stock codes from stdin (for pipeline integration)",
)
@click.option(
    "--list-stocks",
    is_flag=True,
    help="List all available stock codes to stdout (for piping)",
)
@click.option(
    "--market",
    type=click.Choice(["kospi", "kosdaq"], case_sensitive=False),
    default=None,
    help="Filter by market (KOSPI or KOSDAQ)",
)
@click.option(
    "--frequency",
    "-f",
    type=click.Choice(["daily", "weekly", "monthly", "all"], case_sensitive=False),
    multiple=True,
    default=("all",),
    help="Chart data frequencies to import (can specify multiple times)",
)
@click.option(
    "--start",
    type=str,
    default=None,
    help="Start date in YYYYMMDD format (default: 3 years ago)",
)
@click.option(
    "--end",
    type=str,
    default=None,
    help="End date in YYYYMMDD format (default: today)",
)
@click.option(
    "--show-progress",
    is_flag=True,
    help="Show progress bar during import",
)
@click.option(
    "--skip-existing",
    is_flag=True,
    default=True,
    help="Skip import if data already exists",
)
@click.option(
    "--check-db",
    is_flag=True,
    help="Show database statistics and exit",
)
@click.option(
    "--clear-db",
    is_flag=True,
    help="Clear all data from database",
)
@click.option(
    "--industry-codes",
    is_flag=True,
    help="Import industry codes for all market types",
)
@click.option(
    "--industry-charts",
    is_flag=True,
    help="Import industry chart data (positional args are industry codes)",
)
def import_command(
    stock_codes: tuple,
    from_stdin: bool,
    list_stocks: bool,
    market: Optional[str],
    frequency: tuple,
    start: Optional[str],
    end: Optional[str],
    show_progress: bool,
    skip_existing: bool,
    check_db: bool,
    clear_db: bool,
    industry_codes: bool,
    industry_charts: bool,
):
    """Import stock chart data from Kiwoom API to DuckDB.

    Examples:
        # Import 3 years of data for specific stocks
        cluefin-cli import 005930 035720

        # Import all KOSPI stocks
        cluefin-cli import --market kospi

        # Import from stdin (pipeline)
        echo "005930\\n035720" | cluefin-cli import --from-stdin

        # List stocks for piping
        cluefin-cli import --list-stocks --market kosdaq

        # Custom date range
        cluefin-cli import 005930 --start 20220101 --end 20251023

        # Show database statistics
        cluefin-cli import --check-db
    """
    if not settings.kiwoom_app_key:
        raise ValueError("KIWOOM_APP_KEY environment variable is required")
    if not settings.kiwoom_secret_key:
        raise ValueError("KIWOOM_SECRET_KEY environment variable is required")
    if not settings.kiwoom_env:
        raise ValueError("KIWOOM_ENV environment variable is required")
    db_manager = None
    try:
        # Initialize components
        db_manager = DuckDBManager()
        auth = KiwoomAuth(
            app_key=settings.kiwoom_app_key,
            secret_key=SecretStr(settings.kiwoom_secret_key),
            env=settings.kiwoom_env,
        )
        token = auth.generate_token()
        kiwoom_client = KiwoomClient(
            token=token.get_token(),
            env=settings.kiwoom_env,
        )
        stock_fetcher = StockListFetcher(kiwoom_client, db_manager)
        importer = StockChartImporter(kiwoom_client, db_manager)
        industry_importer = IndustryCodeImporter(kiwoom_client, db_manager)
        industry_chart_importer = IndustryChartImporter(kiwoom_client, db_manager)

        # Handle database operations
        if check_db:
            _show_database_stats(db_manager)
            return

        if clear_db:
            db_manager.clear_all_tables(confirm=True)
            return

        # Handle industry codes import
        if industry_codes:
            _import_industry_codes(industry_importer, market)
            _show_database_stats(db_manager)
            return

        # Handle industry chart import
        if industry_charts:
            # Collect industry codes
            codes_to_import = _collect_industry_codes(
                industry_codes=stock_codes,  # Reusing parameter name
                db_manager=db_manager,
            )

            if not codes_to_import:
                console.print("[yellow]No industry codes specified for import[/yellow]")
                return

            # Process frequencies
            frequencies = _process_frequencies(frequency)

            # Get date range
            start_date, end_date = _get_date_range(start, end)

            # Display summary
            _display_industry_import_summary(codes_to_import, frequencies, start_date, end_date, skip_existing)

            # Run import
            _run_industry_import(
                industry_chart_importer,
                codes_to_import,
                start_date,
                end_date,
                frequencies,
                skip_existing,
                show_progress,
            )

            # Display final statistics
            _show_database_stats(db_manager)
            return

        # Handle list-stocks operation
        if list_stocks:
            _list_stocks(stock_fetcher, market)
            return

        # Collect stock codes
        codes_to_import = _collect_stock_codes(
            stock_codes=stock_codes,
            from_stdin=from_stdin,
            market=market,
            stock_fetcher=stock_fetcher,
        )

        if not codes_to_import:
            console.print("[yellow]No stock codes specified for import[/yellow]")
            return

        # Process frequencies
        frequencies = _process_frequencies(frequency)

        # Get date range
        start_date, end_date = _get_date_range(start, end)

        # Display summary
        _display_import_summary(codes_to_import, frequencies, start_date, end_date, skip_existing)

        # Run import
        _run_import(
            importer,
            codes_to_import,
            start_date,
            end_date,
            frequencies,
            skip_existing,
            show_progress,
        )

        # Display final statistics
        _show_database_stats(db_manager)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        logger.error(f"Import error: {e}")
        sys.exit(1)
    finally:
        if db_manager:
            db_manager.close()


def _collect_stock_codes(
    stock_codes: tuple,
    from_stdin: bool,
    market: Optional[str],
    stock_fetcher: StockListFetcher,
) -> list[str]:
    """Collect stock codes from various sources.

    Args:
        stock_codes: Stock codes from CLI arguments
        from_stdin: Whether to read from stdin
        market: Market filter
        stock_fetcher: Stock fetcher instance

    Returns:
        List of stock codes to import
    """
    codes = []

    # From stdin
    if from_stdin:
        console.print("[yellow]Reading stock codes from stdin...[/yellow]")
        for line in sys.stdin:
            code = line.strip()
            if code and len(code) == 6 and code.isdigit():
                codes.append(code)
        logger.info(f"Read {len(codes)} stock codes from stdin")

    # From API if no codes specified
    elif not stock_codes:
        console.print("[yellow]Fetching available stocks from Kiwoom API...[/yellow]")
        codes = [item.code for item in stock_fetcher.get_all_stocks(market=market)]

    # From arguments
    else:
        codes = list(stock_codes)

    return sorted(set(codes))


def _process_frequencies(frequency: tuple) -> list[str]:
    """Process frequency options.

    Args:
        frequency: Raw frequency tuple from CLI

    Returns:
        List of normalized frequencies
    """
    if not frequency or frequency == ("all",):
        return ["daily", "weekly", "monthly"]

    result = []
    for f in frequency:
        f_lower = f.lower()
        if f_lower == "all":
            return ["daily", "weekly", "monthly"]
        elif f_lower in ["daily", "weekly", "monthly"]:
            result.append(f_lower)

    return sorted(set(result)) if result else ["daily", "weekly", "monthly"]


def _get_date_range(start: Optional[str], end: Optional[str]) -> tuple[str, str]:
    """Get and validate date range.

    Args:
        start: Start date (YYYYMMDD)
        end: End date (YYYYMMDD)

    Returns:
        Tuple of (start_date, end_date) in YYYYMMDD format
    """
    if not start or not end:
        start_date, end_date = StockChartImporter.get_default_date_range()
        if not start:
            start = start_date
        if not end:
            end = end_date

    # Validate dates
    try:
        datetime.strptime(start, "%Y%m%d")
        datetime.strptime(end, "%Y%m%d")
    except ValueError as e:
        raise ValueError(f"Invalid date format. Use YYYYMMDD format. Error: {e}") from e

    return (start, end)


def _display_import_summary(
    stock_codes: list[str],
    frequencies: list[str],
    start_date: str,
    end_date: str,
    skip_existing: bool,
) -> None:
    """Display import summary before starting.

    Args:
        stock_codes: List of stock codes to import
        frequencies: List of frequencies
        start_date: Start date
        end_date: End date
        skip_existing: Whether to skip existing data
    """
    summary_table = Table(title="Import Summary")
    summary_table.add_column("Parameter", style="cyan")
    summary_table.add_column("Value", style="magenta")

    summary_table.add_row("Stock Codes", str(len(stock_codes)))
    summary_table.add_row("Frequencies", ", ".join(frequencies))
    summary_table.add_row("Start Date", start_date)
    summary_table.add_row("End Date", end_date)
    summary_table.add_row("Skip Existing", "Yes" if skip_existing else "No")

    console.print(summary_table)


def _run_import(
    importer: StockChartImporter,
    stock_codes: list[str],
    start_date: str,
    end_date: str,
    frequencies: list[str],
    skip_existing: bool,
    show_progress: bool,
) -> None:
    """Run the import process.

    Args:
        importer: Chart importer instance
        stock_codes: Stock codes to import
        start_date: Start date
        end_date: End date
        frequencies: Frequencies to import
        skip_existing: Skip existing data
        show_progress: Show progress bar
    """
    if show_progress:
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as progress:
            task = progress.add_task("[cyan]Importing stocks...", total=len(stock_codes))

            def update_progress(current: int, total: int, stock_code: str):
                progress.update(task, advance=1, description=f"[cyan]Processing {stock_code}...")

            importer.import_batch(
                stock_codes,
                start_date,
                end_date,
                frequencies,
                progress_callback=update_progress,
                skip_existing=skip_existing,
            )
    else:
        importer.import_batch(
            stock_codes,
            start_date,
            end_date,
            frequencies,
            skip_existing=skip_existing,
        )

    console.print("[green]✓[/green] Import completed successfully")


def _import_industry_codes(industry_importer: IndustryCodeImporter, market: Optional[str]) -> None:
    """Import industry codes from Kiwoom API.

    Args:
        industry_importer: Industry code importer instance
        market: Market filter (kospi or kosdaq)
    """
    console.print("[yellow]Importing industry codes from Kiwoom API...[/yellow]")

    # Map market filter to market types
    market_type = None
    if market:
        market_lower = market.lower()
        if market_lower == "kospi":
            market_type = "0"
        elif market_lower == "kosdaq":
            market_type = "1"

    # Import industry codes
    results = industry_importer.import_industry_codes(market_type=market_type)

    # Display results
    results_table = Table(title="Industry Code Import Results")
    results_table.add_column("Market", style="cyan")
    results_table.add_column("Count", style="magenta", justify="right")

    for market_name, count in results.items():
        if market_name != "total":
            results_table.add_row(market_name, str(count))

    if "total" in results:
        results_table.add_row("", "", style="dim")
        results_table.add_row("TOTAL", str(results["total"]), style="bold green")

    console.print(results_table)
    console.print(f"[green]✓[/green] Imported {results.get('total', 0)} industry codes successfully")


def _list_stocks(stock_fetcher: StockListFetcher, market: Optional[str]) -> None:
    """List available stocks to stdout.

    Args:
        stock_fetcher: Stock fetcher instance
        market: Market filter
    """
    stderr_console.print("[yellow]Fetching stock list from Kiwoom API...[/yellow]")
    stocks = stock_fetcher.get_all_stocks(market=market)

    for stock in stocks:
        stock_fetcher.fetch_stock_metadata_extended(stock)

    stderr_console.print(f"[green]✓[/green] Listed {len(stocks)} stocks")


def _collect_industry_codes(
    industry_codes: tuple,
    db_manager: DuckDBManager,
) -> list[str]:
    """Collect industry codes from arguments or database.

    Args:
        industry_codes: Industry codes from CLI arguments
        db_manager: DuckDB manager instance

    Returns:
        List of industry codes to import
    """
    codes = []

    # If codes specified, use them
    if industry_codes:
        codes = list(industry_codes)
    else:
        # Otherwise, get all industry codes from database
        console.print("[yellow]Fetching all industry codes from database...[/yellow]")
        industry_df = db_manager.get_industry_codes()
        if not industry_df.empty:
            codes = industry_df["code"].tolist()
            logger.info(f"Found {len(codes)} industry codes in database")
        else:
            console.print(
                "[yellow]No industry codes found in database. "
                "Please run 'cluefin-cli import --industry-codes' first.[/yellow]"
            )

    return sorted(set(codes))


def _display_industry_import_summary(
    industry_codes: list[str],
    frequencies: list[str],
    start_date: str,
    end_date: str,
    skip_existing: bool,
) -> None:
    """Display industry import summary before starting.

    Args:
        industry_codes: List of industry codes to import
        frequencies: List of frequencies
        start_date: Start date
        end_date: End date
        skip_existing: Whether to skip existing data
    """
    summary_table = Table(title="Industry Chart Import Summary")
    summary_table.add_column("Parameter", style="cyan")
    summary_table.add_column("Value", style="magenta")

    summary_table.add_row("Industry Codes", str(len(industry_codes)))
    summary_table.add_row("Frequencies", ", ".join(frequencies))
    summary_table.add_row("Start Date", start_date)
    summary_table.add_row("End Date", end_date)
    summary_table.add_row("Skip Existing", "Yes" if skip_existing else "No")

    console.print(summary_table)


def _run_industry_import(
    importer: IndustryChartImporter,
    industry_codes: list[str],
    start_date: str,
    end_date: str,
    frequencies: list[str],
    skip_existing: bool,
    show_progress: bool,
) -> None:
    """Run the industry chart import process.

    Args:
        importer: Industry chart importer instance
        industry_codes: Industry codes to import
        start_date: Start date
        end_date: End date
        frequencies: Frequencies to import
        skip_existing: Skip existing data
        show_progress: Show progress bar
    """
    if show_progress:
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as progress:
            task = progress.add_task("[cyan]Importing industries...", total=len(industry_codes))

            def update_progress(current: int, total: int, industry_code: str):
                progress.update(task, advance=1, description=f"[cyan]Processing industry {industry_code}...")

            importer.import_batch(
                industry_codes,
                start_date,
                end_date,
                frequencies,
                progress_callback=update_progress,
                skip_existing=skip_existing,
            )
    else:
        importer.import_batch(
            industry_codes,
            start_date,
            end_date,
            frequencies,
            skip_existing=skip_existing,
        )

    console.print("[green]✓[/green] Industry chart import completed successfully")


def _show_database_stats(db_manager: DuckDBManager) -> None:
    """Show database statistics.

    Args:
        db_manager: DuckDB manager instance
    """
    stats = db_manager.get_database_stats()

    stats_table = Table(title="Database Statistics")
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Value", style="magenta")

    stats_table.add_row("Daily Chart Records", f"{stats['daily_charts_count']:,}")
    stats_table.add_row("Daily Chart Stocks", str(stats["daily_charts_stocks"]))
    stats_table.add_row("Weekly Chart Records", f"{stats['weekly_charts_count']:,}")
    stats_table.add_row("Weekly Chart Stocks", str(stats["weekly_charts_stocks"]))
    stats_table.add_row("Monthly Chart Records", f"{stats['monthly_charts_count']:,}")
    stats_table.add_row("Monthly Chart Stocks", str(stats["monthly_charts_stocks"]))
    stats_table.add_row("", "")
    stats_table.add_row("Industry Daily Records", f"{stats.get('industry_daily_charts_count', 0):,}")
    stats_table.add_row("Industry Daily Industries", str(stats.get("industry_daily_charts_industries", 0)))
    stats_table.add_row("Industry Weekly Records", f"{stats.get('industry_weekly_charts_count', 0):,}")
    stats_table.add_row("Industry Weekly Industries", str(stats.get("industry_weekly_charts_industries", 0)))
    stats_table.add_row("Industry Monthly Records", f"{stats.get('industry_monthly_charts_count', 0):,}")
    stats_table.add_row("Industry Monthly Industries", str(stats.get("industry_monthly_charts_industries", 0)))
    stats_table.add_row("", "")
    stats_table.add_row("Tracked Stocks", str(stats["tracked_stocks"]))
    stats_table.add_row("Industry Codes", f"{stats.get('industry_codes_count', 0):,}")
    stats_table.add_row("Database Size", f"{stats['database_size_mb']} MB")

    console.print(stats_table)
