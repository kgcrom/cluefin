"""Session and meta RPC handlers."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from cluefin_rpc.handlers._base import rpc_method

if TYPE_CHECKING:
    from cluefin_rpc.dispatcher import Dispatcher
    from cluefin_rpc.middleware.auth import SessionManager


@rpc_method(
    name="rpc.ping",
    description="Health check. Returns server status and timestamp.",
    parameters={"type": "object", "properties": {}},
    returns={"type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}}},
    category="rpc",
    requires_session=False,
)
def handle_ping(params: dict) -> dict:
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@rpc_method(
    name="rpc.list_methods",
    description="List all registered RPC methods with their JSON Schema. Optionally filter by category or broker.",
    parameters={
        "type": "object",
        "properties": {
            "category": {"type": "string", "description": "Filter by category (rpc, quote, ta, account, dart)"},
            "broker": {"type": "string", "description": "Filter by broker (kis, kiwoom, krx, dart)"},
        },
    },
    returns={"type": "array", "items": {"type": "object"}},
    category="rpc",
    requires_session=False,
)
def handle_list_methods(params: dict, *, _dispatcher: Dispatcher | None = None) -> list[dict]:
    if _dispatcher is None:
        return []
    return _dispatcher.list_methods(
        category=params.get("category"),
        broker=params.get("broker"),
    )


@rpc_method(
    name="session.initialize",
    description="Initialize a broker session. Must be called before using broker-specific methods.",
    parameters={
        "type": "object",
        "properties": {
            "broker": {
                "type": "string",
                "enum": ["kis", "kiwoom", "krx", "dart"],
                "description": "Broker to initialize",
            },
        },
        "required": ["broker"],
    },
    returns={"type": "object"},
    category="session",
    requires_session=False,
)
def handle_session_initialize(params: dict, *, _session_manager: SessionManager | None = None) -> dict:
    if _session_manager is None:
        raise RuntimeError("SessionManager not available")
    return _session_manager.initialize(params["broker"])


@rpc_method(
    name="session.status",
    description="Query active broker sessions.",
    parameters={"type": "object", "properties": {}},
    returns={"type": "object"},
    category="session",
    requires_session=False,
)
def handle_session_status(params: dict, *, _session_manager: SessionManager | None = None) -> dict:
    if _session_manager is None:
        raise RuntimeError("SessionManager not available")
    return _session_manager.status()


@rpc_method(
    name="session.close",
    description="Close a specific broker session or all sessions.",
    parameters={
        "type": "object",
        "properties": {
            "broker": {
                "type": "string",
                "enum": ["kis", "kiwoom", "krx", "dart"],
                "description": "Broker to close. Omit to close all.",
            },
        },
    },
    returns={"type": "object"},
    category="session",
    requires_session=False,
)
def handle_session_close(params: dict, *, _session_manager: SessionManager | None = None) -> dict:
    if _session_manager is None:
        raise RuntimeError("SessionManager not available")
    return _session_manager.close(params.get("broker"))


def register_session_handlers(dispatcher: Dispatcher, session_manager: SessionManager | None) -> None:
    """Register all session/meta handlers with the dispatcher."""
    dispatcher.register("rpc.ping", handle_ping, handle_ping._rpc_schema)

    # list_methods needs a reference to the dispatcher
    def _list_methods(params: dict) -> list[dict]:
        return handle_list_methods(params, _dispatcher=dispatcher)

    dispatcher.register("rpc.list_methods", _list_methods, handle_list_methods._rpc_schema)

    # Session handlers need session_manager
    def _init(params: dict) -> dict:
        return handle_session_initialize(params, _session_manager=session_manager)

    def _status(params: dict) -> dict:
        return handle_session_status(params, _session_manager=session_manager)

    def _close(params: dict) -> dict:
        return handle_session_close(params, _session_manager=session_manager)

    dispatcher.register("session.initialize", _init, handle_session_initialize._rpc_schema)
    dispatcher.register("session.status", _status, handle_session_status._rpc_schema)
    dispatcher.register("session.close", _close, handle_session_close._rpc_schema)
