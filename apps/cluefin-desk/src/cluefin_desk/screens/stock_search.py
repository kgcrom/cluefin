"""`/` 종목 검색 모달 — 코드나 이름으로 종목을 골라 코드를 돌려준다.

순위 표에 없는 종목도 상세 화면으로 열 수 있게 하는 입구다. 색인(키움 종목 목록)은
앱이 한 번만 받아 두고, 이 화면은 워커에서 그 로더를 부른다. 6자리 코드는 색인이
아직 없거나 받지 못했어도 그대로 연다.
"""

import logging
from collections.abc import Callable

from rich.markup import escape
from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Input, OptionList, Static
from textual.widgets.option_list import Option

from cluefin_desk.data.listing import ListedStock, StockListing, is_stock_code
from cluefin_desk.formatting import pad
from cluefin_desk.screens._guard import screen_gone, set_text

logger = logging.getLogger(__name__)

LOADING = "종목 목록 불러오는 중…"


class StockSearchScreen(ModalScreen[str | None]):
    """Dismisses with the chosen stock code, or None on escape."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
        Binding("down", "focus_results", "Results", show=False),
    ]

    def __init__(self, load_listing: Callable[[], StockListing]):
        super().__init__()
        self._load_listing = load_listing
        self._listing: StockListing | None = None

    def compose(self) -> ComposeResult:
        with Vertical(id="search-dialog"):
            yield Static("종목 검색 — 코드 또는 이름, Enter 로 열기 · Esc 닫기", id="search-title")
            yield Input(placeholder="005930 / 삼성전자", id="search-input")
            yield OptionList(id="search-results")
            yield Static(LOADING, id="search-status")

    def on_mount(self) -> None:
        self.query_one("#search-input", Input).focus()
        self.load_index()

    @work(thread=True, exclusive=True, group="stock-search-index")
    def load_index(self) -> None:
        try:
            listing = self._load_listing()
            self.app.call_from_thread(self._index_ready, listing)
        except Exception as e:
            if screen_gone(self, e):
                return

            logger.error(f"Failed to load stock listing: {e}")
            set_text(self, "#search-status", f"종목 목록 로딩 실패: {escape(str(e))} — 6자리 코드는 그대로 열 수 있다")

    def _index_ready(self, listing: StockListing) -> None:
        self._listing = listing
        self._show_candidates(self.query_one("#search-input", Input).value)

    def on_input_changed(self, event: Input.Changed) -> None:
        self._show_candidates(event.value)

    def _show_candidates(self, text: str) -> None:
        if self._listing is None:
            return
        candidates = self._listing.suggest(text)
        results = self.query_one("#search-results", OptionList)
        results.clear_options()
        results.add_options([Option(self._format_candidate(stock), id=stock.code) for stock in candidates])
        status = self.query_one("#search-status", Static)
        if not text.strip():
            status.update(f"{len(self._listing):,}종목")
        elif candidates:
            status.update(f"후보 {len(candidates)}개 — ↓ 로 고르기")
        else:
            status.update("맞는 종목 없음")

    @staticmethod
    def _format_candidate(stock: ListedStock) -> str:
        return f"{pad(stock.code, 7)} {pad(escape(stock.name), 30)} {stock.market} {stock.kind}"

    def on_input_submitted(self, event: Input.Submitted) -> None:
        text = event.value.strip()
        if not text:
            return
        code = text.upper()
        if is_stock_code(code) and (self._listing is None or self._listing.get(code) is not None):
            self.dismiss(code)
            return
        if self._listing is None:
            return
        stock = self._listing.resolve(text)
        if stock is not None:
            self.dismiss(stock.code)
        elif self.query_one("#search-results", OptionList).option_count:
            self.action_focus_results()
        else:
            self.query_one("#search-status", Static).update("맞는 종목 없음")

    def action_focus_results(self) -> None:
        results = self.query_one("#search-results", OptionList)
        if results.option_count:
            results.focus()
            if results.highlighted is None:
                results.highlighted = 0

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.dismiss(event.option.id)

    def action_cancel(self) -> None:
        self.dismiss(None)
