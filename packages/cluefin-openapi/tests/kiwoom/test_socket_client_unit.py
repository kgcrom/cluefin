"""미국주식 WebSocket 클라이언트(``_socket_client``) unit 테스트.

실제 네트워크 없이 FakeReader/FakeWriter로 프레임 codec, LOGIN, PING 회신을 검증한다.
"""

import asyncio
import base64
import contextlib
import hashlib
import json
import ssl
import struct
from unittest.mock import Mock

import pytest
from loguru import logger

from cluefin_openapi.kiwoom._exceptions import KiwoomAPIError, KiwoomNetworkError
from cluefin_openapi.kiwoom._socket_client import KiwoomWebSocketClient, KiwoomWebSocketMessage


class FakeWriter:
    def __init__(self):
        self.writes: list[bytes] = []
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
        if len(self.data) < size:
            raise asyncio.IncompleteReadError(bytes(self.data), size)
        chunk = bytes(self.data[:size])
        del self.data[:size]
        return chunk


def _server_frame(payload: bytes, opcode: int = 0x1) -> bytes:
    """서버→클라이언트 프레임(마스킹 없음)을 만든다."""
    header = bytearray([0x80 | opcode])
    length = len(payload)
    if length <= 125:
        header.append(length)
    elif length <= 65535:
        header.append(126)
        header.extend(struct.pack(">H", length))
    else:
        header.append(127)
        header.extend(struct.pack(">Q", length))
    return bytes(header) + payload


def _json_frame(obj: dict) -> bytes:
    return _server_frame(json.dumps(obj).encode("utf-8"))


def _decode_client_frame(frame: bytes) -> dict:
    """클라이언트가 송신한 마스킹된 텍스트 프레임을 언마스킹해 JSON으로 되돌린다."""
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
    unmasked = bytes(byte ^ mask_key[i % 4] for i, byte in enumerate(payload))
    return json.loads(unmasked.decode("utf-8"))


@pytest.fixture
def client() -> KiwoomWebSocketClient:
    return KiwoomWebSocketClient(token="test-token", env="dev")


class TestFraming:
    @pytest.mark.parametrize("payload", [b"abc", b"x" * 126, b"x" * 66000])
    @pytest.mark.asyncio
    async def test_send_frame_masks_payload(self, client, payload):
        client._writer = FakeWriter()
        await client._send_frame(payload)
        sent = client._writer.writes[0]
        assert sent[0] == 0x81  # FIN + text
        assert sent[1] & 0x80  # mask bit set

    @pytest.mark.asyncio
    async def test_send_frame_requires_writer(self, client):
        with pytest.raises(KiwoomNetworkError):
            await client._send_frame(b"abc")

    @pytest.mark.parametrize("payload", [b"abc", b"x" * 126, b"x" * 66000])
    @pytest.mark.asyncio
    async def test_receive_frame_reads_unmasked(self, client, payload):
        client._reader = FakeReader(_server_frame(payload))
        opcode, received = await client._receive_frame()
        assert opcode == 0x1
        assert received == payload

    @pytest.mark.asyncio
    async def test_recv_json_parses_text_frame(self, client):
        client._reader = FakeReader(_json_frame({"trnm": "REAL", "data": []}))
        message = await client._recv_json()
        assert isinstance(message, KiwoomWebSocketMessage)
        assert message.trnm == "REAL"
        assert message.body == {"trnm": "REAL", "data": []}

    @pytest.mark.asyncio
    async def test_recv_json_answers_protocol_ping(self, client):
        client._writer = FakeWriter()
        client._reader = FakeReader(_server_frame(b"", opcode=0x9) + _json_frame({"trnm": "REAL"}))
        message = await client._recv_json()
        assert message.trnm == "REAL"
        # protocol ping(0x9) 수신시 pong(0xA)을 회신했는지 확인
        assert client._writer.writes[0][0] == 0x80 | 0xA

    @pytest.mark.asyncio
    async def test_recv_json_close_frame_raises(self, client):
        client._connected = True
        client._reader = FakeReader(_server_frame(b"", opcode=0x8))
        with pytest.raises(KiwoomNetworkError):
            await client._recv_json()
        assert client._connected is False


class TestLogin:
    @pytest.mark.asyncio
    async def test_login_success(self, client):
        client._writer = FakeWriter()
        client._reader = FakeReader(_json_frame({"trnm": "LOGIN", "return_code": 0, "return_msg": ""}))
        await client._login()
        sent = _decode_client_frame(client._writer.writes[0])
        assert sent == {"trnm": "LOGIN", "token": "test-token"}

    @pytest.mark.asyncio
    async def test_login_failure_raises(self, client):
        client._writer = FakeWriter()
        client._reader = FakeReader(_json_frame({"trnm": "LOGIN", "return_code": 1, "return_msg": "인증 실패"}))
        with pytest.raises(KiwoomAPIError, match="인증 실패"):
            await client._login()

    @pytest.mark.asyncio
    async def test_login_echoes_ping_before_login(self, client):
        client._writer = FakeWriter()
        client._reader = FakeReader(
            _json_frame({"trnm": "PING", "seq": "1"}) + _json_frame({"trnm": "LOGIN", "return_code": 0})
        )
        await client._login()
        # LOGIN 요청 1회 + PING 회신 1회 = 2회 송신
        assert len(client._writer.writes) == 2


class TestReceiveLoop:
    @pytest.mark.asyncio
    async def test_receive_loop_echoes_ping_and_queues_real(self, client):
        client._writer = FakeWriter()
        client._reader = FakeReader(
            _json_frame({"trnm": "PING", "seq": "1"}) + _json_frame({"trnm": "REAL", "data": [{"type": "F5"}]})
        )
        client._connected = True
        await client._receive_loop()  # reader 소진 후 IncompleteReadError로 종료
        message = await client.recv()
        assert message.trnm == "REAL"
        # PING 회신이 송신되었는지
        assert len(client._writer.writes) == 1

    @pytest.mark.asyncio
    async def test_emit_drops_oldest_when_full(self):
        client = KiwoomWebSocketClient(token="t", env="dev", queue_maxsize=1)
        await client._emit(KiwoomWebSocketMessage(trnm="A"))
        await client._emit(KiwoomWebSocketMessage(trnm="B"))
        message = await client.recv()
        assert message.trnm == "B"


class TestEvents:
    @pytest.mark.asyncio
    async def test_events_yields_queued_messages_in_order(self, client):
        await client._emit(KiwoomWebSocketMessage(trnm="A"))
        await client._emit(KiwoomWebSocketMessage(trnm="B"))
        client._connected = True

        received: list[str] = []
        async for message in client.events():
            received.append(message.trnm)
            if len(received) == 2:
                # 큐가 비었으니 연결을 끊어 제너레이터가 종료되도록 한다.
                client._connected = False

        assert received == ["A", "B"]

    @pytest.mark.asyncio
    async def test_events_terminates_immediately_when_disconnected_and_queue_empty(self, client):
        client._connected = False
        received = [message async for message in client.events()]
        assert received == []


class TestSend:
    @pytest.mark.asyncio
    async def test_send_serializes_pydantic_by_alias(self, client):
        from cluefin_openapi.kiwoom._overseas_realtime_types import (
            OverseasRealtimeRegisterData,
            OverseasRealtimeRegisterItem,
            OverseasRealtimeRequest,
        )

        client._writer = FakeWriter()
        request = OverseasRealtimeRequest(
            trnm="REG",
            grp_no="1",
            refresh="1",
            data=[
                OverseasRealtimeRegisterData(
                    item=[OverseasRealtimeRegisterItem(jmcode="NVDA", stex_tp="ND")], type=["F5"]
                )
            ],
        )
        await client.send(request)
        assert _decode_client_frame(client._writer.writes[0]) == {
            "trnm": "REG",
            "grp_no": "1",
            "refresh": "1",
            "data": [{"item": [{"jmcode": "NVDA", "stex_tp": "ND"}], "type": ["F5"]}],
        }


class TestConnect:
    @pytest.mark.asyncio
    async def test_connect_performs_handshake_login_and_starts_loop(self, client, monkeypatch):
        writer = FakeWriter()
        # 핸드셰이크 응답에 올바른 Sec-WebSocket-Accept를 넣기 위해 검증을 우회한다.
        reader = FakeReader(
            _json_frame({"trnm": "LOGIN", "return_code": 0}),
            handshake_response=b"HTTP/1.1 101 Switching Protocols\r\n\r\n",
        )

        async def fake_open_connection(host, port, ssl=None):
            return reader, writer

        monkeypatch.setattr(asyncio, "open_connection", fake_open_connection)
        monkeypatch.setattr(client, "_websocket_handshake", _noop_handshake)

        await client.connect()
        assert client.connected is True
        assert client._receive_task is not None
        await client.close()
        assert client.connected is False


async def _noop_handshake(*args, **kwargs):
    return None


def _websocket_accept(ws_key_bytes: bytes) -> str:
    ws_key = base64.b64encode(ws_key_bytes).decode()
    return base64.b64encode(
        hashlib.sha1(
            (ws_key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode(),
            usedforsecurity=False,
        ).digest()
    ).decode()


def _handshake_response(status: bytes = b"101 Switching Protocols") -> bytes:
    return b"HTTP/1.1 " + status + b"\r\nSec-WebSocket-Accept: " + _websocket_accept(b"0" * 16).encode() + b"\r\n\r\n"


def _client_opcode(frame: bytes) -> int:
    return frame[0] & 0x0F


@pytest.fixture
def debug_client():
    client = KiwoomWebSocketClient(token="test-token", env="dev", market="domestic", debug=True)
    yield client
    logger.disable("cluefin_openapi.kiwoom")


class TestConnectEndToEnd:
    @pytest.mark.parametrize(
        ("env", "market", "host", "path"),
        [
            ("dev", "domestic", "mockapi.kiwoom.com", "/api/dostk/websocket"),
            ("prod", "overseas", "api.kiwoom.com", "/api/us/websocket"),
        ],
    )
    @pytest.mark.asyncio
    async def test_connect_handshakes_logs_in_and_queues_frames(self, monkeypatch, env, market, host, path):
        client = KiwoomWebSocketClient(token="test-token", env=env, market=market)
        writer = FakeWriter()
        reader = FakeReader(
            _json_frame({"trnm": "LOGIN", "return_code": "0"}) + _json_frame({"trnm": "REAL", "data": []}),
            handshake_response=_handshake_response(),
        )
        opened = []

        async def fake_open_connection(open_host, open_port, ssl=None):
            opened.append((open_host, open_port, ssl))
            return reader, writer

        monkeypatch.setattr(asyncio, "open_connection", fake_open_connection)
        # deterministic handshake key (16 bytes) and frame masks (4 bytes)
        monkeypatch.setattr("os.urandom", lambda size: b"0" * size)

        async with client:
            assert client.connected is True
            message = await asyncio.wait_for(client.recv(), timeout=1)

        [(open_host, open_port, ssl_context)] = opened
        assert (open_host, open_port) == (host, 10000)
        assert isinstance(ssl_context, ssl.SSLContext)
        assert writer.writes[0].decode().startswith(f"GET {path} HTTP/1.1\r\nHost: {host}:10000\r\n")
        assert _decode_client_frame(writer.writes[1]) == {"trnm": "LOGIN", "token": "test-token"}
        assert message.trnm == "REAL"
        # __aexit__ closed the socket with a close frame
        assert _client_opcode(writer.writes[-1]) == 0x8
        assert writer.closed is True
        assert client.connected is False

    @pytest.mark.parametrize("error", [ConnectionRefusedError("refused"), asyncio.IncompleteReadError(b"", 2)])
    @pytest.mark.asyncio
    async def test_connect_wraps_transport_errors(self, client, monkeypatch, error):
        async def fail(host, port, ssl=None):
            raise error

        monkeypatch.setattr(asyncio, "open_connection", fail)

        with pytest.raises(KiwoomNetworkError, match="Failed to connect to WebSocket") as exc_info:
            await client.connect()

        assert exc_info.value.__cause__ is error
        assert client.connected is False
        assert client._receive_task is None

    @pytest.mark.asyncio
    async def test_connect_login_rejection_leaves_client_disconnected(self, client, monkeypatch):
        reader = FakeReader(_json_frame({"trnm": "LOGIN", "return_code": 8005, "return_msg": "토큰 만료"}))

        async def fake_open_connection(host, port, ssl=None):
            return reader, FakeWriter()

        monkeypatch.setattr(asyncio, "open_connection", fake_open_connection)
        monkeypatch.setattr(client, "_websocket_handshake", _noop_handshake)

        with pytest.raises(KiwoomAPIError, match="토큰 만료") as exc_info:
            await client.connect()

        assert exc_info.value.response_data["return_code"] == 8005
        assert client.connected is False
        assert client._receive_task is None


class TestHandshake:
    @pytest.mark.asyncio
    async def test_handshake_accepts_valid_response(self, client, monkeypatch):
        client._writer = FakeWriter()
        client._reader = FakeReader(handshake_response=_handshake_response())
        monkeypatch.setattr("os.urandom", Mock(return_value=b"0" * 16))

        await client._websocket_handshake("api.kiwoom.com", 10000, "/api/us/websocket")

        request = client._writer.writes[0].decode()
        assert f"Sec-WebSocket-Key: {base64.b64encode(b'0' * 16).decode()}\r\n" in request
        assert "Sec-WebSocket-Version: 13\r\n" in request

    @pytest.mark.asyncio
    async def test_handshake_rejects_non_101_status(self, client):
        client._writer = FakeWriter()
        client._reader = FakeReader(handshake_response=b"HTTP/1.1 401 Unauthorized\r\n\r\n")

        with pytest.raises(KiwoomNetworkError, match="handshake failed: HTTP/1.1 401 Unauthorized"):
            await client._websocket_handshake("api.kiwoom.com", 10000, "/")

    @pytest.mark.asyncio
    async def test_handshake_rejects_wrong_accept(self, client, monkeypatch):
        client._writer = FakeWriter()
        client._reader = FakeReader(handshake_response=_handshake_response())
        monkeypatch.setattr("os.urandom", Mock(return_value=b"1" * 16))  # key no longer matches the accept

        with pytest.raises(KiwoomNetworkError, match="invalid Sec-WebSocket-Accept"):
            await client._websocket_handshake("api.kiwoom.com", 10000, "/")

    @pytest.mark.asyncio
    async def test_handshake_requires_connection(self, client):
        with pytest.raises(KiwoomNetworkError, match="connection not initialized"):
            await client._websocket_handshake("api.kiwoom.com", 10000, "/")


class TestFramingEdgeCases:
    @pytest.mark.asyncio
    async def test_receive_frame_requires_reader(self, client):
        with pytest.raises(KiwoomNetworkError, match="connection not initialized"):
            await client._receive_frame()

    @pytest.mark.asyncio
    async def test_receive_frame_unmasks_masked_payload(self, client):
        mask_key = b"\x01\x02\x03\x04"
        payload = b"masked"
        masked = bytes(byte ^ mask_key[index % 4] for index, byte in enumerate(payload))
        client._reader = FakeReader(bytes([0x81, 0x80 | len(payload)]) + mask_key + masked)

        assert await client._receive_frame() == (0x1, payload)

    @pytest.mark.asyncio
    async def test_recv_json_skips_pong_and_reads_binary_frame(self, client):
        client._reader = FakeReader(
            _server_frame(b"", opcode=0xA) + _server_frame(json.dumps({"trnm": "CNSRLST"}).encode(), opcode=0x2)
        )

        message = await client._recv_json()

        assert message.trnm == "CNSRLST"

    @pytest.mark.asyncio
    async def test_recv_json_non_object_body_becomes_empty(self, client):
        client._reader = FakeReader(_server_frame(b"[1, 2]"))

        message = await client._recv_json()

        assert (message.trnm, message.body, message.raw) == ("", {}, "[1, 2]")


class TestLoginEdgeCases:
    @pytest.mark.asyncio
    async def test_login_ignores_unexpected_frames_before_login(self, debug_client):
        debug_client._writer = FakeWriter()
        debug_client._reader = FakeReader(
            _json_frame({"trnm": "REAL", "data": []}) + _json_frame({"trnm": "LOGIN", "return_code": 0})
        )

        await debug_client._login()

        # only the LOGIN request was sent; the stray REAL frame got no reply
        assert len(debug_client._writer.writes) == 1

    @pytest.mark.asyncio
    async def test_login_failure_without_message_reports_unknown(self, client):
        client._writer = FakeWriter()
        client._reader = FakeReader(_json_frame({"trnm": "LOGIN", "return_code": 1}))

        with pytest.raises(KiwoomAPIError, match="WebSocket LOGIN failed: unknown error"):
            await client._login()


class TestSendEdgeCases:
    @pytest.mark.asyncio
    async def test_send_raises_when_rate_limited_and_sends_nothing(self, client):
        client._writer = FakeWriter()
        client._rate_limiter.wait_for_tokens = Mock(return_value=False)

        with pytest.raises(KiwoomAPIError, match="rate limit exceeded"):
            await client.send({"trnm": "REG"})

        assert client._writer.writes == []

    @pytest.mark.asyncio
    async def test_send_dict_in_debug_mode(self, debug_client):
        debug_client._writer = FakeWriter()

        await debug_client.send({"trnm": "REMOVE", "grp_no": "1"})

        assert _decode_client_frame(debug_client._writer.writes[0]) == {"trnm": "REMOVE", "grp_no": "1"}


class TestLifecycleEdgeCases:
    @pytest.mark.asyncio
    async def test_close_releases_writer_even_if_close_frame_and_wait_closed_fail(self, debug_client):
        class BrokenWriter(FakeWriter):
            async def drain(self):
                raise ConnectionResetError("peer gone")

            async def wait_closed(self):
                raise ConnectionResetError("peer gone")

        writer = BrokenWriter()
        debug_client._writer = writer
        debug_client._reader = FakeReader()
        debug_client._connected = True

        await debug_client.close()

        assert writer.closed is True
        assert debug_client._writer is None
        assert debug_client._reader is None
        assert debug_client.connected is False

    @pytest.mark.asyncio
    async def test_receive_loop_exits_quietly_when_cancelled(self, client):
        client._connected = True
        reading = asyncio.Event()

        async def recv_json():
            reading.set()
            await asyncio.Event().wait()

        client._recv_json = recv_json
        task = asyncio.create_task(client._receive_loop())
        await asyncio.wait_for(reading.wait(), timeout=1)

        task.cancel()
        await task

        assert task.done() and not task.cancelled()
        assert client.connected is True  # cancellation is close()'s job, not a receive error

    @pytest.mark.asyncio
    async def test_receive_loop_marks_disconnected_on_server_close(self, client):
        client._connected = True
        client._reader = FakeReader(_json_frame({"trnm": "REAL"}) + _server_frame(b"", opcode=0x8))

        # The loop currently lets KiwoomNetworkError escape on a server close frame; only the
        # state change and the already-queued frame are pinned here.
        with contextlib.suppress(KiwoomNetworkError):
            await client._receive_loop()

        assert client.connected is False
        assert (await client.recv()).trnm == "REAL"

    @pytest.mark.asyncio
    async def test_events_keeps_waiting_through_timeouts_while_connected(self, client, monkeypatch):
        client._connected = True
        calls = []

        async def fake_wait_for(awaitable, timeout):
            calls.append(timeout)
            awaitable.close()
            if len(calls) == 2:
                client._connected = False
            raise asyncio.TimeoutError

        monkeypatch.setattr(asyncio, "wait_for", fake_wait_for)

        received = [message async for message in client.events()]

        assert received == []
        assert calls == [1.0, 1.0]

    @pytest.mark.asyncio
    async def test_emit_drops_message_when_queue_drains_concurrently(self, client):
        queue = Mock()
        queue.put_nowait.side_effect = asyncio.QueueFull
        queue.get_nowait.side_effect = asyncio.QueueEmpty
        client._event_queue = queue

        await client._emit(KiwoomWebSocketMessage(trnm="REAL"))

        queue.put_nowait.assert_called_once()
        queue.get_nowait.assert_called_once_with()
