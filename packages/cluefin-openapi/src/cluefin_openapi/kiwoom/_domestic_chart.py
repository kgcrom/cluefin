from typing import Literal

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_chart_types import (
    DomesticChartIndividualStockInstitutional,
    DomesticChartIndustryDaily,
    DomesticChartIndustryMinute,
    DomesticChartIndustryMonthly,
    DomesticChartIndustryTick,
    DomesticChartIndustryWeekly,
    DomesticChartIndustryYearly,
    DomesticChartIntradayInvestorTrading,
    DomesticChartStockDaily,
    DomesticChartStockMinute,
    DomesticChartStockMonthly,
    DomesticChartStockTick,
    DomesticChartStockWeekly,
    DomesticChartStockYearly,
)
from cluefin_openapi.kiwoom._model import (
    KiwoomHttpHeader,
    KiwoomHttpResponse,
)


class DomesticChart:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/api/dostk/chart"

    def get_individual_stock_institutional_chart(
        self,
        dt: str,
        stk_cd: str,
        amt_qty_tp: str,
        trde_tp: str,
        unit_tp: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticChartIndividualStockInstitutional]:
        """종목별투자자기관별차트요청

        Args:
            dt (str): 일자 (YYYYMMDD)
            stk_cd (str): 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            amt_qty_tp (str): 금액수량구분 (1:금액, 2:수량)
            trde_tp (str): 매매구분 (0:순매수, 1:매수, 2:매도)
            unit_tp (str): 단위구분 (1000:천주, 1:단주)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticChartIndividualStockInstitutional]: 종목별 투자자 기관별 차트 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10060",
        }
        body = {
            "dt": dt,
            "stk_cd": stk_cd,
            "amt_qty_tp": amt_qty_tp,
            "trde_tp": trde_tp,
            "unit_tp": unit_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching individual stock institutional chart: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticChartIndividualStockInstitutional.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_intraday_investor_trading(
        self,
        mrkt_tp: Literal["000", "001", "101"],
        amt_qty_tp: Literal["1", "2"],
        trde_tp: Literal["0", "1", "2"],
        stk_cd: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticChartIntradayInvestorTrading]:
        """장중투자자별매매차트요청

        Args:
            mrkt_tp (Literal["000", "001", "101"]): 시장구분 (000:전체, 001:코스피, 101:코스닥)
            amt_qty_tp (Literal["1", "2"]): 금액수량구분 (1:금액, 2:수량)
            trde_tp (Literal["0", "1", "2"]): 매매구분 (0:순매수, 1:매수, 2:매도)
            stk_cd (str): 거래소별 종목코드
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticChartIntradayInvestorTrading]: 장중 투자자별 매매 차트 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10064",
        }
        body = {
            "stk_cd": stk_cd,
            "amt_qty_tp": amt_qty_tp,
            "trde_tp": trde_tp,
            "mrkt_tp": mrkt_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching intraday investor trading chart: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticChartIntradayInvestorTrading.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_stock_tick(
        self,
        stk_cd: str,
        tic_scope: str,
        upd_stkpc_tp: str = "0",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticChartStockTick]:
        """주식틱차트조회요청

        Args:
            stk_cd (str): 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            tic_scope (str): 틱범위 (1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱)
            upd_stkpc_tp (str, optional): 수정주가구분. Defaults to "0".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticChartStockTick]: 주식 틱 차트 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10079",
        }
        body = {
            "stk_cd": stk_cd,
            "tic_scope": tic_scope,
            "upd_stkpc_tp": upd_stkpc_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock tick chart: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticChartStockTick.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_stock_minute(
        self,
        stk_cd: str,
        tic_scope: str,
        upd_stkpc_tp: str = "0",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticChartStockMinute]:
        """주식분봉차트조회요청

        Args:
            stk_cd (str): 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            tic_scope (str): 틱범위 (1:1분, 3:3분, 5:5분, 10:10분, 15:15분, 30:30분, 45:45분, 60:60분)
            upd_stkpc_tp (str, optional): 수정주가구분. Defaults to "0".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticChartStockMinute]: 주식 분봉 차트 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10080",
        }
        body = {
            "stk_cd": stk_cd,
            "tic_scope": tic_scope,
            "upd_stkpc_tp": upd_stkpc_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock minute chart: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticChartStockMinute.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_stock_daily(
        self,
        stk_cd: str,
        base_dt: str,
        upd_stkpc_tp: Literal["0", "1"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticChartStockDaily]:
        """주식일봉차트조회요청

        Args:
            stk_cd (str): 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            base_dt (str): 기준일자 (YYYYMMDD)
            upd_stkpc_tp (Literal["0", "1"]): 수정주가구분 (0:수정주가적용안함, 1:수정주가)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticChartStockDaily]: 주식 일봉 차트 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10081",
        }
        body = {
            "stk_cd": stk_cd,
            "base_dt": base_dt,
            "upd_stkpc_tp": upd_stkpc_tp,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock daily chart: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticChartStockDaily.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_stock_weekly(
        self,
        stk_cd: str,
        base_dt: str,
        upd_stkpc_tp: Literal["0", "1"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticChartStockWeekly]:
        """주식주봉차트조회요청

        Args:
            stk_cd (str): 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            base_dt (str): 기준일자 (YYYYMMDD)
            upd_stkpc_tp (Literal["0", "1"]): 수정주가구분 (0:수정주가적용안함, 1:수정주가)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticChartStockWeekly]: 주식 주봉 차트 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10082",
        }
        body = {
            "stk_cd": stk_cd,
            "base_dt": base_dt,
            "upd_stkpc_tp": upd_stkpc_tp,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock weekly chart: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticChartStockWeekly.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_stock_monthly(
        self,
        stk_cd: str,
        base_dt: str,
        upd_stkpc_tp: Literal["0", "1"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticChartStockMonthly]:
        """주식월봉차트조회요청

        Args:
            stk_cd (str): 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            base_dt (str): 기준일자 (YYYYMMDD)
            upd_stkpc_tp (Literal["0", "1"]): 수정주가구분 (0:수정주가적용안함, 1:수정주가)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticChartStockMonthly]: 주식 월봉 차트 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10083",
        }
        body = {
            "stk_cd": stk_cd,
            "base_dt": base_dt,
            "upd_stkpc_tp": upd_stkpc_tp,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock monthly chart: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticChartStockMonthly.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_stock_yearly(
        self,
        stk_cd: str,
        base_dt: str,
        upd_stkpc_tp: Literal["0", "1"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticChartStockYearly]:
        """주식년봉차트조회요청

        Args:
            stk_cd (str): 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            base_dt (str): 기준일자 (YYYYMMDD)
            upd_stkpc_tp (Literal["0", "1"]): 수정주가구분 (0:수정주가적용안함, 1:수정주가)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticChartStockYearly]: 주식 년봉 차트 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10094",
        }
        body = {
            "stk_cd": stk_cd,
            "base_dt": base_dt,
            "upd_stkpc_tp": upd_stkpc_tp,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock yearly chart: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticChartStockYearly.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_industry_tick(
        self,
        inds_cd: str,
        tic_scope: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticChartIndustryTick]:
        """업종틱차트조회요청
        Args:
            inds_cd (str): 업종코드 (001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주, 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100)
            tic_scope (str): 틱범위 (1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticChartIndustryTick]: 업종 틱 차트 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka20004",
        }
        body = {
            "inds_cd": inds_cd,
            "tic_scope": tic_scope,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching industry tick chart: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticChartIndustryTick.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_industry_minute(
        self,
        inds_cd: str,
        tic_scope: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticChartIndustryMinute]:
        """업종분봉차트조회요청

        Args:
            inds_cd (str): 업종코드 (001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주, 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100)
            tic_scope (str): 틱범위 (1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticChartIndustryMinute]: 업종 분봉 차트 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka20005",
        }
        body = {
            "inds_cd": inds_cd,
            "tic_scope": tic_scope,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching industry minute chart: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticChartIndustryMinute.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_industry_daily(
        self,
        inds_cd: str,
        base_dt: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticChartIndustryDaily]:
        """업종일봉차트조회요청

        Args:
            inds_cd (str): 업종코드 (001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주, 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100)
            base_dt (str): 기준일자 (YYYYMMDD)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticChartIndustryDaily]: 업종 일봉 차트 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka20006",
        }
        body = {
            "inds_cd": inds_cd,
            "base_dt": base_dt,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching industry daily chart: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticChartIndustryDaily.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_industry_weekly(
        self,
        inds_cd: str,
        base_dt: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticChartIndustryWeekly]:
        """업종주봉차트조회요청

        Args:
            inds_cd (str): 업종코드 (001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주, 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100)
            base_dt (str): 기준일자 (YYYYMMDD)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticChartIndustryWeekly]: 업종 주봉 차트 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka20007",
        }
        body = {
            "inds_cd": inds_cd,
            "base_dt": base_dt,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching industry weekly chart: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticChartIndustryWeekly.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_industry_monthly(
        self,
        inds_cd: str,
        base_dt: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticChartIndustryMonthly]:
        """업종월봉차트조회요청

        Args:
            inds_cd (str): 업종코드 (001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주, 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100)
            base_dt (str): 기준일자 (YYYYMMDD)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticChartIndustryMonthly]: 업종 월봉 차트 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka20008",
        }
        body = {
            "inds_cd": inds_cd,
            "base_dt": base_dt,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching industry monthly chart: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticChartIndustryMonthly.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_industry_yearly(
        self,
        inds_cd: str,
        base_dt: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticChartIndustryYearly]:
        """업종년봉차트조회요청

        Args:
            inds_cd (str): 업종코드 (001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주, 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100)
            base_dt (str): 기준일자 (YYYYMMDD)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticChartIndustryYearly]: 업종 년봉 차트 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka20019",
        }
        body = {
            "inds_cd": inds_cd,
            "base_dt": base_dt,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching industry yearly chart: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticChartIndustryYearly.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)
