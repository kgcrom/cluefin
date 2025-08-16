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
from cluefin_cli.utils.formatters import format_number, format_currency

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

    # TODO basic company data
    basic_data = await data_fetcher.get_basic_data(stock_code)

    # TODO daily and weekly chart data
    stock_data = await data_fetcher.get_stock_data(stock_code, period)

    console.print("[yellow]Fetching foreign trading data...[/yellow]")
    foreign_data = await data_fetcher.get_foreign_trading(stock_code)

    # TODO 업종 별 투자자 순매수요청,
    # TODO 업종현재가 요청   // 해당 업종에 돈이 들어오고 있는지 아닌지 판단. 한 기업이 여러 업종에 속한다면??


    console.print("[yellow]Fetching market indices...[/yellow]")
    kospi_data = await data_fetcher.get_kospi_data()
    kosdaq_data = await data_fetcher.get_kosdaq_data()

    # Calculate technical indicators
    console.print("[yellow]Calculating technical indicators...[/yellow]")
    indicators = technical_analyzer.calculate_all(stock_data)

    # Display results
    _display_company_info(stock_code, basic_data)
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


def _display_company_info(stock_code: str, data: pd.DataFrame):
    """Display basic company information."""
    if data.empty:
        console.print("[red]No company data available[/red]")
        return
    
    table = Table(title=f"Company Information - {stock_code}")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    
    # Get the first row of data
    info = data.iloc[0]
    
    # Basic company info
    if 'stock_name' in data.columns and info['stock_name']:
        table.add_row("Company Name", str(info['stock_name']))
    
    if 'settlement_month' in data.columns and info['settlement_month']:
        table.add_row('Settlement Month', f"{str(info['settlement_month'])} month")
    
    if 'industry_name' in data.columns and info['industry_name']:
        table.add_row("Industry", str(info['industry_name']))
    
    if 'registration_day' in data.columns and info['registration_day']:
        table.add_row("Registration Day", str(info['registration_day']))
    
    if 'sector_name' in data.columns and info['sector_name']:
        table.add_row("Sector", str(info['sector_name']))
    
    if 'distribution_stock' in data.columns and info['distribution_stock'] and info['distribution_stock']:
        if 'distribution_ratio' in data.columns and info['distribution_ratio']:
            table.add_row('Distribution stock / Floating Stock', f"{str(info['distribution_stock'])} / {info['floating_stock']}({str(info['distribution_ratio'])}%)")

    if 'company_size' in data.columns and info['company_size']:
        table.add_row("Company Size", str(info['company_size']))
    
    # Financial metrics
    if 'market_cap' in data.columns and info['market_cap']:
        table.add_row("Market Cap", format_currency(info['market_cap'], '억원'))
    
    if 'per' in data.columns and info['per']:
        table.add_row("PER", str(info['per']))
    
    if 'eps' in data.columns and info['eps']:
        table.add_row("EPS", format_currency(info['eps']))
    
    if 'pbr' in data.columns and info['pbr']:
        table.add_row("PBR", str(info['pbr']))
    
    if 'roe' in data.columns and info['roe']:
        table.add_row("ROE", f"{info['roe']}%")

    if 'bps' in data.columns and info['bps']:
        table.add_row('BPS', format_currency(info['bps']))

    if 'revenue' in data.columns and info['revenue']:
        table.add_row('Revenue', format_currency(info['revenue'], '억원'))

    if 'operating_profit' in data.columns and info['operating_profit']:
        table.add_row('Operation profit', format_currency(info['operating_profit'], '억원'))
    
    if 'net_profit' in data.columns and info['net_profit']:
        table.add_row('Net profit', format_currency(info['net_profit'], '억원'))

    
    # Price information
    if '250_day_high' in data.columns and info['250_day_high']:
        if '250hgst_pric_pre_rt' in data.columns and info['250hgst_pric_pre_rt']:
            table.add_row("52 Week High", f"{format_currency(info['250_day_high'])}(#{info['250hgst_pric_pre_rt']}%)")
    
    if '250_day_low' in data.columns and info['250_day_low']:
        if '250lwst_pric_pre_rt' in data.columns and info['250lwst_pric_pre_rt']:
            table.add_row("52 Week Low", f"{format_currency(info['250_day_low'])}(#{info['250lwst_pric_pre_rt']}%)")
    
    # Shares information
    if 'floating_stock' in data.columns and info['floating_stock']:
        table.add_row("Floating Stock", str(info['floating_stock']))
    
    if 'foreign_exhaustion_rate' in data.columns and info['foreign_exhaustion_rate']:
        table.add_row("Foreign Ownership", f"{info['foreign_exhaustion_rate']}%")
    
    # Additional info
    if 'order_warning' in data.columns and info['order_warning'] and info['order_warning'] != '0':
        warning_map = {
            '2': 'Liquidation Trading',
            '3': 'Short-term Overheating',
            '4': 'Investment Risk',
            '5': 'Investment Elapsed',
            '1': 'ETF Investment Caution'
        }
        warning = warning_map.get(str(info['order_warning']), 'Warning')
        table.add_row("Investment Warning", warning)
    
    console.print(table)


def _display_stock_info(stock_code: str, data):
    """Display basic stock information."""
    table = Table(title=f"Stock Information - {stock_code}")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")

    current_price = data["close"].iloc[-1] if not data.empty else 0
    prev_price = data["close"].iloc[-2] if len(data) > 1 else current_price
    change = current_price - prev_price
    change_pct = (change / prev_price * 100) if prev_price != 0 else 0

    table.add_row("Current Price", format_currency(current_price))
    change_str = format_currency(abs(change))
    change_str = f"+{change_str[1:]}" if change >= 0 else f"-{change_str[1:]}"
    table.add_row("Change", f"{change_str} ({change_pct:+.2f}%)")
    table.add_row("Volume", format_number(data['volume'].iloc[-1]) if not data.empty else "N/A")

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

    table.add_row("Foreign Buy", format_currency(foreign_data.get('buy', 0)))
    table.add_row("Foreign Sell", format_currency(foreign_data.get('sell', 0)))
    net = foreign_data.get("buy", 0) - foreign_data.get("sell", 0)
    net_str = format_currency(abs(net))
    net_str = f"+{net_str[1:]}" if net >= 0 else f"-{net_str[1:]}"
    table.add_row("Net Foreign", net_str)

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
        table.add_row("SMA (20)", format_currency(sma_20), signal)

    console.print(table)
