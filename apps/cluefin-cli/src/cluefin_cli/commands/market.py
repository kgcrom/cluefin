"""Domain command group for market scanner data."""

from __future__ import annotations

import click
from loguru import logger
from rich.console import Console
from rich.table import Table

from cluefin_cli.domains.market import MarketCategory, MarketService
from cluefin_cli.domains.models import MarketRankItem
from cluefin_cli.output import error_envelope, success_envelope, write_json

console = Console()


@click.group(name="market")
def market_command() -> None:
    """Fetch domain-oriented market scanner data."""


def _market_subcommand(category: MarketCategory) -> click.Command:
    @click.command(name=category)
    @click.pass_context
    @click.option("--source", type=click.Choice(["auto", "kis", "kiwoom", "all"]), default="auto", show_default=True)
    @click.option("--limit", type=click.IntRange(1, 100), default=20, show_default=True)
    @click.option("--json", "json_output", is_flag=True, help="Emit JSON output")
    def command(ctx: click.Context, source: str, limit: int, json_output: bool) -> None:
        use_json = json_output or bool(ctx.obj and ctx.obj.get("json"))
        params = {"category": category, "source": source, "limit": limit}
        try:
            items = MarketService().fetch(category=category, source=source, limit=limit)
        except Exception as exc:
            if use_json:
                write_json(
                    error_envelope(command=f"market {category}", error_type=type(exc).__name__, message=str(exc))
                )
                raise click.exceptions.Exit(1) from exc
            console.print(f"[red]Error fetching market {category}: {exc}[/red]")
            logger.exception("Market command failed")
            raise click.exceptions.Exit(1) from exc

        if use_json:
            write_json(
                success_envelope(command=f"market {category}", source=source, params=params, data={"items": items})
            )
            return
        _display_table(category=category, items=items)

    return command


def _display_table(*, category: str, items: list[MarketRankItem]) -> None:
    table = Table(title=f"Market {category}")
    table.add_column("Source")
    table.add_column("Rank", justify="right")
    table.add_column("Code")
    table.add_column("Name")
    table.add_column("Value", justify="right")
    table.add_column("Change", justify="right")
    for item in items:
        table.add_row(
            item.source,
            str(item.rank or "-"),
            item.stock_code or "-",
            item.stock_name or "-",
            str(item.value if item.value is not None else "-"),
            str(item.change_rate if item.change_rate is not None else "-"),
        )
    console.print(table)


for _category in ["volume", "ranking", "theme", "sector"]:
    market_command.add_command(_market_subcommand(_category))
