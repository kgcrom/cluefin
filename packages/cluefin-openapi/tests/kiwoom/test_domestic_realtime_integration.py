"""키움 국내주식 실시간 시세(WebSocket) 통합 테스트.

KRX 연속매매 시간(평일 09:00–15:20 KST)에 `-m "integration and realtime"` 으로만 돈다. 모의 WS 도 KRX 를
지원하므로 `KIWOOM_ENV=dev` 로도 검증된다. 삼성전자는 그 시간에 몇 초마다 체결되므로 수신 timeout 은
skip 이 아니라 실패다.

서버는 없는 종목(예: 999999)의 REG 에도 `return_code: 0` 을 답한다(2026-10-12 실측). 등록 응답은
검증 수단이 아니고, 데이터 수신만 의미가 있다.
"""

import asyncio

import pytest
from pydantic import BaseModel

from cluefin_openapi.kiwoom._domestic_realtime import DomesticRealtime
from cluefin_openapi.kiwoom._domestic_realtime_types import (
    DomesticRealtimeStockExecution,
    DomesticRealtimeStockQuoteRemaining,
)
from cluefin_openapi.kiwoom._socket_client import KiwoomWebSocketClient, KiwoomWebSocketMessage

from ._integration_helpers import kiwoom_env

pytestmark = [
    pytest.mark.integration,
    pytest.mark.realtime,
    # 시간대 gate 가 먼저 — 장외에는 토큰 발급(access_token)까지 가지 않는다.
    pytest.mark.usefixtures("krx_continuous_hours"),
]

STK_CD = "005930"
TIMEOUT_SECONDS = 30


@pytest.fixture(scope="module")
def access_token(auth) -> str:
    return auth.generate_token().get_token()


async def _receive_each(ws: KiwoomWebSocketClient, *models: type[BaseModel]) -> dict[type, BaseModel]:
    """`models` 가 하나씩 파싱될 때까지 받는다. 장중 timeout 이면 실패한다."""
    received: dict[type, BaseModel] = {}

    async def wait() -> None:
        async for message in ws.events():
            for parsed in DomesticRealtime.parse(message):
                received.setdefault(type(parsed), parsed)
            if all(model in received for model in models):
                return

    try:
        await asyncio.wait_for(wait(), timeout=TIMEOUT_SECONDS)
    except TimeoutError:
        missing = [model.__name__ for model in models if model not in received]
        pytest.fail(f"No {missing} for {STK_CD} within {TIMEOUT_SECONDS}s during continuous trading hours.")
    assert all(model in received for model in models), "WebSocket closed before the data arrived"
    return received


async def _recv_ack(ws: KiwoomWebSocketClient, trnm: str) -> KiwoomWebSocketMessage:
    async def wait() -> KiwoomWebSocketMessage:
        while True:
            message = await ws.recv()
            if message.trnm == trnm:
                return message

    return await asyncio.wait_for(wait(), timeout=5)


def _assert_execution(parsed: BaseModel) -> None:
    assert isinstance(parsed, DomesticRealtimeStockExecution)
    for item in parsed.data:
        assert item.item == STK_CD
        # alias(숫자 키) 매핑이 어긋나면 모델은 오류 없이 빈 문자열을 남긴다 — 값이 채워졌는지로 확인한다.
        assert item.values.current_price
        assert item.values.execution_time


def _assert_quote_remaining(parsed: BaseModel) -> None:
    assert isinstance(parsed, DomesticRealtimeStockQuoteRemaining)
    for item in parsed.data:
        assert item.item == STK_CD
        assert item.values.ask_price_1
        assert item.values.quote_time


@pytest.mark.asyncio
async def test_receive_stock_execution(access_token):
    async with KiwoomWebSocketClient(token=access_token, env=kiwoom_env(), market="domestic") as ws:
        await DomesticRealtime(ws).register(["0B"], [STK_CD])

        received = await _receive_each(ws, DomesticRealtimeStockExecution)

        _assert_execution(received[DomesticRealtimeStockExecution])


@pytest.mark.asyncio
async def test_receive_quote_remaining(access_token):
    async with KiwoomWebSocketClient(token=access_token, env=kiwoom_env(), market="domestic") as ws:
        await DomesticRealtime(ws).register(["0D"], [STK_CD])

        received = await _receive_each(ws, DomesticRealtimeStockQuoteRemaining)

        _assert_quote_remaining(received[DomesticRealtimeStockQuoteRemaining])


@pytest.mark.asyncio
async def test_receive_execution_and_quote_together(access_token):
    """함께 등록하면 서버가 0B·0D 를 한 프레임에 섞어 보낸다 — 두 type 모두 값이 채워져야 한다."""
    async with KiwoomWebSocketClient(token=access_token, env=kiwoom_env(), market="domestic") as ws:
        await DomesticRealtime(ws).register(["0B", "0D"], [STK_CD])

        received = await _receive_each(ws, DomesticRealtimeStockExecution, DomesticRealtimeStockQuoteRemaining)

        _assert_execution(received[DomesticRealtimeStockExecution])
        _assert_quote_remaining(received[DomesticRealtimeStockQuoteRemaining])


@pytest.mark.asyncio
async def test_remove_is_acknowledged(access_token):
    async with KiwoomWebSocketClient(token=access_token, env=kiwoom_env(), market="domestic") as ws:
        realtime = DomesticRealtime(ws)
        await realtime.register(["0B"], [STK_CD])
        await _receive_each(ws, DomesticRealtimeStockExecution)

        await realtime.remove(["0B"], [STK_CD])

        ack = await _recv_ack(ws, "REMOVE")
        assert ack.body.get("return_code") == 0
