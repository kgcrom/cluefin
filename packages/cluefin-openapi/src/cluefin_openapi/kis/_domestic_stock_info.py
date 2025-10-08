from cluefin_openapi.kis._client import Client


class DomesticStockInfo:
    """국내주식 종목정보"""

    def __init__(self, client: Client):
        self.client = client

url: /uapi/domestic-stock/v1/quotations/search-info
tr_id: CTPF1604R
arguments:
PDNO	상품번호	string	Y	12	<description>주식(하이닉스) :  000660 (코드 : 300)
선물(101S12) :  KR4101SC0009 (코드 : 301)
미국(AAPL) : AAPL (코드 : 512)</description>
PRDT_TYPE_CD	상품유형코드	string	Y	3	<description>300 주식
301 선물옵션
302 채권
512  미국 나스닥 / 513  미국 뉴욕 / 529  미국 아멕스 
515  일본
501  홍콩 / 543  홍콩CNY / 558  홍콩USD
507  베트남 하노이 / 508  베트남 호치민
551  중국 상해A / 552  중국 심천A</description>
    def get_product_basic_info(self):
        """상품기본조회"""
        pass

url: /uapi/domestic-stock/v1/quotations/search-stock-info
tr_id: CTPF1002R
arguments:
PRDT_TYPE_CD	상품유형코드	string	Y	3	<description>300: 주식, ETF, ETN, ELW
301 : 선물옵션
302 : 채권
306 : ELS</description>
PDNO	상품번호	string	Y	12	<description>종목번호 (6자리). ETN의 경우, Q로 시작 (EX. Q500001)</description>
    def get_stock_basic_info(self):
        """주식기본조회"""
        pass

url: /uapi/domestic-stock/v1/finance/balance-sheet
tr_id: FHKST66430100
arguments:
FID_DIV_CLS_CODE	분류 구분 코드	string	Y	2	0: 년, 1: 분기
fid_cond_mrkt_div_code	조건 시장 분류 코드	string	Y	2	J
fid_input_iscd	입력 종목코드	string	Y	12	000660 : 종목코드
    def get_balance_sheet(self):
        """국내주식 대차대조표"""
        pass

url: /uapi/domestic-stock/v1/finance/income-statement
tr_id: FHKST66430200
arguments:
FID_DIV_CLS_CODE	분류 구분 코드	string	Y	2	<description>0: 년, 1: 분기

※ 분기데이터는 연단위 누적합산</description>
fid_cond_mrkt_div_code	조건 시장 분류 코드	string	Y	2	J
fid_input_iscd	입력 종목코드	string	Y	12	000660 : 종목코드
    def get_income_statement(self):
        """국내주식 손익계산서"""
        pass

url: /uapi/domestic-stock/v1/finance/financial-ratio
tr_id: FHKST66430300
arguments:
FID_DIV_CLS_CODE	분류 구분 코드	string	Y	2	0: 년, 1: 분기
fid_cond_mrkt_div_code	조건 시장 분류 코드	string	Y	2	J
fid_input_iscd	입력 종목코드	string	Y	12	000660 : 종목코드
    def get_financial_ratio(self):
        """국내주식 재무비율"""
        pass

url: /uapi/domestic-stock/v1/finance/profit-ratio
tr_id: FHKST66430400
arguments:
fid_input_iscd	입력 종목코드	string	Y	12	000660 : 종목코드
FID_DIV_CLS_CODE	분류 구분 코드	string	Y	2	0: 년, 1: 분기
fid_cond_mrkt_div_code	조건 시장 분류 코드	string	Y	2	J
    def get_profitability_ratio(self):
        """국내주식 수익성비율"""
        pass

url: /uapi/domestic-stock/v1/finance/other-major-ratios
tr_id: FHKST66430500
arguments:
fid_input_iscd	입력 종목코드	string	Y	12	000660 : 종목코드
fid_div_cls_code	분류 구분 코드	string	Y	2	0: 년, 1: 분기
fid_cond_mrkt_div_code	조건 시장 분류 코드	string	Y	2	J
    def get_other_key_ratio(self):
        """국내주식 기타주요비율"""
        pass

url: /uapi/domestic-stock/v1/finance/stability-ratio
tr_id: FHKST66430600
arguments:
fid_input_iscd	입력 종목코드	string	Y	12	000660 : 종목코드
fid_div_cls_code	분류 구분 코드	string	Y	2	0: 년, 1: 분기
fid_cond_mrkt_div_code	조건 시장 분류 코드	string	Y	2	J
    def get_stability_ratio(self):
        """국내주식 안정성비율"""
        pass

url: /uapi/domestic-stock/v1/finance/growth-ratio
tr_id: FHKST66430800
arguments:
fid_input_iscd	입력 종목코드	string	Y	12	ex : 000660
fid_div_cls_code	분류 구분 코드	string	Y	2	0: 년, 1: 분기
fid_cond_mrkt_div_code	조건 시장 분류 코드	string	Y	2	시장구분코드 (주식 J)
    def get_growth_ratio(self):
        """국내주식 성장성비율"""
        pass

url: /uapi/domestic-stock/v1/quotations/credit-by-company
tr_id: FHPST04770000
arguments:
fid_rank_sort_cls_code	순위 정렬 구분 코드	string	Y	2	0:코드순, 1:이름순
fid_slct_yn	선택 여부	string	Y	1	0:신용주문가능, 1: 신용주문불가
fid_input_iscd	입력 종목코드	string	Y	12	0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100
fid_cond_scr_div_code	조건 화면 분류 코드	string	Y	5	Unique key(20477)
fid_cond_mrkt_div_code	조건 시장 분류 코드	string	Y	2	시장구분코드 (주식 J)
    def get_margin_tradable_stocks(self):
        """국내주식 당사 신용가능종목"""
        pass

url: /uapi/domestic-stock/v1/ksdinfo/dividend
tr_id: HHKDB669102C0
arguments:
CTS	CTS	string	Y	17	공백
GB1	조회구분	string	Y	1	0:배당전체, 1:결산배당, 2:중간배당
F_DT	조회일자From	string	Y	8	일자 ~
T_DT	조회일자To	string	Y	8	~ 일자
SHT_CD	종목코드	string	Y	9	공백: 전체,  특정종목 조회시 : 종목코드
HIGH_GB	고배당여부	string	Y	1	공백
    def get_ksd_dividend_decision(self):
        """예탁원정보(배당결정)"""
        pass

url: /uapi/domestic-stock/v1/ksdinfo/purreq
tr_id: HHKDB669103C0
arguments:
SHT_CD	종목코드	string	Y	9	공백: 전체,  특정종목 조회시 : 종목코드
T_DT	조회일자To	string	Y	8	~ 일자
F_DT	조회일자From	string	Y	8	일자 ~
CTS	CTS	string	Y	17	공백 
    def get_ksd_stock_dividend_decision(self):
        """예탁원정보(주식배수청구결정)"""
        pass

url: /uapi/domestic-stock/v1/ksdinfo/merger-split
tr_id: HHKDB669104C0
arguments:
CTS	CTS	string	Y	17	공백
F_DT	조회일자From	string	Y	8	일자 ~
T_DT	조회일자To	string	Y	8	~ 일자
SHT_CD	종목코드	string	Y	9	공백: 전체,  특정종목 조회시 : 종목코드
    def get_ksd_merger_split_decision(self):
        """예탁원정보(합병/분할결정)"""
        pass

url: /uapi/domestic-stock/v1/ksdinfo/rev-split
tr_id: HHKDB669105C0
arguments:
SHT_CD	종목코드	string	Y	9	공백: 전체,  특정종목 조회시 : 종목코드
CTS	CTS	string	Y	17	공백
F_DT	조회일자From	string	Y	8	일자 ~
T_DT	조회일자To	string	Y	8	~ 일자
MARKET_GB	시장구분	string	Y	1	0:전체, 1:코스피, 2:코스닥
    def get_ksd_par_value_change_decision(self):
        """예탁원정보(액면교체결정)"""
        pass

url: /uapi/domestic-stock/v1/ksdinfo/cap-dcrs
tr_id: HHKDB669106C0
arguments:
CTS	CTS	string	Y	17	공백
F_DT	조회일자From	string	Y	8	일자 ~
T_DT	조회일자To	string	Y	8	~ 일자
SHT_CD	종목코드	string	Y	9	공백: 전체,  특정종목 조회시 : 종목코드
    def get_ksd_capital_reduction_schedule(self):
        """예탁원정보(자본감소일정)"""
        pass

url: /uapi/domestic-stock/v1/ksdinfo/list-info
tr_id: HHKDB669107C0
arguments:
SHT_CD	종목코드	string	Y	9	공백: 전체,  특정종목 조회시 : 종목코드
T_DT	조회일자To	string	Y	8	~ 일자
F_DT	조회일자From	string	Y	8	일자 ~
CTS	CTS	string	Y	17	공백
    def get_ksd_listing_info_schedule(self):
        """예탁원정보(상장정보일정)"""
        pass

url: /uapi/domestic-stock/v1/ksdinfo/pub-offer
tr_id: HHKDB669108C0
arguments:
SHT_CD	종목코드	string	Y	9	공백: 전체,  특정종목 조회시 : 종목코드
CTS	CTS	string	Y	17	공백
F_DT	조회일자From	string	Y	8	일자 ~
T_DT	조회일자To	string	Y	8	~ 일자
    def get_ksd_ipo_subscription_schedule(self):
        """예탁원정보(공모주청약일정)"""
        pass

url: /uapi/domestic-stock/v1/ksdinfo/forfeit
tr_id: HHKDB669109C0
arguments:
SHT_CD	종목코드	string	Y	9	공백: 전체,  특정종목 조회시 : 종목코드
T_DT	조회일자To	string	Y	8	~ 일자
F_DT	조회일자From	string	Y	8	일자 ~
CTS	CTS	string	Y	17	공백
    def get_ksd_forfeited_share_schedule(self):
        """예탁원정보(실권주일정)"""
        pass

url: /uapi/domestic-stock/v1/ksdinfo/mand-deposit
tr_id: HHKDB669110C0
arguments:
T_DT	조회일자To	string	Y	8	~ 일자
SHT_CD	종목코드	string	Y	9	공백: 전체,  특정종목 조회시 : 종목코드
F_DT	조회일자From	string	Y	8	일자 ~
CTS	CTS	string	Y	17	공백
    def get_ksd_deposit_schedule(self):
        """예탁원정보(입무예치일정)"""
        pass

url: /uapi/domestic-stock/v1/ksdinfo/paidin-capin
tr_id: HHKDB669100C0
arguments:
CTS	CTS	string	Y	17	공백
GB1	조회구분	string	Y	1	1(청약일별), 2(기준일별)
F_DT	조회일자From	string	Y	8	일자 ~
T_DT	조회일자To	string	Y	8	~ 일자
SHT_CD	종목코드	string	Y	9	공백(전체),  특정종목 조회시(종목코드)
    def get_ksd_paid_in_capital_increase_schedule(self):
        """예탁원정보(유상증자일정)"""
        pass

url: /uapi/domestic-stock/v1/ksdinfo/bonus-issue
tr_id: HHKDB669101C0
arguments:
CTS	CTS	string	Y	17	공백 
F_DT	조회일자From	string	Y	8	일자 ~
T_DT	조회일자To	string	Y	8	~ 일자
SHT_CD	종목코드	string	Y	9	공백: 전체,  특정종목 조회시 : 종목코드
    def get_ksd_stock_dividend_schedule(self):
        """예탁원정보(무상증자일정)"""
        pass

url: /uapi/domestic-stock/v1/ksdinfo/sharehld-meet
tr_id: HHKDB669111C0
arguments:
CTS	CTS	string	Y	17	공백 
F_DT	조회일자From	string	Y	8	일자 ~
T_DT	조회일자To	string	Y	8	~ 일자
SHT_CD	종목코드	string	Y	9	공백: 전체,  특정종목 조회시 : 종목코드
    def get_ksd_shareholder_meeting_schedule(self):
        """예탁원정보(주주총회일정)"""
        pass

url: /uapi/domestic-stock/v1/quotations/estimate-perform
tr_id: HHKST668300C0
arguments:
SHT_CD	종목코드	string	Y	2	ex) 265520
    def get_estimated_earnings(self):
        """국내주식 종목추정실적"""
        pass

url: /uapi/domestic-stock/v1/quotations/lendable-by-company
tr_id: CTSC2702R
arguments:
EXCG_DVSN_CD	거래소구분코드	string	Y	2	00(전체), 02(거래소), 03(코스닥)
PDNO	상품번호	string	Y	12	공백 : 전체조회, 종목코드 입력 시 해당종목만 조회
THCO_STLN_PSBL_YN	당사대주가능여부	string	Y	1	Y
INQR_DVSN_1	조회구분1	string	Y	1	0 : 전체조회, 1: 종목코드순 정렬
CTX_AREA_FK200	연속조회검색조건200	string	Y	200	미입력 (다음조회 불가)
CTX_AREA_NK100	연속조회키100	string	Y	100	미입력 (다음조회 불가)
    def get_stock_loanable_list(self):
        """당사 대주가능 종목"""
        pass

url: /uapi/domestic-stock/v1/quotations/invest-opinion
tr_id: FHKST663300C0
arguments:
FID_COND_MRKT_DIV_CODE	조건시장분류코드	string	Y	2	J(시장 구분 코드)
FID_COND_SCR_DIV_CODE	조건화면분류코드	string	Y	5	16633(Primary key)
FID_INPUT_ISCD	입력종목코드	string	Y	12	종목코드(ex) 005930(삼성전자))
FID_INPUT_DATE_1	입력날짜1	string	Y	10	이후 ~(ex) 0020231113)
FID_INPUT_DATE_2	입력날짜2	string	Y	10	~ 이전(ex) 0020240513)
    def get_investment_opinion(self):
        """국내주식 종목투자의견"""
        pass

url: /uapi/domestic-stock/v1/quotations/invest-opbysec
tr_id: FHKST663400C0
arguments:
FID_COND_MRKT_DIV_CODE	조건시장분류코드	string	Y	2	J(시장 구분 코드)
FID_COND_SCR_DIV_CODE	조건화면분류코드	string	Y	5	16634(Primary key)
FID_INPUT_ISCD	입력종목코드	string	Y	12	회원사코드 (kis developers 포탈 사이트 포럼-> FAQ -> 종목정보 다운로드(국내) 참조)
FID_DIV_CLS_CODE	분류구분코드	string	Y	2	전체(0) 매수(1) 중립(2) 매도(3)
FID_INPUT_DATE_1	입력날짜1	string	Y	10	이후 ~
FID_INPUT_DATE_2	입력날짜2	string	Y	10	~ 이전
    def get_investment_opinion_by_brokerage(self):
        """국내주식 증권사별 투자의견"""
        pass
