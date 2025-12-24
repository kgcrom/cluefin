"""KIS WebSocket Client for real-time market data.

This module provides an async WebSocket client for Korea Investment & Securities
real-time market data API using Python's standard library (asyncio).

WebSocket URLs:
- Production: ws://ops.koreainvestment.com:21000
- Development (Mock): ws://ops.koreainvestment.com:31000

References:
- https://apiportal.koreainvestment.com/apiservice-apiservice?/oauth2/Approval
- https://github.com/koreainvestment/open-trading-api
"""

import asyncio
import json
import ssl
import struct
from asyncio import Queue
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Literal, Optional, Union

from loguru import logger
from pydantic import SecretStr

from cluefin_openapi._rate_limiter import TokenBucket

from ._exceptions import KISAPIError, KISNetworkError


class SubscriptionType(str, Enum):
    """WebSocket subscription type."""

    SUBSCRIBE = "1"
    UNSUBSCRIBE = "2"


class MessageType(str, Enum):
    """WebSocket message type indicator."""

    PINGPONG = "PINGPONG"
    DATA = "DATA"
    SYSTEM = "SYSTEM"


@dataclass
class WebSocketMessage:
    """Parsed WebSocket message from KIS API."""

    message_type: MessageType
    tr_id: Optional[str] = None
    data: Optional[List[str]] = None
    raw: str = ""
    encrypted: bool = False


@dataclass
class SubscriptionRequest:
    """WebSocket subscription request."""

    tr_id: str
    tr_key: str
    tr_type: SubscriptionType = SubscriptionType.SUBSCRIBE


@dataclass
class WebSocketEvent:
    """Event emitted from WebSocket for queue-based processing."""

    event_type: Literal["data", "connected", "disconnected", "error", "subscribed", "unsubscribed"]
    tr_id: Optional[str] = None
    tr_key: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    error: Optional[Exception] = None
    raw: Optional[str] = None


class SocketClient:
    """Async WebSocket client for KIS real-time market data.

    This client uses Python's standard asyncio library for WebSocket connections.
    It supports event queue-based message processing with rate limiting.

    Example:
        ```python
        from cluefin_openapi.kis import Auth, SocketClient

        auth = Auth(app_key="...", secret_key=SecretStr("..."))
        approval = auth.approve()

        async with SocketClient(
            approval_key=approval.approval_key,
            app_key="...",
            secret_key=SecretStr("..."),
        ) as client:
            # Subscribe to real-time quotes
            await client.subscribe("H0STASP0", "005930")  # Samsung hogas

            # Process events from queue
            async for event in client.events():
                if event.event_type == "data":
                    print(f"Received: {event.tr_id} - {event.data}")
        ```

    Attributes:
        approval_key: WebSocket approval key from Auth.approve()
        app_key: KIS API app key
        secret_key: KIS API secret key
        env: Environment ("prod" or "dev")
        event_queue: Queue for receiving WebSocket events
    """

    # WebSocket URLs
    WS_URL_PROD = "ws://ops.koreainvestment.com:21000"
    WS_URL_DEV = "ws://ops.koreainvestment.com:31000"

    def __init__(
        self,
        approval_key: str,
        app_key: str,
        secret_key: Union[str, SecretStr],
        env: Literal["prod", "dev"] = "prod",
        debug: bool = False,
        queue_maxsize: int = 1000,
        rate_limit_requests_per_second: float = 5.0,
        rate_limit_burst: int = 3,
    ):
        """Initialize WebSocket client.

        Args:
            approval_key: WebSocket approval key from Auth.approve()
            app_key: KIS API app key
            secret_key: KIS API secret key
            env: Environment - "prod" for production, "dev" for mock trading
            debug: Enable debug logging
            queue_maxsize: Maximum size of event queue (0 for unlimited)
            rate_limit_requests_per_second: Rate limit for subscriptions
            rate_limit_burst: Burst limit for subscriptions
        """
        self.approval_key = approval_key
        self.app_key = app_key
        self.secret_key = secret_key.get_secret_value() if isinstance(secret_key, SecretStr) else secret_key
        self.env = env
        self.debug = debug

        self._ws_url = self.WS_URL_PROD if env == "prod" else self.WS_URL_DEV
        self._event_queue: Queue[WebSocketEvent] = Queue(maxsize=queue_maxsize)
        self._subscriptions: Dict[str, str] = {}  # tr_id:tr_key -> subscription key
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._connected = False
        self._receive_task: Optional[asyncio.Task] = None
        self._rate_limiter = TokenBucket(capacity=rate_limit_burst, refill_rate=rate_limit_requests_per_second)

        if debug:
            logger.enable("cluefin_openapi.kis")
        else:
            logger.disable("cluefin_openapi.kis")

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
            KISNetworkError: If connection fails
        """
        try:
            # Parse WebSocket URL
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
                # Remove path if present
                if "/" in port_str:
                    port_str = port_str.split("/")[0]
                port = int(port_str)
            else:
                host = host_port.split("/")[0]
                port = 443 if use_ssl else 80

            if self.debug:
                logger.debug(f"Connecting to {host}:{port} (SSL: {use_ssl})")

            # Create connection
            ssl_context = ssl.create_default_context() if use_ssl else None
            self._reader, self._writer = await asyncio.open_connection(host, port, ssl=ssl_context)

            # Perform WebSocket handshake
            await self._websocket_handshake(host, port)

            self._connected = True

            # Start receive task
            self._receive_task = asyncio.create_task(self._receive_loop())

            # Emit connected event
            await self._emit_event(WebSocketEvent(event_type="connected"))

            if self.debug:
                logger.debug("WebSocket connected successfully")

        except Exception as e:
            raise KISNetworkError(f"Failed to connect to WebSocket: {e}") from e

    async def _websocket_handshake(self, host: str, port: int) -> None:
        """Perform WebSocket handshake.

        Args:
            host: WebSocket server host
            port: WebSocket server port
        """
        import base64
        import hashlib
        import os

        # Generate WebSocket key
        ws_key = base64.b64encode(os.urandom(16)).decode()

        # Build handshake request
        path = "/tryitout"  # KIS WebSocket path
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

        # Read handshake response
        response = await self._reader.readuntil(b"\r\n\r\n")

        if self.debug:
            logger.debug(f"Handshake response: {response.decode()}")

        # Verify handshake response
        if b"101" not in response:
            raise KISNetworkError(f"WebSocket handshake failed: {response.decode()}")

        # Verify Sec-WebSocket-Accept
        expected_accept = base64.b64encode(
            hashlib.sha1((ws_key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest()
        ).decode()

        if expected_accept.encode() not in response:
            raise KISNetworkError("WebSocket handshake: invalid Sec-WebSocket-Accept")

    async def _send_frame(self, data: bytes, opcode: int = 0x1) -> None:
        """Send a WebSocket frame.

        Args:
            data: Data to send
            opcode: WebSocket opcode (0x1 = text, 0x9 = ping, 0xA = pong)
        """
        length = len(data)

        # Build frame header
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

        # Add masking key
        import os

        mask_key = os.urandom(4)
        frame.extend(mask_key)

        # Mask the data
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
        # Read first 2 bytes
        header = await self._reader.readexactly(2)
        # FIN bit: (header[0] >> 7) & 1 - not used but kept for reference
        opcode = header[0] & 0x0F
        masked = (header[1] >> 7) & 1
        length = header[1] & 0x7F

        # Extended length
        if length == 126:
            ext_length = await self._reader.readexactly(2)
            length = struct.unpack(">H", ext_length)[0]
        elif length == 127:
            ext_length = await self._reader.readexactly(8)
            length = struct.unpack(">Q", ext_length)[0]

        # Masking key (server should not send masked frames, but handle it)
        mask_key = None
        if masked:
            mask_key = await self._reader.readexactly(4)

        # Payload
        payload = await self._reader.readexactly(length)

        # Unmask if needed
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

        if message.message_type == MessageType.PINGPONG:
            # Respond to PINGPONG
            if self.debug:
                logger.debug("Received PINGPONG, responding...")
            await self._send_frame(raw.encode())
            return

        if message.message_type == MessageType.DATA and message.tr_id and message.data:
            # Emit data event
            await self._emit_event(
                WebSocketEvent(
                    event_type="data",
                    tr_id=message.tr_id,
                    data={"values": message.data, "encrypted": message.encrypted},
                    raw=raw,
                )
            )

    def _parse_message(self, raw: str) -> WebSocketMessage:
        """Parse raw WebSocket message.

        KIS WebSocket message format:
        - PINGPONG messages: Start with specific indicator
        - Data messages: "encrypted|tr_id|count|data" format
          - encrypted: "0" (plain) or "1" (AES encrypted)
          - data: "^" separated values

        Args:
            raw: Raw message string

        Returns:
            Parsed WebSocketMessage
        """
        # Check for PINGPONG
        if raw.startswith("PINGPONG"):
            return WebSocketMessage(message_type=MessageType.PINGPONG, raw=raw)

        # Try to parse as data message
        # Format: encrypted|tr_id|count|data
        if raw and raw[0] in ("0", "1"):
            parts = raw.split("|")
            if len(parts) >= 4:
                encrypted = parts[0] == "1"
                tr_id = parts[1]
                # count = int(parts[2])
                data_str = parts[3]

                # Split data by "^"
                data = data_str.split("^") if data_str else []

                return WebSocketMessage(
                    message_type=MessageType.DATA,
                    tr_id=tr_id,
                    data=data,
                    raw=raw,
                    encrypted=encrypted,
                )

        # Unknown message type
        return WebSocketMessage(message_type=MessageType.SYSTEM, raw=raw)

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

    async def subscribe(self, tr_id: str, tr_key: str) -> None:
        """Subscribe to real-time data.

        Args:
            tr_id: Transaction ID (e.g., "H0STASP0" for stock quotes)
            tr_key: Transaction key (e.g., stock code "005930")

        Raises:
            KISAPIError: If subscription fails
        """
        if not self._connected:
            raise KISAPIError("WebSocket not connected")

        # Rate limiting
        if not self._rate_limiter.wait_for_tokens(timeout=5.0):
            raise KISAPIError("Subscription rate limit exceeded")

        subscription_key = f"{tr_id}:{tr_key}"
        if subscription_key in self._subscriptions:
            if self.debug:
                logger.debug(f"Already subscribed to {subscription_key}")
            return

        message = self._build_subscription_message(tr_id, tr_key, SubscriptionType.SUBSCRIBE)

        if self.debug:
            logger.debug(f"Subscribing: {message}")

        await self._send_frame(message.encode())
        self._subscriptions[subscription_key] = tr_key

        await self._emit_event(WebSocketEvent(event_type="subscribed", tr_id=tr_id, tr_key=tr_key))

    async def unsubscribe(self, tr_id: str, tr_key: str) -> None:
        """Unsubscribe from real-time data.

        Args:
            tr_id: Transaction ID
            tr_key: Transaction key
        """
        if not self._connected:
            raise KISAPIError("WebSocket not connected")

        subscription_key = f"{tr_id}:{tr_key}"
        if subscription_key not in self._subscriptions:
            if self.debug:
                logger.debug(f"Not subscribed to {subscription_key}")
            return

        message = self._build_subscription_message(tr_id, tr_key, SubscriptionType.UNSUBSCRIBE)

        if self.debug:
            logger.debug(f"Unsubscribing: {message}")

        await self._send_frame(message.encode())
        del self._subscriptions[subscription_key]

        await self._emit_event(WebSocketEvent(event_type="unsubscribed", tr_id=tr_id, tr_key=tr_key))

    def _build_subscription_message(self, tr_id: str, tr_key: str, tr_type: SubscriptionType) -> str:
        """Build subscription/unsubscription message.

        Args:
            tr_id: Transaction ID
            tr_key: Transaction key
            tr_type: Subscription type

        Returns:
            JSON message string
        """
        message = {
            "header": {
                "approval_key": self.approval_key,
                "custtype": "P",  # P: Personal, B: Corporate
                "tr_type": tr_type.value,
                "content-type": "utf-8",
            },
            "body": {
                "input": {
                    "tr_id": tr_id,
                    "tr_key": tr_key,
                }
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
                # Send close frame
                await self._send_frame(b"", opcode=0x8)
            except Exception:
                pass
            self._writer.close()
            try:
                await self._writer.wait_closed()
            except Exception:
                pass
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
