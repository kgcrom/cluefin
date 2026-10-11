"""Unit tests for KIS SocketClient module."""

import asyncio
import base64
import json
import struct
from unittest.mock import AsyncMock, Mock

import pytest
from loguru import logger
from pydantic import SecretStr

from cluefin_openapi.kis._exceptions import KISAPIError, KISNetworkError
from cluefin_openapi.kis._socket_client import (
    MessageType,
    SocketClient,
    SubscriptionType,
    WebSocketEvent,
    WebSocketMessage,
)

MOCK_CREDENTIAL_VALUE = "test_key"


class FakeWriter:
    def __init__(self):
        self.writes = []
        self.closed = False

    def write(self, data):
        self.writes.append(data)

    async def drain(self):
        return None

    def close(self):
        self.closed = True

    async def wait_closed(self):
        return None


class FakeReader:
    def __init__(self, data: bytes = b"", handshake_response: bytes | None = None):
        self.data = bytearray(data)
        self.handshake_response = handshake_response or b""

    async def readuntil(self, separator):
        return self.handshake_response

    async def readexactly(self, size):
        chunk = bytes(self.data[:size])
        del self.data[:size]
        return chunk


# RFC 6455 section 1.3 sample handshake: a client that sends this 16-byte nonce as its key
# must get back this Sec-WebSocket-Accept. Using the spec's pair checks the client against
# an outside answer instead of re-deriving SHA1 here.
_RFC6455_NONCE = b"the sample nonce"
_RFC6455_ACCEPT = "s3pPLMBiTxaQ9kYGzzhZRbK+xOo="


def _server_frame(payload: bytes, opcode: int = 0x1, mask_key: bytes | None = None) -> bytes:
    header = bytearray([0x80 | opcode])
    length = len(payload)
    masked_bit = 0x80 if mask_key else 0
    if length <= 125:
        header.append(masked_bit | length)
    elif length <= 65535:
        header.append(masked_bit | 126)
        header.extend(struct.pack(">H", length))
    else:
        header.append(masked_bit | 127)
        header.extend(struct.pack(">Q", length))
    if mask_key:
        header.extend(mask_key)
        payload = bytes(byte ^ mask_key[index % 4] for index, byte in enumerate(payload))
    return bytes(header) + payload


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


class TestWebSocketHandshakeAndFrames:
    @pytest.mark.asyncio
    async def test_websocket_handshake_success(self, socket_client, monkeypatch):
        ws_key = base64.b64encode(_RFC6455_NONCE).decode()
        socket_client._reader = FakeReader(
            handshake_response=(
                f"HTTP/1.1 101 Switching Protocols\r\nSec-WebSocket-Accept: {_RFC6455_ACCEPT}\r\n\r\n"
            ).encode()
        )
        socket_client._writer = FakeWriter()
        monkeypatch.setattr("os.urandom", Mock(return_value=_RFC6455_NONCE))

        await socket_client._websocket_handshake("example.test", 80)

        handshake = socket_client._writer.writes[0].decode()
        assert "GET /tryitout HTTP/1.1" in handshake
        assert f"Sec-WebSocket-Key: {ws_key}" in handshake

    @pytest.mark.asyncio
    async def test_websocket_handshake_rejects_invalid_accept(self, socket_client, monkeypatch):
        socket_client._reader = FakeReader(
            handshake_response=b"HTTP/1.1 101 Switching Protocols\r\nSec-WebSocket-Accept: wrong\r\n\r\n"
        )
        socket_client._writer = FakeWriter()
        monkeypatch.setattr("os.urandom", Mock(return_value=_RFC6455_NONCE))

        with pytest.raises(KISNetworkError, match="invalid Sec-WebSocket-Accept"):
            await socket_client._websocket_handshake("example.test", 80)

    @pytest.mark.asyncio
    async def test_websocket_handshake_requires_initialized_connection(self, socket_client):
        with pytest.raises(KISNetworkError, match="connection not initialized"):
            await socket_client._websocket_handshake("example.test", 80)

    @pytest.mark.parametrize("payload", [b"abc", b"x" * 126, b"x" * 66000])
    @pytest.mark.asyncio
    async def test_send_frame_masks_payloads(self, socket_client, monkeypatch, payload):
        socket_client._writer = FakeWriter()
        monkeypatch.setattr("os.urandom", Mock(return_value=b"\x01\x02\x03\x04"))

        await socket_client._send_frame(payload)

        frame = socket_client._writer.writes[0]
        assert frame[0] == 0x81
        assert frame[-len(payload) :] != payload

    @pytest.mark.asyncio
    async def test_send_frame_requires_initialized_writer(self, socket_client):
        with pytest.raises(KISNetworkError, match="connection not initialized"):
            await socket_client._send_frame(b"payload")

    @pytest.mark.parametrize("payload", [b"abc", b"x" * 126, b"x" * 66000])
    @pytest.mark.asyncio
    async def test_receive_frame_reads_unmasked_payloads(self, socket_client, payload):
        socket_client._reader = FakeReader(_server_frame(payload, opcode=0x1))

        opcode, received_payload = await socket_client._receive_frame()

        assert opcode == 0x1
        assert received_payload == payload

    @pytest.mark.asyncio
    async def test_receive_frame_unmasks_payload(self, socket_client):
        socket_client._reader = FakeReader(_server_frame(b"masked", opcode=0x1, mask_key=b"\x01\x02\x03\x04"))

        opcode, payload = await socket_client._receive_frame()

        assert opcode == 0x1
        assert payload == b"masked"

    @pytest.mark.asyncio
    async def test_receive_frame_requires_initialized_reader(self, socket_client):
        with pytest.raises(KISNetworkError, match="connection not initialized"):
            await socket_client._receive_frame()


class TestSocketMessageHandling:
    @pytest.mark.asyncio
    async def test_handle_pingpong_sends_response(self, socket_client):
        socket_client._send_frame = AsyncMock()

        await socket_client._handle_message("PINGPONG")

        socket_client._send_frame.assert_awaited_once_with(b"PINGPONG")

    @pytest.mark.asyncio
    async def test_handle_data_message_emits_event(self, socket_client):
        await socket_client._handle_message("0|H0STASP0|001|123^456")

        event = socket_client._event_queue.get_nowait()
        assert event.event_type == "data"
        assert event.tr_id == "H0STASP0"
        assert event.data == {"values": ["123", "456"], "encrypted": False}

    @pytest.mark.asyncio
    async def test_emit_event_drops_oldest_when_queue_is_full(self):
        client = SocketClient("approval", "app", "secret", queue_maxsize=1)
        await client._emit_event(WebSocketEvent(event_type="connected"))

        await client._emit_event(WebSocketEvent(event_type="error", error=RuntimeError("boom")))

        event = client._event_queue.get_nowait()
        assert event.event_type == "error"


class TestSocketReceiveLoop:
    @pytest.mark.asyncio
    async def test_receive_loop_handles_text_and_close_frames(self, socket_client):
        frames = [(0x1, b"hello"), (0x8, b"")]
        socket_client._connected = True
        socket_client._handle_message = AsyncMock()

        async def receive_frame():
            return frames.pop(0)

        socket_client._receive_frame = receive_frame

        await socket_client._receive_loop()

        socket_client._handle_message.assert_awaited_once_with("hello")
        assert socket_client.connected is False
        assert socket_client._event_queue.get_nowait().event_type == "disconnected"

    @pytest.mark.asyncio
    async def test_receive_loop_answers_ping(self, socket_client):
        frames = [(0x9, b"ping"), (0x8, b"")]
        socket_client._connected = True
        socket_client._send_frame = AsyncMock()

        async def receive_frame():
            return frames.pop(0)

        socket_client._receive_frame = receive_frame

        await socket_client._receive_loop()

        socket_client._send_frame.assert_awaited_once_with(b"ping", opcode=0xA)

    @pytest.mark.asyncio
    async def test_receive_loop_ignores_pong(self, socket_client):
        frames = [(0xA, b"pong"), (0x8, b"")]
        socket_client._connected = True

        async def receive_frame():
            return frames.pop(0)

        socket_client._receive_frame = receive_frame

        await socket_client._receive_loop()

        assert socket_client.connected is False

    @pytest.mark.asyncio
    async def test_receive_loop_emits_errors_while_connected(self, socket_client):
        socket_client._connected = True

        async def receive_frame():
            raise RuntimeError("read failed")

        socket_client._receive_frame = receive_frame

        await socket_client._receive_loop()

        event = socket_client._event_queue.get_nowait()
        assert event.event_type == "error"
        assert isinstance(event.error, RuntimeError)
        assert socket_client.connected is False


class TestSocketSubscriptions:
    @pytest.mark.asyncio
    async def test_subscribe_requires_connection(self, socket_client):
        with pytest.raises(KISAPIError, match="not connected"):
            await socket_client.subscribe("H0STASP0", "005930")

    @pytest.mark.asyncio
    async def test_subscribe_sends_message_and_emits_event(self, socket_client):
        socket_client._connected = True
        socket_client._send_frame = AsyncMock()

        await socket_client.subscribe("H0STASP0", "005930")

        socket_client._send_frame.assert_awaited_once()
        assert socket_client.subscriptions == {"H0STASP0:005930": "005930"}
        assert socket_client._event_queue.get_nowait().event_type == "subscribed"

    @pytest.mark.asyncio
    async def test_subscribe_skips_existing_subscription(self, socket_client):
        socket_client._connected = True
        socket_client._subscriptions["H0STASP0:005930"] = "005930"
        socket_client._send_frame = AsyncMock()

        await socket_client.subscribe("H0STASP0", "005930")

        socket_client._send_frame.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_subscribe_raises_on_rate_limit(self, socket_client):
        socket_client._connected = True
        socket_client._rate_limiter.wait_for_tokens = Mock(return_value=False)

        with pytest.raises(KISAPIError, match="rate limit"):
            await socket_client.subscribe("H0STASP0", "005930")

    @pytest.mark.asyncio
    async def test_unsubscribe_requires_connection(self, socket_client):
        with pytest.raises(KISAPIError, match="not connected"):
            await socket_client.unsubscribe("H0STASP0", "005930")

    @pytest.mark.asyncio
    async def test_unsubscribe_sends_message_and_emits_event(self, socket_client):
        socket_client._connected = True
        socket_client._subscriptions["H0STASP0:005930"] = "005930"
        socket_client._send_frame = AsyncMock()

        await socket_client.unsubscribe("H0STASP0", "005930")

        socket_client._send_frame.assert_awaited_once()
        assert socket_client.subscriptions == {}
        assert socket_client._event_queue.get_nowait().event_type == "unsubscribed"

    @pytest.mark.asyncio
    async def test_unsubscribe_skips_missing_subscription(self, socket_client):
        socket_client._connected = True
        socket_client._send_frame = AsyncMock()

        await socket_client.unsubscribe("H0STASP0", "005930")

        socket_client._send_frame.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_close_forgets_subscriptions(self, socket_client):
        socket_client._connected = True
        socket_client._subscriptions["H0STASP0:005930"] = "005930"

        await socket_client.close()

        assert socket_client.subscriptions == {}

    @pytest.mark.asyncio
    async def test_reconnect_after_server_drop_resubscribes(self, socket_client, monkeypatch):
        """서버가 끊은 뒤 남은 구독 키 때문에 재연결 후 같은 구독이 전송되지 않던 문제."""
        socket_client._subscriptions["H0STASP0:005930"] = "005930"  # left over from the dropped session

        async def fake_open_connection(host, port, ssl=None):
            return FakeReader(handshake_response=_handshake_response()), FakeWriter()

        async def idle_receive_loop():
            await asyncio.Event().wait()

        monkeypatch.setattr(asyncio, "open_connection", fake_open_connection)
        monkeypatch.setattr("os.urandom", Mock(return_value=_RFC6455_NONCE))
        socket_client._receive_loop = idle_receive_loop

        await socket_client.connect()
        socket_client._send_frame = AsyncMock()
        await socket_client.subscribe("H0STASP0", "005930")

        socket_client._send_frame.assert_awaited_once()
        assert socket_client.subscriptions == {"H0STASP0:005930": "005930"}

        await socket_client.close()


class TestSocketConnectionLifecycle:
    @pytest.mark.asyncio
    async def test_events_yields_queued_events_until_empty(self, socket_client):
        await socket_client._emit_event(WebSocketEvent(event_type="connected"))

        events = [event async for event in socket_client.events()]

        assert [event.event_type for event in events] == ["connected"]

    @pytest.mark.asyncio
    async def test_close_cancels_receive_task_and_closes_writer(self, socket_client):
        async def wait_forever():
            await asyncio.sleep(60)

        socket_client._connected = True
        socket_client._writer = FakeWriter()
        socket_client._reader = FakeReader()
        socket_client._receive_task = asyncio.create_task(wait_forever())

        await socket_client.close()

        assert socket_client.connected is False
        assert socket_client._writer is None
        assert socket_client._reader is None
        assert socket_client._receive_task is None

    @pytest.mark.asyncio
    async def test_connect_rejects_invalid_websocket_url(self, socket_client):
        socket_client._ws_url = "http://not-websocket"

        with pytest.raises(KISNetworkError, match="Failed to connect"):
            await socket_client.connect()


def _decode_client_frame(frame: bytes) -> tuple[int, bytes]:
    """Unmask a client→server frame and return (opcode, payload)."""
    assert frame[1] & 0x80, "client frames must be masked"
    length = frame[1] & 0x7F
    offset = 2
    if length == 126:
        length = struct.unpack(">H", frame[2:4])[0]
        offset = 4
    elif length == 127:
        length = struct.unpack(">Q", frame[2:10])[0]
        offset = 10
    mask_key = frame[offset : offset + 4]
    payload = frame[offset + 4 : offset + 4 + length]
    assert len(payload) == length
    return frame[0] & 0x0F, bytes(byte ^ mask_key[index % 4] for index, byte in enumerate(payload))


def _handshake_response(status: bytes = b"101 Switching Protocols") -> bytes:
    return b"HTTP/1.1 " + status + b"\r\nSec-WebSocket-Accept: " + _RFC6455_ACCEPT.encode() + b"\r\n\r\n"


class TestSendFrameEncoding:
    @pytest.mark.parametrize("payload", [b"abc", b"x" * 126, b"x" * 66000])
    @pytest.mark.parametrize("opcode", [0x1, 0x8, 0xA])
    @pytest.mark.asyncio
    async def test_send_frame_round_trips_opcode_and_payload(self, socket_client, payload, opcode):
        socket_client._writer = FakeWriter()

        await socket_client._send_frame(payload, opcode=opcode)

        assert _decode_client_frame(socket_client._writer.writes[0]) == (opcode, payload)


class TestSocketConnect:
    @pytest.mark.parametrize(
        ("url", "host", "port", "use_ssl"),
        [
            ("ws://ops.koreainvestment.com:31000", "ops.koreainvestment.com", 31000, False),
            ("ws://example.test:9000/tryitout", "example.test", 9000, False),
            ("ws://example.test/tryitout", "example.test", 80, False),
            ("wss://example.test/tryitout", "example.test", 443, True),
        ],
    )
    @pytest.mark.asyncio
    async def test_connect_opens_connection_handshakes_and_starts_receive_loop(
        self, socket_client, monkeypatch, url, host, port, use_ssl
    ):
        socket_client._ws_url = url
        opened = []
        reader = FakeReader(handshake_response=_handshake_response())
        writer = FakeWriter()

        async def fake_open_connection(open_host, open_port, ssl=None):
            opened.append((open_host, open_port, ssl))
            return reader, writer

        loop_started = asyncio.Event()

        async def fake_receive_loop():
            loop_started.set()
            await asyncio.Event().wait()

        monkeypatch.setattr(asyncio, "open_connection", fake_open_connection)
        monkeypatch.setattr("os.urandom", Mock(return_value=_RFC6455_NONCE))
        socket_client._receive_loop = fake_receive_loop

        await socket_client.connect()
        await asyncio.wait_for(loop_started.wait(), timeout=1)

        [(open_host, open_port, ssl_context)] = opened
        assert (open_host, open_port) == (host, port)
        assert (ssl_context is not None) is use_ssl
        assert writer.writes[0].decode().startswith(f"GET /tryitout HTTP/1.1\r\nHost: {host}:{port}\r\n")
        assert socket_client.connected is True
        assert socket_client._event_queue.get_nowait().event_type == "connected"

        await socket_client.close()

        assert socket_client._receive_task is None
        assert writer.closed is True
        # close() sends a masked close frame after the handshake bytes
        assert _decode_client_frame(writer.writes[-1]) == (0x8, b"")

    @pytest.mark.asyncio
    async def test_connect_wraps_rejected_handshake_and_stays_disconnected(self, socket_client, monkeypatch):
        reader = FakeReader(handshake_response=b"HTTP/1.1 403 Forbidden\r\n\r\n")

        async def fake_open_connection(host, port, ssl=None):
            return reader, FakeWriter()

        monkeypatch.setattr(asyncio, "open_connection", fake_open_connection)

        with pytest.raises(KISNetworkError, match="Failed to connect to WebSocket: WebSocket handshake failed"):
            await socket_client.connect()

        assert socket_client.connected is False
        assert socket_client._receive_task is None
        assert socket_client._event_queue.empty()

    @pytest.mark.asyncio
    async def test_connect_wraps_connection_refused(self, socket_client, monkeypatch):
        async def refuse(host, port, ssl=None):
            raise ConnectionRefusedError("refused")

        monkeypatch.setattr(asyncio, "open_connection", refuse)

        with pytest.raises(KISNetworkError, match="refused") as exc_info:
            await socket_client.connect()

        assert isinstance(exc_info.value.__cause__, ConnectionRefusedError)
        assert socket_client.connected is False

    @pytest.mark.asyncio
    async def test_websocket_handshake_rejects_non_101_status(self, socket_client):
        socket_client._reader = FakeReader(handshake_response=b"HTTP/1.1 400 Bad Request\r\n\r\n")
        socket_client._writer = FakeWriter()

        with pytest.raises(KISNetworkError, match="handshake failed: HTTP/1.1 400 Bad Request"):
            await socket_client._websocket_handshake("example.test", 80)

    @pytest.mark.asyncio
    async def test_async_context_manager_connects_then_closes(self, socket_client):
        socket_client.connect = AsyncMock()
        socket_client.close = AsyncMock()

        async with socket_client as entered:
            assert entered is socket_client
            socket_client.connect.assert_awaited_once_with()
            socket_client.close.assert_not_awaited()

        socket_client.close.assert_awaited_once_with()


class TestSocketCloseAndEventsEdgeCases:
    @pytest.mark.asyncio
    async def test_close_still_releases_writer_when_close_frame_and_wait_closed_fail(self):
        client = SocketClient("approval", "app", "secret", debug=True)

        class BrokenWriter(FakeWriter):
            async def drain(self):
                raise ConnectionResetError("peer gone")

            async def wait_closed(self):
                raise ConnectionResetError("peer gone")

        writer = BrokenWriter()
        client._writer = writer
        client._reader = FakeReader()

        try:
            await client.close()
        finally:
            logger.disable("cluefin_openapi.kis")

        assert writer.closed is True
        assert client._writer is None
        assert client._reader is None

    @pytest.mark.asyncio
    async def test_events_keeps_waiting_through_timeouts_while_connected(self, socket_client, monkeypatch):
        socket_client._connected = True
        calls = []

        async def fake_wait_for(awaitable, timeout):
            calls.append(timeout)
            awaitable.close()
            if len(calls) == 2:
                socket_client._connected = False
            raise asyncio.TimeoutError

        monkeypatch.setattr(asyncio, "wait_for", fake_wait_for)

        events = [event async for event in socket_client.events()]

        assert events == []
        assert calls == [1.0, 1.0]

    @pytest.mark.asyncio
    async def test_emit_event_drops_event_when_queue_drains_concurrently(self, socket_client):
        queue = Mock()
        queue.put_nowait.side_effect = asyncio.QueueFull
        queue.get_nowait.side_effect = asyncio.QueueEmpty
        socket_client._event_queue = queue

        await socket_client._emit_event(WebSocketEvent(event_type="connected"))

        queue.put_nowait.assert_called_once()
        queue.get_nowait.assert_called_once_with()

    @pytest.mark.asyncio
    async def test_receive_loop_error_after_close_is_not_reported(self, socket_client):
        socket_client._connected = True

        async def receive_frame():
            socket_client._connected = False  # close() raced the read
            raise ConnectionResetError("closed")

        socket_client._receive_frame = receive_frame

        await socket_client._receive_loop()

        assert socket_client._event_queue.empty()

    @pytest.mark.asyncio
    async def test_receive_loop_exits_quietly_when_cancelled(self, socket_client):
        socket_client._connected = True
        reading = asyncio.Event()

        async def receive_frame():
            reading.set()
            await asyncio.Event().wait()

        socket_client._receive_frame = receive_frame
        task = asyncio.create_task(socket_client._receive_loop())
        await asyncio.wait_for(reading.wait(), timeout=1)

        task.cancel()
        await task  # CancelledError is swallowed by the loop

        assert task.done() and not task.cancelled()
        assert socket_client._event_queue.empty()


class TestSocketDebugMode:
    """debug=True only adds logging; the wire behavior must be identical."""

    @pytest.fixture
    def debug_client(self):
        client = SocketClient("approval", "app", "secret", env="dev", debug=True)
        yield client
        logger.disable("cluefin_openapi.kis")

    @pytest.mark.asyncio
    async def test_subscription_flow_in_debug_mode(self, debug_client):
        debug_client._connected = True
        debug_client._writer = FakeWriter()

        await debug_client.subscribe("H0STCNI0", "HTSID")
        await debug_client.subscribe("H0STCNI0", "HTSID")  # duplicate: no second frame
        await debug_client.unsubscribe("H0STCNI0", "HTSID")
        await debug_client.unsubscribe("H0STCNI0", "HTSID")  # already gone: no frame

        sent = [json.loads(_decode_client_frame(frame)[1]) for frame in debug_client._writer.writes]
        assert [message["header"]["tr_type"] for message in sent] == ["1", "2"]
        assert all(message["header"]["approval_key"] == "approval" for message in sent)
        assert all(message["body"]["input"] == {"tr_id": "H0STCNI0", "tr_key": "HTSID"} for message in sent)
        assert [debug_client._event_queue.get_nowait().event_type for _ in range(2)] == ["subscribed", "unsubscribed"]

    @pytest.mark.asyncio
    async def test_receive_loop_in_debug_mode(self, debug_client):
        debug_client._connected = True
        debug_client._writer = FakeWriter()
        frames = [(0x1, b"PINGPONG"), (0x9, b"hb"), (0xA, b""), (0x8, b"")]

        async def receive_frame():
            return frames.pop(0)

        debug_client._receive_frame = receive_frame

        await debug_client._receive_loop()

        replies = [_decode_client_frame(frame) for frame in debug_client._writer.writes]
        assert replies == [(0x1, b"PINGPONG"), (0xA, b"hb")]
        assert debug_client._event_queue.get_nowait().event_type == "disconnected"
        assert debug_client.connected is False

    @pytest.mark.asyncio
    async def test_handshake_in_debug_mode(self, debug_client, monkeypatch):
        debug_client._reader = FakeReader(handshake_response=_handshake_response())
        debug_client._writer = FakeWriter()
        monkeypatch.setattr("os.urandom", Mock(return_value=_RFC6455_NONCE))

        await debug_client._websocket_handshake("example.test", 80)

        assert debug_client._writer.writes[0].startswith(b"GET /tryitout HTTP/1.1\r\n")
