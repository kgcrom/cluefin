"""Method routing dispatcher for JSON-RPC server."""

from __future__ import annotations

from typing import Any, Callable

from cluefin_rpc.handlers._base import MethodSchema
from cluefin_rpc.protocol import INVALID_PARAMS, METHOD_NOT_FOUND


class Dispatcher:
    def __init__(self) -> None:
        self._registry: dict[str, tuple[Callable, MethodSchema]] = {}

    def register(self, method_name: str, handler: Callable, schema: MethodSchema) -> None:
        self._registry[method_name] = (handler, schema)

    def dispatch(self, method: str, params: dict | list | None, session_manager: Any) -> Any:
        entry = self._registry.get(method)
        if entry is None:
            raise MethodNotFoundError(f"Method not found: {method}")

        handler, schema = entry
        if params is None:
            params = {}
        if not isinstance(params, dict):
            raise InvalidParamsError("params must be an object")

        if schema.requires_session:
            return handler(params, session_manager)
        return handler(params)

    def list_methods(self, category: str | None = None, broker: str | None = None) -> list[dict]:
        results = []
        for _name, (_, schema) in self._registry.items():
            if category and schema.category != category:
                continue
            if broker and schema.broker != broker:
                continue
            results.append(
                {
                    "name": schema.name,
                    "description": schema.description,
                    "parameters": schema.parameters,
                    "returns": schema.returns,
                    "category": schema.category,
                    "requires_session": schema.requires_session,
                    "broker": schema.broker,
                }
            )
        return results


class MethodNotFoundError(Exception):
    code = METHOD_NOT_FOUND


class InvalidParamsError(Exception):
    code = INVALID_PARAMS
