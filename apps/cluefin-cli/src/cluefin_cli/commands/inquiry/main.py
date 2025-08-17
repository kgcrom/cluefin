"""
Main entry point for the stock inquiry command.

This module provides the main CLI command for interactive stock inquiry functionality.
"""

import click
from cluefin_openapi.kiwoom import Client as KiwoomClient
from cluefin_openapi.kiwoom._auth import Auth as KiwoomAuth
from pydantic import SecretStr
from rich.console import Console
from rich.panel import Panel

from cluefin_cli.config.settings import settings

from .menu_controller import MenuController

console = Console()


def _create_kiwoom_client() -> KiwoomClient:
    """
    Initialize and return a Kiwoom API client using environment variables.

    Returns:
        KiwoomClient: Configured Kiwoom API client

    Raises:
        ValueError: If required environment variables are missing
    """
    if not settings.kiwoom_app_key:
        raise ValueError("KIWOOM_APP_KEY environment variable is required") from None
    if not settings.kiwoom_secret_key:
        raise ValueError("KIWOOM_SECRET_KEY environment variable is required") from None

    try:
        auth = KiwoomAuth(
            app_key=settings.kiwoom_app_key,
            secret_key=SecretStr(settings.kiwoom_secret_key),
            env="dev",
        )
        token = auth.generate_token()
        client = KiwoomClient(
            token=token.get_token(),
            env="dev",
        )
        return client
    except Exception as e:
        raise ValueError(f"Failed to initialize Kiwoom client: {str(e)}") from e


@click.command()
@click.pass_context
def inquiry(ctx, mock: bool):
    """
    Interactive stock inquiry tool for Korean financial markets.

    Explore Korean stock market data through an intuitive menu-driven interface.
    Access ranking information, sector analysis, and detailed stock information
    using Kiwoom Securities APIs.

    \b
    Features:
    • 순위정보: Trading volume rankings, foreign investor activity
    • 업종정보: Sector performance and investor flows
    • 종목정보: Individual stock analysis and metrics

    \b
    Requirements:
    • KIWOOM_APP_KEY: Your Kiwoom Securities API key
    • KIWOOM_SECRET_KEY: Your Kiwoom Securities secret key

    \b
    Examples:
    cluefin inquiry           # Start interactive inquiry session
    cluefin inquiry --mock    # Run in mock mode for testing
    """
    # Display welcome message
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]📊 Cluefin 주식 조회 시스템 📊[/bold cyan]\n[dim]한국 금융시장 실시간 데이터 조회 도구[/dim]",
            border_style="blue",
        )
    )

    if mock:
        console.print("[yellow]🧪 Mock mode enabled - No API calls will be made[/yellow]\n")

    try:
        # Initialize Kiwoom client (unless in mock mode)
        client = None
        if not mock:
            console.print("[yellow]🔌 Kiwoom API 클라이언트를 초기화하는 중...[/yellow]")
            client = _create_kiwoom_client()
            console.print("[green]✅ API 클라이언트 초기화 완료[/green]\n")

        # Initialize and run menu controller
        menu_controller = MenuController(client)
        menu_controller.run_main_menu()

    except ValueError as e:
        console.print(f"[red]❌ 설정 오류: {str(e)}[/red]")
        console.print("\n[dim]환경 변수를 확인하고 다시 시도해주세요.[/dim]")
        console.print("[dim]필요한 환경 변수:[/dim]")
        console.print("[dim]  • KIWOOM_APP_KEY[/dim]")
        console.print("[dim]  • KIWOOM_SECRET_KEY[/dim]")
        ctx.exit(1)

    except KeyboardInterrupt:
        console.print("\n[yellow]👋 프로그램을 종료합니다.[/yellow]")

    except Exception as e:
        console.print(f"[red]❌ 예상치 못한 오류가 발생했습니다: {str(e)}[/red]")
        console.print("[dim]문제가 지속되면 개발팀에 문의해주세요.[/dim]")
        ctx.exit(1)
