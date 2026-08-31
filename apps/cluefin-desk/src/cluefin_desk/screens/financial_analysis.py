from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import DataTable, Header, Static, TabbedContent, TabPane

from cluefin_desk.widgets.nav_footer import NavFooter


class FinancialAnalysisScreen(Screen):
    """Screen 7: Financial Analysis via DART API."""

    BINDINGS = [
        Binding("escape", "go_back", "Back"),
        Binding("r", "refresh", "Refresh"),
    ]

    def __init__(self, stock_code: str):
        super().__init__()
        self.stock_code = stock_code

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static(f"{self.stock_code} — 재무 분석  [Esc·뒤로]", id="financial-title-bar")
        with TabbedContent(id="financial-tabs"):
            with TabPane("KIS 재무", id="tab-kis-financial"):
                yield Static("Loading KIS financials...", id="kis-financial-content")
            with TabPane("재무제표", id="tab-statement"):
                yield Static("Loading financial statements...", id="financial-statement-content")
            with TabPane("공시목록", id="tab-disclosure"):
                yield DataTable(id="disclosure-list-content")
            with TabPane("주요주주", id="tab-shareholder"):
                yield Static("Loading major shareholder data...", id="major-shareholder-content")
            with TabPane("주식변동", id="tab-share-change"):
                yield Static("Loading share change data...", id="share-change-content")
        yield NavFooter(id="nav-footer")

    def on_mount(self) -> None:
        self.query_one("#nav-footer", NavFooter).active_screen_key = self.app._current_screen_key
        self._setup_tables()
        self.load_all_data()

    def _setup_tables(self) -> None:
        tbl = self.query_one("#disclosure-list-content", DataTable)
        tbl.cursor_type = "row"
        tbl.zebra_stripes = True
        for label, width in [
            ("접수일", 12),
            ("공시유형", 16),
            ("보고서명", 40),
        ]:
            tbl.add_column(label, key=label, width=width)

    @work(thread=True)
    def load_all_data(self) -> None:
        self._load_kis_financials()
        self._load_disclosure_list()
        self._load_major_shareholders()

    def _load_kis_financials(self) -> None:
        """KIS 재무비율·손익계산서 시계열. 진행연도 누적(YTD) 행이 연간 행과 섞여
        내려오므로 기간을 그대로 보여주고 라벨로만 구분한다."""
        fetcher = self.app.fetcher
        if not fetcher.has_kis:

            def _show_missing_kis_key():
                panel = self.query_one("#kis-financial-content", Static)
                panel.update(
                    "KIS API keys not configured.\nSet KIS_APP_KEY / KIS_SECRET_KEY in .env to use KIS financials."
                )

            self.app.call_from_thread(_show_missing_kis_key)
            return

        try:
            ratios = fetcher.get_financial_ratio_series(self.stock_code)
            statements = fetcher.get_income_statement_series(self.stock_code)

            def _update():
                lines = []
                if statements:
                    lines += [
                        "[bold]손익계산서 (KIS, 년 시리즈 — 최신 행은 진행연도 누적일 수 있음)[/bold]",
                        "",
                        f"{'결산':>8s} {'매출액':>14s} {'영업이익':>14s} {'당기순이익':>14s}",
                        "-" * 56,
                    ]
                    for item in statements[:8]:
                        lines.append(
                            f"{item.stac_yymm:>8s} {item.sale_account:>14s} {item.bsop_prti:>14s} {item.thtr_ntin:>14s}"
                        )
                if ratios:
                    lines += [
                        "",
                        "[bold]재무비율 (KIS)[/bold]",
                        "",
                        f"{'결산':>8s} {'ROE':>8s} {'부채비율':>10s} {'유보율':>12s} {'매출성장':>10s}",
                        "-" * 56,
                    ]
                    for item in ratios[:8]:
                        lines.append(
                            f"{item.stac_yymm:>8s} {item.roe_val:>8s} {item.lblt_rate:>10s} "
                            f"{item.rsrv_rate:>12s} {item.grs:>10s}"
                        )
                if not lines:
                    lines = ["No KIS financial data available (ETF/ETN and some names have none)."]

                panel = self.query_one("#kis-financial-content", Static)
                panel.update("\n".join(lines))

            self.app.call_from_thread(_update)
        except Exception as e:
            from loguru import logger

            logger.error(f"Failed to load KIS financials: {e}")

    def _load_disclosure_list(self) -> None:
        dart_client = self.app.dart_client
        if dart_client is None:

            def _clear_disclosure_table():
                tbl = self.query_one("#disclosure-list-content", DataTable)
                tbl.clear()

            self.app.call_from_thread(_clear_disclosure_table)

            def _show_missing_dart_key():
                panel = self.query_one("#financial-statement-content", Static)
                panel.update("DART API key not configured.\nSet DART_AUTH_KEY in .env to use financial analysis.")

            self.app.call_from_thread(_show_missing_dart_key)
            return

        try:
            # Look up corp_code from stock_code
            corp_code = self._find_corp_code(dart_client)
            if not corp_code:
                return

            response = dart_client.public_disclosure.public_disclosure_search(
                corp_code=corp_code,
                page_count=20,
            )
            items = response.body.result.list
            if not items:
                return

            def _update_disclosure_table():
                tbl = self.query_one("#disclosure-list-content", DataTable)
                tbl.clear()
                for item in items:
                    tbl.add_row(
                        item.rcept_dt,
                        item.corp_cls or "-",
                        item.report_nm,
                        key=item.rcept_no,
                    )

            self.app.call_from_thread(_update_disclosure_table)

            # Update title with company name
            if items:

                def _update_financial_title():
                    title = self.query_one("#financial-title-bar", Static)
                    title.update(f"[bold]{items[0].corp_name}[/bold] ({self.stock_code}) — 재무 분석  [Esc·뒤로]")

                self.app.call_from_thread(_update_financial_title)

        except Exception as e:
            from loguru import logger

            logger.error(f"Failed to load disclosures: {e}")

    def _load_major_shareholders(self) -> None:
        dart_client = self.app.dart_client
        if dart_client is None:
            return

        try:
            corp_code = self._find_corp_code(dart_client)
            if not corp_code:
                return

            response = dart_client.share_disclosure.large_holding_report(corp_code=corp_code)
            items = response.body.result.list
            if not items:

                def _show_empty_major_shareholders():
                    panel = self.query_one("#major-shareholder-content", Static)
                    panel.update("No major shareholder data available")

                self.app.call_from_thread(_show_empty_major_shareholders)
                return

            def _update_major_shareholders():
                lines = ["[bold]주식등의 대량보유 상황보고[/bold]", ""]
                for item in items[:20]:
                    rcept_dt = getattr(item, "rcept_dt", "-")
                    report_nm = getattr(item, "report_nm", "-")
                    corp_name = getattr(item, "corp_name", "-")
                    lines.append(f"  {rcept_dt}  {corp_name}  {report_nm}")
                panel = self.query_one("#major-shareholder-content", Static)
                panel.update("\n".join(lines))

            self.app.call_from_thread(_update_major_shareholders)
        except Exception as e:
            from loguru import logger

            logger.error(f"Failed to load major shareholders: {e}")
            err_msg = str(e)

            def _update_err():
                panel = self.query_one("#major-shareholder-content", Static)
                panel.update(f"Failed to load: {err_msg}")

            self.app.call_from_thread(_update_err)

    def _find_corp_code(self, dart_client) -> str | None:
        """Find DART corp_code from stock_code."""
        try:
            corp_list = dart_client.public_disclosure.corp_code()
            for item in corp_list.body.result:
                if item.stock_code == self.stock_code:
                    return item.corp_code
        except Exception as e:
            from loguru import logger

            logger.error(f"Failed to find corp_code for {self.stock_code}: {e}")
        return None

    def action_go_back(self) -> None:
        self.app.pop_screen()

    def action_refresh(self) -> None:
        self.load_all_data()
