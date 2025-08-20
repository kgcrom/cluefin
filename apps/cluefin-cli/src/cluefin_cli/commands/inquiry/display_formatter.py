"""Display formatting system for stock inquiry results."""

import unicodedata
from decimal import Decimal
from typing import TYPE_CHECKING, Any, List, Optional, Union

from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from rich.text import Text

if TYPE_CHECKING:
    from .config_models import APIConfig


class DisplayFormatter:
    """Base display formatter with Korean text support and rich formatting."""

    def __init__(self):
        """Initialize the display formatter with console and styling."""
        self.console = Console()

        # Color schemes for different data types
        self.colors = {
            "positive": "bright_red",  # 상승 (빨간색)
            "negative": "bright_blue",  # 하락 (파란색)
            "neutral": "white",
            "header": "bold cyan",
            "volume": "yellow",
            "price": "bright_white",
            "percentage": "magenta",
            "error": "bold red",
            "success": "bold green",
            "info": "bright_blue",
        }

        # Styles for different contexts
        self.styles = {
            "title": Style(color="cyan", bold=True),
            "subtitle": Style(color="cyan"),
            "data_positive": Style(color="bright_red"),
            "data_negative": Style(color="bright_blue"),
            "data_neutral": Style(color="white"),
            "header": Style(color="cyan", bold=True),
            "error": Style(color="red", bold=True),
            "success": Style(color="green", bold=True),
        }

    def calculate_text_width(self, text: str) -> int:
        """
        Calculate display width of text containing Korean characters.

        Korean characters are typically double-width in terminal display.

        Args:
            text: Text string that may contain Korean characters

        Returns:
            Display width of the text
        """
        width = 0
        for char in text:
            if unicodedata.east_asian_width(char) in ("F", "W"):
                # Full-width or Wide characters (Korean, Chinese, Japanese)
                width += 2
            else:
                # Half-width characters (ASCII, etc.)
                width += 1
        return width

    def pad_korean_text(self, text: str, target_width: int, align: str = "left") -> str:
        """
        Pad text to target width considering Korean character widths.

        Args:
            text: Text to pad
            target_width: Target display width
            align: Alignment ('left', 'right', 'center')

        Returns:
            Padded text string
        """
        current_width = self.calculate_text_width(text)
        padding_needed = target_width - current_width

        if padding_needed <= 0:
            return text

        if align == "right":
            return " " * padding_needed + text
        elif align == "center":
            left_pad = padding_needed // 2
            right_pad = padding_needed - left_pad
            return " " * left_pad + text + " " * right_pad
        else:  # left align
            return text + " " * padding_needed

    def format_number(self, value: Union[int, float, Decimal, str], number_type: str = "default") -> str:
        """
        Format numbers with appropriate styling and Korean number formatting.

        Args:
            value: Numeric value to format
            number_type: Type of number ('price', 'volume', 'percentage', 'default')

        Returns:
            Formatted number string
        """
        if value is None or value == "":
            return "-"

        try:
            if isinstance(value, str):
                # Try to convert string to number
                if "." in value:
                    num_value = float(value)
                else:
                    num_value = int(value)
            else:
                num_value = float(value) if isinstance(value, Decimal) else value

            if number_type == "price":
                # Format price with commas and 2 decimal places if needed
                if num_value == int(num_value):
                    return f"{int(num_value):,}"
                else:
                    return f"{num_value:,.2f}"

            elif number_type == "volume":
                # Format large volumes with Korean units
                if num_value >= 100000000:  # 1억 이상
                    return f"{num_value / 100000000:.1f}억"
                elif num_value >= 10000:  # 1만 이상
                    return f"{num_value / 10000:.1f}만"
                else:
                    return f"{int(num_value):,}"

            elif number_type == "percentage":
                # Format percentage with + or - sign
                sign = "+" if num_value > 0 else ""
                return f"{sign}{num_value:.2f}%"

            else:  # default
                if isinstance(num_value, int) or num_value == int(num_value):
                    return f"{int(num_value):,}"
                else:
                    return f"{num_value:,.2f}"

        except (ValueError, TypeError):
            return str(value)

    def get_color_for_value(self, value: Union[int, float, str]) -> str:
        """
        Get appropriate color for a numeric value (positive/negative/neutral).

        Args:
            value: Numeric value to evaluate

        Returns:
            Color name for the value
        """
        try:
            if isinstance(value, str):
                # Handle percentage strings like "+1.23%" or "-0.45%"
                clean_value = value.replace("%", "").replace("+", "").replace(",", "")
                num_value = float(clean_value)
            else:
                num_value = float(value)

            if num_value > 0:
                return self.colors["positive"]
            elif num_value < 0:
                return self.colors["negative"]
            else:
                return self.colors["neutral"]
        except (ValueError, TypeError):
            return self.colors["neutral"]

    def create_table(
        self, headers: List[str], rows: List[List[str]], title: Optional[str] = None, show_lines: bool = True
    ) -> Table:
        """
        Create a formatted table with Korean text support.

        Args:
            headers: List of column headers
            rows: List of row data
            title: Optional table title
            show_lines: Whether to show grid lines

        Returns:
            Rich Table object
        """
        # Create table with appropriate styling
        table = Table(
            title=title,
            title_style=self.styles["title"],
            box=box.ROUNDED if show_lines else box.SIMPLE,
            show_header=True,
            header_style=self.styles["header"],
            show_lines=show_lines,
            expand=True,
        )

        # Add columns with proper width calculation
        for header in headers:
            table.add_column(header, justify="center", style=self.styles["data_neutral"], no_wrap=False)

        # Add rows with appropriate styling
        for row in rows:
            styled_row = []
            for i, cell in enumerate(row):
                # Apply color coding based on content
                if i > 0 and any(char in str(cell) for char in ["+", "-", "%"]):
                    # This looks like a numeric value that might need color coding
                    color = self.get_color_for_value(cell)
                    styled_row.append(Text(str(cell), style=color))
                else:
                    styled_row.append(str(cell))

            table.add_row(*styled_row)

        return table

    def display_table(self, headers: List[str], rows: List[List[str]], title: Optional[str] = None) -> None:
        """
        Display a formatted table to console.

        Args:
            headers: List of column headers
            rows: List of row data
            title: Optional table title
        """
        table = self.create_table(headers, rows, title)
        self.console.print(table)
        self.console.print()  # Add spacing after table

    def display_error(self, message: str, title: str = "오류") -> None:
        """
        Display an error message with appropriate styling and helpful tips.

        Args:
            message: Error message to display
            title: Error title (default: "오류")
        """
        error_content = message

        # Add helpful tips based on error type
        if "인증" in message or "API 키" in message:
            error_content += "\n\n💡 도움말:"
            error_content += "\n• KIWOOM_APP_KEY 환경변수를 확인해보세요"
            error_content += "\n• KIWOOM_SECRET_KEY 환경변수를 확인해보세요"
        elif "네트워크" in message or "연결" in message:
            error_content += "\n\n💡 도움말:"
            error_content += "\n• 인터넷 연결을 확인해보세요"
            error_content += "\n• 잠시 후 다시 시도해보세요"
        elif "한도" in message or "429" in message:
            error_content += "\n\n💡 도움말:"
            error_content += "\n• 1분 정도 기다린 후 다시 시도해보세요"
            error_content += "\n• 요청 건수를 줄여보세요"
        elif "데이터 없음" in title or "조회된 데이터가 없" in message:
            error_content += "\n\n💡 도움말:"
            error_content += "\n• 다른 조건으로 검색해보세요"
            error_content += "\n• 시장 시간 내에 다시 시도해보세요"

        error_panel = Panel(
            Text(error_content, style=self.styles["error"]),
            title=f"[red bold]❗ {title} ❗[/red bold]",
            border_style="red",
            expand=False,
        )
        self.console.print(error_panel)
        self.console.print()

    def display_success(self, message: str, title: str = "성공") -> None:
        """
        Display a success message with appropriate styling.

        Args:
            message: Success message to display
            title: Success title (default: "성공")
        """
        success_panel = Panel(
            Text(message, style=self.styles["success"]),
            title=f"[green bold]{title}[/green bold]",
            border_style="green",
            expand=False,
        )
        self.console.print(success_panel)
        self.console.print()

    def display_info(self, message: str, title: str = "정보") -> None:
        """
        Display an info message with appropriate styling.

        Args:
            message: Info message to display
            title: Info title (default: "정보")
        """
        info_panel = Panel(
            Text(message, style=Style(color=self.colors["info"])),
            title=f"[bright_blue]{title}[/bright_blue]",
            border_style="blue",
            expand=False,
        )
        self.console.print(info_panel)
        self.console.print()

    def display_loading(self, message: str = "데이터를 가져오는 중...") -> None:
        """
        Display a loading message.

        Args:
            message: Loading message to display
        """
        self.console.print(f"[yellow]⏳ {message}[/yellow]")

    def clear_screen(self) -> None:
        """Clear the console screen."""
        self.console.clear()

    def print_separator(self, char: str = "─", length: int = 80) -> None:
        """
        Print a separator line.

        Args:
            char: Character to use for separator
            length: Length of separator line
        """
        self.console.print(char * length, style="dim")


class RankingDataFormatter(DisplayFormatter):
    """Specialized formatter for ranking API responses."""

    def format_ranking_data(self, data: Any, api_config: "APIConfig") -> None:
        """
        Format and display ranking data with volume and price formatting.

        Args:
            data: API response data
            api_config: APIConfig object containing API metadata
        """
        if not data:
            self.display_error("조회된 데이터가 없습니다.", "데이터 없음")
            return

        # Route to specific formatter based on API configuration
        api_name = api_config.name

        if api_name == "rapidly_increasing_trading_volume":
            self._format_rapidly_increasing_trading_volume(data, api_config.korean_name)
        elif api_name == "current_day_trading_volume_top":
            self._format_current_day_trading_volume(data, api_config.korean_name)
        elif api_name == "previous_day_trading_volume_top":
            self._format_previous_day_trading_volume(data, api_config.korean_name)
        elif api_name == "trading_value_top":
            self._format_top_trading_value(data, api_config.korean_name)
        elif api_name == "foreign_period_trading_top":
            self._format_top_foreign_period_trading(data, api_config.korean_name)
        elif api_name == "foreign_consecutive_trading_top":
            self._format_foreign_consecutive_trading(data, api_config.korean_name)
        elif api_name == "foreign_institutional_trading_top":
            self._format_foreign_institutional_trading(data, api_config.korean_name)
        else:
            # Fallback to generic formatting
            self._format_generic_ranking(data, api_config.korean_name)

    def _format_rapidly_increasing_trading_volume(self, data: Any, title: str) -> None:
        """Format rapidly increasing trading volume data."""
        headers = ["순위", "종목명", "종목코드", "현재가", "등락률", "이전거래량", "현재거래량", "급증량", "급증률"]
        rows = []

        # Access the trde_qty_sdnin array from the response
        items = []
        if hasattr(data, "trde_qty_sdnin"):
            items = data.trde_qty_sdnin
        elif isinstance(data, list):
            items = data
        else:
            # Fallback to generic formatting
            self._format_generic_ranking(data, title)
            return

        for i, item in enumerate(items[:20], 1):  # Show top 20
            try:
                # Extract fields based on DomesticRankInfoRapidlyIncreasingTradingVolumeItem
                stock_name = getattr(item, "stk_nm", "-")
                stock_code = getattr(item, "stk_cd", "-")
                current_price = getattr(item, "cur_prc", "0")
                change_rate = getattr(item, "flu_rt", "0")
                prev_volume = getattr(item, "prev_trde_qty", "0")
                current_volume = getattr(item, "now_trde_qty", "0")
                increase_qty = getattr(item, "sdnin_qty", "0")
                increase_rate = getattr(item, "sdnin_rt", "0")

                rows.append([
                    str(i),
                    stock_name,
                    stock_code,
                    self.format_number(current_price, "price"),
                    self.format_number(change_rate, "percentage"),
                    self.format_number(prev_volume, "volume"),
                    self.format_number(current_volume, "volume"),
                    self.format_number(increase_qty, "volume"),
                    self.format_number(increase_rate, "percentage"),
                ])
            except Exception:
                continue

        if rows:
            self.display_table(headers, rows, f"🚀 {title}")
        else:
            self.display_error("데이터 형식을 인식할 수 없습니다.", "형식 오류")

    def _format_current_day_trading_volume(self, data: Any, title: str) -> None:
        """Format current day trading volume top data."""
        headers = ["순위", "종목명", "종목코드", "현재가", "등락률", "거래량", "거래회전율", "거래대금", "장중거래량"]
        rows = []

        # Access the tdy_trde_qty_upper array from the response
        items = []
        if hasattr(data, "tdy_trde_qty_upper"):
            items = data.tdy_trde_qty_upper
        elif isinstance(data, list):
            items = data
        else:
            # Fallback to generic formatting
            self._format_generic_ranking(data, title)
            return

        for i, item in enumerate(items[:20], 1):  # Show top 20
            try:
                # Extract fields based on DomesticRankInfoTopCurrentDayTradingVolumeItem
                stock_name = getattr(item, "stk_nm", "-")
                stock_code = getattr(item, "stk_cd", "-")
                current_price = getattr(item, "cur_prc", "0")
                change_rate = getattr(item, "flu_rt", "0")
                trading_volume = getattr(item, "trde_qty", "0")
                trading_turnover = getattr(item, "trde_tern_rt", "0")
                trading_amount = getattr(item, "trde_amt", "0")
                intraday_volume = getattr(item, "opmr_trde_qty", "0")

                rows.append([
                    str(i),
                    stock_name,
                    stock_code,
                    self.format_number(current_price, "price"),
                    self.format_number(change_rate, "percentage"),
                    self.format_number(trading_volume, "volume"),
                    self.format_number(trading_turnover, "percentage"),
                    self.format_number(trading_amount, "volume"),
                    self.format_number(intraday_volume, "volume"),
                ])
            except Exception:
                continue

        if rows:
            self.display_table(headers, rows, f"📊 {title}")
        else:
            self.display_error("데이터 형식을 인식할 수 없습니다.", "형식 오류")

    def _format_previous_day_trading_volume(self, data: Any, title: str) -> None:
        """Format previous day trading volume top data."""
        headers = ["순위", "종목명", "종목코드", "현재가", "전일대비", "거래량"]
        rows = []

        # Access the pred_trde_qty_upper array from the response
        items = []
        if hasattr(data, "pred_trde_qty_upper"):
            items = data.pred_trde_qty_upper
        elif isinstance(data, list):
            items = data
        else:
            # Fallback to generic formatting
            self._format_generic_ranking(data, title)
            return

        for i, item in enumerate(items[:20], 1):  # Show top 20
            try:
                # Extract fields based on DomesticRankInfoTopPreviousDayTradingVolumeItem
                stock_name = getattr(item, "stk_nm", "-")
                stock_code = getattr(item, "stk_cd", "-")
                current_price = getattr(item, "cur_prc", "0")
                prev_diff = getattr(item, "pred_pre", "0")
                trading_volume = getattr(item, "trde_qty", "0")

                rows.append([
                    str(i),
                    stock_name,
                    stock_code,
                    self.format_number(current_price, "price"),
                    self.format_number(prev_diff, "price"),
                    self.format_number(trading_volume, "volume"),
                ])
            except Exception:
                continue

        if rows:
            self.display_table(headers, rows, f"📉 {title}")
        else:
            self.display_error("데이터 형식을 인식할 수 없습니다.", "형식 오류")

    def _format_top_trading_value(self, data: Any, title: str) -> None:
        """Format trading value top data with ranking changes."""
        headers = ["현재순위", "전일순위", "변동", "종목명", "종목코드", "현재가", "등락률", "거래대금", "현재거래량"]
        rows = []

        # Access the trde_prica_upper array from the response
        items = []
        if hasattr(data, "trde_prica_upper"):
            items = data.trde_prica_upper
        elif isinstance(data, list):
            items = data
        else:
            # Fallback to generic formatting
            self._format_generic_ranking(data, title)
            return

        for item in items[:20]:  # Show top 20
            try:
                # Extract fields based on DomesticRankInfoTopTransactionValueItem
                now_rank = getattr(item, "now_rank", "0")
                prev_rank = getattr(item, "pred_rank", "0")
                stock_name = getattr(item, "stk_nm", "-")
                stock_code = getattr(item, "stk_cd", "-")
                current_price = getattr(item, "cur_prc", "0")
                change_rate = getattr(item, "flu_rt", "0")
                trading_value = getattr(item, "trde_prica", "0")
                current_volume = getattr(item, "now_trde_qty", "0")

                # Calculate rank change
                rank_change = ""
                try:
                    now_rank_int = int(now_rank)
                    prev_rank_int = int(prev_rank)
                    if prev_rank_int == 0:
                        rank_change = "신규"
                    else:
                        diff = prev_rank_int - now_rank_int
                        if diff > 0:
                            rank_change = f"↑{diff}"
                        elif diff < 0:
                            rank_change = f"↓{abs(diff)}"
                        else:
                            rank_change = "-"
                except (ValueError, TypeError):
                    rank_change = "-"

                rows.append([
                    now_rank,
                    prev_rank if prev_rank != "0" else "-",
                    rank_change,
                    stock_name,
                    stock_code,
                    self.format_number(current_price, "price"),
                    self.format_number(change_rate, "percentage"),
                    self.format_number(trading_value, "volume"),
                    self.format_number(current_volume, "volume"),
                ])
            except Exception:
                continue

        if rows:
            self.display_table(headers, rows, f"💵 {title}")
        else:
            self.display_error("데이터 형식을 인식할 수 없습니다.", "형식 오류")

    def _format_top_foreign_period_trading(self, data: Any, title: str) -> None:
        """Format foreign period trading top data."""
        headers = ["순위", "종목명", "종목코드", "현재가", "전일대비", "거래량", "순매수량", "취득가능주식수"]
        rows = []

        # Access the for_dt_trde_upper array from the response
        items = []
        if hasattr(data, "for_dt_trde_upper"):
            items = data.for_dt_trde_upper
        elif isinstance(data, list):
            items = data
        else:
            # Fallback to generic formatting
            self._format_generic_ranking(data, title)
            return

        for item in items[:20]:  # Show top 20
            try:
                # Extract fields based on DomesticRankInfoTopForeignerPeriodTradingItem
                rank = getattr(item, "rank", "0")
                stock_name = getattr(item, "stk_nm", "-")
                stock_code = getattr(item, "stk_cd", "-")
                current_price = getattr(item, "cur_prc", "0")
                prev_diff = getattr(item, "pred_pre", "0")
                trading_volume = getattr(item, "trde_qty", "0")
                net_buy_qty = getattr(item, "netprps_qty", "0")
                acquirable_shares = getattr(item, "gain_pos_stkcnt", "0")

                rows.append([
                    rank,
                    stock_name,
                    stock_code,
                    self.format_number(current_price, "price"),
                    self.format_number(prev_diff, "price"),
                    self.format_number(trading_volume, "volume"),
                    self.format_number(net_buy_qty, "volume"),
                    self.format_number(acquirable_shares, "volume"),
                ])
            except Exception:
                continue

        if rows:
            self.display_table(headers, rows, f"🌍 {title}")
        else:
            self.display_error("데이터 형식을 인식할 수 없습니다.", "형식 오류")

    def _format_foreign_consecutive_trading(self, data: Any, title: str) -> None:
        """Format foreign consecutive trading top data with daily breakdown."""
        headers = ["순위", "종목명", "종목코드", "현재가", "전일대비", "D-1", "D-2", "D-3", "합계", "한도소진율"]
        rows = []

        # Access the for_cont_nettrde_upper array from the response
        items = []
        if hasattr(data, "for_cont_nettrde_upper"):
            items = data.for_cont_nettrde_upper
        elif isinstance(data, list):
            items = data
        else:
            # Fallback to generic formatting
            self._format_generic_ranking(data, title)
            return

        for i, item in enumerate(items[:20], 1):  # Show top 20
            try:
                # Extract fields based on DomesticRankInfoTopConsecutiveNetBuySellByForeignersItem
                stock_name = getattr(item, "stk_nm", "-")
                stock_code = getattr(item, "stk_cd", "-")
                current_price = getattr(item, "cur_prc", "0")
                prev_diff = getattr(item, "pred_pre", "0")
                dm1 = getattr(item, "dm1", "0")
                dm2 = getattr(item, "dm2", "0")
                dm3 = getattr(item, "dm3", "0")
                total = getattr(item, "tot", "0")
                limit_exhaustion_rate = getattr(item, "limit_exh_rt", "0")

                rows.append([
                    str(i),
                    stock_name,
                    stock_code,
                    self.format_number(current_price, "price"),
                    self.format_number(prev_diff, "price"),
                    self.format_number(dm1, "volume"),
                    self.format_number(dm2, "volume"),
                    self.format_number(dm3, "volume"),
                    self.format_number(total, "volume"),
                    self.format_number(limit_exhaustion_rate, "percentage"),
                ])
            except Exception:
                continue

        if rows:
            self.display_table(headers, rows, f"🔄 {title}")
        else:
            self.display_error("데이터 형식을 인식할 수 없습니다.", "형식 오류")

    def _format_foreign_institutional_trading(self, data: Any, title: str) -> None:
        """Format foreign institutional trading top data with foreign/institutional breakdown."""
        headers = ["순위", "외인종목", "외인매도대금", "외인매수대금", "기관종목", "기관매도대금", "기관매수대금"]
        rows = []

        # Access the frgnr_orgn_trde_upper array from the response
        items = []
        if hasattr(data, "frgnr_orgn_trde_upper"):
            items = data.frgnr_orgn_trde_upper
        elif isinstance(data, list):
            items = data
        else:
            # Fallback to generic formatting
            self._format_generic_ranking(data, title)
            return

        for i, item in enumerate(items[:15], 1):  # Show top 15 (more columns)
            try:
                # Extract fields based on DomesticRankInfoTopForeignerLimitExhaustionRateItem
                # Foreign data
                for_sell_stock = getattr(item, "for_netslmt_stk_nm", "-")
                for_sell_amt = getattr(item, "for_netslmt_amt", "0")
                for_buy_stock = getattr(item, "for_netprps_stk_nm", "-")
                for_buy_amt = getattr(item, "for_netprps_amt", "0")

                # Institutional data
                orgn_sell_stock = getattr(item, "orgn_netslmt_stk_nm", "-")
                orgn_sell_amt = getattr(item, "orgn_netslmt_amt", "0")
                orgn_buy_stock = getattr(item, "orgn_netprps_stk_nm", "-")
                orgn_buy_amt = getattr(item, "orgn_netprps_amt", "0")

                rows.append([
                    str(i),
                    for_sell_stock if for_sell_stock != for_buy_stock else f"{for_sell_stock}(양)",
                    self.format_number(for_sell_amt, "volume"),
                    self.format_number(for_buy_amt, "volume"),
                    orgn_sell_stock if orgn_sell_stock != orgn_buy_stock else f"{orgn_sell_stock}(양)",
                    self.format_number(orgn_sell_amt, "volume"),
                    self.format_number(orgn_buy_amt, "volume"),
                ])
            except Exception:
                continue

        if rows:
            self.display_table(headers, rows, f"🏛️ {title}")
        else:
            self.display_error("데이터 형식을 인식할 수 없습니다.", "형식 오류")

    def _format_volume_ranking(self, data: Any, title: str) -> None:
        """Format volume-based ranking data."""
        headers = ["순위", "종목명", "종목코드", "현재가", "등락률", "거래량", "거래대금"]
        rows = []

        items = data if isinstance(data, list) else [data]

        for i, item in enumerate(items[:20], 1):  # Show top 20
            try:
                # Extract common fields with fallbacks
                stock_name = getattr(item, "hts_kor_isnm", getattr(item, "itm_nm", "-"))
                stock_code = getattr(item, "mksc_shrn_iscd", getattr(item, "stck_shrn_iscd", "-"))
                current_price = getattr(item, "stck_prpr", getattr(item, "prpr", "0"))
                change_rate = getattr(item, "prdy_ctrt", getattr(item, "ctrt", "0"))
                volume = getattr(item, "acml_vol", getattr(item, "vol", "0"))
                trading_value = getattr(item, "acml_tr_pbmn", getattr(item, "tr_pbmn", "0"))

                rows.append(
                    [
                        str(i),
                        stock_name,
                        stock_code,
                        self.format_number(current_price, "price"),
                        self.format_number(change_rate, "percentage"),
                        self.format_number(volume, "volume"),
                        self.format_number(trading_value, "volume"),
                    ]
                )
            except Exception:
                # Skip malformed entries
                continue

        if rows:
            self.display_table(headers, rows, f"📊 {title}")
        else:
            self.display_error("데이터 형식을 인식할 수 없습니다.", "형식 오류")

    def _format_trading_value_ranking(self, data: Any, title: str) -> None:
        """Format trading value ranking data."""
        headers = ["순위", "종목명", "종목코드", "현재가", "등락률", "거래대금", "시가총액"]
        rows = []

        items = data if isinstance(data, list) else [data]

        for i, item in enumerate(items[:20], 1):
            try:
                stock_name = getattr(item, "hts_kor_isnm", getattr(item, "itm_nm", "-"))
                stock_code = getattr(item, "mksc_shrn_iscd", getattr(item, "stck_shrn_iscd", "-"))
                current_price = getattr(item, "stck_prpr", getattr(item, "prpr", "0"))
                change_rate = getattr(item, "prdy_ctrt", getattr(item, "ctrt", "0"))
                trading_value = getattr(item, "acml_tr_pbmn", getattr(item, "tr_pbmn", "0"))
                market_cap = getattr(item, "lstg_stcn", getattr(item, "stcn", "0"))

                rows.append(
                    [
                        str(i),
                        stock_name,
                        stock_code,
                        self.format_number(current_price, "price"),
                        self.format_number(change_rate, "percentage"),
                        self.format_number(trading_value, "volume"),
                        self.format_number(market_cap, "volume"),
                    ]
                )
            except Exception:
                continue

        if rows:
            self.display_table(headers, rows, f"💰 {title}")
        else:
            self.display_error("데이터 형식을 인식할 수 없습니다.", "형식 오류")

    def _format_foreign_ranking(self, data: Any, title: str) -> None:
        """Format foreign investor ranking data."""
        headers = ["순위", "종목명", "종목코드", "현재가", "등락률", "순매수량", "순매수대금"]
        rows = []

        items = data if isinstance(data, list) else [data]

        for i, item in enumerate(items[:20], 1):
            try:
                stock_name = getattr(item, "hts_kor_isnm", getattr(item, "itm_nm", "-"))
                stock_code = getattr(item, "mksc_shrn_iscd", getattr(item, "stck_shrn_iscd", "-"))
                current_price = getattr(item, "stck_prpr", getattr(item, "prpr", "0"))
                change_rate = getattr(item, "prdy_ctrt", getattr(item, "ctrt", "0"))
                net_buy_qty = getattr(item, "frgn_ntby_qty", getattr(item, "ntby_qty", "0"))
                net_buy_amt = getattr(item, "frgn_ntby_tr_pbmn", getattr(item, "ntby_pbmn", "0"))

                rows.append(
                    [
                        str(i),
                        stock_name,
                        stock_code,
                        self.format_number(current_price, "price"),
                        self.format_number(change_rate, "percentage"),
                        self.format_number(net_buy_qty, "volume"),
                        self.format_number(net_buy_amt, "volume"),
                    ]
                )
            except Exception:
                continue

        if rows:
            self.display_table(headers, rows, f"🌍 {title}")
        else:
            self.display_error("데이터 형식을 인식할 수 없습니다.", "형식 오류")

    def _format_generic_ranking(self, data: Any, title: str) -> None:
        """Format generic ranking data when specific format is unknown."""
        if isinstance(data, list) and len(data) > 0:
            # Try to extract common fields from first item
            first_item = data[0]
            if hasattr(first_item, "__dict__"):
                # Get all attributes and create a generic table
                attrs = [attr for attr in dir(first_item) if not attr.startswith("_")]
                if attrs:
                    headers = ["순위"] + attrs[:6]  # Limit to 7 columns total
                    rows = []

                    for i, item in enumerate(data[:15], 1):  # Show top 15
                        row = [str(i)]
                        for attr in attrs[:6]:
                            value = getattr(item, attr, "-")
                            if isinstance(value, (int, float)) and attr in ["prpr", "stck_prpr"]:
                                row.append(self.format_number(value, "price"))
                            elif isinstance(value, (int, float)) and "vol" in attr:
                                row.append(self.format_number(value, "volume"))
                            elif isinstance(value, (int, float)) and "ctrt" in attr:
                                row.append(self.format_number(value, "percentage"))
                            else:
                                row.append(str(value))
                        rows.append(row)

                    self.display_table(headers, rows, f"📈 {title}")
                    return

        # Fallback: display raw data structure
        self.display_info(f"데이터 구조: {type(data)}", "디버그 정보")
        if hasattr(data, "__dict__"):
            for key, value in data.__dict__.items():
                self.console.print(f"{key}: {value}")


class SectorDataFormatter(DisplayFormatter):
    """Specialized formatter for sector API responses."""

    def format_sector_data(self, data: Any, api_name: str) -> None:
        """
        Format and display sector data with percentage and index formatting.

        Args:
            data: API response data
            api_name: Name of the API for context
        """
        if not data or not hasattr(data, "output") or not data.output:
            self.display_error("조회된 데이터가 없습니다.", "데이터 없음")
            return

        output_data = data.output
        if isinstance(output_data, list) and len(output_data) == 0:
            self.display_error("조회된 데이터가 없습니다.", "데이터 없음")
            return

        # Handle different sector API response formats
        if "투자자" in api_name:
            self._format_investor_sector_data(output_data, api_name)
        elif "지수" in api_name:
            self._format_index_data(output_data, api_name)
        elif "현재가" in api_name:
            self._format_sector_price_data(output_data, api_name)
        else:
            self._format_generic_sector_data(output_data, api_name)

    def _format_investor_sector_data(self, data: Any, title: str) -> None:
        """Format sector investor data."""
        headers = ["업종명", "개인순매수", "외국인순매수", "기관순매수", "등락률", "거래대금"]
        rows = []

        items = data if isinstance(data, list) else [data]

        for item in items:
            try:
                sector_name = getattr(item, "bstp_kor_isnm", getattr(item, "upjong_nm", "-"))
                individual_net = getattr(item, "indv_ntby_tr_pbmn", "0")
                foreign_net = getattr(item, "frgn_ntby_tr_pbmn", "0")
                institution_net = getattr(item, "inst_ntby_tr_pbmn", "0")
                change_rate = getattr(item, "bstp_prdy_ctrt", getattr(item, "ctrt", "0"))
                trading_value = getattr(item, "tot_tr_pbmn", "0")

                rows.append(
                    [
                        sector_name,
                        self.format_number(individual_net, "volume"),
                        self.format_number(foreign_net, "volume"),
                        self.format_number(institution_net, "volume"),
                        self.format_number(change_rate, "percentage"),
                        self.format_number(trading_value, "volume"),
                    ]
                )
            except Exception:
                continue

        if rows:
            self.display_table(headers, rows, f"👥 {title}")
        else:
            self.display_error("데이터 형식을 인식할 수 없습니다.", "형식 오류")

    def _format_index_data(self, data: Any, title: str) -> None:
        """Format sector index data."""
        headers = ["업종명", "현재지수", "전일대비", "등락률", "거래량", "거래대금"]
        rows = []

        items = data if isinstance(data, list) else [data]

        for item in items:
            try:
                sector_name = getattr(item, "bstp_kor_isnm", getattr(item, "upjong_nm", "-"))
                current_index = getattr(item, "bstp_nmix_prpr", getattr(item, "idx_prpr", "0"))
                change_value = getattr(item, "bstp_nmix_prdy_vrss", getattr(item, "prdy_vrss", "0"))
                change_rate = getattr(item, "bstp_nmix_prdy_ctrt", getattr(item, "prdy_ctrt", "0"))
                volume = getattr(item, "acml_vol", "0")
                trading_value = getattr(item, "acml_tr_pbmn", "0")

                rows.append(
                    [
                        sector_name,
                        self.format_number(current_index, "price"),
                        self.format_number(change_value, "price"),
                        self.format_number(change_rate, "percentage"),
                        self.format_number(volume, "volume"),
                        self.format_number(trading_value, "volume"),
                    ]
                )
            except Exception:
                continue

        if rows:
            self.display_table(headers, rows, f"📊 {title}")
        else:
            self.display_error("데이터 형식을 인식할 수 없습니다.", "형식 오류")

    def _format_sector_price_data(self, data: Any, title: str) -> None:
        """Format sector price data."""
        headers = ["업종명", "현재가", "시가", "고가", "저가", "등락률", "거래량"]
        rows = []

        items = data if isinstance(data, list) else [data]

        for item in items:
            try:
                sector_name = getattr(item, "bstp_kor_isnm", getattr(item, "upjong_nm", "-"))
                current_price = getattr(item, "bstp_nmix_prpr", getattr(item, "prpr", "0"))
                open_price = getattr(item, "bstp_nmix_oprc", getattr(item, "oprc", "0"))
                high_price = getattr(item, "bstp_nmix_hgpr", getattr(item, "hgpr", "0"))
                low_price = getattr(item, "bstp_nmix_lwpr", getattr(item, "lwpr", "0"))
                change_rate = getattr(item, "bstp_nmix_prdy_ctrt", getattr(item, "prdy_ctrt", "0"))
                volume = getattr(item, "acml_vol", "0")

                rows.append(
                    [
                        sector_name,
                        self.format_number(current_price, "price"),
                        self.format_number(open_price, "price"),
                        self.format_number(high_price, "price"),
                        self.format_number(low_price, "price"),
                        self.format_number(change_rate, "percentage"),
                        self.format_number(volume, "volume"),
                    ]
                )
            except Exception:
                continue

        if rows:
            self.display_table(headers, rows, f"💹 {title}")
        else:
            self.display_error("데이터 형식을 인식할 수 없습니다.", "형식 오류")

    def _format_generic_sector_data(self, data: Any, title: str) -> None:
        """Format generic sector data when specific format is unknown."""
        if isinstance(data, list) and len(data) > 0:
            first_item = data[0]
            if hasattr(first_item, "__dict__"):
                attrs = [attr for attr in dir(first_item) if not attr.startswith("_")]
                if attrs:
                    headers = attrs[:7]  # Limit to 7 columns
                    rows = []

                    for item in data[:15]:  # Show top 15
                        row = []
                        for attr in attrs[:7]:
                            value = getattr(item, attr, "-")
                            if isinstance(value, (int, float)) and any(x in attr for x in ["prpr", "idx"]):
                                row.append(self.format_number(value, "price"))
                            elif isinstance(value, (int, float)) and "vol" in attr:
                                row.append(self.format_number(value, "volume"))
                            elif isinstance(value, (int, float)) and "ctrt" in attr:
                                row.append(self.format_number(value, "percentage"))
                            else:
                                row.append(str(value))
                        rows.append(row)

                    self.display_table(headers, rows, f"🏢 {title}")
                    return

        self.display_info(f"데이터 구조: {type(data)}", "디버그 정보")


class StockDataFormatter(DisplayFormatter):
    """Specialized formatter for stock information API responses."""

    def format_stock_data(self, data: Any, api_name: str) -> None:
        """
        Format and display stock information with detailed metrics.

        Args:
            data: API response data
            api_name: Name of the API for context
        """
        if not data or not hasattr(data, "output") or not data.output:
            self.display_error("조회된 데이터가 없습니다.", "데이터 없음")
            return

        output_data = data.output
        if isinstance(output_data, list) and len(output_data) == 0:
            self.display_error("조회된 데이터가 없습니다.", "데이터 없음")
            return

        # Handle different stock API response formats
        if "거래량갱신" in api_name:
            self._format_volume_renewal_data(output_data, api_name)
        elif "매물대집중" in api_name:
            self._format_sales_concentration_data(output_data, api_name)
        elif "거래원" in api_name:
            self._format_broker_analysis_data(output_data, api_name)
        elif "투자자" in api_name:
            self._format_investor_totals_data(output_data, api_name)
        else:
            self._format_generic_stock_data(output_data, api_name)

    def _format_volume_renewal_data(self, data: Any, title: str) -> None:
        """Format volume renewal data."""
        headers = ["시간", "현재가", "전일대비", "등락률", "거래량", "누적거래량"]
        rows = []

        items = data if isinstance(data, list) else [data]

        for item in items:
            try:
                time_info = getattr(item, "stck_cntg_hour", getattr(item, "hour", "-"))
                current_price = getattr(item, "stck_prpr", getattr(item, "prpr", "0"))
                change_value = getattr(item, "prdy_vrss", "0")
                change_rate = getattr(item, "prdy_ctrt", "0")
                volume = getattr(item, "cntg_vol", getattr(item, "vol", "0"))
                cumulative_vol = getattr(item, "acml_vol", "0")

                rows.append(
                    [
                        time_info,
                        self.format_number(current_price, "price"),
                        self.format_number(change_value, "price"),
                        self.format_number(change_rate, "percentage"),
                        self.format_number(volume, "volume"),
                        self.format_number(cumulative_vol, "volume"),
                    ]
                )
            except Exception:
                continue

        if rows:
            self.display_table(headers, rows, f"🔄 {title}")
        else:
            self.display_error("데이터 형식을 인식할 수 없습니다.", "형식 오류")

    def _format_sales_concentration_data(self, data: Any, title: str) -> None:
        """Format sales concentration analysis data."""
        headers = ["가격대", "매도잔량", "매수잔량", "총잔량", "비율"]
        rows = []

        items = data if isinstance(data, list) else [data]

        for item in items:
            try:
                price_level = getattr(item, "askp_rsqn", getattr(item, "price", "-"))
                sell_qty = getattr(item, "askp_rsqn_qty", "0")
                buy_qty = getattr(item, "bidp_rsqn_qty", "0")
                total_qty = int(sell_qty) + int(buy_qty) if sell_qty.isdigit() and buy_qty.isdigit() else 0
                ratio = getattr(item, "rsqn_rate", "0")

                rows.append(
                    [
                        self.format_number(price_level, "price"),
                        self.format_number(sell_qty, "volume"),
                        self.format_number(buy_qty, "volume"),
                        self.format_number(total_qty, "volume"),
                        self.format_number(ratio, "percentage"),
                    ]
                )
            except Exception:
                continue

        if rows:
            self.display_table(headers, rows, f"📊 {title}")
        else:
            self.display_error("데이터 형식을 인식할 수 없습니다.", "형식 오류")

    def _format_broker_analysis_data(self, data: Any, title: str) -> None:
        """Format broker order book analysis data."""
        headers = ["거래원명", "매도량", "매수량", "순매수량", "비율"]
        rows = []

        items = data if isinstance(data, list) else [data]

        for item in items:
            try:
                broker_name = getattr(item, "mbcr_name", getattr(item, "broker_nm", "-"))
                sell_qty = getattr(item, "seln_qty", "0")
                buy_qty = getattr(item, "shnu_qty", "0")
                net_qty = int(buy_qty) - int(sell_qty) if buy_qty.isdigit() and sell_qty.isdigit() else 0
                ratio = getattr(item, "ntby_qty_rate", "0")

                rows.append(
                    [
                        broker_name,
                        self.format_number(sell_qty, "volume"),
                        self.format_number(buy_qty, "volume"),
                        self.format_number(net_qty, "volume"),
                        self.format_number(ratio, "percentage"),
                    ]
                )
            except Exception:
                continue

        if rows:
            self.display_table(headers, rows, f"🏦 {title}")
        else:
            self.display_error("데이터 형식을 인식할 수 없습니다.", "형식 오류")

    def _format_investor_totals_data(self, data: Any, title: str) -> None:
        """Format investor and institutional totals data."""
        headers = ["투자자구분", "매도량", "매수량", "순매수량", "비율"]
        rows = []

        items = data if isinstance(data, list) else [data]

        for item in items:
            try:
                investor_type = getattr(item, "invst_tp_nm", getattr(item, "tp_nm", "-"))
                sell_qty = getattr(item, "seln_qty", "0")
                buy_qty = getattr(item, "shnu_qty", "0")
                net_qty = int(buy_qty) - int(sell_qty) if buy_qty.isdigit() and sell_qty.isdigit() else 0
                ratio = getattr(item, "ntby_qty_rate", "0")

                rows.append(
                    [
                        investor_type,
                        self.format_number(sell_qty, "volume"),
                        self.format_number(buy_qty, "volume"),
                        self.format_number(net_qty, "volume"),
                        self.format_number(ratio, "percentage"),
                    ]
                )
            except Exception:
                continue

        if rows:
            self.display_table(headers, rows, f"👤 {title}")
        else:
            self.display_error("데이터 형식을 인식할 수 없습니다.", "형식 오류")

    def _format_generic_stock_data(self, data: Any, title: str) -> None:
        """Format generic stock data when specific format is unknown."""
        if isinstance(data, list) and len(data) > 0:
            first_item = data[0]
            if hasattr(first_item, "__dict__"):
                attrs = [attr for attr in dir(first_item) if not attr.startswith("_")]
                if attrs:
                    headers = attrs[:7]  # Limit to 7 columns
                    rows = []

                    for item in data[:15]:  # Show top 15
                        row = []
                        for attr in attrs[:7]:
                            value = getattr(item, attr, "-")
                            if isinstance(value, (int, float)) and any(x in attr for x in ["prpr", "price"]):
                                row.append(self.format_number(value, "price"))
                            elif isinstance(value, (int, float)) and "vol" in attr:
                                row.append(self.format_number(value, "volume"))
                            elif isinstance(value, (int, float)) and "ctrt" in attr:
                                row.append(self.format_number(value, "percentage"))
                            else:
                                row.append(str(value))
                        rows.append(row)

                    self.display_table(headers, rows, f"📈 {title}")
                    return

        self.display_info(f"데이터 구조: {type(data)}", "디버그 정보")
