"""``DomesticConditionSearch`` 도메인 래퍼 unit 테스트.

실제 WebSocket 없이 FakeSocketClient로 요청 프레임 송신과 응답 파싱, 그리고 실시간 푸시
프레임이 섞여 있을 때 응답 프레임만 골라내는 ``_recv_until`` 동작을 검증한다.
(미국주식 ``test_overseas_condition_search_ws_unit`` 과 대칭.)
"""

import pytest
from pydantic import BaseModel

from cluefin_openapi.kiwoom._domestic_condition_search import DomesticConditionSearch
from cluefin_openapi.kiwoom._domestic_condition_search_types import (
    DomesticConditionSearchListResponse,
    DomesticConditionSearchRealtimeCancelResponse,
    DomesticConditionSearchRealtimeResponse,
    DomesticConditionSearchResponse,
)
from cluefin_openapi.kiwoom._socket_client import KiwoomWebSocketMessage


class FakeSocketClient:
    """송신 프레임을 기록하고, 미리 큐잉한 메시지를 recv()로 반환한다."""

    def __init__(self, incoming: list[KiwoomWebSocketMessage] | None = None):
        self.sent: list[dict] = []
        self._incoming = list(incoming or [])

    async def send(self, message):
        self.sent.append(message.model_dump(by_alias=True) if isinstance(message, BaseModel) else message)

    async def recv(self) -> KiwoomWebSocketMessage:
        return self._incoming.pop(0)


def _msg(body: dict) -> KiwoomWebSocketMessage:
    return KiwoomWebSocketMessage(trnm=body.get("trnm", ""), body=body)


class TestGetConditionSearchList:
    @pytest.mark.asyncio
    async def test_sends_cnsrlst_and_parses_response(self):
        socket = FakeSocketClient(
            [_msg({"trnm": "CNSRLST", "return_code": 0, "data": [{"seq": "0", "name": "조건식1"}]})]
        )
        condition = DomesticConditionSearch(socket)

        result = await condition.get_condition_search_list()

        assert socket.sent[0] == {"trnm": "CNSRLST"}
        assert isinstance(result, DomesticConditionSearchListResponse)
        assert result.data[0].seq == "0"
        assert result.data[0].name == "조건식1"


class TestRequestConditionSearch:
    @pytest.mark.asyncio
    async def test_sends_cnsrreq_search_type_0_and_parses(self):
        socket = FakeSocketClient(
            [
                _msg(
                    {
                        "trnm": "CNSRREQ",
                        "return_code": 0,
                        "seq": "0",
                        "cont_yn": "N",
                        "next_key": "",
                        "data": [{"9001": "005930", "302": "삼성전자"}],
                    }
                )
            ]
        )
        condition = DomesticConditionSearch(socket)

        result = await condition.request_condition_search(seq="0")

        assert socket.sent[0] == {
            "trnm": "CNSRREQ",
            "seq": "0",
            "search_type": "0",
            "stex_tp": "K",
            "cont_yn": "N",
            "next_key": "",
        }
        assert isinstance(result, DomesticConditionSearchResponse)
        assert result.data[0].stock_code == "005930"
        assert result.data[0].stock_name == "삼성전자"

    @pytest.mark.asyncio
    async def test_continuation_params_are_forwarded(self):
        socket = FakeSocketClient([_msg({"trnm": "CNSRREQ", "return_code": 0, "seq": "0", "data": []})])
        condition = DomesticConditionSearch(socket)

        await condition.request_condition_search(seq="0", cont_yn="Y", next_key="000123")

        assert socket.sent[0]["cont_yn"] == "Y"
        assert socket.sent[0]["next_key"] == "000123"


class TestRealtimeConditionSearch:
    @pytest.mark.asyncio
    async def test_request_realtime_sends_search_type_1(self):
        socket = FakeSocketClient([_msg({"trnm": "CNSRREQ", "seq": "0", "data": [{"jmcode": "005930"}]})])
        condition = DomesticConditionSearch(socket)

        result = await condition.request_realtime_condition_search(seq="0")

        assert socket.sent[0] == {"trnm": "CNSRREQ", "seq": "0", "search_type": "1", "stex_tp": "K"}
        assert isinstance(result, DomesticConditionSearchRealtimeResponse)
        assert result.data[0].jmcode == "005930"

    @pytest.mark.asyncio
    async def test_recv_until_skips_interleaved_real_frames(self):
        """실시간 푸시 프레임(REAL)이 먼저 와도 CNSRREQ 응답만 골라 반환한다."""
        socket = FakeSocketClient(
            [
                _msg({"trnm": "REAL", "data": [{"type": "0A", "name": "005930", "values": {"9001": "A005930"}}]}),
                _msg({"trnm": "CNSRREQ", "seq": "0", "data": []}),
            ]
        )
        condition = DomesticConditionSearch(socket)

        result = await condition.request_realtime_condition_search(seq="0")

        assert isinstance(result, DomesticConditionSearchRealtimeResponse)
        assert result.seq == "0"

    @pytest.mark.asyncio
    async def test_cancel_sends_cnsrclr_and_parses_ack(self):
        socket = FakeSocketClient([_msg({"trnm": "CNSRCLR", "return_code": 0, "return_msg": "", "seq": "0"})])
        condition = DomesticConditionSearch(socket)

        result = await condition.cancel_realtime_condition_search(seq="0")

        assert socket.sent[0] == {"trnm": "CNSRCLR", "seq": "0"}
        assert isinstance(result, DomesticConditionSearchRealtimeCancelResponse)
        assert result.return_code == 0
        assert result.seq == "0"
