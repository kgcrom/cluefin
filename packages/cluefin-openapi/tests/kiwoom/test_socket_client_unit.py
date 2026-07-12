"""미국주식 WebSocket 클라이언트(``_socket_client``) unit 테스트.

실제 네트워크 없이 FakeReader/FakeWriter로 프레임 codec, LOGIN, PING 회신을 검증한다.
"""

import asyncio
import json
import struct

import pytest

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
