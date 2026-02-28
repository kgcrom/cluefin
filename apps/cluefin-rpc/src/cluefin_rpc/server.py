"""Main JSON-RPC 2.0 server event loop.

Reads newline-delimited JSON from stdin, dispatches to handlers, writes responses to stdout.
All logs go to stderr via loguru.
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict

from loguru import logger

from cluefin_rpc.config import RpcSettings
from cluefin_rpc.dispatcher import Dispatcher, InvalidParamsError, MethodNotFoundError
from cluefin_rpc.handlers.dart import register_dart_handlers
from cluefin_rpc.handlers.quote import register_quote_handlers
from cluefin_rpc.handlers.session import register_session_handlers
from cluefin_rpc.handlers.ta import register_ta_handlers
from cluefin_rpc.middleware.auth import SessionManager
from cluefin_rpc.middleware.errors import map_exception_to_rpc_error
from cluefin_rpc.protocol import (
    INTERNAL_ERROR,
    INVALID_REQUEST,
    PARSE_ERROR,
    parse_request,
    write_error,
    write_response,
)

VERSION = "0.1.0"

# Configure loguru to stderr only
logger.remove()
logger.add(sys.stderr, level="DEBUG")


def _build_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    register_session_handlers(dispatcher, session_manager=None)
    register_quote_handlers(dispatcher)
    register_ta_handlers(dispatcher)
    register_dart_handlers(dispatcher)
    return dispatcher


def _print_methods(dispatcher: Dispatcher) -> None:
    methods = dispatcher.list_methods()
    grouped: dict[str, list[dict]] = defaultdict(list)
    for m in methods:
        grouped[m["category"] or "other"].append(m)

    logger.info("cluefin-rpc v{} — {} methods\n", VERSION, len(methods))
    for category in sorted(grouped):
        items = sorted(grouped[category], key=lambda m: m["name"])
        logger.info("[{}] ({})", category, len(items))
        max_name = max(len(m["name"]) for m in items)
        for m in items:
            logger.info("  {:<{}}  {}", m["name"], max_name, m["description"])
        logger.info("")


def main() -> int:
    parser = argparse.ArgumentParser(description="cluefin JSON-RPC 2.0 server")
    parser.add_argument(
        "--list-methods",
        action="store_true",
        help="Print registered RPC methods and exit",
    )
    args = parser.parse_args()

    if args.list_methods:
        dispatcher = _build_dispatcher()
        _print_methods(dispatcher)
        return 0

    settings = RpcSettings()
    dispatcher = Dispatcher()
    session_manager = SessionManager(settings)

    register_session_handlers(dispatcher, session_manager)
    register_quote_handlers(dispatcher)
    register_ta_handlers(dispatcher)
    register_dart_handlers(dispatcher)

    logger.info("cluefin-rpc server started")

    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue

        try:
            request = parse_request(line)
        except ValueError as e:
            write_error(None, PARSE_ERROR, str(e))
            continue

        request_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        if not method:
            write_error(request_id, INVALID_REQUEST, "Missing method")
            continue

        try:
            result = dispatcher.dispatch(method, params, session_manager)
        except (MethodNotFoundError, InvalidParamsError) as exc:
            if request_id is not None:
                write_error(request_id, exc.code, str(exc))
            continue
        except Exception as exc:
            logger.exception("Handler error for method={}", method)
            if request_id is not None:
                code, message, data = map_exception_to_rpc_error(exc)
                write_error(request_id, code, message, data)
            continue

        if request_id is not None:
            write_response({"jsonrpc": "2.0", "id": request_id, "result": result})

    session_manager.close_all()
    logger.info("cluefin-rpc server stopped")
    return 0
