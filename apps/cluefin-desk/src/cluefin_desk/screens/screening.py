import asyncio

from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import DataTable, Header, TabbedContent, TabPane

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
]


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
        yield NavFooter(active_screen_key="2")

    def on_mount(self) -> None:
        nav = self.query_one("#nav-bar", NavBar)
        nav.set_active("2")
        self.load_all_data()

    @work(thread=True)
    def load_all_data(self) -> None:
        self._load_market_overview()
        self._load_screening_data()

    def _load_market_overview(self) -> None:
        fetcher = self.app.fetcher
        loop = asyncio.new_event_loop()
        try:
            kospi = loop.run_until_complete(fetcher.get_kospi_index_series())
            kosdaq = loop.run_until_complete(fetcher.get_kosdaq_index_series())
        finally:
            loop.close()

        bar = self.query_one("#market-bar", MarketOverviewBar)
        self.app.call_from_thread(bar.update_indices, kospi, kosdaq)

    def _load_screening_data(self) -> None:
        screener = self.app.screener

        loaders = [
            ("table-gainers", screener.get_top_gainers),
            ("table-losers", screener.get_top_losers),
            ("table-volume", screener.get_top_volume),
            ("table-value", screener.get_top_value),
            ("table-foreigner", screener.get_top_foreigner_net_buy),
            ("table-newhigh", screener.get_new_high_price),
            ("table-volatility", screener.get_price_volatility),
            ("table-margin", screener.get_top_margin_ratio),
        ]

        for table_id, loader_fn in loaders:
            try:
                data = loader_fn()
                table = self.query_one(f"#{table_id}", StockScreeningTable)
                self.app.call_from_thread(table.load_data, data)
            except Exception:
                pass

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
