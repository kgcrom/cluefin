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
from cluefin_rpc.registry import CATEGORY_DESCRIPTIONS, VERSION, build_dispatcher

# Configure loguru to stderr only
logger.remove()
logger.add(sys.stderr, level="DEBUG")


def _build_dispatcher() -> Dispatcher:
    return build_dispatcher(session_manager=None)


def _print_categories(dispatcher: Dispatcher) -> None:
    methods = dispatcher.list_methods()
    grouped: dict[str, int] = defaultdict(int)
    for m in methods:
        grouped[m["category"] or "other"] += 1

    logger.info("cluefin-rpc v{} — {} categories, {} methods\n", VERSION, len(grouped), len(methods))
    max_cat = max(len(c) for c in grouped)
    for category in sorted(grouped):
        desc = CATEGORY_DESCRIPTIONS.get(category, "")
        logger.info("  {:<{}}  {:>3} methods  {}", category, max_cat, grouped[category], desc)


def _print_methods(dispatcher: Dispatcher, category: str | None = None) -> None:
    methods = dispatcher.list_methods(category=category)
    if not methods:
        logger.info("카테고리 '{}'에 해당하는 메서드가 없습니다.", category)
        logger.info("사용 가능한 카테고리 목록은 --list-categories 로 확인하세요.")
        return

    grouped: dict[str, list[dict]] = defaultdict(list)
    for m in methods:
        grouped[m["category"] or "other"].append(m)

    logger.info("cluefin-rpc v{} — {} methods\n", VERSION, len(methods))
    for cat in sorted(grouped):
        items = sorted(grouped[cat], key=lambda m: m["name"])
        logger.info("[{}] ({})", cat, len(items))
        max_name = max(len(m["name"]) for m in items)
        for m in items:
            logger.info("  {:<{}}  {}", m["name"], max_name, m["description"])
        logger.info("")


def main() -> int:
    parser = argparse.ArgumentParser(description="cluefin JSON-RPC 2.0 server")
    parser.add_argument(
        "--list-categories",
        action="store_true",
        help="Print RPC method categories and exit",
    )
    parser.add_argument(
        "--list-methods",
        nargs="?",
        const=True,
        default=None,
        metavar="CATEGORY",
        help="Print registered RPC methods and exit (optionally filter by category)",
    )
    args = parser.parse_args()

    if args.list_categories:
        dispatcher = _build_dispatcher()
        _print_categories(dispatcher)
        return 0

    if args.list_methods is not None:
        dispatcher = _build_dispatcher()
        category = args.list_methods if isinstance(args.list_methods, str) else None
        _print_methods(dispatcher, category=category)
        return 0

    settings = RpcSettings()
    session_manager = SessionManager(settings)
    dispatcher = build_dispatcher(session_manager=session_manager)

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
