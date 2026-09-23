"""Unit tests for NH PLUG SocketClient (network-free logic only).

REST 소켓과 달리 인증은 header.token 에 access token 만 담는다 — approval_key 가
없다. 여기서는 네트워크 I/O 없이 검증 가능한 부분만 다룬다: 메시지 파싱,
구독/해지 메시지 조립, connected/subscriptions 상태, 이벤트 큐 처리.
"""

import json

import pytest

from cluefin_openapi.nhplug._socket_client import (
    SocketClient,
    SubscriptionType,
    WebSocketEvent,
)


@pytest.fixture
def socket_client() -> SocketClient:
    return SocketClient(token="test-token", env="prod", market="kr", debug=False)


class TestSocketClientInit:
    def test_default_state(self, socket_client):
        assert socket_client.connected is False
        assert socket_client.subscriptions == {}

    def test_prod_kr_url(self):
        client = SocketClient(token="t", env="prod", market="kr")
        assert client._ws_url == SocketClient.WS_URL_PROD_KR

    def test_prod_gb_url(self):
        client = SocketClient(token="t", env="prod", market="gb")
        assert client._ws_url == SocketClient.WS_URL_PROD_GB

    def test_dev_url_ignores_market(self):
        # dev 는 단일 주소 — market="gb" 를 줘도 동일하다.
        client = SocketClient(token="t", env="dev", market="gb")
        assert client._ws_url == SocketClient.WS_URL_DEV


class TestParseMessage:
    def test_parses_data_message(self, socket_client):
        raw = json.dumps({"header": {"tr_cd": "mc", "tr_key": "005930"}, "body": {"stck_prpr": "71000"}})

        message = socket_client._parse_message(raw)

        assert message.tr_cd == "mc"
        assert message.tr_key == "005930"
        assert message.body == {"stck_prpr": "71000"}
        assert message.raw == raw

    def test_missing_header_yields_no_tr_cd(self, socket_client):
        raw = json.dumps({"body": {"stck_prpr": "71000"}})

        message = socket_client._parse_message(raw)

        assert message.tr_cd is None
        assert message.tr_key is None
        assert message.body == {"stck_prpr": "71000"}

    def test_non_dict_body_is_dropped(self, socket_client):
        raw = json.dumps({"header": {"tr_cd": "mc", "tr_key": "005930"}, "body": ["not", "a", "dict"]})

        message = socket_client._parse_message(raw)

        assert message.tr_cd == "mc"
        assert message.body is None

    def test_missing_body_is_none(self, socket_client):
        raw = json.dumps({"header": {"tr_cd": "mc", "tr_key": "005930"}})

        message = socket_client._parse_message(raw)

        assert message.body is None

    def test_malformed_json_falls_back_to_raw(self, socket_client):
        raw = "not json at all"

        message = socket_client._parse_message(raw)

        assert message.tr_cd is None
        assert message.tr_key is None
        assert message.body is None
        assert message.raw == raw

    def test_non_dict_json_falls_back_to_raw(self, socket_client):
        raw = json.dumps(["not", "a", "dict"])

        message = socket_client._parse_message(raw)

        assert message.tr_cd is None
        assert message.raw == raw


class TestBuildSubscriptionMessage:
    def test_subscribe_message_carries_token_only(self, socket_client):
        message = socket_client._build_subscription_message("mc", "005930", SubscriptionType.SUBSCRIBE)
        parsed = json.loads(message)

        assert parsed["header"]["token"] == "test-token"
        assert parsed["header"]["tr_type"] == "1"
        assert "approval_key" not in parsed["header"]
        assert parsed["body"]["tr_cd"] == "mc"
        assert parsed["body"]["tr_key"] == "005930"

    def test_unsubscribe_message_uses_tr_type_2(self, socket_client):
        message = socket_client._build_subscription_message("mc", "005930", SubscriptionType.UNSUBSCRIBE)
        parsed = json.loads(message)

        assert parsed["header"]["tr_type"] == "2"
        assert parsed["body"]["tr_cd"] == "mc"
        assert parsed["body"]["tr_key"] == "005930"


class TestSubscriptionTypeEnum:
    def test_values(self):
        assert SubscriptionType.SUBSCRIBE.value == "1"
        assert SubscriptionType.UNSUBSCRIBE.value == "2"


class TestProperties:
    def test_connected_reflects_internal_state(self, socket_client):
        assert socket_client.connected is False
        socket_client._connected = True
        assert socket_client.connected is True

    def test_subscriptions_returns_a_copy(self, socket_client):
        socket_client._subscriptions["mc:005930"] = "005930"

        subs = socket_client.subscriptions
        subs["mb:000660"] = "000660"

        assert "mb:000660" not in socket_client._subscriptions


class TestHandleMessage:
    @pytest.mark.asyncio
    async def test_data_message_emits_data_event(self, socket_client):
        raw = json.dumps({"header": {"tr_cd": "mc", "tr_key": "005930"}, "body": {"stck_prpr": "71000"}})

        await socket_client._handle_message(raw)

        event = socket_client._event_queue.get_nowait()
        assert event.event_type == "data"
        assert event.tr_cd == "mc"
        assert event.tr_key == "005930"
        assert event.data == {"stck_prpr": "71000"}
        assert event.raw == raw

    @pytest.mark.asyncio
    async def test_message_without_tr_cd_emits_system_event(self, socket_client):
        raw = json.dumps({"rsp_cd": "00000"})

        await socket_client._handle_message(raw)

        event = socket_client._event_queue.get_nowait()
        assert event.event_type == "system"
        assert event.raw == raw


class TestEmitEvent:
    @pytest.mark.asyncio
    async def test_emit_event_drops_oldest_when_queue_is_full(self):
        client = SocketClient(token="t", queue_maxsize=1)
        await client._emit_event(WebSocketEvent(event_type="connected"))

        await client._emit_event(WebSocketEvent(event_type="error", error=RuntimeError("boom")))

        event = client._event_queue.get_nowait()
        assert event.event_type == "error"


class TestEventsGenerator:
    @pytest.mark.asyncio
    async def test_events_yields_queued_events_until_empty(self, socket_client):
        await socket_client._emit_event(WebSocketEvent(event_type="connected"))

        events = [event async for event in socket_client.events()]

        assert [event.event_type for event in events] == ["connected"]
