"""국내주식 실시간 시세 (웹소켓).

운영: wss://api.kiwoom.com:10000/api/dostk/websocket
모의투자: wss://mockapi.kiwoom.com:10000/api/dostk/websocket (KRX만 지원)

``KiwoomWebSocketClient``(LOGIN/PING 처리)를 감싸 실시간 시세 등록/해지(REG/REMOVE)
프레임을 송신하고, 수신한 REAL 프레임을 TR별 응답 모델로 파싱한다. 국내는 등록 요소
``item``이 거래소별 종목/업종코드 문자열(KRX:039490, NXT:039490_NX, SOR:039490_AL)이다.
(미국주식 ``_overseas_realtime`` 와 대칭.)

TR (type):
- 00 주문체결        → DomesticRealtimeOrderExecution
- 04 잔고            → DomesticRealtimeBalance
- 0A 주식기세        → DomesticRealtimeStockMomentum
- 0B 주식체결        → DomesticRealtimeStockExecution
- 0C 주식우선호가    → DomesticRealtimeStockPriorityQuote
- 0D 주식호가잔량    → DomesticRealtimeStockQuoteRemaining
- 0E 주식시간외호가  → DomesticRealtimeStockAfterHoursQuote
- 0F 주식당일거래원  → DomesticRealtimeStockCurrentDayTrader
- 0G ETF NAV         → DomesticRealtimeEtfNav
- 0H 주식예상체결    → DomesticRealtimeStockExpectedExecution
- 0I 국제금환산가격  → DomesticRealtimeIntlGoldPrice
- 0J 업종지수        → DomesticRealtimeIndustryIndex
- 0U 업종등락        → DomesticRealtimeIndustryFluctuation
- 0g 주식종목정보    → DomesticRealtimeStockItemInfo
- 0m ELW 이론가      → DomesticRealtimeElwTheoreticalPrice
- 0s 장시작시간      → DomesticRealtimeMarketStartTime
- 0u ELW 지표        → DomesticRealtimeElwIndicator
- 0w 종목프로그램매매 → DomesticRealtimeStockProgramTrading
- 1h VI발동/해제     → DomesticRealtimeViActivation
"""

from typing import Iterable, Optional

from pydantic import BaseModel

from ._domestic_realtime_types import (
    DomesticRealtimeBalance,
    DomesticRealtimeElwIndicator,
    DomesticRealtimeElwTheoreticalPrice,
    DomesticRealtimeEtfNav,
    DomesticRealtimeIndustryFluctuation,
    DomesticRealtimeIndustryIndex,
    DomesticRealtimeIntlGoldPrice,
    DomesticRealtimeMarketStartTime,
    DomesticRealtimeOrderExecution,
    DomesticRealtimeRegisterData,
    DomesticRealtimeRequest,
    DomesticRealtimeStockAfterHoursQuote,
    DomesticRealtimeStockCurrentDayTrader,
    DomesticRealtimeStockExecution,
    DomesticRealtimeStockExpectedExecution,
    DomesticRealtimeStockItemInfo,
    DomesticRealtimeStockMomentum,
    DomesticRealtimeStockPriorityQuote,
    DomesticRealtimeStockProgramTrading,
    DomesticRealtimeStockQuoteRemaining,
    DomesticRealtimeViActivation,
)
from ._socket_client import KiwoomWebSocketClient, KiwoomWebSocketMessage

# 수신한 REAL 프레임의 ``data[].type`` → 응답 모델 매핑
_FRAME_MODELS = {
    "00": DomesticRealtimeOrderExecution,
    "04": DomesticRealtimeBalance,
    "0A": DomesticRealtimeStockMomentum,
    "0B": DomesticRealtimeStockExecution,
    "0C": DomesticRealtimeStockPriorityQuote,
    "0D": DomesticRealtimeStockQuoteRemaining,
    "0E": DomesticRealtimeStockAfterHoursQuote,
    "0F": DomesticRealtimeStockCurrentDayTrader,
    "0G": DomesticRealtimeEtfNav,
    "0H": DomesticRealtimeStockExpectedExecution,
    "0I": DomesticRealtimeIntlGoldPrice,
    "0J": DomesticRealtimeIndustryIndex,
    "0U": DomesticRealtimeIndustryFluctuation,
    "0g": DomesticRealtimeStockItemInfo,
    "0m": DomesticRealtimeElwTheoreticalPrice,
    "0s": DomesticRealtimeMarketStartTime,
    "0u": DomesticRealtimeElwIndicator,
    "0w": DomesticRealtimeStockProgramTrading,
    "1h": DomesticRealtimeViActivation,
}


class DomesticRealtime:
    """국내주식 실시간 시세 WebSocket API.

    Example:
        ```python
        async with KiwoomWebSocketClient(token="...", env="prod", market="domestic") as ws:
            realtime = DomesticRealtime(ws)
            await realtime.register(["0B", "0D"], ["005930", "000660"])
            async for message in ws.events():
                parsed = realtime.parse(message)
                if parsed is not None:
                    print(parsed)
        ```
    """

    def __init__(self, socket_client: KiwoomWebSocketClient):
        self.socket_client = socket_client

    async def register(
        self,
        types: Iterable[str],
        items: Iterable[str],
        grp_no: str = "1",
        refresh: str = "1",
    ) -> None:
        """실시간 시세를 등록(REG)한다.

        Args:
            types: 등록할 TR type 리스트 (예: ["0B", "0D"]).
            items: 등록할 종목코드 리스트. 거래소별 종목/업종코드
                (KRX:039490, NXT:039490_NX, SOR:039490_AL).
            grp_no: 그룹번호. Defaults to "1".
            refresh: 기존등록유지여부. "1":기존유지(Default), "0":기존등록 item/type 해지.
        """
        await self._send("REG", types, items, grp_no, refresh)

    async def remove(
        self,
        types: Iterable[str],
        items: Iterable[str],
        grp_no: str = "1",
    ) -> None:
        """실시간 시세를 해지(REMOVE)한다.

        Args:
            types: 해지할 TR type 리스트.
            items: 해지할 종목코드 리스트.
            grp_no: 그룹번호. Defaults to "1".
        """
        # 해지시 refresh 값은 스펙상 불필요하지만 필수 필드이므로 "0"을 전달한다.
        await self._send("REMOVE", types, items, grp_no, "0")

    async def _send(
        self,
        trnm: str,
        types: Iterable[str],
        items: Iterable[str],
        grp_no: str,
        refresh: str,
    ) -> None:
        request = DomesticRealtimeRequest(
            trnm=trnm,
            grp_no=grp_no,
            refresh=refresh,
            data=[DomesticRealtimeRegisterData(item=list(items), type=list(types))],
        )
        await self.socket_client.send(request)

    @staticmethod
    def parse(message: KiwoomWebSocketMessage) -> Optional[BaseModel]:
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
