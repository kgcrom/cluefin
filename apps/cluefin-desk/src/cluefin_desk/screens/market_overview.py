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

INDUSTRY_CODES = [("KOSPI", "001"), ("KOSDAQ", "101")]


class MarketOverviewScreen(Screen):
    """Screen 1: Market Overview - sector performance + top movers."""

    BINDINGS = [
        Binding("r", "refresh", "Refresh"),
        Binding("enter", "select_stock", "Detail"),
        Binding("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield NavBar(id="nav-bar")
        yield MarketOverviewBar(id="market-bar")
        with Vertical(id="market-overview-content"):
            yield Select(INDUSTRY_CODES, value="001", id="sector-select")
            yield DataTable(id="sector-table-container")
            with Horizontal(id="top-movers-container"):
                yield Static("Loading...", id="top-gainers-panel")
                yield Static("Loading...", id="top-losers-panel")
            with Horizontal(id="kis-market-container"):
                yield Static("Loading...", id="kis-investor-panel")
                yield Static("Loading...", id="kis-fund-panel")
        yield NavFooter(active_screen_key="1")

    def on_mount(self) -> None:
        nav = self.query_one("#nav-bar", NavBar)
        nav.set_active("1")
        self._setup_sector_table()
        self.load_all_data()

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "sector-select" and event.value != Select.BLANK:
            self._reload_sector_data(str(event.value))

    def _setup_sector_table(self) -> None:
        table = self.query_one("#sector-table-container", DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        for label, width in [
            ("#", 4),
            ("업종명", 16),
            ("현재가", 12),
            ("전일대비", 10),
            ("등락률", 10),
            ("거래량", 14),
        ]:
            table.add_column(label, key=label, width=width)

    # `r` 연타로 워커가 겹치면 같은 패널에 두 응답이 번갈아 써진다 — 최신 것만 남긴다.
    @work(thread=True, exclusive=True, group="market-load")
    def load_all_data(self) -> None:
        self._load_sector_data("001")
        self._load_top_movers()
        self._load_kis_market_data()

    @work(thread=True)
    def _reload_sector_data(self, inds_cd: str) -> None:
        self._load_sector_data(inds_cd)

    def _load_sector_data(self, inds_cd: str = "001") -> None:
        try:
            fetcher = self.app.fetcher
            response = fetcher.get_all_industry_index(inds_cd=inds_cd)
            items = response.body.all_inds_idex
            if not items:
                return

            def _update():
                table = self.query_one("#sector-table-container", DataTable)
                table.clear()
                for idx, item in enumerate(items[:30]):
                    rate = float(item.flu_rt) if item.flu_rt and item.flu_rt != "-" else 0.0
                    sign = item.pre_sig if hasattr(item, "pre_sig") else ""
                    if rate > 0 or sign == "2":
                        rate_str = f"[red]+{rate:.2f}%[/red]"
                        pred_str = f"[red]\u25b2 {item.pred_pre}[/red]"
                    elif rate < 0 or sign == "5":
                        rate_str = f"[blue]{rate:.2f}%[/blue]"
                        pred_str = f"[blue]\u25bc {item.pred_pre}[/blue]"
                    else:
                        rate_str = f"{rate:.2f}%"
                        pred_str = item.pred_pre

                    try:
                        vol_str = f"{int(float(item.trde_qty)):,}" if item.trde_qty else "-"
                    except (ValueError, TypeError):
                        vol_str = item.trde_qty or "-"

                    table.add_row(
                        str(idx + 1),
                        item.stk_nm,
                        item.cur_prc,
                        pred_str,
                        rate_str,
                        vol_str,
                        key=item.stk_cd,
                    )

            self.app.call_from_thread(_update)
        except Exception as e:
            if screen_gone(self, e):
                return
            from loguru import logger

            logger.error(f"Failed to load sector data: {e}")

    @staticmethod
    def _format_mover_lines(title: str, items, positive: bool) -> list[str]:
        """급등/급락 패널 한 줄씩. 종목명은 한글(두 칸)이라 `pad` 로 셀 폭을 맞춘다 —
        f-string 정렬은 글자 수 기준이어서 현재가·등락률 컬럼이 줄마다 어긋난다."""
        color = "red" if positive else "blue"
        arrow = "\u25b2" if positive else "\u25bc"
        lines = [f"[bold {color}]{arrow} {title}[/bold {color}]"]
        if not items:
            lines.append("  데이터 없음")
            return lines
        for item in items[:5]:
            try:
                rate = float(item.change_rate) if item.change_rate else 0.0
            except (ValueError, TypeError):
                rate = 0.0
            try:
                price_str = f"{int(float(item.current_price)):,}"
            except (ValueError, TypeError):
                price_str = item.current_price or "-"
            sign = "+" if rate > 0 else ""
            rate_str = pad(f"{sign}{rate:.2f}%", 8, align="right")
            lines.append(
                f"  {pad(item.stock_name, 16)} {pad(price_str, 10, align='right')}  [{color}]{rate_str}[/{color}]"
            )
        return lines

    def _load_top_movers(self) -> None:
        try:
            screener = self.app.screener
            gainers = screener.get_top_gainers()
            losers = screener.get_top_losers()

            def _update():
                self.query_one("#top-gainers-panel", Static).update(
                    "\n".join(self._format_mover_lines("급등 (Top Gainers)", gainers, positive=True))
                )
                self.query_one("#top-losers-panel", Static).update(
                    "\n".join(self._format_mover_lines("급락 (Top Losers)", losers, positive=False))
                )

            self.app.call_from_thread(_update)
        except Exception as e:
            if screen_gone(self, e):
                return
            from loguru import logger

            logger.error(f"Failed to load top movers: {e}")
            err_msg = str(e)

            def _update_error():
                # 실패를 로그에만 남기면 두 패널이 영구히 "Loading..." 으로 남는다.
                for selector, title in (
                    ("#top-gainers-panel", "급등 (Top Gainers)"),
                    ("#top-losers-panel", "급락 (Top Losers)"),
                ):
                    self.query_one(selector, Static).update(f"[bold]{title}[/bold]\n\n  로드 실패: {err_msg}")

            self.app.call_from_thread(_update_error)

    @staticmethod
    def _fmt_amount(value) -> str:
        try:
            return f"{int(float(value)):,}"
        except (ValueError, TypeError):
            return str(value) if value else "-"

    @staticmethod
    def _format_kis_investor_lines(investors) -> list[str]:
        """코스피 투자자별 순매수. KIS 는 조회 시작일부터 오름차순으로 주므로
        최근 날짜가 위로 오게 정렬한 뒤 5일만 보인다."""
        lines = ["[bold]코스피 투자자별 순매수 (KIS, 주)[/bold]"]
        if not investors:
            lines.append("  데이터 없음")
            return lines
        lines.append(
            f"{pad('일자', 10)} {pad('개인', 12, 'right')} {pad('외국인', 12, 'right')} {pad('기관', 12, 'right')}"
        )
        ordered = sorted(investors, key=lambda i: i.stck_bsop_date, reverse=True)
        for item in ordered[:5]:
            lines.append(
                f"{pad(item.stck_bsop_date, 10)} "
                f"{pad(MarketOverviewScreen._fmt_amount(item.prsn_ntby_qty), 12, 'right')} "
                f"{pad(MarketOverviewScreen._fmt_amount(item.frgn_ntby_qty), 12, 'right')} "
                f"{pad(MarketOverviewScreen._fmt_amount(item.orgn_ntby_qty), 12, 'right')}"
            )
        return lines

    @staticmethod
    def _format_kis_fund_lines(funds) -> list[str]:
        lines = ["[bold]시장 자금 동향 (KIS, 억원)[/bold]"]
        if not funds:
            lines.append("  데이터 없음")
            return lines
        lines.append(
            f"{pad('일자', 10)} {pad('예탁금', 12, 'right')} {pad('신용융자', 12, 'right')} {pad('MMF', 12, 'right')}"
        )
        ordered = sorted(funds, key=lambda i: i.bsop_date, reverse=True)
        for item in ordered[:5]:
            lines.append(
                f"{pad(item.bsop_date, 10)} "
                f"{pad(MarketOverviewScreen._fmt_amount(item.cust_dpmn_amt), 12, 'right')} "
                f"{pad(MarketOverviewScreen._fmt_amount(item.crdt_loan_rmnd), 12, 'right')} "
                f"{pad(MarketOverviewScreen._fmt_amount(item.mmf_amt), 12, 'right')}"
            )
        return lines

    def _set_panel(self, selector: str, text: str) -> None:
        def _apply():
            self.query_one(selector, Static).update(text)

        self.app.call_from_thread(_apply)

    def _load_kis_market_data(self) -> None:
        """KIS 시장 수급·자금 패널. 키가 없거나 실패해도 패널에 그 사실을 남긴다 —
        빈 문자열로 두면 자리만 차지한 채 "안 보이는" 패널이 된다."""
        fetcher = self.app.fetcher
        if not fetcher.has_kis:
            self._set_panel("#kis-investor-panel", "[bold]코스피 투자자별 순매수 (KIS)[/bold]\n  KIS 키 없음")
            self._set_panel("#kis-fund-panel", "[bold]시장 자금 동향 (KIS)[/bold]\n  KIS 키 없음")
            return

        for selector, label, fetch, fmt in (
            (
                "#kis-investor-panel",
                "투자자별 순매수",
                lambda: fetcher.get_market_investor_trend_daily(market="KSP"),
                self._format_kis_investor_lines,
            ),
            ("#kis-fund-panel", "시장 자금 동향", fetcher.get_market_fund_summary, self._format_kis_fund_lines),
        ):
            try:
                self._set_panel(selector, "\n".join(fmt(fetch())))
            except Exception as e:
                if screen_gone(self, e):
                    return
                from loguru import logger

                logger.error(f"Failed to load KIS {label}: {e}")
                self._set_panel(selector, f"[bold]{label} (KIS)[/bold]\n  로드 실패: {e}")

    def action_refresh(self) -> None:
        self.load_all_data()

    def action_select_stock(self) -> None:
        table = self.query_one("#sector-table-container", DataTable)
        if table.cursor_row is not None and table.row_count > 0:
            row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
            stock_code = str(row_key.value)
            if stock_code:
                from cluefin_desk.screens.stock_detail import StockDetailScreen

                self.app.push_screen(StockDetailScreen(stock_code=stock_code))

    def action_quit(self) -> None:
        self.app.exit()
