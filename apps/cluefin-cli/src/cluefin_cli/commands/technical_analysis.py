import asyncio
from typing import Any, Dict, List

import click
import pandas as pd
from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cluefin_cli.commands.analysis.ai_analyzer import AIAnalyzer
from cluefin_cli.commands.analysis.indicators import TechnicalAnalyzer
from cluefin_cli.config.settings import settings
from cluefin_cli.data.fetcher import DataFetcher
from cluefin_cli.display.charts import ChartRenderer
from cluefin_cli.ml import StockMLPredictor
from cluefin_cli.utils.formatters import format_currency, format_number

console = Console()


@click.command(name="ta")
@click.argument("stock_code")
@click.option("--chart", "-c", is_flag=True, help="Display chart in terminal")
@click.option("--ai-analysis", "-a", is_flag=True, help="Include AI-powered analysis")
@click.option("--ml-predict", "-m", is_flag=True, help="Include ML-based price prediction")
@click.option(
    "--feature-importance", "-f", is_flag=True, help="Display basic feature importance (requires --ml-predict)"
)
@click.option(
    "--shap-analysis",
    "-s",
    is_flag=True,
    help="Display detailed SHAP analysis with explanations (requires --ml-predict)",
)
def technical_analysis(
    stock_code: str, chart: bool, ai_analysis: bool, ml_predict: bool, feature_importance: bool, shap_analysis: bool
):
    """Run technical analysis for a given stock code."""
    console.print(f"[bold blue]Analyzing {stock_code}...[/bold blue]")

    try:
        # Run async analysis
        asyncio.run(_analyze_stock(stock_code, chart, ai_analysis, ml_predict, feature_importance, shap_analysis))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        logger.error(f"Analysis error for {stock_code}: {e}")


async def _analyze_stock(
    stock_code: str, chart: bool, ai_analysis: bool, ml_predict: bool, feature_importance: bool, shap_analysis: bool
):
    """Main analysis logic."""
    # Initialize components
    data_fetcher = DataFetcher()
    technical_analyzer = TechnicalAnalyzer()
    chart_renderer = ChartRenderer()

    # Initialize ML predictor if needed
    ml_predictor = None
    if ml_predict or feature_importance or shap_analysis:
        ml_predictor = StockMLPredictor()

    # Validate ML-dependent options
    if (feature_importance or shap_analysis) and not ml_predict:
        console.print(
            "[yellow]⚠️  --feature-importance and --shap-analysis require --ml-predict. Enabling ML prediction.[/yellow]"
        )
        ml_predict = True

    # Fetch data
    console.print("[yellow]Fetching stock data...[/yellow]")

    basic_data = await data_fetcher.get_basic_data(stock_code)

    stock_data = await data_fetcher.get_stock_data(stock_code, "1D")

    # Ensure we have enough data for ML analysis
    if ml_predict and len(stock_data) < 30:
        console.print("[red]⚠️  Not enough historical data for ML prediction (minimum 30 days required)[/red]")
        ml_predict = False
        feature_importance = False
        shap_analysis = False

    console.print("[yellow]Fetching foreign trading data...[/yellow]")
    trading_trend_data = await data_fetcher.get_trading_trend(stock_code)

    console.print("[yellow]Fetching market indices...[/yellow]")
    kospi_data = await data_fetcher.get_kospi_index_series()
    kosdaq_data = await data_fetcher.get_kosdaq_index_series()

    # Calculate technical indicators
    console.print("[yellow]Calculating technical indicators...[/yellow]")
    indicators = technical_analyzer.calculate_all(stock_data)

    # Display results
    _display_company_info(stock_code, basic_data)
    _display_stock_info(stock_code, stock_data)
    _display_market_indices(kospi_data, kosdaq_data)
    _display_trading_trend(trading_trend_data)
    _display_technical_indicators(indicators)

    # Display chart if requested
    if chart:
        console.print("\n[bold cyan]Price Chart with Technical Indicators[/bold cyan]")
        chart_renderer.render_stock_chart(stock_data, indicators)

    # ML prediction if requested
    if ml_predict and ml_predictor:
        await _perform_ml_analysis(ml_predictor, stock_code, stock_data, indicators, feature_importance, shap_analysis)

    # AI analysis if requested
    if ai_analysis and settings.openai_api_key:
        console.print("\n[yellow]Generating AI analysis...[/yellow]")
        ai_analyzer = AIAnalyzer()
        analysis = await ai_analyzer.analyze_stock(stock_code, stock_data, indicators)
        if analysis is None:
            raise Exception("Error analysis stock")

        console.print("\n[bold green]AI Market Analysis[/bold green]")
        console.print(Panel(analysis, expand=False))
    elif ai_analysis:
        console.print("[red]OpenAI API key not configured for AI analysis[/red]")


async def _perform_ml_analysis(
    ml_predictor: StockMLPredictor,
    stock_code: str,
    stock_data: pd.DataFrame,
    indicators: Dict,
    show_feature_importance: bool,
    show_shap_analysis: bool,
):
    """
    Perform ML analysis including training and prediction.

    Args:
        ml_predictor: ML predictor instance
        stock_code: Stock code being analyzed
        stock_data: Historical stock data
        indicators: Technical indicators
        show_feature_importance: Whether to display basic feature importance
        show_shap_analysis: Whether to display detailed SHAP analysis
    """
    try:
        console.print("\n[yellow]🤖 Preparing ML analysis...[/yellow]")

        # Prepare data for ML
        prepared_df, feature_names = ml_predictor.prepare_data(stock_data, indicators)

        console.print(f"[green]✓[/green] Data preparation completed. Features: {len(feature_names)}")
        console.print(f"[green]✓[/green] Training samples: {len(prepared_df)}")

        # Check if we have enough data for training
        if len(prepared_df) < 50:
            console.print(
                f"[yellow]⚠️  Limited data for ML training ({len(prepared_df)} samples). Results may be less reliable.[/yellow]"
            )

        # Train model
        console.print("[yellow]🏋️  Training ML model...[/yellow]")
        training_metrics = ml_predictor.train_model(prepared_df)

        console.print("[green]✓[/green] Model training completed")

        # Make prediction
        console.print("[yellow]🔮 Making prediction...[/yellow]")
        prediction_result = ml_predictor.predict(stock_data, indicators)

        # Display results
        console.print("\n" + "=" * 50)
        ml_predictor.display_prediction_results(prediction_result)

        # Display basic feature importance if requested (LightGBM built-in)
        if show_feature_importance:
            console.print("\n" + "=" * 50)
            _display_basic_feature_importance(ml_predictor, feature_names)

        # Display detailed SHAP analysis if requested
        if show_shap_analysis:
            console.print("\n" + "=" * 50)
            ml_predictor.display_feature_importance(prediction_result, top_n=15)

        # Display model summary
        _display_ml_model_summary(training_metrics, len(feature_names))

    except Exception as e:
        console.print(f"[red]❌ ML Analysis Error: {e}[/red]")
        logger.error(f"ML analysis error for {stock_code}: {e}")


def _display_basic_feature_importance(ml_predictor: StockMLPredictor, feature_names: List[str]):
    """
    Display basic feature importance from LightGBM model.

    Args:
        ml_predictor: Trained ML predictor
        feature_names: List of feature names
    """
    try:
        console.print("[bold cyan]📊 Basic Feature Importance (LightGBM)[/bold cyan]")

        # Get feature importance from trained model
        importance_series = ml_predictor.model.get_feature_importance(top_n=15)

        # Create table
        table = Table(title="Top 15 Important Features")
        table.add_column("Rank", style="dim", width=6)
        table.add_column("Feature", style="bold blue", min_width=20)
        table.add_column("Importance", justify="right", style="green")
        table.add_column("Relative %", justify="right", style="yellow")

        total_importance = importance_series.sum()

        for idx, (feature, importance) in enumerate(importance_series.items(), 1):
            relative_pct = (importance / total_importance) * 100
            table.add_row(str(idx), feature, f"{importance:.3f}", f"{relative_pct:.1f}%")

        console.print(table)

        # Add explanation
        explanation_text = """
[bold]Feature Importance Explanation:[/bold]
• Higher values indicate more important features for prediction
• Based on how frequently features are used in tree splits
• Relative % shows each feature's contribution to total importance
        """

        console.print(Panel(explanation_text.strip(), title="💡 Understanding Feature Importance", border_style="cyan"))

    except Exception as e:
        console.print(f"[red]Error displaying basic feature importance: {e}[/red]")
        logger.error(f"Error displaying basic feature importance: {e}")


def _display_ml_model_summary(training_metrics: Dict[str, float], n_features: int):
    """
    Display ML model training summary.

    Args:
        training_metrics: Dictionary of training metrics
        n_features: Number of features used
    """
    try:
        table = Table(title="🔬 ML Model Training Summary")
        table.add_column("Metric", style="cyan", min_width=20)
        table.add_column("Value", style="magenta", min_width=15)
        table.add_column("Interpretation", style="green", min_width=25)

        # Add metrics with interpretations
        val_accuracy = training_metrics.get("val_accuracy", 0)
        if val_accuracy > 0.6:
            acc_interpretation = "Good"
            acc_style = "green"
        elif val_accuracy > 0.55:
            acc_interpretation = "Fair"
            acc_style = "yellow"
        else:
            acc_interpretation = "Poor"
            acc_style = "red"

        table.add_row("Validation Accuracy", f"{val_accuracy:.1%}", f"[{acc_style}]{acc_interpretation}[/{acc_style}]")

        val_precision = training_metrics.get("val_precision", 0)
        table.add_row("Precision", f"{val_precision:.3f}", "Higher is better")

        val_recall = training_metrics.get("val_recall", 0)
        table.add_row("Recall", f"{val_recall:.3f}", "Higher is better")

        val_f1 = training_metrics.get("val_f1", 0)
        table.add_row("F1-Score", f"{val_f1:.3f}", "Balanced metric")

        val_auc = training_metrics.get("val_auc", 0)
        if val_auc > 0.7:
            auc_interpretation = "Excellent"
            auc_style = "green"
        elif val_auc > 0.6:
            auc_interpretation = "Good"
            auc_style = "yellow"
        else:
            auc_interpretation = "Fair"
            auc_style = "red"

        table.add_row("AUC Score", f"{val_auc:.3f}", f"[{auc_style}]{auc_interpretation}[/{auc_style}]")

        table.add_row("Features Used", str(n_features), "Technical indicators")

        console.print(table)

        # Add interpretation note
        interpretation_text = """
[bold]Model Performance Guide:[/bold]
• Accuracy > 60%: The model can predict price direction reasonably well
• AUC > 0.7: Excellent discrimination between up/down movements
• F1-Score: Balances precision and recall for reliable predictions

[yellow]Note: Stock prediction is inherently uncertain. Use predictions as one factor among many in investment decisions.[/yellow]
        """

        console.print(Panel(interpretation_text.strip(), title="📚 How to Interpret Results", border_style="blue"))

    except Exception as e:
        logger.error(f"Error displaying ML model summary: {e}")


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
    if "stock_name" in data.columns and info["stock_name"]:
        table.add_row("Company Name", str(info["stock_name"]))

    if "settlement_month" in data.columns and info["settlement_month"]:
        table.add_row("Settlement Month", f"{str(info['settlement_month'])} month")

    if "industry_name" in data.columns and info["industry_name"]:
        table.add_row("Industry", str(info["industry_name"]))

    if "registration_day" in data.columns and info["registration_day"]:
        table.add_row("Registration Day", str(info["registration_day"]))

    if "sector_name" in data.columns and info["sector_name"]:
        table.add_row("Sector", str(info["sector_name"]))

    if "distribution_stock" in data.columns and info["distribution_stock"] and info["distribution_stock"]:
        if "distribution_ratio" in data.columns and info["distribution_ratio"]:
            table.add_row(
                "Distribution stock / Floating Stock",
                f"{str(info['distribution_stock'])} / {info['floating_stock']}({str(info['distribution_ratio'])}%)",
            )

    if "company_size" in data.columns and info["company_size"]:
        table.add_row("Company Size", str(info["company_size"]))

    # Financial metrics
    if "market_cap" in data.columns and info["market_cap"]:
        table.add_row("Market Cap", format_currency(info["market_cap"], "억원"))

    if "per" in data.columns and info["per"]:
        table.add_row("PER", str(info["per"]))

    if "eps" in data.columns and info["eps"]:
        table.add_row("EPS", format_currency(info["eps"]))

    if "pbr" in data.columns and info["pbr"]:
        table.add_row("PBR", str(info["pbr"]))

    if "roe" in data.columns and info["roe"]:
        table.add_row("ROE", f"{info['roe']}%")

    if "bps" in data.columns and info["bps"]:
        table.add_row("BPS", format_currency(info["bps"]))

    if "revenue" in data.columns and info["revenue"]:
        table.add_row("Revenue", format_currency(info["revenue"], "억원"))

    if "operating_profit" in data.columns and info["operating_profit"]:
        table.add_row("Operation profit", format_currency(info["operating_profit"], "억원"))

    if "net_profit" in data.columns and info["net_profit"]:
        table.add_row("Net profit", format_currency(info["net_profit"], "억원"))

    # Price information
    if "250_day_high" in data.columns and info["250_day_high"]:
        if "250hgst_pric_pre_rt" in data.columns and info["250hgst_pric_pre_rt"]:
            table.add_row("52 Week High", f"{format_currency(info['250_day_high'])}(#{info['250hgst_pric_pre_rt']}%)")

    if "250_day_low" in data.columns and info["250_day_low"]:
        if "250lwst_pric_pre_rt" in data.columns and info["250lwst_pric_pre_rt"]:
            table.add_row("52 Week Low", f"{format_currency(info['250_day_low'])}(#{info['250lwst_pric_pre_rt']}%)")

    # Shares information
    if "floating_stock" in data.columns and info["floating_stock"]:
        table.add_row("Floating Stock", str(info["floating_stock"]))

    if "foreign_exhaustion_rate" in data.columns and info["foreign_exhaustion_rate"]:
        table.add_row("Foreign Ownership", f"{info['foreign_exhaustion_rate']}%")

    # Additional info
    if "order_warning" in data.columns and info["order_warning"] and info["order_warning"] != "0":
        warning_map = {
            "2": "Liquidation Trading",
            "3": "Short-term Overheating",
            "4": "Investment Risk",
            "5": "Investment Elapsed",
            "1": "ETF Investment Caution",
        }
        warning = warning_map.get(str(info["order_warning"]), "Warning")
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
    table.add_row("Volume", format_number(data["volume"].iloc[-1]) if not data.empty else "N/A")

    console.print(table)


def _display_market_indices(kospi_data: List[Dict[str, Any]], kosdaq_data: List[Dict[str, Any]]):
    """Display KOSPI and KOSDAQ indices."""
    table = Table(title="Market Indices")
    table.add_column("Index", style="cyan")
    table.add_column("Close Price", style="magenta")
    table.add_column("Change %", style="green")
    table.add_column("Trading Value", style="yellow")
    table.add_column("Transaction Amount", style="blue")

    # Display KOSPI data
    if kospi_data:
        for item in kospi_data:
            # Format change percentage with color
            change_pct = item.get("fluctuation_rate", 0)
            if change_pct > 0:
                change_color = "green"
                change_str = f"+{change_pct:.2f}%"
            elif change_pct < 0:
                change_color = "red"
                change_str = f"{change_pct:.2f}%"
            else:
                change_color = "white"
                change_str = f"{change_pct:.2f}%"

            # Format large numbers with commas and units
            trading_value = item.get("trading_value", 0)
            transaction_amount = item.get("transaction_amount", 0)

            # Convert to billions for better readability
            trading_value_formatted = f"{trading_value / 1_000_000_000:.1f}B"
            transaction_amount_formatted = f"{transaction_amount / 1_000_000:.1f}M"

            table.add_row(
                item.get("name", "KOSPI"),
                f"{item.get('close_price', 0):.2f}",
                f"[{change_color}]{change_str}[/{change_color}]",
                f"[yellow]{trading_value_formatted}[/yellow]",
                f"[blue]{transaction_amount_formatted}[/blue]",
            )

    # Display KOSDAQ data
    if kosdaq_data:
        for item in kosdaq_data:
            # Format change percentage with color
            change_pct = item.get("fluctuation_rate", 0)
            if change_pct > 0:
                change_color = "green"
                change_str = f"+{change_pct:.2f}%"
            elif change_pct < 0:
                change_color = "red"
                change_str = f"{change_pct:.2f}%"
            else:
                change_color = "white"
                change_str = f"{change_pct:.2f}%"

            # Format large numbers with commas and units
            trading_value = item.get("trading_value", 0)
            transaction_amount = item.get("transaction_amount", 0)

            # Convert to billions for better readability
            trading_value_formatted = f"{trading_value / 1_000_000_000:.1f}B"
            transaction_amount_formatted = f"{transaction_amount / 1_000_000:.1f}M"

            table.add_row(
                item.get("name", "KOSDAQ"),
                f"{item.get('close_price', 0):.2f}",
                f"[{change_color}]{change_str}[/{change_color}]",
                f"[yellow]{trading_value_formatted}[/yellow]",
                f"[blue]{transaction_amount_formatted}[/blue]",
            )

    console.print(table)


def _display_trading_trend(trading_trend_data):
    """Display trading trend information."""
    if not trading_trend_data:
        return

    table = Table(title="Trading Trend (Last year)")
    table.add_column("Investor Type", style="cyan")
    table.add_column("Net Amount", style="magenta")

    for investor_type, amount in trading_trend_data.items():
        # Format amount with proper currency formatting
        formatted_amount = (
            format_currency(float(amount))
            if amount and str(amount).replace("-", "").replace("+", "").isdigit()
            else str(amount)
        )
        table.add_row(investor_type, formatted_amount)

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
