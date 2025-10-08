from cluefin_openapi.kis._client import Client


class DomesticIssueOther:
    """국내주식 업종/기타"""

    def __init__(self, client: Client):
        self.client = client

url: /uapi/domestic-stock/v1/quotations/inquire-index-price
tr_id: FHPUP02100000
argument:
FID_COND_MRKT_DIV_CODE	FID 조건 시장 분류 코드	String	Y	2	업종(U)
FID_INPUT_ISCD	FID 입력 종목코드	String	Y	12	코스피(0001), 코스닥(1001), 코스피200(2001) ... 포탈 (FAQ : 종목정보 다운로드(국내) - 업종코드 참조)
    def get_sector_current_index(self):
        """국내업종 현재지수"""
        pass


url: /uapi/domestic-stock/v1/quotations/inquire-index-daily-price
tr_id: FHPUP02120000
argument:
FID_PERIOD_DIV_CODE	FID 기간 분류 코드	String	Y	32	일/주/월 구분코드 ( D:일별 , W:주별, M:월별 )
FID_COND_MRKT_DIV_CODE	FID 조건 시장 분류 코드	String	Y	2	시장구분코드 (업종 U)
FID_INPUT_ISCD	FID 입력 종목코드	String	Y	12	코스피(0001), 코스닥(1001), 코스피200(2001) ... 포탈 (FAQ : 종목정보 다운로드(국내) - 업종코드 참조)
FID_INPUT_DATE_1	FID 입력 날짜1	String	Y	10	입력 날짜(ex. 20240223)
    def get_sector_daily_index(self):
        """국내업종 일자별지수"""
        pass

url: /uapi/domestic-stock/v1/quotations/inquire-index-tickprice
tr_id: FHPUP02110100
argument:
FID_INPUT_ISCD	입력 종목코드	String	Y	12	0001:거래소, 1001:코스닥, 2001:코스피200, 3003:KSQ150
FID_COND_MRKT_DIV_CODE	시장 분류 코드	String	Y	2	시장구분코드 (업종 U)
    def get_sector_time_index_second(self):
        """국내업종 시간별지수(초)"""
        pass

url: /uapi/domestic-stock/v1/quotations/inquire-index-timeprice
tr_id: FHPUP02110200
argument:
FID_INPUT_HOUR_1	?입력 시간1	String	Y	10	초단위, 60(1분), 300(5분), 600(10분)
FID_INPUT_ISCD	입력 종목코드	String	Y	12	0001:거래소, 1001:코스닥, 2001:코스피200, 3003:KSQ150
FID_COND_MRKT_DIV_CODE	조건 시장 분류 코드	String	Y	2	시장구분코드 (업종 U)
    def get_sector_time_index_minute(self):
        """국내업종 시간별지수(분)"""
        pass

url: /uapi/domestic-stock/v1/quotations/inquire-time-indexchartprice
tr_id: FHKUP03500200
argument:
FID_COND_MRKT_DIV_CODE	FID 조건 시장 분류 코드	String	Y	2	U
FID_ETC_CLS_CODE	FID 기타 구분 코드	String	Y	12	0: 기본 1:장마감,시간외 제외
FID_INPUT_ISCD	FID 입력 종목코드	String	Y	12	0001 : 종합 0002 : 대형주 ... 포탈 (FAQ : 종목정보 다운로드(국내) - 업종코드 참조)
FID_INPUT_HOUR_1	FID 입력 시간1	String	Y	12	30, 60 -> 1분, 600-> 10분, 3600 -> 1시간
FID_PW_DATA_INCU_YN	FID 과거 데이터 포함 여부	String	Y	12	Y (과거) / N (당일)
    def get_sector_minute_inquiry(self):
        """업종 분봉조회"""
        pass

url: /uapi/domestic-stock/v1/quotations/inquire-daily-indexchartprice
tr_id: FHKUP03500100
argument:
FID_COND_MRKT_DIV_CODE	조건 시장 분류 코드	String	Y	2	업종 : U
FID_INPUT_ISCD	업종 상세코드	String	Y	2	'0001 : 종합 0002 : 대형주 ... 포탈 (FAQ : 종목정보 다운로드(국내) - 업종코드 참조)'
FID_INPUT_DATE_1	조회 시작일자	String	Y	10	조회 시작일자 (ex. 20220501)
FID_INPUT_DATE_2	조회 종료일자	String	Y	10	조회 종료일자 (ex. 20220530)
FID_PERIOD_DIV_CODE	' 기간분류코드'	String	Y	32	' D:일봉 W:주봉, M:월봉, Y:년봉'
    def get_sector_period_quote(self):
        """국내주식업종기간별시세(일/주/월/년)"""
        pass

url: /uapi/domestic-stock/v1/quotations/inquire-index-category-price
tr_id: FHPUP02140000
argument:
FID_COND_MRKT_DIV_CODE	FID 조건 시장 분류 코드	String	Y	2	시장구분코드 (업종 U)
FID_INPUT_ISCD	FID 입력 종목코드	String	Y	12	코스피(0001), 코스닥(1001), 코스피200(2001) ... 포탈 (FAQ : 종목정보 다운로드(국내) - 업종코드 참조)
FID_COND_SCR_DIV_CODE	FID 조건 화면 분류 코드	String	Y	5	Unique key( 20214 )
FID_MRKT_CLS_CODE	FID 시장 구분 코드	String	Y	2	시장구분코드(K:거래소, Q:코스닥, K2:코스피200)
FID_BLNG_CLS_CODE	FID 소속 구분 코드	String	Y	2	시장구분코드에 따라 아래와 같이 입력. 시장구분코드(K:거래소) 0:전업종, 1:기타구분, 2:자본금구분 3:상업별구분, 시장구분코드(Q:코스닥) 0:전업종, 1:기타구분, 2:벤처구분 3:일반구분, 시장구분코드(K2:코스닥) 0:전업종
    def get_sector_all_quote_by_category(self):
        """국내업종 구분별전체시세"""
        pass

url: /uapi/domestic-stock/v1/quotations/exp-index-trend
tr_id: FHPST01840000
argument:
FID_MKOP_CLS_CODE	장운영 구분 코드	String	Y	2	1: 장시작전, 2: 장마감
FID_INPUT_HOUR_1	입력 시간1	String	Y	10	10(10초), 30(30초), 60(1분), 600(10분)
FID_INPUT_ISCD	입력 종목코드	String	Y	12	0000:전체, 0001:코스피, 1001:코스닥, 2001:코스피200, 4001: KRX100
FID_COND_MRKT_DIV_CODE	조건 시장 분류 코드	String	Y	2	시장구분코드 (주식 U)
    def get_expected_index_trend(self):
        """국내주식 예상체결지수 추이"""
        pass

url: /uapi/domestic-stock/v1/quotations/exp-total-index
tr_id: FHKUP11750000
argument:
fid_mrkt_cls_code	시장 구분 코드	String	Y	2	0:전체 K:거래소 Q:코스닥
fid_cond_mrkt_div_code	조건 시장 분류 코드	String	Y	2	시장구분코드 (업종 U)
fid_cond_scr_div_code	조건 화면 분류 코드	String	Y	5	Unique key(11175)
fid_input_iscd	입력 종목코드	String	Y	12	0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100
fid_mkop_cls_code	장운영 구분 코드	String	Y	2	1:장시작전, 2:장마감
    def get_expected_index_all(self):
        """국내주식 예상체결 전체지수"""
        pass

url: /uapi/domestic-stock/v1/quotations/inquire-vi-status
tr_id: FHPST01390000
argument:
FID_DIV_CLS_CODE	FID 분류 구분 코드	String	Y	2	0:전체 1:상승 2:하락
FID_COND_SCR_DIV_CODE	FID 조건 화면 분류 코드	String	Y	5	20139
FID_MRKT_CLS_CODE	FID 시장 구분 코드	String	Y	2	0:전체 K:거래소 Q:코스닥
FID_INPUT_ISCD	FID 입력 종목코드	String	Y	12	
FID_RANK_SORT_CLS_CODE	FID 순위 정렬 구분 코드	String	Y	2	0:전체1:정적2:동적3:정적&동적
FID_INPUT_DATE_1	FID 입력 날짜1	String	Y	10	영업일
FID_TRGT_CLS_CODE	FID 대상 구분 코드	String	Y	32	
FID_TRGT_EXLS_CLS_CODE	FID 대상 제외 구분 코드	String	Y	32	
    def get_volatility_interruption_status(self):
        """변동성완화장치(VI) 현황"""
        pass

url: /uapi/domestic-stock/v1/quotations/comp-interest
tr_id: FHPST07020000
argument:
FID_COND_MRKT_DIV_CODE	조건시장분류코드	String	Y	2	Unique key(I)
FID_COND_SCR_DIV_CODE	조건화면분류코드	String	Y	5	Unique key(20702)
FID_DIV_CLS_CODE	분류구분코드	String	Y	2	1: 해외금리지표
FID_DIV_CLS_CODE1	분류구분코드	String	Y	2	공백 : 전체
    def get_interest_rate_summary(self):
        """금리 종합(국내채권/금리)"""
        pass

url: /uapi/domestic-stock/v1/quotations/news-title
tr_id: FHKST01011800
argument:
FID_NEWS_OFER_ENTP_CODE	뉴스 제공 업체 코드	String	Y	40	공백 필수 입력
FID_COND_MRKT_CLS_CODE	조건 시장 구분 코드	String	Y	6	공백 필수 입력
FID_INPUT_ISCD	입력 종목코드	String	Y	12	공백: 전체, 종목코드 : 해당코드가 등록된 뉴스
FID_TITL_CNTT	제목 내용	String	Y	132	공백 필수 입력
FID_INPUT_DATE_1	입력 날짜	String	Y	10	공백: 현재기준, 조회일자(ex 00YYYYMMDD)
FID_INPUT_HOUR_1	입력 시간	String	Y	10	공백: 현재기준, 조회시간(ex 0000HHMMSS)
FID_RANK_SORT_CLS_CODE	순위 정렬 구분 코드	String	Y	2	공백 필수 입력
FID_INPUT_SRNO	입력 일련번호	String	Y	20	공백 필수 입력
    def get_market_announcement_schedule(self):
        """종합 시황/공시(제목)"""
        pass

url: /uapi/domestic-stock/v1/quotations/chk-holiday
tr_id: CTCA0903R
argument:
BASS_DT	기준일자	String	Y	8	기준일자(YYYYMMDD)
CTX_AREA_NK	연속조회키	String	Y	20	공백으로 입력
CTX_AREA_FK	연속조회검색조건	String	Y	20	공백으로 입력
    def get_holiday_inquiry(self):
        """국내휴장일조회"""
        pass

url: /uapi/domestic-stock/v1/quotations/market-time
tr_id: HHMCM000002C0
argument:
    def get_futures_business_day_inquiry(self):
        """국내선물 영업일조회"""
        pass
