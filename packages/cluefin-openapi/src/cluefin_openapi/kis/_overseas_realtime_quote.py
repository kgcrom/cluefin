"""해외주식 실시간시세 WebSocket API.

WebSocket을 통해 해외주식 실시간 호가, 지연호가(아시아), 실시간지연체결가 데이터를 구독합니다.

References:
- https://apiportal.koreainvestment.com/apiservice/apiservice-oversea-stock-real
"""

from functools import wraps
from typing import List

from ._overseas_realtime_quote_types import (
    OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES,
    OVERSEAS_EXECUTION_FIELD_NAMES,
    OVERSEAS_EXECUTION_NOTIFICATION_FIELD_NAMES,
    OVERSEAS_ORDERBOOK_FIELD_NAMES,
    OverseasRealtimeDelayedOrderbookItem,
    OverseasRealtimeExecutionItem,
    OverseasRealtimeExecutionNotificationItem,
    OverseasRealtimeOrderbookItem,
)
from ._socket_client import SocketClient


def _require_prod_env(func):
    """Decorator that validates production environment before method execution.

    Raises:
        ValueError: If socket client is not connected to production environment
    """

    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if self.socket_client.env != "prod":
            raise ValueError(
                f"해외주식 실시간시세는 운영 서버(prod)에서만 사용 가능합니다. 현재 환경: {self.socket_client.env}"
            )
        return await func(self, *args, **kwargs)

    return wrapper


class OverseasRealtimeQuote:
    """해외주식 실시간시세 WebSocket API.

    SocketClient를 사용하여 해외주식 실시간 호가, 지연호가(아시아), 실시간지연체결가 데이터를 구독합니다.

    Note:
        이 API는 운영 서버(prod)에서만 사용 가능합니다. 모의투자는 미지원됩니다.
    """

    # Transaction IDs
    TR_ID = "HDFSASP0"  # 해외주식 실시간호가 (실전 전용)
    TR_ID_EXECUTION = "HDFSCNT0"  # 해외주식 실시간지연체결가
    TR_ID_DELAYED_ORDERBOOK = "HDFSASP1"  # 해외주식 지연호가(아시아)
    TR_ID_EXECUTION_NOTIFICATION = "H0GSCNI0"  # 해외주식 실시간체결통보

    def __init__(self, socket_client: SocketClient):
        """Initialize OverseasRealtimeQuote.

        Args:
            socket_client: Connected SocketClient instance
        """
        self.socket_client = socket_client

    def _generate_tr_key(self, stock_code: str, market_code: str, service_type: str) -> str:
        """Generate TR Key (R거래소명종목코드) based on service type.

        Args:
            stock_code: Symbol code (e.g. AAPL)
            market_code: Market code (e.g. NAS, NYS, AMS, ... or BAQ, BAY, BAA ...)
            service_type: Service type. "R": Regular/Day, "D": US Night

        Returns:
            TR Key string (e.g. RNASAAPL)
        """
        return f"{service_type}{market_code}{stock_code}"

    @_require_prod_env
    async def subscribe(self, stock_code: str, market_code: str, service_type: str = "R") -> None:
        """Subscribe to real-time orderbook data.

        Args:
            stock_code: Stock code (e.g., "AAPL")
            market_code: Market code (e.g., "NAS", "NYS", "HKS", etc.)
            service_type: Service type indicator ("R" or "D", default "R")
                          - "R": Regular market / US Day market
                          - "D": US Night market
        """
        tr_key = self._generate_tr_key(stock_code, market_code, service_type)
        await self.socket_client.subscribe(self.TR_ID, tr_key)

    @_require_prod_env
    async def unsubscribe(self, stock_code: str, market_code: str, service_type: str = "R") -> None:
        """Unsubscribe from real-time orderbook data.

        Args:
            stock_code: Stock code to unsubscribe
            market_code: Market code
            service_type: Service type ("R" or "D")
        """
        tr_key = self._generate_tr_key(stock_code, market_code, service_type)
        await self.socket_client.unsubscribe(self.TR_ID, tr_key)

    @staticmethod
    def parse_data(data: List[str]) -> List[OverseasRealtimeOrderbookItem]:
        """Parse WebSocket data into list of OverseasRealtimeOrderbookItem.

        Args:
            data: List of string values from WebSocket message.
                  - Single record: 71 fields

        Returns:
            List of parsed OverseasRealtimeOrderbookItem models.
        """
        field_count = len(OVERSEAS_ORDERBOOK_FIELD_NAMES)

        # Validate minimum field count
        if len(data) < field_count:
            raise ValueError(
                f"Expected at least {field_count} fields, got {len(data)}. First field: {data[0] if data else 'empty'}"
            )

        # Calculate number of complete records
        num_records = len(data) // field_count

        results = []
        for i in range(num_records):
            start_idx = i * field_count
            end_idx = start_idx + field_count

            record_data = data[start_idx:end_idx]

            field_dict = dict(zip(OVERSEAS_ORDERBOOK_FIELD_NAMES, record_data, strict=False))
            item = OverseasRealtimeOrderbookItem.model_validate(field_dict)
            results.append(item)

        return results

    @_require_prod_env
    async def subscribe_execution(self, tr_key: str) -> None:
        """Subscribe to real-time delayed execution data.

        Args:
            tr_key: Transaction key (e.g., "DNASAAPL")
                    Format: D + market code (3 chars) + stock code
        """
        await self.socket_client.subscribe(self.TR_ID_EXECUTION, tr_key)

    @_require_prod_env
    async def unsubscribe_execution(self, tr_key: str) -> None:
        """Unsubscribe from real-time delayed execution data.

        Args:
            tr_key: Transaction key to unsubscribe
        """
        await self.socket_client.unsubscribe(self.TR_ID_EXECUTION, tr_key)

    @staticmethod
    def parse_execution_data(data: List[str]) -> List[OverseasRealtimeExecutionItem]:
        """Parse WebSocket data into list of OverseasRealtimeExecutionItem.

        WebSocket data is received as a list of string values separated by "^" delimiter.
        The API may send batched updates (multiple records concatenated).
        This method parses ALL records and returns them as a list.

        Args:
            data: List of string values from WebSocket message.
                  - Single record: 26 fields
                  - Batched: N×26 fields
                  - With extra fields: 26+ per record (forward compatible)

        Returns:
            List of parsed OverseasRealtimeExecutionItem models.
            Always returns a list, even for single records.

        Raises:
            ValueError: If data has insufficient fields (< 26)
        """
        field_count = len(OVERSEAS_EXECUTION_FIELD_NAMES)

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
            field_dict = dict(zip(OVERSEAS_EXECUTION_FIELD_NAMES, record_data, strict=False))
            item = OverseasRealtimeExecutionItem.model_validate(field_dict)
            results.append(item)

        return results

    @_require_prod_env
    async def subscribe_delayed_orderbook(self, tr_key: str) -> None:
        """Subscribe to delayed orderbook data (Asia).

        Args:
            tr_key: Transaction key (e.g., "DHKS00003")
                    Format: D + market code (3 chars) + stock code
        """
        await self.socket_client.subscribe(self.TR_ID_DELAYED_ORDERBOOK, tr_key)

    @_require_prod_env
    async def unsubscribe_delayed_orderbook(self, tr_key: str) -> None:
        """Unsubscribe from delayed orderbook data (Asia).

        Args:
            tr_key: Transaction key to unsubscribe
        """
        await self.socket_client.unsubscribe(self.TR_ID_DELAYED_ORDERBOOK, tr_key)

    @staticmethod
    def parse_delayed_orderbook_data(data: List[str]) -> List[OverseasRealtimeDelayedOrderbookItem]:
        """Parse WebSocket data into list of OverseasRealtimeDelayedOrderbookItem.

        WebSocket data is received as a list of string values separated by "^" delimiter.
        The API may send batched updates (multiple records concatenated).
        This method parses ALL records and returns them as a list.

        Args:
            data: List of string values from WebSocket message.
                  - Single record: 17 fields
                  - Batched: N×17 fields
                  - With extra fields: 17+ per record (forward compatible)

        Returns:
            List of parsed OverseasRealtimeDelayedOrderbookItem models.
            Always returns a list, even for single records.

        Raises:
            ValueError: If data has insufficient fields (< 17)
        """
        field_count = len(OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES)

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
            field_dict = dict(zip(OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES, record_data, strict=False))
            item = OverseasRealtimeDelayedOrderbookItem.model_validate(field_dict)
            results.append(item)

        return results

    @_require_prod_env
    async def subscribe_execution_notification(self, hts_id: str) -> None:
        """Subscribe to real-time execution notification.

        Args:
            hts_id: HTS ID for execution notification subscription
        """
        await self.socket_client.subscribe(self.TR_ID_EXECUTION_NOTIFICATION, hts_id)

    @_require_prod_env
    async def unsubscribe_execution_notification(self, hts_id: str) -> None:
        """Unsubscribe from real-time execution notification.

        Args:
            hts_id: HTS ID to unsubscribe
        """
        await self.socket_client.unsubscribe(self.TR_ID_EXECUTION_NOTIFICATION, hts_id)

    @staticmethod
    def parse_execution_notification_data(
        data: List[str],
    ) -> List[OverseasRealtimeExecutionNotificationItem]:
        """Parse WebSocket data into list of OverseasRealtimeExecutionNotificationItem.

        WebSocket data is received as a list of string values separated by "^" delimiter.
        The API may send batched updates (multiple records concatenated).
        This method parses ALL records and returns them as a list.

        Args:
            data: List of string values from WebSocket message.
                  - Single record: 25 fields
                  - Batched: N×25 fields
                  - With extra fields: 25+ per record (forward compatible)

        Returns:
            List of parsed OverseasRealtimeExecutionNotificationItem models.
            Always returns a list, even for single records.

        Raises:
            ValueError: If data has insufficient fields (< 25)
        """
        field_count = len(OVERSEAS_EXECUTION_NOTIFICATION_FIELD_NAMES)

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
            field_dict = dict(zip(OVERSEAS_EXECUTION_NOTIFICATION_FIELD_NAMES, record_data, strict=False))
            item = OverseasRealtimeExecutionNotificationItem.model_validate(field_dict)
            results.append(item)

        return results
