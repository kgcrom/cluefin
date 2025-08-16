"""
Main entry point for the stock inquiry command.

This module provides the main CLI command for interactive stock inquiry functionality.
"""

import click


@click.command()
@click.pass_context
def inquiry(ctx):
    """Interactive stock inquiry tool for Korean markets."""
    # TODO: Implementation will be added in subsequent tasks
    click.echo("Stock inquiry feature - implementation coming soon!")