import numpy as np
import pandas as pd
from cluefin_ta import ADX, BBANDS, MACD, RSI
from textual.widgets import Static


def _signal_text(label: str, value: float, thresholds: tuple) -> str:
    """Generate colored signal text based on thresholds."""
    low, high = thresholds
    if value >= high:
        return f"[red]{label}: {value:.2f} (과매수)[/red]"
    elif value <= low:
        return f"[green]{label}: {value:.2f} (과매도)[/green]"
    return f"{label}: {value:.2f} (중립)"


class IndicatorPanel(Static):
    """Technical indicator summary panel."""

    DEFAULT_CSS = """
    IndicatorPanel {
        height: 1fr;
        padding: 1;
    }
    """

    def update_indicators(self, df: pd.DataFrame) -> None:
        if df is None or df.empty or len(df) < 26:
            self.update("Insufficient data for indicators")
            return

        close = np.array(df["close"].values, dtype=float)
        high = np.array(df["high"].values, dtype=float)
        low = np.array(df["low"].values, dtype=float)

        lines = ["[bold]Technical Indicators[/bold]", ""]

        # RSI
        rsi = RSI(close, timeperiod=14)
        rsi_val = rsi[-1] if not np.isnan(rsi[-1]) else 0.0
        lines.append(_signal_text("RSI(14)", rsi_val, (30, 70)))

        # MACD
        macd_line, signal, hist = MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
        if not np.isnan(macd_line[-1]):
            macd_val = macd_line[-1]
            signal_val = signal[-1]
            hist_val = hist[-1]
            if hist_val > 0:
                lines.append(f"[red]MACD: {macd_val:.2f} / Signal: {signal_val:.2f} (상승)[/red]")
            else:
                lines.append(f"[blue]MACD: {macd_val:.2f} / Signal: {signal_val:.2f} (하락)[/blue]")
        else:
            lines.append("MACD: N/A")

        # Bollinger Bands
        upper, middle, lower = BBANDS(close, timeperiod=20, nbdevup=2.0, nbdevdn=2.0)
        if not np.isnan(upper[-1]):
            curr = close[-1]
            bb_pos = (curr - lower[-1]) / (upper[-1] - lower[-1]) * 100 if upper[-1] != lower[-1] else 50.0
            lines.append(f"BB(20): U={upper[-1]:,.0f} M={middle[-1]:,.0f} L={lower[-1]:,.0f}")
            if bb_pos >= 80:
                lines.append(f"  [red]BB%: {bb_pos:.1f}% (상단 근접)[/red]")
            elif bb_pos <= 20:
                lines.append(f"  [green]BB%: {bb_pos:.1f}% (하단 근접)[/green]")
            else:
                lines.append(f"  BB%: {bb_pos:.1f}%")
        else:
            lines.append("BB(20): N/A")

        # ADX
        adx = ADX(high, low, close, timeperiod=14)
        if not np.isnan(adx[-1]):
            adx_val = adx[-1]
            if adx_val >= 25:
                lines.append(f"[bold]ADX(14): {adx_val:.2f} (강한 추세)[/bold]")
            else:
                lines.append(f"ADX(14): {adx_val:.2f} (약한 추세)")
        else:
            lines.append("ADX(14): N/A")

        self.update("\n".join(lines))
