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
            try:
                console.print("\n[bold green]─" * 60 + "[/bold green]")
                console.print("[bold cyan]📊 Cluefin 주식 조회 시스템 📊[/bold cyan]")
                console.print("[bold green]─" * 60 + "[/bold green]")
                console.print("[dim]한국 금융시장 데이터를 조회할 수 있습니다.[/dim]")
                console.print("[dim]팁: Ctrl+C로 언제든지 종료할 수 있습니다.[/dim]\n")

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
                    console.print("[yellow]사용자에 의해 종료되었습니다.[/yellow]")
                    break

                choice = answers.get("main_choice")
                if not choice:
                    console.print("[red]잘못된 선택입니다. 다시 시도해주세요.[/red]")
                    continue

                if choice == "ranking":
                    self._handle_module_execution(self.ranking_module, "순위정보")
                elif choice == "sector":
                    self._handle_module_execution(self.sector_module, "업종정보")
                elif choice == "stock":
                    self._handle_module_execution(self.stock_module, "종목정보")
                elif choice == "exit":
                    console.print("[yellow]프로그램을 종료합니다.[/yellow]")
                    break
                else:
                    console.print(f"[red]알 수 없는 선택: {choice}[/red]")

            except KeyboardInterrupt:
                console.print("\n[yellow]프로그램을 종료합니다.[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]메뉴 실행 중 오류가 발생했습니다: {str(e)}[/red]")
                console.print("[dim]엔터를 눌러 계속하거나 Ctrl+C로 종료하세요.[/dim]")
                input()

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

    def _handle_module_execution(self, module, module_name: str) -> None:
        """
        Handle execution of a specific module with error recovery.

        Args:
            module: The API module to execute
            module_name: Korean name of the module for error messages
        """
        try:
            module.handle_menu_loop()
        except KeyboardInterrupt:
            console.print(f"\n[yellow]{module_name} 메뉴에서 나갔습니다.[/yellow]")
        except Exception as e:
            console.print(f"[red]{module_name} 실행 중 오류가 발생했습니다: {str(e)}[/red]")
            console.print("[dim]메인 메뉴로 돌아갑니다.[/dim]")
            console.print("[dim]엔터를 눌러 계속하세요.[/dim]")
            input()
