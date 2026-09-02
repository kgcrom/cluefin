from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import DataTable, Header, Static

from cluefin_desk.formatting import pad
from cluefin_desk.screens._guard import screen_gone
from cluefin_desk.widgets.market_overview import MarketOverviewBar
from cluefin_desk.widgets.nav_bar import NavBar
from cluefin_desk.widgets.nav_footer import NavFooter

NAV_HINT = "ETF 행을 고르고 N 을 누르면 NAV 괴리 추이·구성종목 (KIS) 이 여기에 뜬다"


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
            # 표만 있으면 빈 표가 "데이터 없음" 인지 "조회 실패" 인지 알 수 없다
            yield Static("Loading...", id="etf-status")
            yield Static(NAV_HINT, id="etf-kis-panel")
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
        self._guarded("#etf-status", "ETF 시세", self._load_etf_prices)

    def _guarded(self, selector: str, label: str, fn, *args) -> None:
        """실패를 로그에만 남기면 표가 빈 채로 멈춰 있어 사용자는 원인을 알 수 없다."""
        try:
            fn(*args)
        except Exception as e:
            if screen_gone(self, e):
                return
            from loguru import logger

            logger.error(f"Failed to load {label}: {e}")
            self._set_text(selector, f"{label} 로딩 실패: {e}")

    def _set_text(self, selector: str, text: str) -> None:
        def _apply():
            self.query_one(selector, Static).update(text)

        self.app.call_from_thread(_apply)

    def _load_etf_prices(self) -> None:
        fetcher = self.app.fetcher
        items = fetcher.get_etf_full_price().body.etfall_mrpr or []

        def _update():
            tbl = self.query_one("#etf-price-table", DataTable)
            tbl.clear()
            for idx, item in enumerate(items[:50]):
                tbl.add_row(*self._format_etf_row(idx + 1, item), key=item.stk_cd)
            self.query_one("#etf-status", Static).update(
                f"ETF {min(len(items), 50)}건 (전체 {len(items)})" if items else "ETF 데이터 없음"
            )

        self.app.call_from_thread(_update)

    @staticmethod
    def _format_etf_row(rank: int, item) -> tuple[str, str, str, str, str, str, str, str]:
        """ETF 전체시세 한 행 → 표 셀 문자열. 키움은 없는 값을 "" 또는 "-" 로 준다."""
        try:
            rate = float(item.pre_rt) if item.pre_rt and item.pre_rt != "-" else 0.0
        except (ValueError, TypeError):
            rate = 0.0
        if rate > 0:
            rate_str = f"[red]+{rate:.2f}%[/red]"
        elif rate < 0:
            rate_str = f"[blue]{rate:.2f}%[/blue]"
        else:
            rate_str = f"{rate:.2f}%"

        nav_val = getattr(item, "nav", None) or "-"

        disp_str = "-"
        trace = getattr(item, "trace_eor_rt", None)
        if trace:
            try:
                disp_str = f"{float(trace):.2f}%"
            except (ValueError, TypeError):
                disp_str = str(trace)

        try:
            vol_str = f"{int(float(item.trde_qty)):,}" if item.trde_qty else "-"
        except (ValueError, TypeError):
            vol_str = "-"

        return (str(rank), item.stk_cd, item.stk_nm, item.close_pric, rate_str, nav_val, disp_str, vol_str)

    def action_refresh(self) -> None:
        self.load_all_data()

    def _selected_code(self) -> str | None:
        tbl = self.query_one("#etf-price-table", DataTable)
        if tbl.cursor_row is not None and tbl.row_count > 0:
            row_key, _ = tbl.coordinate_to_cell_key(tbl.cursor_coordinate)
            return str(row_key.value) or None
        return None

    def action_select_etf(self) -> None:
        stock_code = self._selected_code()
        if stock_code:
            from cluefin_desk.screens.stock_detail import StockDetailScreen

            self.app.push_screen(StockDetailScreen(stock_code=stock_code))

    def action_nav_detail(self) -> None:
        stock_code = self._selected_code()
        if stock_code:
            self.query_one("#etf-kis-panel", Static).update(f"{stock_code} — NAV 상세 조회 중 (KIS)...")
            self._load_kis_nav_detail(stock_code)

    # 다른 ETF 로 N 을 연타하면 앞선 조회가 늦게 도착해 패널을 덮어쓴다 — 최신 것만 남긴다.
    @work(thread=True, exclusive=True, group="etf-nav-detail")
    def _load_kis_nav_detail(self, stock_code: str) -> None:
        """선택 ETF 의 KIS NAV 괴리 추이 + 구성종목 상위. KIS 키가 없으면 안내만."""
        fetcher = self.app.fetcher
        if not fetcher.has_kis:
            self._set_text(
                "#etf-kis-panel", "KIS API keys not configured — NAV 상세는 KIS_APP_KEY 설정 후 사용 가능합니다."
            )
            return

        self._guarded("#etf-kis-panel", f"{stock_code} NAV 상세", self._fetch_and_show_nav, stock_code)

    def _fetch_and_show_nav(self, stock_code: str) -> None:
        fetcher = self.app.fetcher
        nav_rows = fetcher.get_etf_nav_daily_trend(stock_code, days=30)
        components = fetcher.get_etf_component_prices(stock_code)
        self._set_text("#etf-kis-panel", "\n".join(self._format_nav_lines(stock_code, nav_rows, components)))

    @staticmethod
    def _format_nav_lines(stock_code: str, nav_rows, components) -> list[str]:
        nav_rows, components = list(nav_rows or []), list(components or [])
        lines = [f"[bold]{stock_code} — NAV 괴리 추이 (KIS)[/bold]"]
        if nav_rows:
            lines.append(
                f"{pad('일자', 10)} {pad('종가', 10, 'right')} {pad('NAV', 12, 'right')} {pad('괴리율', 8, 'right')}"
            )
            for item in nav_rows[:10]:
                lines.append(
                    f"{pad(item.stck_bsop_date, 10)} {pad(item.stck_clpr, 10, 'right')} "
                    f"{pad(item.nav, 12, 'right')} {pad((item.dprt or '-') + '%', 8, 'right')}"
                )
        else:
            lines.append("NAV 데이터 없음")

        if components:
            lines += ["", "[bold]구성종목 상위 (비중순, KIS)[/bold]"]
            for item in components[:10]:
                lines.append(
                    f"  {pad(item.hts_kor_isnm, 16)} {pad(item.stck_prpr, 10, 'right')} "
                    f"({item.prdy_ctrt}%)  비중 {item.etf_cnfg_issu_rlim}%"
                )
        else:
            lines += ["", "구성종목 데이터 없음"]
        return lines

    def action_go_back(self) -> None:
        self.app.action_switch_screen("1")

    def action_quit(self) -> None:
        self.app.exit()
