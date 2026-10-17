"""Screen 6: KIS HTS 관심종목 — 그룹 → 그룹별 종목 → 멀티 시세.

관심 그룹은 한국투자 앱(MTS)에서 만든 것도 바로 보인다(2026-10-17 실측). 조회 전용이고,
HTS ID(`KIS_HTS_USER_ID`)가 있어야 한다. ID 값은 화면·로그에 찍지 않는다.
"""

from typing import Optional

from rich.markup import escape
from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import DataTable, Header, Static

from cluefin_desk.screens._guard import guarded, set_text
from cluefin_desk.widgets.nav_bar import NavBar
from cluefin_desk.widgets.nav_footer import NavFooter

NO_HTS = "KIS_HTS_USER_ID 미설정 — .env 에 KIS HTS 로그인 ID 를 넣고 재시작 (KIS 키도 필요)"
NO_GROUPS = "관심 그룹 없음 — 한국투자 앱·HTS 에서 그룹을 만들면 여기에 보인다"

STOCK_COLUMNS = [
    ("종목코드", 8),
    ("종목명", 16),
    ("현재가", 10),
    ("등락률", 8),
    ("거래량", 12),
    ("거래대금(억)", 11),
    ("시가", 10),
    ("고가", 10),
    ("저가", 10),
]


class WatchlistScreen(Screen):
    """Screen 6: KIS HTS watchlist groups and their quotes."""

    BINDINGS = [
        Binding("r", "refresh", "Refresh"),
        Binding("escape", "go_back", "Back"),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self._group_names: dict[str, str] = {}
        self._current_group: Optional[str] = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield NavBar(id="nav-bar")
        with Horizontal(id="watchlist-content"):
            yield DataTable(id="watchlist-groups")
            with Vertical(id="watchlist-main"):
                yield DataTable(id="watchlist-stocks")
                yield Static("", id="watchlist-status")
        yield NavFooter(active_screen_key="6")

    def on_mount(self) -> None:
        self.query_one("#nav-bar", NavBar).set_active("6")
        self._setup_tables()
        if not self.app.fetcher.has_hts:
            self.query_one("#watchlist-status", Static).update(NO_HTS)
            return
        self.query_one("#watchlist-status", Static).update("관심 그룹 불러오는 중…")
        self.load_groups()

    def _setup_tables(self) -> None:
        groups = self.query_one("#watchlist-groups", DataTable)
        groups.cursor_type = "row"
        groups.zebra_stripes = True
        for label, width in [("그룹", 16), ("종목수", 6)]:
            groups.add_column(label, key=label, width=width)

        stocks = self.query_one("#watchlist-stocks", DataTable)
        stocks.cursor_type = "row"
        stocks.zebra_stripes = True
        for label, width in STOCK_COLUMNS:
            stocks.add_column(label, key=label, width=width)

    # ── loaders ──────────────────────────────

    @work(thread=True, exclusive=True, group="watchlist-load")
    def load_groups(self) -> None:
        guarded(self, "#watchlist-status", "관심 그룹", self._load_groups)

    def _load_groups(self) -> None:
        groups = self.app.fetcher.get_watchlist_groups()
        self._group_names = {group.inter_grp_code: group.inter_grp_name for group in groups}
        rows = [
            (group.inter_grp_code, escape(group.inter_grp_name), WatchlistScreen._number(group.ask_cnt))
            for group in groups
        ]
        self.app.call_from_thread(self._fill_groups, rows)
        if not groups:
            set_text(self, "#watchlist-status", NO_GROUPS)
            return
        # 새로고침이면 보던 그룹을, 처음이거나 그룹이 사라졌으면 첫 그룹을 연다
        if self._current_group not in self._group_names:
            self._current_group = groups[0].inter_grp_code
        self._load_stocks(self._current_group)

    def _fill_groups(self, rows: list[tuple[str, str, str]]) -> None:
        table = self.query_one("#watchlist-groups", DataTable)
        table.clear()
        for code, name, count in rows:
            table.add_row(name, count, key=code)

    @work(thread=True, exclusive=True, group="watchlist-load")
    def load_stocks(self, group_code: str) -> None:
        guarded(self, "#watchlist-status", "관심종목", self._load_stocks, group_code)

    def _load_stocks(self, group_code: str) -> None:
        fetcher = self.app.fetcher
        name = escape(self._group_names.get(group_code, group_code))
        stocks = fetcher.get_watchlist_stocks(group_code)
        quotes = (
            fetcher.get_watchlist_quotes([(s.fid_mrkt_cls_code or "J", s.jong_code) for s in stocks]) if stocks else []
        )
        rows = self._format_quote_rows(stocks, quotes)
        self.app.call_from_thread(self._fill_stocks, rows)
        status = f"{name} — {len(rows)}종목 · Enter 상세 · r 새로고침" if rows else f"{name} — 종목 없음"
        set_text(self, "#watchlist-status", status)

    def _fill_stocks(self, rows: list[tuple]) -> None:
        table = self.query_one("#watchlist-stocks", DataTable)
        table.clear()
        for row in rows:
            table.add_row(*row, key=row[0])

    # ── formatting (pure) ────────────────────

    @staticmethod
    def _format_quote_rows(stocks: list, quotes: list) -> list[tuple]:
        """그룹 순서대로 한 행씩. 시세가 빠진 종목도 코드·이름은 남긴다."""
        by_code = {quote.inter_shrn_iscd: quote for quote in quotes}
        rows = []
        for stock in stocks:
            quote = by_code.get(stock.jong_code)
            name = escape((quote.inter_kor_isnm if quote else "") or stock.hts_kor_isnm)
            if quote is None:
                rows.append((stock.jong_code, name, *["-"] * (len(STOCK_COLUMNS) - 2)))
                continue
            rows.append(
                (
                    stock.jong_code,
                    name,
                    WatchlistScreen._number(quote.inter2_prpr),
                    WatchlistScreen._rate(quote.prdy_ctrt),
                    WatchlistScreen._number(quote.acml_vol),
                    WatchlistScreen._eok(quote.acml_tr_pbmn),
                    WatchlistScreen._number(quote.inter2_oprc),
                    WatchlistScreen._number(quote.inter2_hgpr),
                    WatchlistScreen._number(quote.inter2_lwpr),
                )
            )
        return rows

    @staticmethod
    def _to_float(value: str) -> Optional[float]:
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _number(value: str) -> str:
        number = WatchlistScreen._to_float(value)
        return "-" if number is None else f"{number:,.0f}"

    @staticmethod
    def _eok(value: str) -> str:
        number = WatchlistScreen._to_float(value)
        return "-" if number is None else f"{number / 1e8:,.1f}"

    @staticmethod
    def _rate(value: str) -> str:
        rate = WatchlistScreen._to_float(value)
        if rate is None:
            return "-"
        if rate > 0:
            return f"[red]+{rate:.2f}%[/red]"
        if rate < 0:
            return f"[blue]{rate:.2f}%[/blue]"
        return f"{rate:.2f}%"

    # ── events & actions ─────────────────────

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        key = str(event.row_key.value)
        if event.data_table.id == "watchlist-groups":
            self._current_group = key
            self.query_one("#watchlist-status", Static).update("관심종목 불러오는 중…")
            self.load_stocks(key)
        elif event.data_table.id == "watchlist-stocks" and key:
            from cluefin_desk.screens.stock_detail import StockDetailScreen

            self.app.push_screen(StockDetailScreen(stock_code=key))

    def action_refresh(self) -> None:
        if self.app.fetcher.has_hts:
            self.load_groups()

    def action_go_back(self) -> None:
        self.app.action_switch_screen("1")

    def action_quit(self) -> None:
        self.app.exit()
