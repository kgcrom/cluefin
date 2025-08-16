import click
from rich.console import Console

from cluefin_cli.commands.analyze import analyze
from cluefin_cli.commands.inquiry import inquiry

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="cluefin-cli")
def cli():
    """Korean financial investment CLI toolkit with technical analysis and AI insights."""
    console.print("[bold blue]Cluefin CLI - Korean Stock Analysis Tool[/bold blue]")
    console.print("Use --help to see available commands")


cli.add_command(analyze)
cli.add_command(inquiry)


if __name__ == "__main__":
    cli()
