"""Unit tests for KIS SocketClient module."""

import json

import pytest
from pydantic import SecretStr

from cluefin_openapi.kis._socket_client import (
    MessageType,
    SocketClient,
    SubscriptionType,
    WebSocketEvent,
    WebSocketMessage,
)

MOCK_CREDENTIAL_VALUE = "test_key"


@pytest.fixture
def socket_client() -> SocketClient:
    """Create SocketClient instance for testing."""
    return SocketClient(
        approval_key="test_approval_key",
        app_key="test_app_key",
        secret_key=SecretStr(MOCK_CREDENTIAL_VALUE),
        env="dev",
        debug=False,
    )


class TestSocketClientInit:
    """Test SocketClient initialization."""

    def test_init_with_string_secret(self):
        """Test initialization with string secret key."""
        client = SocketClient(
            approval_key="test_approval_key",
            app_key="test_app_key",
            secret_key=MOCK_CREDENTIAL_VALUE,
            env="prod",
        )
        assert client.secret_key == MOCK_CREDENTIAL_VALUE
        assert client._ws_url == SocketClient.WS_URL_PROD

    def test_init_with_secret_str(self):
        """Test initialization with SecretStr secret key."""
        client = SocketClient(
            approval_key="test_approval_key",
            app_key="test_app_key",
            secret_key=SecretStr(MOCK_CREDENTIAL_VALUE),
            env="dev",
        )
        assert client.secret_key == MOCK_CREDENTIAL_VALUE
        assert client._ws_url == SocketClient.WS_URL_DEV

    def test_init_prod_url(self):
        """Test production URL configuration."""
        client = SocketClient(
            approval_key="test",
            app_key="test",
            secret_key="test",
            env="prod",
        )
        assert client._ws_url == "ws://ops.koreainvestment.com:21000"

    def test_init_dev_url(self):
        """Test development URL configuration."""
        client = SocketClient(
            approval_key="test",
            app_key="test",
            secret_key="test",
            env="dev",
        )
        assert client._ws_url == "ws://ops.koreainvestment.com:31000"

    def test_init_default_values(self, socket_client):
        """Test default initialization values."""
        assert socket_client._connected is False
        assert socket_client._subscriptions == {}
        assert socket_client._reader is None
        assert socket_client._writer is None


class TestMessageParsing:
    """Test WebSocket message parsing."""

    def test_parse_pingpong_message(self, socket_client):
        """Test PINGPONG message parsing."""
        raw = "PINGPONG"
        message = socket_client._parse_message(raw)

        assert message.message_type == MessageType.PINGPONG
        assert message.raw == raw

    def test_parse_data_message_unencrypted(self, socket_client):
        """Test unencrypted data message parsing."""
        # Format: encrypted|tr_id|count|data
        raw = "0|H0STASP0|001|123000^124000^122000"
        message = socket_client._parse_message(raw)

        assert message.message_type == MessageType.DATA
        assert message.tr_id == "H0STASP0"
        assert message.encrypted is False
        assert message.data == ["123000", "124000", "122000"]

    def test_parse_data_message_encrypted(self, socket_client):
        """Test encrypted data message parsing."""
        raw = "1|H0STCNI0|001|encrypted_data_here"
        message = socket_client._parse_message(raw)

        assert message.message_type == MessageType.DATA
        assert message.tr_id == "H0STCNI0"
        assert message.encrypted is True
        assert message.data == ["encrypted_data_here"]

    def test_parse_system_message(self, socket_client):
        """Test unknown/system message parsing."""
        raw = "some unknown message format"
        message = socket_client._parse_message(raw)

        assert message.message_type == MessageType.SYSTEM
        assert message.raw == raw

    def test_parse_empty_data(self, socket_client):
        """Test message with empty data field."""
        raw = "0|H0STASP0|000|"
        message = socket_client._parse_message(raw)

        assert message.message_type == MessageType.DATA
        assert message.data == []  # Empty string splits to empty list


class TestSubscriptionMessage:
    """Test subscription message building."""

    def test_build_subscribe_message(self, socket_client):
        """Test subscribe message format."""
        message = socket_client._build_subscription_message("H0STASP0", "005930", SubscriptionType.SUBSCRIBE)
        parsed = json.loads(message)

        assert parsed["header"]["approval_key"] == "test_approval_key"
        assert parsed["header"]["custtype"] == "P"
        assert parsed["header"]["tr_type"] == "1"
        assert parsed["body"]["input"]["tr_id"] == "H0STASP0"
        assert parsed["body"]["input"]["tr_key"] == "005930"

    def test_build_unsubscribe_message(self, socket_client):
        """Test unsubscribe message format."""
        message = socket_client._build_subscription_message("H0STASP0", "005930", SubscriptionType.UNSUBSCRIBE)
        parsed = json.loads(message)

        assert parsed["header"]["tr_type"] == "2"
        assert parsed["body"]["input"]["tr_id"] == "H0STASP0"
        assert parsed["body"]["input"]["tr_key"] == "005930"


class TestProperties:
    """Test SocketClient properties."""

    def test_connected_property(self, socket_client):
        """Test connected property."""
        assert socket_client.connected is False
        socket_client._connected = True
        assert socket_client.connected is True

    def test_subscriptions_property(self, socket_client):
        """Test subscriptions property returns copy."""
        socket_client._subscriptions = {"H0STASP0:005930": "005930"}
        subs = socket_client.subscriptions

        # Should be a copy
        assert subs == {"H0STASP0:005930": "005930"}
        subs["new"] = "value"
        assert "new" not in socket_client._subscriptions


class TestSubscriptionType:
    """Test SubscriptionType enum."""

    def test_subscribe_value(self):
        """Test SUBSCRIBE value."""
        assert SubscriptionType.SUBSCRIBE.value == "1"

    def test_unsubscribe_value(self):
        """Test UNSUBSCRIBE value."""
        assert SubscriptionType.UNSUBSCRIBE.value == "2"


class TestWebSocketEvent:
    """Test WebSocketEvent dataclass."""

    def test_data_event(self):
        """Test data event creation."""
        event = WebSocketEvent(
            event_type="data",
            tr_id="H0STASP0",
            tr_key="005930",
            data={"values": ["123", "456"]},
        )
        assert event.event_type == "data"
        assert event.tr_id == "H0STASP0"
        assert event.data == {"values": ["123", "456"]}

    def test_error_event(self):
        """Test error event creation."""
        error = Exception("Test error")
        event = WebSocketEvent(
            event_type="error",
            error=error,
        )
        assert event.event_type == "error"
        assert event.error == error


class TestWebSocketMessage:
    """Test WebSocketMessage dataclass."""

    def test_message_creation(self):
        """Test message creation with all fields."""
        message = WebSocketMessage(
            message_type=MessageType.DATA,
            tr_id="H0STASP0",
            data=["123", "456"],
            raw="0|H0STASP0|001|123^456",
            encrypted=False,
        )
        assert message.message_type == MessageType.DATA
        assert message.tr_id == "H0STASP0"
        assert message.data == ["123", "456"]
        assert message.encrypted is False

    def test_message_defaults(self):
        """Test message with default values."""
        message = WebSocketMessage(message_type=MessageType.PINGPONG)
        assert message.tr_id is None
        assert message.data is None
        assert message.raw == ""
        assert message.encrypted is False
