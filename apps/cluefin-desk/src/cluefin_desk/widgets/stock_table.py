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


def _unsigned_int(value: str) -> str:
    """키움 현재가·거래량은 전일 대비 부호(`+`/`-`)를 달고 온다 — 값 자체는 음수가 아니다."""
    try:
        return f"{abs(int(float(value))):,}"
    except (ValueError, TypeError):
        return value


class StockScreeningTable(DataTable):
    """DataTable for stock screening results.

    `extra_label` 을 주면 7번째 열에 `ScreeningItem.extra`(탭의 정렬 기준 지표)를 보인다.
    """

    DEFAULT_CSS = """
    StockScreeningTable {
        height: 1fr;
    }
    """

    def __init__(self, *args, extra_label: str | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra_label = extra_label

    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.zebra_stripes = True
        for label, width in COLUMNS:
            self.add_column(label, key=label, width=width)
        if self.extra_label:
            self.add_column(self.extra_label, key="extra", width=14)

    def load_data(self, items: list[ScreeningItem]) -> None:
        self.clear()
        for item in items:
            self.add_row(*self.row_cells(item), key=item.stock_code)

    def row_cells(self, item: ScreeningItem) -> list[str]:
        cells = [
            str(item.rank),
            item.stock_code,
            item.stock_name,
            _unsigned_int(item.current_price),
            self._format_rate(item.change_rate),
            _unsigned_int(item.volume),
        ]
        if self.extra_label:
            cells.append(item.extra or "-")
        return cells

    @staticmethod
    def _format_rate(change_rate: str) -> str:
        # 등락률을 주지 않는 랭킹(외인 순매수 등)은 0.00% 가 아니라 '-' 로 둔다
        if not change_rate:
            return "-"
        try:
            rate = float(change_rate)
        except ValueError:
            return change_rate
        if rate > 0:
            return f"[red]+{rate:.2f}%[/red]"
        if rate < 0:
            return f"[blue]{rate:.2f}%[/blue]"
        return f"{rate:.2f}%"

    def get_selected_stock_code(self) -> str | None:
        if self.cursor_row is not None and self.row_count > 0:
            row_key, _ = self.coordinate_to_cell_key(self.cursor_coordinate)
            return str(row_key.value)
        return None
