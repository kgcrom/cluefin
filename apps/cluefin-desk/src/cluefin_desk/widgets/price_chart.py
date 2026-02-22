import numpy as np
import pandas as pd
import plotext as plt
from cluefin_ta import SMA
from rich.text import Text
from textual.widgets import Static


class PriceChartWidget(Static):
    """Price chart widget using plotext."""

    DEFAULT_CSS = """
    PriceChartWidget {
        height: 2fr;
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._df = None
        self._stock_name = ""

    def update_chart(self, df: pd.DataFrame, stock_name: str = "") -> None:
        self._df = df
        self._stock_name = stock_name
        self._render_chart()

    def on_resize(self) -> None:
        if self._df is not None:
            self._render_chart()

    def _render_chart(self) -> None:
        if self._df is None or self._df.empty:
            self.update("No chart data available")
            return

        df = self._df.tail(60)
        close = df["close"].values
        dates = [d.strftime("%m/%d") for d in df.index]

        width = max(self.size.width - 2, 40)
        height = max(self.size.height - 2, 10)

        plt.clear_figure()
        plt.plot_size(width, height)
        plt.theme("dark")
        plt.title(f"{self._stock_name} Price Chart (60D)")

        plt.plot(close, label="Close", color="white")

        # SMA overlays
        if len(close) >= 20:
            sma20 = SMA(np.array(close, dtype=float), timeperiod=20)
            valid = ~np.isnan(sma20)
            if valid.any():
                sma20_plot = [float(v) if not np.isnan(v) else None for v in sma20]
                plt.plot(sma20_plot, label="SMA20", color="yellow")

        if len(close) >= 50:
            sma50 = SMA(np.array(close, dtype=float), timeperiod=50)
            valid = ~np.isnan(sma50)
            if valid.any():
                sma50_plot = [float(v) if not np.isnan(v) else None for v in sma50]
                plt.plot(sma50_plot, label="SMA50", color="cyan")

        # Set x-axis labels (show every 10th date)
        x_ticks = list(range(0, len(dates), 10))
        x_labels = [dates[i] for i in x_ticks]
        plt.xticks(x_ticks, x_labels)

        chart_str = plt.build()
        self.update(Text.from_ansi(chart_str))
