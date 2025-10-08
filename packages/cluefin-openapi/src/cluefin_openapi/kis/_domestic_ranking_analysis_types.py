from pydantic import BaseModel, Field
from typing import Sequence
from cluefin_openapi.kis._models import KisHttpBody


hts_kor_isnm	HTS 한글 종목명	string	Y	40
mksc_shrn_iscd	유가증권 단축 종목코드	string	Y	9
data_rank	데이터 순위	string	Y	10
stck_prpr	주식 현재가	string	Y	10
prdy_vrss_sign	전일 대비 부호	string	Y	1
prdy_vrss	전일 대비	string	Y	10
prdy_ctrt	전일 대비율	string	Y	82
acml_vol	누적 거래량	string	Y	18
prdy_vol	전일 거래량	string	Y	18
lstn_stcn	상장 주수	string	Y	18
avrg_vol	평균 거래량	string	Y	18
n_befr_clpr_vrss_prpr_rate	N일전종가대비현재가대비율	string	Y	82
vol_inrt	거래량증가율	string	Y	84
vol_tnrt	거래량 회전율	string	Y	82
nday_vol_tnrt	N일 거래량 회전율	string	Y	8
avrg_tr_pbmn	평균 거래 대금	string	Y	18
tr_pbmn_tnrt	거래대금회전율	string	Y	82
nday_tr_pbmn_tnrt	N일 거래대금 회전율	string	Y	8
acml_tr_pbmn	누적 거래 대금	string	Y	18
class TradingVolumeRankItem(BaseModel):
    pass


class TradingVolumeRank(BaseModel, KisHttpBody):
    """거래량순위"""

    output: Sequence[TradingVolumeRankItem] = Field(default_factory=list)

stck_shrn_iscd	주식 단축 종목코드	string	Y	9
data_rank	데이터 순위	string	Y	10
hts_kor_isnm	HTS 한글 종목명	string	Y	40
stck_prpr	주식 현재가	string	Y	10
prdy_vrss	전일 대비	string	Y	10
prdy_vrss_sign	전일 대비 부호	string	Y	1
prdy_ctrt	전일 대비율	string	Y	82
acml_vol	누적 거래량	string	Y	18
stck_hgpr	주식 최고가	string	Y	10
hgpr_hour	최고가 시간	string	Y	6
acml_hgpr_date	누적 최고가 일자	string	Y	8
stck_lwpr	주식 최저가	string	Y	10
lwpr_hour	최저가 시간	string	Y	6
acml_lwpr_date	누적 최저가 일자	string	Y	8
lwpr_vrss_prpr_rate	최저가 대비 현재가 비율	string	Y	84
dsgt_date_clpr_vrss_prpr_rate	지정 일자 종가 대비 현재가 비	string	Y	84
cnnt_ascn_dynu	연속 상승 일수	string	Y	5
hgpr_vrss_prpr_rate	최고가 대비 현재가 비율	string	Y	84
cnnt_down_dynu	연속 하락 일수	string	Y	5
oprc_vrss_prpr_sign	시가2 대비 현재가 부호	string	Y	1
oprc_vrss_prpr	시가2 대비 현재가	string	Y	10
oprc_vrss_prpr_rate	시가2 대비 현재가 비율	string	Y	84
prd_rsfl	기간 등락	string	Y	10
prd_rsfl_rate	기간 등락 비율	string	Y	84
class StockFluctuationRankItem(BaseModel):
    pass


class StockFluctuationRank(BaseModel, KisHttpBody):
    """국내주식 등락률 순위"""

    output: Sequence[StockFluctuationRankItem] = Field(default_factory=list)


mksc_shrn_iscd	유가증권 단축 종목코드	string	Y	9
data_rank	데이터 순위	string	Y	10
hts_kor_isnm	HTS 한글 종목명	string	Y	40
stck_prpr	주식 현재가	string	Y	10
prdy_vrss	전일 대비	string	Y	10
prdy_vrss_sign	전일 대비 부호	string	Y	1
prdy_ctrt	전일 대비율	string	Y	82
acml_vol	누적 거래량	string	Y	18
total_askp_rsqn	총 매도호가 잔량	string	Y	12
total_bidp_rsqn	총 매수호가 잔량	string	Y	12
total_ntsl_bidp_rsqn	총 순 매수호가 잔량	string	Y	12
shnu_rsqn_rate	매수 잔량 비율	string	Y	84
seln_rsqn_rate	매도 잔량 비율	string	Y	84
class StockHogaQuantityRankItem(BaseModel):
    pass


class StockHogaQuantityRank(BaseModel, KisHttpBody):
    """국내주식 호가잔량 순위"""

    output: Sequence[StockHogaQuantityRankItem] = Field(default_factory=list)

data_rank	데이터 순위	string	Y	10
hts_kor_isnm	HTS 한글 종목명	string	Y	40
prdy_vrss_sign	전일 대비 부호	string	Y	1
mksc_shrn_iscd	유가증권 단축 종목코드	string	Y	9
stck_prpr	주식 현재가	string	Y	10
prdy_vrss	전일 대비	string	Y	10
prdy_ctrt	전일 대비율	string	Y	82
acml_vol	누적 거래량	string	Y	18
sale_totl_prfi	매출 총 이익	string	Y	182
bsop_prti	영업 이익	string	Y	182
op_prfi	경상 이익	string	Y	182
thtr_ntin	당기순이익	string	Y	102
total_aset	자산총계	string	Y	102
total_lblt	부채총계	string	Y	102
total_cptl	자본총계	string	Y	102
stac_month	결산 월	string	Y	2
stac_month_cls_code	결산 월 구분 코드	string	Y	2
iqry_csnu	조회 건수	string	Y	10
class StockProfitabilityIndicatorRankItem(BaseModel):
    pass


class StockProfitabilityIndicatorRank(BaseModel, KisHttpBody):
    """국내주식 수익자산지표 순위"""

    output: Sequence[StockProfitabilityIndicatorRankItem] = Field(default_factory=list) 

mksc_shrn_iscd	유가증권 단축 종목코드	string	Y	9
data_rank	데이터 순위	string	Y	10
hts_kor_isnm	HTS 한글 종목명	string	Y	40
stck_prpr	주식 현재가	string	Y	10
prdy_vrss	전일 대비	string	Y	10
prdy_vrss_sign	전일 대비 부호	string	Y	1
prdy_ctrt	전일 대비율	string	Y	82
acml_vol	누적 거래량	string	Y	18
lstn_stcn	상장 주수	string	Y	18
stck_avls	시가 총액	string	Y	18
mrkt_whol_avls_rlim	시장 전체 시가총액 비중	string	Y	52
class StockMarketCapTopItem(BaseModel):
    pass


class StockMarketCapTop(BaseModel, KisHttpBody):
    """국내주식 시가총액 상위"""

    output: Sequence[StockMarketCapTopItem] = Field(default_factory=list)

data_rank	데이터 순위	string	Y	10
hts_kor_isnm	HTS 한글 종목명	string	Y	40
mksc_shrn_iscd	유가증권 단축 종목코드	string	Y	9
stck_prpr	주식 현재가	string	Y	10
prdy_vrss	전일 대비	string	Y	10
prdy_vrss_sign	전일 대비 부호	string	Y	1
prdy_ctrt	전일 대비율	string	Y	82
acml_vol	누적 거래량	string	Y	18
cptl_op_prfi	총자본경상이익율	string	Y	92
cptl_ntin_rate	총자본 순이익율	string	Y	92
sale_totl_rate	매출액 총이익율	string	Y	92
sale_ntin_rate	매출액 순이익율	string	Y	92
bis	자기자본비율	string	Y	92
lblt_rate	부채 비율	string	Y	84
bram_depn	차입금 의존도	string	Y	92
rsrv_rate	유보 비율	string	Y	124
grs	매출액 증가율	string	Y	124
op_prfi_inrt	경상 이익 증가율	string	Y	124
bsop_prfi_inrt	영업 이익 증가율	string	Y	124
ntin_inrt	순이익 증가율	string	Y	124
equt_inrt	자기자본 증가율	string	Y	92
cptl_tnrt	총자본회전율	string	Y	92
sale_bond_tnrt	매출 채권 회전율	string	Y	92
totl_aset_inrt	총자산 증가율	string	Y	92
stac_month	결산 월	string	Y	2
stac_month_cls_code	결산 월 구분 코드	string	Y	2
iqry_csnu	조회 건수	string	Y	10
class StockFinanceRatioRankItem(BaseModel):
    pass


class StockFinanceRatioRank(BaseModel, KisHttpBody):
    """국내주식 재무비율 순위"""

    output: Sequence[StockFinanceRatioRankItem] = Field(default_factory=list)

stck_shrn_iscd	주식 단축 종목코드	string	Y	9
data_rank	데이터 순위	string	Y	10
hts_kor_isnm	HTS 한글 종목명	string	Y	40
stck_prpr	주식 현재가	string	Y	10
prdy_vrss	전일 대비	string	Y	10
prdy_vrss_sign	전일 대비 부호	string	Y	1
prdy_ctrt	전일 대비율	string	Y	82
ovtm_total_askp_rsqn	시간외 총 매도호가 잔량	string	Y	12
ovtm_total_bidp_rsqn	시간외 총 매수호가 잔량	string	Y	12
mkob_otcp_vol	장개시전 시간외종가 거래량	string	Y	18
mkfa_otcp_vol	장종료후 시간외종가 거래량	string	Y	18
class StockTimeHogaRankItem(BaseModel):
    pass


class StockTimeHogaRank(BaseModel,  KisHttpBody):
    """국내주식 시간외잔량 순위"""

    output: Sequence[StockTimeHogaRankItem] = Field(default_factory=list)

mksc_shrn_iscd	유가증권 단축 종목코드	string	Y	9
data_rank	데이터 순위	string	Y	10
hts_kor_isnm	HTS 한글 종목명	string	Y	10
stck_prpr	주식 현재가	string	Y	10
prdy_vrss	전일 대비	string	Y	10
prdy_vrss_sign	전일 대비 부호	string	Y	10
acml_vol	누적 거래량	string	Y	10
prst_iscd	우선주 종목코드	string	Y	10
prst_kor_isnm	우선주 한글 종목명	string	Y	10
prst_prpr	우선주 현재가	string	Y	10
prst_prdy_vrss	우선주 전일대비	string	Y	10
prst_prdy_vrss_sign	우선주 전일 대비 부호	string	Y	10
prst_acml_vol	우선주 누적 거래량	string	Y	40
diff_prpr	차이 현재가	string	Y	10
dprt	괴리율	string	Y	10
prdy_ctrt	전일 대비율	string	Y	1
prst_prdy_ctrt	우선주 전일 대비율	string	Y	82
class StockPreferredStockRatioTopItem(BaseModel):
    pass


class StockPreferredStockRatioTop(BaseModel, KisHttpBody):
    """국내주식 우선주/리리율 상위"""

    pass

mksc_shrn_iscd	유가증권 단축 종목코드	string	Y	9
data_rank	데이터 순위	string	Y	10
hts_kor_isnm	HTS 한글 종목명	string	Y	40
stck_prpr	주식 현재가	string	Y	10
prdy_vrss	전일 대비	string	Y	10
prdy_ctrt	전일 대비율	string	Y	82
prdy_vrss_sign	전일 대비 부호	string	Y	1
acml_vol	누적 거래량	string	Y	18
d5_dsrt	5일 이격도	string	Y	112
d10_dsrt	10일 이격도	string	Y	112
d20_dsrt	20일 이격도	string	Y	112
d60_dsrt	60일 이격도	string	Y	112
d120_dsrt	120일 이격도	string	Y	112
class StockDisparityIndexRankItem(BaseModel):
    pass


class StockDisparityIndexRank(BaseModel, KisHttpBody):
    """국내주식 이격도 순위"""

    output: Sequence[StockDisparityIndexRankItem] = Field(default_factory=list)

data_rank	데이터 순위	string	Y	10
hts_kor_isnm	HTS 한글 종목명	string	Y	40
mksc_shrn_iscd	유가증권 단축 종목코드	string	Y	9
stck_prpr	주식 현재가	string	Y	10
prdy_vrss	전일 대비	string	Y	10
prdy_vrss_sign	전일 대비 부호	string	Y	1
prdy_ctrt	전일 대비율	string	Y	82
acml_vol	누적 거래량	string	Y	18
per	PER	string	Y	82
pbr	PBR	string	Y	82
pcr	PCR	string	Y	82
psr	PSR	string	Y	82
eps	EPS	string	Y	112
eva	EVA	string	Y	82
ebitda	EBITDA	string	Y	82
pv_div_ebitda	PV DIV EBITDA	string	Y	82
ebitda_div_fnnc_expn	EBITDA DIV 금융비용	string	Y	82
stac_month	결산 월	string	Y	2
stac_month_cls_code	결산 월 구분 코드	string	Y	2
iqry_csnu	조회 건수	string	Y	10
class StockMarketPriceRankItem(BaseModel):
    pass


class StockMarketPriceRank(BaseModel, KisHttpBody):
    """국내주식 시장가치 순위"""

    output: Sequence[StockMarketPriceRankItem] = Field(default_factory=list)

stck_shrn_iscd	주식 단축 종목코드	string	Y	9
data_rank	데이터 순위	string	Y	10
hts_kor_isnm	HTS 한글 종목명	string	Y	40
stck_prpr	주식 현재가	string	Y	10
prdy_vrss	전일 대비	string	Y	10
prdy_vrss_sign	전일 대비 부호	string	Y	1
prdy_ctrt	전일 대비율	string	Y	82
acml_vol	누적 거래량	string	Y	18
tday_rltv	당일 체결강도	string	Y	112
seln_cnqn_smtn	매도 체결량 합계	string	Y	18
shnu_cnqn_smtn	매수2 체결량 합계	string	Y	18
class StockExecutionStrengthTopItem(BaseModel):
    pass


class StockExecutionStrengthTop(BaseModel, KisHttpBody):
    """국내주식 체결강도 상위"""

    pass

mrkt_div_cls_name	시장 분류 구분 명	string	Y	40
mksc_shrn_iscd	유가증권 단축 종목코드	string	Y	9
hts_kor_isnm	HTS 한글 종목명	string	Y	40
stck_prpr	주식 현재가	string	Y	10
prdy_vrss	전일 대비	string	Y	10
prdy_vrss_sign	전일 대비 부호	string	Y	1
prdy_ctrt	전일 대비율	string	Y	82
acml_vol	누적 거래량	string	Y	18
acml_tr_pbmn	누적 거래 대금	string	Y	18
askp	매도호가	string	Y	10
bidp	매수호가	string	Y	10
data_rank	데이터 순위	string	Y	10
inter_issu_reg_csnu	관심 종목 등록 건수	string	Y	10
class StockWatchlistRegistrationTopItem(BaseModel):
    pass


class StockWatchlistRegistrationTop(BaseModel, KisHttpBody):
    """국내주식 관심종목등록 상위"""

    output: Sequence[StockWatchlistRegistrationTopItem] = Field(default_factory=list)

stck_shrn_iscd	주식 단축 종목코드	string	Y	9
hts_kor_isnm	HTS 한글 종목명	string	Y	40
stck_prpr	주식 현재가	string	Y	10
prdy_vrss	전일 대비	string	Y	10
prdy_vrss_sign	전일 대비 부호	string	Y	1
prdy_ctrt	전일 대비율	string	Y	82
stck_sdpr	주식 기준가	string	Y	10
seln_rsqn	매도 잔량	string	Y	12
askp	매도호가	string	Y	10
bidp	매수호가	string	Y	10
shnu_rsqn	매수2 잔량	string	Y	12
cntg_vol	체결 거래량	string	Y	18
antc_tr_pbmn	체결 거래대금	string	Y	18
total_askp_rsqn	총 매도호가 잔량	string	Y	12
total_bidp_rsqn	총 매수호가 잔량	string	Y	12
class StockExpectedExecutionRiseDeclineTopItem(BaseModel):
    pass


class StockExpectedExecutionRiseDeclineTop(BaseModel, KisHttpBody):
    """국내주식 예상체결 상승/하락상위"""

    output: Sequence[StockExpectedExecutionRiseDeclineTopItem] = Field(default_factory=list)


data_rank	데이터 순위	string	Y	10
mksc_shrn_iscd	유가증권 단축 종목코드	string	Y	9
hts_kor_isnm	HTS 한글 종목명	string	Y	40
stck_prpr	주식 현재가	string	Y	10
prdy_vrss_sign	전일 대비 부호	string	Y	1
prdy_vrss	전일 대비	string	Y	10
prdy_ctrt	전일 대비율	string	Y	82
acml_vol	누적 거래량	string	Y	18
acml_tr_pbmn	누적 거래 대금	string	Y	18
seln_cnqn_smtn	매도 체결량 합계	string	Y	18
shnu_cnqn_smtn	매수2 체결량 합계	string	Y	18
ntby_cnqn	순매수 체결량	string	Y	18
class StockProprietaryTradingTopItem(BaseModel):
    pass


class StockProprietaryTradingTop(BaseModel, KisHttpBody):
    """국내주식 당사매매종목 상위"""

    output: Sequence[StockProprietaryTradingTopItem] = Field(default_factory=list)


hts_kor_isnm	HTS 한글 종목명	string	Y	40
mksc_shrn_iscd	유가증권 단축 종목코드	string	Y	9
stck_prpr	주식 현재가	string	Y	10
prdy_vrss_sign	전일 대비 부호	string	Y	1
prdy_vrss	전일 대비	string	Y	10
prdy_ctrt	전일 대비율	string	Y	82
askp	매도호가	string	Y	10
askp_rsqn1	매도호가 잔량1	string	Y	12
bidp	매수호가	string	Y	10
bidp_rsqn1	매수호가 잔량1	string	Y	12
acml_vol	누적 거래량	string	Y	18
new_hgpr	신 최고가	string	Y	10
hprc_near_rate	고가 근접 비율	string	Y	84
new_lwpr	신 최저가	string	Y	10
lwpr_near_rate	저가 근접 비율	string	Y	84
stck_sdpr	주식 기준가	string	Y	10
class StockNewHighLowApproachingTopItem(BaseModel):
    pass


class StockNewHighLowApproachingTop(BaseModel, KisHttpBody):
    """국내주식 신고/신저근접종목 상위"""

    output: Sequence[StockNewHighLowApproachingTopItem] = Field(default_factory=list)

rank	순위	string	Y	4
sht_cd	종목코드	string	Y	9
isin_name	종목명	string	Y	40
record_date	기준일	string	Y	8
per_sto_divi_amt	현금/주식배당금	string	Y	12
divi_rate	현금/주식배당률(%)	string	Y	62
divi_kind	배당종류	string	Y	8
class StockDividendYieldTopItem(BaseModel):
    pass


class StockDividendYieldTop(BaseModel, KisHttpBody):
    """국내주식 배당률 상위"""

    output1: Sequence[StockDividendYieldTopItem] = Field(default_factory=list)

mksc_shrn_iscd	유가증권 단축 종목코드	string	Y	9
data_rank	데이터 순위	string	Y	10
hts_kor_isnm	HTS 한글 종목명	string	Y	40
stck_prpr	주식 현재가	string	Y	10
prdy_vrss_sign	전일 대비 부호	string	Y	1
prdy_vrss	전일 대비	string	Y	10
prdy_ctrt	전일 대비율	string	Y	82
acml_vol	누적 거래량	string	Y	18
shnu_cntg_csnu	매수2 체결 건수	string	Y	10
seln_cntg_csnu	매도 체결 건수	string	Y	10
ntby_cnqn	순매수 체결량	string	Y	18
class StockLargeExecutionCountTopItem(BaseModel):
    pass


class StockLargeExecutionCountTop(BaseModel, KisHttpBody):
    """국내주식 대량체결건수 상위"""

    pass

mksc_shrn_iscd	유가증권 단축 종목코드	string	Y	9
hts_kor_isnm	HTS 한글 종목명	string	Y	40
stck_prpr	주식 현재가	string	Y	10
prdy_vrss	전일 대비	string	Y	10
prdy_vrss_sign	전일 대비 부호	string	Y	1
prdy_ctrt	전일 대비율	string	Y	82
acml_vol	누적 거래량	string	Y	18
acml_tr_pbmn	누적 거래 대금	string	Y	18
ssts_cntg_qty	공매도 체결 수량	string	Y	12
ssts_vol_rlim	공매도 거래량 비중	string	Y	62
ssts_tr_pbmn	공매도 거래 대금	string	Y	18
ssts_tr_pbmn_rlim	공매도 거래대금 비중	string	Y	62
stnd_date1	기준 일자1	string	Y	8
stnd_date2	기준 일자2	string	Y	8
avrg_prc	평균가격	string	Y	11
class StockCreditBalanceTopItem(BaseModel):
    pass


class StockCreditBalanceTop(BaseModel, KisHttpBody):
    """국내주식 신용잔고 상위"""

    output: Sequence[StockCreditBalanceTopItem] = Field(default_factory=list)


ovtm_untp_uplm_issu_cnt	시간외 단일가 상한 종목 수             	string	Y	7
ovtm_untp_ascn_issu_cnt	시간외 단일가 상승 종목 수         	string	Y	7
ovtm_untp_stnr_issu_cnt	시간외 단일가 보합 종목 수      	string	Y	7
ovtm_untp_lslm_issu_cnt	시간외 단일가 하한 종목 수          	string	Y	7
ovtm_untp_down_issu_cnt	시간외 단일가 하락 종목 수              	string	Y	7
ovtm_untp_acml_vol	시간외 단일가 누적 거래량  	string	Y	19
ovtm_untp_acml_tr_pbmn	 시간외 단일가 누적 거래대금 	string	Y	19
ovtm_untp_exch_vol	시간외 단일가 거래소 거래량	string	Y	18
ovtm_untp_exch_tr_pbmn	시간외 단일가 거래소 거래대금	string	Y	18
ovtm_untp_kosdaq_vol	시간외 단일가 KOSDAQ 거래량              	string	Y	18
ovtm_untp_kosdaq_tr_pbmn	시간외 단일가 KOSDAQ 거래대금         	string	Y	18
class StockShortSellingTopItem1(BaseModel):
    pass

mksc_shrn_iscd	유가증권 단축 종목코드	string	Y	9
hts_kor_isnm	HTS 한글 종목명	string	Y	40
ovtm_untp_prpr	시간외 단일가 현재가	string	Y	10
ovtm_untp_prdy_vrss	시간외 단일가 전일 대비	string	Y	10
ovtm_untp_prdy_vrss_sign	시간외 단일가 전일 대비 부호	string	Y	1
ovtm_untp_prdy_ctrt	시간외 단일가 전일 대비율	string	Y	82
ovtm_untp_askp1	시간외 단일가 매도호가1       	string	Y	10
ovtm_untp_seln_rsqn	시간외 단일가 매도 잔량       	string	Y	12
ovtm_untp_bidp1	시간외 단일가 매수호가1       	string	Y	10
ovtm_untp_shnu_rsqn	시간외 단일가 매수 잔량       	string	Y	12
ovtm_untp_vol	시간외 단일가 거래량	string	Y	18
ovtm_vrss_acml_vol_rlim	시간외 대비 누적 거래량 비중  	string	Y	52
stck_prpr	주식 현재가	string	Y	10
acml_vol	누적 거래량	string	Y	18
bidp	매수호가	string	Y	10
askp	매도호가	string	Y	10
class StockShortSellingTopItem2(BaseModel):
    pass

class StockShortSellingTop(BaseModel, KisHttpBody):
    """국내주식 공매도 상위종목"""

    output1: StockShortSellingTopItem1 = Field(title="응답상세1")
    output2: Sequence[StockShortSellingTopItem2] = Field(default_factory=list)

ovtm_untp_uplm_issu_cnt	시간외 단일가 상한 종목 수             	string	Y	7
ovtm_untp_ascn_issu_cnt	시간외 단일가 상승 종목 수         	string	Y	7
ovtm_untp_stnr_issu_cnt	시간외 단일가 보합 종목 수      	string	Y	7
ovtm_untp_lslm_issu_cnt	시간외 단일가 하한 종목 수          	string	Y	7
ovtm_untp_down_issu_cnt	시간외 단일가 하락 종목 수              	string	Y	7
ovtm_untp_acml_vol	시간외 단일가 누적 거래량  	string	Y	19
ovtm_untp_acml_tr_pbmn	 시간외 단일가 누적 거래대금 	string	Y	19
ovtm_untp_exch_vol	시간외 단일가 거래소 거래량	string	Y	18
ovtm_untp_exch_tr_pbmn	시간외 단일가 거래소 거래대금	string	Y	18
ovtm_untp_kosdaq_vol	시간외 단일가 KOSDAQ 거래량              	string	Y	18
ovtm_untp_kosdaq_tr_pbmn	시간외 단일가 KOSDAQ 거래대금         	string	Y	18
class StockAfterHoursFluctuationRankItem1(BaseModel):
    pass

mksc_shrn_iscd	유가증권 단축 종목코드	string	Y	9
hts_kor_isnm	HTS 한글 종목명	string	Y	40
ovtm_untp_prpr	시간외 단일가 현재가	string	Y	10
ovtm_untp_prdy_vrss	시간외 단일가 전일 대비	string	Y	10
ovtm_untp_prdy_vrss_sign	시간외 단일가 전일 대비 부호	string	Y	1
ovtm_untp_prdy_ctrt	시간외 단일가 전일 대비율	string	Y	82
ovtm_untp_askp1	시간외 단일가 매도호가1       	string	Y	10
ovtm_untp_seln_rsqn	시간외 단일가 매도 잔량       	string	Y	12
ovtm_untp_bidp1	시간외 단일가 매수호가1       	string	Y	10
ovtm_untp_shnu_rsqn	시간외 단일가 매수 잔량       	string	Y	12
ovtm_untp_vol	시간외 단일가 거래량	string	Y	18
ovtm_vrss_acml_vol_rlim	시간외 대비 누적 거래량 비중  	string	Y	52
stck_prpr	주식 현재가	string	Y	10
acml_vol	누적 거래량	string	Y	18
bidp	매수호가	string	Y	10
askp	매도호가	string	Y	10
class StockAfterHoursFluctuationRankItem2(BaseModel):
    pass

class StockAfterHoursFluctuationRank(BaseModel, KisHttpBody):
    """국내주식 시간외등락율순위"""

    output1: StockAfterHoursFluctuationRankItem1 = Field(title="응답상세1")
    output2: Sequence[StockAfterHoursFluctuationRankItem2] = Field(default_factory=list)


ovtm_untp_exch_vol	시간외 단일가 거래소 거래량	string	Y	18
ovtm_untp_exch_tr_pbmn	시간외 단일가 거래소 거래대금	string	Y	18
ovtm_untp_kosdaq_vol	시간외 단일가 KOSDAQ 거래량	string	Y	18
ovtm_untp_kosdaq_tr_pbmn	시간외 단일가 KOSDAQ 거래대금	string	Y	18
class StockAfterHoursVolumeRankItem1(BaseModel):
    pass

stck_shrn_iscd	주식 단축 종목코드	string	Y	9
hts_kor_isnm	HTS 한글 종목명	string	Y	40
ovtm_untp_prpr	시간외 단일가 현재가	string	Y	10
ovtm_untp_prdy_vrss	시간외 단일가 전일 대비	string	Y	10
ovtm_untp_prdy_vrss_sign	시간외 단일가 전일 대비 부호	string	Y	1
ovtm_untp_prdy_ctrt	시간외 단일가 전일 대비율	string	Y	82
ovtm_untp_seln_rsqn	시간외 단일가 매도 잔량	string	Y	12
ovtm_untp_shnu_rsqn	시간외 단일가 매수 잔량	string	Y	12
ovtm_untp_vol	시간외 단일가 거래량	string	Y	18
ovtm_vrss_acml_vol_rlim	시간외 대비 누적 거래량 비중	string	Y	52
stck_prpr	주식 현재가	string	Y	10
acml_vol	누적 거래량	string	Y	18
bidp	매수호가	string	Y	10
askp	매도호가	string	Y	10
class StockAfterHoursVolumeRankItem2(BaseModel):
    pass


class StockAfterHoursVolumeRank(BaseModel, KisHttpBody):
    """국내주식 시간외거래량순위"""

    output1: StockAfterHoursVolumeRankItem1 = Field(title="응답상세1")
    output2: Sequence[StockAfterHoursVolumeRankItem2] = Field(default_factory=list)

mrkt_div_cls_code	시장구분	string	Y	9	 J : 코스피, Q : 코스닥
mksc_shrn_iscd	종목코드	string	Y	2	종목코드
class HtsInquiryTop20Item(BaseModel):
    pass


class HtsInquiryTop20(BaseModel, KisHttpBody):
    """HTS조회상위20종목"""

    output1: Sequence[HtsInquiryTop20Item] = Field(default_factory=list)
