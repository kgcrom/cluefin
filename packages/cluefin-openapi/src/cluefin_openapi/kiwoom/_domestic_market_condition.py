from typing import Literal

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_market_condition_types import (
    DomesticMarketConditionAfterHoursSinglePrice,
    DomesticMarketConditionAfterMarketTradingByInvestor,
    DomesticMarketConditionDailyInstitutionalTrading,
    DomesticMarketConditionDailyStockPrice,
    DomesticMarketConditionExecutionIntensityTrendByDate,
    DomesticMarketConditionExecutionIntensityTrendByTime,
    DomesticMarketConditionInstitutionalTradingTrendByStock,
    DomesticMarketConditionIntradayTradingByInvestor,
    DomesticMarketConditionMarketSentimentInfo,
    DomesticMarketConditionNewStockWarrantPrice,
    DomesticMarketConditionProgramTradingArbitrageBalanceTrend,
    DomesticMarketConditionProgramTradingCumulativeTrend,
    DomesticMarketConditionProgramTradingTrendByDate,
    DomesticMarketConditionProgramTradingTrendByStockAndDate,
    DomesticMarketConditionProgramTradingTrendByStockAndTime,
    DomesticMarketConditionProgramTradingTrendByTime,
    DomesticMarketConditionSecuritiesFirmTradingTrendByStock,
    DomesticMarketConditionStockPrice,
    DomesticMarketConditionStockQuote,
    DomesticMarketConditionStockQuoteByDate,
)
from cluefin_openapi.kiwoom._model import (
    KiwoomHttpBody,
    KiwoomHttpHeader,
    KiwoomHttpResponse,
)


class DomesticMarketCondition:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/api/dostk/mrkcond"

    def get_stock_quote(
        self,
        stk_cd: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticMarketConditionStockQuote]:
        """
        주식호가요청

        Args:
            stk_cd (str): 종목코드 (거래소별 종목코드, 예: KRX:039490, NXT:039490_NX, SOR:039490_AL)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticMarketConditionStockQuote]: 주식호가요청 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10004",
        }
        body = {
            "stk_cd": stk_cd,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock quote: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticMarketConditionStockQuote.model_validate(response.json())

        return KiwoomHttpResponse[DomesticMarketConditionStockQuote](
            headers=headers,
            body=body,
        )

    def get_stock_quote_by_date(
        self,
        stk_cd: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticMarketConditionStockQuoteByDate]:
        """
        주식일자별호가요청

        Args:
            stk_cd (str): 종목코드 (거래소별 종목코드, 예: KRX:039490, NXT:039490_NX, SOR:039490_AL)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticMarketConditionStockQuoteByDate]: 주식일자별호가요청 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10005",
        }
        body = {
            "stk_cd": stk_cd,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching individual stock institutional chart by date: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticMarketConditionStockQuoteByDate.model_validate(response.json())
        return KiwoomHttpResponse[DomesticMarketConditionStockQuoteByDate](
            headers=headers,
            body=body,
        )

    def get_stock_price(
        self,
        stk_cd: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticMarketConditionStockPrice]:
        """
        주식시세요청

        Args:
            stk_cd (str): 종목코드 (거래소별 종목코드, 예: KRX:039490, NXT:039490_NX, SOR:039490_AL)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticMarketConditionStockPrice]: 주식시세 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10006",
        }
        body = {
            "stk_cd": stk_cd,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock price: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticMarketConditionStockPrice.model_validate(response.json())
        return KiwoomHttpResponse[DomesticMarketConditionStockPrice](
            headers=headers,
            body=body,
        )

    def get_market_sentiment_info(
        self,
        stk_cd: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticMarketConditionMarketSentimentInfo]:
        """
        시세표정보요청

        Args:
            stk_cd (str): 종목코드 (거래소별 종목코드, 예: KRX:039490, NXT:039490_NX, SOR:039490_AL)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticMarketConditionMarketSentimentInfo]: 시세표정보 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10007",
        }
        body = {
            "stk_cd": stk_cd,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching market sentiment info: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticMarketConditionMarketSentimentInfo.model_validate(response.json())
        return KiwoomHttpResponse[DomesticMarketConditionMarketSentimentInfo](
            headers=headers,
            body=body,
        )

    def get_new_stock_warrant_price(
        self,
        newstk_recvrht_tp: Literal["00", "05", "07"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticMarketConditionNewStockWarrantPrice]:
        """
        신주인수권증서시세요청

        Args:
            newstk_recvrht_tp (Literal["00", "05", "07"]): 신주인수권구분. Defaults to "00".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticMarketConditionNewStockWarrantPrice]: 신주인수권증서 시세 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10011",
        }
        body = {
            "newstk_recvrht_tp": newstk_recvrht_tp,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching new stock warrant price: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticMarketConditionNewStockWarrantPrice.model_validate(response.json())
        return KiwoomHttpResponse[DomesticMarketConditionNewStockWarrantPrice](
            headers=headers,
            body=body,
        )

    def get_daily_institutional_trading_items(
        self,
        strt_dt: str,
        end_dt: str,
        trde_tp: Literal["1", "2"],
        mrkt_tp: Literal["001", "101"],
        stex_tp: Literal["1", "2", "3"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticMarketConditionDailyInstitutionalTrading]:
        """
        일별기관별매매종목요청

        Args:
            strt_dt (str): 시작일자 (YYYYMMDD 형식)
            end_dt (str): 종료일자 (YYYYMMDD 형식)
            trde_tp (Literal["1", "2"]): 매매구분. Defaults to "1" (순매도).
            mrkt_tp (Literal["001", "101"]): 시장구분. Defaults to "001" (코스피).
            stex_tp (Literal["1", "2", "3"]): 거래소구분. Defaults to "1" (KRX).
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticMarketConditionDailyInstitutionalTrading]: 일별 기관별 매매 종목 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10044",
        }
        body = {
            "strt_dt": strt_dt,
            "end_dt": end_dt,
            "trde_tp": trde_tp,
            "mrkt_tp": mrkt_tp,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching daily institutional trading items: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticMarketConditionDailyInstitutionalTrading.model_validate(response.json())
        return KiwoomHttpResponse[DomesticMarketConditionDailyInstitutionalTrading](
            headers=headers,
            body=body,
        )

    def get_institutional_trading_trend_by_stock(
        self,
        stk_cd: str,
        strt_dt: str,
        end_dt: str,
        orgn_prsm_unp_tp: Literal["1", "2"],
        for_prsm_unp_tp: Literal["1", "2"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticMarketConditionInstitutionalTradingTrendByStock]:
        """
        종목별기관별매매추이요청

        Args:
            stk_cd (str): 종목코드 (거래소별 종목코드, 예: KRX:039490, NXT:039490_NX, SOR:039490_AL)
            strt_dt (str): 시작일자 (YYYYMMDD 형식)
            end_dt (str): 종료일자 (YYYYMMDD 형식)
            orgn_prsm_unp_tp (Literal["1", "2"]): 기관추정단가구분. Defaults to "1" (매수단가).
            for_prsm_unp_tp (Literal["1", "2"]): 외인추정단가구분. Defaults to "1" (매수단가).
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticMarketConditionInstitutionalTradingTrendByStock]: 종목별 기관별 매매 추이 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10045",
        }
        body = {
            "stk_cd": stk_cd,
            "strt_dt": strt_dt,
            "end_dt": end_dt,
            "orgn_prsm_unp_tp": orgn_prsm_unp_tp,
            "for_prsm_unp_tp": for_prsm_unp_tp,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching institutional trading trend by stock: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticMarketConditionInstitutionalTradingTrendByStock.model_validate(response.json())
        return KiwoomHttpResponse[DomesticMarketConditionInstitutionalTradingTrendByStock](
            headers=headers,
            body=body,
        )

    def get_execution_intensity_trend_by_time(
        self,
        stk_cd: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticMarketConditionExecutionIntensityTrendByTime]:
        """
        체결강도추이시간별요청

        Args:
            stk_cd (str): 종목코드 (거래소별 종목코드, 예: KRX:039490, NXT:039490_NX, SOR:039490_AL)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticMarketConditionExecutionIntensityTrendByTime]: 체결강도 추이 시간별 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10046",
        }
        body = {
            "stk_cd": stk_cd,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching execution intensity trend by time: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticMarketConditionExecutionIntensityTrendByTime.model_validate(response.json())
        return KiwoomHttpResponse[DomesticMarketConditionExecutionIntensityTrendByTime](
            headers=headers,
            body=body,
        )

    def get_execution_intensity_trend_by_date(
        self,
        stk_cd: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticMarketConditionExecutionIntensityTrendByDate]:
        """
        체결강도추이일별요청

        Args:
            stk_cd (str): 종목코드 (거래소별 종목코드, 예: KRX:039490, NXT:039490_NX, SOR:039490_AL)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticMarketConditionExecutionIntensityTrendByDate]: 체결강도 추이 일별 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10047",
        }
        body = {
            "stk_cd": stk_cd,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching execution intensity trend by date: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticMarketConditionExecutionIntensityTrendByDate.model_validate(response.json())
        return KiwoomHttpResponse[DomesticMarketConditionExecutionIntensityTrendByDate](
            headers=headers,
            body=body,
        )

    def get_intraday_trading_by_investor(
        self,
        mrkt_tp: Literal["000", "001", "101"],
        amt_qty_tp: Literal["1", "2"],
        invsr: Literal["6", "7", "1", "0", "2", "3", "4", "5"],
        frgn_all: Literal["1", "0"],
        smtm_netprps_tp: Literal["1", "0"],
        stex_tp: Literal["1", "2", "3"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticMarketConditionIntradayTradingByInvestor]:
        """
        장중투자자별매매요청

        Args:
            mrkt_tp (Literal["000", "001", "101"]): 시장구분
            amt_qty_tp (Literal["1", "2"]): 금액수량구분
            invsr (Literal["6", "7", "1", "0", "2", "3", "4", "5"]): 투자자별
            frgn_all (Literal["1", "0"]): 외국계전체
            smtm_netprps_tp (Literal["1", "0"]): 동시순매수구분
            stex_tp (Literal["1", "2", "3"]): 거래소구분
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticMarketConditionIntradayTradingByInvestor]: 장중 투자자별 매매 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10063",
        }
        body = {
            "mrkt_tp": mrkt_tp,
            "amt_qty_tp": amt_qty_tp,
            "invsr": invsr,
            "frgn_all": frgn_all,
            "smtm_netprps_tp": smtm_netprps_tp,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching intraday trading by investor: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticMarketConditionIntradayTradingByInvestor.model_validate(response.json())
        return KiwoomHttpResponse[DomesticMarketConditionIntradayTradingByInvestor](
            headers=headers,
            body=body,
        )

    def get_after_market_trading_by_investor(
        self,
        mrkt_tp: Literal["000", "001", "101"],
        amt_qty_tp: Literal["1", "2"],
        trde_tp: Literal["0", "1", "2"],
        stex_tp: Literal["1", "2", "3"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticMarketConditionAfterMarketTradingByInvestor]:
        """
        장마감후투자자별매매요청

        Args:
            mrkt_tp (Literal["000", "001", "101"]): 시장구분
            amt_qty_tp (Literal["1", "2"]): 금액수량구분
            trde_tp (Literal["0", "1", "2"]): 매매구분
            stex_tp (Literal["1", "2", "3"]): 거래소구분
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticMarketConditionAfterMarketTradingByInvestor]: 장마감 후 투자자별 매매 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10066",
        }
        body = {
            "mrkt_tp": mrkt_tp,
            "amt_qty_tp": amt_qty_tp,
            "trde_tp": trde_tp,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching after market trading by investor: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticMarketConditionAfterMarketTradingByInvestor.model_validate(response.json())
        return KiwoomHttpResponse[DomesticMarketConditionAfterMarketTradingByInvestor](
            headers=headers,
            body=body,
        )

    def get_securities_firm_trading_trend_by_stock(
        self,
        mmcm_cd: str,
        stk_cd: str,
        strt_dt: str,
        end_dt: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticMarketConditionSecuritiesFirmTradingTrendByStock]:
        """
        증권사별종목매매동향요청

        Args:
            mmcm_cd (str): 회원사코드 (3자리 코드)
            stk_cd (str): 종목코드 (거래소별 종목코드, 예: KRX:039490, NXT:039490_NX, SOR:039490_AL)
            strt_dt (str): 시작일자 (YYYYMMDD 형식)
            end_dt (str): 종료일자 (YYYYMMDD 형식)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticMarketConditionSecuritiesFirmTradingTrendByStock]: 증권사별 종목 매매 동향 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10078",
        }
        body = {
            "mmcm_cd": mmcm_cd,
            "stk_cd": stk_cd,
            "strt_dt": strt_dt,
            "end_dt": end_dt,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching securities firm trading trend by stock: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticMarketConditionSecuritiesFirmTradingTrendByStock.model_validate(response.json())
        return KiwoomHttpResponse[DomesticMarketConditionSecuritiesFirmTradingTrendByStock](
            headers=headers,
            body=body,
        )

    def get_daily_stock_price(
        self,
        stk_cd: str,
        qry_dt: str,
        indc_tp: Literal["0", "1"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticMarketConditionDailyStockPrice]:
        """
        일별주가요청

        Args:
            stk_cd (str): 종목코드 (거래소별 종목코드, 예: KRX:039490, NXT:039490_NX, SOR:039490_AL)
            qry_dt (str): 조회일자 (YYYYMMDD 형식)
            indc_tp (Literal["0", "1"]): 표시구분. Defaults to "0" (수량).
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticMarketConditionDailyStockPrice]: 일별 주가 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10086",
        }
        body = {
            "stk_cd": stk_cd,
            "qry_dt": qry_dt,
            "indc_tp": indc_tp,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching daily stock price: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticMarketConditionDailyStockPrice.model_validate(response.json())
        return KiwoomHttpResponse[DomesticMarketConditionDailyStockPrice](
            headers=headers,
            body=body,
        )

    def get_after_hours_single_price(
        self,
        stk_cd: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticMarketConditionAfterHoursSinglePrice]:
        """
        시간외단일가요청

        Args:
            stk_cd (str): 종목코드 (거래소별 종목코드, 예: KRX:039490, NXT:039490_NX, SOR:039490_AL)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticMarketConditionAfterHoursSinglePrice]: 시간외 단일가 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10087",
        }
        body = {
            "stk_cd": stk_cd,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching after hours single price: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticMarketConditionAfterHoursSinglePrice.model_validate(response.json())
        return KiwoomHttpResponse[DomesticMarketConditionAfterHoursSinglePrice](
            headers=headers,
            body=body,
        )

    def get_program_trading_trend_by_time(
        self,
        date: str,
        amt_qty_tp: Literal["1", "2"],
        mrkt_tp: Literal["P00101", "P001_NX01", "P001_AL01", "P10102", "P101_NX02", "P001_AL02"],
        min_tic_tp: Literal["0", "1"],
        stex_tp: Literal["1", "2", "3"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticMarketConditionProgramTradingTrendByTime]:
        """
        프로그램매매추이요청시간대별

        Args:
            date (str): 날짜 (YYYYMMDD 형식)
            amt_qty_tp (Literal["1", "2"]): 금액수량구분
            mrkt_tp (Literal["P00101", "P001_NX01", "P001_AL01", "P10102", "P101_NX02", "P001_AL02"]): 시장구분
            min_tic_tp (Literal["0", "1"]): 분틱구분
            stex_tp (Literal["1", "2", "3"]): 거래소구분
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticMarketConditionProgramTradingTrendByTime]: 프로그램 매매 추이 시간대별 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka90005",
        }
        body = {
            "date": date,
            "amt_qty_tp": amt_qty_tp,
            "mrkt_tp": mrkt_tp,
            "min_tic_tp": min_tic_tp,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching program trading trend by time: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticMarketConditionProgramTradingTrendByTime.model_validate(response.json())
        return KiwoomHttpResponse[DomesticMarketConditionProgramTradingTrendByTime](
            headers=headers,
            body=body,
        )

    def get_program_trading_arbitrage_balance_trend(
        self,
        date: str,
        stex_tp: Literal["1", "2", "3"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticMarketConditionProgramTradingArbitrageBalanceTrend]:
        """
        프로그램매매차익잔고추이 요청

        Args:
            date (str): 날짜 (YYYYMMDD 형식)
            stex_tp (Literal["1", "2", "3"]): 거래소구분
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticMarketConditionProgramTradingArbitrageBalanceTrend]: 프로그램 매매 차익 잔고 추이 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka90006",
        }
        body = {
            "date": date,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching program trading arbitrage balance trend: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticMarketConditionProgramTradingArbitrageBalanceTrend.model_validate(response.json())
        return KiwoomHttpResponse[DomesticMarketConditionProgramTradingArbitrageBalanceTrend](
            headers=headers,
            body=body,
        )

    def get_program_trading_cumulative_trend(
        self,
        date: str,
        amt_qty_tp: Literal["1", "2"],
        mrkt_tp: Literal["0", "1"],
        stex_tp: Literal["1", "2", "3"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticMarketConditionProgramTradingCumulativeTrend]:
        """
        프로그램매매누적추이요청

        Args:
            date (str): 날짜 (YYYYMMDD 형식)
            amt_qty_tp (Literal["1", "2"]): 금액수량구분
            mrkt_tp (Literal["0", "1"]): 시장구분
            stex_tp (Literal["1", "2", "3"]): 거래소구분
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticMarketConditionProgramTradingCumulativeTrend]: 프로그램 매매 누적 추이 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka90007",
        }
        body = {
            "date": date,
            "amt_qty_tp": amt_qty_tp,
            "mrkt_tp": mrkt_tp,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching program trading cumulative trend: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticMarketConditionProgramTradingCumulativeTrend.model_validate(response.json())
        return KiwoomHttpResponse[DomesticMarketConditionProgramTradingCumulativeTrend](
            headers=headers,
            body=body,
        )

    def get_program_trading_trend_by_stock_and_time(
        self,
        amt_qty_tp: Literal["1", "2"],
        stk_cd: str,
        date: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticMarketConditionProgramTradingTrendByStockAndTime]:
        """
        종목시간별프로그램매매추이요청

        Args:
            amt_qty_tp (Literal["1", "2"]): 금액수량구분
            stk_cd (str): 종목코드 (거래소별 종목코드, 예: KRX:039490, NXT:039490_NX, SOR:039490_AL)
            date (str): 날짜 (YYYYMMDD 형식)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticMarketConditionProgramTradingTrendByStockAndTime]: 종목 시간별 프로그램 매매 추이 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka90008",
        }
        body = {
            "amt_qty_tp": amt_qty_tp,
            "stk_cd": stk_cd,
            "date": date,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching program trading trend by stock and time: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticMarketConditionProgramTradingTrendByStockAndTime.model_validate(response.json())
        return KiwoomHttpResponse[DomesticMarketConditionProgramTradingTrendByStockAndTime](
            headers=headers,
            body=body,
        )

    def get_program_trading_trend_by_date(
        self,
        date: str,
        amt_qty_tp: Literal["1", "2"],
        mrkt_tp: Literal["P00101", "P001_NX01", "P001_AL01", "P10102", "P101_NX02", "P001_AL02"],
        min_tic_tp: Literal["0", "1"],
        stex_tp: Literal["1", "2", "3"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticMarketConditionProgramTradingTrendByDate]:
        """
        프로그램매매추이요청일자별

        Args:
            date (str): 날짜 (YYYYMMDD 형식)
            amt_qty_tp (Literal["1", "2"]): 금액수량구분
            mrkt_tp (Literal["P00101", "P001_NX01", "P001_AL01", "P10102", "P101_NX02", "P001_AL02"]): 시장구분
            min_tic_tp (Literal["0", "1"]): 분틱구분
            stex_tp (Literal["1", "2", "3"]): 거래소구분
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticMarketConditionProgramTradingTrendByDate]: 프로그램 매매 추이 일자별 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka90010",
        }
        body = {
            "date": date,
            "amt_qty_tp": amt_qty_tp,
            "mrkt_tp": mrkt_tp,
            "min_tic_tp": min_tic_tp,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching program trading trend by date: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticMarketConditionProgramTradingTrendByDate.model_validate(response.json())
        return KiwoomHttpResponse[DomesticMarketConditionProgramTradingTrendByDate](
            headers=headers,
            body=body,
        )

    def get_program_trading_trend_by_stock_and_date(
        self,
        amt_qty_tp: Literal["1", "2"],
        stk_cd: str,
        date: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticMarketConditionProgramTradingTrendByStockAndDate]:
        """
        종목일별프로그램매매추이요청

        Args:
            amt_qty_tp (Literal["1", "2"]): 금액수량구분
            stk_cd (str): 종목코드 (거래소별 종목코드, 예: KRX:039490, NXT:039490_NX, SOR:039490_AL)
            date (str): 날짜 (YYYYMMDD 형식)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticMarketConditionProgramTradingTrendByStockAndDate]: 종목 일별 프로그램 매매 추이 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka90013",
        }
        body = {
            "amt_qty_tp": amt_qty_tp,
            "stk_cd": stk_cd,
            "date": date,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching program trading trend by stock and date: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticMarketConditionProgramTradingTrendByStockAndDate.model_validate(response.json())
        return KiwoomHttpResponse[DomesticMarketConditionProgramTradingTrendByStockAndDate](
            headers=headers,
            body=body,
        )
