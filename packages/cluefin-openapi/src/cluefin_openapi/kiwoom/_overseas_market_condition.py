from typing import Literal

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._model import (
    KiwoomHttpHeader,
    KiwoomHttpResponse,
)
from cluefin_openapi.kiwoom._overseas_market_condition_types import (
    OverseasMarketConditionCurrentPriceStockInfo,
    OverseasMarketConditionCurrentPriceTenQuotes,
    OverseasMarketConditionDailyExecutionHistory,
    OverseasMarketConditionDailyStockPrice,
    OverseasMarketConditionDetailedExecutionHistory,
)


class OverseasMarketCondition:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/api/us/mrkcond"

    def get_current_price_stock_info(
        self,
        stex_tp: Literal["NA", "ND", "NY"],
        stk_cd: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasMarketConditionCurrentPriceStockInfo]:
        """미국주식 현재가 종목정보 (usa20100)

        Args:
            stex_tp (Literal["NA", "ND", "NY"]): 거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE
            stk_cd (str): 종목코드
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasMarketConditionCurrentPriceStockInfo]: 미국주식 현재가 종목정보 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20100",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching current price stock info: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasMarketConditionCurrentPriceStockInfo.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_current_price_ten_quotes(
        self,
        stex_tp: Literal["NA", "ND", "NY"],
        stk_cd: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasMarketConditionCurrentPriceTenQuotes]:
        """미국주식 현재가 10호가 (usa20101)

        Args:
            stex_tp (Literal["NA", "ND", "NY"]): 거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE
            stk_cd (str): 종목코드
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasMarketConditionCurrentPriceTenQuotes]: 미국주식 현재가 10호가 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20101",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching current price ten quotes: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasMarketConditionCurrentPriceTenQuotes.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_detailed_execution_history(
        self,
        stex_tp: Literal["NA", "ND", "NY"],
        stk_cd: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasMarketConditionDetailedExecutionHistory]:
        """미국주식 상세 체결내역 (usa20150)

        Args:
            stex_tp (Literal["NA", "ND", "NY"]): 거래소구분. NA:AMEX,ND:NASDAQ,NY:NYSE
            stk_cd (str): 종목코드
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasMarketConditionDetailedExecutionHistory]: 미국주식 상세 체결내역 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20150",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching detailed execution history: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasMarketConditionDetailedExecutionHistory.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_daily_execution_history(
        self,
        stex_tp: Literal["NA", "ND", "NY"],
        stk_cd: str,
        base_dt: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasMarketConditionDailyExecutionHistory]:
        """미국주식 일별 체결내역 (usa20151)

        Args:
            stex_tp (Literal["NA", "ND", "NY"]): 거래소구분. NA:AMEX,ND:NASDAQ,NY:NYSE
            stk_cd (str): 종목코드
            base_dt (str, optional): 기준일자. 기준일자 이전 내역 조회. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasMarketConditionDailyExecutionHistory]: 미국주식 일별 체결내역 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20151",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
            "base_dt": base_dt,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching daily execution history: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasMarketConditionDailyExecutionHistory.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_daily_stock_price(
        self,
        stex_tp: Literal["", "NA", "ND", "NY"] = "",
        stk_cd: str = "",
        base_dt: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasMarketConditionDailyStockPrice]:
        """미국주식 일별주가 (usa20590)

        Args:
            stex_tp (Literal["", "NA", "ND", "NY"], optional): 거래소구분. NA:AMEX,ND:NASDAQ,NY:NYSE. Defaults to "".
            stk_cd (str, optional): 종목코드. Defaults to "".
            base_dt (str, optional): 기준일자. 기준일자 이전 내역 조회. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasMarketConditionDailyStockPrice]: 미국주식 일별주가 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20590",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
            "base_dt": base_dt,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching daily stock price: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasMarketConditionDailyStockPrice.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)
