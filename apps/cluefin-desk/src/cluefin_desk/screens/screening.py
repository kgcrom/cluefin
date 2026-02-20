from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header, TabbedContent, TabPane

from cluefin_desk.widgets.market_overview import MarketOverviewBar
from cluefin_desk.widgets.stock_table import StockScreeningTable


class ScreeningScreen(Screen):
    """Main screening screen with tabbed stock rankings."""

    BINDINGS = [
        Binding("r", "refresh", "Refresh"),
        Binding("enter", "select_stock", "Detail"),
        Binding("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield MarketOverviewBar(id="market-bar")
        with Vertical(id="screening-content"):
            with TabbedContent(id="screening-tabs"):
                with TabPane("상승률", id="tab-gainers"):
                    yield StockScreeningTable(id="table-gainers")
                with TabPane("거래량", id="tab-volume"):
                    yield StockScreeningTable(id="table-volume")
                with TabPane("거래대금", id="tab-value"):
                    yield StockScreeningTable(id="table-value")
        yield Footer()

    def on_mount(self) -> None:
        self.load_all_data()

    @work(thread=True)
    def load_all_data(self) -> None:
        self._load_market_overview()
        self._load_screening_data()

    def _load_market_overview(self) -> None:
        import asyncio

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

        gainers = screener.get_top_gainers()
        table_gainers = self.query_one("#table-gainers", StockScreeningTable)
        self.app.call_from_thread(table_gainers.load_data, gainers)

        volume = screener.get_top_volume()
        table_volume = self.query_one("#table-volume", StockScreeningTable)
        self.app.call_from_thread(table_volume.load_data, volume)

        value = screener.get_top_value()
        table_value = self.query_one("#table-value", StockScreeningTable)
        self.app.call_from_thread(table_value.load_data, value)

    def action_refresh(self) -> None:
        self.load_all_data()

    def action_select_stock(self) -> None:
        tabs = self.query_one("#screening-tabs", TabbedContent)
        active_tab_id = tabs.active
        table_map = {
            "tab-gainers": "#table-gainers",
            "tab-volume": "#table-volume",
            "tab-value": "#table-value",
        }
        table_id = table_map.get(active_tab_id, "#table-gainers")
        table = self.query_one(table_id, StockScreeningTable)
        stock_code = table.get_selected_stock_code()
        if stock_code:
            from cluefin_desk.screens.stock_detail import StockDetailScreen

            self.app.push_screen(StockDetailScreen(stock_code=stock_code))

    def action_quit(self) -> None:
        self.app.exit()
