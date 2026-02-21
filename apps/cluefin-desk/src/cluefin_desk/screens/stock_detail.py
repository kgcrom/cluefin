import asyncio

from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import DataTable, Header, Static, TabbedContent, TabPane

from cluefin_desk.widgets.company_info import CompanyInfoWidget
from cluefin_desk.widgets.indicator_panel import IndicatorPanel
from cluefin_desk.widgets.nav_footer import NavFooter
from cluefin_desk.widgets.price_chart import PriceChartWidget


class StockDetailScreen(Screen):
    """Screen 6: Stock detail with 4 tabs (chart, investor, broker, supply-demand)."""

    BINDINGS = [
        Binding("escape", "go_back", "Back"),
        Binding("r", "refresh", "Refresh"),
        Binding("f", "financial", "Financial"),
    ]

    def __init__(self, stock_code: str):
        super().__init__()
        self.stock_code = stock_code

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static(f"Loading {self.stock_code}...", id="detail-title-bar")
        with TabbedContent(id="detail-tabs"):
            with TabPane("차트", id="tab-chart"):
                with Horizontal(id="detail-chart-content"):
                    with Vertical(id="detail-left"):
                        yield CompanyInfoWidget(id="company-info")
                    with Vertical(id="detail-right"):
                        yield PriceChartWidget(id="price-chart")
                        yield IndicatorPanel(id="indicator-panel")
            with TabPane("투자자", id="tab-investor"):
                yield DataTable(id="investor-detail-table")
            with TabPane("매매원", id="tab-broker"):
                yield Static("Loading broker data...", id="broker-detail-content")
            with TabPane("수급", id="tab-supply"):
                yield Static("Loading supply/demand data...", id="supply-detail-content")
        yield NavFooter(id="nav-footer")

    def on_mount(self) -> None:
        self.query_one("#nav-footer", NavFooter).active_screen_key = self.app._current_screen_key
        self._setup_investor_table()
        self.load_detail_data()

    def _setup_investor_table(self) -> None:
        tbl = self.query_one("#investor-detail-table", DataTable)
        tbl.cursor_type = "row"
        tbl.zebra_stripes = True
        for label, width in [
            ("일자", 12),
            ("현재가", 10),
            ("등락률", 8),
            ("개인", 12),
            ("외국인", 12),
            ("기관", 12),
        ]:
            tbl.add_column(label, key=label, width=width)

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

        def _update_title():
            title = self.query_one("#detail-title-bar", Static)
            if not basic_df.empty:
                row = basic_df.iloc[0]
                title.update(
                    f"[bold]{row.get('stock_name', 'N/A')}[/bold] ({self.stock_code})  "
                    f"{row.get('market_name', '')}  [F\u00b7재무] [Esc\u00b7뒤로]"
                )

        self.app.call_from_thread(_update_title)

        company_info = self.query_one("#company-info", CompanyInfoWidget)
        self.app.call_from_thread(company_info.update_info, basic_df)

        chart = self.query_one("#price-chart", PriceChartWidget)
        self.app.call_from_thread(chart.update_chart, stock_df, stock_name)

        indicator = self.query_one("#indicator-panel", IndicatorPanel)
        self.app.call_from_thread(indicator.update_indicators, stock_df)

        # Load investor data
        self._load_investor_data()
        self._load_broker_data()
        self._load_supply_data()

    def _load_investor_data(self) -> None:
        try:
            fetcher = self.app.fetcher
            response = fetcher.get_institutional_investor_by_stock(self.stock_code)
            items = response.body.stk_invsr_orgn
            if not items:
                return

            def _update():
                tbl = self.query_one("#investor-detail-table", DataTable)
                tbl.clear()
                for item in items[:30]:
                    rate = float(item.flu_rt) if item.flu_rt and item.flu_rt != "-" else 0.0
                    if rate > 0:
                        rate_str = f"[red]+{rate:.2f}%[/red]"
                    elif rate < 0:
                        rate_str = f"[blue]{rate:.2f}%[/blue]"
                    else:
                        rate_str = f"{rate:.2f}%"
                    tbl.add_row(
                        item.dt,
                        item.cur_prc,
                        rate_str,
                        item.ind_invsr,
                        item.frgnr_invsr,
                        item.orgn,
                        key=item.dt,
                    )

            self.app.call_from_thread(_update)
        except Exception as e:
            from loguru import logger

            logger.error(f"Failed to load investor data: {e}")

    def _load_broker_data(self) -> None:
        try:
            fetcher = self.app.fetcher
            response = fetcher.get_stock_trading_member(self.stock_code)
            body = response.body

            def _update():
                lines = [
                    f"[bold]매매원 현황 — {body.stk_nm} ({body.stk_cd})[/bold]",
                    f"현재가: {body.cur_prc}  등락률: {body.flu_rt}%",
                    "",
                    "[bold]매수 상위[/bold]",
                ]
                for i in range(1, 6):
                    nm = getattr(body, f"buy_trde_ori_nm_{i}", "-")
                    qty = getattr(body, f"buy_trde_qty_{i}", "-")
                    lines.append(f"  {i}. {nm:<16s}  {qty:>12s}")
                lines.append("")
                lines.append("[bold]매도 상위[/bold]")
                for i in range(1, 6):
                    nm = getattr(body, f"sel_trde_ori_nm_{i}", "-")
                    qty = getattr(body, f"sel_trde_qty_{i}", "-")
                    lines.append(f"  {i}. {nm:<16s}  {qty:>12s}")

                panel = self.query_one("#broker-detail-content", Static)
                panel.update("\n".join(lines))

            self.app.call_from_thread(_update)
        except Exception as e:
            from loguru import logger

            logger.error(f"Failed to load broker data: {e}")

    def _load_supply_data(self) -> None:
        try:
            fetcher = self.app.fetcher
            response = fetcher.get_margin_trading_trend(self.stock_code)
            items = response.body.crd_trde_trend
            if not items:
                return

            def _update():
                lines = [
                    "[bold]신용거래 추이[/bold]",
                    "",
                    f"{'일자':<12s} {'현재가':>10s} {'신규':>8s} {'상환':>8s} {'잔고':>10s} {'잔고율':>6s}",
                    "-" * 60,
                ]
                for item in items[:15]:
                    lines.append(
                        f"{item.dt:<12s} {item.cur_prc:>10s} {item.new:>8s} "
                        f"{item.rpya:>8s} {item.remn:>10s} {item.remn_rt:>6s}"
                    )

                panel = self.query_one("#supply-detail-content", Static)
                panel.update("\n".join(lines))

            self.app.call_from_thread(_update)
        except Exception as e:
            from loguru import logger

            logger.error(f"Failed to load supply data: {e}")

    def action_go_back(self) -> None:
        self.app.pop_screen()

    def action_refresh(self) -> None:
        self.load_detail_data()

    def action_financial(self) -> None:
        from cluefin_desk.screens.financial_analysis import FinancialAnalysisScreen

        self.app.push_screen(FinancialAnalysisScreen(stock_code=self.stock_code))
