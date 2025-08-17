"""
Menu controller for interactive navigation in the stock inquiry system.

This module handles the main menu display and navigation logic for the inquiry feature.
"""

from typing import Optional

import inquirer
from cluefin_openapi.kiwoom import Client as KiwoomClient
from rich.console import Console

from .ranking_info import RankingInfoModule
from .sector_info import SectorInfoModule
from .stock_info import StockInfoModule

console = Console()


class MenuController:
    def __init__(self, client: Optional[KiwoomClient] = None):
        self.client = client
        self.ranking_module = RankingInfoModule(client)
        self.sector_module = SectorInfoModule(client)
        self.stock_module = StockInfoModule(client)

    def run_main_menu(self):
        """메인 메뉴를 실행합니다."""
        while True:
            console.print("\n[bold green]─" * 60 + "[/bold green]")
            console.print("[bold cyan]📊 Cluefin 주식 조회 시스템 📊[/bold cyan]")
            console.print("[bold green]─" * 60 + "[/bold green]")
            console.print("[dim]한국 금융시장 데이터를 조회할 수 있습니다.[/dim]\n")

            questions = [
                inquirer.List(
                    "main_choice",
                    message="조회할 정보 유형을 선택하세요",
                    choices=[
                        ("📈 순위정보", "ranking"),
                        ("🏢 업종정보", "sector"),
                        ("💰 종목정보", "stock"),
                        ("🚪 종료", "exit"),
                    ],
                ),
            ]

            answers = inquirer.prompt(questions)
            if not answers:
                break

            choice = answers["main_choice"]

            if choice == "ranking":
                self.ranking_module.handle_menu_loop()
            elif choice == "sector":
                self.sector_module.handle_menu_loop()
            elif choice == "stock":
                self.stock_module.handle_menu_loop()
            elif choice == "exit":
                console.print("[yellow]프로그램을 종료합니다.[/yellow]")
                break

    def set_client(self, client: KiwoomClient) -> None:
        """
        Set the Kiwoom API client for all modules.

        Args:
            client: The Kiwoom API client instance
        """
        self.client = client
        self.ranking_module.set_client(client)
        self.sector_module.set_client(client)
        self.stock_module.set_client(client)
