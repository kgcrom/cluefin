"""키움 실시간 WebSocket 클라이언트.

미국주식 실시간 시세(``_overseas_realtime``)/조건검색(``_overseas_condition_search``)과
국내주식 조건검색(``_domestic_condition_search``)이 공유하는 저수준 WebSocket 클라이언트다.
Python 표준 라이브러리(asyncio)만 사용하며 외부 의존성을 추가하지 않는다
(KIS ``_socket_client``와 동일한 방식).

WebSocket URL은 ``market``으로 국내(dostk)/미국(us) 엔드포인트를 선택한다:
- 미국 운영: wss://api.kiwoom.com:10000/api/us/websocket
- 미국 모의투자: wss://mockapi.kiwoom.com:10000/api/us/websocket
- 국내 운영: wss://api.kiwoom.com:10000/api/dostk/websocket
- 국내 모의투자: wss://mockapi.kiwoom.com:10000/api/dostk/websocket (KRX만 지원)

프로토콜 (JSON 텍스트 프레임):
- 접속 후 ``{"trnm": "LOGIN", "token": <access_token>}`` 전송 → LOGIN 응답(return_code) 수신
- 서버가 주기적으로 ``{"trnm": "PING", ...}`` 전송 → 받은 프레임을 그대로 회신
- REG/REMOVE(실시간 등록/해지), GCNSRLST/GCNSRREQ/GCNSRCLR(조건검색) 프레임 송신
- ``{"trnm": "REAL", ...}`` 실시간 푸시 및 각 요청에 대한 응답 프레임 수신
"""

import asyncio
import base64
import hashlib
import json
import os
import ssl
import struct
from dataclasses import dataclass, field
from typing import Any, Dict, Literal, Optional, Union
from urllib.parse import urlparse

from loguru import logger
from pydantic import BaseModel

from cluefin_openapi._rate_limiter import TokenBucket

from ._exceptions import KiwoomAPIError, KiwoomNetworkError


@dataclass
class KiwoomWebSocketMessage:
    """수신한 WebSocket 프레임 (파싱된 JSON)."""

    trnm: str
    body: Dict[str, Any] = field(default_factory=dict)
    raw: str = ""


class KiwoomWebSocketClient:
    """키움 실시간 WebSocket 클라이언트.

    LOGIN 인증과 PING/PONG 유지는 이 클라이언트가 처리하고, 그 외 프레임은 이벤트 큐로
    전달한다. ``OverseasRealtime``/``OverseasConditionSearch``/``DomesticConditionSearch``가
    이 클라이언트를 감싸 도메인별 요청 프레임을 송신하고 응답을 파싱한다. 접속 URL은
    ``market``으로 국내(dostk)/미국(us) 엔드포인트를 선택한다.

    Example:
        ```python
        # 미국주식 조건검색
        async with KiwoomWebSocketClient(token="...", env="prod") as ws:
            await ws.send({"trnm": "GCNSRLST"})
            message = await ws.recv()
            print(message.trnm, message.body)

        # 국내주식 조건검색
        async with KiwoomWebSocketClient(token="...", env="prod", market="domestic") as ws:
            await ws.send({"trnm": "CNSRLST"})
            message = await ws.recv()
        ```
    """

    WS_HOST_PROD = "wss://api.kiwoom.com:10000"
    WS_HOST_DEV = "wss://mockapi.kiwoom.com:10000"
    WS_PATH = {"domestic": "/api/dostk/websocket", "overseas": "/api/us/websocket"}

    def __init__(
        self,
        token: str,
        env: Literal["dev", "prod"] = "prod",
        market: Literal["domestic", "overseas"] = "overseas",
        debug: bool = False,
        queue_maxsize: int = 1000,
        rate_limit_requests_per_second: float = 5.0,
        rate_limit_burst: int = 3,
    ):
        """WebSocket 클라이언트 초기화.

        Args:
            token: 접근토큰 (LOGIN 프레임에 사용).
            env: 환경. "prod":운영, "dev":모의투자.
            market: 시장. "overseas":미국주식(us), "domestic":국내주식(dostk).
            debug: 디버그 로깅 활성화 여부.
            queue_maxsize: 이벤트 큐 최대 크기 (0이면 무제한).
            rate_limit_requests_per_second: 송신 rate limit.
            rate_limit_burst: 송신 burst 한도.
        """
        self.token = token
        self.env = env
        self.market = market
        self.debug = debug

        host = self.WS_HOST_PROD if env == "prod" else self.WS_HOST_DEV
        self._ws_url = f"{host}{self.WS_PATH[market]}"
        self._event_queue: "asyncio.Queue[KiwoomWebSocketMessage]" = asyncio.Queue(maxsize=queue_maxsize)
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._connected = False
        self._receive_task: Optional[asyncio.Task] = None
        self._rate_limiter = TokenBucket(capacity=rate_limit_burst, refill_rate=rate_limit_requests_per_second)

        if debug:
            logger.enable("cluefin_openapi.kiwoom")

    async def __aenter__(self) -> "KiwoomWebSocketClient":
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    @property
    def connected(self) -> bool:
        """WebSocket 연결 여부."""
        return self._connected

    # ------------------------------------------------------------------
    # 연결 / 종료
    # ------------------------------------------------------------------

    async def connect(self) -> None:
        """WebSocket 서버에 접속하고 LOGIN 인증까지 수행한다.

        Raises:
            KiwoomNetworkError: 접속/핸드셰이크 실패.
            KiwoomAPIError: LOGIN 인증 실패 (return_code != 0).
        """
        parsed = urlparse(self._ws_url)
        use_ssl = parsed.scheme == "wss"
        host = parsed.hostname or ""
        port = parsed.port or (443 if use_ssl else 80)
        path = parsed.path or "/"

        try:
            ssl_context = ssl.create_default_context() if use_ssl else None
            self._reader, self._writer = await asyncio.open_connection(host, port, ssl=ssl_context)
            await self._websocket_handshake(host, port, path)
        except (OSError, asyncio.IncompleteReadError) as e:
            raise KiwoomNetworkError(f"Failed to connect to WebSocket: {e}") from e

        await self._login()

        self._connected = True
        self._receive_task = asyncio.create_task(self._receive_loop())

        if self.debug:
            logger.debug("Kiwoom WebSocket connected: {}", self._ws_url)

    async def close(self) -> None:
        """WebSocket 연결을 종료한다."""
        self._connected = False

        if self._receive_task:
            self._receive_task.cancel()
            try:
                await self._receive_task
            except asyncio.CancelledError:
                pass
            self._receive_task = None

        if self._writer:
            try:
                await self._send_frame(b"", opcode=0x8)  # Close frame
            except Exception as exc:
                if self.debug:
                    logger.debug("Failed to send close frame: {}", exc)
            self._writer.close()
            try:
                await self._writer.wait_closed()
            except Exception as exc:
                if self.debug:
                    logger.debug("Failed to close writer: {}", exc)
            self._writer = None
            self._reader = None

        if self.debug:
            logger.debug("Kiwoom WebSocket closed")

    async def _login(self) -> None:
        """LOGIN 프레임을 전송하고 인증 응답을 확인한다.

        LOGIN 응답 전 PING이 먼저 도착할 수 있으므로 그대로 회신하며 대기한다.
        """
        await self.send({"trnm": "LOGIN", "token": self.token})

        while True:
            message = await self._recv_json()
            if message.trnm == "PING":
                await self.send(message.body)
                continue
            if message.trnm == "LOGIN":
                return_code = message.body.get("return_code")
                if return_code not in (0, "0"):
                    raise KiwoomAPIError(
                        f"WebSocket LOGIN failed: {message.body.get('return_msg') or 'unknown error'}",
                        response_data=message.body,
                    )
                return
            # LOGIN 이전의 예상치 못한 프레임은 무시한다.
            if self.debug:
                logger.debug("Ignoring pre-LOGIN frame: {}", message.trnm)

    # ------------------------------------------------------------------
    # 송신 / 수신 (도메인 클래스에서 사용하는 공개 API)
    # ------------------------------------------------------------------

    async def send(self, message: Union[Dict[str, Any], BaseModel]) -> None:
        """JSON 프레임을 송신한다.

        Args:
            message: 송신할 프레임. dict 또는 Pydantic 모델(``model_dump(by_alias=True)``로 직렬화).

        Raises:
            KiwoomNetworkError: 연결이 초기화되지 않았거나 송신 실패.
            KiwoomAPIError: rate limit 초과.
        """
        if isinstance(message, BaseModel):
            payload = message.model_dump(by_alias=True)
        else:
            payload = message

        if not self._rate_limiter.wait_for_tokens(timeout=5.0):
            raise KiwoomAPIError("WebSocket send rate limit exceeded")

        if self.debug:
            logger.debug("WS send: {}", payload)

        await self._send_frame(json.dumps(payload).encode("utf-8"))

    async def recv(self) -> KiwoomWebSocketMessage:
        """다음 (PING이 아닌) 프레임을 이벤트 큐에서 꺼낸다.

        요청-응답형 TR(조건검색 목록/요청 등)에서 응답 프레임을 기다릴 때 사용한다.
        """
        return await self._event_queue.get()

    async def events(self):
        """이벤트 큐의 프레임을 순회하는 async generator.

        Yields:
            KiwoomWebSocketMessage: PING을 제외한 수신 프레임.
        """
        while self._connected or not self._event_queue.empty():
            try:
                message = await asyncio.wait_for(self._event_queue.get(), timeout=1.0)
                yield message
            except asyncio.TimeoutError:
                continue

    # ------------------------------------------------------------------
    # 수신 루프 / 메시지 처리
    # ------------------------------------------------------------------

    async def _receive_loop(self) -> None:
        """수신 루프. PING은 회신하고 나머지 프레임은 큐에 넣는다."""
        try:
            while self._connected:
                message = await self._recv_json()
                if message.trnm == "PING":
                    await self.send(message.body)
                    continue
                await self._emit(message)
        except asyncio.CancelledError:
            pass
        except (asyncio.IncompleteReadError, ConnectionError, OSError) as e:
            if self._connected:
                logger.error("Kiwoom WebSocket receive error: {}", e)
                self._connected = False

    async def _emit(self, message: KiwoomWebSocketMessage) -> None:
        """이벤트 큐에 메시지를 넣는다. 큐가 가득 차면 가장 오래된 항목을 버린다."""
        try:
            self._event_queue.put_nowait(message)
        except asyncio.QueueFull:
            logger.warning("Kiwoom WebSocket event queue full, dropping oldest message")
            try:
                self._event_queue.get_nowait()
                self._event_queue.put_nowait(message)
            except asyncio.QueueEmpty:
                pass

    async def _recv_json(self) -> KiwoomWebSocketMessage:
        """텍스트 프레임 하나를 읽어 JSON으로 파싱한다.

        Ping(0x9)/Pong(0xA)/Close(0x8) 제어 프레임을 처리하며, 텍스트 프레임을 만날 때까지
        읽는다.
        """
        while True:
            opcode, payload = await self._receive_frame()
            if opcode in (0x1, 0x2):  # Text / Binary
                raw = payload.decode("utf-8")
                body = json.loads(raw)
                trnm = body.get("trnm", "") if isinstance(body, dict) else ""
                return KiwoomWebSocketMessage(trnm=trnm, body=body if isinstance(body, dict) else {}, raw=raw)
            if opcode == 0x8:  # Close
                self._connected = False
                raise KiwoomNetworkError("WebSocket closed by server")
            if opcode == 0x9:  # Ping (protocol-level)
                await self._send_frame(payload, opcode=0xA)  # Pong
            # Pong(0xA)은 무시

    # ------------------------------------------------------------------
    # 저수준 WebSocket 프레이밍 (RFC 6455)
    # ------------------------------------------------------------------

    async def _websocket_handshake(self, host: str, port: int, path: str) -> None:
        """RFC 6455 WebSocket 핸드셰이크를 수행한다."""
        if self._writer is None or self._reader is None:
            raise KiwoomNetworkError("WebSocket handshake failed: connection not initialized")

        ws_key = base64.b64encode(os.urandom(16)).decode()
        handshake = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {ws_key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n"
            f"\r\n"
        )
        self._writer.write(handshake.encode())
        await self._writer.drain()

        response = await self._reader.readuntil(b"\r\n\r\n")
        if b"101" not in response:
            raise KiwoomNetworkError(f"WebSocket handshake failed: {response.decode(errors='replace')}")

        # SHA1은 RFC 6455 WebSocket 프로토콜에서 요구하는 것으로 보안 용도가 아니다.
        expected_accept = base64.b64encode(
            hashlib.sha1(  # nosemgrep
                (ws_key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode(),
                usedforsecurity=False,
            ).digest()
        ).decode()
        if expected_accept.encode() not in response:
            raise KiwoomNetworkError("WebSocket handshake: invalid Sec-WebSocket-Accept")

    async def _send_frame(self, data: bytes, opcode: int = 0x1) -> None:
        """WebSocket 프레임을 송신한다 (클라이언트→서버는 마스킹 필수).

        Args:
            data: 송신 데이터.
            opcode: WebSocket opcode (0x1:text, 0x8:close, 0x9:ping, 0xA:pong).
        """
        if self._writer is None:
            raise KiwoomNetworkError("WebSocket send failed: connection not initialized")

        length = len(data)
        frame = bytearray()
        frame.append(0x80 | opcode)  # FIN + opcode

        mask_bit = 0x80  # 클라이언트→서버 프레임은 마스킹 필수
        if length <= 125:
            frame.append(mask_bit | length)
        elif length <= 65535:
            frame.append(mask_bit | 126)
            frame.extend(struct.pack(">H", length))
        else:
            frame.append(mask_bit | 127)
            frame.extend(struct.pack(">Q", length))

        mask_key = os.urandom(4)
        frame.extend(mask_key)
        frame.extend(byte ^ mask_key[index % 4] for index, byte in enumerate(data))

        self._writer.write(bytes(frame))
        await self._writer.drain()

    async def _receive_frame(self) -> tuple[int, bytes]:
        """WebSocket 프레임 하나를 수신한다.

        Returns:
            (opcode, payload) 튜플.
        """
        if self._reader is None:
            raise KiwoomNetworkError("WebSocket receive failed: connection not initialized")

        header = await self._reader.readexactly(2)
        opcode = header[0] & 0x0F
        masked = (header[1] >> 7) & 1
        length = header[1] & 0x7F

        if length == 126:
            length = struct.unpack(">H", await self._reader.readexactly(2))[0]
        elif length == 127:
            length = struct.unpack(">Q", await self._reader.readexactly(8))[0]

        mask_key = await self._reader.readexactly(4) if masked else None
        payload = await self._reader.readexactly(length)

        if mask_key:
            payload = bytes(byte ^ mask_key[index % 4] for index, byte in enumerate(payload))

        return opcode, payload
