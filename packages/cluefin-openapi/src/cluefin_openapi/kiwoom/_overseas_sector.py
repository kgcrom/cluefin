from typing import Literal

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._model import (
    KiwoomHttpHeader,
    KiwoomHttpResponse,
)
from cluefin_openapi.kiwoom._overseas_sector_types import (
    OverseasSectorIndustryFluctuationRank,
    OverseasSectorIndustryPeriodProfitRate,
)


class OverseasSector:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/api/us/sect"

    def get_industry_period_profit_rate(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasSectorIndustryPeriodProfitRate]:
        """미국주식 업종별 기간별 수익률 조회 (usa23000)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasSectorIndustryPeriodProfitRate]: 미국주식 업종별 기간별 수익률 조회 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa23000",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching industry period profit rate: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasSectorIndustryPeriodProfitRate.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_industry_fluctuation_rank(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasSectorIndustryFluctuationRank]:
        """미국주식 업종별 등락률 상위/하위 조회 (usa23100)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasSectorIndustryFluctuationRank]: 미국주식 업종별 등락률 상위/하위 조회 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa23100",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching industry fluctuation rank: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasSectorIndustryFluctuationRank.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)
