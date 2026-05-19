import click
from rich.console import Console

from cluefin_cli.commands.fundamental_analysis import fundamental_analysis
from cluefin_cli.commands.news import news_command
from cluefin_cli.commands.statements import statements_command
from cluefin_cli.commands.technical_analysis import technical_analysis
from cluefin_cli.commands.xbrl_analysis import xbrl_analysis
from cluefin_cli.config.logging import setup_logging
from cluefin_cli.output import success_envelope, write_json

console = Console()


@click.group(invoke_without_command=True)
@click.pass_context
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.option("--json", "json_output", is_flag=True, help="Emit JSON output where supported")
@click.version_option(version="0.1.0", prog_name="cluefin-cli")
def cli(ctx: click.Context, debug: bool, json_output: bool):
    """Korean financial investment CLI toolkit with technical analysis and AI insights."""
    setup_logging(debug=debug)
    ctx.ensure_object(dict)
    ctx.obj["json"] = json_output
    if ctx.invoked_subcommand is not None:
        return

    if json_output:
        write_json(
            success_envelope(
                command="root",
                source=None,
                params={"debug": debug},
                data={
                    "app": "cluefin-cli",
                    "commands": ["statements", "chart", "news", "trading-flow", "market"],
                    "deprecated_commands": ["ta", "fa", "xbrl"],
                },
                meta={"version": "0.1.0"},
            )
        )
        return

    console.print("[bold blue]Cluefin CLI - Stock Analysis Tool[/bold blue]")
    console.print("Use --help to see available commands")


cli.add_command(technical_analysis)
cli.add_command(fundamental_analysis)
cli.add_command(xbrl_analysis)
cli.add_command(statements_command)
cli.add_command(news_command)


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
