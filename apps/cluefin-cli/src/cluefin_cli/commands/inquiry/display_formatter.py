"""
Display formatting system for API responses.

This module handles formatting and displaying API responses in readable table format
with proper Korean text support.
"""

from typing import Any

from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()


class DisplayFormatter:
    def display_volume_surge_results(self, response_body: Any):
        """거래량급증요청 결과를 표시합니다."""
        console.print("\n[bold green]🚀 거래량급증 상위종목[/bold green]")

        table = Table(show_header=True, header_style="bold magenta", show_lines=True)
        table.add_column("순위", style="cyan", width=6)
        table.add_column("종목코드", style="blue", width=8)
        table.add_column("종목명", style="white", width=12)
        table.add_column("현재가", style="yellow", width=10, justify="right")
        table.add_column("등락률", style="red", width=8, justify="right")
        table.add_column("거래량", style="green", width=12, justify="right")
        table.add_column("급증률", style="bright_red", width=8, justify="right")

        for i, item in enumerate(response_body.output1[:20], 1):  # 상위 20개만 표시
            table.add_row(
                str(i),
                getattr(item, "stk_cd", ""),
                getattr(item, "stk_nm", ""),
                f"{int(getattr(item, 'stk_prpr', 0)):,}",
                f"{float(getattr(item, 'prdyVrss_prpr_sgn', 0)):+.2f}%",
                f"{int(getattr(item, 'acml_tr_pbmn', 0)):,}",
                f"{float(getattr(item, 'prdy_tr_pbmn_rate', 0)):+.2f}%",
            )

        console.print(table)
        console.print(f"\n[dim]총 {len(response_body.output1)}개 종목 조회됨[/dim]")

    def display_current_day_volume_results(self, response_body: Any):
        """당일거래량상위요청 결과를 표시합니다."""
        console.print("\n[bold green]📊 당일거래량 상위종목[/bold green]")

        table = Table(show_header=True, header_style="bold magenta", show_lines=True)
        table.add_column("순위", style="cyan", width=6)
        table.add_column("종목코드", style="blue", width=8)
        table.add_column("종목명", style="white", width=12)
        table.add_column("현재가", style="yellow", width=10, justify="right")
        table.add_column("등락률", style="red", width=8, justify="right")
        table.add_column("거래량", style="green", width=12, justify="right")
        table.add_column("거래대금", style="bright_green", width=15, justify="right")

        for i, item in enumerate(response_body.output1[:20], 1):
            table.add_row(
                str(i),
                getattr(item, "stk_cd", ""),
                getattr(item, "stk_nm", ""),
                f"{int(getattr(item, 'stk_prpr', 0)):,}",
                f"{float(getattr(item, 'prdy_vrss_sign', 0)):+.2f}%",
                f"{int(getattr(item, 'acml_tr_pbmn', 0)):,}",
                f"{int(getattr(item, 'acml_tr_pbmn_prc', 0)):,}",
            )

        console.print(table)
        console.print(f"\n[dim]총 {len(response_body.output1)}개 종목 조회됨[/dim]")

    def display_previous_day_volume_results(self, response_body: Any):
        """전일거래량상위요청 결과를 표시합니다."""
        console.print("\n[bold green]📉 전일거래량 상위종목[/bold green]")

        table = Table(show_header=True, header_style="bold magenta", show_lines=True)
        table.add_column("순위", style="cyan", width=6)
        table.add_column("종목코드", style="blue", width=8)
        table.add_column("종목명", style="white", width=12)
        table.add_column("현재가", style="yellow", width=10, justify="right")
        table.add_column("등락률", style="red", width=8, justify="right")
        table.add_column("전일거래량", style="green", width=12, justify="right")
        table.add_column("전일거래대금", style="bright_green", width=15, justify="right")

        for item in response_body.output1:
            table.add_row(
                getattr(item, "rank", ""),
                getattr(item, "stk_cd", ""),
                getattr(item, "stk_nm", ""),
                f"{int(getattr(item, 'stk_prpr', 0)):,}",
                f"{float(getattr(item, 'prdy_vrss_sign', 0)):+.2f}%",
                f"{int(getattr(item, 'prdy_tr_pbmn', 0)):,}",
                f"{int(getattr(item, 'prdy_tr_pbmn_prc', 0)):,}",
            )

        console.print(table)
        console.print(f"\n[dim]총 {len(response_body.output1)}개 종목 조회됨[/dim]")

    def display_transaction_value_results(self, response_body: Any):
        """거래대금상위요청 결과를 표시합니다."""
        console.print("\n[bold green]💵 거래대금 상위종목[/bold green]")

        table = Table(show_header=True, header_style="bold magenta", show_lines=True)
        table.add_column("순위", style="cyan", width=6)
        table.add_column("종목코드", style="blue", width=8)
        table.add_column("종목명", style="white", width=12)
        table.add_column("현재가", style="yellow", width=10, justify="right")
        table.add_column("등락률", style="red", width=8, justify="right")
        table.add_column("거래량", style="green", width=12, justify="right")
        table.add_column("거래대금", style="bright_green", width=15, justify="right")

        for i, item in enumerate(response_body.output1[:20], 1):
            table.add_row(
                str(i),
                getattr(item, "stk_cd", ""),
                getattr(item, "stk_nm", ""),
                f"{int(getattr(item, 'stk_prpr', 0)):,}",
                f"{float(getattr(item, 'prdy_vrss_sign', 0)):+.2f}%",
                f"{int(getattr(item, 'acml_tr_pbmn', 0)):,}",
                f"{int(getattr(item, 'acml_tr_pbmn_prc', 0)):,}",
            )

        console.print(table)
        console.print(f"\n[dim]총 {len(response_body.output1)}개 종목 조회됨[/dim]")

    def display_foreign_period_trading_results(self, response_body: Any):
        """외인기간별매매상위요청 결과를 표시합니다."""
        console.print("\n[bold green]🌍 외국인 기간별매매 상위종목[/bold green]")

        table = Table(show_header=True, header_style="bold magenta", show_lines=True)
        table.add_column("순위", style="cyan", width=6)
        table.add_column("종목코드", style="blue", width=8)
        table.add_column("종목명", style="white", width=12)
        table.add_column("현재가", style="yellow", width=10, justify="right")
        table.add_column("등락률", style="red", width=8, justify="right")
        table.add_column("외국인순매수", style="bright_blue", width=12, justify="right")
        table.add_column("순매수금액", style="bright_green", width=15, justify="right")

        for i, item in enumerate(response_body.output1[:20], 1):
            table.add_row(
                str(i),
                getattr(item, "stk_cd", ""),
                getattr(item, "stk_nm", ""),
                f"{int(getattr(item, 'stk_prpr', 0)):,}",
                f"{float(getattr(item, 'prdy_vrss_sign', 0)):+.2f}%",
                f"{int(getattr(item, 'frgn_ntby_qty', 0)):,}",
                f"{int(getattr(item, 'frgn_ntby_tr_pbmn', 0)):,}",
            )

        console.print(table)
        console.print(f"\n[dim]총 {len(response_body.output1)}개 종목 조회됨[/dim]")

    def display_foreign_consecutive_trading_results(self, response_body: Any):
        """외인연속순매매상위요청 결과를 표시합니다."""
        console.print("\n[bold green]🔄 외국인 연속순매매 상위종목[/bold green]")

        table = Table(show_header=True, header_style="bold magenta", show_lines=True)
        table.add_column("순위", style="cyan", width=6)
        table.add_column("종목코드", style="blue", width=8)
        table.add_column("종목명", style="white", width=12)
        table.add_column("현재가", style="yellow", width=10, justify="right")
        table.add_column("등락률", style="red", width=8, justify="right")
        table.add_column("연속일수", style="bright_cyan", width=10, justify="right")
        table.add_column("순매수량", style="bright_blue", width=12, justify="right")

        for i, item in enumerate(response_body.output1[:20], 1):
            table.add_row(
                str(i),
                getattr(item, "stk_cd", ""),
                getattr(item, "stk_nm", ""),
                f"{int(getattr(item, 'stk_prpr', 0)):,}",
                f"{float(getattr(item, 'prdy_vrss_sign', 0)):+.2f}%",
                f"{int(getattr(item, 'cont_day_yn', 0))}일",
                f"{int(getattr(item, 'frgn_ntby_qty', 0)):,}",
            )

        console.print(table)
        console.print(f"\n[dim]총 {len(response_body.output1)}개 종목 조회됨[/dim]")

    def display_foreign_institutional_trading_results(self, response_body: Any):
        """외국인기관매매상위요청 결과를 표시합니다."""
        console.print("\n[bold green]🏛️ 외국인기관매매 상위종목[/bold green]")

        table = Table(show_header=True, header_style="bold magenta", show_lines=True)
        table.add_column("순위", style="cyan", width=6)
        table.add_column("종목코드", style="blue", width=8)
        table.add_column("종목명", style="white", width=12)
        table.add_column("현재가", style="yellow", width=10, justify="right")
        table.add_column("등락률", style="red", width=8, justify="right")
        table.add_column("외국인순매수", style="bright_blue", width=12, justify="right")
        table.add_column("기관순매수", style="bright_magenta", width=12, justify="right")

        for i, item in enumerate(response_body.output1[:20], 1):
            table.add_row(
                str(i),
                getattr(item, "stk_cd", ""),
                getattr(item, "stk_nm", ""),
                f"{int(getattr(item, 'stk_prpr', 0)):,}",
                f"{float(getattr(item, 'prdy_vrss_sign', 0)):+.2f}%",
                f"{int(getattr(item, 'frgn_ntby_qty', 0)):,}",
                f"{int(getattr(item, 'orgn_ntby_qty', 0)):,}",
            )

        console.print(table)
        console.print(f"\n[dim]총 {len(response_body.output1)}개 종목 조회됨[/dim]")

    def _format_number(self, value: Any) -> str:
        """숫자를 포맷팅합니다."""
        try:
            return f"{int(value):,}"
        except (ValueError, TypeError):
            return str(value)

    def _format_percentage(self, value: Any) -> str:
        """퍼센티지를 포맷팅합니다."""
        try:
            return f"{float(value):+.2f}%"
        except (ValueError, TypeError):
            return str(value)
