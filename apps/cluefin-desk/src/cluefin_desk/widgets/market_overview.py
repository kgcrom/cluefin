from typing import Any, Dict, List

from textual.app import ComposeResult
from textual.widgets import Static


class MarketOverviewBar(Static):
    """KOSPI/KOSDAQ index summary bar."""

    DEFAULT_CSS = """
    MarketOverviewBar {
        height: 1;
        background: $surface;
        color: $text;
        padding: 0 1;
    }
    """

    def update_indices(self, kospi: List[Dict[str, Any]], kosdaq: List[Dict[str, Any]]) -> None:
        parts = []
        for item in kospi:
            rate = item.get("fluctuation_rate", 0.0)
            color = "red" if rate >= 0 else "blue"
            sign = "+" if rate >= 0 else ""
            parts.append(f"[bold]{item['name']}[/bold] {item['close_price']:,.2f} [{color}]{sign}{rate:.2f}%[/{color}]")

        for item in kosdaq:
            rate = item.get("fluctuation_rate", 0.0)
            color = "red" if rate >= 0 else "blue"
            sign = "+" if rate >= 0 else ""
            parts.append(f"[bold]{item['name']}[/bold] {item['close_price']:,.2f} [{color}]{sign}{rate:.2f}%[/{color}]")

        self.update("  |  ".join(parts) if parts else "Market data loading...")

    def compose(self) -> ComposeResult:
        yield from []
