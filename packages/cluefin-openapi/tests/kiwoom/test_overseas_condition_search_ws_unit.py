"""``OverseasConditionSearch`` 도메인 래퍼 unit 테스트.

실제 WebSocket 없이 FakeSocketClient로 요청 프레임 송신과 응답 파싱, 그리고 실시간 푸시
프레임이 섞여 있을 때 응답 프레임만 골라내는 ``_recv_until`` 동작을 검증한다.
"""

import pytest
from pydantic import BaseModel

from cluefin_openapi.kiwoom._overseas_condition_search import OverseasConditionSearch
from cluefin_openapi.kiwoom._overseas_condition_search_types import (
    OverseasConditionSearchListResponse,
    OverseasConditionSearchRealtimeCancelResponse,
    OverseasConditionSearchRealtimeResponse,
    OverseasConditionSearchResponse,
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
    async def test_sends_gcnsrlst_and_parses_response(self):
        socket = FakeSocketClient(
            [_msg({"trnm": "GCNSRLST", "return_code": 0, "data": [{"seq": "0", "name": "조건식1"}]})]
        )
        condition = OverseasConditionSearch(socket)

        result = await condition.get_condition_search_list()

        assert socket.sent[0] == {"trnm": "GCNSRLST"}
        assert isinstance(result, OverseasConditionSearchListResponse)
        assert result.data[0].seq == "0"
        assert result.data[0].name == "조건식1"


class TestRequestConditionSearch:
    @pytest.mark.asyncio
    async def test_sends_gcnsrreq_search_type_0_and_parses(self):
        socket = FakeSocketClient(
            [
                _msg(
                    {
                        "trnm": "GCNSRREQ",
                        "return_code": 0,
                        "seq": "0",
                        "cont_yn": "N",
                        "next_key": "",
                        "data": [{"9001": "NVDA", "302": "엔비디아"}],
                    }
                )
            ]
        )
        condition = OverseasConditionSearch(socket)

        result = await condition.request_condition_search(seq="0")

        assert socket.sent[0] == {
            "trnm": "GCNSRREQ",
            "seq": "0",
            "search_type": "0",
            "cont_yn": "N",
            "next_key": "",
        }
        assert isinstance(result, OverseasConditionSearchResponse)
        assert result.data[0].stock_code == "NVDA"
        assert result.data[0].stock_name == "엔비디아"

    @pytest.mark.asyncio
    async def test_continuation_params_are_forwarded(self):
        socket = FakeSocketClient([_msg({"trnm": "GCNSRREQ", "return_code": 0, "seq": "0", "data": []})])
        condition = OverseasConditionSearch(socket)

        await condition.request_condition_search(seq="0", cont_yn="Y", next_key="000123")

        assert socket.sent[0]["cont_yn"] == "Y"
        assert socket.sent[0]["next_key"] == "000123"


class TestRealtimeConditionSearch:
    @pytest.mark.asyncio
    async def test_request_realtime_sends_search_type_1(self):
        socket = FakeSocketClient(
            [_msg({"trnm": "GCNSRREQ", "seq": "0", "data": [{"jmcode": "AAPL", "stexTp": "ND"}]})]
        )
        condition = OverseasConditionSearch(socket)

        result = await condition.request_realtime_condition_search(seq="0")

        assert socket.sent[0] == {"trnm": "GCNSRREQ", "seq": "0", "search_type": "1"}
        assert isinstance(result, OverseasConditionSearchRealtimeResponse)
        assert result.data[0].jmcode == "AAPL"
        assert result.data[0].stex_tp == "ND"

    @pytest.mark.asyncio
    async def test_recv_until_skips_interleaved_real_frames(self):
        """실시간 푸시 프레임(REAL)이 먼저 와도 GCNSRREQ 응답만 골라 반환한다."""
        socket = FakeSocketClient(
            [
                _msg({"trnm": "REAL", "data": [{"type": "FE"}]}),
                _msg({"trnm": "GCNSRREQ", "seq": "0", "data": []}),
            ]
        )
        condition = OverseasConditionSearch(socket)

        result = await condition.request_realtime_condition_search(seq="0")

        assert isinstance(result, OverseasConditionSearchRealtimeResponse)
        assert result.seq == "0"

    @pytest.mark.asyncio
    async def test_cancel_sends_gcnsrclr_and_parses_ack(self):
        socket = FakeSocketClient([_msg({"trnm": "GCNSRCLR", "return_code": 0, "return_msg": "", "seq": "0"})])
        condition = OverseasConditionSearch(socket)

        result = await condition.cancel_realtime_condition_search(seq="0")

        assert socket.sent[0] == {"trnm": "GCNSRCLR", "seq": "0"}
        assert isinstance(result, OverseasConditionSearchRealtimeCancelResponse)
        assert result.return_code == 0
        assert result.seq == "0"
