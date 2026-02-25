"""장내채권 실시간시세 WebSocket API.

WebSocket을 통해 일반채권 실시간 체결가 및 채권지수 실시간 체결가 데이터를 구독합니다.

References:
- https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-bond-real
"""

from functools import wraps
from typing import List

from ._onmarket_bond_realtime_quote_types import (
    BOND_EXECUTION_FIELD_NAMES,
    BOND_INDEX_EXECUTION_FIELD_NAMES,
    OnmarketBondIndexRealtimeExecutionItem,
    OnmarketBondRealtimeExecutionItem,
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
                f"장내채권 실시간 체결가는 운영 서버(prod)에서만 사용 가능합니다. 현재 환경: {self.socket_client.env}"
            )
        return await func(self, *args, **kwargs)

    return wrapper


class OnmarketBondRealtimeQuote:
    """장내채권 실시간시세 WebSocket API.

    SocketClient를 사용하여 일반채권 실시간 체결가 및 채권지수 실시간 체결가 데이터를 구독합니다.

    Note:
        이 API는 운영 서버(prod)에서만 사용 가능합니다. 모의투자는 미지원됩니다.

    Example:
        ```python
        from cluefin_openapi.kis import Auth, SocketClient, OnmarketBondRealtimeQuote

        auth = Auth(app_key="...", secret_key=SecretStr("..."))
        approval = auth.approve()

        async with SocketClient(
            approval_key=approval.approval_key,
            app_key="...",
            secret_key=SecretStr("..."),
        ) as socket_client:
            realtime = OnmarketBondRealtimeQuote(socket_client)

            # Subscribe to real-time bond execution data
            await realtime.subscribe_execution("KR103502GA34")

            # Subscribe to real-time bond index execution data
            await realtime.subscribe_index_execution("BOND_IDX_001")

            # Process events
            async for event in socket_client.events():
                if event.event_type == "data" and event.tr_id == OnmarketBondRealtimeQuote.TR_ID_EXECUTION:
                    executions = realtime.parse_execution_data(event.data["values"])
                    for execution in executions:
                        print(f"Price: {execution.stck_prpr}, Yield: {execution.bond_cntg_ert}")
                elif event.event_type == "data" and event.tr_id == OnmarketBondRealtimeQuote.TR_ID_INDEX_EXECUTION:
                    index_data = realtime.parse_index_execution_data(event.data["values"])
                    for idx in index_data:
                        print(f"Index: {idx.nmix_id}, Total Return: {idx.totl_ernn_nmix}")
        ```
    """

    # Transaction IDs
    TR_ID_EXECUTION = "H0BJCNT0"  # 일반채권 실시간 체결가
    TR_ID_INDEX_EXECUTION = "H0BICNT0"  # 채권지수 실시간 체결가

    def __init__(self, socket_client: SocketClient):
        """Initialize OnmarketBondRealtimeQuote.

        Args:
            socket_client: Connected SocketClient instance
        """
        self.socket_client = socket_client

    @_require_prod_env
    async def subscribe_execution(self, bond_code: str) -> None:
        """Subscribe to real-time bond execution data.

        Args:
            bond_code: Bond code (e.g., "KR103502GA34")
        """
        await self.socket_client.subscribe(self.TR_ID_EXECUTION, bond_code)

    @_require_prod_env
    async def unsubscribe_execution(self, bond_code: str) -> None:
        """Unsubscribe from real-time bond execution data.

        Args:
            bond_code: Bond code to unsubscribe
        """
        await self.socket_client.unsubscribe(self.TR_ID_EXECUTION, bond_code)

    @staticmethod
    def parse_execution_data(data: List[str]) -> List[OnmarketBondRealtimeExecutionItem]:
        """Parse WebSocket data into list of OnmarketBondRealtimeExecutionItem.

        WebSocket data is received as a list of string values separated by "^" delimiter.
        The API may send batched updates (multiple records concatenated).
        This method parses ALL records and returns them as a list.

        Args:
            data: List of string values from WebSocket message.
                  - Single record: 19 fields
                  - Batched: N×19 fields
                  - With extra fields: 19+ per record (forward compatible)

        Returns:
            List of parsed OnmarketBondRealtimeExecutionItem models.
            Always returns a list, even for single records.

        Raises:
            ValueError: If data has insufficient fields (< 19)

        Example:
            ```python
            # Single record
            data = ["KR103502GA34", "국고채권03500-5306", "093000", ...]  # 19 fields
            items = parse_execution_data(data)
            assert len(items) == 1

            # Batched records
            data = [...] * 5  # 95 fields = 5 records
            items = parse_execution_data(data)
            assert len(items) == 5

            for item in items:
                print(f"Price: {item.stck_prpr}, Yield: {item.bond_cntg_ert}")
            ```
        """
        field_count = len(BOND_EXECUTION_FIELD_NAMES)

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
            field_dict = dict(zip(BOND_EXECUTION_FIELD_NAMES, record_data, strict=False))
            item = OnmarketBondRealtimeExecutionItem.model_validate(field_dict)
            results.append(item)

        return results

    @_require_prod_env
    async def subscribe_index_execution(self, bond_code: str) -> None:
        """Subscribe to real-time bond index execution data.

        Args:
            bond_code: Bond index code (e.g., "BOND_IDX_001")
        """
        await self.socket_client.subscribe(self.TR_ID_INDEX_EXECUTION, bond_code)

    @_require_prod_env
    async def unsubscribe_index_execution(self, bond_code: str) -> None:
        """Unsubscribe from real-time bond index execution data.

        Args:
            bond_code: Bond index code to unsubscribe
        """
        await self.socket_client.unsubscribe(self.TR_ID_INDEX_EXECUTION, bond_code)

    @staticmethod
    def parse_index_execution_data(data: List[str]) -> List[OnmarketBondIndexRealtimeExecutionItem]:
        """Parse WebSocket data into list of OnmarketBondIndexRealtimeExecutionItem.

        WebSocket data is received as a list of string values separated by "^" delimiter.
        The API may send batched updates (multiple records concatenated).
        This method parses ALL records and returns them as a list.

        Args:
            data: List of string values from WebSocket message.
                  - Single record: 20 fields
                  - Batched: N×20 fields
                  - With extra fields: 20+ per record (forward compatible)

        Returns:
            List of parsed OnmarketBondIndexRealtimeExecutionItem models.
            Always returns a list, even for single records.

        Raises:
            ValueError: If data has insufficient fields (< 20)

        Example:
            ```python
            # Single record
            data = ["BOND_IDX_001", "20240101", "093000", ...]  # 20 fields
            items = parse_index_execution_data(data)
            assert len(items) == 1

            # Batched records
            data = [...] * 5  # 100 fields = 5 records
            items = parse_index_execution_data(data)
            assert len(items) == 5

            for item in items:
                print(f"Index: {item.nmix_id}, Total Return: {item.totl_ernn_nmix}")
            ```
        """
        field_count = len(BOND_INDEX_EXECUTION_FIELD_NAMES)

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
            field_dict = dict(zip(BOND_INDEX_EXECUTION_FIELD_NAMES, record_data, strict=False))
            item = OnmarketBondIndexRealtimeExecutionItem.model_validate(field_dict)
            results.append(item)

        return results
