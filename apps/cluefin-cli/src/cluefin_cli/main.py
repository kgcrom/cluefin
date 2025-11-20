import click
from rich.console import Console

from cluefin_cli.commands.fundamental_analysis import fundamental_analysis
from cluefin_cli.commands.import_cmd import import_command
from cluefin_cli.commands.technical_analysis import technical_analysis
from cluefin_cli.config.logging import setup_logging

console = Console()


@click.group()
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.version_option(version="0.1.0", prog_name="cluefin-cli")
def cli(debug: bool):
    """Korean financial investment CLI toolkit with technical analysis and AI insights."""
    setup_logging(debug=debug)
    console.print("[bold blue]Cluefin CLI - Korean Stock Analysis Tool[/bold blue]")
    console.print("Use --help to see available commands")


cli.add_command(technical_analysis)
cli.add_command(fundamental_analysis)
cli.add_command(import_command)


if __name__ == "__main__":
    cli()
