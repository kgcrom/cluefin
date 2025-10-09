from pydantic import BaseModel, Field
from cluefin_openapi.kis._model import KisHttpBody
from typing import Sequence, Optional, Literal

zdiv	소수점자리수	string	Y	1
stat	거래상태	string	Y	20
nrec	RecordCount	string	Y	4
class StockPriceRiseFallItem1(BaseModel):
    pass

rsym	실시간조회심볼	string	Y	16
excd	거래소코드	string	Y	4
symb	종목코드	string	Y	16
knam	종목명	string	Y	48
last	현재가	string	Y	12
sign	기호	string	Y	1
diff	대비	string	Y	12
rate	등락율	string	Y	12
tvol	거래량	string	Y	14
pask	매도호가	string	Y	12
pbid	매수호가	string	Y	12
n_base	기준가격	string	Y	12
n_diff	기준가격대비	string	Y	12
n_rate	기준가격대비율	string	Y	12
enam	영문종목명	string	Y	48
e_ordyn	매매가능	string	Y	2
class StockPriceRiseFallItem2(BaseModel):
    pass


class StockPriceRiseFall(BaseModel, KisHttpBody):
    """해외주식 가격급등락"""

    output1: StockPriceRiseFallItem1 = Field(title="응답상세1")
    output2: Sequence[StockPriceRiseFallItem2] = Field(default_factory=list)

zdiv	소수점자리수	string	Y	1
stat	거래상태	string	Y	20
nrec	RecordCount	string	Y	4
class StockVolumeSurgeItem1(BaseModel):
    pass

rsym	실시간조회심볼	string	Y	16
excd	거래소코드	string	Y	4
symb	종목코드	string	Y	16
knam	종목명	string	Y	48
last	현재가	string	Y	12
sign	기호	string	Y	1
diff	대비	string	Y	12
rate	등락율	string	Y	12
tvol	거래량	string	Y	14
pask	매도호가	string	Y	12
pbid	매수호가	string	Y	12
n_tvol	기준거래량	string	Y	14
n_diff	증가량	string	Y	12
n_rate	증가율	string	Y	12
enam	영문종목명	string	Y	48
e_ordyn	매매가능	string	Y	2
class StockVolumeSurgeItem2(BaseModel):
    pass


class StockVolumeSurge(BaseModel, KisHttpBody):
    """해외주식 거래량급증"""

    output1: StockVolumeSurgeItem1 = Field(title="응답상세1")
    output2: Sequence[StockVolumeSurgeItem2] = Field(default_factory=list)


zdiv	소수점자리수	string	Y	1
stat	거래상태	string	Y	20
nrec	RecordCount	string	Y	4
class StockBuyExecutionStrengthTopItem1(BaseModel):
    pass

rsym	실시간조회심볼	string	Y	16
excd	거래소코드	string	Y	4
symb	종목코드	string	Y	16
knam	종목명	string	Y	48
last	현재가	string	Y	12
sign	기호	string	Y	1
diff	대비	string	Y	12
rate	등락율	string	Y	12
tvol	거래량	string	Y	14
pask	매도호가	string	Y	12
pbid	매수호가	string	Y	12
tpow	당일체결강도	string	Y	10
powx	체결강도	string	Y	10
enam	영문종목명	string	Y	48
e_ordyn	매매가능	string	Y	2
class StockBuyExecutionStrengthTopItem2(BaseModel):
    pass

class StockBuyExecutionStrengthTop(BaseModel, KisHttpBody):
    """해외주식 매수체결강도상위"""

    output1: StockBuyExecutionStrengthTopItem1 = Field(title="응답상세1")
    output2: Sequence[StockBuyExecutionStrengthTopItem2] = Field(default_factory=list)

zdiv	소수점자리수	string	Y	1
stat	거래상태정보	string	Y	20
crec	현재Count	string	Y	6
trec	전체조회종목수	string	Y	6
nrec	RecordCount	string	Y	4
class StockRiseDeclineRateItem1(BaseModel):
    pass

rsym	실시간조회심볼	string	Y	16
excd	거래소코드	string	Y	4
symb	종목코드	string	Y	1
name	종목명	string	Y	48
last	현재가	string	Y	16
sign	기호	string	Y	1
diff	대비	string	Y	12
rate	등락율	string	Y	12
tvol	거래량	string	Y	14
pask	매도호가	string	Y	12
pbid	매수호가	string	Y	12
n_base	기준가격	string	Y	12
n_diff	기준가격대비	string	Y	12
n_rate	기준가격대비율	string	Y	12
rank	순위	string	Y	6
ename	영문종목명	string	Y	48
e_ordyn	매매가능	string	Y	2
class StockRiseDeclineRateItem2(BaseModel):
    pass

class StockRiseDeclineRate(BaseModel, KisHttpBody):
    """해외주식 상승률/하락율"""

    output1: StockRiseDeclineRateItem1 = Field(title="응답상세1")
    output2: Sequence[StockRiseDeclineRateItem2] = Field(default_factory=list)


zdiv	소수점자리수	string	Y	1
stat	거래상태정보	string	Y	20
nrec	RecordCount	string	Y	4
class StockNewHighLowPriceItem1(BaseModel):
    pass

rsym	실시간조회심볼	string	Y	16
excd	거래소코드	string	Y	4
symb	종목코드	string	Y	1
name	종목명	string	Y	48
last	현재가	string	Y	16
sign	기호	string	Y	1
diff	대비	string	Y	12
rate	등락율	string	Y	12
tvol	거래량	string	Y	14
pask	매도호가	string	Y	12
pbid	매수호가	string	Y	12
n_base	기준가	string	Y	12
n_diff	기준가대비	string	Y	12
n_rate	기준가대비율	string	Y	12
ename	영문종목명	string	Y	48
e_ordyn	매매가능	string	Y	2
class StockNewHighLowPriceItem2(BaseModel):
    pass


class StockNewHighLowPrice(BaseModel, KisHttpBody):
    """해외주식 신고/신저가"""

    output: StockNewHighLowPriceItem1 = Field(title="응답상세1")
    output2: Sequence[StockNewHighLowPriceItem2] = Field(default_factory=list)

zdiv	소수점자리수	string	Y	1
stat	거래상태정보	string	Y	20
crec	현재조회종목수	string	Y	6
trec	전체조회종목수	string	Y	6
nrec	RecordCount	string	Y	4
class StockTradingVolumeRankItem1(BaseModel):
    pass

rsym	실시간조회심볼	string	Y	16
excd	거래소코드	string	Y	4
symb	종목코드	string	Y	1
name	종목명	string	Y	48
last	현재가	string	Y	16
sign	기호	string	Y	1
diff	대비	string	Y	12
rate	등락율	string	Y	12
pask	매도호가	string	Y	12
pbid	매수호가	string	Y	12
tvol	거래량	string	Y	14
tamt	거래대금	string	Y	14
a_tvol	평균거래량	string	Y	14
rank	순위	string	Y	6
ename	영문종목명	string	Y	48
e_ordyn	매매가능	string	Y	2
class StockTradingVolumeRankItem2(BaseModel):
    pass

class StockTradingVolumeRank(BaseModel, KisHttpBody):
    """해외주식 거래량순위"""

    output: StockTradingVolumeRankItem1 = Field(title="응답상세1")
    output2: Sequence[StockTradingVolumeRankItem2] = Field(default_factory=list)

zdiv	소수점자리수	string	Y	1
stat	거래상태정보	string	Y	20
crec	현재조회종목수	string	Y	6
trec	전체조회종목수	string	Y	6
nrec	RecordCount	string	Y	4
class StockTradingAmountRankItem1(BaseModel):
    pass

rsym	실시간조회심볼	string	Y	16
excd	거래소코드	string	Y	4
symb	종목코드	string	Y	1
name	종목명	string	Y	48
last	현재가	string	Y	16
sign	기호	string	Y	1
diff	대비	string	Y	12
rate	등락율	string	Y	12
pask	매도호가	string	Y	12
pbid	매수호가	string	Y	12
tvol	거래량	string	Y	14
tamt	거래대금	string	Y	14
a_tamt	평균거래대금	string	Y	14
rank	순위	string	Y	6
ename	영문종목명	string	Y	48
e_ordyn	매매가능	string	Y	2
class StockTradingAmountRankItem2(BaseModel):
    pass

class StockTradingAmountRank(BaseModel, KisHttpBody):
    """해외주식 거래대금순위"""

    output1: StockTradingAmountRankItem1 = Field(title="응답상세1")
    output2: Sequence[StockTradingAmountRankItem2] = Field(default_factory=list)

zdiv	소수점자리수	string	Y	1
stat	거래상태정보	string	Y	20
crec	현재조회종목수	string	Y	6
trec	전체조회종목수	string	Y	6
nrec	RecordCount	string	Y	4
class StockTradingIncreaseRateRankItem1(BaseModel):
    pass

rsym	실시간조회심볼	string	Y	16
excd	거래소코드	string	Y	4
symb	종목코드	string	Y	1
name	종목명	string	Y	48
last	현재가	string	Y	16
sign	기호	string	Y	1
diff	대비	string	Y	12
rate	등락율	string	Y	12
pask	매도호가	string	Y	12
pbid	매수호가	string	Y	12
tvol	거래량	string	Y	14
n_tvol	평균거래량	string	Y	14
n_rate	증가율	string	Y	12
rank	순위	string	Y	6
ename	영문종목명	string	Y	48
e_ordyn	매매가능	string	Y	2
class StockTradingIncreaseRateRankItem2(BaseModel):
    pass


class StockTradingIncreaseRateRank(BaseModel, KisHttpBody):
    """해외주식 거래증가율순위"""

    output1: StockTradingIncreaseRateRankItem1 = Field(title="응답상세1")
    output2: Sequence[StockTradingIncreaseRateRankItem2] = Field(default_factory=list)


zdiv	소수점자리수	string	Y	1
stat	거래상태정보	string	Y	20
crec	현재조회종목수	string	Y	6
trec	전체조회종목수	string	Y	6
nrec	RecordCount	string	Y	4
class StockTradingTurnoverRateRankItem1(BaseModel):
    pass

rsym	실시간조회심볼	string	Y	16
excd	거래소코드	string	Y	4
symb	종목코드	string	Y	1
name	종목명	string	Y	48
last	현재가	string	Y	16
sign	기호	string	Y	1
diff	대비	string	Y	12
rate	등락율	string	Y	12
tvol	거래량	string	Y	14
pask	매도호가	string	Y	12
pbid	매수호가	string	Y	12
n_tvol	평균거래량	string	Y	14
shar	상장주식수	string	Y	16
tover	회전율	string	Y	10
rank	순위	string	Y	6
ename	영문종목명	string	Y	48
e_ordyn	매매가능	string	Y	2
class StockTradingTurnoverRateRankItem2(BaseModel):
    pass


class StockTradingTurnoverRateRank(BaseModel, KisHttpBody):
    """해외주식 거래회전율순위"""

    output1: StockTradingTurnoverRateRankItem1 = Field(title="응답상세1")
    output2: Sequence[StockTradingTurnoverRateRankItem2] = Field(default_factory=list)

zdiv	소수점자리수	string	Y	1
stat	거래상태정보	string	Y	20
crec	현재조회종목수	string	Y	6
trec	전체조회종목수	string	Y	6
nrec	RecordCount	string	Y	4
class StockMarketCapRankItem1(BaseModel):
    pass

rsym	실시간조회심볼	string	Y	16
excd	거래소코드	string	Y	4
symb	종목코드	string	Y	1
name	종목명	string	Y	48
last	현재가	string	Y	16
sign	기호	string	Y	1
diff	대비	string	Y	12
rate	등락율	string	Y	12
tvol	거래량	string	Y	14
shar	상장주식수	string	Y	16
tomv	시가총액	string	Y	16
grav	비중	string	Y	10
rank	순위	string	Y	6
ename	영문종목명	string	Y	48
e_ordyn	매매가능	string	Y	2
class StockMarketCapRankItem2(BaseModel):
    pass

class StockMarketCapRank(BaseModel, KisHttpBody):
    """해외주식 시가총액순위"""

    output1: StockMarketCapRankItem1 = Field(title="응답상세1")
    output2: Sequence[StockMarketCapRankItem2] = Field(default_factory=list)

bass_dt	기준일자	string	Y	8
rght_type_cd	권리유형코드	string	Y	2
pdno	상품번호	string	Y	12
prdt_name	상품명	string	Y	60
prdt_type_cd	상품유형코드	string	Y	3
std_pdno	표준상품번호	string	Y	12
acpl_bass_dt	현지기준일자	string	Y	8
sbsc_strt_dt	청약시작일자	string	Y	8
sbsc_end_dt	청약종료일자	string	Y	8
cash_alct_rt	현금배정비율	string	Y	191
stck_alct_rt	주식배정비율	string	Y	2012
crcy_cd	통화코드	string	Y	3
crcy_cd2	통화코드2	string	Y	3
crcy_cd3	통화코드3	string	Y	3
crcy_cd4	통화코드4	string	Y	3
alct_frcr_unpr	배정외화단가	string	Y	195
stkp_dvdn_frcr_amt2	주당배당외화금액2	string	Y	195
stkp_dvdn_frcr_amt3	주당배당외화금액3	string	Y	195
stkp_dvdn_frcr_amt4	주당배당외화금액4	string	Y	195
dfnt_yn	확정여부	string	Y	1
class StockPeriodRightsInquiryItem(BaseModel):
    pass


class StockPeriodRightsInquiry(BaseModel, KisHttpBody):
    """해외주식 기간별권리조회"""

    output: StockPeriodRightsInquiryItem = Field(title="응답상세")

info_gb	뉴스구분	string	Y	1
news_key	뉴스키	string	Y	20
data_dt	조회일자	string	Y	8
data_tm	조회시간	string	Y	6
class_cd	중분류	string	Y	2
class_name	중분류명	string	Y	20
source	자료원	string	Y	20
nation_cd	국가코드	string	Y	2
exchange_cd	거래소코드	string	Y	3
symb	종목코드	string	Y	20
symb_name	종목명	string	Y	48
title	제목	string	Y	128
class NewsAggregateTitleItem(BaseModel):
    pass


class NewsAggregateTitle(BaseModel, KisHttpBody):
    """해외뉴스종합(제목)"""

    outblock1: Sequence[NewsAggregateTitleItem] = Field(default_factory=list)

anno_dt	ICE공시일	string	Y	8
ca_title	권리유형	string	Y	12
div_lock_dt	배당락일	string	Y	8
pay_dt	지급일	string	Y	8
record_dt	기준일	string	Y	8
validity_dt	효력일자	string	Y	8
local_end_dt	현지지시마감일	string	Y	8
lock_dt	권리락일	string	Y	8
delist_dt	상장폐지일	string	Y	8
redempt_dt	상환일자	string	Y	8
early_redempt_dt	조기상환일자	string	Y	8
effective_dt	적용일	string	Y	8
class StockRightsAggregateItem(BaseModel):
    pass


class StockRightsAggregate(BaseModel, KisHttpBody):
    """해외주식 권리종합"""

    output1: Sequence[StockRightsAggregateItem] = Field(default_factory=list)

pdno	상품번호	string	Y	12	
ovrs_item_name	해외종목명	string	Y	60	
loan_rt	대출비율	string	Y	238	
mgge_mntn_rt	담보유지비율	string	Y	238	
mgge_ensu_rt	담보확보비율	string	Y	238	
loan_exec_psbl_yn	대출실행가능여부	string	Y	1	
stff_name	직원명	string	Y	60	
erlm_dt	등록일자	string	Y	8	
tr_mket_name	거래시장명	string	Y	60	
crcy_cd	통화코드	string	Y	3	
natn_kor_name	국가한글명	string	Y	60	
ovrs_excg_cd	해외거래소코드	string	Y	4	
class StockCollateralLoanEligibleItem1(BaseModel):
    pass

loan_psbl_item_num	대출가능종목수	string	Y	20
class StockCollateralLoanEligibleItem2(BaseModel):
    pass


class StockCollateralLoanEligible(BaseModel, KisHttpBody):
    """당사 해외주식담보대출 가능 종목"""

    output1: Sequence[StockCollateralLoanEligibleItem1] = Field(default_factory=list)
    output2: Sequence[StockCollateralLoanEligibleItem2] = Field(default_factory=list)

cntt_usiq_srno	내용조회용일련번호	string	Y	20
news_ofer_entp_code	뉴스제공업체코드	string	Y	1
data_dt	작성일자	string	Y	8
data_tm	작성시간	string	Y	6
hts_pbnt_titl_cntt	HTS공시제목내용	string	Y	400
news_lrdv_code	뉴스대구분	string	Y	8
dorg	자료원	string	Y	20
iscd1	종목코드1	string	Y	9
iscd2	종목코드2	string	Y	9
iscd3	종목코드3	string	Y	9
iscd4	종목코드4	string	Y	9
iscd5	종목코드5	string	Y	9
iscd6	종목코드6	string	Y	9
iscd7	종목코드7	string	Y	9
iscd8	종목코드8	string	Y	9
iscd9	종목코드9	string	Y	9
iscd10	종목코드10	string	Y	9
kor_isnm1	한글종목명1	string	Y	40
kor_isnm2	한글종목명2	string	Y	40
kor_isnm3	한글종목명3	string	Y	40
kor_isnm4	한글종목명4	string	Y	40
kor_isnm5	한글종목명5	string	Y	40
kor_isnm6	한글종목명6	string	Y	40
kor_isnm7	한글종목명7	string	Y	40
kor_isnm8	한글종목명8	string	Y	40
kor_isnm9	한글종목명9	string	Y	40
kor_isnm10	한글종목명10	string	Y	40
class BreakingNewsTitleItem(BaseModel):
    pass


class BreakingNewsTitle(BaseModel, KisHttpBody):
    """해외속보(제목)"""

    output: Sequence[BreakingNewsTitleItem] = Field(default_factory=list)
