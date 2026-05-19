"""Domain command for statements data."""

from __future__ import annotations

import click
from loguru import logger
from rich.console import Console
from rich.table import Table

from cluefin_cli.domains.statements import REPORT_CODE_MAP, StatementsService, default_business_year
from cluefin_cli.output import error_envelope, success_envelope, write_json

console = Console()


@click.command(name="statements")
@click.pass_context
@click.argument("stock_code")
@click.option("--source", type=click.Choice(["auto", "dart", "kis", "all"]), default="auto", show_default=True)
@click.option("--year", default=default_business_year(), show_default=True)
@click.option("--report", type=click.Choice(list(REPORT_CODE_MAP.keys())), default="annual", show_default=True)
@click.option("--include-xbrl", is_flag=True)
@click.option("--statement-type", type=click.Choice(["BS", "IS", "CIS", "CF", "SCE"], case_sensitive=False))
@click.option("--json", "json_output", is_flag=True, help="Emit JSON output")
def statements_command(
    ctx: click.Context,
    stock_code: str,
    source: str,
    year: str,
    report: str,
    include_xbrl: bool,
    statement_type: str | None,
    json_output: bool,
) -> None:
    """Fetch domain-oriented financial statement data."""
    use_json = json_output or bool(ctx.obj and ctx.obj.get("json"))
    params = {
        "stock_code": stock_code,
        "source": source,
        "year": year,
        "report": report,
        "include_xbrl": include_xbrl,
        "statement_type": statement_type,
    }
    try:
        snapshots = StatementsService().fetch(**params)
    except Exception as exc:
        if use_json:
            write_json(error_envelope(command="statements", error_type=type(exc).__name__, message=str(exc)))
            raise click.exceptions.Exit(1) from exc
        console.print(f"[red]Error fetching statements: {exc}[/red]")
        logger.exception("Statements command failed")
        raise click.exceptions.Exit(1) from exc

    if use_json:
        write_json(success_envelope(command="statements", source=source, params=params, data={"items": snapshots}))
        return

    table = Table(title=f"Statements {stock_code}")
    table.add_column("Source")
    table.add_column("Company")
    table.add_column("Accounts", justify="right")
    table.add_column("Metrics", justify="right")
    for snapshot in snapshots:
        table.add_row(
            snapshot.source,
            snapshot.company_name or "-",
            str(len(snapshot.accounts)),
            str(len(snapshot.metrics)),
        )
    console.print(table)
