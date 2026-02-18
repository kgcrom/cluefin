from typing_extensions import Literal

from cluefin_openapi.kis._domestic_basic_quote_types import (
    DomesticEtfComponentStockPrice,
    DomesticEtfEtnCurrentPrice,
    DomesticEtfNavComparisonDailyTrend,
    DomesticEtfNavComparisonTimeTrend,
    DomesticEtfNavComparisonTrend,
    DomesticStockClosingExpectedPrice,
    DomesticStockCurrentPrice,
    DomesticStockCurrentPrice2,
    DomesticStockCurrentPriceAskingExpectedConclusion,
    DomesticStockCurrentPriceConclusion,
    DomesticStockCurrentPriceDaily,
    DomesticStockCurrentPriceDailyOvertimePrice,
    DomesticStockCurrentPriceInvestor,
    DomesticStockCurrentPriceMember,
    DomesticStockCurrentPriceOvertimeConclusion,
    DomesticStockCurrentPriceTimeItemConclusion,
    DomesticStockOvertimeAskingPrice,
    DomesticStockOvertimeCurrentPrice,
    DomesticStockPeriodQuote,
    DomesticStockTodayMinuteChart,
)
from cluefin_openapi.kis._http_client import HttpClient
from cluefin_openapi.kis._model import KisHttpHeader, KisHttpResponse


class DomesticBasicQuote:
    """국내주식 기본시세"""

    def __init__(self, client: HttpClient):
        self.client = client

    def _check_response_error(self, response_data: dict) -> None:
        """Check if API response contains an error and raise if so."""
        rt_cd = response_data.get("rt_cd")
        if rt_cd != "0":
            msg_cd = response_data.get("msg_cd", "")
            msg1 = response_data.get("msg1", "Unknown error")
            raise ValueError(f"KIS API Error [{msg_cd}]: {msg1} (rt_cd={rt_cd})")

    def get_stock_current_price(
        self,
        fid_cond_mrkt_div_code: Literal["J", "NX", "UN"],
        fid_input_iscd: str,
    ) -> KisHttpResponse[DomesticStockCurrentPrice]:
        """
        주식현재가 시세

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J:KRX, NX:NXT, UN:통합
            fid_input_iscd (str): 입력 종목코드

        Returns:
            KisHttpResponse[DomesticStockCurrentPrice]: 주식현재가 시세
        """
        headers = {
            "tr_id": "FHKST01010100",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
        }
        response = self.client._get("/uapi/domestic-stock/v1/quotations/inquire-price", headers=headers, params=params)
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = DomesticStockCurrentPrice.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_stock_current_price_2(
        self, fid_cond_mrkt_div_code: Literal["J", "NX", "UN"], fid_input_iscd: str
    ) -> KisHttpResponse[DomesticStockCurrentPrice2]:
        """
        주식현재가 시세2

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J:KRX, NX:NXT, UN:통합
            fid_input_iscd (str): 입력 종목코드

        Returns:
            KisHttpResponse[DomesticStockCurrentPrice2]: 주식현재가 시세2
        """
        headers = {
            "tr_id": "FHPST01010000",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-price-2", headers=headers, params=params
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = DomesticStockCurrentPrice2.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_stock_current_price_conclusion(
        self, fid_cond_mrkt_div_code: Literal["J", "NX", "UN"], fid_input_iscd: str
    ) -> KisHttpResponse[DomesticStockCurrentPriceConclusion]:
        """
        주식현재가 체결

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J:KRX, NX:NXT, UN:통합
            fid_input_iscd (str): 입력 종목코드

        Returns:
            KisHttpResponse[DomesticStockCurrentPriceConclusion]: 주식현재가 체결
        """
        headers = {
            "tr_id": "FHKST01010300",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
        }
        response = self.client._get("/uapi/domestic-stock/v1/quotations/inquire-ccnl", headers=headers, params=params)
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = DomesticStockCurrentPriceConclusion.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_stock_current_price_daily(
        self,
        fid_cond_mrkt_div_code: Literal["J", "NX", "UN"],
        fid_input_iscd: str,
        fid_period_div_code: Literal["D", "W", "M"],
        fid_org_adj_prc: Literal["0", "1"],
    ) -> KisHttpResponse[DomesticStockCurrentPriceDaily]:
        """
        주식현재가 일자별

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J:KRX, NX:NXT, UN:통합
            fid_input_iscd (str): 입력 종목코드
            fid_period_div_code (str): 기간 분류 코드, D:일, W:주, M:월
            fid_org_adj_prc (str): 수정주가 원주가 가격, 0:수정주가미반영, 1:수정주가반영

        Returns:
            KisHttpResponse[DomesticStockCurrentPriceDaily]: 주식현재가 일자별
        """
        headers = {
            "tr_id": "FHKST01010400",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_PERIOD_DIV_CODE": fid_period_div_code,
            "FID_ORG_ADJ_PRC": fid_org_adj_prc,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-daily-price", headers=headers, params=params
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = DomesticStockCurrentPriceDaily.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_stock_current_price_asking_expected_conclusion(
        self, fid_cond_mrkt_div_code: Literal["J", "NX", "UN"], fid_input_iscd: str
    ) -> KisHttpResponse[DomesticStockCurrentPriceAskingExpectedConclusion]:
        """
        주식현재가 호가/예상체결

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J:KRX, NX:NXT, UN:통합
            fid_input_iscd (str): 입력 종목코드

        Returns:
            KisHttpResponse[DomesticStockCurrentPriceAskingExpectedConclusion]: 주식현재가 호가/예상
        """
        headers = {
            "tr_id": "FHKST01010200",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-asking-price-exp-ccn", headers=headers, params=params
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = DomesticStockCurrentPriceAskingExpectedConclusion.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_stock_current_price_investor(
        self, fid_cond_mrkt_div_code: Literal["J", "NX", "UN"], fid_input_iscd: str
    ) -> KisHttpResponse[DomesticStockCurrentPriceInvestor]:
        """
        주식현재가 투자자

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J:KRX, NX:NXT, UN:통합
            fid_input_iscd (str): 입력 종목코드

        Returns:
            KisHttpResponse[DomesticStockCurrentPriceInvestor]: 주식현재가 투자자
        """
        headers = {
            "tr_id": "FHKST01010900",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-investor", headers=headers, params=params
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = DomesticStockCurrentPriceInvestor.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_stock_current_price_member(
        self, fid_cond_mrkt_div_code: Literal["J", "NX", "UN"], fid_input_iscd: str
    ) -> KisHttpResponse[DomesticStockCurrentPriceMember]:
        """주식현재가 회원사"""
        headers = {
            "tr_id": "FHKST01010600",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
        }
        response = self.client._get("/uapi/domestic-stock/v1/quotations/inquire-member", headers=headers, params=params)
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = DomesticStockCurrentPriceMember.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_stock_period_quote(
        self,
        fid_cond_mrkt_div_code: Literal["J", "NX", "UN"],
        fid_input_iscd: str,
        fid_input_date_1: str,
        fid_input_date_2: str,
        fid_period_div_code: Literal["D", "W", "M", "Y"],
        fid_org_adj_prc: Literal["0", "1"],
    ) -> KisHttpResponse[DomesticStockPeriodQuote]:
        """
        국내주식기간별시세(일/주/월/년)

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J:KRX, NX:NXT, UN:통합
            fid_input_iscd (str): 입력 종목코드
            fid_input_date_1 (str): 입력 날짜 1, 조회 시작일자 (YYYYMMDD)
            fid_input_date_2 (str): 입력 날짜 2, 조회 종료일자 (YYYYMMDD)
            fid_period_div_code (str): 기간 분류 코드, D:일봉, W:주봉, M:월봉, Y:년봉
            fid_org_adj_prc (str): 수정 주가 원주가 가격 여부, 0:수정주가, 1:원주가

        Returns:
            KisHttpResponse[DomesticStockPeriodQuote]: 국내주식기간별시세(일/주/월/년)
        """
        headers = {
            "tr_id": "FHKST03010100",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_INPUT_DATE_1": fid_input_date_1,
            "FID_INPUT_DATE_2": fid_input_date_2,
            "FID_PERIOD_DIV_CODE": fid_period_div_code,
            "FID_ORG_ADJ_PRC": fid_org_adj_prc,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice", headers=headers, params=params
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = DomesticStockPeriodQuote.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_stock_today_minute_chart(
        self,
        fid_cond_mrkt_div_code: Literal["J", "NX", "UN"],
        fid_input_iscd: str,
        fid_input_hour_1: str,
        fid_pw_data_incu_yn: Literal["N", "Y"],
        fid_etc_cls_code: str,
    ) -> KisHttpResponse[DomesticStockTodayMinuteChart]:
        """
        주식당일분봉조회

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J:KRX, NX:NXT, UN:통합
            fid_input_iscd (str): 입력 종목코드
            fid_input_hour_1 (str): 입력 시간 1, 조회 시작시간 (HHMMSS)
            fid_pw_data_incu_yn (str): 체결량 포함 여부, N:체결량미포함, Y:체결량포함
            fid_etc_cls_code (str): 기타 분류 코드

        Returns:
            KisHttpResponse[DomesticStockTodayMinuteChart]: 주식당일분봉조회
        """
        headers = {
            "tr_id": "FHKST03010200",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_INPUT_HOUR_1": fid_input_hour_1,
            "FID_PW_DATA_INCU_YN": fid_pw_data_incu_yn,
            "FID_ETC_CLS_CODE": fid_etc_cls_code,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice", headers=headers, params=params
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = DomesticStockTodayMinuteChart.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_stock_daily_minute_chart(
        self,
        fid_cond_mrkt_div_code: Literal["J", "NX", "UN"],
        fid_input_iscd: str,
        fid_input_hour_1: str,
        fid_input_date_1: str,
        fid_pw_data_incu_yn: Literal["N", "Y"],
        fid_fake_tick_incu_yn: Literal["", "N", "Y"] = "",
    ) -> KisHttpResponse[DomesticStockTodayMinuteChart]:
        """
        주식일별분봉조회

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J:KRX, NX:NXT, UN:통합
            fid_input_iscd (str): 입력 종목코드
            fid_input_hour_1 (str): 입력 시간 1, 조회 시작시간 (HHMMSS)
            fid_input_date_1 (str): 입력 날짜 1, 조회 시작일자 (YYYYMMDD)
            fid_pw_data_incu_yn (str): 과거 데이터 포함 여부, N:과거데이터미포함, Y:과거데이터포함
            fid_fake_tick_incu_yn (str): 허봉 포함 여부, N:허봉미포함, Y:허봉포함, 공백 필수 입력

        Returns:
            KisHttpResponse[DomesticStockTodayMinuteChart]: 주식일별분봉조회
        """
        headers = {
            "tr_id": "FHKST03010230",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_INPUT_HOUR_1": fid_input_hour_1,
            "FID_INPUT_DATE_1": fid_input_date_1,
            "FID_PW_DATA_INCU_YN": fid_pw_data_incu_yn,
            "FID_FAKE_TICK_INCU_YN": fid_fake_tick_incu_yn,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-time-dailychartprice", headers=headers, params=params
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = DomesticStockTodayMinuteChart.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_stock_current_price_time_item_conclusion(
        self,
        fid_cond_mrkt_div_code: Literal["J", "NX", "UN"],
        fid_input_iscd: str,
        fid_input_hour_1: str,
    ) -> KisHttpResponse[DomesticStockCurrentPriceTimeItemConclusion]:
        """
        주식현재가 당일시간대별체결

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J:KRX, NX:NXT, UN:통합
            fid_input_iscd (str): 입력 종목코드
            fid_input_hour_1 (str): 입력 시간 1, 조회 시작시간 (HHMMSS)

        Returns:
            KisHttpResponse[DomesticStockCurrentPriceTimeItemConclusion]: 주식현재가 당일시간대별체결
        """
        headers = {
            "tr_id": "FHPST01060000",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_INPUT_HOUR_1": fid_input_hour_1,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-time-itemconclusion", headers=headers, params=params
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = DomesticStockCurrentPriceTimeItemConclusion.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_stock_current_price_daily_overtime_price(
        self,
        fid_cond_mrkt_div_code: Literal["J", "NX", "UN"],
        fid_input_iscd: str,
    ) -> KisHttpResponse[DomesticStockCurrentPriceDailyOvertimePrice]:
        """
        주식현재가 시간외일자별주가

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J:KRX, NX:NXT, UN:통합
            fid_input_iscd (str): 입력 종목코드

        Returns:
            KisHttpResponse[DomesticStockCurrentPriceDailyOvertimePrice]: 주식현재가 시간외일자별주가
        """
        headers = {
            "tr_id": "FHPST02320000",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-daily-overtimeprice", headers=headers, params=params
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = DomesticStockCurrentPriceDailyOvertimePrice.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_stock_current_price_overtime_conclusion(
        self, fid_cond_mrkt_div_code: Literal["J", "NX", "UN"], fid_input_iscd: str
    ) -> KisHttpResponse[DomesticStockCurrentPriceOvertimeConclusion]:
        """
        주식현재가 시간외시간별체결

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J:KRX, NX:NXT, UN:통합
            fid_input_iscd (str): 입력 종목코드

        Returns:
            KisHttpResponse[DomesticStockCurrentPriceOvertimeConclusion]: 주식현재가 시간외시간별체결
        """
        headers = {
            "tr_id": "FHPST02310000",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_HOUR_CLS_CODE": "1",
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-time-overtimeconclusion", headers=headers, params=params
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = DomesticStockCurrentPriceOvertimeConclusion.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_stock_overtime_current_price(
        self, fid_cond_mrkt_div_code: Literal["J", "NX", "UN"], fid_input_iscd: str
    ) -> KisHttpResponse[DomesticStockOvertimeCurrentPrice]:
        """
        국내주식 시간외현재가
        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J:KRX, NX:NXT, UN:통합
            fid_input_iscd (str): 입력 종목코드

        Returns:
            KisHttpResponse[DomesticStockOvertimeCurrentPrice]: 국내주식 시간외현재가
        """
        heders = {
            "tr_id": "FHPST02300000",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-overtime-price", headers=heders, params=params
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = DomesticStockOvertimeCurrentPrice.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_stock_overtime_asking_price(
        self, fid_input_iscd: str, fid_cond_mrkt_div_code: Literal["J"] = "J"
    ) -> KisHttpResponse[DomesticStockOvertimeAskingPrice]:
        """
        국내주식 시간외호가

        Args:
            fid_input_iscd (str): 입력 종목코드
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J: 주식

        Returns:
            KisHttpResponse[DomesticStockOvertimeAskingPrice]: 국내주식 시간외호가
        """
        headers = {
            "tr_id": "FHPST02300400",
        }
        params = {
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-overtime-asking-price", headers=headers, params=params
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = DomesticStockOvertimeAskingPrice.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_stock_closing_expected_price(
        self,
        fid_rank_sort_cls_code: Literal["0", "1", "2", "3", "4"],
        fid_input_iscd: Literal["0000", "0001", "1001", "2001", "4001"],
        fid_blng_cls_code: Literal["0", "1"],
        fid_cond_mrkt_div_code: Literal["J"] = "J",
        fid_cond_scr_div_code: Literal["11173"] = "11173",
    ) -> KisHttpResponse[DomesticStockClosingExpectedPrice]:
        """
        국내주식 장마감 예상체결가

        Args:
            fid_rank_sort_cls_code (str): 순위 정렬 구분 코드, 0:전체, 1:상한가마감예상, 2:하한가마감예상, 3:직전대비상승률상위 ,4:직전대비하락률상위
            fid_input_iscd (str): 입력 종목코드, 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100
            fid_blng_cls_code (str): 소속 구분 코드, 0:전체, 1:종가범위연장
            fid_cond_mrkt_div (str): 조건 시장 분류 코드, J: 주식
            fid_cond_scr_div_code (str): 조건 화면 분류 코드, 11173:Unique key(11173)

        Returns:
            KisHttpResponse[DomesticStockClosingExpectedPrice]: 국내주식 장마감 예상체결가
        """
        headers = {
            "tr_id": "FHKST117300C0",
        }
        params = {
            "FID_RANK_SORT_CLS_CODE": fid_rank_sort_cls_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_BLNG_CLS_CODE": fid_blng_cls_code,
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_COND_SCR_DIV_CODE": fid_cond_scr_div_code,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/exp-closing-price", headers=headers, params=params
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = DomesticStockClosingExpectedPrice.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_etfetn_current_price(
        self, fid_input_iscd: str, fid_cond_mrkt_div_code: Literal["J"] = "J"
    ) -> KisHttpResponse[DomesticEtfEtnCurrentPrice]:
        """
        ETF/ETN 현재가

        Args:
            fid_input_iscd (str): 입력 종목코드
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J: 주식

        Returns:
            KisHttpResponse[DomesticEtfEtnCurrentPrice]: ETF/ETN 현재가
        """
        headers = {
            "tr_id": "FHPST02400000",
        }
        params = {
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
        }
        response = self.client._get("/uapi/etfetn/v1/quotations/inquire-price", headers=headers, params=params)
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = DomesticEtfEtnCurrentPrice.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_etf_component_stock_price(
        self, fid_input_iscd: str, fid_cond_mrkt_div_code: Literal["J"] = "J", fid_cond_scr_div_code: str = "11216"
    ) -> KisHttpResponse[DomesticEtfComponentStockPrice]:
        """
        ETF 구성종목시세

        Args:
            fid_input_iscd (str): 입력 종목코드
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J: 주식
            fid_cond_scr_div_code (str): 조건 화면 분류 코드, 11216:Unique key(11216)

        Returns:
            KisHttpResponse[DomesticEtfComponentStockPrice]: ETF 구성종목시세
        """
        headers = {
            "tr_id": "FHKST121600C0",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_COND_SCR_DIV_CODE": fid_cond_scr_div_code,
            # KIS has been observed to intermittently require `_1`-suffixed field names for this endpoint.
            # Sending both variants keeps the request compatible across backend versions.
            "FID_COND_MRKT_DIV_CODE_1": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD_1": fid_input_iscd,
            "FID_COND_SCR_DIV_CODE_1": fid_cond_scr_div_code,
        }
        response = self.client._get(
            "/uapi/etfetn/v1/quotations/inquire-component-stock-price", headers=headers, params=params
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = DomesticEtfComponentStockPrice.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_etf_nav_comparison_trend(
        self, fid_input_iscd: str, fid_cond_mrkt_div_code: Literal["J"] = "J"
    ) -> KisHttpResponse[DomesticEtfNavComparisonTrend]:
        """
        NAV 비교추이(종목)

        Args:
            fid_input_iscd (str): 입력 종목코드
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J: 주식

        Returns:
            KisHttpResponse[DomesticEtfNavComparisonTrend]: NAV 비교추이(종목)
        """
        headers = {
            "tr_id": "FHPST02440000",
        }
        params = {
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
        }
        response = self.client._get("/uapi/etfetn/v1/quotations/nav-comparison-trend", headers=headers, params=params)
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = DomesticEtfNavComparisonTrend.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_etf_nav_comparison_daily_trend(
        self,
        fid_input_iscd: str,
        fid_input_date_1: str,
        fid_input_date_2: str,
        fid_cond_mrkt_div_code: Literal["J"] = "J",
    ) -> KisHttpResponse[DomesticEtfNavComparisonDailyTrend]:
        """
        NAV 비교추이(일)

        Args:
            fid_input_iscd (str): 입력 종목코드
            fid_input_date_1 (str): 입력 날짜1, 조회 시작일자 (ex. 20240101)
            fid_input_date_2 (str): 입력 날짜2, 조회 종료일자 (ex. 20240220)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J: 주식

        Returns:
            KisHttpResponse[DomesticEtfNavComparisonDailyTrend]: NAV 비교추이(일)
        """
        headers = {
            "tr_id": "FHPST02440200",
        }
        params = {
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
            "fid_input_iscd": fid_input_iscd,
            "fid_input_date_1": fid_input_date_1,
            "fid_input_date_2": fid_input_date_2,
        }
        response = self.client._get(
            "/uapi/etfetn/v1/quotations/nav-comparison-daily-trend", headers=headers, params=params
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = DomesticEtfNavComparisonDailyTrend.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_etf_nav_comparison_time_trend(
        self,
        fid_hour_cls_code: str,
        fid_input_iscd: str,
        fid_cond_mrkt_div_code: Literal["E"] = "E",
    ) -> KisHttpResponse[DomesticEtfNavComparisonTimeTrend]:
        """
        NAV 비교추이(분)

        Args:
            fid_hour_cls_code (str): FID 시간 구분 코드, 1분 :60, 3분: 180 … 120분:7200
            fid_input_iscd (str): 입력 종목코드
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J: 주식

        Returns:
            KisHttpResponse[DomesticEtfNavComparisonTimeTrend]: NAV 비교추이(분)
        """
        headers = {
            "tr_id": "FHPST02440100",
        }
        params = {
            "fid_hour_cls_code": fid_hour_cls_code,
            "fid_input_iscd": fid_input_iscd,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
        }
        response = self.client._get(
            "/uapi/etfetn/v1/quotations/nav-comparison-time-trend", headers=headers, params=params
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = DomesticEtfNavComparisonTimeTrend.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)
