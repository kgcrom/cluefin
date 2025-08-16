"""
Menu controller for interactive navigation in the stock inquiry system.

This module handles the main menu display and navigation logic for the inquiry feature.
"""

import inquirer
from rich.console import Console

from .ranking_info import RankingInfoHandler
from .sector_info import SectorInfoHandler
from .stock_info import StockInfoHandler

console = Console()


class MenuController:
    def __init__(self):
        self.ranking_handler = RankingInfoHandler()
        self.sector_handler = SectorInfoHandler()
        self.stock_handler = StockInfoHandler()

    def run_main_menu(self):
        """메인 메뉴를 실행합니다."""
        while True:
            console.print("\n[bold green]─" * 50 + "[/bold green]")
            console.print("[bold cyan]📊 메인 메뉴 📊[/bold cyan]")
            console.print("[bold green]─" * 50 + "[/bold green]")

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
                self.ranking_handler.handle_ranking_menu()
            elif choice == "sector":
                self.sector_handler.handle_sector_menu()
            elif choice == "stock":
                self.stock_handler.handle_stock_menu()
            elif choice == "exit":
                console.print("[yellow]프로그램을 종료합니다.[/yellow]")
                break
