from typing import Any, Dict, Literal

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient
from cluefin_openapi.nhplug._krstock_quote_types import KrStockQuoteCurrentPrice
from cluefin_openapi.nhplug._model import SUCCESS_RSP_CODES, NHPlugHttpHeader, NHPlugHttpResponse


class KrStockQuote:
    """국내주식 시세.

    스펙 정본: https://www.nhplug.com/openapi-docs/krstock/openapi.json
    시세 조회 API 는 계좌번호가 필요 없다(조회·주문 카테고리와 다름).
    """

    def __init__(self, client: HttpClient):
        self.client = client

    def _check_response_error(self, response_data: dict) -> None:
        """HTTP 200 이어도 body rsp_cd 가 실패일 수 있으므로 여기서 확인한다."""
        rsp_cd = response_data.get("rsp_cd")
        if rsp_cd is not None and rsp_cd not in SUCCESS_RSP_CODES:
            raise NHPlugAPIError(
                f"API error {rsp_cd}: {response_data.get('rsp_msg', '')}",
                status_code=200,
                response_data=response_data,
            )

    @staticmethod
    def _drop_none(body: Dict[str, Any]) -> Dict[str, Any]:
        """선택 파라미터는 값이 있을 때만 전송한다."""
        return {k: v for k, v in body.items() if v is not None}

    def current_price(
        self,
        market_cd: Literal["KRX", "NXT", "UNT"],
        iem_cd: str,
    ) -> NHPlugHttpResponse[KrStockQuoteCurrentPrice]:
        """주식현재가 시세 (`POST /krstock/quote/v1/currentPrice`).

        스펙상 2개 입력 필드가 모두 required 다. 계좌번호가 필요 없는 시세 조회
        API 다. 스펙에 `CtsHeader` 파라미터가 없어 연속조회를 지원하지 않는다
        (다른 조회 API 와 달리 `cts` 인자가 없다).

        Args:
            market_cd: 시장구분코드 (KRX/NXT/UNT)
            iem_cd: 종목코드 (예: 005930)
        """
        body = self._drop_none(
            {
                "market_cd": market_cd,
                "iem_cd": iem_cd,
            }
        )
        response = self.client.post("/krstock/quote/v1/currentPrice", body=body)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockQuoteCurrentPrice.model_validate(data))
