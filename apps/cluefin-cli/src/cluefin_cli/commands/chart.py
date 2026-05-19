"""Domain command for OHLCV chart data."""

from __future__ import annotations

import click
import pandas as pd
from loguru import logger
from rich.console import Console
from rich.table import Table

from cluefin_cli.display.charts import ChartRenderer
from cluefin_cli.domains.chart import ChartService
from cluefin_cli.domains.models import OhlcvSeries
from cluefin_cli.output import error_envelope, success_envelope, write_json

console = Console()


@click.command(name="chart")
@click.pass_context
@click.argument("stock_code")
@click.option("--source", type=click.Choice(["auto", "kiwoom", "kis"]), default="auto", show_default=True)
@click.option("--interval", type=click.Choice(["daily", "minute"]), default="daily", show_default=True)
@click.option("--days", type=click.IntRange(1, 2000), default=300, show_default=True)
@click.option("--volume", is_flag=True, help="Include volume rows in table output")
@click.option("--indicators", is_flag=True, help="Calculate technical indicators")
@click.option("--render", "render_chart", is_flag=True, help="Render a terminal chart in non-JSON mode")
@click.option("--json", "json_output", is_flag=True, help="Emit JSON output")
def chart_command(
    ctx: click.Context,
    stock_code: str,
    source: str,
    interval: str,
    days: int,
    volume: bool,
    indicators: bool,
    render_chart: bool,
    json_output: bool,
) -> None:
    """Fetch normalized OHLCV chart data."""
    use_json = json_output or bool(ctx.obj and ctx.obj.get("json"))
    params = {
        "stock_code": stock_code,
        "source": source,
        "interval": interval,
        "days": days,
        "volume": volume,
        "indicators": indicators,
        "render": render_chart,
    }
    try:
        series = ChartService().fetch(
            stock_code=stock_code, source=source, interval=interval, days=days, indicators=indicators
        )
    except Exception as exc:
        if use_json:
            write_json(error_envelope(command="chart", error_type=type(exc).__name__, message=str(exc)))
            raise click.exceptions.Exit(1) from exc
        console.print(f"[red]Error fetching chart data: {exc}[/red]")
        logger.exception("Chart command failed")
        raise click.exceptions.Exit(1) from exc

    if use_json:
        write_json(success_envelope(command="chart", source=series.source, params=params, data=series))
        return

    _display_chart_table(series, include_volume=volume)
    if render_chart:
        ChartRenderer().render_stock_chart(_series_to_frame(series))


def _display_chart_table(series: OhlcvSeries, *, include_volume: bool) -> None:
    table = Table(title=f"Chart {series.stock_code} ({series.source}, {series.interval})")
    table.add_column("Timestamp")
    table.add_column("Open", justify="right")
    table.add_column("High", justify="right")
    table.add_column("Low", justify="right")
    table.add_column("Close", justify="right")
    if include_volume:
        table.add_column("Volume", justify="right")
    for point in series.points[-20:]:
        row = [
            point.timestamp,
            _fmt(point.open),
            _fmt(point.high),
            _fmt(point.low),
            _fmt(point.close),
        ]
        if include_volume:
            row.append(_fmt(point.volume))
        table.add_row(*row)
    console.print(table)


def _series_to_frame(series: OhlcvSeries) -> pd.DataFrame:
    rows = [
        {
            "date": pd.to_datetime(point.timestamp[:8], errors="coerce"),
            "open": point.open,
            "high": point.high,
            "low": point.low,
            "close": point.close,
            "volume": point.volume,
        }
        for point in series.points
    ]
    frame = pd.DataFrame(rows)
    if frame.empty:
        return frame
    frame.set_index("date", inplace=True)
    return frame


def _fmt(value: float | None) -> str:
    if value is None:
        return "-"
    return f"{value:,.2f}"
