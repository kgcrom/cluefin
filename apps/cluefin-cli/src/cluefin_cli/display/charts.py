from typing import Optional

import pandas as pd
import plotext as plt
from loguru import logger


class ChartRenderer:
    """Renders charts in the terminal using plotext."""

    def render_stock_chart(self, data: pd.DataFrame, indicators: Optional[pd.DataFrame] = None):
        """
        Render stock price chart with technical indicators in terminal.

        Args:
            data: Stock OHLCV data
            indicators: Technical indicators data
        """
        if data.empty:
            logger.info("No data available for chart rendering")
            return

        # Prepare data
        dates = list(range(len(data.tail(50))))  # Use indices instead of dates for plotext
        closes = data["close"].tail(50).tolist()
        volumes = data["volume"].tail(50).tolist()

        # Create subplots
        plt.subplots(2, 1)

        # Price chart (top subplot)
        plt.subplot(1, 1)
        plt.title("Stock Price Chart (Last 50 Days)")

        # Plot closing price
        plt.plot(dates, closes, label="Close Price", color="blue", marker="dot")

        # Add moving averages if available
        if indicators is not None and not indicators.empty:
            indicators_tail = indicators.tail(50)

            if "sma_20" in indicators_tail and not indicators_tail["sma_20"].isna().all():
                sma_20 = indicators_tail["sma_20"].ffill().tolist()
                plt.plot(dates, sma_20, label="SMA(20)", color="red")

            if "sma_50" in indicators_tail and not indicators_tail["sma_50"].isna().all():
                sma_50 = indicators_tail["sma_50"].ffill().tolist()
                plt.plot(dates, sma_50, label="SMA(50)", color="green")

        plt.xlabel("Days")
        plt.ylabel("Price (₩)")

        # Volume chart (bottom subplot)
        plt.subplot(2, 1)
        plt.title("Volume")
        plt.bar(dates, volumes, color="gray")
        plt.xlabel("Days")
        plt.ylabel("Volume")

        # Show the chart
        plt.show()

        # RSI chart if available
        if indicators is not None and "rsi" in indicators and not indicators["rsi"].isna().all():
            self._render_rsi_chart(dates, indicators.tail(50))

        # MACD chart if available
        if (
            indicators is not None
            and "macd" in indicators
            and "macd_signal" in indicators
            and not indicators["macd"].isna().all()
        ):
            self._render_macd_chart(dates, indicators.tail(50))

    def _render_rsi_chart(self, dates, indicators):
        """Render RSI chart."""
        plt.clear_data()
        plt.title("RSI (14)")

        rsi_values = indicators["rsi"].ffill().tolist()
        plt.plot(dates, rsi_values, label="RSI", color="purple", marker="dot")

        # Add overbought/oversold lines
        plt.hline(70, color="red")
        plt.hline(30, color="green")
        plt.hline(50, color="gray")

        plt.xlabel("Days")
        plt.ylabel("RSI")
        plt.ylim(0, 100)
        plt.show()

    def _render_macd_chart(self, dates, indicators):
        """Render MACD chart."""
        plt.clear_data()
        plt.title("MACD")

        macd_values = indicators["macd"].fillna(0).tolist()
        signal_values = indicators["macd_signal"].fillna(0).tolist()
        histogram_values = (
            indicators.get("macd_histogram", indicators["macd"] - indicators["macd_signal"]).fillna(0).tolist()
        )

        plt.plot(dates, macd_values, label="MACD", color="blue", marker="dot")
        plt.plot(dates, signal_values, label="Signal", color="red", marker="dot")
        plt.bar(dates, histogram_values, label="Histogram", color="gray")

        plt.hline(0, color="black")
        plt.xlabel("Days")
        plt.ylabel("MACD")
        plt.show()

    def render_market_overview(self, kospi_data, kosdaq_data):
        """Render market indices overview."""
        plt.clear_data()
        plt.title("Market Indices")

        indices = ["KOSPI", "KOSDAQ"]
        values = [kospi_data.get("value", 0), kosdaq_data.get("value", 0)]
        changes = [kospi_data.get("change", 0), kosdaq_data.get("change", 0)]

        # Color based on change
        colors = ["green" if change >= 0 else "red" for change in changes]

        plt.bar(indices, values, color=colors)

        # Add change labels
        for i, (_, value, change) in enumerate(zip(indices, values, changes, strict=False)):
            plt.text(i, value + 50, f"{change:+.2f}%")

        plt.xlabel("Index")
        plt.ylabel("Value")
        plt.show()

    def render_foreign_trading_chart(self, foreign_data):
        """Render foreign trading data as a simple bar chart."""
        if not foreign_data:
            return

        plt.clear_data()
        plt.title("Foreign Trading")

        categories = ["Buy", "Sell"]
        amounts = [
            foreign_data.get("buy", 0) / 1e9,  # Convert to billions
            foreign_data.get("sell", 0) / 1e9,
        ]

        colors = ["green", "red"]
        plt.bar(categories, amounts, color=colors)

        plt.xlabel("Transaction Type")
        plt.ylabel("Amount (Billion ₩)")
        plt.show()
