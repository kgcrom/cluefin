from typing import Sequence
from pydantic import BaseModel, Field


user_id	HTS ID	String	Y	40	
seq	조건키값	String	Y	10	해당 값을 종목조건검색조회 API의 input으로 사용 (0번부터 시작)
grp_nm	그룹명	String	Y	40	HTS(eFriend Plus) [0110] "사용자조건검색"화면을 통해
등록한 사용자조건 그룹
condition_nm	조건명	String	Y	40	등록한 사용자 조건명
class ConditionSearchListItem(BaseModel):
    pass


class ConditionSearchList(BaseModel):
    """종목조건검색 목록조회"""

    output2: Sequence[ConditionSearchListItem] = Field(default_factory=list)

code	종목코드	String	Y	6	
name	종목명	String	Y	20	
daebi	전일대비부호	String	Y	1	1. 상한 2. 상승 3. 보합 4. 하한 5. 하락
price	현재가	String	Y	16	
chgrate	등락율	String	Y	16	
acml_vol	거래량	String	Y	16	
trade_amt	거래대금	String	Y	16	
change	전일대비	String	Y	16	
cttr	체결강도	String	Y	16	
open	시가	String	Y	16	
high	고가	String	Y	16	
low	저가	String	Y	16	
high52	52주최고가	String	Y	16	
low52	52주최저가	String	Y	16	
expprice	예상체결가	String	Y	16	
expchange	예상대비	String	Y	16	
expchggrate	예상등락률	String	Y	16	
expcvol	예상체결수량	String	Y	16	
chgrate2	전일거래량대비율	String	Y	16	
expdaebi	예상대비부호	String	Y	1	
recprice	기준가	String	Y	16	
uplmtprice	상한가	String	Y	16	
dnlmtprice	하한가	String	Y	16	
stotprice	시가총액	String	Y	16
class ConditionSearchResultItem(BaseModel):
    pass


class ConditionSearchResult(BaseModel):
    """종목조건검색조회"""

    output2: Sequence[ConditionSearchResultItem] = Field(default_factory=list)


date	일자	String	Y	8	
trnm_hour	전송 시간	String	Y	6	
data_rank	데이터 순위	String	Y	10	
inter_grp_code	관심 그룹 코드	String	Y	3	
inter_grp_name	관심 그룹 명	String	Y	40	
ask_cnt	요청 개수	String	Y	4
class WatchlistGroupsItem(BaseModel):
    pass

class WatchlistGroups(BaseModel):
    """관심종목 그룹조회"""

    output2: WatchlistGroupsItem = Field(title="응답상세")

kospi_kosdaq_cls_name	코스피 코스닥 구분 명	String	Y	10	
mrkt_trtm_cls_name	시장 조치 구분 명	String	Y	10	
hour_cls_code	시간 구분 코드	String	Y	1	
inter_shrn_iscd	관심 단축 종목코드	String	Y	16	
inter_kor_isnm	관심 한글 종목명	String	Y	40	
inter2_prpr	관심2 현재가	String	Y	11	
inter2_prdy_vrss	관심2 전일 대비	String	Y	11	
prdy_vrss_sign	전일 대비 부호	String	Y	1	
prdy_ctrt	전일 대비율	String	Y	82	
acml_vol	누적 거래량	String	Y	18	
inter2_oprc	관심2 시가	String	Y	11	
inter2_hgpr	관심2 고가	String	Y	11	
inter2_lwpr	관심2 저가	String	Y	11	
inter2_llam	관심2 하한가	String	Y	11	
inter2_mxpr	관심2 상한가	String	Y	11	
inter2_askp	관심2 매도호가	String	Y	11	
inter2_bidp	관심2 매수호가	String	Y	11	
seln_rsqn	매도 잔량	String	Y	12	
shnu_rsqn	매수2 잔량	String	Y	12	
total_askp_rsqn	총 매도호가 잔량	String	Y	12	
total_bidp_rsqn	총 매수호가 잔량	String	Y	12	
acml_tr_pbmn	누적 거래 대금	String	Y	18	
inter2_prdy_clpr	관심2 전일 종가	String	Y	11	
oprc_vrss_hgpr_rate	시가 대비 최고가 비율	String	Y	84	
intr_antc_cntg_vrss	관심 예상 체결 대비	String	Y	11	
intr_antc_cntg_vrss_sign	관심 예상 체결 대비 부호	String	Y	1	
intr_antc_cntg_prdy_ctrt	관심 예상 체결 전일 대비율	String	Y	72	
intr_antc_vol	관심 예상 거래량	String	Y	18	
inter2_sdpr	관심2 기준가	String	Y	11	
class WatchlistMultiQuoteItem(BaseModel):
    pass


class WatchlistMultiQuote(BaseModel):
    """관심종목(멀티종목) 시세조회"""

    output: WaatchlistMultiQuoteItem = Field(title="응답상세")


data_rank	데이터 순위	String	Y	10	
inter_grp_name	관심 그룹 명	String	Y	40	
class WatchlistStocksByGroupItem1(BaseModel):
    pass

fid_mrkt_cls_code	FID 시장 구분 코드	String	Y	2	
data_rank	데이터 순위	String	Y	10	
exch_code	거래소코드	String	Y	4	
jong_code	종목코드	String	Y	16	
color_code	생상 코드	String	Y	8	
memo	메모	String	Y	128	
hts_kor_isnm	HTS 한글 종목명	String	Y	40	
fxdt_ntby_qty	기준일 순매수 수량	String	Y	12	
cntg_unpr	체결단가	String	Y	11	
cntg_cls_code	체결 구분 코드	String	Y	1	
class WatchlistStocksByGroupItem2(BaseModel):
    pass


class WatchlistStocksByGroup(BaseModel):
    """관심종목 그룹별 종목조회"""

    output1: WatchlistGroupsItem1 = Field(title="응답상세1")
    output2: Sequence[WatchlistStocksByGroupItem2] = Field(default_factory=list)

hts_kor_isnm	HTS 한글 종목명	String	Y	40	
mksc_shrn_iscd	유가증권 단축 종목코드	String	Y	9	
ntby_qty	순매수 수량	String	Y	18	
stck_prpr	주식 현재가	String	Y	10	
prdy_vrss_sign	전일 대비 부호	String	Y	1	
prdy_vrss	전일 대비	String	Y	10	
prdy_ctrt	전일 대비율	String	Y	8	
acml_vol	누적 거래량	String	Y	18	
frgn_ntby_qty	외국인 순매수 수량	String	Y	12	
orgn_ntby_qty	기관계 순매수 수량	String	Y	18	
ivtr_ntby_qty	투자신탁 순매수 수량	String	Y	12	
bank_ntby_qty	은행 순매수 수량	String	Y	12	
insu_ntby_qty	보험 순매수 수량	String	Y	12	
mrbn_ntby_qty	종금 순매수 수량	String	Y	12	
fund_ntby_qty	기금 순매수 수량	String	Y	12	
etc_orgt_ntby_vol	기타 단체 순매수 거래량	String	Y	18	
etc_corp_ntby_vol	기타 법인 순매수 거래량	String	Y	18	
frgn_ntby_tr_pbmn	외국인 순매수 거래 대금	String	Y	18	frgn_ntby_tr_pbmn ~ etc_corp_ntby_tr_pbmn (단위 : 백만원, 수량*현재가)
orgn_ntby_tr_pbmn	기관계 순매수 거래 대금	String	Y	18	
ivtr_ntby_tr_pbmn	투자신탁 순매수 거래 대금	String	Y	18	
bank_ntby_tr_pbmn	은행 순매수 거래 대금	String	Y	18	
insu_ntby_tr_pbmn	보험 순매수 거래 대금	String	Y	18	
mrbn_ntby_tr_pbmn	종금 순매수 거래 대금	String	Y	18	
fund_ntby_tr_pbmn	기금 순매수 거래 대금	String	Y	18	
etc_orgt_ntby_tr_pbmn	기타 단체 순매수 거래 대금	String	Y	18	
etc_corp_ntby_tr_pbmn	기타 법인 순매수 거래 대금	String	Y	18
class InstitutionalForeignTradingAggregateItem(BaseModel):
    pass


class InstitutionalForeignTradingAggregate(BaseModel):
    """국내기관_외국인 매매종목가집계"""

    output: InstitutionalForeignTradingAggregateItem = Field(title="응답상세")

stck_shrn_iscd	주식단축종목코드	String	Y	9	
hts_kor_isnm	HTS한글종목명	String	Y	40	
glob_ntsl_qty	외국계순매도수량	String	Y	12	
stck_prpr	주식현재가	String	Y	10	
prdy_vrss	전일대비	String	Y	10	
prdy_vrss_sign	전일대비부호	String	Y	1	
prdy_ctrt	전일대비율	String	Y	82	
acml_vol	누적거래량	String	Y	18	
glob_total_seln_qty	외국계총매도수량	String	Y	18	
glob_total_shnu_qty	외국계총매수2수량	String	Y	18	
class ForeignBrokerageTradingAggregateItem(BaseModel):
    pass


class ForeignBrokerageTradingAggregate(BaseModel):
    """외국계 매매종목 가집계"""

    pass


stck_prpr	주식 현재가	String	Y	10	
prdy_vrss	전일 대비	String	Y	10	
prdy_vrss_sign	전일 대비 부호	String	Y	1	
prdy_ctrt	전일 대비율	String	Y	82	
acml_vol	누적 거래량	String	Y	18	
prdy_vol	전일 거래량	String	Y	18	
rprs_mrkt_kor_name	대표 시장 한글 명	String	Y	40	
class InvestorTradingTrendByStockDailyItem1(BaseModel):
    pass

stck_bsop_date	주식 영업 일자	String	Y	8	
stck_clpr	주식 종가	String	Y	10	
prdy_vrss	전일 대비	String	Y	10	
prdy_vrss_sign	전일 대비 부호	String	Y	1	
prdy_ctrt	전일 대비율	String	Y	82	
acml_vol	누적 거래량	String	Y	18	단위 : 주
acml_tr_pbmn	누적 거래 대금	String	Y	18	단위 : 백만원
stck_oprc	주식 시가2	String	Y	10	
stck_hgpr	주식 최고가	String	Y	10	
stck_lwpr	주식 최저가	String	Y	10	
frgn_ntby_qty	외국인 순매수 수량	String	Y	12	단위 : 주
frgn_reg_ntby_qty	외국인 등록 순매수 수량	String	Y	18	
frgn_nreg_ntby_qty	외국인 비등록 순매수 수량	String	Y	18	
prsn_ntby_qty	개인 순매수 수량	String	Y	12	
orgn_ntby_qty	기관계 순매수 수량	String	Y	18	
scrt_ntby_qty	증권 순매수 수량	String	Y	12	
ivtr_ntby_qty	투자신탁 순매수 수량	String	Y	12	
pe_fund_ntby_vol	사모 펀드 순매수 거래량	String	Y	18	
bank_ntby_qty	은행 순매수 수량	String	Y	12	
insu_ntby_qty	보험 순매수 수량	String	Y	12	
mrbn_ntby_qty	종금 순매수 수량	String	Y	12	
fund_ntby_qty	기금 순매수 수량	String	Y	12	
etc_ntby_qty	기타 순매수 수량	String	Y	12	
etc_corp_ntby_vol	기타 법인 순매수 거래량	String	Y	18	
etc_orgt_ntby_vol	기타 단체 순매수 거래량	String	Y	18	
frgn_reg_ntby_pbmn	외국인 등록 순매수 대금	String	Y	18	단위 : 백만원
frgn_ntby_tr_pbmn	외국인 순매수 거래 대금	String	Y	18	
frgn_nreg_ntby_pbmn	외국인 비등록 순매수 대금	String	Y	18	
prsn_ntby_tr_pbmn	개인 순매수 거래 대금	String	Y	18	
orgn_ntby_tr_pbmn	기관계 순매수 거래 대금	String	Y	18	
scrt_ntby_tr_pbmn	증권 순매수 거래 대금	String	Y	18	
pe_fund_ntby_tr_pbmn	사모 펀드 순매수 거래 대금	String	Y	18	
ivtr_ntby_tr_pbmn	투자신탁 순매수 거래 대금	String	Y	18	
bank_ntby_tr_pbmn	은행 순매수 거래 대금	String	Y	18	
insu_ntby_tr_pbmn	보험 순매수 거래 대금	String	Y	18	
mrbn_ntby_tr_pbmn	종금 순매수 거래 대금	String	Y	18	
fund_ntby_tr_pbmn	기금 순매수 거래 대금	String	Y	18	
etc_ntby_tr_pbmn	기타 순매수 거래 대금	String	Y	18	
etc_corp_ntby_tr_pbmn	기타 법인 순매수 거래 대금	String	Y	18	
etc_orgt_ntby_tr_pbmn	기타 단체 순매수 거래 대금	String	Y	18	
frgn_seln_vol	외국인 매도 거래량	String	Y	18	
frgn_shnu_vol	외국인 매수2 거래량	String	Y	18	
frgn_seln_tr_pbmn	외국인 매도 거래 대금	String	Y	18	
frgn_shnu_tr_pbmn	외국인 매수2 거래 대금	String	Y	18	
frgn_reg_askp_qty	외국인 등록 매도 수량	String	Y	18	
frgn_reg_bidp_qty	외국인 등록 매수 수량	String	Y	18	
frgn_reg_askp_pbmn	외국인 등록 매도 대금	String	Y	18	
frgn_reg_bidp_pbmn	외국인 등록 매수 대금	String	Y	18	
frgn_nreg_askp_qty	외국인 비등록 매도 수량	String	Y	18	
frgn_nreg_bidp_qty	외국인 비등록 매수 수량	String	Y	18	
frgn_nreg_askp_pbmn	외국인 비등록 매도 대금	String	Y	18	
frgn_nreg_bidp_pbmn	외국인 비등록 매수 대금	String	Y	18	
prsn_seln_vol	개인 매도 거래량	String	Y	18	
prsn_shnu_vol	개인 매수2 거래량	String	Y	18	
prsn_seln_tr_pbmn	개인 매도 거래 대금	String	Y	18	
prsn_shnu_tr_pbmn	개인 매수2 거래 대금	String	Y	18	
orgn_seln_vol	기관계 매도 거래량	String	Y	18	
orgn_shnu_vol	기관계 매수2 거래량	String	Y	18	
orgn_seln_tr_pbmn	기관계 매도 거래 대금	String	Y	18	
orgn_shnu_tr_pbmn	기관계 매수2 거래 대금	String	Y	18	
scrt_seln_vol	증권 매도 거래량	String	Y	18	
scrt_shnu_vol	증권 매수2 거래량	String	Y	18	
scrt_seln_tr_pbmn	증권 매도 거래 대금	String	Y	18	
scrt_shnu_tr_pbmn	증권 매수2 거래 대금	String	Y	18	
ivtr_seln_vol	투자신탁 매도 거래량	String	Y	18	
ivtr_shnu_vol	투자신탁 매수2 거래량	String	Y	18	
ivtr_seln_tr_pbmn	투자신탁 매도 거래 대금	String	Y	18	
ivtr_shnu_tr_pbmn	투자신탁 매수2 거래 대금	String	Y	18	
pe_fund_seln_tr_pbmn	사모 펀드 매도 거래 대금	String	Y	18	
pe_fund_seln_vol	사모 펀드 매도 거래량	String	Y	18	
pe_fund_shnu_tr_pbmn	사모 펀드 매수2 거래 대금	String	Y	18	
pe_fund_shnu_vol	사모 펀드 매수2 거래량	String	Y	18	
bank_seln_vol	은행 매도 거래량	String	Y	18	
bank_shnu_vol	은행 매수2 거래량	String	Y	18	
bank_seln_tr_pbmn	은행 매도 거래 대금	String	Y	18	
bank_shnu_tr_pbmn	은행 매수2 거래 대금	String	Y	18	
insu_seln_vol	보험 매도 거래량	String	Y	18	
insu_shnu_vol	보험 매수2 거래량	String	Y	18	
insu_seln_tr_pbmn	보험 매도 거래 대금	String	Y	18	
insu_shnu_tr_pbmn	보험 매수2 거래 대금	String	Y	18	
mrbn_seln_vol	종금 매도 거래량	String	Y	18	
mrbn_shnu_vol	종금 매수2 거래량	String	Y	18	
mrbn_seln_tr_pbmn	종금 매도 거래 대금	String	Y	18	
mrbn_shnu_tr_pbmn	종금 매수2 거래 대금	String	Y	18	
fund_seln_vol	기금 매도 거래량	String	Y	18	
fund_shnu_vol	기금 매수2 거래량	String	Y	18	
fund_seln_tr_pbmn	기금 매도 거래 대금	String	Y	18	
fund_shnu_tr_pbmn	기금 매수2 거래 대금	String	Y	18	
etc_seln_vol	기타 매도 거래량	String	Y	18	
etc_shnu_vol	기타 매수2 거래량	String	Y	18	
etc_seln_tr_pbmn	기타 매도 거래 대금	String	Y	18	
etc_shnu_tr_pbmn	기타 매수2 거래 대금	String	Y	18	
etc_orgt_seln_vol	기타 단체 매도 거래량	String	Y	18	
etc_orgt_shnu_vol	기타 단체 매수2 거래량	String	Y	18	
etc_orgt_seln_tr_pbmn	기타 단체 매도 거래 대금	String	Y	18	
etc_orgt_shnu_tr_pbmn	기타 단체 매수2 거래 대금	String	Y	18	
etc_corp_seln_vol	기타 법인 매도 거래량	String	Y	18	
etc_corp_shnu_vol	기타 법인 매수2 거래량	String	Y	18	
etc_corp_seln_tr_pbmn	기타 법인 매도 거래 대금	String	Y	18	
etc_corp_shnu_tr_pbmn	기타 법인 매수2 거래 대금	String	Y	18	
bold_yn	BOLD 여부	String	Y	18
class InvestorTradingTrendByStockDailyItem2(BaseModel):
    pass

class InvestorTradingTrendByStockDaily(BaseModel):
    """종목별 투자자매매동향(일별)"""

    output1: InvestorTradingTrendByStockDailyItem1 = Field(title="응답상세1")
    output2: Sequence[InvestorTradingTrendByStockDailyItem2] = Field(default_factory=list)

stck_bsop_date	주식 영업 일자	String	Y	8	
bstp_nmix_prpr	업종 지수 현재가	String	Y	112	
bstp_nmix_prdy_vrss	업종 지수 전일 대비	String	Y	112	
prdy_vrss_sign	전일 대비 부호	String	Y	1	
bstp_nmix_prdy_ctrt	업종 지수 전일 대비율	String	Y	82	
bstp_nmix_oprc	업종 지수 시가2	String	Y	112	
bstp_nmix_hgpr	업종 지수 최고가	String	Y	112	
bstp_nmix_lwpr	업종 지수 최저가	String	Y	112	
stck_prdy_clpr	주식 전일 종가	String	Y	10	
frgn_ntby_qty	외국인 순매수 수량	String	Y	12	
frgn_reg_ntby_qty	외국인 등록 순매수 수량	String	Y	18	
frgn_nreg_ntby_qty	외국인 비등록 순매수 수량	String	Y	18	
prsn_ntby_qty	개인 순매수 수량	String	Y	12	
orgn_ntby_qty	기관계 순매수 수량	String	Y	18	
scrt_ntby_qty	증권 순매수 수량	String	Y	12	
ivtr_ntby_qty	투자신탁 순매수 수량	String	Y	12	
pe_fund_ntby_vol	사모 펀드 순매수 거래량	String	Y	18	
bank_ntby_qty	은행 순매수 수량	String	Y	12	
insu_ntby_qty	보험 순매수 수량	String	Y	12	
mrbn_ntby_qty	종금 순매수 수량	String	Y	12	
fund_ntby_qty	기금 순매수 수량	String	Y	12	
etc_ntby_qty	기타 순매수 수량	String	Y	12	
etc_orgt_ntby_vol	기타 단체 순매수 거래량	String	Y	18	
etc_corp_ntby_vol	기타 법인 순매수 거래량	String	Y	18	
frgn_ntby_tr_pbmn	외국인 순매수 거래 대금	String	Y	18	
frgn_reg_ntby_pbmn	외국인 등록 순매수 대금	String	Y	18	
frgn_nreg_ntby_pbmn	외국인 비등록 순매수 대금	String	Y	18	
prsn_ntby_tr_pbmn	개인 순매수 거래 대금	String	Y	18	
orgn_ntby_tr_pbmn	기관계 순매수 거래 대금	String	Y	18	
scrt_ntby_tr_pbmn	증권 순매수 거래 대금	String	Y	18	
ivtr_ntby_tr_pbmn	투자신탁 순매수 거래 대금	String	Y	18	
pe_fund_ntby_tr_pbmn	사모 펀드 순매수 거래 대금	String	Y	18	
bank_ntby_tr_pbmn	은행 순매수 거래 대금	String	Y	18	
insu_ntby_tr_pbmn	보험 순매수 거래 대금	String	Y	18	
mrbn_ntby_tr_pbmn	종금 순매수 거래 대금	String	Y	18	
fund_ntby_tr_pbmn	기금 순매수 거래 대금	String	Y	18	
etc_ntby_tr_pbmn	기타 순매수 거래 대금	String	Y	18	
etc_orgt_ntby_tr_pbmn	기타 단체 순매수 거래 대금	String	Y	18	
etc_corp_ntby_tr_pbmn	기타 법인 순매수 거래 대금	String	Y	18
class InvestorTradingTrendByMarketIntradayItem(BaseModel):
    pass


class InvestorTradingTrendByMarketIntraday(BaseModel):
    """시장별 투자자매매동향(시세)"""

    output: Sequence[InvestorTradingTrendByMarketIntradayItem] = Field(default_factory=list)


bsop_hour	영업시간	String	Y	6	
stck_prpr	주식현재가	String	Y	10	
prdy_vrss	전일대비	String	Y	10	
prdy_vrss_sign	전일대비부호	String	Y	1	
prdy_ctrt	전일대비율	String	Y	82	
acml_vol	누적거래량	String	Y	18	
frgn_seln_vol	외국인매도거래량	String	Y	18	
frgn_shnu_vol	외국인매수2거래량	String	Y	18	
glob_ntby_qty	외국계순매수수량	String	Y	12	
frgn_ntby_qty_icdc	외국인순매수수량증감	String	Y	10
class InvestorTradingTrendByMarketDailyItem(BaseModel):
    pass


class InvestorTradingTrendByMarketDaily(BaseModel):
    """시장별 투자자매매동향(일별)"""

    output: Sequence[InvestorTradingTrendByMarketDailyItem] = Field(default_factory=list)


total_seln_qty	총매도수량	String	Y	18	
total_shnu_qty	총매수2수량	String	Y	18	
class ForeignNetBuyTrendByStockItem1(BaseModel):
    pass

bsop_hour	영업시간	String	Y	6	
mbcr_name	회원사명	String	Y	50	
hts_kor_isnm	HTS한글종목명	String	Y	40	
stck_prpr	주식현재가	String	Y	10	
prdy_vrss	전일대비	String	Y	10	
prdy_vrss_sign	전일대비부호	String	Y	1	
cntg_vol	체결거래량	String	Y	18	
acml_ntby_qty	누적순매수수량	String	Y	18	
glob_ntby_qty	외국계순매수수량	String	Y	12	
frgn_ntby_qty_icdc	외국인순매수수량증감	String	Y	10	
class ForeignNetBuyTrendByStockItem2(BaseModel):
    pass


class ForeignNetBuyTrendByStock(BaseModel):
    """종목별 외국계 순매수추이"""

    output1: Sequence[ForeignNetBuyTrendByStockItem1] = Field(default_factory=list)
    output2: Sequence[ForeignNetBuyTrendByStockItem2] = Field(default_factory=list)


stck_bsop_date	주식영업일자	String	Y	8	
total_seln_qty	총매도수량	String	Y	18	
total_shnu_qty	총매수2수량	String	Y	18	
ntby_qty	순매수수량	String	Y	18	
stck_prpr	주식현재가	String	Y	10	
prdy_vrss	전일대비	String	Y	10	
prdy_vrss_sign	전일대비부호	String	Y	1	
prdy_ctrt	전일대비율	String	Y	82	
acml_vol	누적거래량	String	Y	18
class MemberTradingTrendTickItem(BaseModel):
    pass


class MemberTradingTrendTick(BaseModel):
    """회원사 실시간 매매동향(틱)"""

    output: Sequence[MemberTradingTrendTickItem] = Field(default_factory=list)


stck_bsop_date	주식영업일자	String	Y	8	
total_seln_qty	총매도수량	String	Y	18	
total_shnu_qty	총매수2수량	String	Y	18	
ntby_qty	순매수수량	String	Y	18	
stck_prpr	주식현재가	String	Y	10	
prdy_vrss	전일대비	String	Y	10	
prdy_vrss_sign	전일대비부호	String	Y	1	
prdy_ctrt	전일대비율	String	Y	82	
acml_vol	누적거래량	String	Y	18
class MemberTradingTrendByStockItem(BaseModel):
    pass


class MemberTradingTrendByStock(BaseModel):
    """주식현재가 회원사 종목매매동향"""

    output: Sequence[MemberTradingTrendByStockItem] = Field(default_factory=list)

bsop_hour	영업 시간	String	Y	6	
stck_prpr	주식 현재가	String	Y	10	
prdy_vrss	전일 대비	String	Y	10	
prdy_vrss_sign	전일 대비 부호	String	Y	1	
prdy_ctrt	전일 대비율	String	Y	82	
acml_vol	누적 거래량	String	Y	18	
whol_smtn_seln_vol	전체 합계 매도 거래량	String	Y	18	
whol_smtn_shnu_vol	전체 합계 매수2 거래량	String	Y	18	
whol_smtn_ntby_qty	전체 합계 순매수 수량	String	Y	18	
whol_smtn_seln_tr_pbmn	전체 합계 매도 거래 대금	String	Y	18	
whol_smtn_shnu_tr_pbmn	전체 합계 매수2 거래 대금	String	Y	18	
whol_smtn_ntby_tr_pbmn	전체 합계 순매수 거래 대금	String	Y	18	
whol_ntby_vol_icdc	전체 순매수 거래량 증감	String	Y	10	
whol_ntby_tr_pbmn_icdc	전체 순매수 거래 대금 증감	String	Y	10
class ProgramTradingTrendByStockIntradayItem(BaseModel):
    pass


class ProgramTradingTrendByStockIntraday(BaseModel):
    """종목별 프로그램매매추이(체결)"""

    output: Sequence[ProgramTradingTrendByStockIntradayItem] = Field(default_factory=list)


stck_bsop_date	주식 영업 일자	String	Y	8	
stck_clpr	주식 종가	String	Y	10	
prdy_vrss	전일 대비	String	Y	10	
prdy_vrss_sign	전일 대비 부호	String	Y	1	
prdy_ctrt	전일 대비율	String	Y	82	
acml_vol	누적 거래량	String	Y	18	
acml_tr_pbmn	누적 거래 대금	String	Y	18	
whol_smtn_seln_vol	전체 합계 매도 거래량	String	Y	18	
whol_smtn_shnu_vol	전체 합계 매수2 거래량	String	Y	18	
whol_smtn_ntby_qty	전체 합계 순매수 수량	String	Y	18	
whol_smtn_seln_tr_pbmn	전체 합계 매도 거래 대금	String	Y	18	
whol_smtn_shnu_tr_pbmn	전체 합계 매수2 거래 대금	String	Y	18	
whol_smtn_ntby_tr_pbmn	전체 합계 순매수 거래 대금	String	Y	18	
whol_ntby_vol_icdc	전체 순매수 거래량 증감	String	Y	10	
whol_ntby_tr_pbmn_icdc2	전체 순매수 거래 대금 증감2	String	Y	18
class ProgramTradingTrendByStockDailyItem(BaseModel):
    pass


class ProgramTradingTrendByStockDaily(BaseModel):
    """종목별 프로그램매매추이(일별)"""

    output: Sequence[ProgramTradingTrendByStockDailyItem] = Field(default_factory=list)


bsop_hour_gb	입력구분	String	Y	1	<description>1: 09시 30분 입력
2: 10시 00분 입력
3: 11시 20분 입력
4: 13시 20분 입력
5: 14시 30분 입력
</description>
frgn_fake_ntby_qty	외국인수량(가집계)	String	Y	18	
orgn_fake_ntby_qty	기관수량(가집계)	String	Y	18	
sum_fake_ntby_qty	합산수량(가집계)	String	Y	18	
class ForeignInstitutionalEstimateByStockItem(BaseModel):
    pass


class ForeignInstitutionalEstimateByStock(BaseModel):
    """종목별 외인기관 추정기전계"""

    output2: Sequence[ForeignInstitutionalEstimateByStockItem] = Field(default_factory=list)

shnu_cnqn_smtn	매수 체결량 합계	String	Y	18	
seln_cnqn_smtn	매도 체결량 합계	String	Y	18	
class BuySellVolumeByStockDailyItem1(BaseModel):
    pass

stck_bsop_date	거래상태정보	String	Y	8	
total_seln_qty	총 매도 수량	String	Y	18	
total_shnu_qty	총 매수 수량	String	Y	18	
class BuySellVolumeByStockDailyItem2(BaseModel):
    pass


class BuySellVolumeByStockDaily(BaseModel):
    """종목별일별매수매도체결량"""

    output1: BuySellVolumeByStockDailyItem1 = Field(title="응답상세1")
    output2: Sequence[BuySellVolumeByStockDailyItem2] = Field(default_factory=list)

bsop_hour	영업 시간	String	Y	6	
arbt_smtn_seln_tr_pbmn	차익 합계 매도 거래 대금	String	Y	18	
arbt_smtm_seln_tr_pbmn_rate	차익 합계 매도 거래대금 비율	String	Y	72	
arbt_smtn_shnu_tr_pbmn	차익 합계 매수2 거래 대금	String	Y	18	
arbt_smtm_shun_tr_pbmn_rate	차익합계매수거래대금비율	String	Y	72	
nabt_smtn_seln_tr_pbmn	비차익 합계 매도 거래 대금	String	Y	18	
nabt_smtm_seln_tr_pbmn_rate	비차익 합계 매도 거래대금 비율	String	Y	72	
nabt_smtn_shnu_tr_pbmn	비차익 합계 매수2 거래 대금	String	Y	18	
nabt_smtm_shun_tr_pbmn_rate	비차익합계매수거래대금비율	String	Y	72	
arbt_smtn_ntby_tr_pbmn	차익 합계 순매수 거래 대금	String	Y	18	
arbt_smtm_ntby_tr_pbmn_rate	차익 합계 순매수 거래대금 비율	String	Y	72	
nabt_smtn_ntby_tr_pbmn	비차익 합계 순매수 거래 대금	String	Y	18	
nabt_smtm_ntby_tr_pbmn_rate	비차익 합계 순매수 거래대금 비	String	Y	72	
whol_smtn_ntby_tr_pbmn	전체 합계 순매수 거래 대금	String	Y	18	
whol_ntby_tr_pbmn_rate	전체 순매수 거래대금 비율	String	Y	72	
bstp_nmix_prpr	업종 지수 현재가	String	Y	112	
bstp_nmix_prdy_vrss	업종 지수 전일 대비	String	Y	112	
prdy_vrss_sign	전일 대비 부호	String	Y	1
class ProgramTradingSummaryIntradayItem(BaseModel):
    pass


class ProgramTradingSummaryIntraday(BaseModel):
    """프로그램매매 종합현황(시간)"""

    output1: Sequence[ProgramTradingSummaryIntradayItem] = Field(default_factory=list)
    
stck_bsop_date	주식 영업 일자	String	Y	8	
nabt_entm_seln_tr_pbmn	비차익 위탁 매도 거래 대금	String	Y	18	
nabt_onsl_seln_vol	비차익 자기 매도 거래량	String	Y	18	
whol_onsl_seln_tr_pbmn	전체 자기 매도 거래 대금	String	Y	18	
arbt_smtn_shnu_vol	차익 합계 매수2 거래량	String	Y	18	
nabt_smtn_shnu_tr_pbmn	비차익 합계 매수2 거래 대금	String	Y	18	
arbt_entm_ntby_qty	차익 위탁 순매수 수량	String	Y	18	
nabt_entm_ntby_tr_pbmn	비차익 위탁 순매수 거래 대금	String	Y	18	
arbt_entm_seln_vol	차익 위탁 매도 거래량	String	Y	18	
nabt_entm_seln_vol_rate	비차익 위탁 매도 거래량 비율	String	Y	82	
nabt_onsl_seln_vol_rate	비차익 자기 매도 거래량 비율	String	Y	82	
whol_onsl_seln_tr_pbmn_rate	전체 자기 매도 거래 대금 비율	String	Y	82	
arbt_smtm_shun_vol_rate	차익 합계 매수 거래량 비율	String	Y	72	
nabt_smtm_shun_tr_pbmn_rate	비차익 합계 매수 거래대금 비율	String	Y	72	
arbt_entm_ntby_qty_rate	차익 위탁 순매수 수량 비율	String	Y	82	
nabt_entm_ntby_tr_pbmn_rate	비차익 위탁 순매수 거래 대금	String	Y	82	
arbt_entm_seln_vol_rate	차익 위탁 매도 거래량 비율	String	Y	82	
nabt_entm_seln_tr_pbmn_rate	비차익 위탁 매도 거래 대금 비	String	Y	82	
nabt_onsl_seln_tr_pbmn	비차익 자기 매도 거래 대금	String	Y	18	
whol_smtn_seln_vol	전체 합계 매도 거래량	String	Y	18	
arbt_smtn_shnu_tr_pbmn	차익 합계 매수2 거래 대금	String	Y	18	
whol_entm_shnu_vol	전체 위탁 매수2 거래량	String	Y	18	
arbt_entm_ntby_tr_pbmn	차익 위탁 순매수 거래 대금	String	Y	18	
nabt_onsl_ntby_qty	비차익 자기 순매수 수량	String	Y	18	
arbt_entm_seln_tr_pbmn	차익 위탁 매도 거래 대금	String	Y	18	
nabt_onsl_seln_tr_pbmn_rate	비차익 자기 매도 거래 대금 비	String	Y	82	
whol_seln_vol_rate	전체 매도 거래량 비율	String	Y	72	
arbt_smtm_shun_tr_pbmn_rate	차익 합계 매수 거래대금 비율	String	Y	72	
whol_entm_shnu_vol_rate	전체 위탁 매수 거래량 비율	String	Y	82	
arbt_entm_ntby_tr_pbmn_rate	차익 위탁 순매수 거래 대금 비	String	Y	82	
nabt_onsl_ntby_qty_rate	비차익 자기 순매수 수량 비율	String	Y	82	
arbt_entm_seln_tr_pbmn_rate	차익 위탁 매도 거래 대금 비율	String	Y	82	
nabt_smtn_seln_vol	비차익 합계 매도 거래량	String	Y	18	
whol_smtn_seln_tr_pbmn	전체 합계 매도 거래 대금	String	Y	18	
nabt_entm_shnu_vol	비차익 위탁 매수2 거래량	String	Y	18	
whol_entm_shnu_tr_pbmn	전체 위탁 매수2 거래 대금	String	Y	18	
arbt_onsl_ntby_qty	차익 자기 순매수 수량	String	Y	18	
nabt_onsl_ntby_tr_pbmn	비차익 자기 순매수 거래 대금	String	Y	18	
arbt_onsl_seln_tr_pbmn	차익 자기 매도 거래 대금	String	Y	18	
nabt_smtm_seln_vol_rate	비차익 합계 매도 거래량 비율	String	Y	72	
whol_seln_tr_pbmn_rate	전체 매도 거래대금 비율	String	Y	72	
nabt_entm_shnu_vol_rate	비차익 위탁 매수 거래량 비율	String	Y	82	
whol_entm_shnu_tr_pbmn_rate	전체 위탁 매수 거래 대금 비율	String	Y	82	
arbt_onsl_ntby_qty_rate	차익 자기 순매수 수량 비율	String	Y	82	
nabt_onsl_ntby_tr_pbmn_rate	비차익 자기 순매수 거래 대금	String	Y	82	
arbt_onsl_seln_tr_pbmn_rate	차익 자기 매도 거래 대금 비율	String	Y	82	
nabt_smtn_seln_tr_pbmn	비차익 합계 매도 거래 대금	String	Y	18	
arbt_entm_shnu_vol	차익 위탁 매수2 거래량	String	Y	18	
nabt_entm_shnu_tr_pbmn	비차익 위탁 매수2 거래 대금	String	Y	18	
whol_onsl_shnu_vol	전체 자기 매수2 거래량	String	Y	18	
arbt_onsl_ntby_tr_pbmn	차익 자기 순매수 거래 대금	String	Y	18	
nabt_smtn_ntby_qty	비차익 합계 순매수 수량	String	Y	18	
arbt_onsl_seln_vol	차익 자기 매도 거래량	String	Y	18	
nabt_smtm_seln_tr_pbmn_rate	비차익 합계 매도 거래대금 비율	String	Y	72	
arbt_entm_shnu_vol_rate	차익 위탁 매수 거래량 비율	String	Y	82	
nabt_entm_shnu_tr_pbmn_rate	비차익 위탁 매수 거래 대금 비	String	Y	82	
whol_onsl_shnu_tr_pbmn	전체 자기 매수2 거래 대금	String	Y	18	
arbt_onsl_ntby_tr_pbmn_rate	차익 자기 순매수 거래 대금 비	String	Y	82	
nabt_smtm_ntby_qty_rate	비차익 합계 순매수 수량 비율	String	Y	72	
arbt_onsl_seln_vol_rate	차익 자기 매도 거래량 비율	String	Y	82	
whol_entm_seln_vol	전체 위탁 매도 거래량	String	Y	18	
arbt_entm_shnu_tr_pbmn	차익 위탁 매수2 거래 대금	String	Y	18	
nabt_onsl_shnu_vol	비차익 자기 매수2 거래량	String	Y	18	
whol_onsl_shnu_tr_pbmn_rate	전체 자기 매수 거래 대금 비율	String	Y	82	
arbt_smtn_ntby_qty	차익 합계 순매수 수량	String	Y	18	
nabt_smtn_ntby_tr_pbmn	비차익 합계 순매수 거래 대금	String	Y	18	
arbt_smtn_seln_vol	차익 합계 매도 거래량	String	Y	18	
whol_entm_seln_tr_pbmn	전체 위탁 매도 거래 대금	String	Y	18	
arbt_entm_shnu_tr_pbmn_rate	차익 위탁 매수 거래 대금 비율	String	Y	82	
nabt_onsl_shnu_vol_rate	비차익 자기 매수 거래량 비율	String	Y	82	
whol_onsl_shnu_vol_rate	전체 자기 매수 거래량 비율	String	Y	82	
arbt_smtm_ntby_qty_rate	차익 합계 순매수 수량 비율	String	Y	72	
nabt_smtm_ntby_tr_pbmn_rate	비차익 합계 순매수 거래대금 비	String	Y	72	
arbt_smtm_seln_vol_rate	차익 합계 매도 거래량 비율	String	Y	72	
whol_entm_seln_vol_rate	전체 위탁 매도 거래량 비율	String	Y	82	
arbt_onsl_shnu_vol	차익 자기 매수2 거래량	String	Y	18	
nabt_onsl_shnu_tr_pbmn	비차익 자기 매수2 거래 대금	String	Y	18	
whol_smtn_shnu_vol	전체 합계 매수2 거래량	String	Y	18	
arbt_smtn_ntby_tr_pbmn	차익 합계 순매수 거래 대금	String	Y	18	
whol_entm_ntby_qty	전체 위탁 순매수 수량	String	Y	18	
arbt_smtn_seln_tr_pbmn	차익 합계 매도 거래 대금	String	Y	18	
whol_entm_seln_tr_pbmn_rate	전체 위탁 매도 거래 대금 비율	String	Y	82	
arbt_onsl_shnu_vol_rate	차익 자기 매수 거래량 비율	String	Y	82	
nabt_onsl_shnu_tr_pbmn_rate	비차익 자기 매수 거래 대금 비	String	Y	82	
whol_shun_vol_rate	전체 매수 거래량 비율	String	Y	72	
arbt_smtm_ntby_tr_pbmn_rate	차익 합계 순매수 거래대금 비율	String	Y	72	
whol_entm_ntby_qty_rate	전체 위탁 순매수 수량 비율	String	Y	82	
arbt_smtm_seln_tr_pbmn_rate	차익 합계 매도 거래대금 비율	String	Y	72	
whol_onsl_seln_vol	전체 자기 매도 거래량	String	Y	18	
arbt_onsl_shnu_tr_pbmn	차익 자기 매수2 거래 대금	String	Y	18	
nabt_smtn_shnu_vol	비차익 합계 매수2 거래량	String	Y	18	
whol_smtn_shnu_tr_pbmn	전체 합계 매수2 거래 대금	String	Y	18	
nabt_entm_ntby_qty	비차익 위탁 순매수 수량	String	Y	18	
whol_entm_ntby_tr_pbmn	전체 위탁 순매수 거래 대금	String	Y	18	
nabt_entm_seln_vol	비차익 위탁 매도 거래량	String	Y	18	
whol_onsl_seln_vol_rate	전체 자기 매도 거래량 비율	String	Y	82	
arbt_onsl_shnu_tr_pbmn_rate	차익 자기 매수 거래 대금 비율	String	Y	82	
nabt_smtm_shun_vol_rate	비차익 합계 매수 거래량 비율	String	Y	72	
whol_shun_tr_pbmn_rate	전체 매수 거래대금 비율	String	Y	72	
nabt_entm_ntby_qty_rate	비차익 위탁 순매수 수량 비율	String	Y	82	
class ProgramTradingSummaryDailyItem(BaseModel):
    pass


class ProgramTradingSummaryDaily(BaseModel):
    """프로그램매매 종합현황(일별)"""

    output: Sequence[ProgramTradingSummaryDailyItem] = Field(default_factory=list)

invr_cls_code	투자자코드	String	Y	4	
all_seln_qty	전체매도수량	String	Y	18	
all_seln_amt	전체매도대금	String	Y	18	
invr_cls_name	투자자 구분 명	String	Y	20	
all_shnu_qty	전체매수수량	String	Y	18	
all_shnu_amt	전체매수대금	String	Y	18	
all_ntby_amt	전체순매수대금	String	Y	12	
arbt_seln_qty	차익매도수량	String	Y	18	
all_ntby_qty	전체순매수수량	String	Y	12	
arbt_shnu_qty	차익매수수량	String	Y	18	
arbt_ntby_qty	차익순매수수량	String	Y	12	
arbt_seln_amt	차익매도대금	String	Y	18	
arbt_shnu_amt	차익매수대금	String	Y	18	
arbt_ntby_amt	차익순매수대금	String	Y	12	
nabt_seln_qty	비차익매도수량	String	Y	18	
nabt_shnu_qty	비차익매수수량	String	Y	18	
nabt_ntby_qty	비차익순매수수량	String	Y	12	
nabt_seln_amt	비차익매도대금	String	Y	18	
nabt_shnu_amt	비차익매수대금	String	Y	18	
nabt_ntby_amt	비차익순매수대금	String	Y	12	
class ProgramTradingInvestorTrendTodayItem(BaseModel):
    pass


class ProgramTradingInvestorTrendToday(BaseModel):
    """프로그램매매 투자자매매동향(당일)"""

    output1: Sequence[ProgramTradingInvestorTrendTodayItem] = Field(default_factory=list)


deal_date	매매 일자	String	Y	8	
stck_prpr	주식 현재가	String	Y	10	
prdy_vrss_sign	전일 대비 부호	String	Y	1	
prdy_vrss	전일 대비	String	Y	10	
prdy_ctrt	전일 대비율	String	Y	82	
acml_vol	누적 거래량	String	Y	18	
stlm_date	결제 일자	String	Y	8	
whol_loan_new_stcn	전체 융자 신규 주수	String	Y	18	단위: 주
whol_loan_rdmp_stcn	전체 융자 상환 주수	String	Y	18	단위: 주
whol_loan_rmnd_stcn	전체 융자 잔고 주수	String	Y	18	단위: 주
whol_loan_new_amt	전체 융자 신규 금액	String	Y	18	단위: 만원
whol_loan_rdmp_amt	전체 융자 상환 금액	String	Y	18	단위: 만원
whol_loan_rmnd_amt	전체 융자 잔고 금액	String	Y	18	단위: 만원
whol_loan_rmnd_rate	전체 융자 잔고 비율	String	Y	84	
whol_loan_gvrt	전체 융자 공여율	String	Y	82	
whol_stln_new_stcn	전체 대주 신규 주수	String	Y	18	단위: 주
whol_stln_rdmp_stcn	전체 대주 상환 주수	String	Y	18	단위: 주
whol_stln_rmnd_stcn	전체 대주 잔고 주수	String	Y	18	단위: 주
whol_stln_new_amt	전체 대주 신규 금액	String	Y	18	단위: 만원
whol_stln_rdmp_amt	전체 대주 상환 금액	String	Y	18	단위: 만원
whol_stln_rmnd_amt	전체 대주 잔고 금액	String	Y	18	단위: 만원
whol_stln_rmnd_rate	전체 대주 잔고 비율	String	Y	84	
whol_stln_gvrt	전체 대주 공여율	String	Y	82	
stck_oprc	주식 시가2	String	Y	10	
stck_hgpr	주식 최고가	String	Y	10	
stck_lwpr	주식 최저가	String	Y	10	
class CreditBalanceTrendDailyItem(BaseModel):
    pass


class CreditBalanceTrendDaily(BaseModel):
    """국내주식 신용잔고 일별추이"""

    output: Sequence[CreditBalanceTrendDailyItem] = Field(default_factory=list)

rprs_mrkt_kor_name	대표 시장 한글 명	string	Y	40
antc_cnpr	예상 체결가	string	Y	10
antc_cntg_vrss_sign	예상 체결 대비 부호	string	Y	1
antc_cntg_vrss	예상 체결 대비	string	Y	10
antc_cntg_prdy_ctrt	예상 체결 전일 대비율	string	Y	82
antc_vol	예상 거래량	string	Y	18
antc_tr_pbmn	예상 거래대금	string	Y	19
class ExpectedPriceTrendItem1(BaseModel):
    pass

stck_bsop_date	주식 영업 일자	string	Y	8
stck_cntg_hour	주식 체결 시간	string	Y	6
stck_prpr	주식 현재가	string	Y	10
prdy_vrss_sign	전일 대비 부호	string	Y	1
prdy_vrss	전일 대비	string	Y	10
prdy_ctrt	전일 대비율	string	Y	82
acml_vol	누적 거래량	string	Y	18
class ExpectedPriceTrendItem2(BaseModel):
    pass

class ExpectedPriceTrend(BaseModel):
    """국내주식 예상체결가 추이"""

    output1: ExpectedPriceTrendItem1 = Field(title="응답상세1")
    output2: Sequence[ExpectedPriceTrendItem2] = Field(default_factory=list)


stck_prpr	주식 현재가	string	Y	10
prdy_vrss	전일 대비	string	Y	10
prdy_vrss_sign	전일 대비 부호	string	Y	1
prdy_ctrt	전일 대비율	string	Y	82
acml_vol	누적 거래량	string	Y	18
prdy_vol	전일 거래량	string	Y	18
class ShortSellingTrendDailyItem1(BaseModel):
    pass

stck_bsop_date	주식 영업 일자	string	Y	8
stck_clpr	주식 종가	string	Y	10
prdy_vrss	전일 대비	string	Y	10
prdy_vrss_sign	전일 대비 부호	string	Y	1
prdy_ctrt	전일 대비율	string	Y	82
acml_vol	누적 거래량	string	Y	18
stnd_vol_smtn	기준 거래량 합계	string	Y	18
ssts_cntg_qty	공매도 체결 수량	string	Y	12
ssts_vol_rlim	공매도 거래량 비중	string	Y	62
acml_ssts_cntg_qty	누적 공매도 체결 수량	string	Y	13
acml_ssts_cntg_qty_rlim	누적 공매도 체결 수량 비중	string	Y	72
acml_tr_pbmn	누적 거래 대금	string	Y	18
stnd_tr_pbmn_smtn	기준 거래대금 합계	string	Y	18
ssts_tr_pbmn	공매도 거래 대금	string	Y	18
ssts_tr_pbmn_rlim	공매도 거래대금 비중	string	Y	62
acml_ssts_tr_pbmn	누적 공매도 거래 대금	string	Y	19
acml_ssts_tr_pbmn_rlim	누적 공매도 거래 대금 비중	string	Y	72
stck_oprc	주식 시가2	string	Y	10
stck_hgpr	주식 최고가	string	Y	10
stck_lwpr	주식 최저가	string	Y	10
avrg_prc	평균가격	string	Y	11
class ShortSellingTrendDailyItem2(BaseModel):
    pass

class ShortSellingTrendDaily(BaseModel):
    """국내주식 공매도 일별추이"""

    output1: ShortSellingTrendDailyItem1 = Field(title="응답상세1")
    output2: Sequence[ShortSellingTrendDailyItem2] = Field(default_factory=list)

data_rank	데이터 순위	string	Y	10
iscd_stat_cls_code	종목 상태 구분 코드	string	Y	3
stck_shrn_iscd	주식 단축 종목코드	string	Y	9
hts_kor_isnm	HTS 한글 종목명	string	Y	40
ovtm_untp_antc_cnpr	시간외 단일가 예상 체결가	string	Y	10
ovtm_untp_antc_cntg_vrss	 시간외 단일가 예상 체결 대비	string	Y	10
ovtm_untp_antc_cntg_vrsssign	시간외 단일가 예상 체결 대비	string	Y	1
ovtm_untp_antc_cntg_ctrt	시간외 단일가 예상 체결 대비율	string	Y	82
ovtm_untp_askp_rsqn1	시간외 단일가 매도호가 잔량1	string	Y	12
ovtm_untp_bidp_rsqn1	시간외 단일가 매수호가 잔량1	string	Y	12
ovtm_untp_antc_cnqn	시간외 단일가 예상 체결량	string	Y	18
itmt_vol	장중 거래량	string	Y	18
stck_prpr	주식 현재가	string	Y	10
class AfterHoursExpectedFluctuationItem(BaseModel):
    pass


class AfterHoursExpectedFluctuation(BaseModel):
    """국내주식 시간외예상체결등락율"""

    output: AfterHoursExpectedFluctuationItem = Field(title="응답상세")

prpr_name	가격명	string	Y	40
smtn_avrg_prpr	합계 평균가격	string	Y	10
acml_vol	합계 거래량	string	Y	18
whol_ntby_qty_rate	합계 순매수비율	string	Y	72
ntby_cntg_csnu	합계 순매수건수	string	Y	10
seln_cnqn_smtn	매도 거래량	string	Y	18
whol_seln_vol_rate	매도 거래량비율	string	Y	72
seln_cntg_csnu	매도 건수	string	Y	10
shnu_cnqn_smtn	매수 거래량	string	Y	18
whol_shun_vol_rate	매수 거래량비율	string	Y	72
shnu_cntg_csnu	매수 건수	string	Y	10
class TradingWeightByAmountItem(BaseModel):
    pass


class TradingWeightByAmount(BaseModel):
    """국내주식 체결금액별 매매비중"""

    output: Sequence[TradingWeightByAmountItem] = Field(default_factory=list)

bsop_date	영업일자	string	Y	8	 
bstp_nmix_prpr	업종지수현재가	string	Y	112	 
bstp_nmix_prdy_vrss	업종지수전일대비	string	Y	112	 
prdy_vrss_sign	전일대비부호	string	Y	1	 1. 상한 2. 상승 3. 보합 4. 하한 5. 하락
prdy_ctrt	전일대비율	string	Y	82	 
hts_avls	HTS시가총액	string	Y	18	단위: 백만원
cust_dpmn_amt	고객예탁금금액	string	Y	18	단위: 억원
cust_dpmn_amt_prdy_vrss	고객예탁금금액전일대비	string	Y	18	 
amt_tnrt	금액회전율	string	Y	84	 
uncl_amt	미수금액	string	Y	18	단위: 억원
crdt_loan_rmnd	신용융자잔고	string	Y	18	단위: 억원
futs_tfam_amt	선물예수금금액	string	Y	18	단위: 억원
sttp_amt	주식형금액	string	Y	18	단위: 억원
mxtp_amt	혼합형금액	string	Y	18	단위: 억원
bntp_amt	채권형금액	string	Y	18	단위: 억원
mmf_amt	MMF금액	string	Y	18	단위: 억원
secu_lend_amt	담보대출잔고금액	string	Y	18	단위: 억원
class MarketFundSummaryItem(BaseModel):
    pass


class MarketFundSummary(BaseModel):
    """국내 증시자금 종합"""

    output: Sequence[MarketFundSummaryItem] = Field(default_factory=list)


bsop_date	일자	string	Y	8
stck_prpr	주식 종가	string	Y	10
prdy_vrss_sign	전일 대비 부호	string	Y	1
prdy_vrss	전일 대비	string	Y	10
prdy_ctrt	전일 대비율	string	Y	8
acml_vol	누적 거래량	string	Y	18
new_stcn	당일 증가 주수 (체결)	string	Y	16
rdmp_stcn	당일 감소 주수 (상환)	string	Y	16
prdy_rmnd_vrss	대차거래 증감	string	Y	16
rmnd_stcn	당일 잔고 주수	string	Y	16
rmnd_amt	당일 잔고 금액	string	Y	20
class StockLoanTrendDailyItem(BaseModel):
    pass


class StockLoanTrendDaily(BaseModel):
    """종목별 일별 대차거래추이"""

    output: Sequence[StockLoanTrendDailyItem] = Field(default_factory=list)

mksc_shrn_iscd	유가증권단축종목코드	string	Y	9
hts_kor_isnm	HTS한글종목명	string	Y	40
stck_prpr	주식현재가	string	Y	10
prdy_vrss_sign	전일대비부호	string	Y	1
prdy_vrss	전일대비	string	Y	10
prdy_ctrt	전일대비율	string	Y	82
acml_vol	누적거래량	string	Y	18
total_askp_rsqn	총매도호가잔량	string	Y	12
total_bidp_rsqn	총매수호가잔량	string	Y	12
askp_rsqn1	매도호가잔량1	string	Y	12
bidp_rsqn1	매수호가잔량1	string	Y	12
prdy_vol	전일거래량	string	Y	18
seln_cnqn	매도체결량	string	Y	18
shnu_cnqn	매수2체결량	string	Y	18
stck_llam	주식하한가	string	Y	10
stck_mxpr	주식상한가	string	Y	10
prdy_vrss_vol_rate	전일대비거래량비율	string	Y	84
class LimitPriceStocksItem(BaseModel):
    pass


class LimitPriceStocks(BaseModel):
    """국내주식 상하한가 표착"""

    output: Sequence[LimitPriceStocksItem] = Field(default_factory=list)


rprs_mrkt_kor_name	대표시장한글명	string	Y	40
stck_shrn_iscd	주식단축종목코드	string	Y	9
hts_kor_isnm	HTS한글종목명	string	Y	40
stck_prpr	주식현재가	string	Y	10
prdy_vrss_sign	전일대비부호	string	Y	1
prdy_vrss	전일대비	string	Y	10
prdy_ctrt	전일대비율	string	Y	82
acml_vol	누적거래량	string	Y	18
prdy_vol	전일거래량	string	Y	18
wghn_avrg_stck_prc	가중평균주식가격	string	Y	192
lstn_stcn	상장주수	string	Y	18
class ResistanceLevelTradingWeightItem1(BaseModel):
    pass

data_rank	데이터순위	string	Y	10
stck_prpr	주식현재가	string	Y	10
cntg_vol	체결거래량	string	Y	18
acml_vol_rlim	누적거래량비중	string	Y	72
class ResistanceLevelTradingWeightItem2(BaseModel):
    pass

class ResistanceLevelTradingWeight(BaseModel):
    """국내주식 매물대/거래비중"""

    output1: ResistanceLevelTradingWeightItem1 = Field(title="응답상세1")
    output2: Sequence[ResistanceLevelTradingWeightItem2] = Field(default_factory=list)
