from pydantic import BaseModel, Field
from cluefin_openapi.kis._model import KisHttpBody
from typing import Sequence, Optional, Literal

class StockPriceRiseFallItem1(BaseModel):
    zdiv: str = Field(title="소수점자리수", max_length=1)
    stat: str = Field(title="거래상태", max_length=20)
    nrec: str = Field(title="RecordCount", max_length=4)

class StockPriceRiseFallItem2(BaseModel):
    rsym: str = Field(title="실시간조회심볼", max_length=16)
    excd: str = Field(title="거래소코드", max_length=4)
    symb: str = Field(title="종목코드", max_length=16)
    knam: str = Field(title="종목명", max_length=48)
    last: str = Field(title="현재가", max_length=12)
    sign: str = Field(title="기호", max_length=1)
    diff: str = Field(title="대비", max_length=12)
    rate: str = Field(title="등락율", max_length=12)
    tvol: str = Field(title="거래량", max_length=14)
    pask: str = Field(title="매도호가", max_length=12)
    pbid: str = Field(title="매수호가", max_length=12)
    n_base: str = Field(title="기준가격", max_length=12)
    n_diff: str = Field(title="기준가격대비", max_length=12)
    n_rate: str = Field(title="기준가격대비율", max_length=12)
    enam: str = Field(title="영문종목명", max_length=48)
    e_ordyn: str = Field(title="매매가능", max_length=2)


class StockPriceRiseFall(BaseModel, KisHttpBody):
    """해외주식 가격급등락"""

    output1: StockPriceRiseFallItem1 = Field(title="응답상세1")
    output2: Sequence[StockPriceRiseFallItem2] = Field(default_factory=list)

class StockVolumeSurgeItem1(BaseModel):
    zdiv: str = Field(title="소수점자리수", max_length=1)
    stat: str = Field(title="거래상태", max_length=20)
    nrec: str = Field(title="RecordCount", max_length=4)

class StockVolumeSurgeItem2(BaseModel):
    rsym: str = Field(title="실시간조회심볼", max_length=16)
    excd: str = Field(title="거래소코드", max_length=4)
    symb: str = Field(title="종목코드", max_length=16)
    knam: str = Field(title="종목명", max_length=48)
    last: str = Field(title="현재가", max_length=12)
    sign: str = Field(title="기호", max_length=1)
    diff: str = Field(title="대비", max_length=12)
    rate: str = Field(title="등락율", max_length=12)
    tvol: str = Field(title="거래량", max_length=14)
    pask: str = Field(title="매도호가", max_length=12)
    pbid: str = Field(title="매수호가", max_length=12)
    n_tvol: str = Field(title="기준거래량", max_length=14)
    n_diff: str = Field(title="증가량", max_length=12)
    n_rate: str = Field(title="증가율", max_length=12)
    enam: str = Field(title="영문종목명", max_length=48)
    e_ordyn: str = Field(title="매매가능", max_length=2)


class StockVolumeSurge(BaseModel, KisHttpBody):
    """해외주식 거래량급증"""

    output1: StockVolumeSurgeItem1 = Field(title="응답상세1")
    output2: Sequence[StockVolumeSurgeItem2] = Field(default_factory=list)


class StockBuyExecutionStrengthTopItem1(BaseModel):
    zdiv: str = Field(title="소수점자리수", max_length=1)
    stat: str = Field(title="거래상태", max_length=20)
    nrec: str = Field(title="RecordCount", max_length=4)

class StockBuyExecutionStrengthTopItem2(BaseModel):
    rsym: str = Field(title="실시간조회심볼", max_length=16)
    excd: str = Field(title="거래소코드", max_length=4)
    symb: str = Field(title="종목코드", max_length=16)
    knam: str = Field(title="종목명", max_length=48)
    last: str = Field(title="현재가", max_length=12)
    sign: str = Field(title="기호", max_length=1)
    diff: str = Field(title="대비", max_length=12)
    rate: str = Field(title="등락율", max_length=12)
    tvol: str = Field(title="거래량", max_length=14)
    pask: str = Field(title="매도호가", max_length=12)
    pbid: str = Field(title="매수호가", max_length=12)
    tpow: str = Field(title="당일체결강도", max_length=10)
    powx: str = Field(title="체결강도", max_length=10)
    enam: str = Field(title="영문종목명", max_length=48)
    e_ordyn: str = Field(title="매매가능", max_length=2)

class StockBuyExecutionStrengthTop(BaseModel, KisHttpBody):
    """해외주식 매수체결강도상위"""

    output1: StockBuyExecutionStrengthTopItem1 = Field(title="응답상세1")
    output2: Sequence[StockBuyExecutionStrengthTopItem2] = Field(default_factory=list)

class StockRiseDeclineRateItem1(BaseModel):
    zdiv: str = Field(title="소수점자리수", max_length=1)
    stat: str = Field(title="거래상태정보", max_length=20)
    crec: str = Field(title="현재Count", max_length=6)
    trec: str = Field(title="전체조회종목수", max_length=6)
    nrec: str = Field(title="RecordCount", max_length=4)

class StockRiseDeclineRateItem2(BaseModel):
    rsym: str = Field(title="실시간조회심볼", max_length=16)
    excd: str = Field(title="거래소코드", max_length=4)
    symb: str = Field(title="종목코드", max_length=1)
    name: str = Field(title="종목명", max_length=48)
    last: str = Field(title="현재가", max_length=16)
    sign: str = Field(title="기호", max_length=1)
    diff: str = Field(title="대비", max_length=12)
    rate: str = Field(title="등락율", max_length=12)
    tvol: str = Field(title="거래량", max_length=14)
    pask: str = Field(title="매도호가", max_length=12)
    pbid: str = Field(title="매수호가", max_length=12)
    n_base: str = Field(title="기준가격", max_length=12)
    n_diff: str = Field(title="기준가격대비", max_length=12)
    n_rate: str = Field(title="기준가격대비율", max_length=12)
    rank: str = Field(title="순위", max_length=6)
    ename: str = Field(title="영문종목명", max_length=48)
    e_ordyn: str = Field(title="매매가능", max_length=2)

class StockRiseDeclineRate(BaseModel, KisHttpBody):
    """해외주식 상승률/하락율"""

    output1: StockRiseDeclineRateItem1 = Field(title="응답상세1")
    output2: Sequence[StockRiseDeclineRateItem2] = Field(default_factory=list)


class StockNewHighLowPriceItem1(BaseModel):
    zdiv: str = Field(title="소수점자리수", max_length=1)
    stat: str = Field(title="거래상태정보", max_length=20)
    nrec: str = Field(title="RecordCount", max_length=4)

class StockNewHighLowPriceItem2(BaseModel):
    rsym: str = Field(title="실시간조회심볼", max_length=16)
    excd: str = Field(title="거래소코드", max_length=4)
    symb: str = Field(title="종목코드", max_length=1)
    name: str = Field(title="종목명", max_length=48)
    last: str = Field(title="현재가", max_length=16)
    sign: str = Field(title="기호", max_length=1)
    diff: str = Field(title="대비", max_length=12)
    rate: str = Field(title="등락율", max_length=12)
    tvol: str = Field(title="거래량", max_length=14)
    pask: str = Field(title="매도호가", max_length=12)
    pbid: str = Field(title="매수호가", max_length=12)
    n_base: str = Field(title="기준가", max_length=12)
    n_diff: str = Field(title="기준가대비", max_length=12)
    n_rate: str = Field(title="기준가대비율", max_length=12)
    ename: str = Field(title="영문종목명", max_length=48)
    e_ordyn: str = Field(title="매매가능", max_length=2)


class StockNewHighLowPrice(BaseModel, KisHttpBody):
    """해외주식 신고/신저가"""

    output: StockNewHighLowPriceItem1 = Field(title="응답상세1")
    output2: Sequence[StockNewHighLowPriceItem2] = Field(default_factory=list)

class StockTradingVolumeRankItem1(BaseModel):
    zdiv: str = Field(title="소수점자리수", max_length=1)
    stat: str = Field(title="거래상태정보", max_length=20)
    crec: str = Field(title="현재조회종목수", max_length=6)
    trec: str = Field(title="전체조회종목수", max_length=6)
    nrec: str = Field(title="RecordCount", max_length=4)

class StockTradingVolumeRankItem2(BaseModel):
    rsym: str = Field(title="실시간조회심볼", max_length=16)
    excd: str = Field(title="거래소코드", max_length=4)
    symb: str = Field(title="종목코드", max_length=1)
    name: str = Field(title="종목명", max_length=48)
    last: str = Field(title="현재가", max_length=16)
    sign: str = Field(title="기호", max_length=1)
    diff: str = Field(title="대비", max_length=12)
    rate: str = Field(title="등락율", max_length=12)
    pask: str = Field(title="매도호가", max_length=12)
    pbid: str = Field(title="매수호가", max_length=12)
    tvol: str = Field(title="거래량", max_length=14)
    tamt: str = Field(title="거래대금", max_length=14)
    a_tvol: str = Field(title="평균거래량", max_length=14)
    rank: str = Field(title="순위", max_length=6)
    ename: str = Field(title="영문종목명", max_length=48)
    e_ordyn: str = Field(title="매매가능", max_length=2)

class StockTradingVolumeRank(BaseModel, KisHttpBody):
    """해외주식 거래량순위"""

    output: StockTradingVolumeRankItem1 = Field(title="응답상세1")
    output2: Sequence[StockTradingVolumeRankItem2] = Field(default_factory=list)

class StockTradingAmountRankItem1(BaseModel):
    zdiv: str = Field(title="소수점자리수", max_length=1)
    stat: str = Field(title="거래상태정보", max_length=20)
    crec: str = Field(title="현재조회종목수", max_length=6)
    trec: str = Field(title="전체조회종목수", max_length=6)
    nrec: str = Field(title="RecordCount", max_length=4)

class StockTradingAmountRankItem2(BaseModel):
    rsym: str = Field(title="실시간조회심볼", max_length=16)
    excd: str = Field(title="거래소코드", max_length=4)
    symb: str = Field(title="종목코드", max_length=1)
    name: str = Field(title="종목명", max_length=48)
    last: str = Field(title="현재가", max_length=16)
    sign: str = Field(title="기호", max_length=1)
    diff: str = Field(title="대비", max_length=12)
    rate: str = Field(title="등락율", max_length=12)
    pask: str = Field(title="매도호가", max_length=12)
    pbid: str = Field(title="매수호가", max_length=12)
    tvol: str = Field(title="거래량", max_length=14)
    tamt: str = Field(title="거래대금", max_length=14)
    a_tamt: str = Field(title="평균거래대금", max_length=14)
    rank: str = Field(title="순위", max_length=6)
    ename: str = Field(title="영문종목명", max_length=48)
    e_ordyn: str = Field(title="매매가능", max_length=2)

class StockTradingAmountRank(BaseModel, KisHttpBody):
    """해외주식 거래대금순위"""

    output1: StockTradingAmountRankItem1 = Field(title="응답상세1")
    output2: Sequence[StockTradingAmountRankItem2] = Field(default_factory=list)

class StockTradingIncreaseRateRankItem1(BaseModel):
    zdiv: str = Field(title="소수점자리수", max_length=1)
    stat: str = Field(title="거래상태정보", max_length=20)
    crec: str = Field(title="현재조회종목수", max_length=6)
    trec: str = Field(title="전체조회종목수", max_length=6)
    nrec: str = Field(title="RecordCount", max_length=4)

class StockTradingIncreaseRateRankItem2(BaseModel):
    rsym: str = Field(title="실시간조회심볼", max_length=16)
    excd: str = Field(title="거래소코드", max_length=4)
    symb: str = Field(title="종목코드", max_length=1)
    name: str = Field(title="종목명", max_length=48)
    last: str = Field(title="현재가", max_length=16)
    sign: str = Field(title="기호", max_length=1)
    diff: str = Field(title="대비", max_length=12)
    rate: str = Field(title="등락율", max_length=12)
    pask: str = Field(title="매도호가", max_length=12)
    pbid: str = Field(title="매수호가", max_length=12)
    tvol: str = Field(title="거래량", max_length=14)
    n_tvol: str = Field(title="평균거래량", max_length=14)
    n_rate: str = Field(title="증가율", max_length=12)
    rank: str = Field(title="순위", max_length=6)
    ename: str = Field(title="영문종목명", max_length=48)
    e_ordyn: str = Field(title="매매가능", max_length=2)


class StockTradingIncreaseRateRank(BaseModel, KisHttpBody):
    """해외주식 거래증가율순위"""

    output1: StockTradingIncreaseRateRankItem1 = Field(title="응답상세1")
    output2: Sequence[StockTradingIncreaseRateRankItem2] = Field(default_factory=list)


class StockTradingTurnoverRateRankItem1(BaseModel):
    zdiv: str = Field(title="소수점자리수", max_length=1)
    stat: str = Field(title="거래상태정보", max_length=20)
    crec: str = Field(title="현재조회종목수", max_length=6)
    trec: str = Field(title="전체조회종목수", max_length=6)
    nrec: str = Field(title="RecordCount", max_length=4)

class StockTradingTurnoverRateRankItem2(BaseModel):
    rsym: str = Field(title="실시간조회심볼", max_length=16)
    excd: str = Field(title="거래소코드", max_length=4)
    symb: str = Field(title="종목코드", max_length=1)
    name: str = Field(title="종목명", max_length=48)
    last: str = Field(title="현재가", max_length=16)
    sign: str = Field(title="기호", max_length=1)
    diff: str = Field(title="대비", max_length=12)
    rate: str = Field(title="등락율", max_length=12)
    tvol: str = Field(title="거래량", max_length=14)
    pask: str = Field(title="매도호가", max_length=12)
    pbid: str = Field(title="매수호가", max_length=12)
    n_tvol: str = Field(title="평균거래량", max_length=14)
    shar: str = Field(title="상장주식수", max_length=16)
    tover: str = Field(title="회전율", max_length=10)
    rank: str = Field(title="순위", max_length=6)
    ename: str = Field(title="영문종목명", max_length=48)
    e_ordyn: str = Field(title="매매가능", max_length=2)


class StockTradingTurnoverRateRank(BaseModel, KisHttpBody):
    """해외주식 거래회전율순위"""

    output1: StockTradingTurnoverRateRankItem1 = Field(title="응답상세1")
    output2: Sequence[StockTradingTurnoverRateRankItem2] = Field(default_factory=list)

class StockMarketCapRankItem1(BaseModel):
    zdiv: str = Field(title="소수점자리수", max_length=1)
    stat: str = Field(title="거래상태정보", max_length=20)
    crec: str = Field(title="현재조회종목수", max_length=6)
    trec: str = Field(title="전체조회종목수", max_length=6)
    nrec: str = Field(title="RecordCount", max_length=4)

class StockMarketCapRankItem2(BaseModel):
    rsym: str = Field(title="실시간조회심볼", max_length=16)
    excd: str = Field(title="거래소코드", max_length=4)
    symb: str = Field(title="종목코드", max_length=1)
    name: str = Field(title="종목명", max_length=48)
    last: str = Field(title="현재가", max_length=16)
    sign: str = Field(title="기호", max_length=1)
    diff: str = Field(title="대비", max_length=12)
    rate: str = Field(title="등락율", max_length=12)
    tvol: str = Field(title="거래량", max_length=14)
    shar: str = Field(title="상장주식수", max_length=16)
    tomv: str = Field(title="시가총액", max_length=16)
    grav: str = Field(title="비중", max_length=10)
    rank: str = Field(title="순위", max_length=6)
    ename: str = Field(title="영문종목명", max_length=48)
    e_ordyn: str = Field(title="매매가능", max_length=2)

class StockMarketCapRank(BaseModel, KisHttpBody):
    """해외주식 시가총액순위"""

    output1: StockMarketCapRankItem1 = Field(title="응답상세1")
    output2: Sequence[StockMarketCapRankItem2] = Field(default_factory=list)

class StockPeriodRightsInquiryItem(BaseModel):
    bass_dt: str = Field(title="기준일자", max_length=8)
    rght_type_cd: str = Field(title="권리유형코드", max_length=2)
    pdno: str = Field(title="상품번호", max_length=12)
    prdt_name: str = Field(title="상품명", max_length=60)
    prdt_type_cd: str = Field(title="상품유형코드", max_length=3)
    std_pdno: str = Field(title="표준상품번호", max_length=12)
    acpl_bass_dt: str = Field(title="현지기준일자", max_length=8)
    sbsc_strt_dt: str = Field(title="청약시작일자", max_length=8)
    sbsc_end_dt: str = Field(title="청약종료일자", max_length=8)
    cash_alct_rt: str = Field(title="현금배정비율", max_length=191)
    stck_alct_rt: str = Field(title="주식배정비율", max_length=2012)
    crcy_cd: str = Field(title="통화코드", max_length=3)
    crcy_cd2: str = Field(title="통화코드2", max_length=3)
    crcy_cd3: str = Field(title="통화코드3", max_length=3)
    crcy_cd4: str = Field(title="통화코드4", max_length=3)
    alct_frcr_unpr: str = Field(title="배정외화단가", max_length=195)
    stkp_dvdn_frcr_amt2: str = Field(title="주당배당외화금액2", max_length=195)
    stkp_dvdn_frcr_amt3: str = Field(title="주당배당외화금액3", max_length=195)
    stkp_dvdn_frcr_amt4: str = Field(title="주당배당외화금액4", max_length=195)
    dfnt_yn: str = Field(title="확정여부", max_length=1)


class StockPeriodRightsInquiry(BaseModel, KisHttpBody):
    """해외주식 기간별권리조회"""

    output: StockPeriodRightsInquiryItem = Field(title="응답상세")

class NewsAggregateTitleItem(BaseModel):
    info_gb: str = Field(title="뉴스구분", max_length=1)
    news_key: str = Field(title="뉴스키", max_length=20)
    data_dt: str = Field(title="조회일자", max_length=8)
    data_tm: str = Field(title="조회시간", max_length=6)
    class_cd: str = Field(title="중분류", max_length=2)
    class_name: str = Field(title="중분류명", max_length=20)
    source: str = Field(title="자료원", max_length=20)
    nation_cd: str = Field(title="국가코드", max_length=2)
    exchange_cd: str = Field(title="거래소코드", max_length=3)
    symb: str = Field(title="종목코드", max_length=20)
    symb_name: str = Field(title="종목명", max_length=48)
    title: str = Field(title="제목", max_length=128)


class NewsAggregateTitle(BaseModel, KisHttpBody):
    """해외뉴스종합(제목)"""

    outblock1: Sequence[NewsAggregateTitleItem] = Field(default_factory=list)

class StockRightsAggregateItem(BaseModel):
    anno_dt: str = Field(title="ICE공시일", max_length=8)
    ca_title: str = Field(title="권리유형", max_length=12)
    div_lock_dt: str = Field(title="배당락일", max_length=8)
    pay_dt: str = Field(title="지급일", max_length=8)
    record_dt: str = Field(title="기준일", max_length=8)
    validity_dt: str = Field(title="효력일자", max_length=8)
    local_end_dt: str = Field(title="현지지시마감일", max_length=8)
    lock_dt: str = Field(title="권리락일", max_length=8)
    delist_dt: str = Field(title="상장폐지일", max_length=8)
    redempt_dt: str = Field(title="상환일자", max_length=8)
    early_redempt_dt: str = Field(title="조기상환일자", max_length=8)
    effective_dt: str = Field(title="적용일", max_length=8)


class StockRightsAggregate(BaseModel, KisHttpBody):
    """해외주식 권리종합"""

    output1: Sequence[StockRightsAggregateItem] = Field(default_factory=list)

class StockCollateralLoanEligibleItem1(BaseModel):
    pdno: str = Field(title="상품번호", max_length=12)
    ovrs_item_name: str = Field(title="해외종목명", max_length=60)
    loan_rt: str = Field(title="대출비율", max_length=238)
    mgge_mntn_rt: str = Field(title="담보유지비율", max_length=238)
    mgge_ensu_rt: str = Field(title="담보확보비율", max_length=238)
    loan_exec_psbl_yn: str = Field(title="대출실행가능여부", max_length=1)
    stff_name: str = Field(title="직원명", max_length=60)
    erlm_dt: str = Field(title="등록일자", max_length=8)
    tr_mket_name: str = Field(title="거래시장명", max_length=60)
    crcy_cd: str = Field(title="통화코드", max_length=3)
    natn_kor_name: str = Field(title="국가한글명", max_length=60)
    ovrs_excg_cd: str = Field(title="해외거래소코드", max_length=4)

class StockCollateralLoanEligibleItem2(BaseModel):
    loan_psbl_item_num: str = Field(title="대출가능종목수", max_length=20)


class StockCollateralLoanEligible(BaseModel, KisHttpBody):
    """당사 해외주식담보대출 가능 종목"""

    output1: Sequence[StockCollateralLoanEligibleItem1] = Field(default_factory=list)
    output2: Sequence[StockCollateralLoanEligibleItem2] = Field(default_factory=list)

class BreakingNewsTitleItem(BaseModel):
    cntt_usiq_srno: str = Field(title="내용조회용일련번호", max_length=20)
    news_ofer_entp_code: str = Field(title="뉴스제공업체코드", max_length=1)
    data_dt: str = Field(title="작성일자", max_length=8)
    data_tm: str = Field(title="작성시간", max_length=6)
    hts_pbnt_titl_cntt: str = Field(title="HTS공시제목내용", max_length=400)
    news_lrdv_code: str = Field(title="뉴스대구분", max_length=8)
    dorg: str = Field(title="자료원", max_length=20)
    iscd1: str = Field(title="종목코드1", max_length=9)
    iscd2: str = Field(title="종목코드2", max_length=9)
    iscd3: str = Field(title="종목코드3", max_length=9)
    iscd4: str = Field(title="종목코드4", max_length=9)
    iscd5: str = Field(title="종목코드5", max_length=9)
    iscd6: str = Field(title="종목코드6", max_length=9)
    iscd7: str = Field(title="종목코드7", max_length=9)
    iscd8: str = Field(title="종목코드8", max_length=9)
    iscd9: str = Field(title="종목코드9", max_length=9)
    iscd10: str = Field(title="종목코드10", max_length=9)
    kor_isnm1: str = Field(title="한글종목명1", max_length=40)
    kor_isnm2: str = Field(title="한글종목명2", max_length=40)
    kor_isnm3: str = Field(title="한글종목명3", max_length=40)
    kor_isnm4: str = Field(title="한글종목명4", max_length=40)
    kor_isnm5: str = Field(title="한글종목명5", max_length=40)
    kor_isnm6: str = Field(title="한글종목명6", max_length=40)
    kor_isnm7: str = Field(title="한글종목명7", max_length=40)
    kor_isnm8: str = Field(title="한글종목명8", max_length=40)
    kor_isnm9: str = Field(title="한글종목명9", max_length=40)
    kor_isnm10: str = Field(title="한글종목명10", max_length=40)


class BreakingNewsTitle(BaseModel, KisHttpBody):
    """해외속보(제목)"""

    output: Sequence[BreakingNewsTitleItem] = Field(default_factory=list)
