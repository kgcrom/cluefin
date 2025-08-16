"""
Main entry point for the stock inquiry command.

This module provides the main CLI command for interactive stock inquiry functionality.
"""

import click
import inquirer
from rich.console import Console
from rich.text import Text

from .menu_controller import MenuController

console = Console()


@click.command()
@click.pass_context
def inquiry(ctx):
    """Interactive stock inquiry tool for Korean markets."""
    console.print("[bold blue]한국 주식시장 정보 조회 시스템[/bold blue]")
    console.print("키움증권 API를 통한 실시간 시장 정보 조회")
    console.print()

    try:
        menu_controller = MenuController()
        menu_controller.run_main_menu()
    except KeyboardInterrupt:
        console.print("\n[yellow]프로그램을 종료합니다.[/yellow]")
    except Exception as e:
        console.print(f"[red]오류가 발생했습니다: {str(e)}[/red]")
