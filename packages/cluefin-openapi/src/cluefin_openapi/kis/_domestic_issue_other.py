from cluefin_openapi.kis._client import Client
from cluefin_openapi.kis._domestic_issue_other_types import (
    ExpectedIndexAll,
    ExpectedIndexTrend,
    FuturesBusinessDayInquiry,
    HolidayInquiry,
    InterestRateSummary,
    MarketAnnouncementSchedule,
    SectorAllQuoteByCategory,
    SectorCurrentIndex,
    SectorDailyIndex,
    SectorMinuteInquiry,
    SectorPeriodQuote,
    SectorTimeIndexMinute,
    SectorTimeIndexSecond,
    VolatilityInterruptionStatus,
)


class DomesticIssueOther:
    """국내주식 업종/기타"""

    def __init__(self, client: Client):
        self.client = client

    def get_sector_current_index(
        self,
        fid_cond_mrkt_div_code: str,
        fid_input_iscd: str,
    ) -> SectorCurrentIndex:
        """
        국내업종 현재지수

        Args:
            fid_cond_mrkt_div_code (str): FID 조건 시장 분류 코드
            fid_input_iscd (str): FID 입력 종목코드

        Returns:
            SectorCurrentIndex: 국내업종 현재지수 응답 객체
        """
        headers = {
            "tr_id": "FHPUP02100000",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-index-price", headers=headers, params=params
        )
        return SectorCurrentIndex.model_validate(response.json())

    def get_sector_daily_index(
        self,
        fid_period_div_code: str,
        fid_cond_mrkt_div_code: str,
        fid_input_iscd: str,
        fid_input_date_1: str,
    ) -> SectorDailyIndex:
        """
        국내업종 일자별지수

        Args:
            fid_period_div_code (str): FID 기간 분류 코드 (D:일별, W:주별, M:월별)
            fid_cond_mrkt_div_code (str): FID 조건 시장 분류 코드 (업종 U)
            fid_input_iscd (str): FID 입력 종목코드 (0001:코스피, 1001:코스닥, 2001:코스피200)
            fid_input_date_1 (str): FID 입력 날짜1 (ex. 20240223)

        Returns:
            SectorDailyIndex: 국내업종 일자별지수 응답 객체
        """
        headers = {
            "tr_id": "FHPUP02120000",
        }
        params = {
            "FID_PERIOD_DIV_CODE": fid_period_div_code,
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_INPUT_DATE_1": fid_input_date_1,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-index-daily-price", headers=headers, params=params
        )
        return SectorDailyIndex.model_validate(response.json())

    def get_sector_time_index_second(
        self,
        fid_input_iscd: str,
        fid_cond_mrkt_div_code: str,
    ) -> SectorTimeIndexSecond:
        """
        국내업종 시간별지수(초)

        Args:
            fid_input_iscd (str): 입력 종목코드 (0001:거래소, 1001:코스닥, 2001:코스피200, 3003:KSQ150)
            fid_cond_mrkt_div_code (str): 시장 분류 코드 (업종 U)

        Returns:
            SectorTimeIndexSecond: 국내업종 시간별지수(초) 응답 객체
        """
        headers = {
            "tr_id": "FHPUP02110100",
        }
        params = {
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-index-tickprice", headers=headers, params=params
        )
        return SectorTimeIndexSecond.model_validate(response.json())

    def get_sector_time_index_minute(
        self,
        fid_input_hour_1: str,
        fid_input_iscd: str,
        fid_cond_mrkt_div_code: str,
    ) -> SectorTimeIndexMinute:
        """
        국내업종 시간별지수(분)

        Args:
            fid_input_hour_1 (str): 입력 시간1 초단위 (60:1분, 300:5분, 600:10분)
            fid_input_iscd (str): 입력 종목코드 (0001:거래소, 1001:코스닥, 2001:코스피200, 3003:KSQ150)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (업종 U)

        Returns:
            SectorTimeIndexMinute: 국내업종 시간별지수(분) 응답 객체
        """
        headers = {
            "tr_id": "FHPUP02110200",
        }
        params = {
            "FID_INPUT_HOUR_1": fid_input_hour_1,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-index-timeprice", headers=headers, params=params
        )
        return SectorTimeIndexMinute.model_validate(response.json())

    def get_sector_minute_inquiry(
        self,
        fid_cond_mrkt_div_code: str,
        fid_etc_cls_code: str,
        fid_input_iscd: str,
        fid_input_hour_1: str,
        fid_pw_data_incu_yn: str,
    ) -> SectorMinuteInquiry:
        """
        업종 분봉조회

        Args:
            fid_cond_mrkt_div_code (str): FID 조건 시장 분류 코드 (U)
            fid_etc_cls_code (str): FID 기타 구분 코드 (0:기본, 1:장마감,시간외 제외)
            fid_input_iscd (str): FID 입력 종목코드 (0001:종합, 0002:대형주)
            fid_input_hour_1 (str): FID 입력 시간1 (30, 60:1분, 600:10분, 3600:1시간)
            fid_pw_data_incu_yn (str): FID 과거 데이터 포함 여부 (Y:과거, N:당일)

        Returns:
            SectorMinuteInquiry: 업종 분봉조회 응답 객체
        """
        headers = {
            "tr_id": "FHKUP03500200",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_ETC_CLS_CODE": fid_etc_cls_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_INPUT_HOUR_1": fid_input_hour_1,
            "FID_PW_DATA_INCU_YN": fid_pw_data_incu_yn,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-time-indexchartprice", headers=headers, params=params
        )
        return SectorMinuteInquiry.model_validate(response.json())

    def get_sector_period_quote(
        self,
        fid_cond_mrkt_div_code: str,
        fid_input_iscd: str,
        fid_input_date_1: str,
        fid_input_date_2: str,
        fid_period_div_code: str,
    ) -> SectorPeriodQuote:
        """
        국내주식업종기간별시세(일/주/월/년)

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (업종:U)
            fid_input_iscd (str): 업종 상세코드 (0001:종합, 0002:대형주)
            fid_input_date_1 (str): 조회 시작일자 (ex. 20220501)
            fid_input_date_2 (str): 조회 종료일자 (ex. 20220530)
            fid_period_div_code (str): 기간분류코드 (D:일봉, W:주봉, M:월봉, Y:년봉)

        Returns:
            SectorPeriodQuote: 국내주식업종기간별시세 응답 객체
        """
        headers = {
            "tr_id": "FHKUP03500100",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_INPUT_DATE_1": fid_input_date_1,
            "FID_INPUT_DATE_2": fid_input_date_2,
            "FID_PERIOD_DIV_CODE": fid_period_div_code,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-daily-indexchartprice", headers=headers, params=params
        )
        return SectorPeriodQuote.model_validate(response.json())

    def get_sector_all_quote_by_category(
        self,
        fid_cond_mrkt_div_code: str,
        fid_input_iscd: str,
        fid_cond_scr_div_code: str,
        fid_mrkt_cls_code: str,
        fid_blng_cls_code: str,
    ) -> SectorAllQuoteByCategory:
        """
        국내업종 구분별전체시세

        Args:
            fid_cond_mrkt_div_code (str): FID 조건 시장 분류 코드 (업종 U)
            fid_input_iscd (str): FID 입력 종목코드 (0001:코스피, 1001:코스닥, 2001:코스피200)
            fid_cond_scr_div_code (str): FID 조건 화면 분류 코드 (Unique key: 20214)
            fid_mrkt_cls_code (str): FID 시장 구분 코드 (K:거래소, Q:코스닥, K2:코스피200)
            fid_blng_cls_code (str): FID 소속 구분 코드 (0:전업종, 1:기타구분, 2:자본금/벤처구분, 3:상업별/일반구분)

        Returns:
            SectorAllQuoteByCategory: 국내업종 구분별전체시세 응답 객체
        """
        headers = {
            "tr_id": "FHPUP02140000",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_COND_SCR_DIV_CODE": fid_cond_scr_div_code,
            "FID_MRKT_CLS_CODE": fid_mrkt_cls_code,
            "FID_BLNG_CLS_CODE": fid_blng_cls_code,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-index-category-price", headers=headers, params=params
        )
        return SectorAllQuoteByCategory.model_validate(response.json())

    def get_expected_index_trend(
        self,
        fid_mkop_cls_code: str,
        fid_input_hour_1: str,
        fid_input_iscd: str,
        fid_cond_mrkt_div_code: str,
    ) -> ExpectedIndexTrend:
        """
        국내주식 예상체결지수 추이

        Args:
            fid_mkop_cls_code (str): 장운영 구분 코드 (1:장시작전, 2:장마감)
            fid_input_hour_1 (str): 입력 시간1 (10:10초, 30:30초, 60:1분, 600:10분)
            fid_input_iscd (str): 입력 종목코드 (0000:전체, 0001:코스피, 1001:코스닥, 2001:코스피200, 4001:KRX100)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (주식 U)

        Returns:
            ExpectedIndexTrend: 국내주식 예상체결지수 추이 응답 객체
        """
        headers = {
            "tr_id": "FHPST01840000",
        }
        params = {
            "FID_MKOP_CLS_CODE": fid_mkop_cls_code,
            "FID_INPUT_HOUR_1": fid_input_hour_1,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/exp-index-trend", headers=headers, params=params
        )
        return ExpectedIndexTrend.model_validate(response.json())

    def get_expected_index_all(
        self,
        fid_mrkt_cls_code: str,
        fid_cond_mrkt_div_code: str,
        fid_cond_scr_div_code: str,
        fid_input_iscd: str,
        fid_mkop_cls_code: str,
    ) -> ExpectedIndexAll:
        """
        국내주식 예상체결 전체지수

        Args:
            fid_mrkt_cls_code (str): 시장 구분 코드 (0:전체, K:거래소, Q:코스닥)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (업종 U)
            fid_cond_scr_div_code (str): 조건 화면 분류 코드 (Unique key: 11175)
            fid_input_iscd (str): 입력 종목코드 (0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001:KRX100)
            fid_mkop_cls_code (str): 장운영 구분 코드 (1:장시작전, 2:장마감)

        Returns:
            ExpectedIndexAll: 국내주식 예상체결 전체지수 응답 객체
        """
        headers = {
            "tr_id": "FHKUP11750000",
        }
        params = {
            "fid_mrkt_cls_code": fid_mrkt_cls_code,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
            "fid_cond_scr_div_code": fid_cond_scr_div_code,
            "fid_input_iscd": fid_input_iscd,
            "fid_mkop_cls_code": fid_mkop_cls_code,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/exp-total-index", headers=headers, params=params
        )
        return ExpectedIndexAll.model_validate(response.json())

    def get_volatility_interruption_status(
        self,
        fid_div_cls_code: str,
        fid_cond_scr_div_code: str,
        fid_mrkt_cls_code: str,
        fid_input_iscd: str,
        fid_rank_sort_cls_code: str,
        fid_input_date_1: str,
        fid_trgt_cls_code: str,
        fid_trgt_exls_cls_code: str,
    ) -> VolatilityInterruptionStatus:
        """
        변동성완화장치(VI) 현황

        Args:
            fid_div_cls_code (str): FID 분류 구분 코드 (0:전체, 1:상승, 2:하락)
            fid_cond_scr_div_code (str): FID 조건 화면 분류 코드 (20139)
            fid_mrkt_cls_code (str): FID 시장 구분 코드 (0:전체, K:거래소, Q:코스닥)
            fid_input_iscd (str): FID 입력 종목코드
            fid_rank_sort_cls_code (str): FID 순위 정렬 구분 코드 (0:전체, 1:정적, 2:동적, 3:정적&동적)
            fid_input_date_1 (str): FID 입력 날짜1 (영업일)
            fid_trgt_cls_code (str): FID 대상 구분 코드
            fid_trgt_exls_cls_code (str): FID 대상 제외 구분 코드

        Returns:
            VolatilityInterruptionStatus: 변동성완화장치(VI) 현황 응답 객체
        """
        headers = {
            "tr_id": "FHPST01390000",
        }
        params = {
            "FID_DIV_CLS_CODE": fid_div_cls_code,
            "FID_COND_SCR_DIV_CODE": fid_cond_scr_div_code,
            "FID_MRKT_CLS_CODE": fid_mrkt_cls_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_RANK_SORT_CLS_CODE": fid_rank_sort_cls_code,
            "FID_INPUT_DATE_1": fid_input_date_1,
            "FID_TRGT_CLS_CODE": fid_trgt_cls_code,
            "FID_TRGT_EXLS_CLS_CODE": fid_trgt_exls_cls_code,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/inquire-vi-status", headers=headers, params=params
        )
        return VolatilityInterruptionStatus.model_validate(response.json())

    def get_interest_rate_summary(
        self,
        fid_cond_mrkt_div_code: str,
        fid_cond_scr_div_code: str,
        fid_div_cls_code: str,
        fid_div_cls_code1: str,
    ) -> InterestRateSummary:
        """
        금리 종합(국내채권/금리)

        Args:
            fid_cond_mrkt_div_code (str): 조건시장분류코드 (Unique key: I)
            fid_cond_scr_div_code (str): 조건화면분류코드 (Unique key: 20702)
            fid_div_cls_code (str): 분류구분코드 (1:해외금리지표)
            fid_div_cls_code1 (str): 분류구분코드 (공백:전체)

        Returns:
            InterestRateSummary: 금리 종합 응답 객체
        """
        headers = {
            "tr_id": "FHPST07020000",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_COND_SCR_DIV_CODE": fid_cond_scr_div_code,
            "FID_DIV_CLS_CODE": fid_div_cls_code,
            "FID_DIV_CLS_CODE1": fid_div_cls_code1,
        }
        response = self.client._get("/uapi/domestic-stock/v1/quotations/comp-interest", headers=headers, params=params)
        return InterestRateSummary.model_validate(response.json())

    def get_market_announcement_schedule(
        self,
        fid_news_ofer_entp_code: str,
        fid_cond_mrkt_cls_code: str,
        fid_input_iscd: str,
        fid_titl_cntt: str,
        fid_input_date_1: str,
        fid_input_hour_1: str,
        fid_rank_sort_cls_code: str,
        fid_input_srno: str,
    ) -> MarketAnnouncementSchedule:
        """
        종합 시황/공시(제목)

        Args:
            fid_news_ofer_entp_code (str): 뉴스 제공 업체 코드 (공백 필수)
            fid_cond_mrkt_cls_code (str): 조건 시장 구분 코드 (공백 필수)
            fid_input_iscd (str): 입력 종목코드 (공백:전체, 종목코드:해당코드 뉴스)
            fid_titl_cntt (str): 제목 내용 (공백 필수)
            fid_input_date_1 (str): 입력 날짜 (공백:현재기준, 조회일자 ex. 00YYYYMMDD)
            fid_input_hour_1 (str): 입력 시간 (공백:현재기준, 조회시간 ex. 0000HHMMSS)
            fid_rank_sort_cls_code (str): 순위 정렬 구분 코드 (공백 필수)
            fid_input_srno (str): 입력 일련번호 (공백 필수)

        Returns:
            MarketAnnouncementSchedule: 종합 시황/공시 응답 객체
        """
        headers = {
            "tr_id": "FHKST01011800",
        }
        params = {
            "FID_NEWS_OFER_ENTP_CODE": fid_news_ofer_entp_code,
            "FID_COND_MRKT_CLS_CODE": fid_cond_mrkt_cls_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_TITL_CNTT": fid_titl_cntt,
            "FID_INPUT_DATE_1": fid_input_date_1,
            "FID_INPUT_HOUR_1": fid_input_hour_1,
            "FID_RANK_SORT_CLS_CODE": fid_rank_sort_cls_code,
            "FID_INPUT_SRNO": fid_input_srno,
        }
        response = self.client._get("/uapi/domestic-stock/v1/quotations/news-title", headers=headers, params=params)
        return MarketAnnouncementSchedule.model_validate(response.json())

    def get_holiday_inquiry(
        self,
        bass_dt: str,
        ctx_area_nk: str,
        ctx_area_fk: str,
    ) -> HolidayInquiry:
        """
        국내휴장일조회

        Args:
            bass_dt (str): 기준일자 (YYYYMMDD)
            ctx_area_nk (str): 연속조회키 (공백으로 입력)
            ctx_area_fk (str): 연속조회검색조건 (공백으로 입력)

        Returns:
            HolidayInquiry: 국내휴장일조회 응답 객체
        """
        headers = {
            "tr_id": "CTCA0903R",
        }
        params = {
            "BASS_DT": bass_dt,
            "CTX_AREA_NK": ctx_area_nk,
            "CTX_AREA_FK": ctx_area_fk,
        }
        response = self.client._get("/uapi/domestic-stock/v1/quotations/chk-holiday", headers=headers, params=params)
        return HolidayInquiry.model_validate(response.json())

    def get_futures_business_day_inquiry(self) -> FuturesBusinessDayInquiry:
        """
        국내선물 영업일조회

        Returns:
            FuturesBusinessDayInquiry: 국내선물 영업일조회 응답 객체
        """
        headers = {
            "tr_id": "HHMCM000002C0",
        }
        params = {}
        response = self.client._get("/uapi/domestic-stock/v1/quotations/market-time", headers=headers, params=params)
        return FuturesBusinessDayInquiry.model_validate(response.json())
