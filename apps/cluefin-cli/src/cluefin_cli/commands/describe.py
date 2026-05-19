"""AI-friendly command discovery."""

from __future__ import annotations

import click
from rich.console import Console
from rich.table import Table

from cluefin_cli.command_metadata import describe_commands
from cluefin_cli.output import error_envelope, success_envelope, write_json

console = Console()


@click.command(name="describe")
@click.pass_context
@click.argument(
    "command_name",
    required=False,
    type=click.Choice(["statements", "chart", "news", "trading-flow", "market"]),
)
@click.option("--json", "json_output", is_flag=True, help="Emit JSON command metadata")
def describe_command(ctx: click.Context, command_name: str | None, json_output: bool) -> None:
    """Describe domain commands without calling provider APIs."""
    use_json = json_output or bool(ctx.obj and ctx.obj.get("json"))
    commands = describe_commands(command_name)
    if command_name and not commands:
        if use_json:
            write_json(
                error_envelope(
                    command="describe",
                    error_type="CommandNotFound",
                    message=f"Unknown command: {command_name}",
                )
            )
            raise click.exceptions.Exit(1)
        raise click.ClickException(f"Unknown command: {command_name}")

    if use_json:
        write_json(
            success_envelope(
                command="describe",
                source=None,
                params={"command": command_name},
                data={"commands": commands},
            )
        )
        return

    table = Table(title="Cluefin CLI Domain Commands")
    table.add_column("Command")
    table.add_column("Summary")
    table.add_column("Usage")
    for item in commands:
        table.add_row(item["name"], item["summary"], item["usage"])
    console.print(table)
