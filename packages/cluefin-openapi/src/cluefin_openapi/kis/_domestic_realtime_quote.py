"""국내주식 실시간시세 WebSocket API.

WebSocket을 통해 실시간 체결가, 호가 등의 데이터를 구독합니다.

References:
- https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-real2
"""

from typing import List

from ._domestic_realtime_quote_types import (
    EXECUTION_FIELD_NAMES,
    DomesticRealtimeExecutionItem,
)
from ._socket_client import SocketClient


class DomesticRealtimeQuote:
    """국내주식 실시간시세 WebSocket API.

    SocketClient를 사용하여 실시간 시세 데이터를 구독합니다.

    Example:
        ```python
        from cluefin_openapi.kis import Auth, SocketClient, DomesticRealtimeQuote

        auth = Auth(app_key="...", secret_key=SecretStr("..."))
        approval = auth.approve()

        async with SocketClient(
            approval_key=approval.approval_key,
            app_key="...",
            secret_key=SecretStr("..."),
        ) as socket_client:
            realtime = DomesticRealtimeQuote(socket_client)

            # Subscribe to real-time execution data
            await realtime.subscribe_execution("005930")

            # Process events
            async for event in socket_client.events():
                if event.event_type == "data" and event.tr_id == DomesticRealtimeQuote.TR_ID_EXECUTION:
                    execution = realtime.parse_execution_data(event.data["values"])
                    print(f"Price: {execution.stck_prpr}, Volume: {execution.cntg_vol}")
        ```
    """

    # Transaction IDs
    TR_ID_EXECUTION = "H0UNCNT0"  # 실시간 체결가 (통합)

    def __init__(self, socket_client: SocketClient):
        """Initialize DomesticRealtimeQuote.

        Args:
            socket_client: Connected SocketClient instance
        """
        self.socket_client = socket_client

    async def subscribe_execution(self, stock_code: str) -> None:
        """Subscribe to real-time execution data.

        Args:
            stock_code: Stock code (e.g., "005930" for Samsung Electronics)
        """
        await self.socket_client.subscribe(self.TR_ID_EXECUTION, stock_code)

    async def unsubscribe_execution(self, stock_code: str) -> None:
        """Unsubscribe from real-time execution data.

        Args:
            stock_code: Stock code to unsubscribe
        """
        await self.socket_client.unsubscribe(self.TR_ID_EXECUTION, stock_code)

    @staticmethod
    def parse_execution_data(data: List[str]) -> DomesticRealtimeExecutionItem:
        """Parse WebSocket data into DomesticRealtimeExecutionItem.

        WebSocket data is received as a list of 46 string values
        separated by "^" delimiter.

        Args:
            data: List of 46 string values from WebSocket message

        Returns:
            Parsed DomesticRealtimeExecutionItem model

        Raises:
            ValueError: If data does not contain exactly 46 fields
        """
        if len(data) != len(EXECUTION_FIELD_NAMES):
            raise ValueError(
                f"Expected {len(EXECUTION_FIELD_NAMES)} fields, got {len(data)}. "
                f"First field: {data[0] if data else 'empty'}"
            )

        field_dict = dict(zip(EXECUTION_FIELD_NAMES, data, strict=False))
        return DomesticRealtimeExecutionItem.model_validate(field_dict)
