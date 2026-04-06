"""Shared registry helpers for RPC and CLI surfaces."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from cluefin_rpc.dispatcher import Dispatcher
from cluefin_rpc.handlers.dart import register_dart_handlers
from cluefin_rpc.handlers.kis import register_kis_handlers
from cluefin_rpc.handlers.kiwoom import register_kiwoom_handlers
from cluefin_rpc.handlers.quote import register_quote_handlers
from cluefin_rpc.handlers.session import register_session_handlers
from cluefin_rpc.handlers.ta import register_ta_handlers

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


@dataclass(frozen=True)
class CliCommandDefinition:
    """Broker-only command metadata normalized for the CLI namespace."""

    broker: str
    category: str
    method_name: str
    command_name: str
    path_segments: tuple[str, ...]
    description: str
    parameters: dict[str, Any]
    returns: dict[str, Any]
    requires_session: bool
    executor: Callable[..., Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "broker": self.broker,
            "category": self.category,
            "method_name": self.method_name,
            "command_name": self.command_name,
            "path_segments": list(self.path_segments),
            "description": self.description,
            "parameters": self.parameters,
            "returns": self.returns,
            "requires_session": self.requires_session,
        }


def _kebab_case(value: str) -> str:
    return value.replace("_", "-").replace(".", "-")


def build_dispatcher(session_manager: Any | None = None) -> Dispatcher:
    """Build the full dispatcher used by the RPC server."""
    dispatcher = Dispatcher()
    register_session_handlers(dispatcher, session_manager)
    register_kis_handlers(dispatcher)
    register_kiwoom_handlers(dispatcher)
    register_quote_handlers(dispatcher)
    register_ta_handlers(dispatcher)
    register_dart_handlers(dispatcher)
    return dispatcher


def build_cli_registry() -> dict[tuple[str, ...], CliCommandDefinition]:
    """Build a broker-only CLI registry from the shared dispatcher."""
    dispatcher = build_dispatcher(session_manager=None)
    registry: dict[tuple[str, ...], CliCommandDefinition] = {}

    for method_name, handler, schema in dispatcher.iter_entries():
        if schema.broker not in {"kis", "kiwoom", "dart"}:
            continue

        if schema.broker == "dart":
            _, leaf_name = method_name.split(".", 1)
            category = "dart"
            path_segments = ("dart", _kebab_case(leaf_name))
            command_name = _kebab_case(leaf_name)
        else:
            category, leaf_name = method_name.split(".", 1)
            path_segments = (schema.broker, _kebab_case(category), _kebab_case(leaf_name))
            command_name = _kebab_case(leaf_name)

        definition = CliCommandDefinition(
            broker=schema.broker,
            category=category,
            method_name=method_name,
            command_name=command_name,
            path_segments=path_segments,
            description=schema.description,
            parameters=schema.parameters,
            returns=schema.returns,
            requires_session=schema.requires_session,
            executor=handler,
        )
        if path_segments in registry:
            raise ValueError(f"Duplicate CLI path detected: {' '.join(path_segments)}")
        registry[path_segments] = definition

    return registry


def list_cli_commands(*, broker: str | None = None, category: str | None = None) -> list[CliCommandDefinition]:
    commands = list(build_cli_registry().values())
    if broker:
        commands = [command for command in commands if command.broker == broker]
    if category:
        commands = [command for command in commands if command.category == category]
    return sorted(commands, key=lambda command: command.path_segments)


def get_cli_command(path_segments: tuple[str, ...]) -> CliCommandDefinition:
    registry = build_cli_registry()
    try:
        return registry[path_segments]
    except KeyError as exc:
        raise KeyError(f"Unknown CLI command path: {' '.join(path_segments)}") from exc
