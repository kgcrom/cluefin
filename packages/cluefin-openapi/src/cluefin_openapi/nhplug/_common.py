from typing import Optional

from cluefin_openapi.nhplug._common_types import AccountList, WebsocketCloseResponse
from cluefin_openapi.nhplug._http_client import HttpClient
from cluefin_openapi.nhplug._model import NHPlugHttpHeader, NHPlugHttpResponse
from cluefin_openapi.nhplug._response import check_response_error


class Common:
    """공통 (계좌·실시간 세션) — 자산군과 무관한 플랫폼 공통 API.

    스펙 정본: https://www.nhplug.com/openapi-docs/common/openapi.json
    """

    def __init__(self, client: HttpClient):
        self.client = client

    def _check_response_error(self, response_data: dict) -> None:
        check_response_error(response_data)

    def get_account_list(self, cts: Optional[str] = None) -> NHPlugHttpResponse[AccountList]:
        """계좌 목록 조회 (`POST /n2/acctinfo`).

        모든 자산군 조회·주문 API 는 계좌번호(`act_no`)를 입력으로 요구하므로
        토큰 발급 후 가장 먼저 호출한다. `acct_type` 이 호출 환경과 일치하는
        계좌를 선택할 것 (01·02: 운영 전용, 03: 모의투자 전용).

        Args:
            cts: 연속거래키. 이전 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 전달.
        """
        response = self.client.post("/n2/acctinfo", cts=cts)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        body = AccountList.model_validate(data)
        return NHPlugHttpResponse(header=header, body=body)

    def close_websocket_session(self) -> NHPlugHttpResponse[WebsocketCloseResponse]:
        """실시간(Websocket) 세션해제 (`POST /websocket/close/session`).

        현재 토큰으로 열려 있는 실시간 WebSocket 세션을 서버측에서 정리한다.
        """
        response = self.client.post("/websocket/close/session")
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        body = WebsocketCloseResponse.model_validate(data)
        return NHPlugHttpResponse(header=header, body=body)
