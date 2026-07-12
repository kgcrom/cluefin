"""``DomesticRealtime`` 도메인 래퍼 unit 테스트.

실제 WebSocket 없이 FakeSocketClient로 등록/해지 프레임 송신과 REAL 프레임 파싱을
검증한다. (미국주식 ``test_overseas_realtime_ws_unit`` 과 대칭.)
"""

import pytest
from pydantic import BaseModel

from cluefin_openapi.kiwoom._domestic_realtime import DomesticRealtime
from cluefin_openapi.kiwoom._domestic_realtime_types import (
    DomesticRealtimeEtfNav,
    DomesticRealtimeIndustryFluctuation,
    DomesticRealtimeOrderExecution,
    DomesticRealtimeStockExecution,
    DomesticRealtimeStockQuoteRemaining,
    DomesticRealtimeViActivation,
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
    async def test_register_builds_reg_frame(self, socket):
        realtime = DomesticRealtime(socket)
        await realtime.register(["0B", "0D"], ["005930", "000660"])
        assert socket.sent[0] == {
            "trnm": "REG",
            "grp_no": "1",
            "refresh": "1",
            "data": [{"item": ["005930", "000660"], "type": ["0B", "0D"]}],
        }

    @pytest.mark.asyncio
    async def test_register_forwards_grp_no_and_refresh(self, socket):
        realtime = DomesticRealtime(socket)
        await realtime.register(["0B"], ["005930"], grp_no="3", refresh="0")
        assert socket.sent[0]["grp_no"] == "3"
        assert socket.sent[0]["refresh"] == "0"

    @pytest.mark.asyncio
    async def test_remove_builds_remove_frame(self, socket):
        realtime = DomesticRealtime(socket)
        await realtime.remove(["0D"], ["005930"], grp_no="2")
        assert socket.sent[0] == {
            "trnm": "REMOVE",
            "grp_no": "2",
            "refresh": "0",
            "data": [{"item": ["005930"], "type": ["0D"]}],
        }


class TestParse:
    def test_parse_dispatches_stock_execution_frame(self):
        message = KiwoomWebSocketMessage(
            trnm="REAL",
            body={
                "trnm": "REAL",
                "data": [
                    {
                        "type": "0B",
                        "name": "주식체결",
                        "item": "005930",
                        "values": {"20": "165208", "10": "-20800", "12": "-0.24", "13": "30379732"},
                    }
                ],
            },
        )
        parsed = DomesticRealtime.parse(message)
        assert isinstance(parsed, DomesticRealtimeStockExecution)
        values = parsed.data[0].values
        assert values.execution_time == "165208"
        assert values.current_price == "-20800"
        assert values.fluctuation_rate == "-0.24"
        assert values.acc_trade_volume == "30379732"

    def test_parse_dispatches_order_execution_frame(self):
        message = KiwoomWebSocketMessage(
            trnm="REAL",
            body={
                "trnm": "REAL",
                "data": [{"type": "00", "item": "005930", "values": {"9001": "005930", "913": "체결"}}],
            },
        )
        parsed = DomesticRealtime.parse(message)
        assert isinstance(parsed, DomesticRealtimeOrderExecution)
        assert parsed.data[0].values.stock_code == "005930"
        assert parsed.data[0].values.order_status == "체결"

    def test_parse_dispatches_etf_nav_frame(self):
        """0G(ETF NAV)와 0g(주식종목정보)는 코드 대소문자만 다르지만 FID가 완전히 다르다."""
        message = KiwoomWebSocketMessage(
            trnm="REAL",
            body={
                "trnm": "REAL",
                "data": [{"type": "0G", "item": "069500", "values": {"36": "+7488.27", "39": "0.02", "265": "-0.01"}}],
            },
        )
        parsed = DomesticRealtime.parse(message)
        assert isinstance(parsed, DomesticRealtimeEtfNav)
        assert parsed.data[0].values.nav == "+7488.27"
        assert parsed.data[0].values.tracking_error_rate == "0.02"
        assert parsed.data[0].values.nav_index_gap_rate == "-0.01"

    def test_parse_dispatches_industry_fluctuation_frame(self):
        message = KiwoomWebSocketMessage(
            trnm="REAL",
            body={"trnm": "REAL", "data": [{"type": "0U", "item": "001", "values": {"252": "46", "254": "3"}}]},
        )
        parsed = DomesticRealtime.parse(message)
        assert isinstance(parsed, DomesticRealtimeIndustryFluctuation)
        assert parsed.data[0].values.advancing_count == "46"
        assert parsed.data[0].values.lower_limit_count == "3"

    def test_parse_dispatches_quote_remaining_frame(self):
        message = KiwoomWebSocketMessage(
            trnm="REAL",
            body={"trnm": "REAL", "data": [{"type": "0D", "item": "005930", "values": {"41": "20800", "61": "1000"}}]},
        )
        parsed = DomesticRealtime.parse(message)
        assert isinstance(parsed, DomesticRealtimeStockQuoteRemaining)
        assert parsed.data[0].values.ask_price_1 == "20800"
        assert parsed.data[0].values.ask_volume_1 == "1000"

    def test_parse_dispatches_vi_activation_frame(self):
        message = KiwoomWebSocketMessage(
            trnm="REAL",
            body={
                "trnm": "REAL",
                "data": [{"type": "1h", "item": "005930", "values": {"9001": "005930", "1221": "21000"}}],
            },
        )
        parsed = DomesticRealtime.parse(message)
        assert isinstance(parsed, DomesticRealtimeViActivation)
        assert parsed.data[0].values.vi_activation_price == "21000"

    def test_parse_returns_none_for_ack_frame(self):
        """등록/해지 ACK 프레임(빈 data)은 대상 TR이 아니므로 None."""
        message = KiwoomWebSocketMessage(trnm="REG", body={"trnm": "REG", "return_code": 0, "data": []})
        assert DomesticRealtime.parse(message) is None

    def test_parse_returns_none_for_unknown_type(self):
        message = KiwoomWebSocketMessage(trnm="REAL", body={"trnm": "REAL", "data": [{"type": "ZZ"}]})
        assert DomesticRealtime.parse(message) is None
