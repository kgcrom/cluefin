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
        exch_tp: Literal["1", "2"],
        fc_exmn_amt: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasExchangeEstimatedAmount]:
        """환전 예상 금액 조회 (ust31300)

        Args:
            exch_tp (Literal["1", "2"]): 환전구분. 1:원화(KRW)->달러(USD), 2:달러(USD)->원화(KRW)
            fc_exmn_amt (str, optional): 매도통화기준 환전금액. EXCH_TP = 1 인 경우, 매도통화는 KRW 이며, 입력한 금액의 원화를 달러로 환전합니다. EXCH_TP = 2 인 경우, 매도통화: USD이며, 입력한 금액의 달러를 원화로 환전합니다. Defaults to "".
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
        body = {
            "exch_tp": exch_tp,
            "fc_exmn_amt": fc_exmn_amt,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching estimated exchange amount: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasExchangeEstimatedAmount.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_exchange_rate(
        self,
        exch_tp: Literal["1", "2"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasExchangeRate]:
        """환율 조회 (ust31301)

        Args:
            exch_tp (Literal["1", "2"]): 환전구분. 1:원화(KRW)->달러(USD), 2:달러(USD)->원화(KRW)
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
        body = {
            "exch_tp": exch_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching exchange rate: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasExchangeRate.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def request_exchange(
        self,
        exch_tp: Literal["1", "2"],
        fc_exmn_amt: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasExchangeRequest]:
        """환전 신청 (ust31302)

        Args:
            exch_tp (Literal["1", "2"]): 환전구분. 1:원화(KRW)->달러(USD), 2:달러(USD)->원화(KRW)
            fc_exmn_amt (str): 매도통화기준 환전금액. EXCH_TP = 1 인 경우, 매도통화는 KRW 이며, 입력한 금액의 원화를 달러로 환전합니다. EXCH_TP = 2 인 경우, 매도통화: USD이며, 입력한 금액의 달러를 원화로 환전합니다.
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
        body = {
            "exch_tp": exch_tp,
            "fc_exmn_amt": fc_exmn_amt,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error requesting exchange: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasExchangeRequest.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)
