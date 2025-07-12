from typing import Literal, Optional

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_etf_types import (
    DomesticEtfDailyExecution,
    DomesticEtfDailyTrend,
    DomesticEtfFullPrice,
    DomesticEtfHourlyExecution,
    DomesticEtfHourlyExecutionV2,
    DomesticEtfHourlyTrend,
    DomesticEtfHourlyTrendV2,
    DomesticEtfItemInfo,
    DomesticEtfReturnRate,
)
from cluefin_openapi.kiwoom._model import (
    KiwoomHttpHeader,
    KiwoomHttpResponse,
)


class DomesticETF:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/api/dostk/etf"

    def get_etf_return_rate(
        self, stk_cd: str, etfobjt_idex_cd: str, dt: int, cont_yn: Literal["Y", "N"] = "N", next_key: str = ""
    ) -> KiwoomHttpResponse[DomesticEtfReturnRate]:
        """ETF수익률요청

        Args:
            stk_cd (str): 종목코드 (예: KRX:069500)
            etfobjt_idex_cd (str): ETF대상지수코드 (예: 001)
            dt (int): 기간 (0:1주, 1:1달, 2:6개월, 3:1년)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticEtfReturnRate]: ETF 수익률 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka40001",
        }
        body = {"stk_cd": stk_cd, "etfobjt_idex_cd": etfobjt_idex_cd, "dt": dt}

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching ETF return rate: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticEtfReturnRate.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_etf_item_info(
        self, stk_cd: str, cont_yn: Literal["Y", "N"] = "N", next_key: str = ""
    ) -> KiwoomHttpResponse[DomesticEtfItemInfo]:
        """ETF종목정보요청

        Args:
            stk_cd (str): 종목코드 (예: KRX:069500)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticEtfItemInfo]: ETF 종목 정보 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka40002",
        }
        body = {"stk_cd": stk_cd}

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching ETF item info: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticEtfItemInfo.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_etf_daily_trend(
        self, stk_cd: str, cont_yn: Literal["Y", "N"] = "N", next_key: str = ""
    ) -> KiwoomHttpResponse[DomesticEtfDailyTrend]:
        """ETF일별추이요청

        Args:
            stk_cd (str): 종목코드 (예: KRX:069500)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticEtfDailyTrend]: ETF 일별 추이 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka40003",
        }
        body = {"stk_cd": stk_cd}

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching ETF daily trend: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticEtfDailyTrend.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_etf_full_price(
        self,
        txon_type: Literal["0", "1", "2", "3", "4", "5"],
        navpre: Literal["0", "1", "2"],
        mngmcomp: Literal["0000", "3020", "3027", "3191", "3228", "3023", "3022", "9999"],
        txon_yn: Literal["0", "1", "2"],
        trace_idex: Literal["0"],
        stex_tp: Literal["1", "2", "3"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticEtfFullPrice]:
        """ETF전체시세요청

        Args:
            txon_type (Literal["0", "1", "2", "3", "4", "5"]): 과세유형 (0:전체, 1:비과세, 2:보유기간과세, 3:회사형, 4:외국, 5:비과세해외(보유기간관세))
            navpre (Literal["0", "1", "2"]): NAV대비 (0:전체, 1:NAV > 전일종가, 2:NAV < 전일종가)
            mngmcomp (Literal["0000", "3020", "3027", "3191", "3228", "3023", "3022", "9999"]): 운용사 (0000:전체, 3020:KODEX(삼성), 3027:KOSEF(키움), 3191:TIGER(미래에셋), 3228:KINDEX(한국투자), 3023:KStar(KB), 3022:아리랑(한화), 9999:기타운용사)
            txon_yn (Literal["0", "1", "2"]): 과세여부 (0:전체, 1:과세, 2:비과세)
            trace_idex (Literal["0"]): 추적지수 (0:전체)
            stex_tp (Literal["1", "2", "3"]): 거래소구분 (1:KRX, 2:NXT, 3:통합)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".
        Returns:
            KiwoomHttpResponse[DomesticEtfFullPrice]: ETF 전체 시세 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka40004",
        }
        body = {
            "txon_type": txon_type,
            "navpre": navpre,
            "mngmcomp": mngmcomp,
            "txon_yn": txon_yn,
            "trace_idex": trace_idex,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching ETF full price: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticEtfFullPrice.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_etf_hourly_trend(
        self, stk_cd: str, cont_yn: Literal["Y", "N"] = "N", next_key: str = ""
    ) -> KiwoomHttpResponse[DomesticEtfHourlyTrend]:
        """ETF시간대별추이요청

        Args:
            stk_cd (str): 종목코드
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticEtfHourlyTrend]: ETF 시간대별 추이 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka40006",
        }
        body = {"stk_cd": stk_cd}

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching ETF hourly trend: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticEtfHourlyTrend.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_etf_hourly_execution(
        self, stk_cd: str, cont_yn: Literal["Y", "N"] = "N", next_key: str = ""
    ) -> KiwoomHttpResponse[DomesticEtfHourlyExecution]:
        """ETF시간대별체결요청

        Args:
            stk_cd (str): 종목코드
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticEtfHourlyExecution]: ETF 시간대별 체결 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka40007",
        }
        body = {"stk_cd": stk_cd}

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching ETF hourly execution: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticEtfHourlyExecution.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_etf_daily_execution(
        self, stk_cd: str, cont_yn: Literal["Y", "N"] = "N", next_key: str = ""
    ) -> KiwoomHttpResponse[DomesticEtfDailyExecution]:
        """ETF일자별체결요청

        Args:
            stk_cd (str): 종목코드
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticEtfDailyExecution]: ETF 일자별 체결 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka40008",
        }
        body = {"stk_cd": stk_cd}

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching ETF daily execution: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticEtfDailyExecution.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_etf_hourly_execution_v2(
        self, stk_cd: str, cont_yn: Literal["Y", "N"] = "N", next_key: str = ""
    ) -> KiwoomHttpResponse[DomesticEtfHourlyExecutionV2]:
        """ETF시간대별체결요청 (v2)

        Args:
            stk_cd (str): 종목코드
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticEtfHourlyExecutionV2]: ETF 시간대별 체결 데이터 (v2)
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka40009",
        }
        body = {"stk_cd": stk_cd}

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching ETF hourly execution v2: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticEtfHourlyExecutionV2.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_etf_hourly_trend_v2(
        self, stk_cd: str, cont_yn: Literal["Y", "N"] = "N", next_key: str = ""
    ) -> KiwoomHttpResponse[DomesticEtfHourlyTrendV2]:
        """ETF시간대별추이요청 (v2)

        Args:
            stk_cd (str): 종목코드
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticEtfHourlyTrendV2]: ETF 시간대별 추이 데이터 (v2)
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka40010",
        }
        body = {"stk_cd": stk_cd}

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching ETF hourly trend v2: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticEtfHourlyTrendV2.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)
