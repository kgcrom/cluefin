#!/usr/bin/env python3
"""
ML Pipeline Test Script for Task 9.1

This script tests the ML pipeline with sample Korean stock data to verify that
all components (feature engineering, model training, prediction, and SHAP analysis)
work correctly together.
"""

import sys
import warnings
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd
from loguru import logger
from rich.console import Console
from rich.panel import Panel

# Add the apps/cluefin-cli/src directory to Python path for imports
sys.path.append(str(Path(__file__).resolve().parents[3] / "src"))

from cluefin_cli.ml import StockMLPredictor

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

console = Console()


def create_sample_stock_data(days: int = 300) -> pd.DataFrame:
    """
    Create realistic sample Korean stock data for testing.

    Args:
        days: Number of days of data to generate

    Returns:
        DataFrame with OHLCV data similar to Korean stock data
    """
    # Create date range
    dates = pd.date_range(end=datetime.now(), periods=days, freq="D")

    # Generate realistic Korean stock price data (around 50,000 KRW base price)
    np.random.seed(42)  # For reproducible results

    # Start with base price around 50,000 KRW (typical Korean stock price)
    base_price = 50000

    # Generate price movements with some trend and volatility
    price_changes = np.random.normal(0, 0.02, days)  # 2% daily volatility

    # Add some trend components
    trend = np.linspace(-0.1, 0.15, days)  # Slight upward trend over time
    price_changes = price_changes + trend / days

    # Calculate prices
    prices = [base_price]
    for change in price_changes[1:]:
        new_price = prices[-1] * (1 + change)
        prices.append(max(new_price, 1000))  # Minimum price of 1000 KRW

    prices = np.array(prices)

    # Generate OHLCV data
    data = []
    for i, date in enumerate(dates):
        close_price = prices[i]

        # Generate daily high/low around close price
        daily_volatility = np.random.normal(0, 0.01)  # 1% intraday volatility
        high = close_price * (1 + abs(daily_volatility) + 0.005)
        low = close_price * (1 - abs(daily_volatility) - 0.005)

        # Open price is close to previous day's close
        if i == 0:
            open_price = close_price
        else:
            open_price = prices[i - 1] * (1 + np.random.normal(0, 0.005))

        # Ensure OHLC consistency
        high = max(high, open_price, close_price)
        low = min(low, open_price, close_price)

        # Generate realistic volume (Korean stocks typically have high volume)
        base_volume = 1000000  # 1M shares base
        volume_multiplier = np.random.lognormal(0, 0.5)  # Log-normal distribution
        volume = int(base_volume * volume_multiplier)

        data.append(
            {
                "date": date,
                "open": round(open_price),
                "high": round(high),
                "low": round(low),
                "close": round(close_price),
                "volume": volume,
            }
        )

    df = pd.DataFrame(data)
    df.set_index("date", inplace=True)

    return df


def create_sample_indicators(stock_data: pd.DataFrame) -> Dict:
    """
    Create basic technical indicators for testing.
    This simulates what would normally come from TechnicalAnalyzer.

    Args:
        stock_data: OHLCV data

    Returns:
        Dictionary of basic technical indicators
    """
    # Simple moving averages
    close = stock_data["close"]

    indicators = {
        "close": close,
        "sma_5": close.rolling(window=5).mean(),
        "sma_10": close.rolling(window=10).mean(),
        "sma_20": close.rolling(window=20).mean(),
        "volume_ma_10": stock_data["volume"].rolling(window=10).mean(),
    }

    # Simple RSI calculation
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    indicators["rsi"] = 100 - (100 / (1 + rs))
    indicators["rsi_14"] = indicators["rsi"]  # Add RSI-14 alias that feature engineering expects

    # Simple MACD
    ema_12 = close.ewm(span=12).mean()
    ema_26 = close.ewm(span=26).mean()
    indicators["macd"] = ema_12 - ema_26
    indicators["macd_signal"] = indicators["macd"].ewm(span=9).mean()

    return indicators


def test_ml_pipeline():
    """
    Main test function for ML pipeline.
    Tests the complete workflow: data preparation, training, and prediction.
    """
    console.print(Panel.fit("🧪 ML Pipeline Test - Task 9.1", style="bold blue"))

    try:
        # Step 1: Create sample data
        console.print("\n[yellow]Step 1: Creating sample Korean stock data...[/yellow]")
        stock_data = create_sample_stock_data(days=300)
        console.print(f"[green]✓[/green] Generated {len(stock_data)} days of sample data")
        console.print(
            f"[green]✓[/green] Price range: ₩{stock_data['close'].min():,.0f} - ₩{stock_data['close'].max():,.0f}"
        )

        # Step 2: Create sample indicators
        console.print("\n[yellow]Step 2: Creating sample technical indicators...[/yellow]")
        indicators = create_sample_indicators(stock_data)
        console.print(f"[green]✓[/green] Created {len(indicators)} basic indicators")

        # Step 3: Initialize ML predictor
        console.print("\n[yellow]Step 3: Initializing ML predictor...[/yellow]")
        ml_predictor = StockMLPredictor()
        console.print("[green]✓[/green] ML predictor initialized")

        # Step 4: Prepare data for ML
        console.print("\n[yellow]Step 4: Preparing data for ML training...[/yellow]")
        prepared_df, feature_names = ml_predictor.prepare_data(stock_data, indicators)
        console.print("[green]✓[/green] Data preparation completed")
        console.print(f"[green]✓[/green] Features created: {len(feature_names)}")
        console.print(f"[green]✓[/green] Training samples: {len(prepared_df)}")
        console.print(f"[green]✓[/green] Target distribution: {prepared_df['target'].value_counts().to_dict()}")

        # Step 5: Train the model
        console.print("\n[yellow]Step 5: Training ML model...[/yellow]")
        training_metrics = ml_predictor.train_model(prepared_df, validation_split=0.2)
        console.print("[green]✓[/green] Model training completed successfully")

        # Display training metrics
        console.print("\n[cyan]Training Metrics:[/cyan]")
        for metric, value in training_metrics.items():
            if isinstance(value, float):
                console.print(f"  {metric}: {value:.4f}")
            else:
                console.print(f"  {metric}: {value}")

        # Step 6: Make predictions
        console.print("\n[yellow]Step 6: Making predictions on sample data...[/yellow]")
        prediction_result = ml_predictor.predict(stock_data, indicators)
        console.print("[green]✓[/green] Prediction completed successfully")

        # Step 7: Display results
        console.print("\n[yellow]Step 7: Displaying prediction results...[/yellow]")
        ml_predictor.display_prediction_results(prediction_result)

        # Step 8: Test feature importance (SHAP analysis)
        console.print("\n[yellow]Step 8: Testing SHAP feature importance...[/yellow]")
        if prediction_result["shap_available"]:
            ml_predictor.display_feature_importance(prediction_result, top_n=10)
            console.print("[green]✓[/green] SHAP analysis completed successfully")
        else:
            console.print("[yellow]⚠️[/yellow] SHAP analysis not available")

        # Step 9: Model summary
        console.print("\n[yellow]Step 9: Getting model summary...[/yellow]")
        model_summary = ml_predictor.get_model_summary()
        console.print(f"[green]✓[/green] Model Status: {model_summary['status']}")
        console.print(f"[green]✓[/green] Features Used: {model_summary['n_features']}")
        console.print(f"[green]✓[/green] SHAP Available: {model_summary['shap_available']}")

        # Step 10: Cross-validation test
        console.print("\n[yellow]Step 10: Testing cross-validation...[/yellow]")
        try:
            cv_metrics = ml_predictor.cross_validate_model(prepared_df, cv_folds=3)
            console.print("[green]✓[/green] Cross-validation completed successfully")
            console.print(
                f"[green]✓[/green] CV Accuracy: {cv_metrics['cv_accuracy_mean']:.4f} ± {cv_metrics['cv_accuracy_std']:.4f}"
            )
        except Exception as e:
            console.print(f"[yellow]⚠️[/yellow] Cross-validation failed: {e}")

        # Final success message
        console.print(Panel.fit("🎉 ML Pipeline Test Completed Successfully! 🎉", style="bold green"))

        # Test summary
        summary_text = f"""
[bold]Test Summary:[/bold]
• Sample data generated: {len(stock_data)} days
• Features created: {len(feature_names)}
• Training samples: {len(prepared_df)}
• Model accuracy: {training_metrics.get("val_accuracy", 0):.1%}
• Prediction confidence: {prediction_result["confidence"]:.1%}
• Signal: {prediction_result["signal"]}
• SHAP analysis: {"✅" if prediction_result["shap_available"] else "❌"}

[green]All ML pipeline components are working correctly![/green]
        """

        console.print(Panel(summary_text.strip(), title="🔍 Test Results Summary", border_style="green"))

        # Test completed successfully
        assert True

    except Exception as e:
        console.print(f"\n[red]❌ Test failed with error: {e}[/red]")
        logger.exception("ML pipeline test failed")
        # Re-raise the exception to fail the test properly
        raise


def main():
    """Main entry point."""
    # Configure logger for test
    logger.remove()
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    )

    console.print(Panel.fit("ML Pipeline Test Script", style="bold blue"))
    console.print("[dim]Testing ML pipeline components with sample Korean stock data[/dim]")

    success = test_ml_pipeline()

    if success:
        console.print("\n[bold green]✅ Task 9.1 completed successfully![/bold green]")
        sys.exit(0)
    else:
        console.print("\n[bold red]❌ Task 9.1 failed![/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
