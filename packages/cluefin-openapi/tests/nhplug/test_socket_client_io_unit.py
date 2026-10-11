"""Unit tests for NH PLUG SocketClient I/O paths with an in-memory server.

`asyncio.open_connection` is replaced by a fake that hands the client a real
`asyncio.StreamReader` (server → client bytes) and a writer that records every frame
(client → server). The fake answers the handshake with the correct
`Sec-WebSocket-Accept` computed from the key the client actually sent, so connect(),
the receive loop, subscribe/unsubscribe and close() run unmodified with no network.

NH PLUG has no heartbeat or auto-reconnect (see the module docstring); what is covered
here is ping → pong, close/EOF handling and the frame codec.
"""

import asyncio
import base64
import hashlib
import json
import re
import struct

import pytest
import pytest_asyncio

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError, NHPlugNetworkError
from cluefin_openapi.nhplug._socket_client import SocketClient, WebSocketEvent

_WS_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
_KEY_PATTERN = re.compile(rb"Sec-WebSocket-Key: (?P<key>[A-Za-z0-9+/=]+)\r\n")


def _websocket_accept(ws_key: str) -> str:
    return base64.b64encode(hashlib.sha1((ws_key + _WS_GUID).encode(), usedforsecurity=False).digest()).decode()


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


def _decode_client_frame(frame: bytes) -> tuple[int, bytes]:
    """Decode one client → server frame, asserting it is final and masked (RFC 6455 5.3)."""
    assert frame[0] & 0x80, "FIN bit must be set"
    opcode = frame[0] & 0x0F
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
    masked = frame[offset + 4 :]
    assert len(masked) == length
    return opcode, bytes(byte ^ mask_key[index % 4] for index, byte in enumerate(masked))


class FakeServerWriter:
    """Client-side writer that plays the server's part of the handshake."""

    def __init__(self, reader: asyncio.StreamReader, handshake: str = "ok"):
        self.reader = reader
        self.handshake = handshake
        self.request: bytes | None = None
        self.frames: list[bytes] = []
        self.closed = False
        self.fail_writes = False
        self.fail_wait_closed = False

    def write(self, data: bytes) -> None:
        if self.fail_writes:
            raise ConnectionResetError("peer gone")
        if self.request is None:
            self.request = data
            self.reader.feed_data(self._handshake_response(data))
        else:
            self.frames.append(data)

    def _handshake_response(self, request: bytes) -> bytes:
        match = _KEY_PATTERN.search(request)
        assert match is not None
        accept = _websocket_accept(match.group("key").decode())
        if self.handshake == "rejected":
            return b"HTTP/1.1 403 Forbidden\r\n\r\n"
        if self.handshake == "bad_accept":
            accept = _websocket_accept("some-other-key")
        return f"HTTP/1.1 101 Switching Protocols\r\nSec-WebSocket-Accept: {accept}\r\n\r\n".encode()

    async def drain(self) -> None:
        return None

    def close(self) -> None:
        self.closed = True

    async def wait_closed(self) -> None:
        if self.fail_wait_closed:
            raise ConnectionResetError("already gone")

    def decoded_frames(self) -> list[tuple[int, bytes]]:
        return [_decode_client_frame(frame) for frame in self.frames]


class FakeServer:
    """Replaces asyncio.open_connection; records the target and exposes the streams."""

    def __init__(self, handshake: str = "ok"):
        self.handshake = handshake
        self.reader: asyncio.StreamReader | None = None
        self.writer: FakeServerWriter | None = None
        self.target: tuple | None = None

    async def open_connection(self, host, port, ssl=None):
        self.target = (host, port, ssl)
        self.reader = asyncio.StreamReader()
        self.writer = FakeServerWriter(self.reader, handshake=self.handshake)
        return self.reader, self.writer

    def push(self, frame: bytes) -> None:
        assert self.reader is not None
        self.reader.feed_data(frame)


@pytest.fixture
def server(monkeypatch) -> FakeServer:
    fake = FakeServer()
    monkeypatch.setattr(asyncio, "open_connection", fake.open_connection)
    return fake


@pytest_asyncio.fixture
async def client(server):
    socket_client = SocketClient(token="test-token", env="prod", market="kr")
    await socket_client.connect()
    yield socket_client
    await socket_client.close()


def _drain_events(socket_client: SocketClient) -> list:
    events = []
    while not socket_client._event_queue.empty():
        events.append(socket_client._event_queue.get_nowait())
    return events


async def _settle() -> None:
    """Let the receive-loop task consume whatever was fed to the reader."""
    for _ in range(5):
        await asyncio.sleep(0)


class TestConnect:
    @pytest.mark.asyncio
    async def test_connect_opens_tls_to_7070_and_requests_websocket_path(self, client, server):
        host, port, ssl_context = server.target
        assert (host, port) == ("api.nhplug.com", 7070)
        assert ssl_context is not None

        request = server.writer.request.decode()
        assert request.startswith("GET /websocket HTTP/1.1\r\n")
        assert "Host: api.nhplug.com:7070\r\n" in request
        assert "Upgrade: websocket\r\n" in request
        assert "Sec-WebSocket-Version: 13\r\n" in request

        assert client.connected is True
        assert [event.event_type for event in _drain_events(client)] == ["connected"]

    @pytest.mark.parametrize(
        ("env", "market", "expected"),
        [("prod", "gb", ("api.nhplug.com", 7080)), ("dev", "kr", ("moapi.nhplug.com", 17070))],
    )
    @pytest.mark.asyncio
    async def test_connect_targets_per_env_and_market(self, server, env, market, expected):
        socket_client = SocketClient(token="t", env=env, market=market)

        await socket_client.connect()
        try:
            assert server.target[:2] == expected
        finally:
            await socket_client.close()

    @pytest.mark.asyncio
    async def test_open_connection_failure_is_wrapped(self, monkeypatch):
        async def refuse(host, port, ssl=None):
            raise OSError("connection refused")

        monkeypatch.setattr(asyncio, "open_connection", refuse)
        socket_client = SocketClient(token="t")

        with pytest.raises(NHPlugNetworkError, match="Failed to connect to WebSocket: connection refused"):
            await socket_client.connect()
        assert socket_client.connected is False

    @pytest.mark.parametrize(
        ("handshake", "message"),
        [("rejected", "WebSocket handshake failed: HTTP/1.1 403"), ("bad_accept", "invalid Sec-WebSocket-Accept")],
    )
    @pytest.mark.asyncio
    async def test_bad_handshake_fails_connect(self, server, handshake, message):
        server.handshake = handshake
        socket_client = SocketClient(token="t")

        with pytest.raises(NHPlugNetworkError, match=message):
            await socket_client.connect()
        assert socket_client.connected is False
        assert socket_client._receive_task is None

    def test_non_websocket_url_is_rejected(self):
        with pytest.raises(ValueError, match="Invalid WebSocket URL: https://api.nhplug.com"):
            SocketClient._parse_ws_url("https://api.nhplug.com")

    @pytest.mark.asyncio
    async def test_handshake_requires_open_streams(self):
        socket_client = SocketClient(token="t")

        with pytest.raises(NHPlugNetworkError, match="connection not initialized"):
            await socket_client._websocket_handshake("api.nhplug.com", 7070, "/websocket")

    @pytest.mark.asyncio
    async def test_context_manager_connects_and_closes(self, server):
        async with SocketClient(token="t") as socket_client:
            assert socket_client.connected is True

        assert socket_client.connected is False
        assert server.writer.closed is True


class TestFrameCodec:
    @pytest.mark.parametrize("size", [3, 126, 66000], ids=["short", "16bit-length", "64bit-length"])
    @pytest.mark.asyncio
    async def test_send_frame_masks_and_encodes_length(self, client, server, size):
        payload = bytes(index % 251 for index in range(size))

        await client._send_frame(payload)

        assert server.writer.decoded_frames() == [(0x1, payload)]

    @pytest.mark.asyncio
    async def test_send_frame_requires_writer(self):
        with pytest.raises(NHPlugNetworkError, match="send failed: connection not initialized"):
            await SocketClient(token="t")._send_frame(b"x")

    @pytest.mark.parametrize(
        "frame_args",
        [
            {"payload": b"hello"},
            {"payload": b"hello", "mask_key": b"\x01\x02\x03\x04"},
            {"payload": b"y" * 300},
            {"payload": b"z" * 70000},
        ],
        ids=["plain", "masked", "16bit-length", "64bit-length"],
    )
    @pytest.mark.asyncio
    async def test_receive_frame_decodes_server_frames(self, frame_args):
        socket_client = SocketClient(token="t")
        socket_client._reader = asyncio.StreamReader()
        socket_client._reader.feed_data(_server_frame(opcode=0x1, **frame_args))

        assert await socket_client._receive_frame() == (0x1, frame_args["payload"])

    @pytest.mark.asyncio
    async def test_receive_frame_requires_reader(self):
        with pytest.raises(NHPlugNetworkError, match="receive failed: connection not initialized"):
            await SocketClient(token="t")._receive_frame()


class TestReceiveLoop:
    @pytest.mark.asyncio
    async def test_text_frames_become_data_and_system_events(self, client, server):
        _drain_events(client)
        data = {"header": {"tr_cd": "mc", "tr_key": "005930"}, "body": {"cur_prc": "71000"}}
        ack = {"rsp_cd": "00000", "rsp_msg": "정상처리"}
        server.push(_server_frame(json.dumps(data).encode()))
        server.push(_server_frame(json.dumps(ack, ensure_ascii=False).encode()))

        await _settle()

        data_event, system_event = _drain_events(client)
        assert (data_event.event_type, data_event.tr_cd, data_event.tr_key) == ("data", "mc", "005930")
        assert data_event.data == {"cur_prc": "71000"}
        assert system_event.event_type == "system"
        assert json.loads(system_event.raw) == ack

    @pytest.mark.asyncio
    async def test_ping_is_answered_with_pong_carrying_the_same_payload(self, client, server):
        server.push(_server_frame(b"are-you-there", opcode=0x9))

        await _settle()

        assert server.writer.decoded_frames() == [(0xA, b"are-you-there")]
        assert client.connected is True

    @pytest.mark.asyncio
    async def test_pong_from_server_is_ignored(self, client, server):
        _drain_events(client)
        server.push(_server_frame(b"", opcode=0xA))

        await _settle()

        assert _drain_events(client) == []
        assert server.writer.frames == []
        assert client.connected is True

    @pytest.mark.asyncio
    async def test_close_frame_disconnects_and_ends_loop(self, client, server):
        _drain_events(client)
        server.push(_server_frame(b"", opcode=0x8))

        await _settle()

        assert client.connected is False
        assert client._receive_task.done()
        assert [event.event_type for event in _drain_events(client)] == ["disconnected"]

    @pytest.mark.asyncio
    async def test_connection_drop_emits_error_and_disconnects(self, client, server):
        _drain_events(client)
        server.reader.feed_eof()

        await _settle()

        assert client.connected is False
        (event,) = _drain_events(client)
        assert event.event_type == "error"
        assert isinstance(event.error, asyncio.IncompleteReadError)

    @pytest.mark.asyncio
    async def test_drop_after_local_close_emits_nothing(self, client, server):
        _drain_events(client)
        client._connected = False
        server.reader.feed_eof()

        await _settle()

        assert _drain_events(client) == []


class TestSubscribe:
    @pytest.mark.asyncio
    async def test_subscribe_sends_token_in_header_and_records_subscription(self, client, server):
        _drain_events(client)

        await client.subscribe("d2", "user01")

        ((opcode, payload),) = server.writer.decoded_frames()
        assert opcode == 0x1
        assert json.loads(payload) == {
            "header": {"token": "test-token", "tr_type": "1"},
            "body": {"tr_cd": "d2", "tr_key": "user01"},
        }
        assert client.subscriptions == {"d2:user01": "user01"}
        (event,) = _drain_events(client)
        assert (event.event_type, event.tr_cd, event.tr_key) == ("subscribed", "d2", "user01")

    @pytest.mark.asyncio
    async def test_duplicate_subscribe_sends_nothing(self, client, server):
        await client.subscribe("mc", "005930")
        _drain_events(client)

        await client.subscribe("mc", "005930")

        assert len(server.writer.frames) == 1
        assert _drain_events(client) == []

    @pytest.mark.asyncio
    async def test_unsubscribe_sends_tr_type_2_and_forgets_subscription(self, client, server):
        await client.subscribe("mc", "005930")
        _drain_events(client)

        await client.unsubscribe("mc", "005930")

        _, payload = server.writer.decoded_frames()[-1]
        assert json.loads(payload) == {
            "header": {"token": "test-token", "tr_type": "2"},
            "body": {"tr_cd": "mc", "tr_key": "005930"},
        }
        assert client.subscriptions == {}
        (event,) = _drain_events(client)
        assert (event.event_type, event.tr_cd, event.tr_key) == ("unsubscribed", "mc", "005930")

    @pytest.mark.asyncio
    async def test_unsubscribe_unknown_key_sends_nothing(self, client, server):
        await client.unsubscribe("mc", "005930")

        assert server.writer.frames == []

    @pytest.mark.parametrize("method", ["subscribe", "unsubscribe"])
    @pytest.mark.asyncio
    async def test_requires_connection(self, method):
        socket_client = SocketClient(token="t")
        call = socket_client.subscribe if method == "subscribe" else socket_client.unsubscribe

        with pytest.raises(NHPlugAPIError, match="WebSocket not connected"):
            await call("mc", "005930")

    @pytest.mark.asyncio
    async def test_rate_limit_rejects_without_sending(self, client, server, monkeypatch):
        monkeypatch.setattr(client._rate_limiter, "wait_for_tokens", lambda timeout: False)

        with pytest.raises(NHPlugAPIError, match="Subscription rate limit exceeded"):
            await client.subscribe("mc", "005930")
        assert server.writer.frames == []
        assert client.subscriptions == {}

    @pytest.mark.asyncio
    async def test_close_forgets_subscriptions_so_reconnect_can_resubscribe(self, client, server):
        await client.subscribe("mc", "005930")
        await client.close()
        assert client.subscriptions == {}

        await client.connect()
        await client.subscribe("mc", "005930")

        ((_, payload),) = server.writer.decoded_frames()
        assert json.loads(payload)["body"] == {"tr_cd": "mc", "tr_key": "005930"}

    @pytest.mark.asyncio
    async def test_reconnect_after_server_drop_resubscribes(self, client, server):
        await client.subscribe("mc", "005930")
        server.reader.feed_eof()
        await _settle()
        assert client.connected is False

        await client.connect()
        await client.subscribe("mc", "005930")

        ((_, payload),) = server.writer.decoded_frames()
        assert json.loads(payload)["body"] == {"tr_cd": "mc", "tr_key": "005930"}


class TestClose:
    @pytest.mark.asyncio
    async def test_close_sends_close_frame_and_releases_streams(self, server):
        socket_client = SocketClient(token="t")
        await socket_client.connect()
        receive_task = socket_client._receive_task

        await socket_client.close()

        assert server.writer.decoded_frames() == [(0x8, b"")]
        assert server.writer.closed is True
        assert receive_task.cancelled() or receive_task.done()
        assert socket_client._receive_task is None
        assert (socket_client._reader, socket_client._writer) == (None, None)
        assert socket_client.connected is False

    @pytest.mark.asyncio
    async def test_close_survives_a_dead_peer(self, server):
        socket_client = SocketClient(token="t", debug=True)
        try:
            await socket_client.connect()
            server.writer.fail_writes = True
            server.writer.fail_wait_closed = True

            await socket_client.close()
        finally:
            SocketClient(token="t")  # debug=False disables the nhplug logger again

        assert server.writer.closed is True
        assert socket_client._writer is None

    @pytest.mark.asyncio
    async def test_close_without_connect_is_a_noop(self):
        socket_client = SocketClient(token="t")

        await socket_client.close()

        assert socket_client.connected is False


class TestDebugLogging:
    @pytest.mark.asyncio
    async def test_full_session_with_debug_logging(self, server):
        """debug=True only adds logging; the protocol exchange must be identical."""
        socket_client = SocketClient(token="t", debug=True)
        try:
            await socket_client.connect()
            await socket_client.subscribe("mc", "005930")
            await socket_client.subscribe("mc", "005930")
            await socket_client.unsubscribe("mc", "005930")
            await socket_client.unsubscribe("mc", "005930")
            server.push(_server_frame(b"p", opcode=0x9))
            server.push(_server_frame(b"", opcode=0xA))
            server.push(_server_frame(json.dumps({"rsp_cd": "00000"}).encode()))
            server.push(_server_frame(b"", opcode=0x8))
            await _settle()
            await socket_client.close()
        finally:
            SocketClient(token="t")  # debug=False disables the nhplug logger again

        opcodes = [opcode for opcode, _ in server.writer.decoded_frames()]
        assert opcodes == [0x1, 0x1, 0xA, 0x8]
        event_types = [event.event_type for event in _drain_events(socket_client)]
        assert event_types == ["connected", "subscribed", "unsubscribed", "system", "disconnected"]


class TestEventsGenerator:
    @pytest.mark.asyncio
    async def test_events_keeps_waiting_through_idle_timeouts_while_connected(self, monkeypatch):
        socket_client = SocketClient(token="t")
        socket_client._connected = True
        late_event = WebSocketEvent(event_type="system", raw="late")
        real_wait_for = asyncio.wait_for
        calls = 0

        async def wait_for_with_one_idle_timeout(awaitable, timeout):
            nonlocal calls
            calls += 1
            if calls == 1:
                awaitable.close()
                # Server pushes something during the idle period, then the session ends.
                socket_client._event_queue.put_nowait(late_event)
                socket_client._connected = False
                raise asyncio.TimeoutError
            return await real_wait_for(awaitable, timeout)

        monkeypatch.setattr(asyncio, "wait_for", wait_for_with_one_idle_timeout)

        events = [event async for event in socket_client.events()]

        assert calls == 2
        assert [event.raw for event in events] == ["late"]
