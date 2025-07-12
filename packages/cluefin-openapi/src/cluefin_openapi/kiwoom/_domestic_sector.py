from typing import Literal

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_sector_types import (
    DomesticSectorAllIndustryIndex,
    DomesticSectorDailyIndustryCurrentPrice,
    DomesticSectorIndustryCurrentPrice,
    DomesticSectorIndustryInvestorNetBuy,
    DomesticSectorIndustryPriceBySector,
    DomesticSectorIndustryProgram,
)
from cluefin_openapi.kiwoom._model import (
    KiwoomHttpHeader,
    KiwoomHttpResponse,
)


class DomesticSector:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/api/dostk/sect"

    def get_industry_program(
        self, stk_code: str, cont_yn: Literal["Y", "N"] = "N", next_key: str = ""
    ) -> KiwoomHttpResponse[DomesticSectorIndustryProgram]:
        """업종프로그램요청

        Args:
            stk_code (str): 업종코드
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            dict: 업종 프로그램 데이터
        """

        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10010",
        }
        body = {"stk_code": stk_code}

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching industry program: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticSectorIndustryProgram.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_industry_investor_net_buy(
        self,
        mrkt_tp: Literal["0", "1"],
        amt_qty_tp: Literal["0", "1"],
        base_dt: str,
        stex_tp: Literal["1", "2", "3"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticSectorIndustryInvestorNetBuy]:
        """업종별투자자순매수요청

        Args:
            mrkt_tp (Literal["0", "1"]): 시장구분 (코스피:0, 코스닥:1)
            amt_qty_tp (Literal["0", "1"]): 금액수량구분 (금액:0, 수량:1)
            base_dt (str): 기준일자 (YYYYMMDD)
            stex_tp (Literal["1", "2", "3"]): 거래소구분 (1:KRX, 2:NXT, 3:통합)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            dict: 업종별 투자자 순매수 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10051",
        }
        body = {
            "mrkt_tp": mrkt_tp,
            "amt_qty_tp": amt_qty_tp,
            "base_dt": base_dt,
            "stex_tp": stex_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching industry investor net buy: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticSectorIndustryInvestorNetBuy.model_validate(response.json())

        return KiwoomHttpResponse(headers=headers, body=body)

    def get_industry_current_price(
        self, mrkt_tp: Literal["0", "1", "2"], inds_cd: str, cont_yn: Literal["Y", "N"] = "N", next_key: str = ""
    ) -> KiwoomHttpResponse[DomesticSectorIndustryCurrentPrice]:
        """업종현재가요청

        Args:
            mrkt_tp (Literal["0", "1", "2"]): 시장구분 (코스피:0, 코스닥:1, 코스피200:2)
            inds_cd (str): 업종코드 (예: 001:종합(KOSPI), 002:대형주 등)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            dict: 업종 현재가 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka20001",
        }
        body = {
            "mrkt_tp": mrkt_tp,
            "inds_cd": inds_cd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching industry current price: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticSectorIndustryCurrentPrice.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_industry_price_by_sector(
        self,
        mrkt_tp: Literal["0", "1", "2"],
        inds_cd: str,
        stex_tp: Literal["1", "2", "3"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticSectorIndustryPriceBySector]:
        """업종별주가요청

        Args:
            mrkt_tp (Literal["0", "1", "2"]): 시장구분 (코스피:0, 코스닥:1, 코스피200:2)
            inds_cd (str): 업종코드 (예: 001:종합(KOSPI), 002:대형주 등)
            stex_tp (Literal["1", "2", "3"]): 거래소구분 (1:KRX, 2:NXT, 3:통합)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            dict: 업종별 주가 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka20002",
        }
        body = {
            "mrkt_tp": mrkt_tp,
            "inds_cd": inds_cd,
            "stex_tp": stex_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching industry price by sector: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticSectorIndustryPriceBySector.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_all_industry_index(
        self, inds_cd: str, cont_yn: Literal["Y", "N"] = "N", next_key: str = ""
    ) -> KiwoomHttpResponse[DomesticSectorAllIndustryIndex]:
        """전업종지수요청

        Args:
            inds_cd (str): 업종코드 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            dict: 전업종 지수 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka20003",
        }
        body = {
            "inds_cd": inds_cd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching all industry index: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticSectorAllIndustryIndex.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_daily_industry_current_price(
        self, mrkt_tp: Literal["0", "1", "2"], inds_cd: str, cont_yn: Literal["Y", "N"] = "N", next_key: str = ""
    ) -> KiwoomHttpResponse[DomesticSectorDailyIndustryCurrentPrice]:
        """업종현재가일별요청

        Args:
            mrkt_tp (Literal["0", "1", "2"]): 시장구분 (코스피:0, 코스닥:1, 코스피200:2)
            inds_cd (str): 업종코드 (예: 001:종합(KOSPI), 002:대형주 등)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            dict: 업종 현재가 일별 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka20009",
        }
        body = {
            "mrkt_tp": mrkt_tp,
            "inds_cd": inds_cd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching daily industry current price: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticSectorDailyIndustryCurrentPrice.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)
