from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import DataTable, Header, Static, TabbedContent, TabPane

from cluefin_desk.screens._guard import screen_gone
from cluefin_desk.widgets.market_overview import MarketOverviewBar
from cluefin_desk.widgets.nav_bar import NavBar
from cluefin_desk.widgets.nav_footer import NavFooter
from cluefin_desk.widgets.stock_table import StockScreeningTable

TAB_CONFIG = [
    ("상승률", "tab-gainers", "table-gainers"),
    ("하락률", "tab-losers", "table-losers"),
    ("거래량", "tab-volume", "table-volume"),
    ("거래대금", "tab-value", "table-value"),
    ("외인순매", "tab-foreigner", "table-foreigner"),
    ("신고가", "tab-newhigh", "table-newhigh"),
    ("급등/급락", "tab-volatility", "table-volatility"),
    ("신용잔", "tab-margin", "table-margin"),
    # KIS-backed tabs — stay empty without KIS keys
    ("배당수익률", "tab-dividend", "table-dividend"),
    ("공매도", "tab-short", "table-short"),
    ("신용상위", "tab-credit", "table-credit"),
    ("이격도", "tab-disparity", "table-disparity"),
]

KIS_TABLE_IDS = frozenset({"table-dividend", "table-short", "table-credit", "table-disparity"})


class ScreeningScreen(Screen):
    """Screen 2: Rankings with 8 tabs."""

    BINDINGS = [
        Binding("r", "refresh", "Refresh"),
        Binding("enter", "select_stock", "Detail"),
        Binding("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield NavBar(id="nav-bar")
        yield MarketOverviewBar(id="market-bar")
        with Vertical(id="screening-content"):
            with TabbedContent(id="screening-tabs"):
                for tab_label, tab_id, table_id in TAB_CONFIG:
                    with TabPane(tab_label, id=tab_id):
                        yield StockScreeningTable(id=table_id)
                        # 표만 있으면 빈 표가 "데이터 없음·키 없음·실패" 중 무엇인지 알 수 없다
                        yield Static("Loading...", id=f"status-{table_id}", classes="tab-status")
        yield NavFooter(active_screen_key="2")

    def on_mount(self) -> None:
        nav = self.query_one("#nav-bar", NavBar)
        nav.set_active("2")
        self.load_all_data()

    # 12개 탭을 한 스레드에서 차례로 돌리면 KIS 탭 4개는 키움 8건 + KIS 인증이 끝난 뒤에야
    # 채워져, 탭을 눌렀을 때 그제서야 조회하는 것처럼 보인다. 소스별로 워커를 나눠
    # 동시에 미리 채운다. 각 그룹은 exclusive — `r` 연타로 겹치는 워커는 최신만 남긴다.
    def load_all_data(self) -> None:
        self._load_kiwoom_tabs()
        self._load_kis_tabs()

    @work(thread=True, exclusive=True, group="screening-load-kiwoom")
    def _load_kiwoom_tabs(self) -> None:
        screener = self.app.screener
        self._fill_tables(
            [
                ("table-gainers", screener.get_top_gainers),
                ("table-losers", screener.get_top_losers),
                ("table-volume", screener.get_top_volume),
                ("table-value", screener.get_top_value),
                ("table-foreigner", screener.get_top_foreigner_net_buy),
                ("table-newhigh", screener.get_new_high_price),
                ("table-volatility", screener.get_price_volatility),
                ("table-margin", screener.get_top_margin_ratio),
            ]
        )

    @work(thread=True, exclusive=True, group="screening-load-kis")
    def _load_kis_tabs(self) -> None:
        screener = self.app.screener
        self._fill_tables(
            [
                ("table-dividend", screener.get_dividend_yield_top),
                ("table-short", screener.get_short_selling_top),
                ("table-credit", screener.get_credit_balance_top),
                ("table-disparity", screener.get_disparity_index_top),
            ]
        )

    def _fill_tables(self, loaders) -> None:
        has_kis = self.app.fetcher.has_kis
        for table_id, loader_fn in loaders:
            if table_id in KIS_TABLE_IDS and not has_kis:
                self._set_status(table_id, "KIS 키 없음 — KIS_APP_KEY / KIS_SECRET_KEY 설정 후 사용 가능")
                continue
            try:
                data = loader_fn()
                table = self.query_one(f"#{table_id}", StockScreeningTable)
                self.app.call_from_thread(table.load_data, data)
                # screener 는 조회 실패를 삼키고 [] 를 주므로, 빈 표는 "없음" 과 "실패" 를
                # 구분할 수 없다 — 원인은 로그(ERROR) 에 남는다
                self._set_status(table_id, self._status_text(len(data)))
            except Exception as e:
                if screen_gone(self, e):
                    return
                from loguru import logger

                logger.error(f"Failed to load {table_id}: {e}")
                self._set_status(table_id, f"로딩 실패: {e}")

    @staticmethod
    def _status_text(count: int) -> str:
        return f"{count}건" if count else "데이터 없음 (조회 실패면 로그에 원인이 남는다)"

    def _set_status(self, table_id: str, text: str) -> None:
        def _apply():
            self.query_one(f"#status-{table_id}", Static).update(text)

        self.app.call_from_thread(_apply)

    def action_refresh(self) -> None:
        self.load_all_data()

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        stock_code = str(event.row_key.value)
        if stock_code:
            from cluefin_desk.screens.stock_detail import StockDetailScreen

            self.app.push_screen(StockDetailScreen(stock_code=stock_code))

    def action_select_stock(self) -> None:
        tabs = self.query_one("#screening-tabs", TabbedContent)
        active_tab_id = tabs.active
        table_map = {cfg[1]: f"#{cfg[2]}" for cfg in TAB_CONFIG}
        table_id = table_map.get(active_tab_id, f"#{TAB_CONFIG[0][2]}")
        table = self.query_one(table_id, StockScreeningTable)
        stock_code = table.get_selected_stock_code()
        if stock_code:
            from cluefin_desk.screens.stock_detail import StockDetailScreen

            self.app.push_screen(StockDetailScreen(stock_code=stock_code))

    def action_quit(self) -> None:
        self.app.exit()
