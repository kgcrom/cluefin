from typing_extensions import Literal

from cluefin_openapi.kis._client import Client
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
    DomesticStockCurrentPriceDaily,
    DomesticStockCurrentPriceDailyOvertimePrice,
    DomesticStockCurrentPriceDetail,
    DomesticStockCurrentPriceInvestor,
    DomesticStockCurrentPriceMember,
    DomesticStockCurrentPriceOvertimeConclusion,
    DomesticStockCurrentPriceTimeItemConclusion,
    DomesticStockOvertimeAskingPrice,
    DomesticStockOvertimeCurrentPrice,
    DomesticStockPeriodQuote,
    DomesticStockTodayMinuteChart,
)


class DomesticBasicQuote:
    """국내주식 기본시세"""

    def __init__(self, client: Client):
        self.client = client

    def get_stock_current_price(
        self,
        fid_cond_mrkt_div_code: Literal["J", "NX", "UN"],
        fid_input_iscd: str,
    ) -> DomesticStockCurrentPrice:
        """
        주식현재가 시세

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J:KRX, NX:NXT, UN:통합
            fid_input_iscd (str): 입력 종목코드

        Returns:
            DomesticStockCurrentPrice: 주식현재가 시세
        """
        headers = {
            "tr_id": "FHKST01010100",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
        }
        response = self.client._get("/uapi/domestic-stock/v1/quotations/inquire-price", headers=headers, params=params)
        return DomesticStockCurrentPrice.model_validate(response.json())

    def get_stock_current_price_2(
        self, fid_cond_mrkt_div_code: Literal["J", "NX", "UN"], fid_input_iscd: str
    ) -> DomesticStockCurrentPrice2:
        """
        주식현재가 시세2

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J:KRX, NX:NXT, UN:통합
            fid_input_iscd (str): 입력 종목코드

        Returns:
            DomesticStockCurrentPrice2: 주식현재가 시세2
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
        return DomesticStockCurrentPrice2.model_validate(response.json())

    def get_stock_current_price_detail(
        self, fid_cond_mrkt_div_code: Literal["J", "NX", "UN"], fid_input_iscd: str
    ) -> DomesticStockCurrentPriceDetail:
        """
        주식현재가 체결

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J:KRX, NX:NXT, UN:통합
            fid_input_iscd (str): 입력 종목코드

        Returns:
            DomesticStockCurrentPriceDetail: 주식현재가 체결
        """
        headers = {
            "tr_id": "FHKST01010300",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-ccnl", headers=headers, params=params
        )
        return DomesticStockCurrentPriceDetail.model_validate(response.json())

    def get_stock_current_price_daily(
        self,
        fid_cond_mrkt_div_code: Literal["J", "NX", "UN"],
        fid_input_iscd: str,
        fid_period_div_code: Literal["D", "W", "M"],
        fid_org_adj_prc: Literal["0", "1"],
    ) -> DomesticStockCurrentPriceDaily:
        """
        주식현재가 일자별

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J:KRX, NX:NXT, UN:통합
            fid_input_iscd (str): 입력 종목코드
            fid_period_div_code (str): 기간 분류 코드, D:일, W:주, M:월
            fid_org_adj_prc (str): 수정주가 원주가 가격, 0:수정주가미반영, 1:수정주가반영

        Returns:
            DomesticStockCurrentPriceDaily: 주식현재가 일자별
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
        return DomesticStockCurrentPriceDaily.model_validate(response.json())

    def get_stock_current_price_asking_expected_conclusion(
        self, fid_cond_mrkt_div_code: Literal["J", "NX", "UN"], fid_input_iscd: str
    ) -> DomesticStockCurrentPriceAskingExpectedConclusion:
        """
        주식현재가 호가/예상체결

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J:KRX, NX:NXT, UN:통합
            fid_input_iscd (str): 입력 종목코드

        Returns:
            DomesticStockCurrentPriceHogaExpectedConclusion: 주식현재가 호가/예상
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
        return DomesticStockCurrentPriceAskingExpectedConclusion.model_validate(response.json())

    def get_stock_current_price_investor(
        self, fid_cond_mrkt_div_code: Literal["J", "NX", "UN"], fid_input_iscd: str
    ) -> DomesticStockCurrentPriceInvestor:
        """
        주식현재가 투자자

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J:KRX, NX:NXT, UN:통합
            fid_input_iscd (str): 입력 종목코드

        Returns:
            DomesticStockCurrentPriceInvestor: 주식현재가 투자자
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
        return DomesticStockCurrentPriceInvestor.model_validate(response.json())

    def get_stock_current_price_member(
        self, fid_cond_mrkt_div_code: Literal["J", "NX", "UN"], fid_input_iscd: str
    ) -> DomesticStockCurrentPriceMember:
        """주식현재가 회원사"""
        headers = {
            "tr_id": "FHKST01010600",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
        }
        response = self.client._get("/uapi/domestic-stock/v1/quotations/inquire-member", headers=headers, params=params)
        return DomesticStockCurrentPriceMember.model_validate(response.json())

    def get_stock_period_quote(
        self,
        fid_cond_mrkt_div_code: Literal["J", "NX", "UN"],
        fid_input_iscd: str,
        fid_input_date_1: str,
        fid_input_date_2: str,
        fid_period_div_code: Literal["D", "W", "M", "Y"],
        fid_org_adj_prc: Literal["0", "1"],
    ) -> DomesticStockPeriodQuote:
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
            DomesticStockPeriodQuote: 국내주식기간별시세(일/주/월/년)
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
        return DomesticStockPeriodQuote.model_validate(response.json())

    def get_stock_today_minute_chart(
        self,
        fid_cond_mrkt_div_code: Literal["J", "NX", "UN"],
        fid_input_iscd: str,
        fid_input_hour_1: str,
        fid_pw_data_incu_yn: Literal["N", "Y"],
        fid_etc_cls_code: str,
    ) -> DomesticStockTodayMinuteChart:
        """
        주식당일분봉조회

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J:KRX, NX:NXT, UN:통합
            fid_input_iscd (str): 입력 종목코드
            fid_input_hour_1 (str): 입력 시간 1, 조회 시작시간 (HHMMSS)
            fid_pw_data_incu_yn (str): 체결량 포함 여부, N:체결량미포함, Y:체결량포함
            fid_etc_cls_code (str): 기타 분류 코드

        Returns:
            DomesticStockTodayMinuteChart: 주식당일분봉조회
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
        return DomesticStockTodayMinuteChart.model_validate(response.json())

    def get_stock_daily_minute_chart(
        self,
        fid_cond_mrkt_div_code: Literal["J", "NX", "UN"],
        fid_input_iscd: str,
        fid_input_hour_1: str,
        fid_input_date_1: str,
        fid_pw_data_incu_yn: Literal["N", "Y"],
        fid_fake_tick_incu_yn: Literal["", "N", "Y"] = "",
    ):
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
            DomesticStockTodayMinuteChart: 주식일별분봉조회
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
        return DomesticStockTodayMinuteChart.model_validate(response.json())

    def get_stock_current_price_time_item_conclusion(
        self,
        fid_cond_mrkt_div_code: Literal["J", "NX", "UN"],
        fid_input_iscd: str,
        fid_input_hour_1: str,
    ) -> DomesticStockCurrentPriceTimeItemConclusion:
        """
        주식현재가 당일시간대별체결

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J:KRX, NX:NXT, UN:통합
            fid_input_iscd (str): 입력 종목코드
            fid_input_hour_1 (str): 입력 시간 1, 조회 시작시간 (HHMMSS)

        Returns:
            DomesticStockCurrentPriceTimeItemConclusion: 주식현재가 당일시간대별체결
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
        return DomesticStockCurrentPriceTimeItemConclusion.model_validate(response.json())

    def get_stock_current_price_daily_overtime_price(
        self,
        fid_cond_mrkt_div_code: Literal["J", "NX", "UN"],
        fid_input_iscd: str,
    ) -> DomesticStockCurrentPriceDailyOvertimePrice:
        """
        주식현재가 시간외일자별주가

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J:KRX, NX:NXT, UN:통합
            fid_input_iscd (str): 입력 종목코드

        Returns:
            DomesticStockCurrentPriceDailyOvertimePrice: 주식현재가 시간외일자별주가
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
        return DomesticStockCurrentPriceDailyOvertimePrice.model_validate(response.json())

    def get_stock_current_price_overtime_conclusion(
        self, fid_cond_mrkt_div_code: Literal["J", "NX", "UN"], fid_input_iscd: str, fid_input_hour_1: str
    ) -> DomesticStockCurrentPriceOvertimeConclusion:
        """
        주식현재가 시간외시간별체결

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J:KRX, NX:NXT, UN:통합
            fid_input_iscd (str): 입력 종목코드
            fid_input_hour_1 (str): 입력 시간, 조회 시작시간 (HHMMSS)

        Returns:
            DomesticStockCurrentPriceOvertimeConclusion: 주식현재가 시간외시간별체결
        """
        headers = {
            "tr_id": "FHPST02310000",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_INPUT_HOUR_1": fid_input_hour_1,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-time-overtimeconclusion", headers=headers, params=params
        )
        return DomesticStockCurrentPriceOvertimeConclusion.model_validate(response.json())

    def get_stock_overtime_current_price(
        self, fid_cond_mrkt_div_code: Literal["J", "NX", "UN"], fid_input_iscd: str
    ) -> DomesticStockOvertimeCurrentPrice:
        """
        국내주식 시간외현재가
        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J:KRX, NX:NXT, UN:통합
            fid_input_iscd (str): 입력 종목코드

        Returns:
            DomesticStockOvertimeCurrentPrice: 국내주식 시간외현재가
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
        return DomesticStockOvertimeCurrentPrice.model_validate(response.json())

    def get_stock_overtime_asking_price(
        self, fid_input_iscd: str, fid_cond_mrkt_div_code: Literal["J"] = "J"
    ) -> DomesticStockOvertimeAskingPrice:
        """
        국내주식 시간외호가

        Args:
            fid_input_iscd (str): 입력 종목코드
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J: 주식

        Returns:
            DomesticStockOvertimeAskingPrice: 국내주식 시간외호가
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
        return DomesticStockOvertimeAskingPrice.model_validate(response.json())

    def get_stock_closing_expected_price(
        self,
        fid_rank_sort_cls_code: Literal["0", "1", "2", "3", "4"],
        fid_input_iscd: Literal["0000", "0001", "1001", "2001", "4001"],
        fid_blng_cls_code: Literal["0", "1"],
        fid_cond_mrkt_div_code: Literal["J"] = "J",
        fid_cond_scr_div_code: Literal["11173"] = "11173",
    ) -> DomesticStockClosingExpectedPrice:
        """
        국내주식 장마감 예상체결가

        Args:
            fid_rank_sort_cls_code (str): 순위 정렬 구분 코드, 0:전체, 1:상한가마감예상, 2:하한가마감예상, 3:직전대비상승률상위 ,4:직전대비하락률상위
            fid_input_iscd (str): 입력 종목코드, 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100
            fid_blng_cls_code (str): 소속 구분 코드, 0:전체, 1:종가범위연장
            fid_cond_mrkt_div (str): 조건 시장 분류 코드, J: 주식
            fid_cond_scr_div_code (str): 조건 화면 분류 코드, 11173:Unique key(11173)

        Returns:
            DomesticStockClosingExpectedPrice: 국내주식 장마감 예상체결가
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
        return DomesticStockClosingExpectedPrice.model_validate(response.json())

    def get_etfetn_current_price(
        self, fid_input_iscd: str, fid_cond_mrkt_div_code: Literal["J"] = "J"
    ) -> DomesticEtfEtnCurrentPrice:
        """
        ETF/ETN 현재가

        Args:
            fid_input_iscd (str): 입력 종목코드
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J: 주식

        Returns:
            DomesticEtfEtnCurrentPrice: ETF/ETN 현재가
        """
        headers = {
            "tr_id": "FHPST02400000",
        }
        params = {
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
        }
        response = self.client._get("/uapi/etfetn/v1/quotations/inquire-price", headers=headers, params=params)
        return DomesticEtfEtnCurrentPrice.model_validate(response.json())

    def get_etf_component_stock_price(
        self, fid_input_iscd: str, fid_cond_mrkt_div_code: Literal["J"] = "J", fid_cond_scr_div_code: str = "11216"
    ) -> DomesticEtfComponentStockPrice:
        """
        ETF 구성종목시세

        Args:
            fid_input_iscd (str): 입력 종목코드
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J: 주식
            fid_cond_scr_div_code (str): 조건 화면 분류 코드, 11216:Unique key(11216)

        Returns:
            DomesticEtfComponentStockPrice: ETF 구성종목시세
        """
        headers = {
            "tr_id": "FHKST121600C0",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_COND_SCR_DIV_CODE": fid_cond_scr_div_code,
        }
        response = self.client._get(
            "/uapi/etfetn/v1/quotations/inquire-component-stock-price", headers=headers, params=params
        )
        return DomesticEtfComponentStockPrice.model_validate(response.json())

    def get_etf_nav_comparison_trend(
        self, fid_input_iscd: str, fid_cond_mrkt_div_code: Literal["J"] = "J"
    ) -> DomesticEtfNavComparisonTrend:
        """
        NAV 비교추이(종목)

        Args:
            fid_input_iscd (str): 입력 종목코드
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J: 주식

        Returns:
            DomesticNavComparisonTrend: NAV 비교추이(종목)
        """
        headers = {
            "tr_id": "FHPST02440000",
        }
        params = {
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
        }
        response = self.client._get("/uapi/etfetn/v1/quotations/nav-comparison-trend", headers=headers, params=params)
        return DomesticEtfNavComparisonTrend.model_validate(response.json())

    def get_etf_nav_comparison_daily_trend(
        self,
        fid_input_iscd: str,
        fid_input_date_1: str,
        fid_input_date_2: str,
        fid_cond_mrkt_div_code: Literal["J"] = "J",
    ) -> DomesticEtfNavComparisonDailyTrend:
        """
        NAV 비교추이(일)

        Args:
            fid_input_iscd (str): 입력 종목코드
            fid_input_date_1 (str): 입력 날짜1, 조회 시작일자 (ex. 20240101)
            fid_input_date_2 (str): 입력 날짜2, 조회 종료일자 (ex. 20240220)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J: 주식

        Returns:
            DomesticNavComparisonDailyTrend: NAV 비교추이(일)
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
        return DomesticEtfNavComparisonDailyTrend.model_validate(response.json())

    def get_etf_nav_comparison_time_trend(
        self,
        fid_hour_cls_code: str,
        fid_input_iscd: str,
        fid_cond_mrkt_div_code: Literal["E"] = "E",
    ) -> DomesticEtfNavComparisonTimeTrend:
        """
        NAV 비교추이(분)

        Args:
            fid_hour_cls_code (str): FID 시간 구분 코드, 1분 :60, 3분: 180 … 120분:7200
            fid_input_iscd (str): 입력 종목코드
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, J: 주식
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
        return DomesticEtfNavComparisonTimeTrend.model_validate(response.json())
