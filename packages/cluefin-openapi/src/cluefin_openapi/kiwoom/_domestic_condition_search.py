"""국내주식 조건검색 (웹소켓).

운영: wss://api.kiwoom.com:10000/api/dostk/websocket
모의투자: wss://mockapi.kiwoom.com:10000/api/dostk/websocket (KRX만 지원)

``KiwoomWebSocketClient``(LOGIN/PING 처리)를 감싸 조건검색 요청 프레임을 송신하고 응답을
파싱한다. 목록조회/요청 일반/해제는 요청-응답형이고, 요청 실시간(search_type=1)은 이후
편입/이탈 이벤트가 실시간 푸시(trnm=REAL)로 도착한다. 국내는 거래소구분 ``stex_tp="K"``
(KRX)를 요청에 포함한다. (미국주식 ``_overseas_condition_search`` 와 대칭.)

TR:
- ka10171 조건검색 목록조회   CNSRLST → DomesticConditionSearchListResponse
- ka10172 조건검색 요청 일반   CNSRREQ(search_type=0) → DomesticConditionSearchResponse
- ka10173 조건검색 요청 실시간 CNSRREQ(search_type=1) → DomesticConditionSearchRealtimeResponse
- ka10174 조건검색 실시간 해제 CNSRCLR → DomesticConditionSearchRealtimeCancelResponse
"""

from typing import Literal

from ._domestic_condition_search_types import (
    DomesticConditionSearchListRequest,
    DomesticConditionSearchListResponse,
    DomesticConditionSearchRealtimeCancelRequest,
    DomesticConditionSearchRealtimeCancelResponse,
    DomesticConditionSearchRealtimeRequest,
    DomesticConditionSearchRealtimeResponse,
    DomesticConditionSearchRequest,
    DomesticConditionSearchResponse,
)
from ._socket_client import KiwoomWebSocketClient, KiwoomWebSocketMessage


class DomesticConditionSearch:
    """국내주식 조건검색 WebSocket API.

    Example:
        ```python
        async with KiwoomWebSocketClient(token="...", env="prod", market="domestic") as ws:
            condition = DomesticConditionSearch(ws)
            search_list = await condition.get_condition_search_list()
            result = await condition.request_condition_search(seq="0")
            print(result.data)
        ```
    """

    def __init__(self, socket_client: KiwoomWebSocketClient):
        self.socket_client = socket_client

    async def get_condition_search_list(self) -> DomesticConditionSearchListResponse:
        """국내주식 조건검색 목록조회 (ka10171, CNSRLST).

        Returns:
            DomesticConditionSearchListResponse: 조건검색식 목록.
        """
        await self.socket_client.send(DomesticConditionSearchListRequest(trnm="CNSRLST"))
        message = await self._recv_until("CNSRLST")
        return DomesticConditionSearchListResponse.model_validate(message.body)

    async def request_condition_search(
        self,
        seq: str,
        stex_tp: Literal["K"] = "K",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> DomesticConditionSearchResponse:
        """국내주식 조건검색 요청 일반 (ka10172, CNSRREQ search_type=0).

        Args:
            seq: 조건검색식 일련번호.
            stex_tp: 거래소구분. "K":KRX.
            cont_yn: 연속조회여부. "Y":연속조회요청, "N":연속조회미요청.
            next_key: 연속조회키.

        Returns:
            DomesticConditionSearchResponse: 조건검색 결과.
        """
        await self.socket_client.send(
            DomesticConditionSearchRequest(
                trnm="CNSRREQ",
                seq=seq,
                search_type="0",
                stex_tp=stex_tp,
                cont_yn=cont_yn,
                next_key=next_key,
            )
        )
        message = await self._recv_until("CNSRREQ")
        return DomesticConditionSearchResponse.model_validate(message.body)

    async def request_realtime_condition_search(
        self,
        seq: str,
        stex_tp: Literal["K"] = "K",
    ) -> DomesticConditionSearchRealtimeResponse:
        """국내주식 조건검색 요청 실시간 (ka10173, CNSRREQ search_type=1).

        요청 직후 현재 편입 종목이 응답으로 반환되며, 이후 편입/이탈 이벤트는 실시간 푸시로
        도착한다 (``socket_client.events()``로 수신, ``DomesticConditionSearchRealtimePush``).

        Args:
            seq: 조건검색식 일련번호.
            stex_tp: 거래소구분. "K":KRX.

        Returns:
            DomesticConditionSearchRealtimeResponse: 실시간 조건검색 초기 결과.
        """
        await self.socket_client.send(
            DomesticConditionSearchRealtimeRequest(trnm="CNSRREQ", seq=seq, search_type="1", stex_tp=stex_tp)
        )
        message = await self._recv_until("CNSRREQ")
        return DomesticConditionSearchRealtimeResponse.model_validate(message.body)

    async def cancel_realtime_condition_search(self, seq: str) -> DomesticConditionSearchRealtimeCancelResponse:
        """국내주식 조건검색 실시간 해제 (ka10174, CNSRCLR).

        Args:
            seq: 조건검색식 일련번호.

        Returns:
            DomesticConditionSearchRealtimeCancelResponse: 해제 ACK.
        """
        await self.socket_client.send(DomesticConditionSearchRealtimeCancelRequest(trnm="CNSRCLR", seq=seq))
        message = await self._recv_until("CNSRCLR")
        return DomesticConditionSearchRealtimeCancelResponse.model_validate(message.body)

    async def _recv_until(self, trnm: str) -> KiwoomWebSocketMessage:
        """지정한 ``trnm`` 응답 프레임이 올 때까지 수신한다.

        실시간 조건검색이 함께 켜져 있으면 REAL 푸시 프레임이 섞여 들어올 수 있으므로
        요청에 대응하는 응답 프레임만 골라 반환한다.
        """
        while True:
            message = await self.socket_client.recv()
            if message.trnm == trnm:
                return message
