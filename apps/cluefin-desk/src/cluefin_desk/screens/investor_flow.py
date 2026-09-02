from loguru import logger
from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import DataTable, Header, Select, Static

from cluefin_desk.formatting import pad
from cluefin_desk.screens._guard import screen_gone
from cluefin_desk.widgets.market_overview import MarketOverviewBar
from cluefin_desk.widgets.nav_bar import NavBar
from cluefin_desk.widgets.nav_footer import NavFooter

# ka10051/ka20002 의 시장구분 — 한 자리 코드. "0001" 을 주면 서버가 코스닥으로 해석한다.
SECTOR_MARKETS = [("KOSPI", "0"), ("KOSDAQ", "1")]


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
            yield Select(SECTOR_MARKETS, value="0", allow_blank=False, id="sector-market-select")
            with Horizontal(id="sector-investor-container"):
                yield DataTable(id="sector-investor-table")
                yield DataTable(id="sector-stocks-table")
            yield Static("업종 행에서 Enter 를 누르면 구성 종목이 오른쪽에 뜬다", id="sector-status")
        yield NavFooter(active_screen_key="5")

    def on_mount(self) -> None:
        nav = self.query_one("#nav-bar", NavBar)
        nav.set_active("5")
        self._setup_tables()
        self.load_all_data()

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "sector-market-select" and event.value != Select.BLANK:
            self._reload_sector_investor(str(event.value))

    def _sector_market(self) -> str:
        value = self.query_one("#sector-market-select", Select).value
        return "0" if value == Select.BLANK else str(value)

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
            ("지수", 10),
            ("등락률", 8),
            ("외국인", 12),
            ("개인", 12),
        ]:
            tbl.add_column(label, key=label, width=width)

        # Stocks in the selected sector
        tbl = self.query_one("#sector-stocks-table", DataTable)
        tbl.cursor_type = "row"
        tbl.zebra_stripes = True
        for label, width in [
            ("종목코드", 8),
            ("종목명", 16),
            ("현재가", 10),
            ("등락률", 8),
            ("거래량", 12),
        ]:
            tbl.add_column(label, key=label, width=width)

    # `r` 연타로 워커가 겹치면 같은 패널에 두 응답이 번갈아 써진다 — 최신 것만 남긴다.
    @work(thread=True, exclusive=True, group="investor-load")
    def load_all_data(self) -> None:
        self._load_foreign_net_buy()
        self._load_institutional_net_buy()
        self._load_program_trading()
        self._load_sector_investor(self._sector_market())

    @work(thread=True, exclusive=True, group="investor-sector-load")
    def _reload_sector_investor(self, mrkt_tp: str) -> None:
        self._load_sector_investor(mrkt_tp)

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
                    lines.append(
                        f"  {pad(item.stk_nm, 16)} {pad(item.cur_prc, 10, 'right')}  순매수: {pad(item.netprps_qty, 10, 'right')}"
                    )
                panel = self.query_one("#foreign-net-buy-panel", Static)
                panel.update("\n".join(lines))

            self.app.call_from_thread(_update)
        except Exception as e:
            if screen_gone(self, e):
                return
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
                    lines.append(
                        f"  {pad(item.stk_nm, 16)}  매수: {pad(item.buy_qty, 10, 'right')}  매도: {pad(item.sel_qty, 10, 'right')}"
                    )
                panel = self.query_one("#institutional-net-buy-panel", Static)
                panel.update("\n".join(lines))

            self.app.call_from_thread(_update)
        except Exception as e:
            if screen_gone(self, e):
                return
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
            if screen_gone(self, e):
                return
            logger.error(f"Failed to load program trading: {e}")

    @staticmethod
    def _scaled(value: str, digits: int = 2) -> float | None:
        """ka10051 은 지수·등락률을 소수점 없는 100배 정수로 준다 (`-210` → -2.10)."""
        if not value or value == "-":
            return None
        try:
            return int(value) / 100
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return None

    @staticmethod
    def _fmt_signed_int(value: str) -> str:
        try:
            n = int(float(value))
        except (ValueError, TypeError):
            return value or "-"
        return f"{n:+,}" if n else "0"

    @staticmethod
    def _format_sector_row(item) -> tuple[str, str, str, str, str]:
        """업종별투자자순매수 한 행 → (업종명, 지수, 등락률, 외국인, 개인) 표시 문자열."""
        index = InvestorFlowScreen._scaled(item.cur_prc)
        rate = InvestorFlowScreen._scaled(item.flu_rt)
        index_str = f"{abs(index):,.2f}" if index is not None else "-"
        if rate is None:
            rate_str = "-"
        elif rate > 0:
            rate_str = f"[red]+{rate:.2f}%[/red]"
        elif rate < 0:
            rate_str = f"[blue]{rate:.2f}%[/blue]"
        else:
            rate_str = f"{rate:.2f}%"
        return (
            item.inds_nm,
            index_str,
            rate_str,
            InvestorFlowScreen._fmt_signed_int(item.frgnr_netprps),
            InvestorFlowScreen._fmt_signed_int(item.ind_netprps),
        )

    def _set_status(self, text: str) -> None:
        def _apply():
            self.query_one("#sector-status", Static).update(text)

        self.app.call_from_thread(_apply)

    def _load_sector_investor(self, mrkt_tp: str = "0") -> None:
        market_label = dict((code, name) for name, code in SECTOR_MARKETS).get(mrkt_tp, mrkt_tp)
        try:
            fetcher = self.app.fetcher
            response = fetcher.get_industry_investor_net_buy(mrkt_tp=mrkt_tp)
            logger.debug(f"[INV] sector investor API response status: {response.headers}")
            items = response.body.inds_netprps
            logger.debug(f"[INV] sector investor items count: {len(items)}")
            if not items:
                self._set_status(f"{market_label} 업종별 투자자 순매수 데이터 없음")
                return

            def _update():
                tbl = self.query_one("#sector-investor-table", DataTable)
                tbl.clear()
                for item in items[:40]:
                    tbl.add_row(*self._format_sector_row(item), key=item.inds_cd)
                self.query_one("#sector-stocks-table", DataTable).clear()
                self.query_one("#sector-status", Static).update(
                    f"{market_label} 업종 {len(items)}건 (순매수: 수량) — 업종 행에서 Enter 를 누르면 구성 종목이 오른쪽에 뜬다"
                )

            self.app.call_from_thread(_update)
        except Exception as e:
            if screen_gone(self, e):
                return
            logger.error(f"Failed to load sector investor: {e}")
            self._set_status(f"업종별 투자자 순매수 로딩 실패: {e}")

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        # DataTable 이 Enter 를 먼저 먹으므로 Screen 의 `enter` 바인딩은 표에 포커스가 있을 때
        # 오지 않는다 — 행 선택 이벤트로 받는다.
        table_id = event.data_table.id
        code = str(event.row_key.value) if event.row_key is not None else ""
        if not code:
            return
        if table_id == "sector-investor-table":
            self._load_sector_stocks(self._sector_market(), code)
        elif table_id in ("program-trading-table", "sector-stocks-table"):
            self._open_detail(code)

    @work(thread=True, exclusive=True, group="investor-sector-stocks")
    def _load_sector_stocks(self, mrkt_tp: str, inds_cd: str) -> None:
        self._set_status(f"업종 {inds_cd} 구성 종목 조회 중...")
        try:
            response = self.app.fetcher.get_industry_price_by_sector(mrkt_tp=mrkt_tp, inds_cd=inds_cd)
            items = response.body.inds_stkpc or []

            def _update():
                tbl = self.query_one("#sector-stocks-table", DataTable)
                tbl.clear()
                for item in items:
                    tbl.add_row(*self._format_sector_stock_row(item), key=item.stk_cd)
                status = self.query_one("#sector-status", Static)
                if items:
                    status.update(f"업종 {inds_cd} 구성 종목 {len(items)}건 — 종목 행에서 Enter 를 누르면 상세로 간다")
                else:
                    status.update(f"업종 {inds_cd} 구성 종목 없음")

            self.app.call_from_thread(_update)
        except Exception as e:
            if screen_gone(self, e):
                return
            logger.error(f"Failed to load sector stocks: {e}")
            self._set_status(f"업종 {inds_cd} 구성 종목 로딩 실패: {e}")

    @staticmethod
    def _format_sector_stock_row(item) -> tuple[str, str, str, str, str]:
        """업종별주가(ka20002) 한 행. 여기 값들은 부호 붙은 보통 소수 문자열이다 (`-0.58`)."""
        try:
            rate = float(item.flu_rt) if item.flu_rt and item.flu_rt != "-" else 0.0
        except ValueError:
            rate = 0.0
        if rate > 0:
            rate_str = f"[red]+{rate:.2f}%[/red]"
        elif rate < 0:
            rate_str = f"[blue]{rate:.2f}%[/blue]"
        else:
            rate_str = f"{rate:.2f}%"
        try:
            price_str = f"{abs(int(float(item.cur_prc))):,}"
        except (ValueError, TypeError):
            price_str = item.cur_prc or "-"
        try:
            vol_str = f"{int(float(item.now_trde_qty)):,}"
        except (ValueError, TypeError):
            vol_str = item.now_trde_qty or "-"
        return (item.stk_cd, pad(item.stk_nm, 16), price_str, rate_str, vol_str)

    def _open_detail(self, stock_code: str) -> None:
        from cluefin_desk.screens.stock_detail import StockDetailScreen

        self.app.push_screen(StockDetailScreen(stock_code=stock_code))

    def action_refresh(self) -> None:
        self.load_all_data()

    def action_select_stock(self) -> None:
        for selector in ("#sector-stocks-table", "#program-trading-table"):
            tbl = self.query_one(selector, DataTable)
            if tbl.has_focus and tbl.cursor_row is not None and tbl.row_count > 0:
                row_key, _ = tbl.coordinate_to_cell_key(tbl.cursor_coordinate)
                if row_key.value:
                    self._open_detail(str(row_key.value))
                return

    def action_go_back(self) -> None:
        self.app.action_switch_screen("1")

    def action_quit(self) -> None:
        self.app.exit()
