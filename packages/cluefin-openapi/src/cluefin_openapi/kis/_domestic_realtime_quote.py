"""국내주식 실시간시세 WebSocket API.

WebSocket을 통해 실시간 체결가, 호가 등의 데이터를 구독합니다.

References:
- https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-real2
"""

from typing import List

from ._domestic_realtime_quote_types import (
    EXECUTION_FIELD_NAMES,
    ORDERBOOK_FIELD_NAMES,
    DomesticRealtimeExecutionItem,
    DomesticRealtimeOrderbookItem,
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
                    executions = realtime.parse_execution_data(event.data["values"])
                    for execution in executions:
                        print(f"Price: {execution.stck_prpr}, Volume: {execution.cntg_vol}")
        ```
    """

    # Transaction IDs
    TR_ID_EXECUTION = "H0UNCNT0"  # 실시간 체결가 (통합)
    TR_ID_ORDERBOOK = "H0STASP0"  # 실시간 호가 (KRX)

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
    def parse_execution_data(data: List[str]) -> List[DomesticRealtimeExecutionItem]:
        """Parse WebSocket data into list of DomesticRealtimeExecutionItem.

        WebSocket data is received as a list of string values separated by "^" delimiter.
        The API may send batched updates (multiple records concatenated).
        This method parses ALL records and returns them as a list.

        Args:
            data: List of string values from WebSocket message.
                  - Single record: 46 fields
                  - Batched: N×46 fields (e.g., 552 = 12×46)
                  - With extra fields: 46+ per record (forward compatible)

        Returns:
            List of parsed DomesticRealtimeExecutionItem models.
            Always returns a list, even for single records.

        Raises:
            ValueError: If data has insufficient fields (< 46)

        Example:
            ```python
            # Single record
            data = ["005930", "093000", "70000", ...]  # 46 fields
            items = parse_execution_data(data)
            assert len(items) == 1

            # Batched records
            data = [...] * 12  # 552 fields = 12 records
            items = parse_execution_data(data)
            assert len(items) == 12

            for item in items:
                print(f"Price: {item.stck_prpr}")
            ```
        """
        field_count = len(EXECUTION_FIELD_NAMES)

        # Validate minimum field count
        if len(data) < field_count:
            raise ValueError(
                f"Expected at least {field_count} fields, got {len(data)}. First field: {data[0] if data else 'empty'}"
            )

        # Calculate number of complete records
        num_records = len(data) // field_count

        # Parse all complete records
        results = []
        for i in range(num_records):
            start_idx = i * field_count
            end_idx = start_idx + field_count

            # Slice to expected field count (handles extra fields per record)
            record_data = data[start_idx:end_idx]

            # Create field dictionary and validate
            field_dict = dict(zip(EXECUTION_FIELD_NAMES, record_data, strict=False))
            item = DomesticRealtimeExecutionItem.model_validate(field_dict)
            results.append(item)

        return results

    async def subscribe_orderbook(self, stock_code: str) -> None:
        """Subscribe to real-time orderbook data.

        Args:
            stock_code: Stock code (e.g., "005930" for Samsung Electronics)
        """
        await self.socket_client.subscribe(self.TR_ID_ORDERBOOK, stock_code)

    async def unsubscribe_orderbook(self, stock_code: str) -> None:
        """Unsubscribe from real-time orderbook data.

        Args:
            stock_code: Stock code to unsubscribe
        """
        await self.socket_client.unsubscribe(self.TR_ID_ORDERBOOK, stock_code)

    @staticmethod
    def parse_orderbook_data(data: List[str]) -> List[DomesticRealtimeOrderbookItem]:
        """Parse WebSocket data into list of DomesticRealtimeOrderbookItem.

        WebSocket data is received as a list of string values separated by "^" delimiter.
        The API may send batched updates (multiple records concatenated).
        This method parses ALL records and returns them as a list.

        Note: The API may return extra fields beyond the documented 59 fields.
        This parser will use the first 59 fields per record and ignore any extras.
        This provides forward compatibility with future API schema changes.

        Args:
            data: List of string values from WebSocket message.
                  - Single record: 59+ fields
                  - Batched: N×59+ fields
                  - With schema changes: 62+ per record (forward compatible)

        Returns:
            List of parsed DomesticRealtimeOrderbookItem models.
            Always returns a list, even for single records.

        Raises:
            ValueError: If data has insufficient fields (< 59)

        Example:
            ```python
            # Single record with extra fields
            data = [...] * 62  # 62 fields (59 used, 3 ignored)
            items = parse_orderbook_data(data)
            assert len(items) == 1

            # Batched records
            data = [...] * (10 * 59)  # 590 fields = 10 records
            items = parse_orderbook_data(data)
            assert len(items) == 10
            ```
        """
        field_count = len(ORDERBOOK_FIELD_NAMES)

        # Validate minimum field count
        if len(data) < field_count:
            raise ValueError(
                f"Expected at least {field_count} fields, got {len(data)}. First field: {data[0] if data else 'empty'}"
            )

        # Calculate number of complete records
        num_records = len(data) // field_count

        # Parse all complete records
        results = []
        for i in range(num_records):
            start_idx = i * field_count
            end_idx = start_idx + field_count

            # Slice to expected field count (handles extra fields per record)
            record_data = data[start_idx:end_idx]

            # Create field dictionary and validate
            field_dict = dict(zip(ORDERBOOK_FIELD_NAMES, record_data, strict=False))
            item = DomesticRealtimeOrderbookItem.model_validate(field_dict)
            results.append(item)

        return results
