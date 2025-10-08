from cluefin_openapi.kis._client import Client


class DomesticRankingAnalysis:
    """국내주식 순위분석"""

    def __init__(self, client: Client):
        self.client = client

url: /uapi/domestic-stock/v1/quotations/volume-rank
tr_id: FHPST01710000
arguments:
FID_COND_MRKT_DIV_CODE	조건 시장 분류 코드	string	Y	2	J:KRX, NX:NXT
FID_COND_SCR_DIV_CODE	조건 화면 분류 코드	string	Y	5	20171
FID_INPUT_ISCD	입력 종목코드	string	Y	12	0000(전체) 기타(업종코드)
FID_DIV_CLS_CODE	분류 구분 코드	string	Y	2	0(전체) 1(보통주) 2(우선주)
FID_BLNG_CLS_CODE	소속 구분 코드	string	Y	2	0 : 평균거래량 1:거래증가율 2:평균거래회전율 3:거래금액순 4:평균거래금액회전율
FID_TRGT_CLS_CODE	대상 구분 코드	string	Y	32	1 or 0 9자리 (차례대로 증거금 30% 40% 50% 60% 100% 신용보증금 30% 40% 50% 60%), ex) "111111111"
FID_TRGT_EXLS_CLS_CODE	대상 제외 구분 코드	string	Y	32	1 or 0 10자리 (차례대로 투자위험/경고/주의 관리종목 정리매매 불성실공시 우선주 거래정지 ETF ETN 신용주문불가 SPAC) ex) "0000000000"
FID_INPUT_PRICE_1	입력 가격1	string	Y	12	<description>가격 ~. ex) "0", 전체 가격 대상 조회 시 FID_INPUT_PRICE_1, FID_INPUT_PRICE_2 모두 ""(공란) 입력</description>
FID_INPUT_PRICE_2	입력 가격2	string	Y	12	<description>~ 가격 ex) "1000000", 전체 가격 대상 조회 시 FID_INPUT_PRICE_1, FID_INPUT_PRICE_2 모두 ""(공란) 입력</description>
FID_VOL_CNT	거래량 수	string	Y	12	<description>거래량 ~ ex) "100000", 전체 거래량 대상 조회 시 FID_VOL_CNT ""(공란) 입력</description>
FID_INPUT_DATE_1	입력 날짜1	string	Y	10	(공란) 입력
    def get_trading_volume_rank(self):
        """거래량순위"""
        pass

url: /uapi/domestic-stock/v1/ranking/fluctuation
tr_id: FHPST01700000
arguments:
fid_rsfl_rate2	등락 비율2	string	Y	132	공백 입력 시 전체 (~ 비율
fid_cond_mrkt_div_code	조건 시장 분류 코드	string	Y	2	시장구분코드 (J:KRX, NX:NXT)
fid_cond_scr_div_code	조건 화면 분류 코드	string	Y	5	Unique key( 20170 )
fid_input_iscd	입력 종목코드	string	Y	12	0000(전체) 코스피(0001), 코스닥(1001), 코스피200(2001)
fid_rank_sort_cls_code	순위 정렬 구분 코드	string	Y	2	0:상승율순 1:하락율순 2:시가대비상승율 3:시가대비하락율 4:변동율
fid_input_cnt_1	입력 수1	string	Y	12	0:전체 , 누적일수 입력
fid_prc_cls_code	가격 구분 코드	string	Y	2	"'fid_rank_sort_cls_code :0 상승율 순일때 (0:저가대비, 1:종가대비)
fid_rank_sort_cls_code :1 하락율 순일때 (0:고가대비, 1:종가대비)
fid_rank_sort_cls_code : 기타 (0:전체)'"
fid_input_price_1	입력 가격1	string	Y	12	공백 입력 시 전체 (가격 ~)
fid_input_price_2	입력 가격2	string	Y	12	공백 입력 시 전체 (~ 가격)
fid_vol_cnt	거래량 수	string	Y	12	공백 입력 시 전체 (거래량 ~)
fid_trgt_cls_code	대상 구분 코드	string	Y	32	0:전체
fid_trgt_exls_cls_code	대상 제외 구분 코드	string	Y	32	0:전체
fid_div_cls_code	분류 구분 코드	string	Y	2	0:전체
fid_rsfl_rate1	등락 비율1	string	Y	132	공백 입력 시 전체 (비율 ~)
    def get_stock_fluctuation_rank(self):
        """국내주식 등락률 순위"""
        pass

url: /uapi/domestic-stock/v1/ranking/quote-balance
tr_id: FHPST01720000
arguments:
fid_vol_cnt	거래량 수	string	Y	12	입력값 없을때 전체 (거래량 ~)
fid_cond_mrkt_div_code	조건 시장 분류 코드	string	Y	2	시장구분코드 (J:KRX, NX:NXT)
fid_cond_scr_div_code	조건 화면 분류 코드	string	Y	5	Unique key( 20172 )
fid_input_iscd	입력 종목코드	string	Y	12	0000(전체) 코스피(0001), 코스닥(1001), 코스피200(2001)
fid_rank_sort_cls_code	순위 정렬 구분 코드	string	Y	2	0: 순매수잔량순, 1:순매도잔량순, 2:매수비율순, 3:매도비율순
fid_div_cls_code	분류 구분 코드	string	Y	2	0:전체
fid_trgt_cls_code	대상 구분 코드	string	Y	32	0:전체
fid_trgt_exls_cls_code	대상 제외 구분 코드	string	Y	32	0:전체
fid_input_price_1	입력 가격1	string	Y	12	입력값 없을때 전체 (가격 ~)
fid_input_price_2	입력 가격2	string	Y	12	입력값 없을때 전체 (~ 가격)
    def get_stock_hoga_quantity_rank(self):
        """국내주식 호가잔량 순위"""
        pass

url: /uapi/domestic-stock/v1/ranking/profit-asset-index
tr_id: FHPST01730000
arguments:
fid_cond_mrkt_div_code	조건 시장 분류 코드	string	Y	2	시장구분코드 (J:KRX, NX:NXT)
fid_trgt_cls_code	대상 구분 코드	string	Y	32	0:전체
fid_cond_scr_div_code	조건 화면 분류 코드	string	Y	5	Unique key( 20173 )
fid_input_iscd	입력 종목코드	string	Y	12	0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200
fid_div_cls_code	분류 구분 코드	string	Y	2	0:전체
fid_input_price_1	입력 가격1	string	Y	12	입력값 없을때 전체 (가격 ~)
fid_input_price_2	입력 가격2	string	Y	12	입력값 없을때 전체 (~ 가격)
fid_vol_cnt	거래량 수	string	Y	12	입력값 없을때 전체 (거래량 ~)
fid_input_option_1	입력 옵션1	string	Y	10	회계연도 (2023)
fid_input_option_2	입력 옵션2	string	Y	10	0: 1/4분기 , 1: 반기, 2: 3/4분기, 3: 결산
fid_rank_sort_cls_code	순위 정렬 구분 코드	string	Y	2	0:매출이익 1:영업이익 2:경상이익 3:당기순이익 4:자산총계 5:부채총계 6:자본총계
fid_blng_cls_code	소속 구분 코드	string	Y	2	0:전체
fid_trgt_exls_cls_code	대상 제외 구분 코드	string	Y	32	0:전체
    def get_stock_profitability_indicator_rank(self):
        """국내주식 수익자산지표 순위"""
        pass

url: /uapi/domestic-stock/v1/ranking/market-cap
tr_id: FHPST01740000
arguments:
fid_input_price_2	입력 가격2	string	Y	12	입력값 없을때 전체 (~ 가격)
fid_cond_mrkt_div_code	조건 시장 분류 코드	string	Y	2	시장구분코드 (J:KRX, NX:NXT)
fid_cond_scr_div_code	조건 화면 분류 코드	string	Y	5	Unique key( 20174 )
fid_div_cls_code	분류 구분 코드	string	Y	2	0: 전체,  1:보통주,  2:우선주
fid_input_iscd	입력 종목코드	string	Y	12	0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200
fid_trgt_cls_code	대상 구분 코드	string	Y	32	0 : 전체
fid_trgt_exls_cls_code	대상 제외 구분 코드	string	Y	32	0 : 전체
fid_input_price_1	입력 가격1	string	Y	12	입력값 없을때 전체 (가격 ~)
fid_vol_cnt	거래량 수	string	Y	12	입력값 없을때 전체 (거래량 ~)
    def get_stock_market_cap_top(self):
        """국내주식 시가총액 상위"""
        pass

url: /uapi/domestic-stock/v1/ranking/finance-ratio
tr_id: FHPST01750000
arguments:
fid_trgt_cls_code	대상 구분 코드	string	Y	32	0 : 전체
fid_cond_mrkt_div_code	조건 시장 분류 코드	string	Y	2	시장구분코드 (J:KRX, NX:NXT)
fid_cond_scr_div_code	조건 화면 분류 코드	string	Y	5	Unique key( 20175 )
fid_input_iscd	입력 종목코드	string	Y	12	0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200
fid_div_cls_code	분류 구분 코드	string	Y	2	0 : 전체
fid_input_price_1	입력 가격1	string	Y	12	입력값 없을때 전체 (가격 ~)
fid_input_price_2	입력 가격2	string	Y	12	입력값 없을때 전체 (~ 가격)
fid_vol_cnt	거래량 수	string	Y	12	입력값 없을때 전체 (거래량 ~)
fid_input_option_1	입력 옵션1	string	Y	10	회계년도 입력 (ex 2023)
fid_input_option_2	입력 옵션2	string	Y	10	0: 1/4분기 , 1: 반기, 2: 3/4분기, 3: 결산
fid_rank_sort_cls_code	순위 정렬 구분 코드	string	Y	2	7: 수익성 분석, 11 : 안정성 분석, 15: 성장성 분석, 20: 활동성 분석
fid_blng_cls_code	소속 구분 코드	string	Y	2	0
fid_trgt_exls_cls_code	대상 제외 구분 코드	string	Y	32	0 : 전체
    def get_stock_finance_ratio_rank(self):
        """국내주식 재무비율 순위"""
        pass

url: /uapi/domestic-stock/v1/ranking/after-hour-balance
tr_id: FHPST01760000
arguments:
fid_input_price_1	입력 가격1	string	Y	12	입력값 없을때 전체 (가격 ~)
fid_cond_mrkt_div_code	조건 시장 분류 코드	string	Y	2	시장구분코드 (주식 J)
fid_cond_scr_div_code	조건 화면 분류 코드	string	Y	5	Unique key( 20176 )
fid_rank_sort_cls_code	순위 정렬 구분 코드	string	Y	2	1: 장전 시간외, 2: 장후 시간외, 3:매도잔량, 4:매수잔량
fid_div_cls_code	분류 구분 코드	string	Y	2	0 : 전체
fid_input_iscd	입력 종목코드	string	Y	12	0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200
fid_trgt_exls_cls_code	대상 제외 구분 코드	string	Y	32	0 : 전체
fid_trgt_cls_code	대상 구분 코드	string	Y	32	0 : 전체
fid_vol_cnt	거래량 수	string	Y	12	입력값 없을때 전체 (거래량 ~)
fid_input_price_2	입력 가격2	string	Y	12	입력값 없을때 전체 (~ 가격)
    def get_stock_time_hoga_rank(self):
        """국내주식 시간외잔량 순위"""
        pass

url: /uapi/domestic-stock/v1/ranking/prefer-disparate-ratio
tr_id: FHPST01770000
arguments:
fid_vol_cnt	거래량 수	string	Y	12	입력값 없을때 전체 (거래량 ~)
fid_cond_mrkt_div_code	조건 시장 분류 코드	string	Y	2	시장구분코드 (J:KRX, NX:NXT)
fid_cond_scr_div_code	조건 화면 분류 코드	string	Y	5	Unique key( 20177 )
fid_div_cls_code	분류 구분 코드	string	Y	2	0: 전체 
fid_input_iscd	입력 종목코드	string	Y	12	0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200
fid_trgt_cls_code	대상 구분 코드	string	Y	32	0 : 전체
fid_trgt_exls_cls_code	대상 제외 구분 코드	string	Y	32	0 : 전체
fid_input_price_1	입력 가격1	string	Y	12	입력값 없을때 전체 (가격 ~)
fid_input_price_2	입력 가격2	string	Y	12	입력값 없을때 전체 (~ 가격)
    def get_stock_preferred_stock_ratio_top(self):
        """국내주식 우선주/리리율 상위"""
        pass

url: /uapi/domestic-stock/v1/ranking/disparity
tr_id: FHPST01780000
arguments:
fid_input_price_2	입력 가격2	string	Y	12	입력값 없을때 전체 (~ 가격)
fid_cond_mrkt_div_code	조건 시장 분류 코드	string	Y	2	시장구분코드 (J:KRX, NX:NXT)
fid_cond_scr_div_code	조건 화면 분류 코드	string	Y	5	Unique key( 20178 )
fid_div_cls_code	분류 구분 코드	string	Y	2	0: 전체, 1:관리종목, 2:투자주의, 3:투자경고, 4:투자위험예고, 5:투자위험, 6:보톧주, 7:우선주
fid_rank_sort_cls_code	순위 정렬 구분 코드	string	Y	2	0: 이격도상위순, 1:이격도하위순
fid_hour_cls_code	시간 구분 코드	string	Y	5	5:이격도5, 10:이격도10, 20:이격도20, 60:이격도60, 120:이격도120
fid_input_iscd	입력 종목코드	string	Y	12	0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200
fid_trgt_cls_code	대상 구분 코드	string	Y	32	0 : 전체
fid_trgt_exls_cls_code	대상 제외 구분 코드	string	Y	32	0 : 전체
fid_input_price_1	입력 가격1	string	Y	12	입력값 없을때 전체 (가격 ~)
fid_vol_cnt	거래량 수	string	Y	12	입력값 없을때 전체 (거래량 ~)
    def get_stock_disparity_index_rank(self):
        """국내주식 이격도 순위"""
        pass

url: /uapi/domestic-stock/v1/ranking/market-value
tr_id: FHPST01790000
arguments:
fid_trgt_cls_code	대상 구분 코드	string	Y	32	0 : 전체
fid_cond_mrkt_div_code	조건 시장 분류 코드	string	Y	2	시장구분코드 (J:KRX, NX:NXT)
fid_cond_scr_div_code	조건 화면 분류 코드	string	Y	5	Unique key( 20179 )
fid_input_iscd	입력 종목코드	string	Y	12	0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200
fid_div_cls_code	분류 구분 코드	string	Y	2	0: 전체, 1:관리종목, 2:투자주의, 3:투자경고, 4:투자위험예고, 5:투자위험, 6:보톧주, 7:우선주
fid_input_price_1	입력 가격1	string	Y	12	입력값 없을때 전체 (가격 ~)
fid_input_price_2	입력 가격2	string	Y	12	입력값 없을때 전체 (~ 가격)
fid_vol_cnt	거래량 수	string	Y	12	입력값 없을때 전체 (거래량 ~)
fid_input_option_1	입력 옵션1	string	Y	10	회계연도 입력 (ex 2023)
fid_input_option_2	입력 옵션2	string	Y	10	0: 1/4분기 , 1: 반기, 2: 3/4분기, 3: 결산
fid_rank_sort_cls_code	순위 정렬 구분 코드	string	Y	2	"'가치분석(23:PER, 24:PBR, 25:PCR, 26:PSR, 27: EPS, 28:EVA, 29: EBITDA, 30: EV/EBITDA, 31:EBITDA/금융비율'"
fid_blng_cls_code	소속 구분 코드	string	Y	2	0 : 전체
fid_trgt_exls_cls_code	대상 제외 구분 코드	string	Y	32	0 : 전체
    def get_stock_market_price_rank(self):
        """국내주식 시장가치 순위"""
        pass

url: /uapi/domestic-stock/v1/ranking/volume-power
tr_id: FHPST01680000
arguments:
fid_trgt_exls_cls_code	대상 제외 구분 코드	string	Y	10	0 : 전체
fid_cond_mrkt_div_code	조건 시장 분류 코드	string	Y	2	시장구분코드 (J:KRX, NX:NXT)
fid_cond_scr_div_code	조건 화면 분류 코드	string	Y	5	Unique key( 20168 )
fid_input_iscd	입력 종목코드	string	Y	12	0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200
fid_div_cls_code	분류 구분 코드	string	Y	2	0: 전체,  1: 보통주 2: 우선주
fid_input_price_1	입력 가격1	string	Y	12	입력값 없을때 전체 (가격 ~)
fid_input_price_2	입력 가격2	string	Y	12	입력값 없을때 전체 (~ 가격)
fid_vol_cnt	거래량 수	string	Y	12	입력값 없을때 전체 (거래량 ~)
fid_trgt_cls_code	대상 구분 코드	string	Y	10	0 : 전체
    def get_stock_execution_strength_top(self):
        """국내주식 체결강도 상위"""
        pass

url: /uapi/domestic-stock/v1/ranking/top-interest-stock
tr_id: FHPST01800000
arguments:
fid_input_iscd_2	입력 필수값2	string	Y	12	000000 : 필수입력값
fid_cond_mrkt_div_code	조건 시장 분류 코드	string	Y	2	시장구분코드 (J:KRX, NX:NXT)
fid_cond_scr_div_code	조건 화면 분류 코드	string	Y	5	Unique key(20180)
fid_input_iscd	업종 코드	string	Y	12	0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200
fid_trgt_cls_code	대상 구분 코드	string	Y	2	0 : 전체
fid_trgt_exls_cls_code	대상 제외 구분 코드	string	Y	2	0 : 전체
fid_input_price_1	입력 가격1	string	Y	2	입력값 없을때 전체 (가격 ~)
fid_input_price_2	입력 가격2	string	Y	2	입력값 없을때 전체 (~ 가격)
fid_vol_cnt	거래량 수	string	Y	12	입력값 없을때 전체 (거래량 ~)
fid_div_cls_code	분류 구분 코드	string	Y	12	0: 전체 1: 관리종목 2: 투자주의 3: 투자경고 4: 투자위험예고 5: 투자위험 6: 보통주 7: 우선주
fid_input_cnt_1	순위 입력값	string	Y	10	순위검색 입력값(1: 1위부터, 10:10위부터)
    def get_stock_watchlist_registration_top(self):
        """국내주식 관심종목등록 상위"""
        pass

url: /uapi/domestic-stock/v1/ranking/exp-trans-updown
tr_id: FHPST01820000
arguments:
fid_rank_sort_cls_code	순위 정렬 구분 코드	string	Y	2	0:상승률1:상승폭2:보합3:하락율4:하락폭5:체결량6:거래대금
fid_cond_mrkt_div_code	조건 시장 분류 코드	string	Y	2	시장구분코드 (주식 J)
fid_cond_scr_div_code	조건 화면 분류 코드	string	Y	5	Unique key(20182)
fid_input_iscd	입력 종목코드	string	Y	12	0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100
fid_div_cls_code	분류 구분 코드	string	Y	2	0:전체 1:보통주 2:우선주
fid_aply_rang_prc_1	적용 범위 가격1	string	Y	18	입력값 없을때 전체 (가격 ~)
fid_vol_cnt	거래량 수	string	Y	12	입력값 없을때 전체 (거래량 ~)
fid_pbmn	거래대금	string	Y	18	입력값 없을때 전체 (거래대금 ~) 천원단위
fid_blng_cls_code	소속 구분 코드	string	Y	2	0: 전체
fid_mkop_cls_code	장운영 구분 코드	string	Y	2	0:장전예상1:장마감예상
    def get_stock_expected_execution_rise_decline_top(self):
        """국내주식 예상체결 상승/하락상위"""
        pass

url: /uapi/domestic-stock/v1/ranking/traded-by-company
tr_id: FHPST01860000
arguments:
fid_trgt_exls_cls_code	대상 제외 구분 코드	string	Y	32	0: 전체
fid_cond_mrkt_div_code	조건 시장 분류 코드	string	Y	2	시장구분코드 (J:KRX, NX:NXT)
fid_cond_scr_div_code	조건 화면 분류 코드	string	Y	5	Unique key(20186)
fid_div_cls_code	분류 구분 코드	string	Y	2	0:전체, 1:관리종목, 2:투자주의, 3:투자경고, 4:투자위험예고, 5:투자위험, 6:보통주, 7:우선주
fid_rank_sort_cls_code	순위 정렬 구분 코드	string	Y	2	0:매도상위,1:매수상위
fid_input_date_1	입력 날짜1	string	Y	10	기간~
fid_input_date_2	입력 날짜2	string	Y	10	~기간
fid_input_iscd	입력 종목코드	string	Y	12	0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100
fid_trgt_cls_code	대상 구분 코드	string	Y	32	0: 전체
fid_aply_rang_vol	적용 범위 거래량	string	Y	18	0: 전체, 100: 100주 이상
fid_aply_rang_prc_2	적용 범위 가격2	string	Y	18	~ 가격
fid_aply_rang_prc_1	적용 범위 가격1	string	Y	18	가격 ~
    def get_stock_proprietary_trading_top(self):
        """국내주식 당사매매종목 상위"""
        pass

url: /uapi/domestic-stock/v1/ranking/near-new-highlow
tr_id: FHPST01870000
arguments:
fid_aply_rang_vol	적용 범위 거래량	string	Y	18	0: 전체, 100: 100주 이상
fid_cond_mrkt_div_code	조건 시장 분류 코드	string	Y	2	시장구분코드 (주식 J)
fid_cond_scr_div_code	조건 화면 분류 코드	string	Y	5	Unique key(20187)
fid_div_cls_code	분류 구분 코드	string	Y	2	0:전체, 1:관리종목, 2:투자주의, 3:투자경고
fid_input_cnt_1	입력 수1	string	Y	2	괴리율 최소
fid_input_cnt_2	입력 수2	string	Y	10	괴리율 최대
fid_prc_cls_code	가격 구분 코드	string	Y	10	0:신고근접, 1:신저근접
fid_input_iscd	 입력 종목코드	string	Y	12	0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100
fid_trgt_cls_code	대상 구분 코드	string	Y	32	0: 전체
fid_trgt_exls_cls_code	대상 제외 구분 코드	string	Y	32	0:전체, 1:관리종목, 2:투자주의, 3:투자경고, 4:투자위험예고, 5:투자위험, 6:보통주, 7:우선주
fid_aply_rang_prc_1	적용 범위 가격1	string	Y	18	가격 ~
fid_aply_rang_prc_2	적용 범위 가격2	string	Y	18	~ 가격
    def get_stock_new_high_low_approaching_top(self):
        """국내주식 신고/신저근접종목 상위"""
        pass

url: /uapi/domestic-stock/v1/ranking/dividend-rate
tr_id: HHKDB13470100
arguments:
CTS_AREA	CTS_AREA	string	Y	17	공백
GB1	KOSPI	string	Y	1	0:전체, 1:코스피,  2: 코스피200, 3: 코스닥,
UPJONG	업종구분	string	Y	4	<description>코스피(0001:종합, 0002:대형주.…0027:제조업 ), 코스닥(1001:종합, …. 1041:IT부품 코스피200 (2001:KOSPI200, 2007:KOSPI100, 2008:KOSPI50)</description>
GB2	종목선택	string	Y	1	0:전체, 6:보통주, 7:우선주
GB3	배당구분	string	Y	1	1:주식배당, 2: 현금배당
F_DT	기준일From	string	Y	8	 
T_DT	기준일To	string	Y	8	 
GB4	결산/중간배당	string	Y	1	0:전체, 1:결산배당, 2:중간배당
    def get_stock_dividend_yield_top(self):
        """국내주식 배당률 상위"""
        pass

url: /uapi/domestic-stock/v1/ranking/bulk-trans-num
tr_id: HHKST1909000C0
arguments:
fid_aply_rang_prc_2	적용 범위 가격2	string	Y	18	~ 가격
fid_cond_mrkt_div_code	조건 시장 분류 코드	string	Y	2	시장구분코드 (J:KRX, NX:NXT)
fid_cond_scr_div_code	조건 화면 분류 코드	string	Y	5	Unique key(11909)
fid_input_iscd	입력 종목코드	string	Y	12	0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100
fid_rank_sort_cls_code	순위 정렬 구분 코드	string	Y	2	0:매수상위, 1:매도상위
fid_div_cls_code	분류 구분 코드	string	Y	2	0:전체
fid_input_price_1	입력 가격1	string	Y	12	건별금액 ~
fid_aply_rang_prc_1	적용 범위 가격1	string	Y	18	가격 ~
fid_input_iscd_2	입력 종목코드2	string	Y	8	공백:전체종목, 개별종목 조회시 종목코드 (000660)
fid_trgt_exls_cls_code	대상 제외 구분 코드	string	Y	32	0:전체
fid_trgt_cls_code	대상 구분 코드	string	Y	32	0:전체
fid_vol_cnt	 거래량 수	string	Y	12	거래량 ~
    def get_stock_large_execution_count_top(self):
        """국내주식 대량체결건수 상위"""
        pass

url: /uapi/domestic-stock/v1/ranking/credit-balance
tr_id: HHKST17010000
arguments:
FID_COND_SCR_DIV_CODE	조건 화면 분류 코드	string	Y	5	Unique key(11701)
FID_INPUT_ISCD	입력 종목코드	string	Y	12	0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 
FID_OPTION	증가율기간	string	Y	5	2~999
FID_COND_MRKT_DIV_CODE	조건 시장 분류 코드	string	Y	2	시장구분코드 (주식 J)
FID_RANK_SORT_CLS_CODE	순위 정렬 구분 코드	string	Y	2	<description>(융자)0:잔고비율 상위, 1: 잔고수량 상위, 2: 잔고금액 상위, 3: 잔고비율 증가상위, 4: 잔고비율 감소상위 (대주), 5:잔고비율 상위, 6: 잔고수량 상위, 7: 잔고금액 상위, 8: 잔고비율 증가상위, 9: 잔고비율 감소상위 </definition>
    def get_stock_credit_balance_top(self):
        """국내주식 신용잔고 상위"""
        pass

url: /uapi/domestic-stock/v1/ranking/short-sale
tr_id: FHPST04820000
arguments:
FID_APLY_RANG_VOL	FID 적용 범위 거래량	string	Y	18	공백
FID_COND_MRKT_DIV_CODE	조건 시장 분류 코드	string	Y	2	시장구분코드 (주식 J)
FID_COND_SCR_DIV_CODE	조건 화면 분류 코드	string	Y	5	Unique key(20482)
FID_INPUT_ISCD	입력 종목코드	string	Y	12	0000:전체, 0001:코스피, 1001:코스닥, 2001:코스피200, 4001: KRX100, 3003: 코스닥150
FID_PERIOD_DIV_CODE	조회구분 (일/월)	string	Y	32	조회구분 (일/월) D: 일, M:월
FID_INPUT_CNT_1	조회가간(일수	string	Y	12	<description>조회가간(일수): 조회구분(D) 0:1일, 1:2일, 2:3일, 3:4일, 4:1주일, 9:2주일, 14:3주일, 조회구분(M) 1:1개월,  2:2개월, 3:3개월</description>
FID_TRGT_EXLS_CLS_CODE	대상 제외 구분 코드	string	Y	32	공백
FID_TRGT_CLS_CODE	FID 대상 구분 코드	string	Y	32	공백
FID_APLY_RANG_PRC_1	FID 적용 범위 가격1	string	Y	18	가격 ~
FID_APLY_RANG_PRC_2	FID 적용 범위 가격2	string	Y	18	~ 가격
    def get_stock_short_selling_top(self):
        """국내주식 공매도 상위종목"""
        pass

url: /uapi/domestic-stock/v1/ranking/overtime-fluctuation
tr_id: FHPST02340000
arguments:
FID_COND_MRKT_DIV_CODE	조건 시장 분류 코드	string	Y	2	시장구분코드 (J: 주식)
FID_MRKT_CLS_CODE	시장 구분 코드	string	Y	2	공백 입력
FID_COND_SCR_DIV_CODE	조건 화면 분류 코드	string	Y	5	Unique key(20234)
FID_INPUT_ISCD	입력 종목코드	string	Y	12	0000(전체), 0001(코스피), 1001(코스닥)
FID_DIV_CLS_CODE	분류 구분 코드	string	Y	2	1(상한가), 2(상승률), 3(보합),4(하한가),5(하락률)
FID_INPUT_PRICE_1	입력 가격1	string	Y	12	입력값 없을때 전체 (가격 ~)
FID_INPUT_PRICE_2	입력 가격2	string	Y	12	입력값 없을때 전체 (~ 가격)
FID_VOL_CNT	거래량 수	string	Y	12	입력값 없을때 전체 (거래량 ~)
FID_TRGT_CLS_CODE	대상 구분 코드	string	Y	32	공백 입력
FID_TRGT_EXLS_CLS_CODE	대상 제외 구분 코드	string	Y	32	공백 입력
    def get_stock_after_hours_fluctuation_rank(self):
        """국내주식 시간외등락율순위"""
        pass

url: /uapi/domestic-stock/v1/ranking/overtime-volume
tr_id: FHPST02350000
arguments:
FID_COND_MRKT_DIV_CODE	조건 시장 분류 코드	string	Y	2	시장구분코드 (J: 주식)
FID_COND_SCR_DIV_CODE	조건 화면 분류 코드	string	Y	5	Unique key(20235)
FID_INPUT_ISCD	입력 종목코드	string	Y	12	0000(전체), 0001(코스피), 1001(코스닥)
FID_RANK_SORT_CLS_CODE	순위 정렬 구분 코드	string	Y	2	0(매수잔량),  1(매도잔량), 2(거래량)
FID_INPUT_PRICE_1	입력 가격1	string	Y	12	가격 ~
FID_INPUT_PRICE_2	입력 가격2	string	Y	12	~ 가격
FID_VOL_CNT	거래량 수	string	Y	12	거래량 ~
FID_TRGT_CLS_CODE	대상 구분 코드	string	Y	32	공백
FID_TRGT_EXLS_CLS_CODE	대상 제외 구분 코드	string	Y	32	공백
    def get_stock_after_hours_volume_rank(self):
        """국내주식 시간외거래량순위"""
        pass

url: /uapi/domestic-stock/v1/ranking/hts-top-view
tr_id: HHMCM000100C0
arguments:

    def get_hts_inquiry_top_20(self):
        """HTS조회상위20종목"""
        pass
