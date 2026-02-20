import asyncio

from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header, LoadingIndicator

from cluefin_desk.widgets.company_info import CompanyInfoWidget
from cluefin_desk.widgets.indicator_panel import IndicatorPanel
from cluefin_desk.widgets.price_chart import PriceChartWidget


class StockDetailScreen(Screen):
    """Stock detail screen with chart, indicators, and company info."""

    BINDINGS = [
        Binding("escape", "go_back", "Back"),
        Binding("r", "refresh", "Refresh"),
    ]

    def __init__(self, stock_code: str):
        super().__init__()
        self.stock_code = stock_code

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="detail-container"):
            with Vertical(id="detail-left"):
                yield CompanyInfoWidget(id="company-info")
            with Vertical(id="detail-right"):
                yield PriceChartWidget(id="price-chart")
                yield IndicatorPanel(id="indicator-panel")
        yield Footer()

    def on_mount(self) -> None:
        self.load_detail_data()

    @work(thread=True)
    def load_detail_data(self) -> None:
        fetcher = self.app.fetcher
        loop = asyncio.new_event_loop()
        try:
            basic_df = loop.run_until_complete(fetcher.get_basic_data(self.stock_code))
            stock_df = loop.run_until_complete(fetcher.get_stock_data(self.stock_code))
        finally:
            loop.close()

        stock_name = ""
        if not basic_df.empty:
            stock_name = basic_df.iloc[0].get("stock_name", self.stock_code)

        company_info = self.query_one("#company-info", CompanyInfoWidget)
        self.app.call_from_thread(company_info.update_info, basic_df)

        chart = self.query_one("#price-chart", PriceChartWidget)
        self.app.call_from_thread(chart.update_chart, stock_df, stock_name)

        indicator = self.query_one("#indicator-panel", IndicatorPanel)
        self.app.call_from_thread(indicator.update_indicators, stock_df)

    def action_go_back(self) -> None:
        self.app.pop_screen()

    def action_refresh(self) -> None:
        self.load_detail_data()
