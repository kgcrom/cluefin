from typing import Literal

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._model import (
    KiwoomHttpHeader,
    KiwoomHttpResponse,
)
from cluefin_openapi.kiwoom._overseas_investment_info_types import (
    OverseasInvestmentInfoResearch,
)


class OverseasInvestmentInfo:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/api/us/invtinfo"

    def get_research(
        self,
        qry_tp: Literal["", "0", "1"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasInvestmentInfoResearch]:
        """미국주식 리서치(미국주식/ETF) (usa24300)

        Args:
            qry_tp (Literal["", "0", "1"], optional): 주식/ETF 구분. 0:미국주식,1:글로벌ETF. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasInvestmentInfoResearch]: 미국주식 리서치(미국주식/ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa24300",
        }
        body = {
            "qry_tp": qry_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching research: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasInvestmentInfoResearch.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)
