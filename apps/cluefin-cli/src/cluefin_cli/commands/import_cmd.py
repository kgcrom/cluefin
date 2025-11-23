"""Import command for stock chart data."""

import sys
from datetime import datetime
from typing import Optional, Literal

import click
from cluefin_openapi.kis._auth import Auth as KisAuth
from cluefin_openapi.kis._client import Client as KisClient
from cluefin_openapi.kiwoom._auth import Auth as KiwoomAuth
from cluefin_openapi.kiwoom._client import Client as KiwoomClient
from loguru import logger
from pydantic import SecretStr
from rich.console import Console
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TextColumn
from rich.table import Table

from cluefin_cli.config.settings import settings
from cluefin_cli.data.duckdb_manager import DuckDBManager
from cluefin_cli.data.stock_importer import DomesticStockChartImporter, OverseasStockChartImporter
from cluefin_cli.data.industry_chart_importer import DomesticIndustryChartImporter
from cluefin_cli.data.industry_importer import DomesticIndustryCodeImporter
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
    type=click.Choice(["kospi", "kosdaq", "nyse", "nasdaq"], case_sensitive=False),
    default=None,
    help="Filter by market (KOSPI, KOSDAQ, NYSE, or NASDAQ)",
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
    market: Optional[Literal["kospi", "kosdaq", "nyse", "nasdaq"]],
    start: Optional[str],
    end: Optional[str],
    show_progress: bool,
    skip_existing: bool,
    check_db: bool,
    clear_db: bool,
    industry_codes: bool,
    industry_charts: bool,
):
    """Import stock chart data from KIS API to DuckDB.

    Examples:
        # Import 3 years of data for specific stocks
        cluefin-cli import 005930 035720

        # Import from stdin (pipeline)
        echo "005930\\n035720" | cluefin-cli import --from-stdin

        # Custom date range
        cluefin-cli import 005930 --start 20220101 --end 20251023

        # Show database statistics
        cluefin-cli import --check-db
    """
    # Check for KIS API credentials
    if not settings.kis_app_key:
        raise ValueError("KIS_APP_KEY environment variable is required")
    if not settings.kis_secret_key:
        raise ValueError("KIS_SECRET_KEY environment variable is required")
    if not settings.kis_env:
        raise ValueError("KIS_ENV environment variable is required")

    db_manager = None
    try:
        # Initialize components
        db_manager = DuckDBManager()

        # Initialize KIS client for stock chart import
        kis_auth = KisAuth(
            app_key=settings.kis_app_key,
            secret_key=SecretStr(settings.kis_secret_key),
            env=settings.kis_env,
        )
        token = kis_auth.generate()
        kis_client = KisClient(
            token=token.access_token,
            app_key=settings.kis_app_key,
            secret_key=SecretStr(settings.kis_secret_key),
            env=settings.kis_env,
        )
        importer = DomesticStockChartImporter(kis_client, db_manager)
        overseas_importer = OverseasStockChartImporter(kis_client, db_manager)

        # Initialize Kiwoom client for list features (if credentials available)
        kiwoom_client = None
        stock_fetcher = None
        industry_importer = None

        if settings.kiwoom_app_key and settings.kiwoom_secret_key:
            kiwoom_auth = KiwoomAuth(
                app_key=settings.kiwoom_app_key,
                secret_key=SecretStr(settings.kiwoom_secret_key),
                env=settings.kiwoom_env,
            )
            kiwoom_token = kiwoom_auth.generate_token()
            kiwoom_client = KiwoomClient(
                token=kiwoom_token.get_token(),
                env=settings.kiwoom_env,
                rate_limit_requests_per_second=1.0,
                rate_limit_burst=2,
            )
            stock_fetcher = StockListFetcher(kiwoom_client, db_manager, kis_client)
            industry_importer = DomesticIndustryCodeImporter(db_manager)

        # Initialize industry chart importer (uses KIS API)
        industry_chart_importer = DomesticIndustryChartImporter(kis_client, db_manager)

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

            # Get date range
            start_date, end_date = _get_date_range(start, end)

            # Display summary
            _display_industry_import_summary(codes_to_import, start_date, end_date)

            # Run import
            _run_industry_import(
                industry_chart_importer,
                codes_to_import,
                start_date,
                end_date,
                show_progress,
            )

            # Display final statistics
            _show_database_stats(db_manager)
            return

        # Handle list-stocks operation
        if list_stocks:
            if market in ("kospi", "kosdaq"):
                _list_domestic_stocks(stock_fetcher, market)
            elif market in ("nyse", "nasdaq"):
                _list_overseas_stocks(stock_fetcher, market)
            else:
                console.print("[yellow]Please specify a market with --market (kospi, kosdaq, nyse, or nasdaq)[/yellow]")
            return

        # Get date range
        start_date, end_date = _get_date_range(start, end)

        # Branch by market type
        if market in ("kospi", "kosdaq") or market is None:
            # Domestic stocks (KOSPI/KOSDAQ)
            codes_to_import = _collect_stock_codes(
                stock_codes=stock_codes,
                from_stdin=from_stdin,
                market=market,
                stock_fetcher=stock_fetcher,
                db_manager=db_manager,
            )

            if not codes_to_import:
                console.print("[yellow]No stock codes specified for import[/yellow]")
                return

            # Display summary
            _display_import_summary(codes_to_import, start_date, end_date, skip_existing)

            # Run import
            _run_import(
                importer,
                codes_to_import,
                start_date,
                end_date,
                skip_existing,
                show_progress,
            )

            # Display final statistics
            _show_database_stats(db_manager)
        else:
            # Overseas stocks (NYSE/NASDAQ)
            exchange_code = "NYSE" if market == "nyse" else "NASD"
            codes_to_import = _collect_stock_codes(
                stock_codes=stock_codes,
                from_stdin=from_stdin,
                market=market,
                stock_fetcher=stock_fetcher,
                db_manager=db_manager,
            )

            if not codes_to_import:
                console.print("[yellow]No stock codes specified for import[/yellow]")
                return

            # Display summary
            _display_overseas_import_summary(codes_to_import, start_date, end_date)

            # Run import
            _run_overseas_import(
                overseas_importer,
                exchange_code,
                codes_to_import,
                start_date,
                end_date,
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
    stock_fetcher: Optional[StockListFetcher],
    db_manager: DuckDBManager,
) -> list[str]:
    """Collect stock codes from various sources.

    Args:
        stock_codes: Stock codes from CLI arguments
        from_stdin: Whether to read from stdin
        market: Market filter
        stock_fetcher: Stock fetcher instance
        db_manager: DuckDB manager instance

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
        # For overseas stocks, fetch from DuckDB
        if market in ("nyse", "nasdaq"):
            exchange_code = "NYSE" if market == "nyse" else "NASD"
            console.print(
                f"[yellow]Fetching available {market.upper()} stocks from database...[/yellow]"
            )
            codes = db_manager.get_overseas_stock_codes(exchange_code)
            if not codes:
                raise ValueError(
                    f"No {market.upper()} stocks found in database. "
                    "Please run 'cluefin-cli import --market {market} --list-stocks' first."
                )
        # For domestic stocks, fetch from API
        else:
            if stock_fetcher is None:
                raise ValueError(
                    "Cannot fetch stocks from API: Kiwoom credentials not configured. "
                    "Please provide stock codes via arguments or --from-stdin"
                )
            console.print("[yellow]Fetching available stocks from Kiwoom API...[/yellow]")
            codes = [item.code for item in stock_fetcher.get_all_stocks(market=market)]

    # From arguments
    else:
        codes = list(stock_codes)

    return sorted(set(codes))


def _get_date_range(start: Optional[str], end: Optional[str]) -> tuple[str, str]:
    """Get and validate date range.

    Args:
        start: Start date (YYYYMMDD)
        end: End date (YYYYMMDD)

    Returns:
        Tuple of (start_date, end_date) in YYYYMMDD format
    """
    if not start or not end:
        start_date, end_date = DomesticStockChartImporter.get_default_date_range()
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
    start_date: str,
    end_date: str,
    skip_existing: bool,
) -> None:
    """Display import summary before starting.

    Args:
        stock_codes: List of stock codes to import
        start_date: Start date
        end_date: End date
        skip_existing: Whether to skip existing data
    """
    summary_table = Table(title="Import Summary")
    summary_table.add_column("Parameter", style="cyan")
    summary_table.add_column("Value", style="magenta")

    summary_table.add_row("Stock Codes", str(len(stock_codes)))
    summary_table.add_row("Start Date", start_date)
    summary_table.add_row("End Date", end_date)
    summary_table.add_row("Skip Existing", "Yes" if skip_existing else "No")

    console.print(summary_table)


def _run_import(
    importer: DomesticStockChartImporter,
    stock_codes: list[str],
    start_date: str,
    end_date: str,
    skip_existing: bool,
    show_progress: bool,
) -> None:
    """Run the import process.

    Args:
        importer: Chart importer instance
        stock_codes: Stock codes to import
        start_date: Start date
        end_date: End date
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
                progress_callback=update_progress,
                skip_existing=skip_existing,
            )
    else:
        importer.import_batch(
            stock_codes,
            start_date,
            end_date,
            skip_existing=skip_existing,
        )

    console.print("[green]✓[/green] Import completed successfully")


def _import_industry_codes(industry_importer: Optional[DomesticIndustryCodeImporter], market: Optional[str]) -> None:
    """Import industry codes from idxcode.mst file.

    업종코드 파일 다운로드:
    https://apiportal.koreainvestment.com/apiservice-category

    Args:
        industry_importer: Industry code importer instance
        market: Market filter (not used for file-based import, kept for API compatibility)
    """
    if industry_importer is None:
        raise ValueError("Industry code importer not initialized")

    console.print("[yellow]Importing industry codes from idxcode.mst file...[/yellow]")

    # Locate MST file in project root
    from pathlib import Path

    project_root = Path(__file__).parent.parent.parent.parent.parent
    mst_file_path = project_root / "idxcode.mst"

    if not mst_file_path.exists():
        raise FileNotFoundError(
            f"MST file not found at {mst_file_path}\n"
            "Please ensure idxcode.mst is located in the project root directory\n"
            "Download from: https://apiportal.koreainvestment.com/apiservice-category"
        )

    # Import industry codes from file
    results = industry_importer.import_industry_codes(str(mst_file_path))

    # Display results
    results_table = Table(title="Industry Code Import Results")
    results_table.add_column("Description", style="cyan")
    results_table.add_column("Count", style="magenta", justify="right")

    results_table.add_row("Total imported", str(results.get("total", 0)))

    console.print(results_table)
    console.print(f"[green]✓[/green] Imported {results.get('total', 0)} industry codes from {mst_file_path}")


def _list_domestic_stocks(stock_fetcher: Optional[StockListFetcher], market: str) -> None:
    """List available domestic stocks and fetch metadata.

    Args:
        stock_fetcher: Stock fetcher instance
        market: Market filter (kospi or kosdaq)
    """
    if stock_fetcher is None:
        raise ValueError(
            "Listing stocks requires Kiwoom credentials. Please set KIWOOM_APP_KEY, KIWOOM_SECRET_KEY, and KIWOOM_ENV"
        )

    stderr_console.print("[yellow]Fetching domestic stock list from Kiwoom API...[/yellow]")
    stocks = stock_fetcher.get_all_stocks(market=market)

    # Fetch and save metadata in batch
    success_count, failed_count = stock_fetcher.fetch_and_save_metadata_batch(stocks)

    stderr_console.print(
        f"[green]✓[/green] Listed {len(stocks)} domestic stocks "
        f"(metadata saved: {success_count}, failed: {failed_count})"
    )


def _list_overseas_stocks(stock_fetcher: Optional[StockListFetcher], market: str) -> None:
    """List available overseas stocks and fetch metadata.

    Args:
        stock_fetcher: Stock fetcher instance
        market: Market filter (nyse or nasdaq)
    """
    if stock_fetcher is None:
        raise ValueError(
            "Listing stocks requires Kiwoom and KIS credentials. "
            "Please set KIWOOM_APP_KEY, KIWOOM_SECRET_KEY, KIWOOM_ENV, "
            "KIS_APP_KEY, KIS_SECRET_KEY, and KIS_ENV"
        )

    stderr_console.print("[yellow]Fetching overseas stock list from master file...[/yellow]")
    stocks_df = stock_fetcher.get_all_overseas_stocks(market=market)

    if stocks_df.empty:
        stderr_console.print("[yellow]No overseas stocks found for the specified market[/yellow]")
        return

    # Fetch and save metadata in batch
    success_count, failed_count = stock_fetcher.fetch_and_save_overseas_metadata_batch(stocks_df)

    stderr_console.print(
        f"[green]✓[/green] Listed {len(stocks_df)} overseas stocks ({market.upper()}) "
        f"(metadata saved: {success_count}, failed: {failed_count})"
    )


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
        console.print("[yellow]Fetching all domestic industry codes from database...[/yellow]")
        industry_df = db_manager.get_domestic_industry_codes()
        if not industry_df.empty:
            codes = industry_df["code"].tolist()
            logger.info(f"Found {len(codes)} domestic industry codes in database")
        else:
            console.print(
                "[yellow]No domestic industry codes found in database. "
                "Please run 'cluefin-cli import --industry-codes' first.[/yellow]"
            )

    return sorted(set(codes))


def _display_industry_import_summary(
    industry_codes: list[str],
    start_date: str,
    end_date: str,
) -> None:
    """Display industry import summary before starting.

    Args:
        industry_codes: List of industry codes to import
        start_date: Start date
        end_date: End date
    """
    summary_table = Table(title="Industry Chart Import Summary")
    summary_table.add_column("Parameter", style="cyan")
    summary_table.add_column("Value", style="magenta")

    summary_table.add_row("Industry Codes", str(len(industry_codes)))
    summary_table.add_row("Start Date", start_date)
    summary_table.add_row("End Date", end_date)

    console.print(summary_table)


def _run_industry_import(
    importer: Optional[DomesticIndustryChartImporter],
    industry_codes: list[str],
    start_date: str,
    end_date: str,
    show_progress: bool,
) -> None:
    """Run the domestic industry chart import process.

    Args:
        importer: Industry chart importer instance
        industry_codes: Industry codes to import
        start_date: Start date
        end_date: End date
        show_progress: Show progress bar
    """
    if importer is None:
        raise ValueError(
            "Industry chart import requires KIS API credentials. Please set KIS_APP_KEY, KIS_SECRET_KEY, and KIS_ENV"
        )

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
                progress_callback=update_progress,
            )
    else:
        importer.import_batch(
            industry_codes,
            start_date,
            end_date,
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

    # KIS data (new)
    stats_table.add_row("Domestic Stock Daily Charts (KIS)", f"{stats.get('domestic_stock_daily_charts_count', 0):,}")
    stats_table.add_row("└─ Unique Stocks", f"{stats.get('domestic_stock_daily_charts_stocks', 0):,}")
    stats_table.add_row("", "")

    # Industry data
    stats_table.add_row("Domestic Industry Daily Records", f"{stats.get('domestic_industry_daily_charts_count', 0):,}")
    stats_table.add_row("└─ Unique Industries", str(stats.get("domestic_industry_daily_charts_industries", 0)))
    stats_table.add_row("", "")

    # Metadata
    stats_table.add_row("Domestic Stock Metadata Records", str(stats["domestic_tracked_stocks"]))
    stats_table.add_row("Domestic Industry Codes", f"{stats.get('domestic_industry_codes_count', 0):,}")
    stats_table.add_row("", "")

    # Overseas stock data
    stats_table.add_row("Overseas Stock Daily Charts", f"{stats.get('overseas_stock_daily_charts_count', 0):,}")
    stats_table.add_row("└─ Unique Stocks", f"{stats.get('overseas_stock_daily_charts_stocks', 0):,}")
    stats_table.add_row("Overseas Stock Metadata Records", f"{stats.get('overseas_stock_metadata_count', 0):,}")
    stats_table.add_row("", "")

    # Database info
    stats_table.add_row("Database Size", f"{stats['database_size_mb']} MB")

    console.print(stats_table)


def _display_overseas_import_summary(
    stock_codes: list[str],
    start_date: str,
    end_date: str,
) -> None:
    """Display overseas import summary before starting.

    Args:
        stock_codes: List of stock codes to import
        start_date: Start date
        end_date: End date
    """
    summary_table = Table(title="Overseas Stock Import Summary")
    summary_table.add_column("Parameter", style="cyan")
    summary_table.add_column("Value", style="magenta")

    summary_table.add_row("Stock Codes", str(len(stock_codes)))
    summary_table.add_row("Start Date", start_date)
    summary_table.add_row("End Date", end_date)

    console.print(summary_table)


def _run_overseas_import(
    importer: OverseasStockChartImporter,
    exchange_code: str,
    stock_codes: list[str],
    start_date: str,
    end_date: str,
    skip_existing: bool,
    show_progress: bool,
) -> None:
    """Run the overseas stock import process.

    Args:
        importer: Overseas chart importer instance
        exchange_code: Exchange code (NYS, NAS)
        stock_codes: Stock codes to import
        start_date: Start date
        end_date: End date
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
            task = progress.add_task("[cyan]Importing overseas stocks...", total=len(stock_codes))

            def update_progress(current: int, total: int, stock_code: str):
                progress.update(task, advance=1, description=f"[cyan]Processing {stock_code}...")

            importer.import_batch(
                exchange_code,
                stock_codes,
                start_date,
                end_date,
                progress_callback=update_progress,
                skip_existing=skip_existing,
            )
    else:
        importer.import_batch(
            exchange_code,
            stock_codes,
            start_date,
            end_date,
            skip_existing=skip_existing,
        )

    console.print("[green]✓[/green] Overseas stock import completed successfully")
