"""Agent-friendly CLI surface for cluefin-openapi."""

from __future__ import annotations

__all__ = ["main"]


def __getattr__(name: str):
    if name == "main":
        from cluefin_openapi_cli.main import main

        return main
    raise AttributeError(name)
