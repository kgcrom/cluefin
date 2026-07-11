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
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        inds_cd: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasSectorIndustryPeriodProfitRate]:
        """미국주식 업종별 기간별 수익률 조회 (usa23000)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소 구분. 0:전체,1:NYSE,2:AMEX,3:NASDAQ. Defaults to "".
            inds_cd (str, optional): 업종 코드. 0:전체, usa10101 참고. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "inds_cd": inds_cd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching industry period profit rate: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasSectorIndustryPeriodProfitRate.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_industry_fluctuation_rank(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        sort_tp: Literal["", "1", "2"] = "",
        inds_cd: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasSectorIndustryFluctuationRank]:
        """미국주식 업종별 등락률 상위/하위 조회 (usa23100)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소 구분. 0:전체,1:NY(NYSE),2:NA(AMEX),3:ND(NASDAQ). Defaults to "".
            sort_tp (Literal["", "1", "2"], optional): 정렬기준구분. 1:등락율상위,2:등락율하위. Defaults to "".
            inds_cd (str, optional): 업종코드. 000:전체(기본값), usa10101 참고. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "sort_tp": sort_tp,
            "inds_cd": inds_cd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching industry fluctuation rank: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasSectorIndustryFluctuationRank.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)
