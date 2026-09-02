from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import DataTable, Header, Static, TabbedContent, TabPane

from cluefin_desk.widgets.market_overview import MarketOverviewBar
from cluefin_desk.widgets.nav_bar import NavBar
from cluefin_desk.widgets.nav_footer import NavFooter


class ThemeSectorScreen(Screen):
    """Screen 3: Theme & Sector analysis."""

    BINDINGS = [
        Binding("r", "refresh", "Refresh"),
        Binding("enter", "select_stock", "Detail"),
        Binding("escape", "go_back", "Back"),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self._theme_groups = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield NavBar(id="nav-bar")
        yield MarketOverviewBar(id="market-bar")
        with Vertical():
            with TabbedContent(id="theme-sector-tabs"):
                with TabPane("테마", id="tab-theme"):
                    with Horizontal(id="theme-content"):
                        yield DataTable(id="theme-group-list")
                        yield DataTable(id="theme-stocks-table")
                    yield Static("", id="theme-status")
                with TabPane("업종", id="tab-sector"):
                    with Horizontal(id="sector-content"):
                        yield DataTable(id="sector-list")
                        yield Static("Select a sector to view details", id="sector-chart-panel")
        yield NavFooter(active_screen_key="3")

    def on_mount(self) -> None:
        nav = self.query_one("#nav-bar", NavBar)
        nav.set_active("3")
        self._setup_tables()
        self.load_all_data()

    def _setup_tables(self) -> None:
        # Theme group list
        tbl = self.query_one("#theme-group-list", DataTable)
        tbl.cursor_type = "row"
        tbl.zebra_stripes = True
        for label, width in [("테마명", 18), ("등락률", 8), ("종목수", 6)]:
            tbl.add_column(label, key=label, width=width)

        # Theme stocks
        tbl = self.query_one("#theme-stocks-table", DataTable)
        tbl.cursor_type = "row"
        tbl.zebra_stripes = True
        for label, width in [
            ("종목코드", 8),
            ("종목명", 14),
            ("현재가", 10),
            ("등락률", 8),
            ("거래량", 12),
        ]:
            tbl.add_column(label, key=label, width=width)

        # Sector list
        tbl = self.query_one("#sector-list", DataTable)
        tbl.cursor_type = "row"
        tbl.zebra_stripes = True
        for label, width in [("업종명", 18), ("등락률", 8), ("상승", 5), ("하락", 5)]:
            tbl.add_column(label, key=label, width=width)

    # `r` 연타로 워커가 겹치면 같은 패널에 두 응답이 번갈아 써진다 — 최신 것만 남긴다.
    @work(thread=True, exclusive=True, group="theme-load")
    def load_all_data(self) -> None:
        self._guarded("#theme-status", "테마 목록", self._load_theme_groups)
        self._guarded("#sector-chart-panel", "업종 목록", self._load_sector_list)

    def _guarded(self, selector: str, label: str, fn, *args) -> None:
        """탭 하나가 실패해도 나머지는 계속 로드하고, 실패는 화면에 남긴다 —
        로그에만 남기면 표가 빈 채로 멈춰 있어 사용자는 원인을 알 수 없다."""
        try:
            fn(*args)
        except Exception as e:
            from loguru import logger

            logger.error(f"Failed to load {label}: {e}")
            self._set_status(selector, f"{label} 로딩 실패: {e}")

    def _set_status(self, selector: str, text: str) -> None:
        def _apply():
            self.query_one(selector, Static).update(text)

        self.app.call_from_thread(_apply)

    def _load_theme_groups(self) -> None:
        fetcher = self.app.fetcher
        items = fetcher.get_theme_group().body.thema_grp or []
        if not items:
            self._set_status("#theme-status", "테마 데이터 없음")
            return

        self._theme_groups = items

        def _update():
            tbl = self.query_one("#theme-group-list", DataTable)
            tbl.clear()
            for item in items[:50]:
                rate = float(item.flu_rt) if item.flu_rt and item.flu_rt != "-" else 0.0
                if rate > 0:
                    rate_str = f"[red]+{rate:.1f}%[/red]"
                elif rate < 0:
                    rate_str = f"[blue]{rate:.1f}%[/blue]"
                else:
                    rate_str = f"{rate:.1f}%"
                tbl.add_row(
                    item.thema_nm,
                    rate_str,
                    item.stk_num,
                    key=item.thema_grp_cd,
                )
            self.query_one("#theme-status", Static).update(f"테마 {len(items)}건 — 행을 고르면 구성종목이 뜬다")

        self.app.call_from_thread(_update)

    def _load_sector_list(self) -> None:
        fetcher = self.app.fetcher
        items = fetcher.get_all_industry_index().body.all_inds_idex or []
        if not items:
            self._set_status("#sector-chart-panel", "업종 데이터 없음")
            return

        def _update():
            tbl = self.query_one("#sector-list", DataTable)
            tbl.clear()
            for item in items[:30]:
                rate = float(item.flu_rt) if item.flu_rt and item.flu_rt != "-" else 0.0
                if rate > 0:
                    rate_str = f"[red]+{rate:.2f}%[/red]"
                elif rate < 0:
                    rate_str = f"[blue]{rate:.2f}%[/blue]"
                else:
                    rate_str = f"{rate:.2f}%"
                rising = item.rising if hasattr(item, "rising") else "-"
                fall = item.fall if hasattr(item, "fall") else "-"
                tbl.add_row(item.stk_nm, rate_str, rising, fall, key=item.stk_cd)

        self.app.call_from_thread(_update)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        table_id = event.data_table.id
        if table_id == "theme-group-list":
            theme_code = str(event.row_key.value)
            self._load_theme_stocks(theme_code)
        elif table_id == "sector-list":
            sector_code = str(event.row_key.value)
            self._load_sector_detail(sector_code)

    @work(thread=True)
    def _load_theme_stocks(self, theme_code: str) -> None:
        try:
            fetcher = self.app.fetcher
            response = fetcher.get_theme_group_stocks(theme_code)
            items = response.body.thema_comp_stk
            if not items:
                return

            def _update():
                tbl = self.query_one("#theme-stocks-table", DataTable)
                tbl.clear()
                for item in items:
                    rate = float(item.flu_rt) if item.flu_rt and item.flu_rt != "-" else 0.0
                    if rate > 0:
                        rate_str = f"[red]+{rate:.2f}%[/red]"
                    elif rate < 0:
                        rate_str = f"[blue]{rate:.2f}%[/blue]"
                    else:
                        rate_str = f"{rate:.2f}%"
                    try:
                        vol_str = f"{int(float(item.acc_trde_qty)):,}" if item.acc_trde_qty else "-"
                    except (ValueError, TypeError):
                        vol_str = "-"
                    tbl.add_row(
                        item.stk_cd,
                        item.stk_nm,
                        item.cur_prc,
                        rate_str,
                        vol_str,
                        key=item.stk_cd,
                    )

            self.app.call_from_thread(_update)
        except Exception as e:
            from loguru import logger

            logger.error(f"Failed to load theme stocks: {e}")
            self._set_status("#theme-status", f"테마 구성종목 로딩 실패: {e}")

    @work(thread=True)
    def _load_sector_detail(self, sector_code: str) -> None:
        try:
            fetcher = self.app.fetcher
            response = fetcher.get_industry_price_by_sector(inds_cd=sector_code)
            items = response.body.inds_stkpc
            if not items:
                return

            def _update():
                lines = [f"[bold]업종 구성 종목 ({sector_code})[/bold]", ""]
                for item in items[:15]:
                    rate = float(item.flu_rt) if item.flu_rt and item.flu_rt != "-" else 0.0
                    if rate > 0:
                        rate_str = f"[red]+{rate:.2f}%[/red]"
                    elif rate < 0:
                        rate_str = f"[blue]{rate:.2f}%[/blue]"
                    else:
                        rate_str = f"{rate:.2f}%"
                    lines.append(f"  {item.stk_nm:<12s} {item.cur_prc:>10s}  {rate_str}")
                panel = self.query_one("#sector-chart-panel", Static)
                panel.update("\n".join(lines))

            self.app.call_from_thread(_update)
        except Exception as e:
            from loguru import logger

            logger.error(f"Failed to load sector detail: {e}")
            self._set_status("#sector-chart-panel", f"업종 상세 로딩 실패: {e}")

    def action_refresh(self) -> None:
        self.load_all_data()

    def action_select_stock(self) -> None:
        # Try theme stocks table first
        try:
            tbl = self.query_one("#theme-stocks-table", DataTable)
            if tbl.cursor_row is not None and tbl.row_count > 0:
                row_key, _ = tbl.coordinate_to_cell_key(tbl.cursor_coordinate)
                stock_code = str(row_key.value)
                if stock_code and len(stock_code) == 6:
                    from cluefin_desk.screens.stock_detail import StockDetailScreen

                    self.app.push_screen(StockDetailScreen(stock_code=stock_code))
                    return
        except Exception:
            pass

    def action_go_back(self) -> None:
        self.app.action_switch_screen("1")

    def action_quit(self) -> None:
        self.app.exit()
