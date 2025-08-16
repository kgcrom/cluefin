import asyncio

import click
import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cluefin_cli.analysis.ai_analyzer import AIAnalyzer
from cluefin_cli.analysis.indicators import TechnicalAnalyzer
from cluefin_cli.config.settings import settings
from cluefin_cli.data.fetcher import DataFetcher
from cluefin_cli.display.charts import ChartRenderer

console = Console()


@click.command()
@click.argument("stock_code")
@click.option("--period", "-p", default="3M", help="Data period (1M, 3M, 6M, 1Y)")
@click.option("--chart", "-c", is_flag=True, help="Display chart in terminal")
@click.option("--ai-analysis", "-a", is_flag=True, help="Include AI-powered analysis")
def analyze(stock_code: str, period: str, chart: bool, ai_analysis: bool):
    """Analyze stock with technical indicators and market data."""
    console.print(f"[bold blue]Analyzing {stock_code}...[/bold blue]")

    try:
        # Run async analysis
        asyncio.run(_analyze_stock(stock_code, period, chart, ai_analysis))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


async def _analyze_stock(stock_code: str, period: str, chart: bool, ai_analysis: bool):
    """Main analysis logic."""
    # Initialize components
    data_fetcher = DataFetcher()
    technical_analyzer = TechnicalAnalyzer()
    chart_renderer = ChartRenderer()

    # Fetch data
    console.print("[yellow]Fetching stock data...[/yellow]")
    stock_data = await data_fetcher.get_stock_data(stock_code, period)

    console.print("[yellow]Fetching foreign trading data...[/yellow]")
    foreign_data = await data_fetcher.get_foreign_trading(stock_code)

    console.print("[yellow]Fetching market indices...[/yellow]")
    kospi_data = await data_fetcher.get_kospi_data()
    kosdaq_data = await data_fetcher.get_kosdaq_data()

    # Calculate technical indicators
    console.print("[yellow]Calculating technical indicators...[/yellow]")
    indicators = technical_analyzer.calculate_all(stock_data)

    # Display results
    _display_stock_info(stock_code, stock_data)
    _display_market_indices(kospi_data, kosdaq_data)
    _display_foreign_trading(foreign_data)
    _display_technical_indicators(indicators)

    # Display chart if requested
    if chart:
        console.print("\n[bold cyan]Price Chart with Technical Indicators[/bold cyan]")
        chart_renderer.render_stock_chart(stock_data, indicators)

    # AI analysis if requested
    if ai_analysis and settings.openai_api_key:
        console.print("\n[yellow]Generating AI analysis...[/yellow]")
        ai_analyzer = AIAnalyzer()
        analysis = await ai_analyzer.analyze_stock(stock_code, stock_data, indicators, foreign_data)
        if analysis is None:
            raise Exception("Error analysis stock")

        console.print("\n[bold green]AI Market Analysis[/bold green]")
        console.print(Panel(analysis, expand=False))
    elif ai_analysis:
        console.print("[red]OpenAI API key not configured for AI analysis[/red]")


def _display_stock_info(stock_code: str, data):
    """Display basic stock information."""
    table = Table(title=f"Stock Information - {stock_code}")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")

    current_price = data["close"].iloc[-1] if not data.empty else 0
    prev_price = data["close"].iloc[-2] if len(data) > 1 else current_price
    change = current_price - prev_price
    change_pct = (change / prev_price * 100) if prev_price != 0 else 0

    table.add_row("Current Price", f"₩{current_price:,.0f}")
    table.add_row("Change", f"₩{change:+,.0f} ({change_pct:+.2f}%)")
    table.add_row("Volume", f"{data['volume'].iloc[-1]:,.0f}" if not data.empty else "N/A")

    console.print(table)


def _display_market_indices(kospi_data, kosdaq_data):
    """Display KOSPI and KOSDAQ indices."""
    table = Table(title="Market Indices")
    table.add_column("Index", style="cyan")
    table.add_column("Value", style="magenta")
    table.add_column("Change", style="green")

    if kospi_data:
        table.add_row("KOSPI", f"{kospi_data['value']:.2f}", f"{kospi_data['change']:+.2f}%")
    if kosdaq_data:
        table.add_row("KOSDAQ", f"{kosdaq_data['value']:.2f}", f"{kosdaq_data['change']:+.2f}%")

    console.print(table)


def _display_foreign_trading(foreign_data):
    """Display foreign trading information."""
    if not foreign_data:
        return

    table = Table(title="Foreign Trading")
    table.add_column("Type", style="cyan")
    table.add_column("Amount", style="magenta")

    table.add_row("Foreign Buy", f"₩{foreign_data.get('buy', 0):,.0f}")
    table.add_row("Foreign Sell", f"₩{foreign_data.get('sell', 0):,.0f}")
    net = foreign_data.get("buy", 0) - foreign_data.get("sell", 0)
    table.add_row("Net Foreign", f"₩{net:+,.0f}")

    console.print(table)


def _display_technical_indicators(indicators):
    """Display technical indicators."""
    table = Table(title="Technical Indicators")
    table.add_column("Indicator", style="cyan")
    table.add_column("Value", style="magenta")
    table.add_column("Signal", style="green")

    # RSI
    rsi = indicators["rsi"].iloc[-1] if "rsi" in indicators else None
    if rsi is not None:
        signal = "Overbought" if rsi > 70 else "Oversold" if rsi < 30 else "Neutral"
        table.add_row("RSI (14)", f"{rsi:.2f}", signal)

    # MACD
    if all(col in indicators for col in ["macd", "macd_signal"]):
        macd = indicators["macd"].iloc[-1]
        signal_line = indicators["macd_signal"].iloc[-1]
        signal = "Bullish" if macd > signal_line else "Bearish"
        table.add_row("MACD", f"{macd:.4f}", signal)

    # Moving Averages
    if "sma_20" in indicators and not pd.isna(indicators["sma_20"].iloc[-1]):
        sma_20 = indicators["sma_20"].iloc[-1]
        current_price = indicators["close"].iloc[-1] if "close" in indicators else 0
        signal = "Above MA20" if current_price > sma_20 else "Below MA20"
        table.add_row("SMA (20)", f"₩{sma_20:.0f}", signal)

    console.print(table)
