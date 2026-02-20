from typing import List

from textual.widgets import DataTable

from cluefin_desk.data.screener import ScreeningItem

COLUMNS = [
    ("#", 4),
    ("종목코드", 8),
    ("종목명", 20),
    ("현재가", 12),
    ("등락률", 10),
    ("거래량", 14),
]


class StockScreeningTable(DataTable):
    """DataTable for stock screening results."""

    DEFAULT_CSS = """
    StockScreeningTable {
        height: 1fr;
    }
    """

    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.zebra_stripes = True
        for label, width in COLUMNS:
            self.add_column(label, key=label, width=width)

    def load_data(self, items: List[ScreeningItem]) -> None:
        self.clear()
        for item in items:
            rate = float(item.change_rate) if item.change_rate else 0.0
            if rate > 0:
                rate_str = f"[red]+{rate:.2f}%[/red]"
            elif rate < 0:
                rate_str = f"[blue]{rate:.2f}%[/blue]"
            else:
                rate_str = f"{rate:.2f}%"

            try:
                price_val = int(float(item.current_price))
                price_str = f"{price_val:,}"
            except (ValueError, TypeError):
                price_str = item.current_price

            try:
                vol_val = int(float(item.volume))
                vol_str = f"{vol_val:,}"
            except (ValueError, TypeError):
                vol_str = item.volume

            self.add_row(
                str(item.rank),
                item.stock_code,
                item.stock_name,
                price_str,
                rate_str,
                vol_str,
                key=item.stock_code,
            )

    def get_selected_stock_code(self) -> str | None:
        if self.cursor_row is not None and self.row_count > 0:
            row_key, _ = self.coordinate_to_cell_key(self.cursor_coordinate)
            return str(row_key.value)
        return None
