"""
Sector information module for stock inquiry.

This module handles all sector-related APIs (업종) including sector performance,
investor activity by sector, and sector indices.
"""

from datetime import datetime
from typing import Any, Dict, Optional

import inquirer
from cluefin_openapi.kiwoom import Client
from rich.console import Console

from .display_formatter import DisplayFormatter
from .parameter_collector import ParameterCollector

console = Console()


class SectorInfoHandler:
    def __init__(self):
        self.client = None
        self.parameter_collector = ParameterCollector()
        self.display_formatter = DisplayFormatter()

    def _ensure_client(self):
        """클라이언트가 초기화되었는지 확인합니다."""
        console.print("[yellow]API 클라이언트를 초기화하는 중...[/yellow]")
        console.print("[yellow]실제 구현에서는 키움증권 API 토큰이 필요합니다.[/yellow]")
        console.print("[red]데모 모드: API 호출이 구현되지 않았습니다.[/red]")

    def handle_sector_menu(self):
        """업종정보 메뉴를 처리합니다."""
        while True:
            console.print("\n[bold blue]🏢 업종정보 메뉴[/bold blue]")

            questions = [
                inquirer.List(
                    "sector_choice",
                    message="조회할 업종정보를 선택하세요",
                    choices=[
                        ("📊 업종별 투자자 순매수 요청", "sector_investor_net_buy"),
                        ("💰 업종현재가 요청", "sector_current_price"),
                        ("📈 업종별 주가요청", "sector_price_by_sector"),
                        ("🌐 전업종 지수요청", "all_sector_index"),
                        ("📅 업종현재가 일별요청", "daily_sector_current_price"),
                        ("⬅️ 메인메뉴로 돌아가기", "back"),
                    ],
                ),
            ]

            answers = inquirer.prompt(questions)
            if not answers or answers["sector_choice"] == "back":
                break

            choice = answers["sector_choice"]

            try:
                self._ensure_client()

                if choice == "sector_investor_net_buy":
                    self._handle_sector_investor_net_buy()
                elif choice == "sector_current_price":
                    self._handle_sector_current_price()
                elif choice == "sector_price_by_sector":
                    self._handle_sector_price_by_sector()
                elif choice == "all_sector_index":
                    self._handle_all_sector_index()
                elif choice == "daily_sector_current_price":
                    self._handle_daily_sector_current_price()

            except Exception as e:
                console.print(f"[red]오류 발생: {str(e)}[/red]")
                console.print("[yellow]계속하려면 엔터를 누르세요...[/yellow]")
                input()

    def _handle_sector_investor_net_buy(self):
        """업종별 투자자 순매수 요청을 처리합니다."""
        console.print("[cyan]업종별 투자자 순매수 요청 - 파라미터 입력[/cyan]")

        params = self._collect_sector_investor_net_buy_params()
        if not params:
            return

        console.print("[yellow]API 호출이 구현되면 실제 데이터가 표시됩니다.[/yellow]")
        console.print(f"[dim]입력된 파라미터: {params}[/dim]")

    def _handle_sector_current_price(self):
        """업종현재가 요청을 처리합니다."""
        console.print("[cyan]업종현재가 요청 - 파라미터 입력[/cyan]")

        params = self._collect_sector_current_price_params()
        if not params:
            return

        console.print("[yellow]API 호출이 구현되면 실제 데이터가 표시됩니다.[/yellow]")
        console.print(f"[dim]입력된 파라미터: {params}[/dim]")

    def _handle_sector_price_by_sector(self):
        """업종별 주가요청을 처리합니다."""
        console.print("[cyan]업종별 주가요청 - 파라미터 입력[/cyan]")

        params = self._collect_sector_price_by_sector_params()
        if not params:
            return

        console.print("[yellow]API 호출이 구현되면 실제 데이터가 표시됩니다.[/yellow]")
        console.print(f"[dim]입력된 파라미터: {params}[/dim]")

    def _handle_all_sector_index(self):
        """전업종 지수요청을 처리합니다."""
        console.print("[cyan]전업종 지수요청 - 파라미터 입력[/cyan]")

        params = self._collect_all_sector_index_params()
        if not params:
            return

        console.print("[yellow]API 호출이 구현되면 실제 데이터가 표시됩니다.[/yellow]")
        console.print(f"[dim]입력된 파라미터: {params}[/dim]")

    def _handle_daily_sector_current_price(self):
        """업종현재가 일별요청을 처리합니다."""
        console.print("[cyan]업종현재가 일별요청 - 파라미터 입력[/cyan]")

        params = self._collect_daily_sector_current_price_params()
        if not params:
            return

        console.print("[yellow]API 호출이 구현되면 실제 데이터가 표시됩니다.[/yellow]")
        console.print(f"[dim]입력된 파라미터: {params}[/dim]")

    def _collect_sector_investor_net_buy_params(self) -> Optional[Dict[str, Any]]:
        """업종별 투자자 순매수 파라미터를 수집합니다."""
        questions = [
            inquirer.List(
                "mrkt_tp",
                message="시장구분을 선택하세요",
                choices=[("코스피", "0"), ("코스닥", "1")],
            ),
            inquirer.List(
                "amt_qty_tp",
                message="금액수량구분을 선택하세요",
                choices=[("금액", "0"), ("수량", "1")],
            ),
            inquirer.Text(
                "base_dt", message="기준일자를 입력하세요 (YYYYMMDD)", default=datetime.now().strftime("%Y%m%d")
            ),
            inquirer.List(
                "stex_tp",
                message="거래소구분을 선택하세요",
                choices=[("KRX", "1"), ("NXT", "2"), ("통합", "3")],
            ),
        ]

        answers = inquirer.prompt(questions)
        return answers

    def _collect_sector_current_price_params(self) -> Optional[Dict[str, Any]]:
        """업종현재가 파라미터를 수집합니다."""
        questions = [
            inquirer.List(
                "mrkt_tp",
                message="시장구분을 선택하세요",
                choices=[("코스피", "0"), ("코스닥", "1"), ("코스피200", "2")],
            ),
            inquirer.Text(
                "inds_cd", message="업종코드를 입력하세요 (예: 001:종합, 002:대형주, 003:중형주)", default="001"
            ),
        ]

        answers = inquirer.prompt(questions)
        return answers

    def _collect_sector_price_by_sector_params(self) -> Optional[Dict[str, Any]]:
        """업종별 주가 파라미터를 수집합니다."""
        questions = [
            inquirer.List(
                "mrkt_tp",
                message="시장구분을 선택하세요",
                choices=[("코스피", "0"), ("코스닥", "1"), ("코스피200", "2")],
            ),
            inquirer.Text(
                "inds_cd", message="업종코드를 입력하세요 (예: 001:종합, 002:대형주, 003:중형주)", default="001"
            ),
            inquirer.List(
                "stex_tp",
                message="거래소구분을 선택하세요",
                choices=[("KRX", "1"), ("NXT", "2"), ("통합", "3")],
            ),
        ]

        answers = inquirer.prompt(questions)
        return answers

    def _collect_all_sector_index_params(self) -> Optional[Dict[str, Any]]:
        """전업종 지수 파라미터를 수집합니다."""
        questions = [
            inquirer.Text(
                "inds_cd",
                message="업종코드를 입력하세요 (001:종합(KOSPI), 101:종합(KOSDAQ), 201:KOSPI200)",
                default="001",
            ),
        ]

        answers = inquirer.prompt(questions)
        return answers

    def _collect_daily_sector_current_price_params(self) -> Optional[Dict[str, Any]]:
        """업종현재가 일별 파라미터를 수집합니다."""
        questions = [
            inquirer.List(
                "mrkt_tp",
                message="시장구분을 선택하세요",
                choices=[("코스피", "0"), ("코스닥", "1"), ("코스피200", "2")],
            ),
            inquirer.Text(
                "inds_cd", message="업종코드를 입력하세요 (예: 001:종합, 002:대형주, 003:중형주)", default="001"
            ),
        ]

        answers = inquirer.prompt(questions)
        return answers
