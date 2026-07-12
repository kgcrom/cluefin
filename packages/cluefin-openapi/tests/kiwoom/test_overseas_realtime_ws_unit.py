"""``OverseasRealtime`` 도메인 래퍼 unit 테스트.

실제 WebSocket 없이 FakeSocketClient로 등록/해지 프레임 송신과 REAL 프레임 파싱을
검증한다.
"""

import pytest
from pydantic import BaseModel

from cluefin_openapi.kiwoom._overseas_realtime import OverseasRealtime
from cluefin_openapi.kiwoom._overseas_realtime_types import (
    OverseasRealtimeExecution,
    OverseasRealtimeExecutionPrice,
    OverseasRealtimeOrderConfirmation,
    OverseasRealtimeRegisterItem,
    OverseasRealtimeTenQuotes,
)
from cluefin_openapi.kiwoom._socket_client import KiwoomWebSocketMessage


class FakeSocketClient:
    def __init__(self):
        self.sent: list[dict] = []

    async def send(self, message):
        self.sent.append(message.model_dump(by_alias=True) if isinstance(message, BaseModel) else message)


@pytest.fixture
def socket() -> FakeSocketClient:
    return FakeSocketClient()


class TestRegisterRemove:
    @pytest.mark.asyncio
    async def test_register_builds_reg_frame_from_tuples(self, socket):
        realtime = OverseasRealtime(socket)
        await realtime.register(["F5", "FT"], [("NVDA", "ND"), ("AAPL", "ND")])
        assert socket.sent[0] == {
            "trnm": "REG",
            "grp_no": "1",
            "refresh": "1",
            "data": [
                {
                    "item": [{"jmcode": "NVDA", "stex_tp": "ND"}, {"jmcode": "AAPL", "stex_tp": "ND"}],
                    "type": ["F5", "FT"],
                }
            ],
        }

    @pytest.mark.asyncio
    async def test_register_accepts_register_item_objects(self, socket):
        realtime = OverseasRealtime(socket)
        await realtime.register(["F4"], [OverseasRealtimeRegisterItem(jmcode="TSLA", stex_tp="NY")])
        assert socket.sent[0]["data"][0]["item"] == [{"jmcode": "TSLA", "stex_tp": "NY"}]

    @pytest.mark.asyncio
    async def test_remove_builds_remove_frame(self, socket):
        realtime = OverseasRealtime(socket)
        await realtime.remove(["FT"], [("AAPL", "NA")], grp_no="2")
        assert socket.sent[0] == {
            "trnm": "REMOVE",
            "grp_no": "2",
            "refresh": "0",
            "data": [{"item": [{"jmcode": "AAPL", "stex_tp": "NA"}], "type": ["FT"]}],
        }


class TestParse:
    def test_parse_dispatches_execution_frame(self):
        message = KiwoomWebSocketMessage(
            trnm="REAL",
            body={
                "trnm": "REAL",
                "data": [{"type": "F5", "item": "AAPL", "values": {"9001": "AAPL", "910": "190.00"}}],
            },
        )
        parsed = OverseasRealtime.parse(message)
        assert isinstance(parsed, OverseasRealtimeExecution)
        assert parsed.data[0].values.stock_code == "AAPL"
        assert parsed.data[0].values.execution_price == "190.00"

    def test_parse_dispatches_order_confirmation_frame(self):
        message = KiwoomWebSocketMessage(
            trnm="REAL",
            body={"trnm": "REAL", "data": [{"type": "F4", "item": "NVDA", "values": {"9001": "NVDA"}}]},
        )
        assert isinstance(OverseasRealtime.parse(message), OverseasRealtimeOrderConfirmation)

    def test_parse_dispatches_execution_price_frame(self):
        message = KiwoomWebSocketMessage(
            trnm="REAL", body={"trnm": "REAL", "data": [{"type": "FE", "item": "TSLA", "values": {"10": "250.00"}}]}
        )
        assert isinstance(OverseasRealtime.parse(message), OverseasRealtimeExecutionPrice)

    def test_parse_dispatches_ten_quotes_frame(self):
        message = KiwoomWebSocketMessage(
            trnm="REAL", body={"trnm": "REAL", "data": [{"type": "FT", "item": "NVDA", "values": {"41": "500.10"}}]}
        )
        assert isinstance(OverseasRealtime.parse(message), OverseasRealtimeTenQuotes)

    def test_parse_returns_none_for_ack_frame(self):
        """등록/해지 ACK 프레임(빈 data)은 대상 TR이 아니므로 None."""
        message = KiwoomWebSocketMessage(trnm="REG", body={"trnm": "REG", "return_code": 0, "data": []})
        assert OverseasRealtime.parse(message) is None

    def test_parse_returns_none_for_unknown_type(self):
        message = KiwoomWebSocketMessage(trnm="REAL", body={"trnm": "REAL", "data": [{"type": "0A"}]})
        assert OverseasRealtime.parse(message) is None
