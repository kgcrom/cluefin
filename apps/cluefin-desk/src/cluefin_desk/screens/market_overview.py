import asyncio

from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import DataTable, Header, Select, Static

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

    @work(thread=True)
    def load_all_data(self) -> None:
        self._load_market_overview()
        self._load_sector_data("001")
        self._load_top_movers()

    @work(thread=True)
    def _reload_sector_data(self, inds_cd: str) -> None:
        self._load_sector_data(inds_cd)

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
            from loguru import logger

            logger.error(f"Failed to load sector data: {e}")

    def _load_top_movers(self) -> None:
        try:
            screener = self.app.screener
            gainers = screener.get_top_gainers()
            losers = screener.get_top_losers()

            def _update():
                # Top Gainers
                lines = ["[bold red]\u25b2 \uae09\ub4f1 (Top Gainers)[/bold red]"]
                for item in gainers[:5]:
                    rate = float(item.change_rate) if item.change_rate else 0.0
                    try:
                        price_str = f"{int(float(item.current_price)):,}"
                    except (ValueError, TypeError):
                        price_str = item.current_price
                    lines.append(f"  {item.stock_name:<10s} {price_str:>10s}  [red]+{rate:.2f}%[/red]")
                panel = self.query_one("#top-gainers-panel", Static)
                panel.update("\n".join(lines))

                # Top Losers
                lines = ["[bold blue]\u25bc \uae09\ub77d (Top Losers)[/bold blue]"]
                for item in losers[:5]:
                    rate = float(item.change_rate) if item.change_rate else 0.0
                    try:
                        price_str = f"{int(float(item.current_price)):,}"
                    except (ValueError, TypeError):
                        price_str = item.current_price
                    lines.append(f"  {item.stock_name:<10s} {price_str:>10s}  [blue]{rate:.2f}%[/blue]")
                panel = self.query_one("#top-losers-panel", Static)
                panel.update("\n".join(lines))

            self.app.call_from_thread(_update)
        except Exception as e:
            from loguru import logger

            logger.error(f"Failed to load top movers: {e}")

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
