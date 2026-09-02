from typing import Sequence

from pydantic import AliasChoices, BaseModel, Field

from cluefin_openapi.kis._model import KisHttpBody


class StockPriceFluctuationItem1(BaseModel):
    zdiv: str = Field(title="소수점자리수")
    stat: str = Field(title="거래상태")
    nrec: str = Field(title="RecordCount")


class StockPriceFluctuationItem2(BaseModel):
    rsym: str = Field(title="실시간조회심볼")
    excd: str = Field(title="거래소코드")
    symb: str = Field(title="종목코드")
    knam: str = Field(title="종목명")
    last: str = Field(title="현재가")
    sign: str = Field(title="기호")
    diff: str = Field(title="대비")
    rate: str = Field(title="등락율")
    tvol: str = Field(title="거래량")
    pask: str = Field(title="매도호가")
    pbid: str = Field(title="매수호가")
    n_base: str = Field(title="기준가격")
    n_diff: str = Field(title="기준가격대비")
    n_rate: str = Field(title="기준가격대비율")
    enam: str = Field(title="영문종목명")
    e_ordyn: str = Field(title="매매가능")


class StockPriceFluctuation(BaseModel, KisHttpBody):
    """해외주식 가격급등락"""

    output1: StockPriceFluctuationItem1 = Field(title="응답상세1")
    output2: Sequence[StockPriceFluctuationItem2] = Field(default_factory=list)


class StockVolumeSurgeItem1(BaseModel):
    zdiv: str = Field(title="소수점자리수")
    stat: str = Field(title="거래상태")
    nrec: str = Field(title="RecordCount")


class StockVolumeSurgeItem2(BaseModel):
    rsym: str = Field(title="실시간조회심볼")
    excd: str = Field(title="거래소코드")
    symb: str = Field(title="종목코드")
    knam: str = Field(title="종목명")
    last: str = Field(title="현재가")
    sign: str = Field(title="기호")
    diff: str = Field(title="대비")
    rate: str = Field(title="등락율")
    tvol: str = Field(title="거래량")
    pask: str = Field(title="매도호가")
    pbid: str = Field(title="매수호가")
    n_tvol: str = Field(title="기준거래량")
    n_diff: str = Field(title="증가량")
    n_rate: str = Field(title="증가율")
    enam: str = Field(title="영문종목명")
    e_ordyn: str = Field(title="매매가능")


class StockVolumeSurge(BaseModel, KisHttpBody):
    """해외주식 거래량급증"""

    output1: StockVolumeSurgeItem1 = Field(title="응답상세1")
    output2: Sequence[StockVolumeSurgeItem2] = Field(default_factory=list)


class StockBuyExecutionStrengthTopItem1(BaseModel):
    zdiv: str = Field(title="소수점자리수")
    stat: str = Field(title="거래상태")
    nrec: str = Field(title="RecordCount")


class StockBuyExecutionStrengthTopItem2(BaseModel):
    rsym: str = Field(title="실시간조회심볼")
    excd: str = Field(title="거래소코드")
    symb: str = Field(title="종목코드")
    # 공식 문서는 knam/enam으로 표기하지만 실서버 응답 키는 name/ename — 둘 다 수용
    name: str = Field(validation_alias=AliasChoices("name", "knam"), title="종목명")
    last: str = Field(title="현재가")
    sign: str = Field(title="기호")
    diff: str = Field(title="대비")
    rate: str = Field(title="등락율")
    tvol: str = Field(title="거래량")
    pask: str = Field(title="매도호가")
    pbid: str = Field(title="매수호가")
    tpow: str = Field(title="당일체결강도")
    powx: str = Field(title="체결강도")
    ename: str = Field(validation_alias=AliasChoices("ename", "enam"), title="영문종목명")
    e_ordyn: str = Field(title="매매가능")


class StockBuyExecutionStrengthTop(BaseModel, KisHttpBody):
    """해외주식 매수체결강도상위"""

    output1: StockBuyExecutionStrengthTopItem1 = Field(title="응답상세1")
    output2: Sequence[StockBuyExecutionStrengthTopItem2] = Field(default_factory=list)


class StockRiseDeclineRateItem1(BaseModel):
    zdiv: str = Field(title="소수점자리수")
    stat: str = Field(title="거래상태정보")
    crec: str = Field(title="현재Count")
    trec: str = Field(title="전체조회종목수")
    nrec: str = Field(title="RecordCount")


class StockRiseDeclineRateItem2(BaseModel):
    rsym: str = Field(title="실시간조회심볼")
    excd: str = Field(title="거래소코드")
    symb: str = Field(title="종목코드")
    name: str = Field(title="종목명")
    last: str = Field(title="현재가")
    sign: str = Field(title="기호")
    diff: str = Field(title="대비")
    rate: str = Field(title="등락율")
    tvol: str = Field(title="거래량")
    pask: str = Field(title="매도호가")
    pbid: str = Field(title="매수호가")
    n_base: str = Field(title="기준가격")
    n_diff: str = Field(title="기준가격대비")
    n_rate: str = Field(title="기준가격대비율")
    rank: str = Field(title="순위")
    ename: str = Field(title="영문종목명")
    e_ordyn: str = Field(title="매매가능")


class StockRiseDeclineRate(BaseModel, KisHttpBody):
    """해외주식 상승률/하락율"""

    output1: StockRiseDeclineRateItem1 = Field(title="응답상세1")
    output2: Sequence[StockRiseDeclineRateItem2] = Field(default_factory=list)


class StockNewHighLowPriceItem1(BaseModel):
    zdiv: str = Field(title="소수점자리수")
    stat: str = Field(title="거래상태정보")
    nrec: str = Field(title="RecordCount")


class StockNewHighLowPriceItem2(BaseModel):
    rsym: str = Field(title="실시간조회심볼")
    excd: str = Field(title="거래소코드")
    symb: str = Field(title="종목코드")
    name: str = Field(title="종목명")
    last: str = Field(title="현재가")
    sign: str = Field(title="기호")
    diff: str = Field(title="대비")
    rate: str = Field(title="등락율")
    tvol: str = Field(title="거래량")
    pask: str = Field(title="매도호가")
    pbid: str = Field(title="매수호가")
    n_base: str = Field(title="기준가")
    n_diff: str = Field(title="기준가대비")
    n_rate: str = Field(title="기준가대비율")
    ename: str = Field(title="영문종목명")
    e_ordyn: str = Field(title="매매가능")


class StockNewHighLowPrice(BaseModel, KisHttpBody):
    """해외주식 신고/신저가"""

    output1: StockNewHighLowPriceItem1 = Field(title="응답상세1")
    output2: Sequence[StockNewHighLowPriceItem2] = Field(default_factory=list)


class StockTradingVolumeRankItem1(BaseModel):
    zdiv: str = Field(title="소수점자리수")
    stat: str = Field(title="거래상태정보")
    crec: str = Field(title="현재조회종목수")
    trec: str = Field(title="전체조회종목수")
    nrec: str = Field(title="RecordCount")


class StockTradingVolumeRankItem2(BaseModel):
    rsym: str = Field(title="실시간조회심볼")
    excd: str = Field(title="거래소코드")
    symb: str = Field(title="종목코드")
    name: str = Field(title="종목명")
    last: str = Field(title="현재가")
    sign: str = Field(title="기호")
    diff: str = Field(title="대비")
    rate: str = Field(title="등락율")
    pask: str = Field(title="매도호가")
    pbid: str = Field(title="매수호가")
    tvol: str = Field(title="거래량")
    tamt: str = Field(title="거래대금")
    a_tvol: str = Field(title="평균거래량")
    rank: str = Field(title="순위")
    ename: str = Field(title="영문종목명")
    e_ordyn: str = Field(title="매매가능")


class StockTradingVolumeRank(BaseModel, KisHttpBody):
    """해외주식 거래량순위"""

    output1: StockTradingVolumeRankItem1 = Field(title="응답상세1")
    output2: Sequence[StockTradingVolumeRankItem2] = Field(default_factory=list)


class StockTradingAmountRankItem1(BaseModel):
    zdiv: str = Field(title="소수점자리수")
    stat: str = Field(title="거래상태정보")
    crec: str = Field(title="현재조회종목수")
    trec: str = Field(title="전체조회종목수")
    nrec: str = Field(title="RecordCount")


class StockTradingAmountRankItem2(BaseModel):
    rsym: str = Field(title="실시간조회심볼")
    excd: str = Field(title="거래소코드")
    symb: str = Field(title="종목코드")
    name: str = Field(title="종목명")
    last: str = Field(title="현재가")
    sign: str = Field(title="기호")
    diff: str = Field(title="대비")
    rate: str = Field(title="등락율")
    pask: str = Field(title="매도호가")
    pbid: str = Field(title="매수호가")
    tvol: str = Field(title="거래량")
    tamt: str = Field(title="거래대금")
    a_tamt: str = Field(title="평균거래대금")
    rank: str = Field(title="순위")
    ename: str = Field(title="영문종목명")
    e_ordyn: str = Field(title="매매가능")


class StockTradingAmountRank(BaseModel, KisHttpBody):
    """해외주식 거래대금순위"""

    output1: StockTradingAmountRankItem1 = Field(title="응답상세1")
    output2: Sequence[StockTradingAmountRankItem2] = Field(default_factory=list)


class StockTradingIncreaseRateRankItem1(BaseModel):
    zdiv: str = Field(title="소수점자리수")
    stat: str = Field(title="거래상태정보")
    crec: str = Field(title="현재조회종목수")
    trec: str = Field(title="전체조회종목수")
    nrec: str = Field(title="RecordCount")


class StockTradingIncreaseRateRankItem2(BaseModel):
    rsym: str = Field(title="실시간조회심볼")
    excd: str = Field(title="거래소코드")
    symb: str = Field(title="종목코드")
    name: str = Field(title="종목명")
    last: str = Field(title="현재가")
    sign: str = Field(title="기호")
    diff: str = Field(title="대비")
    rate: str = Field(title="등락율")
    pask: str = Field(title="매도호가")
    pbid: str = Field(title="매수호가")
    tvol: str = Field(title="거래량")
    n_tvol: str = Field(title="평균거래량")
    n_rate: str = Field(title="증가율")
    rank: str = Field(title="순위")
    ename: str = Field(title="영문종목명")
    e_ordyn: str = Field(title="매매가능")


class StockTradingIncreaseRateRank(BaseModel, KisHttpBody):
    """해외주식 거래증가율순위"""

    output1: StockTradingIncreaseRateRankItem1 = Field(title="응답상세1")
    output2: Sequence[StockTradingIncreaseRateRankItem2] = Field(default_factory=list)


class StockTradingTurnoverRateRankItem1(BaseModel):
    zdiv: str = Field(title="소수점자리수")
    stat: str = Field(title="거래상태정보")
    crec: str = Field(title="현재조회종목수")
    trec: str = Field(title="전체조회종목수")
    nrec: str = Field(title="RecordCount")


class StockTradingTurnoverRateRankItem2(BaseModel):
    rsym: str = Field(title="실시간조회심볼")
    excd: str = Field(title="거래소코드")
    symb: str = Field(title="종목코드")
    name: str = Field(title="종목명")
    last: str = Field(title="현재가")
    sign: str = Field(title="기호")
    diff: str = Field(title="대비")
    rate: str = Field(title="등락율")
    tvol: str = Field(title="거래량")
    pask: str = Field(title="매도호가")
    pbid: str = Field(title="매수호가")
    shar: str = Field(title="상장주식수")
    tover: str = Field(title="회전율")
    rank: str = Field(title="순위")
    ename: str = Field(title="영문종목명")
    e_ordyn: str = Field(title="매매가능")


class StockTradingTurnoverRateRank(BaseModel, KisHttpBody):
    """해외주식 거래회전율순위"""

    output1: StockTradingTurnoverRateRankItem1 = Field(title="응답상세1")
    output2: Sequence[StockTradingTurnoverRateRankItem2] = Field(default_factory=list)


class StockMarketCapRankItem1(BaseModel):
    zdiv: str = Field(title="소수점자리수")
    stat: str = Field(title="거래상태정보")
    crec: str = Field(title="현재조회종목수")
    trec: str = Field(title="전체조회종목수")
    nrec: str = Field(title="RecordCount")


class StockMarketCapRankItem2(BaseModel):
    rsym: str = Field(title="실시간조회심볼")
    excd: str = Field(title="거래소코드")
    symb: str = Field(title="종목코드")
    name: str = Field(title="종목명")
    last: str = Field(title="현재가")
    last_org: str = Field(title="현재가(원본)")
    sign: str = Field(title="기호")
    diff: str = Field(title="대비")
    diff_org: str = Field(title="대비(원본)")
    rate: str = Field(title="등락율")
    tvol: str = Field(title="거래량")
    shar: str = Field(title="상장주식수")
    tomv: str = Field(title="시가총액")
    tomv_org: str = Field(title="시가총액(원본)")
    grav: str = Field(title="비중")
    rank: str = Field(title="순위")
    ename: str = Field(title="영문종목명")
    e_ordyn: str = Field(title="매매가능")


class StockMarketCapRank(BaseModel, KisHttpBody):
    """해외주식 시가총액순위"""

    output1: StockMarketCapRankItem1 = Field(title="응답상세1")
    output2: Sequence[StockMarketCapRankItem2] = Field(default_factory=list)


class StockPeriodRightsInquiryItem(BaseModel):
    bass_dt: str = Field(title="기준일자")
    rght_type_cd: str = Field(title="권리유형코드")
    pdno: str = Field(title="상품번호")
    prdt_name: str = Field(title="상품명")
    prdt_type_cd: str = Field(title="상품유형코드")
    std_pdno: str = Field(title="표준상품번호")
    acpl_bass_dt: str = Field(title="현지기준일자")
    sbsc_strt_dt: str = Field(title="청약시작일자")
    sbsc_end_dt: str = Field(title="청약종료일자")
    cash_alct_rt: str = Field(title="현금배정비율")
    stck_alct_rt: str = Field(title="주식배정비율")
    crcy_cd: str = Field(title="통화코드")
    crcy_cd2: str = Field(title="통화코드2")
    crcy_cd3: str = Field(title="통화코드3")
    crcy_cd4: str = Field(title="통화코드4")
    alct_frcr_unpr: str = Field(title="배정외화단가")
    stkp_dvdn_frcr_amt2: str = Field(title="주당배당외화금액2")
    stkp_dvdn_frcr_amt3: str = Field(title="주당배당외화금액3")
    stkp_dvdn_frcr_amt4: str = Field(title="주당배당외화금액4")
    dfnt_yn: str = Field(title="확정여부")


class StockPeriodRightsInquiry(BaseModel, KisHttpBody):
    """해외주식 기간별권리조회"""

    ctx_area_fk50: str = Field(default="", title="연속조회검색조건50")
    ctx_area_nk50: str = Field(default="", title="연속조회키50")
    output: Sequence[StockPeriodRightsInquiryItem] = Field(default_factory=list)


class NewsAggregateTitleItem(BaseModel):
    info_gb: str = Field(title="뉴스구분")
    news_key: str = Field(title="뉴스키")
    data_dt: str = Field(title="조회일자")
    data_tm: str = Field(title="조회시간")
    class_cd: str = Field(title="중분류")
    class_name: str = Field(title="중분류명")
    source: str = Field(title="자료원")
    nation_cd: str = Field(title="국가코드")
    exchange_cd: str = Field(title="거래소코드")
    symb: str = Field(title="종목코드")
    symb_name: str = Field(title="종목명")
    title: str = Field(title="제목")


class NewsAggregateTitle(BaseModel, KisHttpBody):
    """해외뉴스종합(제목)"""

    outblock1: Sequence[NewsAggregateTitleItem] = Field(default_factory=list)


class StockRightsAggregateItem(BaseModel):
    anno_dt: str = Field(title="ICE공시일")
    ca_title: str = Field(title="권리유형")
    div_lock_dt: str = Field(title="배당락일")
    pay_dt: str = Field(title="지급일")
    record_dt: str = Field(title="기준일")
    validity_dt: str = Field(title="효력일자")
    local_end_dt: str = Field(title="현지지시마감일")
    lock_dt: str = Field(title="권리락일")
    delist_dt: str = Field(title="상장폐지일")
    redempt_dt: str = Field(title="상환일자")
    early_redempt_dt: str = Field(title="조기상환일자")
    effective_dt: str = Field(title="적용일")


class StockRightsAggregate(BaseModel, KisHttpBody):
    """해외주식 권리종합"""

    output1: Sequence[StockRightsAggregateItem] = Field(default_factory=list)


class StockCollateralLoanEligibleItem1(BaseModel):
    pdno: str = Field(title="상품번호")
    ovrs_item_name: str = Field(title="해외종목명")
    loan_rt: str = Field(title="대출비율")
    mgge_mntn_rt: str = Field(title="담보유지비율")
    mgge_ensu_rt: str = Field(title="담보확보비율")
    loan_exec_psbl_yn: str = Field(title="대출실행가능여부")
    stff_name: str = Field(title="직원명")
    erlm_dt: str = Field(title="등록일자")
    tr_mket_name: str = Field(title="거래시장명")
    crcy_cd: str = Field(title="통화코드")
    natn_kor_name: str = Field(title="국가한글명")
    ovrs_excg_cd: str = Field(title="해외거래소코드")


class StockCollateralLoanEligibleItem2(BaseModel):
    loan_psbl_item_num: str = Field(title="대출가능종목수")


class StockCollateralLoanEligible(BaseModel, KisHttpBody):
    """당사 해외주식담보대출 가능 종목"""

    ctx_area_fk100: str = Field(default="", title="연속조회검색조건100")
    ctx_area_nk100: str = Field(default="", title="연속조회키100")
    output1: Sequence[StockCollateralLoanEligibleItem1] = Field(default_factory=list)
    # TODO(typo): 문서에는 list 형태로 나와있으나 실제로는 단일 객체
    output2: StockCollateralLoanEligibleItem2 = Field(title="응답상세2")


class BreakingNewsTitleItem(BaseModel):
    cntt_usiq_srno: str = Field(title="내용조회용일련번호")
    news_ofer_entp_code: str = Field(title="뉴스제공업체코드")
    data_dt: str = Field(title="작성일자")
    data_tm: str = Field(title="작성시간")
    hts_pbnt_titl_cntt: str = Field(title="HTS공시제목내용")
    news_lrdv_code: str = Field(title="뉴스대구분")
    dorg: str = Field(title="자료원")
    iscd1: str = Field(title="종목코드1")
    iscd2: str = Field(title="종목코드2")
    iscd3: str = Field(title="종목코드3")
    iscd4: str = Field(title="종목코드4")
    iscd5: str = Field(title="종목코드5")
    iscd6: str = Field(title="종목코드6")
    iscd7: str = Field(title="종목코드7")
    iscd8: str = Field(title="종목코드8")
    iscd9: str = Field(title="종목코드9")
    iscd10: str = Field(title="종목코드10")
    kor_isnm1: str = Field(title="한글종목명1")
    kor_isnm2: str = Field(title="한글종목명2")
    kor_isnm3: str = Field(title="한글종목명3")
    kor_isnm4: str = Field(title="한글종목명4")
    kor_isnm5: str = Field(title="한글종목명5")
    kor_isnm6: str = Field(title="한글종목명6")
    kor_isnm7: str = Field(title="한글종목명7")
    kor_isnm8: str = Field(title="한글종목명8")
    kor_isnm9: str = Field(title="한글종목명9")
    kor_isnm10: str = Field(title="한글종목명10")


class BreakingNewsTitle(BaseModel, KisHttpBody):
    """해외속보(제목)"""

    output: Sequence[BreakingNewsTitleItem] = Field(default_factory=list)
