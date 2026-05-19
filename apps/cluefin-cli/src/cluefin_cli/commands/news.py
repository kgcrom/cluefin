"""Domain command for news and disclosures."""

from __future__ import annotations

import click
from loguru import logger
from rich.console import Console
from rich.table import Table

from cluefin_cli.domains.news import NewsService
from cluefin_cli.output import error_envelope, success_envelope, write_json

console = Console()


@click.command(name="news")
@click.pass_context
@click.argument("stock_code", required=False)
@click.option("--source", type=click.Choice(["auto", "kis", "dart", "all"]), default="auto", show_default=True)
@click.option("--days", type=click.IntRange(1, 365), default=7, show_default=True)
@click.option("--query")
@click.option("--json", "json_output", is_flag=True, help="Emit JSON output")
def news_command(
    ctx: click.Context,
    stock_code: str | None,
    source: str,
    days: int,
    query: str | None,
    json_output: bool,
) -> None:
    """Fetch domain-oriented market news and disclosures."""
    use_json = json_output or bool(ctx.obj and ctx.obj.get("json"))
    params = {"stock_code": stock_code, "source": source, "days": days, "query": query}
    try:
        data = NewsService().fetch(**params)
    except Exception as exc:
        if use_json:
            write_json(error_envelope(command="news", error_type=type(exc).__name__, message=str(exc)))
            raise click.exceptions.Exit(1) from exc
        console.print(f"[red]Error fetching news: {exc}[/red]")
        logger.exception("News command failed")
        raise click.exceptions.Exit(1) from exc

    if use_json:
        write_json(success_envelope(command="news", source=source, params=params, data=data))
        return

    table = Table(title="News")
    table.add_column("Source")
    table.add_column("Title")
    table.add_column("Published")
    for item in data["news"]:
        table.add_row(item.source, item.title, item.published_at or "-")
    for item in data["disclosures"]:
        table.add_row(item.source, item.report_name, item.rcept_date or "-")
    console.print(table)
