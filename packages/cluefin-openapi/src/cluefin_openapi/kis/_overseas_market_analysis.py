from cluefin_openapi.kis._client import Client


class OverseasMarketAnalysis:
    """해외주식 시세분석"""

    def __init__(self, client: Client):
        self.client = client

url: /uapi/overseas-stock/v1/ranking/price-fluctuation
tr_id: 실전[HHDFS76260000]
arguments:
KEYB	NEXT KEY BUFF	string	Y	8	공백
AUTH	사용자권한정보	string	Y	32	공백
EXCD	거래소코드	string	Y	4	<description>NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스 
HKS : 홍콩, SHS : 상해 , SZS : 심천
HSX : 호치민, HNX : 하노이
TSE : 도쿄</description>
GUBN	급등/급락구분	string	Y	1	0(급락), 1(급등)
MIXN	N분전콤보값	string	Y	1	N분전 : 0(1분전), 1(2분전), 2(3분전), 3(5분전), 4(10분전), 5(15분전), 6(20분전), 7(30분전), 8(60분전), 9(120분전)
VOL_RANG	거래량조건	string	Y	1	0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)
    def get_stock_price_rise_fall(self):
        """해외주식 가격급등락"""
        pass

url: /uapi/overseas-stock/v1/ranking/volume-surge
tr_id: 실전[HHDFS76270000]
arguments:
KEYB	NEXT KEY BUFF	string	Y	8	공백
AUTH	사용자권한정보	string	Y	32	공백
EXCD	거래소코드	string	Y	4	<description>NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스 
HKS : 홍콩, SHS : 상해 , SZS : 심천
HSX : 호치민, HNX : 하노이
TSE : 도쿄</description>
MIXN	N분전콤보값	string	Y	1	N분전 : 0(1분전), 1(2분전), 2(3분전), 3(5분전), 4(10분전), 5(15분전), 6(20분전), 7(30분전), 8(60분전), 9(120분전)
VOL_RANG	거래량조건	string	Y	1	0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)
    def get_stock_volume_surge(self):
        """해외주식 거래량급증"""
        pass

url: /uapi/overseas-stock/v1/ranking/volume-power
tr_id: 실전[HHDFS76280000]
arguments:
KEYB	NEXT KEY BUFF	string	Y	8	공백
AUTH	사용자권한정보	string	Y	32	공백
EXCD	거래소코드	string	Y	4	<description>NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스
HKS : 홍콩, SHS : 상해 , SZS : 심천
HSX : 호치민, HNX : 하노이
TSE : 도쿄</description>
NDAY	N일자값	string	Y	1	N분전 : 0(1분전), 1(2분전), 2(3분전), 3(5분전), 4(10분전), 5(15분전), 6(20분전), 7(30분전), 8(60분전), 9(120분전)
VOL_RANG	거래량조건	string	Y	1	0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)
    def get_stock_buy_execution_strength_top(self):
        """해외주식 매수체결강도상위"""
        pass

url: /uapi/overseas-stock/v1/ranking/updown-rate
tr_id: 실전[HHDFS76290000]
arguments:
KEYB	NEXT KEY BUFF	string	Y	8	공백
AUTH	사용자권한정보	string	Y	32	공백
EXCD	거래소코드	string	Y	4	<description>NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스 
HKS : 홍콩, SHS : 상해 , SZS : 심천
HSX : 호치민, HNX : 하노이
TSE : 도쿄</description>
GUBN	상승율/하락율 구분	string	Y	1	0(하락율), 1(상승율)
NDAY	N일자값	string	Y	1	N일전 : 0(당일), 1(2일), 2(3일), 3(5일), 4(10일), 5(20일전), 6(30일), 7(60일), 8(120일), 9(1년)
VOL_RANG	거래량조건	string	Y	1	0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)
    def get_stock_rise_decline_rate(self):
        """해외주식 상승률/하락율"""
        pass

url: /uapi/overseas-stock/v1/ranking/new-highlow
tr_id: 실전[HHDFS76300000]
arguments:
KEYB	NEXT KEY BUFF	string	Y	8	공백
AUTH	사용자권한정보	string	Y	32	공백
EXCD	거래소코드	string	Y	4	<description>NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스 
HKS : 홍콩, SHS : 상해 , SZS : 심천
HSX : 호치민, HNX : 하노이
TSE : 도쿄</description>
GUBN	신고/신저 구분	string	Y	1	신고(1) 신저(0)
GUBN2	일시돌파/돌파 구분	string	Y	1	일시돌파(0) 돌파유지(1)
NDAY	N일자값	string	Y	1	N일전 : 0(5일), 1(10일), 2(20일), 3(30일), 4(60일), 5(120일전), 6(52주), 7(1년)
VOL_RANG	거래량조건	string	Y	1	0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)
    def get_stock_new_high_low_price(self):
        """해외주식 신고/신저가"""
        pass

url: /uapi/overseas-stock/v1/ranking/trade-vol
tr_id: 실전[HHDFS76310010]
arguments:
KEYB	NEXT KEY BUFF	string	Y	8	공백
AUTH	사용자권한정보	string	Y	32	공백
EXCD	거래소코드	string	Y	4	<description>NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스 
HKS : 홍콩, SHS : 상해 , SZS : 심천
HSX : 호치민, HNX : 하노이
TSE : 도쿄</description>
NDAY	N일자값	string	Y	1	N일전 : 0(당일), 1(2일), 2(3일), 3(5일), 4(10일), 5(20일전), 6(30일), 7(60일), 8(120일), 9(1년)
PRC1	현재가 필터범위 1	string	Y	12	가격 ~
PRC2	현재가 필터범위 2	string	Y	12	~ 가격
VOL_RANG	거래량조건	string	Y	1	0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)
    def get_stock_trading_volume_rank(self):
        """해외주식 거래량순위"""
        pass

url: /uapi/overseas-stock/v1/ranking/trade-pbmn
tr_id: 실전[HHDFS76320010]
arguments:
KEYB	NEXT KEY BUFF	string	Y	8	공백
AUTH	사용자권한정보	string	Y	32	공백
EXCD	거래소코드	string	Y	4	<description>NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스 
HKS : 홍콩, SHS : 상해 , SZS : 심천
HSX : 호치민, HNX : 하노이
TSE : 도쿄</description>
NDAY	N일자값	string	Y	1	N일전 : 0(당일), 1(2일), 2(3일), 3(5일), 4(10일), 5(20일전), 6(30일), 7(60일), 8(120일), 9(1년)
VOL_RANG	거래량조건	string	Y	1	0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)
PRC1	현재가 필터범위 1	string	Y	12	가격 ~
PRC2	현재가 필터범위 2	string	Y	12	~ 가격
    def get_stock_trading_amount_rank(self):
        """해외주식 거래대금순위"""
        pass

url: /uapi/overseas-stock/v1/ranking/trade-growth
tr_id: 실전[HHDFS76330000]
arguments:
KEYB	NEXT KEY BUFF	string	Y	8	공백
AUTH	사용자권한정보	string	Y	32	공백
EXCD	거래소코드	string	Y	4	<description>NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스
HKS : 홍콩, SHS : 상해 , SZS : 심천
HSX : 호치민, HNX : 하노이
TSE : 도쿄</description>
NDAY	N일자값	string	Y	1	N일전 : 0(당일), 1(2일), 2(3일), 3(5일), 4(10일), 5(20일전), 6(30일), 7(60일), 8(120일), 9(1년)
VOL_RANG	거래량조건	string	Y	1	0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)
    def get_stock_trading_increase_rate_rank(self):
        """해외주식 거래증가율순위"""
        pass

url: /uapi/overseas-stock/v1/ranking/trade-turnover
tr_id: 실전[HHDFS76340000]
arguments:
KEYB	NEXT KEY BUFF	string	Y	8	공백
AUTH	사용자권한정보	string	Y	32	공백
EXCD	거래소코드	string	Y	4	<description>NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스 
HKS : 홍콩, SHS : 상해 , SZS : 심천
HSX : 호치민, HNX : 하노이
TSE : 도쿄</description>
NDAY	N일자값	string	Y	1	N일전 : 0(당일), 1(2일), 2(3일), 3(5일), 4(10일), 5(20일전), 6(30일), 7(60일), 8(120일), 9(1년)
VOL_RANG	거래량조건	string	Y	1	0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)
    def get_stock_trading_turnover_rate_rank(self):
        """해외주식 거래회전율순위"""
        pass

url: /uapi/overseas-stock/v1/ranking/market-cap
tr_id: 실전[HHDFS76350100]
arguments:
KEYB	NEXT KEY BUFF	string	Y	1	공백
AUTH	사용자권한정보	string	Y	32	공백
EXCD	거래소코드	string	Y	4	<description>NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스 
HKS : 홍콩, SHS : 상해 , SZS : 심천
HSX : 호치민, HNX : 하노이
TSE : 도쿄</description>
VOL_RANG	거래량조건	string	Y	1	0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)
    def get_stock_market_cap_rank(self):
        """해외주식 시가총액순위"""
        pass

url: /uapi/overseas-price/v1/quotations/period-rights
tr_id: 실전[CTRGT011R]
arguments:
RGHT_TYPE_CD	권리유형코드	string	Y	2	<description>%%(전체), 01(유상), 02(무상), 03(배당), 11(합병), 
14(액면분할), 15(액면병합), 17(감자), 54(WR청구),
61(원리금상환), 71(WR소멸), 74(배당옵션), 75(특별배당), 76(ISINCODE변경), 77(실권주청약)</description>
INQR_DVSN_CD	조회구분코드	string	Y	2	02(현지기준일), 03(청약시작일), 04(청약종료일)
INQR_STRT_DT	조회시작일자	string	Y	8	일자 ~
INQR_END_DT	조회종료일자	string	Y	8	~ 일자
PDNO	상품번호	string	Y	12	공백
PRDT_TYPE_CD	상품유형코드	string	Y	3	공백
CTX_AREA_NK50	연속조회키50	string	Y	50	공백
CTX_AREA_FK50	연속조회검색조건50	string	Y	50	공백
    def get_stock_period_rights_inquiry(self):
        """해외주식 기간별권리조회"""
        pass

url: /uapi/overseas-price/v1/quotations/news-title
tr_id: 실전[HHPSTH60100C1]
arguments:
INFO_GB	뉴스구분	string	Y	1	전체: 공백
CLASS_CD	중분류	string	Y	2	 전체: 공백
NATION_CD	국가코드	string	Y	2	전체: 공백, CN(중국), HK(홍콩), US(미국)
EXCHANGE_CD	거래소코드	string	Y	3	전체: 공백
SYMB	종목코드	string	Y	20	전체: 공백
DATA_DT	조회일자	string	Y	8	전체: 공백, 특정일자(YYYYMMDD) ex. 20240502
DATA_TM	조회시간	string	Y	6	전체: 공백, 특정시간(HHMMSS) ex. 093500
CTS	다음키	string	Y	35	공백 입력
    def get_news_aggregate_title(self):
        """해외뉴스종합(제목)"""
        pass

url: /uapi/overseas-price/v1/quotations/rights-by-ice
tr_id: 실전[HHDFS78330900]
arguments:
NCOD	국가코드	string	Y	2	CN:중국 HK:홍콩 US:미국 JP:일본 VN:베트남
SYMB	심볼	string	Y	20	종목코드
ST_YMD	일자 시작일	string	Y	8	<description>미입력 시, 오늘-3개월
기간지정 시, 종료일 입력(ex. 20240514)

※ 조회기간 기준일 입력시 참고
- 상환: 상환일자, 조기상환: 조기상환일자, 티커변경: 적용일, 그 외: 발표일</description>
ED_YMD	일자 종료일	string	Y	8	<description>미입력 시, 오늘+3개월
기간지정 시, 종료일 입력(ex. 20240514)

※ 조회기간 기준일 입력시 참고
- 상환: 상환일자, 조기상환: 조기상환일자, 티커변경: 적용일, 그 외: 발표일</description>
    def get_stock_rights_aggregate(self):
        """해외주식 권리종합"""
        pass

url: /uapi/overseas-price/v1/quotations/colable-by-company
tr_id: 실전[CTLN4050R]
arguments:
PDNO	상품번호	string	Y	12	ex)AMD
PRDT_TYPE_CD	상품유형코드	string	Y	3	공백
INQR_STRT_DT	조회시작일자	string	Y	8	공백
INQR_END_DT	조회종료일자	string	Y	8	공백
INQR_DVSN	조회구분	string	Y	2	공백
NATN_CD	국가코드	string	Y	3	840(미국), 344(홍콩), 156(중국)
INQR_SQN_DVSN	조회순서구분	string	Y	2	01(이름순), 02(코드순)
RT_DVSN_CD	비율구분코드	string	Y	2	공백
RT	비율	string	Y	238	공백
LOAN_PSBL_YN	대출가능여부	string	Y	1	공백
CTX_AREA_FK100	연속조회검색조건100	string	Y	100	공백
CTX_AREA_NK100	연속조회키100	string	Y	100	공백
    def get_stock_collateral_loan_eligible(self):
        """당사 해외주식담보대출 가능 종목"""
        pass

url: /uapi/overseas-price/v1/quotations/brknews-title
tr_id: 실전[FHKST01011801]
arguments:
FID_NEWS_OFER_ENTP_CODE	뉴스제공업체코드	string	Y	40	뉴스제공업체구분=>0:전체조회
FID_COND_MRKT_CLS_CODE	조건시장구분코드	string	Y	6	공백
FID_INPUT_ISCD	입력종목코드	string	Y	12	공백
FID_TITL_CNTT	제목내용	string	Y	132	공백
FID_INPUT_DATE_1	입력날짜1	string	Y	10	공백
FID_INPUT_HOUR_1	입력시간1	string	Y	10	공백
FID_RANK_SORT_CLS_CODE	순위정렬구분코드	string	Y	2	공백
FID_INPUT_SRNO	입력일련번호	string	Y	20	공백
FID_COND_SCR_DIV_CODE	조건화면분류코드	string	Y	5	화면번호:11801
    def get_breaking_news_title(self):
        """해외속보(제목)"""
        pass
