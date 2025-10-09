from cluefin_openapi.kis._client import Client


class BasicQuote:
    """해외주식 기본시세"""

    def __init__(self, client: Client):
        self.client = client

url: /uapi/overseas-price/v1/quotations/price-detail
tr_id: 실전[HHDFS76200200], 모의[모의투자 미지원]
arguments:
AUTH	사용자권한정보	string	Y	32 공백입력
EXCD	거래소명	string	Y	4	<description>HKS : 홍콩
NYS : 뉴욕
NAS : 나스닥
AMS : 아멕스
TSE : 도쿄
SHS : 상해
SZS : 심천
SHI : 상해지수
SZI : 심천지수
HSX : 호치민
HNX : 하노이
BAY : 뉴욕(주간)
BAQ : 나스닥(주간)
BAA : 아멕스(주간)</description>
SYMB	종목코드	string	Y	16	 
    def get_stock_current_price_detail(self):
        """해외주식 현재가상세"""
        pass

url: /uapi/overseas-price/v1/quotations/inquire-asking-price
tr_id: 실전[해외주식-033], 모의[모의투자 미지원]
arguments:
AUTH	사용자권한정보	string	Y	32	공백
EXCD	거래소코드	string	Y	4	<description>NYS : 뉴욕
NAS : 나스닥
AMS : 아멕스 
HKS : 홍콩
SHS : 상해 
SZS : 심천
HSX : 호치민
HNX : 하노이
TSE : 도쿄 
BAY : 뉴욕(주간)
BAQ : 나스닥(주간)
BAA : 아멕스(주간)</description>
SYMB	종목코드	string	Y	16	종목코드 예)TSLA
    def get_current_price_first_quote(self):
        """해외주식 현재가 1호가"""
        pass

url: /uapi/overseas-price/v1/quotations/price
tr_id: 실전[HHDFS00000300], 모의[HHDFS00000300]
arguments:
AUTH	사용자권한정보	string	Y	32	"" (Null 값 설정)
EXCD	거래소코드	string	Y	4	<description>HKS : 홍콩
NYS : 뉴욕
NAS : 나스닥
AMS : 아멕스
TSE : 도쿄
SHS : 상해
SZS : 심천
SHI : 상해지수
SZI : 심천지수
HSX : 호치민
HNX : 하노이
BAY : 뉴욕(주간)
BAQ : 나스닥(주간)
BAA : 아멕스(주간)</description>
SYMB	종목코드	string	Y	16	
    def get_stock_current_price_conclusion(self):
        """해외주식 현재체결가"""
        pass

url: /uapi/overseas-price/v1/quotations/inquire-ccnl
tr_id: 실전[해외주식-037], 모의[모의투자 미지원]
arguments:
EXCD	거래소명	string	Y	4	<description>NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스 
HKS : 홍콩, SHS : 상해 , SZS : 심천
HSX : 호치민, HNX : 하노이
TSE : 도쿄</description>
AUTH	사용자권한정보	string	Y	32	공백
KEYB	NEXT KEY BUFF	string	Y	32	공백
TDAY	당일전일구분	string	Y	1	0:전일, 1:당일
SYMB	종목코드	string	Y	16	해외종목코드
    def get_conclusion_trend(self):
        """해외주식 체결추이"""
        pass

url: /uapi/overseas-price/v1/quotations/inquire-time-itemchartprice
tr_id: 실전[HHDFS76950200], 모의[모의투자 미지원]
arguments:
AUTH	사용자권한정보	string	Y	32	"" 공백으로 입력
EXCD	거래소코드	string	Y	4	<description>NYS : 뉴욕
NAS : 나스닥
AMS : 아멕스 
HKS : 홍콩
SHS : 상해 
SZS : 심천
HSX : 호치민
HNX : 하노이
TSE : 도쿄 

※ 주간거래는 최대 1일치 분봉만 조회 가능
BAY : 뉴욕(주간)
BAQ : 나스닥(주간)
BAA : 아멕스(주간)</description>
SYMB	종목코드	string	Y	16	종목코드(ex. TSLA)
NMIN	분갭	string	Y	4	분단위(1: 1분봉, 2: 2분봉, ...)
PINC	전일포함여부	string	Y	1	0:당일 1:전일포함 ※ 다음조회 시 반드시 "1"로 입력
NEXT	다음여부	string	Y	1	처음조회 시, "" 공백 입력, 다음조회 시, "1" 입력
NREC	요청갯수	string	Y	4	레코드요청갯수 (최대 120)
FILL	미체결채움구분	string	Y	1	"" 공백으로 입력
KEYB	NEXT KEY BUFF	string	Y	32	처음 조회 시, "" 공백 입력. 다음 조회 시, 이전 조회 결과의 마지막 분봉 데이터를 이용하여, 1분 전 혹은 n분 전의 시간을 입력 (형식: YYYYMMDDHHMMSS, ex. 20241014140100)
    def get_stock_minute_chart(self):
        """해외주식분봉조회"""
        pass

url: /uapi/overseas-price/v1/quotations/inquire-time-indexchartprice
tr_id: 실전[FHKST03030200], 모의[모의투자 미지원]
arguments:
FID_COND_MRKT_DIV_CODE	조건 시장 분류 코드	string	Y	2	"N: 해외지수, X: 환율, KX: 원화환율"
FID_INPUT_ISCD	입력 종목코드	string	Y	12	종목번호(ex. TSLA)
FID_HOUR_CLS_CODE	시간 구분 코드	string	Y	5	0: 정규장, 1: 시간외
FID_PW_DATA_INCU_YN	과거 데이터 포함 여부	string	Y	2	Y/N
    def get_index_minute_chart(self):
        """해외지수분봉조회"""
        pass

url: /uapi/overseas-price/v1/quotations/dailyprice
tr_id: 실전[HHDFS76240000], 모의[HHDFS76240000]
arguments:
AUTH	사용자권한정보	string	Y	32	"" (Null 값 설정)
EXCD	거래소코드	string	Y	4	<description>HKS : 홍콩
NYS : 뉴욕
NAS : 나스닥
AMS : 아멕스
TSE : 도쿄
SHS : 상해
SZS : 심천
SHI : 상해지수
SZI : 심천지수
HSX : 호치민
HNX : 하노이</description>
SYMB	종목코드	string	Y	16	종목코드 (ex. TSLA)
GUBN	일/주/월구분	string	Y	1	0 : 일, 1 : 주, 2 : 월
BYMD	조회기준일자	string	Y	8	조회기준일자(YYYYMMDD), ※ 공란 설정 시, 기준일 오늘 날짜로 설정
MODP	수정주가반영여부	string	Y	1	0 : 미반영 1 : 반영
KEYB	NEXT KEY BUFF	string	N	1	응답시 다음값이 있으면 값이 셋팅되어 있으므로 다음 조회시 응답값 그대로 셋팅
    def get_stock_period_quote(self):
        """해외주식 기간별시세"""
        pass

url: /uapi/overseas-price/v1/quotations/inquire-daily-chartprice
tr_id: 실전[FHKST03030100], 모의[FHKST03030100]
arguments:
FID_COND_MRKT_DIV_CODE	FID 조건 시장 분류 코드	string	Y	2	N: 해외지수, X 환율, I: 국채, S:금선물
FID_INPUT_ISCD	FID 입력 종목코드	string	Y	12	<description>종목코드
※ 해외주식 마스터 코드 참조 
(포럼 > FAQ > 종목정보 다운로드(해외) > 해외지수)

※ 해당 API로 미국주식 조회 시, 다우30, 나스닥100, S&P500 종목만 조회 가능합니다. 더 많은 미국주식 종목 시세를 이용할 시에는, 해외주식기간별시세 API 사용 부탁드립니다.</description>
FID_INPUT_DATE_1	FID 입력 날짜1	string	Y	10	시작일자(YYYYMMDD)
FID_INPUT_DATE_2	FID 입력 날짜2	string	Y	10	종료일자(YYYYMMDD)
FID_PERIOD_DIV_CODE	FID 기간 분류 코드	string	Y	32	D:일, W:주, M:월, Y:년
    def get_item_index_exchange_period_price(self):
        """해외주식 종목/지수/환율기간별시세(일/주/월/년)"""
        pass

url: /uapi/overseas-price/v1/quotations/inquire-search
tr_id: 실전[HHDFS76410000], 모의[HHDFS76410000]
arguments:
AUTH	사용자권한정보	string	Y	32	"" (Null 값 설정)
EXCD	거래소코드	string	Y	4	<description>NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스 
HKS : 홍콩, SHS : 상해 , SZS : 심천
HSX : 호치민, HNX : 하노이
TSE : 도쿄</description>
CO_YN_PRICECUR	현재가선택조건	string	N	1	해당조건 사용시(1), 미사용시 필수항목아님
CO_ST_PRICECUR	현재가시작범위가	string	N	12	단위: 각국통화(JPY, USD, HKD, CNY, VND) 
CO_EN_PRICECUR	현재가끝범위가	string	N	12	단위: 각국통화(JPY, USD, HKD, CNY, VND) 
CO_YN_RATE	등락율선택조건	string	N	1	해당조건 사용시(1), 미사용시 필수항목아님
CO_ST_RATE	등락율시작율	string	N	12	%
CO_EN_RATE	등락율끝율	string	N	12	%
CO_YN_VALX	시가총액선택조건	string	N	1	해당조건 사용시(1), 미사용시 필수항목아님
CO_ST_VALX	시가총액시작액	string	N	12	단위: 천
CO_EN_VALX	시가총액끝액	string	N	12	단위: 천
CO_YN_SHAR	발행주식수선택조건	string	N	1	해당조건 사용시(1), 미사용시 필수항목아님
CO_ST_SHAR	발행주식시작수	string	N	12	단위: 천
CO_EN_SHAR	발행주식끝수	string	N	112	단위: 천
CO_YN_VOLUME	거래량선택조건	string	N	1	해당조건 사용시(1), 미사용시 필수항목아님
CO_ST_VOLUME	거래량시작량	string	N	12	단위: 주
CO_EN_VOLUME	거래량끝량	string	N	12	단위: 주
CO_YN_AMT	거래대금선택조건	string	N	1	해당조건 사용시(1), 미사용시 필수항목아님
CO_ST_AMT	거래대금시작금	string	N	12	단위: 천
CO_EN_AMT	거래대금끝금	string	N	12	단위: 천
CO_YN_EPS	EPS선택조건	string	N	1	해당조건 사용시(1), 미사용시 필수항목아님
CO_ST_EPS	EPS시작	string	N	12	
CO_EN_EPS	EPS끝	string	N	12	
CO_YN_PER	PER선택조건	string	N	1	해당조건 사용시(1), 미사용시 필수항목아님
CO_ST_PER	PER시작	string	N	12	
CO_EN_PER	PER끝	string	N	12	
KEYB	NEXT KEY BUFF	string	N	8	"" 공백 입력
    def search_by_condition(self):
        """해외주식조건검색"""
        pass

url: /uapi/overseas-stock/v1/quotations/countries-holiday
tr_id: 실전[해외주식-017], 모의[모의투자 미지원]
arguments:
TRAD_DT	기준일자	string	Y	8	기준일자(YYYYMMDD)
CTX_AREA_NK	연속조회키	string	Y	20	 공백으로 입력
CTX_AREA_FK	연속조회검색조건	string	Y	20	공백으로 입력
    def get_settlement_date(self):
        """해외결제일자조회"""
        pass

url: /uapi/overseas-price/v1/quotations/search-info
tr_id: 실전[CTPF1702R], 모의[모의투자 미지원]
PRDT_TYPE_CD	상품유형코드	string	Y	3	<description>512  미국 나스닥 / 513  미국 뉴욕 / 529  미국 아멕스 
515  일본
501  홍콩 / 543  홍콩CNY / 558  홍콩USD
507  베트남 하노이 / 508  베트남 호치민
551  중국 상해A / 552  중국 심천A,</description>
PDNO	상품번호	string	Y	12	예) AAPL (애플)
    def get_product_base_info(self):
        """해외주식 상품기본정보"""
        pass

url: /uapi/overseas-price/v1/quotations/industry-theme
tr_id: 실전[해외주식-048], 모의[모의투자 미지원]
arguments:
KEYB	NEXT KEY BUFF	string	Y	8	공백
AUTH	사용자권한정보	string	Y	32	공백
EXCD	거래소코드	string	Y	4	<description>NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스 
HKS : 홍콩, SHS : 상해 , SZS : 심천
HSX : 호치민, HNX : 하노이
TSE : 도쿄</description>
ICOD	업종코드	string	Y	1	업종코드별조회(HHDFS76370100) 를 통해 확인
VOL_RANG	거래량조건	string	Y	1	0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)
    def get_sector_price(self):
        """해외주식 업종별시세"""
        pass

url: /uapi/overseas-price/v1/quotations/industry-price
tr_id: 실전[해외주식-049], 모의[모의투자 미지원]
arguments:
AUTH	사용자권한정보	string	Y	32	공백
EXCD	거래소코드	string	Y	4	<description>NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스 
HKS : 홍콩, SHS : 상해 , SZS : 심천
HSX : 호치민, HNX : 하노이
TSE : 도쿄</description>
    def get_sector_codes(self):
        """해외주식 업종별코드조회"""
        pass
