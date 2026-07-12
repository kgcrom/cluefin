"""미국주식 실시간 시세 (웹소켓).

운영: wss://api.kiwoom.com:10000/api/us/websocket
모의투자: wss://mockapi.kiwoom.com:10000/api/us/websocket

``KiwoomWebSocketClient``(LOGIN/PING 처리)를 감싸 실시간 시세 등록/해지(REG/REMOVE)
프레임을 송신하고, 수신한 REAL 프레임을 TR별 응답 모델로 파싱한다.

TR:
- F4 미국주식실시간주문확인 → OverseasRealtimeOrderConfirmation
- F5 미국주식실시간체결     → OverseasRealtimeExecution
- FE 미국주식실시간체결가   → OverseasRealtimeExecutionPrice
- FT 미국주식10호가         → OverseasRealtimeTenQuotes
"""

from typing import Iterable, Union

from ._overseas_realtime_types import (
    OverseasRealtimeExecution,
    OverseasRealtimeExecutionPrice,
    OverseasRealtimeOrderConfirmation,
    OverseasRealtimeRegisterData,
    OverseasRealtimeRegisterItem,
    OverseasRealtimeRequest,
    OverseasRealtimeTenQuotes,
)
from ._socket_client import KiwoomWebSocketClient, KiwoomWebSocketMessage

# 수신한 REAL 프레임의 ``data[].type`` → 응답 모델 매핑
_FRAME_MODELS = {
    "F4": OverseasRealtimeOrderConfirmation,
    "F5": OverseasRealtimeExecution,
    "FE": OverseasRealtimeExecutionPrice,
    "FT": OverseasRealtimeTenQuotes,
}


class OverseasRealtime:
    """미국주식 실시간 시세 WebSocket API.

    Example:
        ```python
        async with KiwoomWebSocketClient(token="...", env="prod") as ws:
            realtime = OverseasRealtime(ws)
            await realtime.register(["F5", "FT"], [("NVDA", "ND"), ("AAPL", "ND")])
            async for message in ws.events():
                parsed = realtime.parse(message)
                if parsed is not None:
                    print(parsed)
        ```
    """

    # 실시간 TR (type)
    TR_ORDER_CONFIRMATION = "F4"  # 미국주식실시간주문확인
    TR_EXECUTION = "F5"  # 미국주식실시간체결
    TR_EXECUTION_PRICE = "FE"  # 미국주식실시간체결가
    TR_TEN_QUOTES = "FT"  # 미국주식10호가

    def __init__(self, socket_client: KiwoomWebSocketClient):
        self.socket_client = socket_client

    async def register(
        self,
        types: Iterable[str],
        items: Iterable[Union[OverseasRealtimeRegisterItem, tuple[str, str]]],
        grp_no: str = "1",
        refresh: str = "1",
    ) -> None:
        """실시간 시세를 등록(REG)한다.

        Args:
            types: 등록할 TR type 리스트 (예: ["F5", "FT"]).
            items: 등록할 종목 리스트. ``OverseasRealtimeRegisterItem`` 또는
                ``(jmcode, stex_tp)`` 튜플 (예: ("NVDA", "ND")).
            grp_no: 그룹번호. Defaults to "1".
            refresh: 기존등록유지여부. "1":기존유지(Default), "0":기존등록 item/type 해지.
        """
        await self._send("REG", types, items, grp_no, refresh)

    async def remove(
        self,
        types: Iterable[str],
        items: Iterable[Union[OverseasRealtimeRegisterItem, tuple[str, str]]],
        grp_no: str = "1",
    ) -> None:
        """실시간 시세를 해지(REMOVE)한다.

        Args:
            types: 해지할 TR type 리스트.
            items: 해지할 종목 리스트.
            grp_no: 그룹번호. Defaults to "1".
        """
        # 해지시 refresh 값은 스펙상 불필요하지만 필수 필드이므로 "0"을 전달한다.
        await self._send("REMOVE", types, items, grp_no, "0")

    async def _send(
        self,
        trnm: str,
        types: Iterable[str],
        items: Iterable[Union[OverseasRealtimeRegisterItem, tuple[str, str]]],
        grp_no: str,
        refresh: str,
    ) -> None:
        register_items = [
            item
            if isinstance(item, OverseasRealtimeRegisterItem)
            else OverseasRealtimeRegisterItem(jmcode=item[0], stex_tp=item[1])
            for item in items
        ]
        request = OverseasRealtimeRequest(
            trnm=trnm,
            grp_no=grp_no,
            refresh=refresh,
            data=[OverseasRealtimeRegisterData(item=register_items, type=list(types))],
        )
        await self.socket_client.send(request)

    @staticmethod
    def parse(
        message: KiwoomWebSocketMessage,
    ) -> Union[
        OverseasRealtimeOrderConfirmation,
        OverseasRealtimeExecution,
        OverseasRealtimeExecutionPrice,
        OverseasRealtimeTenQuotes,
        None,
    ]:
        """수신 프레임을 TR type에 맞는 응답 모델로 파싱한다.

        ``data[].type``으로 TR을 판별하며, 실시간 대상이 아닌 프레임(빈 data, LOGIN/PING
        등)은 ``None``을 반환한다.

        Args:
            message: 수신한 WebSocket 메시지.

        Returns:
            파싱된 응답 모델. 대상 TR이 아니면 None.
        """
        data = message.body.get("data") or []
        tr_type = data[0].get("type") if data and isinstance(data[0], dict) else None
        model = _FRAME_MODELS.get(tr_type)
        if model is None:
            return None
        return model.model_validate(message.body)
