from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class MethodSchema:
    name: str
    description: str
    parameters: dict[str, Any]
    returns: dict[str, Any]
    category: str = ""
    requires_session: bool = True
    broker: str | None = None


def rpc_method(
    name: str,
    description: str,
    parameters: dict[str, Any],
    returns: dict[str, Any],
    category: str = "",
    requires_session: bool = True,
    broker: str | None = None,
):
    """Decorator that attaches _rpc_schema metadata to handler functions."""

    def decorator(fn):
        fn._rpc_schema = MethodSchema(
            name=name,
            description=description,
            parameters=parameters,
            returns=returns,
            category=category,
            requires_session=requires_session,
            broker=broker,
        )
        return fn

    return decorator
