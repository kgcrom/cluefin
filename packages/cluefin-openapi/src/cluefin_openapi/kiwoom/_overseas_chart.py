from typing import Literal

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._model import (
    KiwoomHttpHeader,
    KiwoomHttpResponse,
)
from cluefin_openapi.kiwoom._overseas_chart_types import (
    OverseasChartDaily,
    OverseasChartMinute,
    OverseasChartMonthly,
    OverseasChartQuarterly,
    OverseasChartTick,
    OverseasChartWeekly,
    OverseasChartYearly,
)


class OverseasChart:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/api/us/chart"

    def get_tick_chart(
        self,
        stex_tp: Literal["NA", "ND", "NY"],
        stk_cd: str,
        tic_scope: str = "",
        upd_stkpc_tp: Literal["", "0", "1"] = "",
        exrt_appl_tp: Literal["", "0", "1"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasChartTick]:
        """미국주식 틱 차트 (usa06010)

        Args:
            stex_tp (Literal["NA", "ND", "NY"]): 거래소구분. NA:AMEX,ND:NASDAQ,NY:NYSE
            stk_cd (str): 종목코드
            tic_scope (str, optional): 틱범위. Defaults to "".
            upd_stkpc_tp (Literal["", "0", "1"], optional): 수정주가구분. 0:미적용,1:적용. Defaults to "".
            exrt_appl_tp (Literal["", "0", "1"], optional): 환율적용구분. 0:미적용,1:적용. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasChartTick]: 미국주식 틱 차트 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa06010",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
            "tic_scope": tic_scope,
            "upd_stkpc_tp": upd_stkpc_tp,
            "exrt_appl_tp": exrt_appl_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching tick chart: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasChartTick.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_minute_chart(
        self,
        stex_tp: Literal["NA", "ND", "NY"],
        stk_cd: str = "",
        strt_dt: str = "",
        tic_scope: str = "",
        upd_stkpc_tp: Literal["", "0", "1"] = "",
        exrt_appl_tp: Literal["", "0", "1"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasChartMinute]:
        """미국주식 분 차트 (usa06011)

        Args:
            stex_tp (Literal["NA", "ND", "NY"]): 거래소구분. NA:AMEX,ND:NASDAQ,NY:NYSE
            stk_cd (str, optional): 종목코드. Defaults to "".
            strt_dt (str, optional): 시작일자. YYYYMMDD. Defaults to "".
            tic_scope (str, optional): XX분봉. Defaults to "".
            upd_stkpc_tp (Literal["", "0", "1"], optional): 수정주가구분. 0:미적용,1:적용. Defaults to "".
            exrt_appl_tp (Literal["", "0", "1"], optional): 환율적용구분. 0:미적용,1:적용. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasChartMinute]: 미국주식 분 차트 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa06011",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
            "strt_dt": strt_dt,
            "tic_scope": tic_scope,
            "upd_stkpc_tp": upd_stkpc_tp,
            "exrt_appl_tp": exrt_appl_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching minute chart: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasChartMinute.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_daily_chart(
        self,
        stex_tp: Literal["NA", "ND", "NY"],
        stk_cd: str = "",
        strt_dt: str = "",
        upd_stkpc_tp: Literal["", "0", "1"] = "",
        exrt_appl_tp: Literal["", "0", "1"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasChartDaily]:
        """미국주식 일 차트 (usa06012)

        Args:
            stex_tp (Literal["NA", "ND", "NY"]): 거래소구분. NA:AMEX,ND:NASDAQ,NY:NYSE
            stk_cd (str, optional): 종목코드. Defaults to "".
            strt_dt (str, optional): 시작일자. YYYYMMDD. Defaults to "".
            upd_stkpc_tp (Literal["", "0", "1"], optional): 수정주가구분. 0:미적용,1:적용. Defaults to "".
            exrt_appl_tp (Literal["", "0", "1"], optional): 환율적용구분. 0:미적용,1:적용. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasChartDaily]: 미국주식 일 차트 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa06012",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
            "strt_dt": strt_dt,
            "upd_stkpc_tp": upd_stkpc_tp,
            "exrt_appl_tp": exrt_appl_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching daily chart: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasChartDaily.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_weekly_chart(
        self,
        stex_tp: Literal["NA", "ND", "NY"],
        stk_cd: str = "",
        strt_dt: str = "",
        upd_stkpc_tp: Literal["", "0", "1"] = "",
        exrt_appl_tp: Literal["", "0", "1"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasChartWeekly]:
        """미국주식 주 차트 (usa06013)

        Args:
            stex_tp (Literal["NA", "ND", "NY"]): 거래소구분. NA:AMEX,ND:NASDAQ,NY:NYSE
            stk_cd (str, optional): 종목코드. Defaults to "".
            strt_dt (str, optional): 시작일자. YYYYMMDD. Defaults to "".
            upd_stkpc_tp (Literal["", "0", "1"], optional): 수정주가구분. 0:미적용,1:적용. Defaults to "".
            exrt_appl_tp (Literal["", "0", "1"], optional): 환율적용구분. 0:미적용,1:적용. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasChartWeekly]: 미국주식 주 차트 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa06013",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
            "strt_dt": strt_dt,
            "upd_stkpc_tp": upd_stkpc_tp,
            "exrt_appl_tp": exrt_appl_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching weekly chart: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasChartWeekly.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_monthly_chart(
        self,
        stex_tp: Literal["NA", "ND", "NY"],
        stk_cd: str = "",
        strt_dt: str = "",
        upd_stkpc_tp: Literal["", "0", "1"] = "",
        exrt_appl_tp: Literal["", "0", "1"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasChartMonthly]:
        """미국주식 월 차트 (usa06014)

        Args:
            stex_tp (Literal["NA", "ND", "NY"]): 거래소구분. NA:AMEX,ND:NASDAQ,NY:NYSE
            stk_cd (str, optional): 종목코드. Defaults to "".
            strt_dt (str, optional): 시작일자. YYYYMMDD. Defaults to "".
            upd_stkpc_tp (Literal["", "0", "1"], optional): 수정주가구분. 0:미적용,1:적용. Defaults to "".
            exrt_appl_tp (Literal["", "0", "1"], optional): 환율적용구분. 0:미적용,1:적용. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasChartMonthly]: 미국주식 월 차트 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa06014",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
            "strt_dt": strt_dt,
            "upd_stkpc_tp": upd_stkpc_tp,
            "exrt_appl_tp": exrt_appl_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching monthly chart: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasChartMonthly.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_yearly_chart(
        self,
        stex_tp: Literal["NA", "ND", "NY"],
        stk_cd: str = "",
        strt_dt: str = "",
        upd_stkpc_tp: Literal["", "0", "1"] = "",
        exrt_appl_tp: Literal["", "0", "1"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasChartYearly]:
        """미국주식 년 차트 (usa06015)

        Args:
            stex_tp (Literal["NA", "ND", "NY"]): 거래소구분. NA:AMEX,ND:NASDAQ,NY:NYSE
            stk_cd (str, optional): 종목코드. Defaults to "".
            strt_dt (str, optional): 시작일자. YYYYMMDD. Defaults to "".
            upd_stkpc_tp (Literal["", "0", "1"], optional): 수정주가구분. 0:미적용,1:적용. Defaults to "".
            exrt_appl_tp (Literal["", "0", "1"], optional): 환율적용구분. 0:미적용,1:적용. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasChartYearly]: 미국주식 년 차트 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa06015",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
            "strt_dt": strt_dt,
            "upd_stkpc_tp": upd_stkpc_tp,
            "exrt_appl_tp": exrt_appl_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching yearly chart: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasChartYearly.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_quarterly_chart(
        self,
        stex_tp: Literal["NA", "ND", "NY"],
        stk_cd: str = "",
        strt_dt: str = "",
        upd_stkpc_tp: Literal["", "0", "1"] = "",
        exrt_appl_tp: Literal["", "0", "1"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasChartQuarterly]:
        """미국주식 분기 차트 (usa06016)

        Args:
            stex_tp (Literal["NA", "ND", "NY"]): 거래소구분. NA:AMEX,ND:NASDAQ,NY:NYSE
            stk_cd (str, optional): 종목코드. Defaults to "".
            strt_dt (str, optional): 시작일자. YYYYMMDD. Defaults to "".
            upd_stkpc_tp (Literal["", "0", "1"], optional): 수정주가구분. 0:미적용,1:적용. Defaults to "".
            exrt_appl_tp (Literal["", "0", "1"], optional): 환율적용구분. 0:미적용,1:적용. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasChartQuarterly]: 미국주식 분기 차트 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa06016",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
            "strt_dt": strt_dt,
            "upd_stkpc_tp": upd_stkpc_tp,
            "exrt_appl_tp": exrt_appl_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching quarterly chart: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasChartQuarterly.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)
