"""미국주식 조건검색 (웹소켓).

운영: wss://api.kiwoom.com:10000/api/us/websocket
모의투자: wss://mockapi.kiwoom.com:10000/api/us/websocket

``KiwoomWebSocketClient``(LOGIN/PING 처리)를 감싸 조건검색 요청 프레임을 송신하고 응답을
파싱한다. 목록조회/요청 일반/해제는 요청-응답형이고, 요청 실시간(search_type=1)은 이후
편입/이탈 이벤트가 실시간 푸시로 도착한다.

TR:
- usa20280 조건검색 목록조회   GCNSRLST → OverseasConditionSearchListResponse
- usa20281 조건검색 요청 일반   GCNSRREQ(search_type=0) → OverseasConditionSearchResponse
- usa20290 조건검색 요청 실시간 GCNSRREQ(search_type=1) → OverseasConditionSearchRealtimeResponse
- usa20291 조건검색 실시간 해제 GCNSRCLR → OverseasConditionSearchRealtimeCancelResponse
"""

from typing import Literal

from ._overseas_condition_search_types import (
    OverseasConditionSearchListRequest,
    OverseasConditionSearchListResponse,
    OverseasConditionSearchRealtimeCancelRequest,
    OverseasConditionSearchRealtimeCancelResponse,
    OverseasConditionSearchRealtimeRequest,
    OverseasConditionSearchRealtimeResponse,
    OverseasConditionSearchRequest,
    OverseasConditionSearchResponse,
)
from ._socket_client import KiwoomWebSocketClient, KiwoomWebSocketMessage


class OverseasConditionSearch:
    """미국주식 조건검색 WebSocket API.

    Example:
        ```python
        async with KiwoomWebSocketClient(token="...", env="prod") as ws:
            condition = OverseasConditionSearch(ws)
            search_list = await condition.get_condition_search_list()
            result = await condition.request_condition_search(seq="0")
            print(result.data)
        ```
    """

    def __init__(self, socket_client: KiwoomWebSocketClient):
        self.socket_client = socket_client

    async def get_condition_search_list(self) -> OverseasConditionSearchListResponse:
        """미국주식 조건검색 목록조회 (usa20280, GCNSRLST).

        Returns:
            OverseasConditionSearchListResponse: 조건검색식 목록.
        """
        await self.socket_client.send(OverseasConditionSearchListRequest(trnm="GCNSRLST"))
        message = await self._recv_until("GCNSRLST")
        return OverseasConditionSearchListResponse.model_validate(message.body)

    async def request_condition_search(
        self,
        seq: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> OverseasConditionSearchResponse:
        """미국주식 조건검색 요청 일반 (usa20281, GCNSRREQ search_type=0).

        Args:
            seq: 조건검색식 일련번호.
            cont_yn: 연속조회여부. "Y":연속조회요청, "N":연속조회미요청.
            next_key: 연속조회키.

        Returns:
            OverseasConditionSearchResponse: 조건검색 결과.
        """
        await self.socket_client.send(
            OverseasConditionSearchRequest(
                trnm="GCNSRREQ",
                seq=seq,
                search_type="0",
                cont_yn=cont_yn,
                next_key=next_key,
            )
        )
        message = await self._recv_until("GCNSRREQ")
        return OverseasConditionSearchResponse.model_validate(message.body)

    async def request_realtime_condition_search(self, seq: str) -> OverseasConditionSearchRealtimeResponse:
        """미국주식 조건검색 요청 실시간 (usa20290, GCNSRREQ search_type=1).

        요청 직후 현재 편입 종목이 응답으로 반환되며, 이후 편입/이탈 이벤트는 실시간 푸시로
        도착한다 (``socket_client.events()``로 수신).

        Args:
            seq: 조건검색식 일련번호.

        Returns:
            OverseasConditionSearchRealtimeResponse: 실시간 조건검색 초기 결과.
        """
        await self.socket_client.send(OverseasConditionSearchRealtimeRequest(trnm="GCNSRREQ", seq=seq, search_type="1"))
        message = await self._recv_until("GCNSRREQ")
        return OverseasConditionSearchRealtimeResponse.model_validate(message.body)

    async def cancel_realtime_condition_search(self, seq: str) -> OverseasConditionSearchRealtimeCancelResponse:
        """미국주식 조건검색 실시간 해제 (usa20291, GCNSRCLR).

        Args:
            seq: 조건검색식 일련번호.

        Returns:
            OverseasConditionSearchRealtimeCancelResponse: 해제 ACK.
        """
        await self.socket_client.send(OverseasConditionSearchRealtimeCancelRequest(trnm="GCNSRCLR", seq=seq))
        message = await self._recv_until("GCNSRCLR")
        return OverseasConditionSearchRealtimeCancelResponse.model_validate(message.body)

    async def _recv_until(self, trnm: str) -> KiwoomWebSocketMessage:
        """지정한 ``trnm`` 응답 프레임이 올 때까지 수신한다.

        실시간 조건검색이 함께 켜져 있으면 REAL 푸시 프레임이 섞여 들어올 수 있으므로
        요청에 대응하는 응답 프레임만 골라 반환한다.
        """
        while True:
            message = await self.socket_client.recv()
            if message.trnm == trnm:
                return message
