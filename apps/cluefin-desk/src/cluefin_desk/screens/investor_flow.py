import asyncio

from loguru import logger
from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import DataTable, Header, Static

from cluefin_desk.widgets.market_overview import MarketOverviewBar
from cluefin_desk.widgets.nav_bar import NavBar
from cluefin_desk.widgets.nav_footer import NavFooter


class InvestorFlowScreen(Screen):
    """Screen 5: Investor Flow - foreign/institutional net buy + program trading."""

    BINDINGS = [
        Binding("r", "refresh", "Refresh"),
        Binding("enter", "select_stock", "Detail"),
        Binding("escape", "go_back", "Back"),
        Binding("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield NavBar(id="nav-bar")
        yield MarketOverviewBar(id="market-bar")
        with Vertical(id="investor-content"):
            with Horizontal(id="investor-top-container"):
                yield Static("Loading...", id="foreign-net-buy-panel")
                yield Static("Loading...", id="institutional-net-buy-panel")
            yield DataTable(id="program-trading-table")
            yield DataTable(id="sector-investor-table")
        yield NavFooter(active_screen_key="5")

    def on_mount(self) -> None:
        nav = self.query_one("#nav-bar", NavBar)
        nav.set_active("5")
        self._setup_tables()
        self.load_all_data()

    def _setup_tables(self) -> None:
        # Program trading
        tbl = self.query_one("#program-trading-table", DataTable)
        tbl.cursor_type = "row"
        tbl.zebra_stripes = True
        for label, width in [
            ("#", 4),
            ("종목코드", 8),
            ("종목명", 14),
            ("현재가", 10),
            ("프로그램매수", 12),
            ("프로그램매도", 12),
            ("순매수", 12),
        ]:
            tbl.add_column(label, key=label, width=width)

        # Sector investor flow
        tbl = self.query_one("#sector-investor-table", DataTable)
        tbl.cursor_type = "row"
        tbl.zebra_stripes = True
        for label, width in [
            ("업종명", 14),
            ("현재가", 10),
            ("등락률", 8),
            ("외국인", 12),
            ("개인", 12),
        ]:
            tbl.add_column(label, key=label, width=width)

    @work(thread=True)
    def load_all_data(self) -> None:
        self._load_market_overview()
        self._load_foreign_net_buy()
        self._load_institutional_net_buy()
        self._load_program_trading()
        self._load_sector_investor()

    def _load_market_overview(self) -> None:
        fetcher = self.app.fetcher
        loop = asyncio.new_event_loop()
        try:
            kospi = loop.run_until_complete(fetcher.get_kospi_index_series())
            kosdaq = loop.run_until_complete(fetcher.get_kosdaq_index_series())
        finally:
            loop.close()

        bar = self.query_one("#market-bar", MarketOverviewBar)
        self.app.call_from_thread(bar.update_indices, kospi, kosdaq)

    def _load_foreign_net_buy(self) -> None:
        try:
            fetcher = self.app.fetcher
            response = fetcher.get_top_foreigner_period_trading(trde_tp="1")
            logger.debug(f"[INV] foreign API response status: {response.headers}")
            items = response.body.for_dt_trde_upper
            logger.debug(f"[INV] foreign items count: {len(items)}")
            if not items:

                def _update_empty():
                    panel = self.query_one("#foreign-net-buy-panel", Static)
                    panel.update("[bold]외국인 순매수 상위[/bold]\n\n  데이터 없음")

                self.app.call_from_thread(_update_empty)
                return

            def _update():
                lines = ["[bold]외국인 순매수 상위[/bold]", ""]
                for item in items[:8]:
                    lines.append(f"  {item.stk_nm:<12s} {item.cur_prc:>10s}  순매수: {item.netprps_qty:>10s}")
                panel = self.query_one("#foreign-net-buy-panel", Static)
                panel.update("\n".join(lines))

            self.app.call_from_thread(_update)
        except Exception as e:
            logger.error(f"Failed to load foreign net buy: {e}")
            err_msg = str(e)

            def _update_error():
                panel = self.query_one("#foreign-net-buy-panel", Static)
                panel.update(f"[bold]외국인 순매수 상위[/bold]\n\n  로드 실패: {err_msg}")

            self.app.call_from_thread(_update_error)

    def _load_institutional_net_buy(self) -> None:
        try:
            fetcher = self.app.fetcher
            response = fetcher.get_top_intraday_trading_by_investor(trde_tp="1", orgn_tp="1000")
            logger.debug(f"[INV] institutional API response status: {response.headers}")
            items = response.body.opmr_invsr_trde_upper
            logger.debug(f"[INV] institutional items count: {len(items)}")
            if not items:

                def _update_empty():
                    panel = self.query_one("#institutional-net-buy-panel", Static)
                    panel.update("[bold]기관 순매수 상위[/bold]\n\n  데이터 없음")

                self.app.call_from_thread(_update_empty)
                return

            def _update():
                lines = ["[bold]기관 순매수 상위[/bold]", ""]
                for item in items[:8]:
                    lines.append(f"  {item.stk_nm:<12s}  매수: {item.buy_qty:>10s}  매도: {item.sel_qty:>10s}")
                panel = self.query_one("#institutional-net-buy-panel", Static)
                panel.update("\n".join(lines))

            self.app.call_from_thread(_update)
        except Exception as e:
            logger.error(f"Failed to load institutional net buy: {e}")
            err_msg = str(e)

            def _update_error():
                panel = self.query_one("#institutional-net-buy-panel", Static)
                panel.update(f"[bold]기관 순매수 상위[/bold]\n\n  로드 실패: {err_msg}")

            self.app.call_from_thread(_update_error)

    def _load_program_trading(self) -> None:
        try:
            fetcher = self.app.fetcher
            response = fetcher.get_top_50_program_net_buy()
            logger.debug(f"[INV] program trading API response status: {response.headers}")
            items = response.body.prm_netprps_upper_50
            logger.debug(f"[INV] program trading items count: {len(items)}")
            if not items:
                return

            def _update():
                tbl = self.query_one("#program-trading-table", DataTable)
                tbl.clear()
                for idx, item in enumerate(items[:20]):
                    tbl.add_row(
                        str(idx + 1),
                        item.stk_cd,
                        item.stk_nm,
                        item.cur_prc,
                        item.prm_buy_amt,
                        item.prm_sell_amt,
                        item.prm_netprps_amt,
                        key=item.stk_cd,
                    )

            self.app.call_from_thread(_update)
        except Exception as e:
            logger.error(f"Failed to load program trading: {e}")

    def _load_sector_investor(self) -> None:
        try:
            fetcher = self.app.fetcher
            response = fetcher.get_industry_investor_net_buy()
            logger.debug(f"[INV] sector investor API response status: {response.headers}")
            items = response.body.inds_netprps
            logger.debug(f"[INV] sector investor items count: {len(items)}")
            if not items:
                return

            def _update():
                tbl = self.query_one("#sector-investor-table", DataTable)
                tbl.clear()
                for item in items[:20]:
                    rate = float(item.flu_rt) if item.flu_rt and item.flu_rt != "-" else 0.0
                    if rate > 0:
                        rate_str = f"[red]+{rate:.2f}%[/red]"
                    elif rate < 0:
                        rate_str = f"[blue]{rate:.2f}%[/blue]"
                    else:
                        rate_str = f"{rate:.2f}%"
                    tbl.add_row(
                        item.inds_nm,
                        item.cur_prc,
                        rate_str,
                        item.frgnr_netprps,
                        item.ind_netprps,
                        key=item.inds_cd,
                    )

            self.app.call_from_thread(_update)
        except Exception as e:
            logger.error(f"Failed to load sector investor: {e}")

    def action_refresh(self) -> None:
        self.load_all_data()

    def action_select_stock(self) -> None:
        tbl = self.query_one("#program-trading-table", DataTable)
        if tbl.cursor_row is not None and tbl.row_count > 0:
            row_key, _ = tbl.coordinate_to_cell_key(tbl.cursor_coordinate)
            stock_code = str(row_key.value)
            if stock_code:
                from cluefin_desk.screens.stock_detail import StockDetailScreen

                self.app.push_screen(StockDetailScreen(stock_code=stock_code))

    def action_go_back(self) -> None:
        self.app.action_switch_screen("1")

    def action_quit(self) -> None:
        self.app.exit()
