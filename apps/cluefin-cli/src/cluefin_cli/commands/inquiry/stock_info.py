"""
Stock information module for stock inquiry.

This module handles all stock-specific APIs (종목정보) including detailed stock
analysis, volume updates, and broker analysis.
"""

from typing import Any, Dict, Optional

import inquirer
from rich.console import Console

from .display_formatter import DisplayFormatter
from .parameter_collector import ParameterCollector

console = Console()


class StockInfoHandler:
    def __init__(self):
        self.client = None
        self.parameter_collector = ParameterCollector()
        self.display_formatter = DisplayFormatter()

    def _ensure_client(self):
        """클라이언트가 초기화되었는지 확인합니다."""
        console.print("[yellow]API 클라이언트를 초기화하는 중...[/yellow]")
        console.print("[yellow]실제 구현에서는 키움증권 API 토큰이 필요합니다.[/yellow]")
        console.print("[red]데모 모드: API 호출이 구현되지 않았습니다.[/red]")

    def handle_stock_menu(self):
        """종목정보 메뉴를 처리합니다."""
        while True:
            console.print("\n[bold blue]💰 종목정보 메뉴[/bold blue]")

            questions = [
                inquirer.List(
                    "stock_choice",
                    message="조회할 종목정보를 선택하세요",
                    choices=[
                        ("📈 거래량갱신요청", "volume_renewal"),
                        ("💹 매출대집중요청", "supply_demand_concentration"),
                        ("🏢 거래원매물대분석요청", "broker_supply_demand_analysis"),
                        ("👥 종목별투자자기관별합계요청", "stock_investor_institutional_total"),
                        ("⬅️ 메인메뉴로 돌아가기", "back"),
                    ],
                ),
            ]

            answers = inquirer.prompt(questions)
            if not answers or answers["stock_choice"] == "back":
                break

            choice = answers["stock_choice"]

            try:
                self._ensure_client()

                if choice == "volume_renewal":
                    self._handle_volume_renewal()
                elif choice == "supply_demand_concentration":
                    self._handle_supply_demand_concentration()
                elif choice == "broker_supply_demand_analysis":
                    self._handle_broker_supply_demand_analysis()
                elif choice == "stock_investor_institutional_total":
                    self._handle_stock_investor_institutional_total()

            except Exception as e:
                console.print(f"[red]오류 발생: {str(e)}[/red]")
                console.print("[yellow]계속하려면 엔터를 누르세요...[/yellow]")
                input()

    def _handle_volume_renewal(self):
        """거래량갱신요청을 처리합니다."""
        console.print("[cyan]거래량갱신요청 - 파라미터 입력[/cyan]")

        params = self._collect_volume_renewal_params()
        if not params:
            return

        console.print("[yellow]API 호출이 구현되면 실제 데이터가 표시됩니다.[/yellow]")
        console.print(f"[dim]입력된 파라미터: {params}[/dim]")

    def _handle_supply_demand_concentration(self):
        """매출대집중요청을 처리합니다."""
        console.print("[cyan]매출대집중요청 - 파라미터 입력[/cyan]")

        params = self._collect_supply_demand_concentration_params()
        if not params:
            return

        console.print("[yellow]API 호출이 구현되면 실제 데이터가 표시됩니다.[/yellow]")
        console.print(f"[dim]입력된 파라미터: {params}[/dim]")

    def _handle_broker_supply_demand_analysis(self):
        """거래원매물대분석요청을 처리합니다."""
        console.print("[cyan]거래원매물대분석요청 - 파라미터 입력[/cyan]")

        params = self._collect_broker_supply_demand_analysis_params()
        if not params:
            return

        console.print("[yellow]API 호출이 구현되면 실제 데이터가 표시됩니다.[/yellow]")
        console.print(f"[dim]입력된 파라미터: {params}[/dim]")

    def _handle_stock_investor_institutional_total(self):
        """종목별투자자기관별합계요청을 처리합니다."""
        console.print("[cyan]종목별투자자기관별합계요청 - 파라미터 입력[/cyan]")

        params = self._collect_stock_investor_institutional_total_params()
        if not params:
            return

        console.print("[yellow]API 호출이 구현되면 실제 데이터가 표시됩니다.[/yellow]")
        console.print(f"[dim]입력된 파라미터: {params}[/dim]")

    def _collect_volume_renewal_params(self) -> Optional[Dict[str, Any]]:
        """거래량갱신 파라미터를 수집합니다."""
        questions = [
            inquirer.Text("stk_cd", message="종목코드를 입력하세요 (예: 005930)", default="005930"),
        ]

        answers = inquirer.prompt(questions)
        return answers

    def _collect_supply_demand_concentration_params(self) -> Optional[Dict[str, Any]]:
        """매출대집중 파라미터를 수집합니다."""
        questions = [
            inquirer.Text("stk_cd", message="종목코드를 입력하세요 (예: 005930)", default="005930"),
            inquirer.List(
                "prc_tp",
                message="가격구분을 선택하세요",
                choices=[("매도호가", "1"), ("매수호가", "2")],
            ),
        ]

        answers = inquirer.prompt(questions)
        return answers

    def _collect_broker_supply_demand_analysis_params(self) -> Optional[Dict[str, Any]]:
        """거래원매물대분석 파라미터를 수집합니다."""
        questions = [
            inquirer.Text("stk_cd", message="종목코드를 입력하세요 (예: 005930)", default="005930"),
        ]

        answers = inquirer.prompt(questions)
        return answers

    def _collect_stock_investor_institutional_total_params(self) -> Optional[Dict[str, Any]]:
        """종목별투자자기관별합계 파라미터를 수집합니다."""
        questions = [
            inquirer.Text("stk_cd", message="종목코드를 입력하세요 (예: 005930)", default="005930"),
            inquirer.List(
                "trd_dt",
                message="거래일자구분을 선택하세요",
                choices=[("당일", "0"), ("전일", "1")],
            ),
        ]

        answers = inquirer.prompt(questions)
        return answers
