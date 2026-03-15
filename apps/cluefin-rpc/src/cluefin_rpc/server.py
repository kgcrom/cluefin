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
from cluefin_rpc.handlers.kis import register_kis_handlers
from cluefin_rpc.handlers.kiwoom import register_kiwoom_handlers
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

CATEGORY_DESCRIPTIONS: dict[str, str] = {
    "rpc": "서버 상태 확인 및 메서드 목록 조회",
    "session": "브로커 세션 초기화·상태 조회·종료",
    "ta": "기술적 분석 지표 (이동평균, RSI, MACD, 볼린저밴드 등)",
    "stock": "종목 현재가·호가·체결·시세 조회",
    "chart": "일봉·분봉·틱 차트 데이터 조회",
    "etf": "ETF 시세·NAV·구성종목·수익률 조회",
    "financial": "재무제표·재무비율·수익성·안정성·성장성 분석",
    "schedule": "배당·유상증자·IPO·주주총회 등 기업 일정 조회",
    "analysis": "투자자·외국인·기관 매매동향 및 시장 분석",
    "ranking": "거래량·시가총액·등락률·공매도 등 종목 순위",
    "program": "프로그램 매매·차익거래 잔고·투자자별 추이",
    "sector": "업종별 지수·투자자 순매수·시세 조회",
    "market": "금리·공시·휴장일·워런트 등 시장 기본 정보",
    "dart": "DART 공시 검색·기업 개황·대주주 현황 조회",
    "theme": "테마 그룹 목록 및 테마별 종목 조회",
}

# Configure loguru to stderr only
logger.remove()
logger.add(sys.stderr, level="DEBUG")


def _build_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    register_session_handlers(dispatcher, session_manager=None)
    register_kis_handlers(dispatcher)
    register_kiwoom_handlers(dispatcher)
    register_quote_handlers(dispatcher)
    register_ta_handlers(dispatcher)
    register_dart_handlers(dispatcher)
    return dispatcher


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
    dispatcher = Dispatcher()
    session_manager = SessionManager(settings)

    register_session_handlers(dispatcher, session_manager)
    register_kis_handlers(dispatcher)
    register_kiwoom_handlers(dispatcher)
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
