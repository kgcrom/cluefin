from cluefin_openapi.kis._client import Client


class DomesticMarketAnalysis:
    """국내주식 시세분석"""

    def __init__(self, client: Client):
        self.client = client

url: /uapi/domestic-stock/v1/quotations/psearch-title
tr_id: HHKST03900300
argument:
user_id	사용자 HTS ID	String	Y	40
    def get_condition_search_list(self):
        """종목조건검색 목록조회"""
        pass

url: /uapi/domestic-stock/v1/quotations/psearch-result
tr_id: HHKST03900400
argument:
user_id	사용자 HTS ID	String	Y	40	
seq	사용자조건 키값	String	Y	10	종목조건검색 목록조회 API의 output인 'seq'을 이용 (0 부터 시작)
    def get_condition_search_result(self):
        """종목조건검색조회"""
        pass

url: /uapi/domestic-stock/v1/quotations/intstock-grouplist
tr_id: HHKCM113004C7
argument:
TYPE	관심종목구분코드	String	Y	1	Unique key(1)
FID_ETC_CLS_CODE	FID 기타 구분 코드	String	Y	2	Unique key(00)
USER_ID	사용자 ID	String	Y	16	HTS_ID 입력
    def get_watchlist_groups(self):
        """관심종목 그룹조회"""
        pass

url: /uapi/domestic-stock/v1/quotations/intstock-multprice
tr_id: FHKST11300006
argument:
FID_COND_MRKT_DIV_CODE_1	조건 시장 분류 코드1	String	Y	2	그룹별종목조회 결과 fid_mrkt_cls_code(시장구분) 1 입력
J: KRX, NX: NXT, UN: 통합
ex) J
FID_INPUT_ISCD_1	입력 종목코드1	String	Y	16	그룹별종목조회 결과 jong_code(종목코드) 1 입력
ex) 005930
FID_COND_MRKT_DIV_CODE_2	조건 시장 분류 코드2	String	Y	2	
FID_INPUT_ISCD_2	입력 종목코드2	String	Y	16	
FID_COND_MRKT_DIV_CODE_3	조건 시장 분류 코드3	String	Y	2	
FID_INPUT_ISCD_3	입력 종목코드3	String	Y	16	
FID_COND_MRKT_DIV_CODE_4	조건 시장 분류 코드4	String	Y	2	
FID_INPUT_ISCD_4	입력 종목코드4	String	Y	16	
FID_COND_MRKT_DIV_CODE_5	조건 시장 분류 코드5	String	Y	2	
FID_INPUT_ISCD_5	입력 종목코드5	String	Y	16	
FID_COND_MRKT_DIV_CODE_6	조건 시장 분류 코드6	String	Y	2	
FID_INPUT_ISCD_6	입력 종목코드6	String	Y	16	
FID_COND_MRKT_DIV_CODE_7	조건 시장 분류 코드7	String	Y	2	
FID_INPUT_ISCD_7	입력 종목코드7	String	Y	16	
FID_COND_MRKT_DIV_CODE_8	조건 시장 분류 코드8	String	Y	2	
FID_INPUT_ISCD_8	입력 종목코드8	String	Y	16	
FID_COND_MRKT_DIV_CODE_9	조건 시장 분류 코드9	String	Y	2	
FID_INPUT_ISCD_9	입력 종목코드9	String	Y	16	
FID_COND_MRKT_DIV_CODE_10	조건 시장 분류 코드10	String	Y	12	
FID_INPUT_ISCD_10	입력 종목코드10	String	Y	16	
FID_COND_MRKT_DIV_CODE_11	조건 시장 분류 코드11	String	Y	2	
FID_INPUT_ISCD_11	입력 종목코드11	String	Y	16	
FID_COND_MRKT_DIV_CODE_12	조건 시장 분류 코드12	String	Y	2	
FID_INPUT_ISCD_12	입력 종목코드12	String	Y	16	
FID_COND_MRKT_DIV_CODE_13	조건 시장 분류 코드13	String	Y	2	
FID_INPUT_ISCD_13	입력 종목코드13	String	Y	16	
FID_COND_MRKT_DIV_CODE_14	조건 시장 분류 코드14	String	Y	2	
FID_INPUT_ISCD_14	입력 종목코드14	String	Y	16	
FID_COND_MRKT_DIV_CODE_15	조건 시장 분류 코드15	String	Y	2	
FID_INPUT_ISCD_15	입력 종목코드15	String	Y	16	
FID_COND_MRKT_DIV_CODE_16	조건 시장 분류 코드16	String	Y	2	
FID_INPUT_ISCD_16	입력 종목코드16	String	Y	16	
FID_COND_MRKT_DIV_CODE_17	조건 시장 분류 코드17	String	Y	2	
FID_INPUT_ISCD_17	입력 종목코드17	String	Y	16	
FID_COND_MRKT_DIV_CODE_18	조건 시장 분류 코드18	String	Y	2	
FID_INPUT_ISCD_18	입력 종목코드18	String	Y	16	
FID_COND_MRKT_DIV_CODE_19	조건 시장 분류 코드19	String	Y	2	
FID_INPUT_ISCD_19	입력 종목코드19	String	Y	16	
FID_COND_MRKT_DIV_CODE_20	조건 시장 분류 코드20	String	Y	2	
FID_INPUT_ISCD_20	입력 종목코드20	String	Y	16	
FID_COND_MRKT_DIV_CODE_21	조건 시장 분류 코드21	String	Y	2	
FID_INPUT_ISCD_21	입력 종목코드21	String	Y	16	
FID_COND_MRKT_DIV_CODE_22	조건 시장 분류 코드22	String	Y	2	
FID_INPUT_ISCD_22	입력 종목코드22	String	Y	16	
FID_COND_MRKT_DIV_CODE_23	조건 시장 분류 코드23	String	Y	2	
FID_INPUT_ISCD_23	입력 종목코드23	String	Y	16	
FID_COND_MRKT_DIV_CODE_24	조건 시장 분류 코드24	String	Y	2	
FID_INPUT_ISCD_24	입력 종목코드24	String	Y	16	
FID_COND_MRKT_DIV_CODE_25	조건 시장 분류 코드25	String	Y	2	
FID_INPUT_ISCD_25	입력 종목코드25	String	Y	16	
FID_COND_MRKT_DIV_CODE_26	조건 시장 분류 코드26	String	Y	16	
FID_INPUT_ISCD_26	입력 종목코드26	String	Y	2	
FID_COND_MRKT_DIV_CODE_27	조건 시장 분류 코드27	String	Y	2	
FID_INPUT_ISCD_27	입력 종목코드27	String	Y	16	
FID_COND_MRKT_DIV_CODE_28	조건 시장 분류 코드28	String	Y	2	
FID_INPUT_ISCD_28	입력 종목코드28	String	Y	16	
FID_COND_MRKT_DIV_CODE_29	조건 시장 분류 코드29	String	Y	2	
FID_INPUT_ISCD_29	입력 종목코드29	String	Y	16	
FID_COND_MRKT_DIV_CODE_30	조건 시장 분류 코드30	String	Y	2	
FID_INPUT_ISCD_30	입력 종목코드30	String	Y	16
    def get_watchlist_multi_quote(self):
        """관심종목(멀티종목) 시세조회"""
        pass

url: /uapi/domestic-stock/v1/quotations/intstock-stocklist-by-group
tr_id: HHKCM113004C6
argument:
TYPE	관심종목구분코드	String	Y	1	Unique key(1)
USER_ID	사용자 ID	String	Y	16	HTS_ID 입력
DATA_RANK	데이터 순위	String	Y	10	공백
INTER_GRP_CODE	관심 그룹 코드	String	Y	3	관심그룹 조회 결과의 그룹 값 입력
INTER_GRP_NAME	관심 그룹 명	String	Y	40	공백
HTS_KOR_ISNM	HTS 한글 종목명	String	Y	40	공백
CNTG_CLS_CODE	체결 구분 코드	String	Y	1	공백
FID_ETC_CLS_CODE	기타 구분 코드	String	Y	2	Unique key(4)
    def get_watchlist_stocks_by_group(self):
        """관심종목 그룹별 종목조회"""
        pass

url: /uapi/domestic-stock/v1/quotations/intstock-stocklist-by-group
tr_id: HHKCM113004C6
argument:
TYPE	관심종목구분코드	String	Y	1	Unique key(1)
USER_ID	사용자 ID	String	Y	16	HTS_ID 입력
DATA_RANK	데이터 순위	String	Y	10	공백
INTER_GRP_CODE	관심 그룹 코드	String	Y	3	관심그룹 조회 결과의 그룹 값 입력
INTER_GRP_NAME	관심 그룹 명	String	Y	40	공백
HTS_KOR_ISNM	HTS 한글 종목명	String	Y	40	공백
CNTG_CLS_CODE	체결 구분 코드	String	Y	1	공백
FID_ETC_CLS_CODE	기타 구분 코드	String	Y	2	Unique key(4)
    def get_institutional_foreign_trading_aggregate(self):
        """국내기관_외국인 매매종목가집계"""
        pass

url: /uapi/domestic-stock/v1/quotations/foreign-institution-total
tr_id: FHPTJ04400000
argument:
FID_COND_MRKT_DIV_CODE	시장 분류 코드	String	Y	2	V(Default)
FID_COND_SCR_DIV_CODE	조건 화면 분류 코드	String	Y	5	16449(Default)
FID_INPUT_ISCD	입력 종목코드	String	Y	12	0000:전체, 0001:코스피, 1001:코스닥 ... 포탈 (FAQ : 종목정보 다운로드(국내) - 업종코드 참조)
FID_DIV_CLS_CODE	분류 구분 코드	String	Y	2	0: 수량정열, 1: 금액정열
FID_RANK_SORT_CLS_CODE	순위 정렬 구분 코드	String	Y	2	0: 순매수상위, 1: 순매도상위
FID_ETC_CLS_CODE	기타 구분 정렬	String	Y	2	0:전체 1:외국인 2:기관계 3:기타
    def get_foreign_brokerage_trading_aggregate(self):
        """외국계 매매종목 가집계"""
        pass

url: /uapi/domestic-stock/v1/quotations/frgnmem-trade-estimate
tr_id: FHKST644100C0
argument:
FID_COND_MRKT_DIV_CODE	조건시장분류코드	String	Y	2	시장구분코드 (J)
FID_COND_SCR_DIV_CODE	조건화면분류코드	String	Y	5	Uniquekey (16441)
FID_INPUT_ISCD	입력종목코드	String	Y	12	0000(전체), 1001(코스피), 2001(코스닥)
FID_RANK_SORT_CLS_CODE	순위정렬구분코드	String	Y	2	0(금액순), 1(수량순)
FID_RANK_SORT_CLS_CODE_2	순위정렬구분코드2	String	Y	2	0(매수순), 1(매도순)
    def get_investor_trading_trend_by_stock_daily(self):
        """종목별 투자자매매동향(일별)"""
        pass

url: /uapi/domestic-stock/v1/quotations/inquire-investor-time-by-market
tr_id: FHPTJ04030000
argument:
fid_input_iscd	시장구분	String	Y	12	<description>코스피: KSP, 코스닥:KSQ,
선물,콜옵션,풋옵션 : K2I, 주식선물:999,
ETF: ETF, ELW:ELW, ETN: ETN,
미니: MKI, 위클리월 : WKM, 위클리목: WKI
코스닥150: KQI</description>
fid_input_iscd_2	업종구분	String	Y	8	<description>- fid_input_iscd: KSP(코스피) 혹은 KSQ(코스닥)인 경우
코스피(0001_종합, .…0027_제조업 )
코스닥(1001_종합, …. 1041_IT부품)
...
포탈 (FAQ : 종목정보 다운로드(국내) - 업종코드 참조)

- fid_input_iscd가 K2I인 경우
F001(선물)
OC01(콜옵션)
OP01(풋옵션)

- fid_input_iscd가 999인 경우
S001(주식선물)

- fid_input_iscd가 ETF인 경우
T000(ETF)

- fid_input_iscd가 ELW인 경우
W000(ELW)

- fid_input_iscd가 ETN인 경우
E199(ETN)

- fid_input_iscd가 MKI인 경우
F004(미니선물)
OC02(미니콜옵션)
OP02(미니풋옵션)

- fid_input_iscd가 WKM인 경우
OC05(위클리콜(월))
OP05(위클리풋(월))

- fid_input_iscd가 WKI인 경우
OC04(위클리콜(목))
OP04(위클리풋(목))

- fid_input_iscd가 KQI인 경우
F002(코스닥150선물)
OC03(코스닥150콜옵션)
OP03(코스닥150풋옵션)
</description>
    def get_investor_trading_trend_by_market_intraday(self):
        """시장별 투자자매매동향(시세)"""
        pass

url: /uapi/domestic-stock/v1/quotations/inquire-investor-daily-by-market
tr_id: FHPTJ04040000
argument:
FID_COND_MRKT_DIV_CODE	조건 시장 분류 코드	String	Y	2	시장구분코드 (업종 U)
FID_INPUT_ISCD	입력 종목코드	String	Y	12	코스피, 코스닥 : 업종분류코드 (종목정보파일 - 업종코드 참조)
FID_INPUT_DATE_1	입력 날짜1	String	Y	10	ex. 20240517
FID_INPUT_ISCD_1	입력 종목코드	String	Y	12	코스피(KSP), 코스닥(KSQ)
FID_INPUT_DATE_2	입력 날짜2	String	Y	10	입력 날짜1과 동일날짜 입력
FID_INPUT_ISCD_2	하위 분류코드	String	Y	10	코스피, 코스닥 : 업종분류코드 (종목정보파일 - 업종코드 참조)
    def get_investor_trading_trend_by_market_daily(self):
        """시장별 투자자매매동향(일별)"""
        pass

url: /uapi/domestic-stock/v1/quotations/frgnmem-pchs-trend
tr_id: FHKST644400C0
argument:
FID_INPUT_ISCD	조건시장분류코드	String	Y	12	종목코드(ex) 005930(삼성전자))
FID_INPUT_ISCD_2	조건화면분류코드	String	Y	8	외국계 전체(99999)
FID_COND_MRKT_DIV_CODE	시장구분코드	String	Y	10	J (KRX만 지원)
    def get_foreign_net_buy_trend_by_stock(self):
        """종목별 외국계 순매수추이"""
        pass

url: /uapi/domestic-stock/v1/quotations/frgnmem-trade-trend
tr_id: FHPST04320000
argument:
FID_COND_SCR_DIV_CODE	화면분류코드	String	Y	5	20432(primary key)
FID_COND_MRKT_DIV_CODE	FID 조건 시장 분류 코드	String	Y	2	J 고정 입력
FID_INPUT_ISCD	종목코드	String	Y	12	ex. 005930(삼성전자) ※ FID_INPUT_ISCD(종목코드) 혹은 FID_MRKT_CLS_CODE(시장구분코드) 둘 중 하나만 입력
FID_INPUT_ISCD_2	회원사코드	String	Y	10	ex. 99999(전체) ※ 회원사코드 (kis developers 포탈 사이트 포럼-> FAQ -> 종목정보 다운로드(국내) 참조)
FID_MRKT_CLS_CODE	시장구분코드	String	Y	2	A(전체),K(코스피), Q(코스닥), K2(코스피200), W(ELW) ※ FID_INPUT_ISCD(종목코드) 혹은 FID_MRKT_CLS_CODE(시장구분코드) 둘 중 하나만 입력
FID_VOL_CNT	거래량	String	Y	12	거래량 ~
    def get_member_trading_trend_tick(self):
        """회원사 실시간 매매동향(틱)"""
        pass

url: /uapi/domestic-stock/v1/quotations/inquire-member-daily
tr_id: FHPST04540000
argument:
FID_COND_MRKT_DIV_CODE	조건시장분류코드	String	Y	2	J: KRX, NX: NXT, UN: 통합
FID_INPUT_ISCD	입력종목코드	String	Y	12	주식종목코드입력
FID_INPUT_ISCD_2	회원사코드	String	Y	8	회원사코드 (kis developers 포탈 사이트 포럼-> FAQ -> 종목정보 다운로드(국내) > 회원사 참조)
FID_INPUT_DATE_1	입력날짜1	String	Y	10	날짜 ~
FID_INPUT_DATE_2	입력날짜2	String	Y	10	~ 날짜
FID_SCTN_CLS_CODE	구간구분코드	String	Y	2	공백
    def get_member_trading_trend_by_stock(self):
        """주식현재가 회원사 종목매매동향"""
        pass

url: /uapi/domestic-stock/v1/quotations/program-trade-by-stock
tr_id: FHPPG04650101
argument:
FID_COND_MRKT_DIV_CODE	조건 시장 분류 코드	String	Y	2	KRX : J , NXT : NX, 통합 : UN
FID_INPUT_ISCD	입력 종목코드	String	Y	12	종목코드
    def get_program_trading_trend_by_stock_intraday(self):
        """종목별 프로그램매매추이(체결)"""
        pass

url: /uapi/domestic-stock/v1/quotations/program-trade-by-stock-daily
tr_id: FHPPG04650201
argument:
FID_COND_MRKT_DIV_CODE	조건 시장 분류 코드	String	Y	2	KRX : J , NXT : NX, 통합 : UN
FID_INPUT_ISCD	입력 종목코드	String	Y	12	종목코드
FID_INPUT_DATE_1	입력 날짜1	String	Y	10	기준일 (ex 0020240308), 미입력시 당일부터 조회
    def get_program_trading_trend_by_stock_daily(self):
        """종목별 프로그램매매추이(일별)"""
        pass

url: /uapi/domestic-stock/v1/quotations/investor-trend-estimate
tr_id: HHPTJ04160200
argument:
MKSC_SHRN_ISCD	종목코드	String	Y	12	종목코드
    def get_foreign_institutional_estimate_by_stock(self):
        """종목별 외인기관 추정기전계"""
        pass

url: /uapi/domestic-stock/v1/quotations/inquire-daily-trade-volume
tr_id: FHKST03010800
argument:
FID_COND_MRKT_DIV_CODE	FID 조건 시장 분류 코드	String	Y	2	J: KRX, NX: NXT, UN: 통합
FID_INPUT_ISCD	FID 입력 종목코드	String	Y	12	005930
FID_INPUT_DATE_1	FID 입력 날짜1	String	Y	10	from
FID_INPUT_DATE_2	FID 입력 날짜2	String	Y	10	to
FID_PERIOD_DIV_CODE	FID 기간 분류 코드	String	Y	32	D
    def get_buy_sell_volume_by_stock_daily(self):
        """종목별일별매수매도체결량"""
        pass

url: /uapi/domestic-stock/v1/quotations/comp-program-trade-today
tr_id: FHPPG04600101
argument:
FID_COND_MRKT_DIV_CODE	시장 분류 코드	String	Y	2	KRX : J , NXT : NX, 통합 : UN
FID_MRKT_CLS_CODE	시장 구분 코드	String	Y	2	K:코스피, Q:코스닥
FID_SCTN_CLS_CODE	구간 구분 코드	String	Y	2	공백 입력
FID_INPUT_ISCD	입력 종목코드	String	Y	12	공백 입력
FID_COND_MRKT_DIV_CODE1	시장 분류코드1	String	Y	2	공백 입력
FID_INPUT_HOUR_1	입력 시간1	String	Y	10	공백 입력
    def get_program_trading_summary_intraday(self):
        """프로그램매매 종합현황(시간)"""
        pass

url: /uapi/domestic-stock/v1/quotations/comp-program-trade-daily
tr_id: FHPPG04600001
argument:
FID_COND_MRKT_DIV_CODE	시장 분류 코드	String	Y	2	J : KRX, NX : NXT, UN : 통합
FID_MRKT_CLS_CODE	시장 구분 코드	String	Y	2	K:코스피, Q:코스닥
FID_INPUT_DATE_1	검색시작일	String	Y	10	공백 입력, 입력 시 ~ 입력일자까지 조회됨
* 8개월 이상 과거 조회 불가
FID_INPUT_DATE_2	검색종료일	String	Y	10	공백 입력
    def get_program_trading_summary_daily(self):
        """프로그램매매 종합현황(일별)"""
        pass

url: /uapi/domestic-stock/v1/quotations/investor-program-trade-today
tr_id: HHPPG046600C1
argument:
EXCH_DIV_CLS_CODE	거래소 구분 코드	String	Y	2	J : KRX, NX : NXT, UN : 통합
MRKT_DIV_CLS_CODE	시장 구분 코드	String	Y	1	1:코스피, 4:코스닥
    def get_program_trading_investor_trend_today(self):
        """프로그램매매 투자자매매동향(당일)"""
        pass

url: /uapi/domestic-stock/v1/quotations/daily-credit-balance
tr_id: FHPST04760000
argument:
fid_cond_mrkt_div_code	시장 분류 코드	String	Y	2	시장구분코드 (주식 J)
fid_cond_scr_div_code	화면 분류 코드	String	Y	5	Unique key(20476)
fid_input_iscd	종목코드	String	Y	12	종목코드 (ex 005930)
fid_input_date_1	결제일자	String	Y	10	결제일자 (ex 20240313)
    def get_credit_balance_trend_daily(self):
        """국내주식 신용잔고 일별추이"""
        pass

url: /uapi/domestic-stock/v1/quotations/exp-price-trend	
tr_id: FHPST01810000
argument:
fid_mkop_cls_code	장운영 구분 코드	string	Y	12	0:전체, 4:체결량 0 제외
fid_cond_mrkt_div_code	조건 시장 분류 코드	string	Y	2	시장구분코드 (주식 J)
fid_input_iscd	입력 종목코드	string	Y	5	종목코드(ex. 005930)
    def get_expected_price_trend(self):
        """국내주식 예상체결가 추이"""
        pass

url: /uapi/domestic-stock/v1/quotations/daily-short-sale
tr_id: FHPST04830000
argument:
FID_INPUT_DATE_2	입력 날짜2	string	Y	10	~ 누적
FID_COND_MRKT_DIV_CODE	조건 시장 분류 코드	string	Y	2	시장구분코드 (주식 J)
FID_INPUT_ISCD	입력 종목코드	string	Y	12	종목코드
FID_INPUT_DATE_1	입력 날짜1	string	Y	10	공백시 전체 (기간 ~)
    def get_short_selling_trend_daily(self):
        """국내주식 공매도 일별추이"""
        pass

url: /uapi/domestic-stock/v1/ranking/overtime-exp-trans-fluct
tr_id: FHKST11860000
argument:
FID_COND_MRKT_DIV_CODE	조건 시장 분류 코드	string	Y	2	시장구분코드 (J: 주식)
FID_COND_SCR_DIV_CODE	조건 화면 분류 코드	string	Y	5	Unique key(11186)
FID_INPUT_ISCD	입력 종목코드	string	Y	12	0000(전체), 0001(코스피), 1001(코스닥)
FID_RANK_SORT_CLS_CODE	순위 정렬 구분 코드	string	Y	2	0(상승률), 1(상승폭), 2(보합), 3(하락률), 4(하락폭)
FID_DIV_CLS_CODE	분류 구분 코드	string	Y	2	"0(전체), 1(관리종목), 2(투자주의), 3(투자경고), 4(투자위험예고), 5(투자위험), 6(보통주), 7(우선주)"
FID_INPUT_PRICE_1	입력 가격1	string	Y	12	가격 ~
FID_INPUT_PRICE_2	입력 가격2	string	Y	12	공백
FID_INPUT_VOL_1	입력 거래량	string	Y	18	거래량 ~
    def get_after_hours_expected_fluctuation(self):
        """국내주식 시간외예상체결등락율"""
        pass

url: /uapi/domestic-stock/v1/quotations/tradprt-byamt
tr_id: FHKST111900C0
argument:
FID_COND_MRKT_DIV_CODE	조건시장분류코드	string	Y	2	J: KRX, NX: NXT, UN: 통합
FID_COND_SCR_DIV_CODE	조건화면분류코드	string	Y	5	Uniquekey(11119)
FID_INPUT_ISCD	입력종목코드	string	Y	12	종목코드(ex)(005930 (삼성전자))
    def get_trading_weight_by_amount(self):
        """국내주식 체결금액별 매매비중"""
        pass

url: /uapi/domestic-stock/v1/quotations/mktfunds
tr_id: FHKST649100C0
argument:
FID_INPUT_DATE_1	입력날짜1	string	Y	10
    def get_market_fund_summary(self):
        """국내 증시자금 종합"""
        pass

url: /uapi/domestic-stock/v1/quotations/daily-loan-trans
tr_id: HHPST074500C0
argument:
MRKT_DIV_CLS_CODE	조회구분	string	Y	1	1(코스피), 2(코스닥), 3(종목)
MKSC_SHRN_ISCD	종목코드	string	Y	9	종목코드
START_DATE	조회시작일시	string	Y	8	조회기간 ~
END_DATE	조회종료일시	string	Y	8	~ 조회기간
CTS	이전조회KEY	string	Y	8
    def get_stock_loan_trend_daily(self):
        """종목별 일별 대차거래추이"""
        pass

url: /uapi/domestic-stock/v1/quotations/capture-uplowprice
tr_id: FHKST130000C0
argument:
FID_COND_MRKT_DIV_CODE	조건시장분류코드	string	Y	2	시장구분(J)
FID_COND_SCR_DIV_CODE	조건화면분류코드	string	Y	5	11300(Unique key)
FID_PRC_CLS_CODE	상하한가 구분코드	string	Y	2	0(상한가),1(하한가)
FID_DIV_CLS_CODE	분류구분코드	string	Y	2	"0(상하한가종목),6(8%상하한가 근접), 5(10%상하한가 근접), 1(15%상하한가 근접),2(20%상하한가 근접), 3(25%상하한가 근접)"
FID_INPUT_ISCD	입력종목코드	string	Y	12	 전체(0000), 코스피(0001),코스닥(1001)
FID_TRGT_CLS_CODE	대상구분코드	string	Y	32	공백 입력
FID_TRGT_EXLS_CLS_CODE	대상제외구분코드	string	Y	32	공백 입력
FID_INPUT_PRICE_1	입력가격1	string	Y	12	공백 입력
FID_INPUT_PRICE_2	입력가격2	string	Y	12	공백 입력
FID_VOL_CNT	거래량수	string	Y	12	공백 입력
    def get_limit_price_stocks(self):
        """국내주식 상하한가 표착"""
        pass

url: /uapi/domestic-stock/v1/quotations/pbar-tratio
tr_id: FHPST01130000
argument:
FID_COND_MRKT_DIV_CODE	조건시장분류코드	string	Y	2	J:KRX, NX:NXT, UN:통합
FID_INPUT_ISCD	입력종목코드	string	Y	12	주식단축종목코드
FID_COND_SCR_DIV_CODE	조건화면분류코드	string	Y	5	Uniquekey(20113)
FID_INPUT_HOUR_1	입력시간1	string	Y	10	공백
    def get_resistance_level_trading_weight(self):
        """국내주식 매물대/거래비중"""
        pass
