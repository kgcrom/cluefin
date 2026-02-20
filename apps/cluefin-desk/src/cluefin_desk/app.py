from pathlib import Path

from textual.app import App

from cluefin_desk.data.fetcher import DomesticDataFetcher
from cluefin_desk.data.screener import StockScreener
from cluefin_desk.screens.screening import ScreeningScreen

CSS_PATH = Path(__file__).parent / "styles" / "app.tcss"


class CluefinDeskApp(App):
    """Cluefin TUI Dashboard Application."""

    TITLE = "Cluefin Desk"
    SUB_TITLE = "Korean Stock Market Dashboard"
    CSS_PATH = CSS_PATH

    def __init__(self):
        super().__init__()
        self.fetcher = DomesticDataFetcher()
        self.screener = StockScreener(self.fetcher)

    def on_mount(self) -> None:
        self.push_screen(ScreeningScreen())


def main():
    app = CluefinDeskApp()
    app.run()
