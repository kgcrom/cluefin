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
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasMarketConditionCurrentPriceStockInfo]:
        """미국주식 현재가 종목정보 (usa20100)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching current price stock info: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasMarketConditionCurrentPriceStockInfo.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_current_price_ten_quotes(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasMarketConditionCurrentPriceTenQuotes]:
        """미국주식 현재가 10호가 (usa20101)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching current price ten quotes: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasMarketConditionCurrentPriceTenQuotes.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_detailed_execution_history(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasMarketConditionDetailedExecutionHistory]:
        """미국주식 상세 체결내역 (usa20150)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching detailed execution history: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasMarketConditionDetailedExecutionHistory.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_daily_execution_history(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasMarketConditionDailyExecutionHistory]:
        """미국주식 일별 체결내역 (usa20151)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching daily execution history: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasMarketConditionDailyExecutionHistory.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_daily_stock_price(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasMarketConditionDailyStockPrice]:
        """미국주식 일별주가 (usa20590)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching daily stock price: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasMarketConditionDailyStockPrice.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)
