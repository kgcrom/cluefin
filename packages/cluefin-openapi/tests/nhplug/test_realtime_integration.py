"""NH PLUG 실시간 시세(WebSocket) 통합 테스트.

`-m "integration and realtime"` 으로, 해당 시장이 열려 있고 `NHPLUG_ENV=prod` 일 때만 돈다. 시세 채널은
운영 전용이다 — 모의 소켓(:17070)은 `oc` 구독에 `rsp_cd=WSS10006 "허용되지 않는 tr_cd 입니다."` 를 답한다
(2026-10-12 실측). 시세 구독만 하므로 주문은 나가지 않는다.

운영 서버는 없는 종목(999999) 구독에도 `rsp_cd=00000` 을 답한다(2026-10-12 실측). 구독 응답은 검증 수단이
아니고, 데이터 수신만 의미가 있다. 구독 응답도 `tr_cd` 가 붙은 data 이벤트로 오므로 `tr_key` 로 거른다.
"""

import asyncio
from typing import Any

import pytest

from cluefin_openapi.nhplug._socket_client import SocketClient

from ._integration_helpers import nhplug_env

pytestmark = [pytest.mark.integration, pytest.mark.realtime]

TIMEOUT_SECONDS = 30
KR_STOCK = "005930"
US_STOCK = "AAPL"


@pytest.fixture(scope="module")
def _require_prod_env() -> None:
    if nhplug_env() != "prod":
        pytest.skip("NH PLUG realtime quotes are live-only (mock socket answers WSS10006); set NHPLUG_ENV=prod")


@pytest.fixture(scope="module")
def access_token(auth) -> str:
    return auth.generate().access_token


async def _first_data(ws: SocketClient, tr_cd: str, tr_key: str) -> dict[str, Any]:
    """`tr_cd` 채널에서 `tr_key` 종목의 첫 시세 body. 장중 timeout 이면 실패한다."""

    async def wait() -> dict[str, Any]:
        async for event in ws.events():
            if event.event_type == "data" and event.tr_cd == tr_cd and event.tr_key and tr_key in event.tr_key:
                return event.data or {}
        return {}

    try:
        body = await asyncio.wait_for(wait(), timeout=TIMEOUT_SECONDS)
    except asyncio.TimeoutError:
        pytest.fail(f"No {tr_cd} data for {tr_key} within {TIMEOUT_SECONDS}s during market hours.")
    assert body, "WebSocket closed before any data arrived"
    return body


@pytest.mark.usefixtures("krx_continuous_hours", "_require_prod_env")
class TestDomestic:
    @pytest.mark.asyncio
    async def test_receive_execution(self, access_token):
        async with SocketClient(token=access_token, env="prod", market="kr") as ws:
            await ws.subscribe("oc", KR_STOCK)

            body = await _first_data(ws, "oc", KR_STOCK)

            assert body["code"] == KR_STOCK
            assert body["price"]
            assert body["time"]

    @pytest.mark.asyncio
    async def test_receive_orderbook(self, access_token):
        async with SocketClient(token=access_token, env="prod", market="kr") as ws:
            await ws.subscribe("ob", KR_STOCK)

            body = await _first_data(ws, "ob", KR_STOCK)

            assert body["code"] == KR_STOCK
            assert body["offer"]
            assert body["bid"]


@pytest.mark.usefixtures("us_market_hours", "_require_prod_env")
class TestOverseas:
    """미국 지연시세(`rc`·`rh`). 실시간(`RC`·`RH`)은 유료시세 약정 고객만 받는다.

    포털 예시는 `AAPL` 로 구독하고 푸시의 tr_key 는 `USAAAPL` 이라, tr_key 는 포함 여부로 맞춘다.
    """

    @pytest.mark.asyncio
    async def test_receive_delayed_execution(self, access_token):
        async with SocketClient(token=access_token, env="prod", market="gb") as ws:
            await ws.subscribe("rc", US_STOCK)

            body = await _first_data(ws, "rc", US_STOCK)

            assert body["gicz15"].endswith(US_STOCK)
            assert body["trdprc_1z17"]

    @pytest.mark.asyncio
    async def test_receive_delayed_orderbook(self, access_token):
        async with SocketClient(token=access_token, env="prod", market="gb") as ws:
            await ws.subscribe("rh", US_STOCK)

            body = await _first_data(ws, "rh", US_STOCK)

            assert body["gicz15"].endswith(US_STOCK)
            assert body["best_ask1z17"]
