"""NH PLUG WebSocket client for real-time market data.

This module provides an async WebSocket client for NH PLUG real-time data
using Python's standard library (asyncio), mirroring the KIS socket client.

WebSocket URLs (정본은 각 자산군 openapi.json 의 `x-environments`):
- 운영 국내: wss://api.nhplug.com:7070
- 운영 해외: wss://api.nhplug.com:7080
- 모의투자: wss://moapi.nhplug.com:17070

인증은 REST 와 달리 구독 메시지 `header.token` 에 access token 만 전달한다
(별도 approval key 없음). 서버 푸시는 평문 JSON 이며 heartbeat 는 필요 없다.
"""

import asyncio
import json
import ssl
import struct
from asyncio import Queue
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Literal, Optional

from loguru import logger

from cluefin_openapi._rate_limiter import TokenBucket

from ._exceptions import NHPlugAPIError, NHPlugNetworkError


class SubscriptionType(str, Enum):
    """WebSocket subscription type (tr_type)."""

    SUBSCRIBE = "1"
    UNSUBSCRIBE = "2"


@dataclass
class WebSocketMessage:
    """Parsed WebSocket message from NH PLUG API.

    서버 푸시 구조: {"header": {"tr_cd", "tr_key"}, "body": {…응답필드…}}
    """

    tr_cd: Optional[str] = None
    tr_key: Optional[str] = None
    body: Optional[Dict[str, Any]] = None
    raw: str = ""


@dataclass
class WebSocketEvent:
    """Event emitted from WebSocket for queue-based processing."""

    event_type: Literal["data", "connected", "disconnected", "error", "subscribed", "unsubscribed", "system"]
    tr_cd: Optional[str] = None
    tr_key: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    error: Optional[Exception] = None
    raw: Optional[str] = None


class SocketClient:
    """Async WebSocket client for NH PLUG real-time data.

    Example:
        ```python
        from pydantic import SecretStr
        from cluefin_openapi.nhplug import Auth, SocketClient

        auth = Auth(app_key="...", secret_key=SecretStr("..."))
        token = auth.generate()

        async with SocketClient(token=token.access_token) as client:
            # "mc" = 국내주식 실시간체결가(통합시세). 해외는 market="gb" + "rc"/"RC" 등
            await client.subscribe("mc", "005930")

            async for event in client.events():
                if event.event_type == "data":
                    print(f"Received: {event.tr_cd} - {event.data}")
        ```

    Attributes:
        token: REST 와 동일한 access token (Auth.generate())
        env: Environment ("prod" or "dev")
        market: 접속 대상 ("kr": 국내, "gb": 해외 — dev 는 단일 주소)
        event_queue: Queue for receiving WebSocket events
    """

    # WebSocket URLs
    WS_URL_PROD_KR = "wss://api.nhplug.com:7070"
    WS_URL_PROD_GB = "wss://api.nhplug.com:7080"
    WS_URL_DEV = "wss://moapi.nhplug.com:17070"

    def __init__(
        self,
        token: str,
        env: Literal["prod", "dev"] = "prod",
        market: Literal["kr", "gb"] = "kr",
        debug: bool = False,
        queue_maxsize: int = 1000,
        rate_limit_requests_per_second: float = 5.0,
        rate_limit_burst: int = 3,
    ):
        """Initialize WebSocket client.

        Args:
            token: Access token from Auth.generate()
            env: Environment - "prod" for production, "dev" for mock trading
            market: "kr" for domestic, "gb" for overseas (prod only)
            debug: Enable debug logging
            queue_maxsize: Maximum size of event queue (0 for unlimited)
            rate_limit_requests_per_second: Rate limit for subscriptions
            rate_limit_burst: Burst limit for subscriptions
        """
        self.token = token
        self.env = env
        self.market = market
        self.debug = debug

        if env == "prod":
            self._ws_url = self.WS_URL_PROD_KR if market == "kr" else self.WS_URL_PROD_GB
        else:
            self._ws_url = self.WS_URL_DEV
        self._event_queue: Queue[WebSocketEvent] = Queue(maxsize=queue_maxsize)
        self._subscriptions: Dict[str, str] = {}  # tr_cd:tr_key -> tr_key
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._connected = False
        self._receive_task: Optional[asyncio.Task] = None
        self._rate_limiter = TokenBucket(capacity=rate_limit_burst, refill_rate=rate_limit_requests_per_second)

        if debug:
            logger.enable("cluefin_openapi.nhplug")
        else:
            logger.disable("cluefin_openapi.nhplug")

    async def __aenter__(self) -> "SocketClient":
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.close()

    async def connect(self) -> None:
        """Connect to WebSocket server.

        Raises:
            NHPlugNetworkError: If connection fails
        """
        try:
            url = self._ws_url
            if url.startswith("ws://"):
                host_port = url[5:]
                use_ssl = False
            elif url.startswith("wss://"):
                host_port = url[6:]
                use_ssl = True
            else:
                raise ValueError(f"Invalid WebSocket URL: {url}")

            if ":" in host_port:
                host, port_str = host_port.split(":", 1)
                if "/" in port_str:
                    port_str = port_str.split("/")[0]
                port = int(port_str)
            else:
                host = host_port.split("/")[0]
                port = 443 if use_ssl else 80

            if self.debug:
                logger.debug(f"Connecting to {host}:{port} (SSL: {use_ssl})")

            ssl_context = ssl.create_default_context() if use_ssl else None
            self._reader, self._writer = await asyncio.open_connection(host, port, ssl=ssl_context)

            await self._websocket_handshake(host, port)

            self._connected = True

            self._receive_task = asyncio.create_task(self._receive_loop())

            await self._emit_event(WebSocketEvent(event_type="connected"))

            if self.debug:
                logger.debug("WebSocket connected successfully")

        except Exception as e:
            raise NHPlugNetworkError(f"Failed to connect to WebSocket: {e}") from e

    async def _websocket_handshake(self, host: str, port: int) -> None:
        """Perform WebSocket handshake.

        Args:
            host: WebSocket server host
            port: WebSocket server port
        """
        import base64
        import hashlib
        import os

        ws_key = base64.b64encode(os.urandom(16)).decode()

        path = "/"
        handshake = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {ws_key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n"
            f"\r\n"
        )

        if self._writer is None or self._reader is None:
            raise NHPlugNetworkError("WebSocket handshake failed: connection not initialized")

        self._writer.write(handshake.encode())
        await self._writer.drain()

        response = await self._reader.readuntil(b"\r\n\r\n")

        if self.debug:
            logger.debug(f"Handshake response: {response.decode()}")

        if b"101" not in response:
            raise NHPlugNetworkError(f"WebSocket handshake failed: {response.decode()}")

        # Verify Sec-WebSocket-Accept (SHA1 is required by RFC 6455 WebSocket protocol)
        expected_accept = base64.b64encode(
            hashlib.sha1(  # nosemgrep
                (ws_key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode(),
                usedforsecurity=False,
            ).digest()
        ).decode()

        if expected_accept.encode() not in response:
            raise NHPlugNetworkError("WebSocket handshake: invalid Sec-WebSocket-Accept")

    async def _send_frame(self, data: bytes, opcode: int = 0x1) -> None:
        """Send a WebSocket frame.

        Args:
            data: Data to send
            opcode: WebSocket opcode (0x1 = text, 0x9 = ping, 0xA = pong)
        """
        length = len(data)

        if self._writer is None:
            raise NHPlugNetworkError("WebSocket send failed: connection not initialized")

        frame = bytearray()
        frame.append(0x80 | opcode)  # FIN + opcode

        # Mask bit is required for client-to-server messages
        mask_bit = 0x80

        if length <= 125:
            frame.append(mask_bit | length)
        elif length <= 65535:
            frame.append(mask_bit | 126)
            frame.extend(struct.pack(">H", length))
        else:
            frame.append(mask_bit | 127)
            frame.extend(struct.pack(">Q", length))

        import os

        mask_key = os.urandom(4)
        frame.extend(mask_key)

        masked_data = bytearray(data)
        for i in range(len(masked_data)):
            masked_data[i] ^= mask_key[i % 4]
        frame.extend(masked_data)

        self._writer.write(bytes(frame))
        await self._writer.drain()

    async def _receive_frame(self) -> tuple[int, bytes]:
        """Receive a WebSocket frame.

        Returns:
            Tuple of (opcode, payload)
        """
        if self._reader is None:
            raise NHPlugNetworkError("WebSocket receive failed: connection not initialized")

        header = await self._reader.readexactly(2)
        opcode = header[0] & 0x0F
        masked = (header[1] >> 7) & 1
        length = header[1] & 0x7F

        if length == 126:
            ext_length = await self._reader.readexactly(2)
            length = struct.unpack(">H", ext_length)[0]
        elif length == 127:
            ext_length = await self._reader.readexactly(8)
            length = struct.unpack(">Q", ext_length)[0]

        mask_key = None
        if masked:
            mask_key = await self._reader.readexactly(4)

        payload = await self._reader.readexactly(length)

        if mask_key:
            payload = bytearray(payload)
            for i in range(len(payload)):
                payload[i] ^= mask_key[i % 4]
            payload = bytes(payload)

        return opcode, payload

    async def _receive_loop(self) -> None:
        """Main receive loop for WebSocket messages."""
        try:
            while self._connected:
                opcode, payload = await self._receive_frame()

                if opcode == 0x1:  # Text frame
                    await self._handle_message(payload.decode("utf-8"))
                elif opcode == 0x8:  # Close frame
                    if self.debug:
                        logger.debug("Received close frame")
                    self._connected = False
                    await self._emit_event(WebSocketEvent(event_type="disconnected"))
                    break
                elif opcode == 0x9:  # Ping frame
                    if self.debug:
                        logger.debug("Received ping, sending pong")
                    await self._send_frame(payload, opcode=0xA)  # Pong
                elif opcode == 0xA:  # Pong frame
                    if self.debug:
                        logger.debug("Received pong")

        except asyncio.CancelledError:
            pass
        except Exception as e:
            if self._connected:
                logger.error(f"WebSocket receive error: {e}")
                await self._emit_event(WebSocketEvent(event_type="error", error=e))
                self._connected = False

    async def _handle_message(self, raw: str) -> None:
        """Handle incoming WebSocket message.

        Args:
            raw: Raw message string
        """
        if self.debug:
            logger.debug(f"Received message: {raw[:200]}...")

        message = self._parse_message(raw)

        if message.tr_cd is not None:
            await self._emit_event(
                WebSocketEvent(
                    event_type="data",
                    tr_cd=message.tr_cd,
                    tr_key=message.tr_key,
                    data=message.body,
                    raw=raw,
                )
            )
        else:
            # 구독 응답 등 tr_cd 없는 시스템성 메시지
            await self._emit_event(WebSocketEvent(event_type="system", raw=raw))

    def _parse_message(self, raw: str) -> WebSocketMessage:
        """Parse raw WebSocket message.

        NH PLUG push format (평문 JSON, 암호화 없음):
            {"header": {"tr_cd": "...", "tr_key": "..."}, "body": {…응답필드…}}

        Args:
            raw: Raw message string

        Returns:
            Parsed WebSocketMessage
        """
        try:
            parsed = json.loads(raw)
        except (ValueError, json.JSONDecodeError):
            return WebSocketMessage(raw=raw)

        if not isinstance(parsed, dict):
            return WebSocketMessage(raw=raw)

        header = parsed.get("header") or {}
        body = parsed.get("body")
        return WebSocketMessage(
            tr_cd=header.get("tr_cd"),
            tr_key=header.get("tr_key"),
            body=body if isinstance(body, dict) else None,
            raw=raw,
        )

    async def _emit_event(self, event: WebSocketEvent) -> None:
        """Emit event to queue.

        Args:
            event: Event to emit
        """
        try:
            self._event_queue.put_nowait(event)
        except asyncio.QueueFull:
            logger.warning("Event queue full, dropping oldest event")
            try:
                self._event_queue.get_nowait()
                self._event_queue.put_nowait(event)
            except asyncio.QueueEmpty:
                pass

    async def subscribe(self, tr_cd: str, tr_key: str) -> None:
        """Subscribe to real-time data.

        Args:
            tr_cd: 실시간 채널 코드 (REST 경로가 아니라 웹소켓 전용 코드 — 정본은 각
                자산군 openapi.json 의 `x-realtime-channels[].tr_cd`). 국내는
                체결가/호가/예상체결이 통합시세 mc/mb/ma · KRX oc/ob/oa · NXT nc/nb/na,
                통보는 d2(체결)·d3(주문내역). 해외는 체결가/호가가 실시간 RC/RH(유료시세
                약정 필요)·지연 rc/rh(미국·중국만), 통보는 d0(체결)·d1(주문내역).
                해외는 대소문자로 실시간/지연이 갈리므로 주의할 것.
            tr_key: 구독 키. 시세 채널은 종목코드, 체결·주문내역 통보 채널은 사용자ID.

        Raises:
            NHPlugAPIError: If subscription fails
        """
        if not self._connected:
            raise NHPlugAPIError("WebSocket not connected")

        if not self._rate_limiter.wait_for_tokens(timeout=5.0):
            raise NHPlugAPIError("Subscription rate limit exceeded")

        subscription_key = f"{tr_cd}:{tr_key}"
        if subscription_key in self._subscriptions:
            if self.debug:
                logger.debug(f"Already subscribed to {subscription_key}")
            return

        message = self._build_subscription_message(tr_cd, tr_key, SubscriptionType.SUBSCRIBE)

        if self.debug:
            logger.debug(f"Subscribing: {tr_cd}:{tr_key}")

        await self._send_frame(message.encode())
        self._subscriptions[subscription_key] = tr_key

        await self._emit_event(WebSocketEvent(event_type="subscribed", tr_cd=tr_cd, tr_key=tr_key))

    async def unsubscribe(self, tr_cd: str, tr_key: str) -> None:
        """Unsubscribe from real-time data.

        Args:
            tr_cd: 채널 코드
            tr_key: 구독 키
        """
        if not self._connected:
            raise NHPlugAPIError("WebSocket not connected")

        subscription_key = f"{tr_cd}:{tr_key}"
        if subscription_key not in self._subscriptions:
            if self.debug:
                logger.debug(f"Not subscribed to {subscription_key}")
            return

        message = self._build_subscription_message(tr_cd, tr_key, SubscriptionType.UNSUBSCRIBE)

        if self.debug:
            logger.debug(f"Unsubscribing: {tr_cd}:{tr_key}")

        await self._send_frame(message.encode())
        del self._subscriptions[subscription_key]

        await self._emit_event(WebSocketEvent(event_type="unsubscribed", tr_cd=tr_cd, tr_key=tr_key))

    def _build_subscription_message(self, tr_cd: str, tr_key: str, tr_type: SubscriptionType) -> str:
        """Build subscription/unsubscription message.

        인증은 header.token 에 access token 만 전달한다
        (Authorization·x-client-id·x-client-secret 헤더는 사용하지 않음).

        Args:
            tr_cd: 채널 코드
            tr_key: 구독 키
            tr_type: Subscription type

        Returns:
            JSON message string
        """
        message = {
            "header": {
                "token": self.token,
                "tr_type": tr_type.value,
            },
            "body": {
                "tr_cd": tr_cd,
                "tr_key": tr_key,
            },
        }
        return json.dumps(message)

    async def events(self):
        """Async generator for receiving events.

        Yields:
            WebSocketEvent objects

        Example:
            ```python
            async for event in client.events():
                if event.event_type == "data":
                    process_data(event.data)
            ```
        """
        while self._connected or not self._event_queue.empty():
            try:
                event = await asyncio.wait_for(self._event_queue.get(), timeout=1.0)
                yield event
            except asyncio.TimeoutError:
                continue

    async def close(self) -> None:
        """Close WebSocket connection."""
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
                await self._send_frame(b"", opcode=0x8)
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
            logger.debug("WebSocket closed")

    @property
    def connected(self) -> bool:
        """Check if WebSocket is connected."""
        return self._connected

    @property
    def subscriptions(self) -> Dict[str, str]:
        """Get current subscriptions."""
        return dict(self._subscriptions)
