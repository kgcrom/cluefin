import threading
from pathlib import Path

from textual.app import App
from textual.binding import Binding

from cluefin_desk.config.settings import settings
from cluefin_desk.data.fetcher import DomesticDataFetcher
from cluefin_desk.data.listing import StockListing, load_listing
from cluefin_desk.data.screener import StockScreener

CSS_PATH = Path(__file__).parent / "styles" / "app.tcss"


class CluefinDeskApp(App):
    """Cluefin TUI Dashboard Application."""

    TITLE = "Cluefin Desk"
    SUB_TITLE = "Korean Stock Market Dashboard"
    CSS_PATH = CSS_PATH

    BINDINGS = [
        Binding("1", "switch_screen('1')", "MKT", show=True),
        Binding("2", "switch_screen('2')", "RANK", show=True),
        Binding("3", "switch_screen('3')", "THEME", show=True),
        Binding("4", "switch_screen('4')", "ETF", show=True),
        Binding("5", "switch_screen('5')", "INV", show=True),
        Binding("6", "switch_screen('6')", "WATCH", show=True),
        Binding("slash", "search_stock", "Search", show=True),
    ]

    def __init__(self):
        super().__init__()
        self.fetcher = DomesticDataFetcher()
        self.screener = StockScreener(self.fetcher)
        self._current_screen_key = "1"
        self._listing: StockListing | None = None
        self._listing_lock = threading.Lock()

    def on_mount(self) -> None:
        from cluefin_desk.screens.market_overview import MarketOverviewScreen

        self.push_screen(MarketOverviewScreen())

    def action_switch_screen(self, key: str) -> None:
        if key == self._current_screen_key:
            return

        screen = self._create_screen(key)
        if screen is None:
            return

        # Pop back to base and push new screen
        while len(self.screen_stack) > 1:
            self.pop_screen()

        self._current_screen_key = key
        self.push_screen(screen)

    def _create_screen(self, key: str):
        from cluefin_desk.screens.etf_analysis import EtfAnalysisScreen
        from cluefin_desk.screens.investor_flow import InvestorFlowScreen
        from cluefin_desk.screens.market_overview import MarketOverviewScreen
        from cluefin_desk.screens.screening import ScreeningScreen
        from cluefin_desk.screens.theme_sector import ThemeSectorScreen
        from cluefin_desk.screens.watchlist import WatchlistScreen

        screen_map = {
            "1": MarketOverviewScreen,
            "2": ScreeningScreen,
            "3": ThemeSectorScreen,
            "4": EtfAnalysisScreen,
            "5": InvestorFlowScreen,
            "6": WatchlistScreen,
        }
        cls = screen_map.get(key)
        return cls() if cls else None

    def get_listing(self) -> StockListing:
        """Stock search index, fetched once per app run. Called from worker threads."""
        with self._listing_lock:
            if self._listing is None:
                self._listing = load_listing(self.fetcher.kiwoom_client)
            return self._listing

    def action_search_stock(self) -> None:
        from cluefin_desk.screens.stock_search import StockSearchScreen

        if isinstance(self.screen, StockSearchScreen):
            return
        self.push_screen(StockSearchScreen(self.get_listing), self.open_stock_detail)

    def open_stock_detail(self, stock_code: str | None) -> None:
        """Open the detail screen on top of the current one (escape returns)."""
        if not stock_code:
            return
        from cluefin_desk.screens.stock_detail import StockDetailScreen

        self.push_screen(StockDetailScreen(stock_code=stock_code))

    @property
    def dart_client(self):
        """Lazy-init DART client (requires dart_auth_key)."""
        if not hasattr(self, "_dart_client"):
            from cluefin_openapi.dart import Client as DartClient

            if settings.dart_auth_key:
                self._dart_client = DartClient(auth_key=settings.dart_auth_key)
            else:
                self._dart_client = None
        return self._dart_client


def main():
    app = CluefinDeskApp()
    app.run()
