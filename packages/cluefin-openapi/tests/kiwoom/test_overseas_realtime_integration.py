"""키움 미국주식 실시간 시세(WebSocket) 통합 테스트.

미국 정규장(09:30–16:00 America/New_York)에 `-m "integration and realtime"` 이고 `KIWOOM_ENV=prod` 일 때만
돈다. 해외 모의계좌는 만료(RC4091) 상태라 모의로는 검증할 수 없다. 시세 구독만 하므로 주문은 나가지 않는다.
AAPL 은 정규장에 몇 초마다 체결되므로 수신 timeout 은 실패다.
"""

import asyncio

import pytest
from pydantic import BaseModel

from cluefin_openapi.kiwoom._overseas_realtime import OverseasRealtime
from cluefin_openapi.kiwoom._overseas_realtime_types import (
    OverseasRealtimeExecutionPrice,
    OverseasRealtimeTenQuotes,
)
from cluefin_openapi.kiwoom._socket_client import KiwoomWebSocketClient

from ._integration_helpers import kiwoom_env

pytestmark = [
    pytest.mark.integration,
    pytest.mark.realtime,
    # 시간대·환경 gate 가 먼저 — 장외·모의에서는 토큰 발급(access_token)까지 가지 않는다.
    pytest.mark.usefixtures("us_market_hours", "_require_prod_env"),
]

STOCK = ("AAPL", "ND")
TIMEOUT_SECONDS = 30


@pytest.fixture(scope="module")
def _require_prod_env() -> None:
    if kiwoom_env() != "prod":
        pytest.skip("Kiwoom US-stock mock account is expired (RC4091); requires KIWOOM_ENV=prod")


@pytest.fixture(scope="module")
def access_token(auth) -> str:
    return auth.generate_token().get_token()


async def _receive_first(ws: KiwoomWebSocketClient, model: type[BaseModel]) -> BaseModel:
    """`model` 로 파싱되는 첫 항목 묶음. 정규장 timeout 이면 실패한다."""

    async def wait() -> BaseModel | None:
        async for message in ws.events():
            for parsed in OverseasRealtime.parse(message):
                if isinstance(parsed, model):
                    return parsed
        return None

    try:
        received = await asyncio.wait_for(wait(), timeout=TIMEOUT_SECONDS)
    except TimeoutError:
        pytest.fail(f"No {model.__name__} for {STOCK[0]} within {TIMEOUT_SECONDS}s during US market hours.")
    assert received is not None, "WebSocket closed before any data arrived"
    return received


@pytest.mark.asyncio
async def test_receive_execution_price(access_token):
    async with KiwoomWebSocketClient(token=access_token, env="prod", market="overseas") as ws:
        await OverseasRealtime(ws).register([OverseasRealtime.TR_EXECUTION_PRICE], [STOCK])

        parsed = await _receive_first(ws, OverseasRealtimeExecutionPrice)

        assert isinstance(parsed, OverseasRealtimeExecutionPrice)
        for item in parsed.data:
            # alias(숫자 키) 매핑이 어긋나면 모델은 오류 없이 빈 문자열을 남긴다 — 값이 채워졌는지로 확인한다.
            assert item.values.current_price


@pytest.mark.asyncio
async def test_receive_ten_quotes(access_token):
    async with KiwoomWebSocketClient(token=access_token, env="prod", market="overseas") as ws:
        await OverseasRealtime(ws).register([OverseasRealtime.TR_TEN_QUOTES], [STOCK])

        parsed = await _receive_first(ws, OverseasRealtimeTenQuotes)

        assert isinstance(parsed, OverseasRealtimeTenQuotes)
        for item in parsed.data:
            assert item.values.ask_price_1
