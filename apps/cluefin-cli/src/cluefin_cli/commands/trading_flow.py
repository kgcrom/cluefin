"""Domain command for investor trading flow data."""

from __future__ import annotations

import click
from loguru import logger
from rich.console import Console
from rich.table import Table

from cluefin_cli.domains.trading_flow import TradingFlowService
from cluefin_cli.output import error_envelope, success_envelope, write_json

console = Console()


@click.command(name="trading-flow")
@click.pass_context
@click.argument("stock_code")
@click.option("--source", type=click.Choice(["auto", "kiwoom", "kis", "all"]), default="auto", show_default=True)
@click.option("--start-date")
@click.option("--end-date")
@click.option("--json", "json_output", is_flag=True, help="Emit JSON output")
def trading_flow_command(
    ctx: click.Context,
    stock_code: str,
    source: str,
    start_date: str | None,
    end_date: str | None,
    json_output: bool,
) -> None:
    """Fetch normalized investor trading flow data."""
    use_json = json_output or bool(ctx.obj and ctx.obj.get("json"))
    params = {
        "stock_code": stock_code,
        "source": source,
        "start_date": start_date,
        "end_date": end_date,
    }
    try:
        snapshots = TradingFlowService().fetch(
            stock_code=stock_code,
            source=source,
            start_date=start_date,
            end_date=end_date,
        )
    except Exception as exc:
        if use_json:
            write_json(error_envelope(command="trading-flow", error_type=type(exc).__name__, message=str(exc)))
            raise click.exceptions.Exit(1) from exc
        console.print(f"[red]Error fetching trading flow: {exc}[/red]")
        logger.exception("Trading flow command failed")
        raise click.exceptions.Exit(1) from exc

    if use_json:
        write_json(success_envelope(command="trading-flow", source=source, params=params, data={"items": snapshots}))
        return

    table = Table(title=f"Trading Flow {stock_code}")
    table.add_column("Source")
    table.add_column("Rows", justify="right")
    table.add_column("Foreign", justify="right")
    table.add_column("Institution", justify="right")
    table.add_column("Individual", justify="right")
    for snapshot in snapshots:
        table.add_row(
            snapshot.source,
            str(len(snapshot.rows)),
            _fmt(snapshot.totals.get("foreign")),
            _fmt(snapshot.totals.get("institution")),
            _fmt(snapshot.totals.get("individual")),
        )
    console.print(table)


def _fmt(value: object) -> str:
    if value is None:
        return "-"
    try:
        return f"{float(value):,.0f}"
    except (TypeError, ValueError):
        return str(value)
