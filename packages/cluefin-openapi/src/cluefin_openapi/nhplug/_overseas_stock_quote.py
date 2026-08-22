from typing import Optional

from cluefin_openapi.nhplug._http_client import HttpClient
from cluefin_openapi.nhplug._model import NHPlugHttpHeader, NHPlugHttpResponse
from cluefin_openapi.nhplug._overseas_stock_quote_types import OverseasStockCurrentPrice
from cluefin_openapi.nhplug._response import check_response_error


class OverseasStockQuote:
    """해외주식 시세 (gbstock quote).

    스펙 정본: https://www.nhplug.com/openapi-docs/gbstock/openapi.json
    """

    def __init__(self, client: HttpClient):
        self.client = client

    def _check_response_error(self, response_data: dict) -> None:
        check_response_error(response_data)

    def get_current_price(
        self,
        iem_cd: str,
        cts: Optional[str] = None,
    ) -> NHPlugHttpResponse[OverseasStockCurrentPrice]:
        """해외주식 현재가상세 (`POST /gbstock/quote/v1/current`).

        해외주식 현재가를 조회하는 API 이다. 응답 블록은 데이터가 있을 때만
        내려오므로 존재 여부를 먼저 확인해야 한다.

        Args:
            iem_cd: 종목코드 (길이 15). 예: 미국주식 APPLE인 경우 AAPL
            cts: 연속거래키. 이전 응답 헤더의 `cts` 값을 그대로 전달하면 다음 페이지를 받는다.

        Returns:
            NHPlugHttpResponse[OverseasStockCurrentPrice]: 현재가상세 조회 결과(`Output_0`)
        """
        body: dict = {
            "iem_cd": iem_cd,
        }

        response = self.client.post("/gbstock/quote/v1/current", body=body, cts=cts)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=OverseasStockCurrentPrice.model_validate(data))
