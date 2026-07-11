from typing import Literal

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._model import (
    KiwoomHttpHeader,
    KiwoomHttpResponse,
)
from cluefin_openapi.kiwoom._overseas_exchange_types import (
    OverseasExchangeEstimatedAmount,
    OverseasExchangeRate,
    OverseasExchangeRequest,
)


class OverseasExchange:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/api/us/exchange"

    def get_estimated_exchange_amount(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasExchangeEstimatedAmount]:
        """환전 예상 금액 조회 (ust31300)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasExchangeEstimatedAmount]: 환전 예상 금액 조회 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust31300",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching estimated exchange amount: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasExchangeEstimatedAmount.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_exchange_rate(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasExchangeRate]:
        """환율 조회 (ust31301)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasExchangeRate]: 환율 조회 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust31301",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching exchange rate: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasExchangeRate.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def request_exchange(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasExchangeRequest]:
        """환전 신청 (ust31302)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasExchangeRequest]: 환전 신청 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust31302",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error requesting exchange: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasExchangeRequest.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)
