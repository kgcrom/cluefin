from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import DataTable, Header, Static

from cluefin_desk.widgets.market_overview import MarketOverviewBar
from cluefin_desk.widgets.nav_bar import NavBar
from cluefin_desk.widgets.nav_footer import NavFooter


class EtfAnalysisScreen(Screen):
    """Screen 4: ETF Analysis."""

    BINDINGS = [
        Binding("r", "refresh", "Refresh"),
        Binding("enter", "select_etf", "Detail"),
        Binding("n", "nav_detail", "NAV(KIS)"),
        Binding("escape", "go_back", "Back"),
        Binding("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield NavBar(id="nav-bar")
        yield MarketOverviewBar(id="market-bar")
        with Vertical(id="etf-content"):
            yield DataTable(id="etf-price-table")
            yield Static("", id="etf-kis-panel")
        yield NavFooter(active_screen_key="4")

    def on_mount(self) -> None:
        nav = self.query_one("#nav-bar", NavBar)
        nav.set_active("4")
        self._setup_tables()
        self.load_all_data()

    def _setup_tables(self) -> None:
        tbl = self.query_one("#etf-price-table", DataTable)
        tbl.cursor_type = "row"
        tbl.zebra_stripes = True
        for label, width in [
            ("#", 4),
            ("종목코드", 8),
            ("ETF명", 24),
            ("종가", 10),
            ("등락률", 8),
            ("NAV", 10),
            ("괴리율", 8),
            ("거래량", 12),
        ]:
            tbl.add_column(label, key=label, width=width)

    # `r` 연타로 워커가 겹치면 같은 패널에 두 응답이 번갈아 써진다 — 최신 것만 남긴다.
    @work(thread=True, exclusive=True, group="etf-load")
    def load_all_data(self) -> None:
        self._load_etf_prices()

    def _load_etf_prices(self) -> None:
        try:
            fetcher = self.app.fetcher
            response = fetcher.get_etf_full_price()
            items = response.body.etfall_mrpr
            if not items:
                return

            def _update():
                tbl = self.query_one("#etf-price-table", DataTable)
                tbl.clear()
                for idx, item in enumerate(items[:50]):
                    rate = float(item.pre_rt) if item.pre_rt and item.pre_rt != "-" else 0.0
                    if rate > 0:
                        rate_str = f"[red]+{rate:.2f}%[/red]"
                    elif rate < 0:
                        rate_str = f"[blue]{rate:.2f}%[/blue]"
                    else:
                        rate_str = f"{rate:.2f}%"

                    nav_val = item.nav if hasattr(item, "nav") and item.nav else "-"

                    # Disparity rate
                    disp_str = "-"
                    if hasattr(item, "trace_eor_rt") and item.trace_eor_rt:
                        try:
                            disp = float(item.trace_eor_rt)
                            disp_str = f"{disp:.2f}%"
                        except (ValueError, TypeError):
                            disp_str = item.trace_eor_rt

                    try:
                        vol_str = f"{int(float(item.trde_qty)):,}" if item.trde_qty else "-"
                    except (ValueError, TypeError):
                        vol_str = "-"

                    tbl.add_row(
                        str(idx + 1),
                        item.stk_cd,
                        item.stk_nm,
                        item.close_pric,
                        rate_str,
                        nav_val,
                        disp_str,
                        vol_str,
                        key=item.stk_cd,
                    )

            self.app.call_from_thread(_update)
        except Exception as e:
            from loguru import logger

            logger.error(f"Failed to load ETF prices: {e}")

    def action_refresh(self) -> None:
        self.load_all_data()

    def action_select_etf(self) -> None:
        tbl = self.query_one("#etf-price-table", DataTable)
        if tbl.cursor_row is not None and tbl.row_count > 0:
            row_key, _ = tbl.coordinate_to_cell_key(tbl.cursor_coordinate)
            stock_code = str(row_key.value)
            if stock_code:
                from cluefin_desk.screens.stock_detail import StockDetailScreen

                self.app.push_screen(StockDetailScreen(stock_code=stock_code))

    def action_nav_detail(self) -> None:
        tbl = self.query_one("#etf-price-table", DataTable)
        if tbl.cursor_row is not None and tbl.row_count > 0:
            row_key, _ = tbl.coordinate_to_cell_key(tbl.cursor_coordinate)
            stock_code = str(row_key.value)
            if stock_code:
                self._load_kis_nav_detail(stock_code)

    @work(thread=True)
    def _load_kis_nav_detail(self, stock_code: str) -> None:
        """선택 ETF 의 KIS NAV 괴리 추이 + 구성종목 상위. KIS 키가 없으면 안내만."""
        fetcher = self.app.fetcher
        if not fetcher.has_kis:

            def _show_missing():
                self.query_one("#etf-kis-panel", Static).update(
                    "KIS API keys not configured — NAV 상세는 KIS_APP_KEY 설정 후 사용 가능합니다."
                )

            self.app.call_from_thread(_show_missing)
            return

        try:
            nav_rows = fetcher.get_etf_nav_daily_trend(stock_code, days=30)
            components = fetcher.get_etf_component_prices(stock_code)

            def _update():
                lines = [f"[bold]{stock_code} — NAV 괴리 추이 (KIS)[/bold]"]
                if nav_rows:
                    lines.append(f"{'일자':<10s} {'종가':>10s} {'NAV':>12s} {'괴리율':>8s}")
                    for item in nav_rows[:10]:
                        lines.append(
                            f"{item.stck_bsop_date:<10s} {item.stck_clpr:>10s} {item.nav:>12s} {item.dprt:>8s}%"
                        )
                else:
                    lines.append("NAV 데이터 없음")

                if components:
                    lines += ["", "[bold]구성종목 상위 (비중순, KIS)[/bold]"]
                    for item in components[:10]:
                        lines.append(
                            f"  {item.hts_kor_isnm:<16s} {item.stck_prpr:>10s} "
                            f"({item.prdy_ctrt}%)  비중 {item.etf_cnfg_issu_rlim}%"
                        )

                self.query_one("#etf-kis-panel", Static).update("\n".join(lines))

            self.app.call_from_thread(_update)
        except Exception as e:
            from loguru import logger

            logger.error(f"Failed to load KIS NAV detail: {e}")

    def action_go_back(self) -> None:
        self.app.action_switch_screen("1")

    def action_quit(self) -> None:
        self.app.exit()
