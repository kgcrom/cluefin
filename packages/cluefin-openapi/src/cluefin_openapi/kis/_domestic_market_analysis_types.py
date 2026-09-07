from typing import Optional, Sequence

from pydantic import BaseModel, Field

from cluefin_openapi.kis._model import KisHttpBody


class ConditionSearchListItem(BaseModel):
    user_id: str = Field(title="HTS ID", description="")
    seq: str = Field(title="조건키값", description="해당 값을 종목조건검색조회 API의 input으로 사용 (0번부터 시작)")
    grp_nm: str = Field(
        title="그룹명",
        description='HTS(eFriend Plus) [0110] "사용자조건검색"화면을 통해 등록한 사용자조건 그룹',
    )
    condition_nm: str = Field(title="조건명", description="등록한 사용자 조건명")


class ConditionSearchList(BaseModel, KisHttpBody):
    """종목조건검색 목록조회"""

    output2: Sequence[ConditionSearchListItem] = Field(default_factory=list)


class ConditionSearchResultItem(BaseModel):
    code: str = Field(title="종목코드")
    name: str = Field(title="종목명")
    daebi: str = Field(title="전일대비부호", description="1. 상한 2. 상승 3. 보합 4. 하한 5. 하락")
    price: str = Field(title="현재가")
    chgrate: str = Field(title="등락율")
    acml_vol: str = Field(title="거래량")
    trade_amt: str = Field(title="거래대금")
    change: str = Field(title="전일대비")
    cttr: str = Field(title="체결강도")
    open: str = Field(title="시가")
    high: str = Field(title="고가")
    low: str = Field(title="저가")
    high52: str = Field(title="52주최고가")
    low52: str = Field(title="52주최저가")
    expprice: str = Field(title="예상체결가")
    expchange: str = Field(title="예상대비")
    expchggrate: str = Field(title="예상등락률")
    expcvol: str = Field(title="예상체결수량")
    chgrate2: str = Field(title="전일거래량대비율")
    expdaebi: str = Field(title="예상대비부호")
    recprice: str = Field(title="기준가")
    uplmtprice: str = Field(title="상한가")
    dnlmtprice: str = Field(title="하한가")
    stotprice: str = Field(title="시가총액")


class ConditionSearchResult(BaseModel, KisHttpBody):
    """종목조건검색조회"""

    output2: Sequence[ConditionSearchResultItem] = Field(default_factory=list)


class WatchlistGroupsItem(BaseModel):
    date: str = Field(title="일자")
    trnm_hour: str = Field(title="전송 시간")
    data_rank: str = Field(title="데이터 순위")
    inter_grp_code: str = Field(title="관심 그룹 코드")
    inter_grp_name: str = Field(title="관심 그룹 명")
    ask_cnt: str = Field(title="요청 개수")


class WatchlistGroups(BaseModel, KisHttpBody):
    """관심종목 그룹조회"""

    # TODO(typo): 문서에는 object로 되어있으나, 실제로는 list
    output2: Sequence[WatchlistGroupsItem] = Field(default_factory=list)


class WatchlistMultiQuoteItem(BaseModel):
    kospi_kosdaq_cls_name: str = Field(title="코스피 코스닥 구분 명")
    mrkt_trtm_cls_name: str = Field(title="시장 조치 구분 명")
    hour_cls_code: str = Field(title="시간 구분 코드")
    inter_shrn_iscd: str = Field(title="관심 단축 종목코드")
    inter_kor_isnm: str = Field(title="관심 한글 종목명")
    inter2_prpr: str = Field(title="관심2 현재가")
    inter2_prdy_vrss: str = Field(title="관심2 전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    inter2_oprc: str = Field(title="관심2 시가")
    inter2_hgpr: str = Field(title="관심2 고가")
    inter2_lwpr: str = Field(title="관심2 저가")
    inter2_llam: str = Field(title="관심2 하한가")
    inter2_mxpr: str = Field(title="관심2 상한가")
    inter2_askp: str = Field(title="관심2 매도호가")
    inter2_bidp: str = Field(title="관심2 매수호가")
    seln_rsqn: str = Field(title="매도 잔량")
    shnu_rsqn: str = Field(title="매수2 잔량")
    total_askp_rsqn: str = Field(title="총 매도호가 잔량")
    total_bidp_rsqn: str = Field(title="총 매수호가 잔량")
    acml_tr_pbmn: str = Field(title="누적 거래 대금")
    inter2_prdy_clpr: str = Field(title="관심2 전일 종가")
    oprc_vrss_hgpr_rate: str = Field(title="시가 대비 최고가 비율")
    intr_antc_cntg_vrss: str = Field(title="관심 예상 체결 대비")
    intr_antc_cntg_vrss_sign: str = Field(title="관심 예상 체결 대비 부호")
    intr_antc_cntg_prdy_ctrt: str = Field(title="관심 예상 체결 전일 대비율")
    intr_antc_vol: str = Field(title="관심 예상 거래량")
    inter2_sdpr: str = Field(title="관심2 기준가")


class WatchlistMultiQuote(BaseModel, KisHttpBody):
    """관심종목(멀티종목) 시세조회"""

    # TODO(typo): 문서에는 object로 되어있으나, 실제로는 list
    output: Sequence[WatchlistMultiQuoteItem] = Field(default_factory=list)


class WatchlistStocksByGroupItem1(BaseModel):
    data_rank: str = Field(title="데이터 순위")
    inter_grp_name: str = Field(title="관심 그룹 명")


class WatchlistStocksByGroupItem2(BaseModel):
    fid_mrkt_cls_code: str = Field(title="FID 시장 구분 코드")
    data_rank: str = Field(title="데이터 순위")
    exch_code: str = Field(title="거래소코드")
    jong_code: str = Field(title="종목코드")
    color_code: str = Field(title="생상 코드")
    memo: Optional[str] = Field(title="메모")
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    fxdt_ntby_qty: str = Field(title="기준일 순매수 수량")
    cntg_unpr: str = Field(title="체결단가")
    cntg_cls_code: str = Field(title="체결 구분 코드")


class WatchlistStocksByGroup(BaseModel, KisHttpBody):
    """관심종목 그룹별 종목조회"""

    output1: WatchlistStocksByGroupItem1 = Field(title="응답상세1")
    output2: Sequence[WatchlistStocksByGroupItem2] = Field(default_factory=list)


class InstitutionalForeignTradingAggregateItem(BaseModel):
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드")
    ntby_qty: str = Field(title="순매수 수량")
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    frgn_ntby_qty: str = Field(title="외국인 순매수 수량")
    orgn_ntby_qty: str = Field(title="기관계 순매수 수량")
    ivtr_ntby_qty: str = Field(title="투자신탁 순매수 수량")
    bank_ntby_qty: str = Field(title="은행 순매수 수량")
    insu_ntby_qty: str = Field(title="보험 순매수 수량")
    mrbn_ntby_qty: str = Field(title="종금 순매수 수량")
    fund_ntby_qty: str = Field(title="기금 순매수 수량")
    etc_orgt_ntby_vol: str = Field(title="기타 단체 순매수 거래량")
    etc_corp_ntby_vol: str = Field(title="기타 법인 순매수 거래량")
    frgn_ntby_tr_pbmn: str = Field(title="외국인 순매수 거래 대금")
    orgn_ntby_tr_pbmn: str = Field(title="기관계 순매수 거래 대금")
    ivtr_ntby_tr_pbmn: str = Field(title="투자신탁 순매수 거래 대금")
    bank_ntby_tr_pbmn: str = Field(title="은행 순매수 거래 대금")
    insu_ntby_tr_pbmn: str = Field(title="보험 순매수 거래 대금")
    mrbn_ntby_tr_pbmn: str = Field(title="종금 순매수 거래 대금")
    fund_ntby_tr_pbmn: str = Field(title="기금 순매수 거래 대금")
    etc_orgt_ntby_tr_pbmn: str = Field(title="기타 단체 순매수 거래 대금")
    etc_corp_ntby_tr_pbmn: str = Field(title="기타 법인 순매수 거래 대금")


class InstitutionalForeignTradingAggregate(BaseModel, KisHttpBody):
    """국내기관_외국인 매매종목가집계"""

    output: Sequence[InstitutionalForeignTradingAggregateItem] = Field(default_factory=list)


class ForeignBrokerageTradingAggregateItem(BaseModel):
    stck_shrn_iscd: str = Field(title="주식단축종목코드")
    hts_kor_isnm: str = Field(title="HTS한글종목명")
    glob_ntsl_qty: str = Field(title="외국계순매도수량")
    stck_prpr: str = Field(title="주식현재가")
    prdy_vrss: str = Field(title="전일대비")
    prdy_vrss_sign: str = Field(title="전일대비부호")
    prdy_ctrt: str = Field(title="전일대비율")
    acml_vol: str = Field(title="누적거래량")
    glob_total_seln_qty: str = Field(title="외국계총매도수량")
    glob_total_shnu_qty: str = Field(title="외국계총매수2수량")


class ForeignBrokerageTradingAggregate(BaseModel, KisHttpBody):
    """외국계 매매종목 가집계"""

    output: Sequence[ForeignBrokerageTradingAggregateItem] = Field(default_factory=list)


class InvestorTradingTrendByStockDailyItem1(BaseModel):
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    prdy_vol: str = Field(title="전일 거래량")
    rprs_mrkt_kor_name: str = Field(title="대표 시장 한글 명")


class InvestorTradingTrendByStockDailyItem2(BaseModel):
    stck_bsop_date: str = Field(title="주식 영업 일자")
    stck_clpr: str = Field(title="주식 종가")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    acml_tr_pbmn: str = Field(title="누적 거래 대금")
    stck_oprc: str = Field(title="주식 시가2")
    stck_hgpr: str = Field(title="주식 최고가")
    stck_lwpr: str = Field(title="주식 최저가")
    frgn_ntby_qty: str = Field(title="외국인 순매수 수량")
    frgn_reg_ntby_qty: str = Field(title="외국인 등록 순매수 수량")
    frgn_nreg_ntby_qty: str = Field(title="외국인 비등록 순매수 수량")
    prsn_ntby_qty: str = Field(title="개인 순매수 수량")
    orgn_ntby_qty: str = Field(title="기관계 순매수 수량")
    scrt_ntby_qty: str = Field(title="증권 순매수 수량")
    ivtr_ntby_qty: str = Field(title="투자신탁 순매수 수량")
    pe_fund_ntby_vol: str = Field(title="사모 펀드 순매수 거래량")
    bank_ntby_qty: str = Field(title="은행 순매수 수량")
    insu_ntby_qty: str = Field(title="보험 순매수 수량")
    mrbn_ntby_qty: str = Field(title="종금 순매수 수량")
    fund_ntby_qty: str = Field(title="기금 순매수 수량")
    etc_ntby_qty: str = Field(title="기타 순매수 수량")
    etc_corp_ntby_vol: str = Field(title="기타 법인 순매수 거래량")
    etc_orgt_ntby_vol: str = Field(title="기타 단체 순매수 거래량")
    frgn_reg_ntby_pbmn: str = Field(title="외국인 등록 순매수 대금")
    frgn_ntby_tr_pbmn: str = Field(title="외국인 순매수 거래 대금")
    frgn_nreg_ntby_pbmn: str = Field(title="외국인 비등록 순매수 대금")
    prsn_ntby_tr_pbmn: str = Field(title="개인 순매수 거래 대금")
    orgn_ntby_tr_pbmn: str = Field(title="기관계 순매수 거래 대금")
    scrt_ntby_tr_pbmn: str = Field(title="증권 순매수 거래 대금")
    pe_fund_ntby_tr_pbmn: str = Field(title="사모 펀드 순매수 거래 대금")
    ivtr_ntby_tr_pbmn: str = Field(title="투자신탁 순매수 거래 대금")
    bank_ntby_tr_pbmn: str = Field(title="은행 순매수 거래 대금")
    insu_ntby_tr_pbmn: str = Field(title="보험 순매수 거래 대금")
    mrbn_ntby_tr_pbmn: str = Field(title="종금 순매수 거래 대금")
    fund_ntby_tr_pbmn: str = Field(title="기금 순매수 거래 대금")
    etc_ntby_tr_pbmn: str = Field(title="기타 순매수 거래 대금")
    etc_corp_ntby_tr_pbmn: str = Field(title="기타 법인 순매수 거래 대금")
    etc_orgt_ntby_tr_pbmn: str = Field(title="기타 단체 순매수 거래 대금")
    frgn_seln_vol: str = Field(title="외국인 매도 거래량")
    frgn_shnu_vol: str = Field(title="외국인 매수2 거래량")
    frgn_seln_tr_pbmn: str = Field(title="외국인 매도 거래 대금")
    frgn_shnu_tr_pbmn: str = Field(title="외국인 매수2 거래 대금")
    frgn_reg_askp_qty: str = Field(title="외국인 등록 매도 수량")
    frgn_reg_bidp_qty: str = Field(title="외국인 등록 매수 수량")
    frgn_reg_askp_pbmn: str = Field(title="외국인 등록 매도 대금")
    frgn_reg_bidp_pbmn: str = Field(title="외국인 등록 매수 대금")
    frgn_nreg_askp_qty: str = Field(title="외국인 비등록 매도 수량")
    frgn_nreg_bidp_qty: str = Field(title="외국인 비등록 매수 수량")
    frgn_nreg_askp_pbmn: str = Field(title="외국인 비등록 매도 대금")
    frgn_nreg_bidp_pbmn: str = Field(title="외국인 비등록 매수 대금")
    prsn_seln_vol: str = Field(title="개인 매도 거래량")
    prsn_shnu_vol: str = Field(title="개인 매수2 거래량")
    prsn_seln_tr_pbmn: str = Field(title="개인 매도 거래 대금")
    prsn_shnu_tr_pbmn: str = Field(title="개인 매수2 거래 대금")
    orgn_seln_vol: str = Field(title="기관계 매도 거래량")
    orgn_shnu_vol: str = Field(title="기관계 매수2 거래량")
    orgn_seln_tr_pbmn: str = Field(title="기관계 매도 거래 대금")
    orgn_shnu_tr_pbmn: str = Field(title="기관계 매수2 거래 대금")
    scrt_seln_vol: str = Field(title="증권 매도 거래량")
    scrt_shnu_vol: str = Field(title="증권 매수2 거래량")
    scrt_seln_tr_pbmn: str = Field(title="증권 매도 거래 대금")
    scrt_shnu_tr_pbmn: str = Field(title="증권 매수2 거래 대금")
    ivtr_seln_vol: str = Field(title="투자신탁 매도 거래량")
    ivtr_shnu_vol: str = Field(title="투자신탁 매수2 거래량")
    ivtr_seln_tr_pbmn: str = Field(title="투자신탁 매도 거래 대금")
    ivtr_shnu_tr_pbmn: str = Field(title="투자신탁 매수2 거래 대금")
    pe_fund_seln_tr_pbmn: str = Field(title="사모 펀드 매도 거래 대금")
    pe_fund_seln_vol: str = Field(title="사모 펀드 매도 거래량")
    pe_fund_shnu_tr_pbmn: str = Field(title="사모 펀드 매수2 거래 대금")
    pe_fund_shnu_vol: str = Field(title="사모 펀드 매수2 거래량")
    bank_seln_vol: str = Field(title="은행 매도 거래량")
    bank_shnu_vol: str = Field(title="은행 매수2 거래량")
    bank_seln_tr_pbmn: str = Field(title="은행 매도 거래 대금")
    bank_shnu_tr_pbmn: str = Field(title="은행 매수2 거래 대금")
    insu_seln_vol: str = Field(title="보험 매도 거래량")
    insu_shnu_vol: str = Field(title="보험 매수2 거래량")
    insu_seln_tr_pbmn: str = Field(title="보험 매도 거래 대금")
    insu_shnu_tr_pbmn: str = Field(title="보험 매수2 거래 대금")
    mrbn_seln_vol: str = Field(title="종금 매도 거래량")
    mrbn_shnu_vol: str = Field(title="종금 매수2 거래량")
    mrbn_seln_tr_pbmn: str = Field(title="종금 매도 거래 대금")
    mrbn_shnu_tr_pbmn: str = Field(title="종금 매수2 거래 대금")
    fund_seln_vol: str = Field(title="기금 매도 거래량")
    fund_shnu_vol: str = Field(title="기금 매수2 거래량")
    fund_seln_tr_pbmn: str = Field(title="기금 매도 거래 대금")
    fund_shnu_tr_pbmn: str = Field(title="기금 매수2 거래 대금")
    etc_seln_vol: str = Field(title="기타 매도 거래량")
    etc_shnu_vol: str = Field(title="기타 매수2 거래량")
    etc_seln_tr_pbmn: str = Field(title="기타 매도 거래 대금")
    etc_shnu_tr_pbmn: str = Field(title="기타 매수2 거래 대금")
    etc_orgt_seln_vol: str = Field(title="기타 단체 매도 거래량")
    etc_orgt_shnu_vol: str = Field(title="기타 단체 매수2 거래량")
    etc_orgt_seln_tr_pbmn: str = Field(title="기타 단체 매도 거래 대금")
    etc_orgt_shnu_tr_pbmn: str = Field(title="기타 단체 매수2 거래 대금")
    etc_corp_seln_vol: str = Field(title="기타 법인 매도 거래량")
    etc_corp_shnu_vol: str = Field(title="기타 법인 매수2 거래량")
    etc_corp_seln_tr_pbmn: str = Field(title="기타 법인 매도 거래 대금")
    etc_corp_shnu_tr_pbmn: str = Field(title="기타 법인 매수2 거래 대금")
    bold_yn: str = Field(title="BOLD 여부")


class InvestorTradingTrendByStockDaily(BaseModel, KisHttpBody):
    """종목별 투자자매매동향(일별)"""

    output1: InvestorTradingTrendByStockDailyItem1 = Field(title="응답상세1")
    output2: Sequence[InvestorTradingTrendByStockDailyItem2] = Field(default_factory=list)


class InvestorTradingTrendByMarketIntradayItem(BaseModel):
    frgn_seln_vol: str = Field(title="외국인 매도 거래량")
    frgn_shnu_vol: str = Field(title="외국인 매수 거래량")
    frgn_ntby_qty: str = Field(title="외국인 순매수 수량")
    frgn_seln_tr_pbmn: str = Field(title="외국인 매도 거래 대금")
    frgn_shnu_tr_pbmn: str = Field(title="외국인 매수 거래 대금")
    frgn_ntby_tr_pbmn: str = Field(title="외국인 순매수 거래 대금")
    prsn_seln_vol: str = Field(title="개인 매도 거래량")
    prsn_shnu_vol: str = Field(title="개인 매수 거래량")
    prsn_ntby_qty: str = Field(title="개인 순매수 수량")
    prsn_seln_tr_pbmn: str = Field(title="개인 매도 거래 대금")
    prsn_shnu_tr_pbmn: str = Field(title="개인 매수 거래 대금")
    prsn_ntby_tr_pbmn: str = Field(title="개인 순매수 거래 대금")
    orgn_seln_vol: str = Field(title="기관계 매도 거래량")
    orgn_shnu_vol: str = Field(title="기관계 매수 거래량")
    orgn_ntby_qty: str = Field(title="기관계 순매수 수량")
    orgn_seln_tr_pbmn: str = Field(title="기관계 매도 거래 대금")
    orgn_shnu_tr_pbmn: str = Field(title="기관계 매수 거래 대금")
    orgn_ntby_tr_pbmn: str = Field(title="기관계 순매수 거래 대금")
    scrt_seln_vol: str = Field(title="증권 매도 거래량")
    scrt_shnu_vol: str = Field(title="증권 매수 거래량")
    scrt_ntby_qty: str = Field(title="증권 순매수 수량")
    scrt_seln_tr_pbmn: str = Field(title="증권 매도 거래 대금")
    scrt_shnu_tr_pbmn: str = Field(title="증권 매수 거래 대금")
    scrt_ntby_tr_pbmn: str = Field(title="증권 순매수 거래 대금")
    ivtr_seln_vol: str = Field(title="투자신탁 매도 거래량")
    ivtr_shnu_vol: str = Field(title="투자신탁 매수 거래량")
    ivtr_ntby_qty: str = Field(title="투자신탁 순매수 수량")
    ivtr_seln_tr_pbmn: str = Field(title="투자신탁 매도 거래 대금")
    ivtr_shnu_tr_pbmn: str = Field(title="투자신탁 매수 거래 대금")
    ivtr_ntby_tr_pbmn: str = Field(title="투자신탁 순매수 거래 대금")
    pe_fund_seln_tr_pbmn: str = Field(title="사모 펀드 매도 거래 대금")
    pe_fund_seln_vol: str = Field(title="사모 펀드 매도 거래량")
    pe_fund_ntby_vol: str = Field(title="사모 펀드 순매수 거래량")
    pe_fund_shnu_tr_pbmn: str = Field(title="사모 펀드 매수 거래 대금")
    pe_fund_shnu_vol: str = Field(title="사모 펀드 매수 거래량")
    pe_fund_ntby_tr_pbmn: str = Field(title="사모 펀드 순매수 거래 대금")
    bank_seln_vol: str = Field(title="은행 매도 거래량")
    bank_shnu_vol: str = Field(title="은행 매수 거래량")
    bank_ntby_qty: str = Field(title="은행 순매수 수량")
    bank_seln_tr_pbmn: str = Field(title="은행 매도 거래 대금")
    bank_shnu_tr_pbmn: str = Field(title="은행 매수 거래 대금")
    bank_ntby_tr_pbmn: str = Field(title="은행 순매수 거래 대금")
    insu_seln_vol: str = Field(title="보험 매도 거래량")
    insu_shnu_vol: str = Field(title="보험 매수 거래량")
    insu_ntby_qty: str = Field(title="보험 순매수 수량")
    insu_seln_tr_pbmn: str = Field(title="보험 매도 거래 대금")
    insu_shnu_tr_pbmn: str = Field(title="보험 매수 거래 대금")
    insu_ntby_tr_pbmn: str = Field(title="보험 순매수 거래 대금")
    mrbn_seln_vol: str = Field(title="종금 매도 거래량")
    mrbn_shnu_vol: str = Field(title="종금 매수 거래량")
    mrbn_ntby_qty: str = Field(title="종금 순매수 수량")
    mrbn_seln_tr_pbmn: str = Field(title="종금 매도 거래 대금")
    mrbn_shnu_tr_pbmn: str = Field(title="종금 매수 거래 대금")
    mrbn_ntby_tr_pbmn: str = Field(title="종금 순매수 거래 대금")
    fund_seln_vol: str = Field(title="기금 매도 거래량")
    fund_shnu_vol: str = Field(title="기금 매수 거래량")
    fund_ntby_qty: str = Field(title="기금 순매수 수량")
    fund_seln_tr_pbmn: str = Field(title="기금 매도 거래 대금")
    fund_shnu_tr_pbmn: str = Field(title="기금 매수 거래 대금")
    fund_ntby_tr_pbmn: str = Field(title="기금 순매수 거래 대금")
    etc_orgt_seln_vol: str = Field(title="기타 단체 매도 거래량")
    etc_orgt_shnu_vol: str = Field(title="기타 단체 매수 거래량")
    etc_orgt_ntby_vol: str = Field(title="기타 단체 순매수 거래량")
    etc_orgt_seln_tr_pbmn: str = Field(title="기타 단체 매도 거래 대금")
    etc_orgt_shnu_tr_pbmn: str = Field(title="기타 단체 매수 거래 대금")
    etc_orgt_ntby_tr_pbmn: str = Field(title="기타 단체 순매수 거래 대금")
    etc_corp_seln_vol: str = Field(title="기타 법인 매도 거래량")
    etc_corp_shnu_vol: str = Field(title="기타 법인 매수 거래량")
    etc_corp_ntby_vol: str = Field(title="기타 법인 순매수 거래량")
    etc_corp_seln_tr_pbmn: str = Field(title="기타 법인 매도 거래 대금")
    etc_corp_shnu_tr_pbmn: str = Field(title="기타 법인 매수 거래 대금")
    etc_corp_ntby_tr_pbmn: str = Field(title="기타 법인 순매수 거래 대금")


class InvestorTradingTrendByMarketIntraday(BaseModel, KisHttpBody):
    """시장별 투자자매매동향(시세)"""

    output: Sequence[InvestorTradingTrendByMarketIntradayItem] = Field(default_factory=list)


class InvestorTradingTrendByMarketDailyItem1(BaseModel):
    stck_bsop_date: str = Field(title="주식 영업 일자")
    bstp_nmix_prpr: str = Field(title="업종 지수 현재가")
    bstp_nmix_prdy_vrss: str = Field(title="업종 지수 전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    bstp_nmix_prdy_ctrt: str = Field(title="업종 지수 전일 대비율")
    bstp_nmix_oprc: str = Field(title="업종 지수 시가2")
    bstp_nmix_hgpr: str = Field(title="업종 지수 최고가")
    bstp_nmix_lwpr: str = Field(title="업종 지수 최저가")
    stck_prdy_clpr: str = Field(title="주식 전일 종가")
    frgn_ntby_qty: str = Field(title="외국인 순매수 수량")
    frgn_reg_ntby_qty: str = Field(title="외국인 등록 순매수 수량")
    frgn_nreg_ntby_qty: str = Field(title="외국인 비등록 순매수 수량")
    prsn_ntby_qty: str = Field(title="개인 순매수 수량")
    orgn_ntby_qty: str = Field(title="기관계 순매수 수량")
    scrt_ntby_qty: str = Field(title="증권 순매수 수량")
    ivtr_ntby_qty: str = Field(title="투자신탁 순매수 수량")
    pe_fund_ntby_vol: str = Field(title="사모 펀드 순매수 거래량")
    bank_ntby_qty: str = Field(title="은행 순매수 수량")
    insu_ntby_qty: str = Field(title="보험 순매수 수량")
    mrbn_ntby_qty: str = Field(title="종금 순매수 수량")
    fund_ntby_qty: str = Field(title="기금 순매수 수량")
    etc_ntby_qty: str = Field(title="기타 순매수 수량")
    etc_orgt_ntby_vol: str = Field(title="기타 단체 순매수 거래량")
    etc_corp_ntby_vol: str = Field(title="기타 법인 순매수 거래량")
    frgn_ntby_tr_pbmn: str = Field(title="외국인 순매수 거래 대금")
    frgn_reg_ntby_pbmn: str = Field(title="외국인 등록 순매수 대금")
    frgn_nreg_ntby_pbmn: str = Field(title="외국인 비등록 순매수 대금")
    prsn_ntby_tr_pbmn: str = Field(title="개인 순매수 거래 대금")
    orgn_ntby_tr_pbmn: str = Field(title="기관계 순매수 거래 대금")
    scrt_ntby_tr_pbmn: str = Field(title="증권 순매수 거래 대금")
    ivtr_ntby_tr_pbmn: str = Field(title="투자신탁 순매수 거래 대금")
    pe_fund_ntby_tr_pbmn: str = Field(title="사모 펀드 순매수 거래 대금")
    bank_ntby_tr_pbmn: str = Field(title="은행 순매수 거래 대금")
    insu_ntby_tr_pbmn: str = Field(title="보험 순매수 거래 대금")
    mrbn_ntby_tr_pbmn: str = Field(title="종금 순매수 거래 대금")
    fund_ntby_tr_pbmn: str = Field(title="기금 순매수 거래 대금")
    etc_ntby_tr_pbmn: str = Field(title="기타 순매수 거래 대금")
    etc_orgt_ntby_tr_pbmn: str = Field(title="기타 단체 순매수 거래 대금")
    etc_corp_ntby_tr_pbmn: str = Field(title="기타 법인 순매수 거래 대금")


class InvestorTradingTrendByMarketDaily(BaseModel, KisHttpBody):
    """시장별 투자자매매동향(일별)"""

    output: Sequence[InvestorTradingTrendByMarketDailyItem1] = Field(default_factory=list)


class ForeignNetBuyTrendByStockItem1(BaseModel):
    bsop_hour: str = Field(title="영업시간")
    stck_prpr: str = Field(title="주식현재가")
    prdy_vrss: str = Field(title="전일대비")
    prdy_vrss_sign: str = Field(title="전일대비부호")
    prdy_ctrt: str = Field(title="전일대비율")
    acml_vol: str = Field(title="누적거래량")
    frgn_seln_vol: str = Field(title="외국인매도거래량")
    frgn_shnu_vol: str = Field(title="외국인매수거래량")
    glob_ntby_qty: str = Field(title="외국계순매수수량")
    frgn_ntby_qty_icdc: str = Field(title="외국인순매수수량증감")


class ForeignNetBuyTrendByStock(BaseModel, KisHttpBody):
    """종목별 외국계 순매수추이"""

    output: Sequence[ForeignNetBuyTrendByStockItem1] = Field(default_factory=list)


class MemberTradingTrendTickSummaryItem(BaseModel):
    total_seln_qty: str = Field(title="총매도수량")
    total_shnu_qty: str = Field(title="총매수2수량")


class MemberTradingTrendTickItem(BaseModel):
    bsop_hour: str = Field(title="영업시간")
    mbcr_name: str = Field(title="회원사명")
    hts_kor_isnm: str = Field(title="HTS한글종목명")
    stck_prpr: str = Field(title="주식현재가")
    prdy_vrss: str = Field(title="전일대비")
    prdy_vrss_sign: str = Field(title="전일대비부호")
    cntg_vol: str = Field(title="체결거래량")
    acml_ntby_qty: str = Field(title="누적순매수수량")
    glob_ntby_qty: str = Field(title="외국계순매수수량")
    frgn_ntby_qty_icdc: str = Field(title="외국인순매수수량증감")


class MemberTradingTrendTick(BaseModel, KisHttpBody):
    """회원사 실시간 매매동향(틱)"""

    output1: Sequence[MemberTradingTrendTickSummaryItem] = Field(default_factory=list)
    output2: Sequence[MemberTradingTrendTickItem] = Field(default_factory=list)


class MemberTradingTrendByStockItem(BaseModel):
    stck_bsop_date: str = Field(title="주식영업일자")
    total_seln_qty: str = Field(title="총매도수량")
    total_shnu_qty: str = Field(title="총매수2수량")
    ntby_qty: str = Field(title="순매수수량")
    stck_prpr: str = Field(title="주식현재가")
    prdy_vrss: str = Field(title="전일대비")
    prdy_vrss_sign: str = Field(title="전일대비부호")
    prdy_ctrt: str = Field(title="전일대비율")
    acml_vol: str = Field(title="누적거래량")


class MemberTradingTrendByStock(BaseModel, KisHttpBody):
    """주식현재가 회원사 종목매매동향"""

    output: Sequence[MemberTradingTrendByStockItem] = Field(default_factory=list)


class ProgramTradingTrendByStockIntradayItem(BaseModel):
    bsop_hour: str = Field(title="영업 시간")
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    whol_smtn_seln_vol: str = Field(title="전체 합계 매도 거래량")
    whol_smtn_shnu_vol: str = Field(title="전체 합계 매수2 거래량")
    whol_smtn_ntby_qty: str = Field(title="전체 합계 순매수 수량")
    whol_smtn_seln_tr_pbmn: str = Field(title="전체 합계 매도 거래 대금")
    whol_smtn_shnu_tr_pbmn: str = Field(title="전체 합계 매수2 거래 대금")
    whol_smtn_ntby_tr_pbmn: str = Field(title="전체 합계 순매수 거래 대금")
    whol_ntby_vol_icdc: str = Field(title="전체 순매수 거래량 증감")
    whol_ntby_tr_pbmn_icdc: str = Field(title="전체 순매수 거래 대금 증감")


class ProgramTradingTrendByStockIntraday(BaseModel, KisHttpBody):
    """종목별 프로그램매매추이(체결)"""

    output: Sequence[ProgramTradingTrendByStockIntradayItem] = Field(default_factory=list)


class ProgramTradingTrendByStockDailyItem(BaseModel):
    stck_bsop_date: str = Field(title="주식 영업 일자")
    stck_clpr: str = Field(title="주식 종가")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    acml_tr_pbmn: str = Field(title="누적 거래 대금")
    whol_smtn_seln_vol: str = Field(title="전체 합계 매도 거래량")
    whol_smtn_shnu_vol: str = Field(title="전체 합계 매수2 거래량")
    whol_smtn_ntby_qty: str = Field(title="전체 합계 순매수 수량")
    whol_smtn_seln_tr_pbmn: str = Field(title="전체 합계 매도 거래 대금")
    whol_smtn_shnu_tr_pbmn: str = Field(title="전체 합계 매수2 거래 대금")
    whol_smtn_ntby_tr_pbmn: str = Field(title="전체 합계 순매수 거래 대금")
    whol_ntby_vol_icdc: str = Field(title="전체 순매수 거래량 증감")
    whol_ntby_tr_pbmn_icdc2: str = Field(title="전체 순매수 거래 대금 증감2")


class ProgramTradingTrendByStockDaily(BaseModel, KisHttpBody):
    """종목별 프로그램매매추이(일별)"""

    output: Sequence[ProgramTradingTrendByStockDailyItem] = Field(default_factory=list)


class ForeignInstitutionalEstimateByStockItem(BaseModel):
    bsop_hour_gb: str = Field(
        title="입력구분",
        description="1: 09시 30분 입력\n2: 10시 00분 입력\n3: 11시 20분 입력\n4: 13시 20분 입력\n5: 14시 30분 입력",
    )
    frgn_fake_ntby_qty: str = Field(title="외국인수량(가집계)")
    orgn_fake_ntby_qty: str = Field(title="기관수량(가집계)")
    sum_fake_ntby_qty: str = Field(title="합산수량(가집계)")


class ForeignInstitutionalEstimateByStock(BaseModel, KisHttpBody):
    """종목별 외인기관 추정기전계"""

    output2: Sequence[ForeignInstitutionalEstimateByStockItem] = Field(default_factory=list)


class BuySellVolumeByStockDailyItem1(BaseModel):
    shnu_cnqn_smtn: str = Field(title="매수 체결량 합계")
    seln_cnqn_smtn: str = Field(title="매도 체결량 합계")


class BuySellVolumeByStockDailyItem2(BaseModel):
    stck_bsop_date: str = Field(title="거래상태정보")
    total_seln_qty: str = Field(title="총 매도 수량")
    total_shnu_qty: str = Field(title="총 매수 수량")


class BuySellVolumeByStockDaily(BaseModel, KisHttpBody):
    """종목별일별매수매도체결량"""

    output1: BuySellVolumeByStockDailyItem1 = Field(title="응답상세1")
    output2: Sequence[BuySellVolumeByStockDailyItem2] = Field(default_factory=list)


class ProgramTradingSummaryIntradayItem(BaseModel):
    bsop_hour: str = Field(title="영업 시간")
    arbt_smtn_seln_tr_pbmn: str = Field(title="차익 합계 매도 거래 대금")
    arbt_smtn_shnu_tr_pbmn: str = Field(title="차익 합계 매수2 거래 대금")
    nabt_smtn_seln_tr_pbmn: str = Field(title="비차익 합계 매도 거래 대금")
    nabt_smtn_shnu_tr_pbmn: str = Field(title="비차익 합계 매수2 거래 대금")
    arbt_smtn_ntby_tr_pbmn: str = Field(title="차익 합계 순매수 거래 대금")
    nabt_smtn_ntby_tr_pbmn: str = Field(title="비차익 합계 순매수 거래 대금")
    whol_smtn_ntby_tr_pbmn: str = Field(title="전체 합계 순매수 거래 대금")
    bstp_nmix_prpr: str = Field(title="업종 지수 현재가")
    bstp_nmix_prdy_vrss: str = Field(title="업종 지수 전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")


class ProgramTradingSummaryIntraday(BaseModel, KisHttpBody):
    """프로그램매매 종합현황(시간)"""

    output: Sequence[ProgramTradingSummaryIntradayItem] = Field(default_factory=list)


class ProgramTradingSummaryDailyItem(BaseModel):
    stck_bsop_date: str = Field(title="주식 영업 일자")
    nabt_entm_seln_tr_pbmn: str = Field(title="비차익 위탁 매도 거래 대금")
    nabt_onsl_seln_vol: str = Field(title="비차익 자기 매도 거래량")
    whol_onsl_seln_tr_pbmn: str = Field(title="전체 자기 매도 거래 대금")
    arbt_smtn_shnu_vol: str = Field(title="차익 합계 매수2 거래량")
    nabt_smtn_shnu_tr_pbmn: str = Field(title="비차익 합계 매수2 거래 대금")
    arbt_entm_ntby_qty: str = Field(title="차익 위탁 순매수 수량")
    nabt_entm_ntby_tr_pbmn: str = Field(title="비차익 위탁 순매수 거래 대금")
    arbt_entm_seln_vol: str = Field(title="차익 위탁 매도 거래량")
    nabt_entm_seln_vol_rate: str = Field(title="비차익 위탁 매도 거래량 비율")
    nabt_onsl_seln_vol_rate: str = Field(title="비차익 자기 매도 거래량 비율")
    whol_onsl_seln_tr_pbmn_rate: str = Field(title="전체 자기 매도 거래 대금 비율")
    arbt_smtm_shun_vol_rate: str = Field(title="차익 합계 매수 거래량 비율")
    nabt_smtm_shun_tr_pbmn_rate: str = Field(title="비차익 합계 매수 거래대금 비율")
    arbt_entm_ntby_qty_rate: str = Field(title="차익 위탁 순매수 수량 비율")
    nabt_entm_ntby_tr_pbmn_rate: str = Field(title="비차익 위탁 순매수 거래 대금")
    arbt_entm_seln_vol_rate: str = Field(title="차익 위탁 매도 거래량 비율")
    nabt_entm_seln_tr_pbmn_rate: str = Field(title="비차익 위탁 매도 거래 대금 비")
    nabt_onsl_seln_tr_pbmn: str = Field(title="비차익 자기 매도 거래 대금")
    whol_smtn_seln_vol: str = Field(title="전체 합계 매도 거래량")
    arbt_smtn_shnu_tr_pbmn: str = Field(title="차익 합계 매수2 거래 대금")
    whol_entm_shnu_vol: str = Field(title="전체 위탁 매수2 거래량")
    arbt_entm_ntby_tr_pbmn: str = Field(title="차익 위탁 순매수 거래 대금")
    nabt_onsl_ntby_qty: str = Field(title="비차익 자기 순매수 수량")
    arbt_entm_seln_tr_pbmn: str = Field(title="차익 위탁 매도 거래 대금")
    nabt_onsl_seln_tr_pbmn_rate: str = Field(title="비차익 자기 매도 거래 대금 비")
    whol_seln_vol_rate: str = Field(title="전체 매도 거래량 비율")
    arbt_smtm_shun_tr_pbmn_rate: str = Field(title="차익 합계 매수 거래대금 비율")
    whol_entm_shnu_vol_rate: str = Field(title="전체 위탁 매수 거래량 비율")
    arbt_entm_ntby_tr_pbmn_rate: str = Field(title="차익 위탁 순매수 거래 대금 비")
    nabt_onsl_ntby_qty_rate: str = Field(title="비차익 자기 순매수 수량 비율")
    arbt_entm_seln_tr_pbmn_rate: str = Field(title="차익 위탁 매도 거래 대금 비율")
    nabt_smtn_seln_vol: str = Field(title="비차익 합계 매도 거래량")
    whol_smtn_seln_tr_pbmn: str = Field(title="전체 합계 매도 거래 대금")
    nabt_entm_shnu_vol: str = Field(title="비차익 위탁 매수2 거래량")
    whol_entm_shnu_tr_pbmn: str = Field(title="전체 위탁 매수2 거래 대금")
    arbt_onsl_ntby_qty: str = Field(title="차익 자기 순매수 수량")
    nabt_onsl_ntby_tr_pbmn: str = Field(title="비차익 자기 순매수 거래 대금")
    arbt_onsl_seln_tr_pbmn: str = Field(title="차익 자기 매도 거래 대금")
    nabt_smtm_seln_vol_rate: str = Field(title="비차익 합계 매도 거래량 비율")
    whol_seln_tr_pbmn_rate: str = Field(title="전체 매도 거래대금 비율")
    nabt_entm_shnu_vol_rate: str = Field(title="비차익 위탁 매수 거래량 비율")
    whol_entm_shnu_tr_pbmn_rate: str = Field(title="전체 위탁 매수 거래 대금 비율")
    arbt_onsl_ntby_qty_rate: str = Field(title="차익 자기 순매수 수량 비율")
    nabt_onsl_ntby_tr_pbmn_rate: str = Field(title="비차익 자기 순매수 거래 대금")
    arbt_onsl_seln_tr_pbmn_rate: str = Field(title="차익 자기 매도 거래 대금 비율")
    nabt_smtn_seln_tr_pbmn: str = Field(title="비차익 합계 매도 거래 대금")
    arbt_entm_shnu_vol: str = Field(title="차익 위탁 매수2 거래량")
    nabt_entm_shnu_tr_pbmn: str = Field(title="비차익 위탁 매수2 거래 대금")
    whol_onsl_shnu_vol: str = Field(title="전체 자기 매수2 거래량")
    arbt_onsl_ntby_tr_pbmn: str = Field(title="차익 자기 순매수 거래 대금")
    nabt_smtn_ntby_qty: str = Field(title="비차익 합계 순매수 수량")
    arbt_onsl_seln_vol: str = Field(title="차익 자기 매도 거래량")
    nabt_smtm_seln_tr_pbmn_rate: str = Field(title="비차익 합계 매도 거래대금 비율")
    arbt_entm_shnu_vol_rate: str = Field(title="차익 위탁 매수 거래량 비율")
    nabt_entm_shnu_tr_pbmn_rate: str = Field(title="비차익 위탁 매수 거래 대금 비")
    whol_onsl_shnu_tr_pbmn: str = Field(title="전체 자기 매수2 거래 대금")
    arbt_onsl_ntby_tr_pbmn_rate: str = Field(title="차익 자기 순매수 거래 대금 비")
    nabt_smtm_ntby_qty_rate: str = Field(title="비차익 합계 순매수 수량 비율")
    arbt_onsl_seln_vol_rate: str = Field(title="차익 자기 매도 거래량 비율")
    whol_entm_seln_vol: str = Field(title="전체 위탁 매도 거래량")
    arbt_entm_shnu_tr_pbmn: str = Field(title="차익 위탁 매수2 거래 대금")
    nabt_onsl_shnu_vol: str = Field(title="비차익 자기 매수2 거래량")
    whol_onsl_shnu_tr_pbmn_rate: str = Field(title="전체 자기 매수 거래 대금 비율")
    arbt_smtn_ntby_qty: str = Field(title="차익 합계 순매수 수량")
    nabt_smtn_ntby_tr_pbmn: str = Field(title="비차익 합계 순매수 거래 대금")
    arbt_smtn_seln_vol: str = Field(title="차익 합계 매도 거래량")
    whol_entm_seln_tr_pbmn: str = Field(title="전체 위탁 매도 거래 대금")
    arbt_entm_shnu_tr_pbmn_rate: str = Field(title="차익 위탁 매수 거래 대금 비율")
    nabt_onsl_shnu_vol_rate: str = Field(title="비차익 자기 매수 거래량 비율")
    whol_onsl_shnu_vol_rate: str = Field(title="전체 자기 매수 거래량 비율")
    arbt_smtm_ntby_qty_rate: str = Field(title="차익 합계 순매수 수량 비율")
    nabt_smtm_ntby_tr_pbmn_rate: str = Field(title="비차익 합계 순매수 거래대금 비")
    arbt_smtm_seln_vol_rate: str = Field(title="차익 합계 매도 거래량 비율")
    whol_entm_seln_vol_rate: str = Field(title="전체 위탁 매도 거래량 비율")
    arbt_onsl_shnu_vol: str = Field(title="차익 자기 매수2 거래량")
    nabt_onsl_shnu_tr_pbmn: str = Field(title="비차익 자기 매수2 거래 대금")
    whol_smtn_shnu_vol: str = Field(title="전체 합계 매수2 거래량")
    arbt_smtn_ntby_tr_pbmn: str = Field(title="차익 합계 순매수 거래 대금")
    whol_entm_ntby_qty: str = Field(title="전체 위탁 순매수 수량")
    arbt_smtn_seln_tr_pbmn: str = Field(title="차익 합계 매도 거래 대금")
    whol_entm_seln_tr_pbmn_rate: str = Field(title="전체 위탁 매도 거래 대금 비율")
    arbt_onsl_shnu_vol_rate: str = Field(title="차익 자기 매수 거래량 비율")
    nabt_onsl_shnu_tr_pbmn_rate: str = Field(title="비차익 자기 매수 거래 대금 비")
    whol_shun_vol_rate: str = Field(title="전체 매수 거래량 비율")
    arbt_smtm_ntby_tr_pbmn_rate: str = Field(title="차익 합계 순매수 거래대금 비율")
    whol_entm_ntby_qty_rate: str = Field(title="전체 위탁 순매수 수량 비율")
    arbt_smtm_seln_tr_pbmn_rate: str = Field(title="차익 합계 매도 거래대금 비율")
    whol_onsl_seln_vol: str = Field(title="전체 자기 매도 거래량")
    arbt_onsl_shnu_tr_pbmn: str = Field(title="차익 자기 매수2 거래 대금")
    nabt_smtn_shnu_vol: str = Field(title="비차익 합계 매수2 거래량")
    whol_smtn_shnu_tr_pbmn: str = Field(title="전체 합계 매수2 거래 대금")
    nabt_entm_ntby_qty: str = Field(title="비차익 위탁 순매수 수량")
    whol_entm_ntby_tr_pbmn: str = Field(title="전체 위탁 순매수 거래 대금")
    nabt_entm_seln_vol: str = Field(title="비차익 위탁 매도 거래량")
    whol_onsl_seln_vol_rate: str = Field(title="전체 자기 매도 거래량 비율")
    arbt_onsl_shnu_tr_pbmn_rate: str = Field(title="차익 자기 매수 거래 대금 비율")
    nabt_smtm_shun_vol_rate: str = Field(title="비차익 합계 매수 거래량 비율")
    whol_shun_tr_pbmn_rate: str = Field(title="전체 매수 거래대금 비율")
    nabt_entm_ntby_qty_rate: str = Field(title="비차익 위탁 순매수 수량 비율")


class ProgramTradingSummaryDaily(BaseModel, KisHttpBody):
    """프로그램매매 종합현황(일별)"""

    output: Sequence[ProgramTradingSummaryDailyItem] = Field(default_factory=list)


class ProgramTradingInvestorTrendTodayItem(BaseModel):
    invr_cls_code: str = Field(title="투자자코드")
    all_seln_qty: str = Field(title="전체매도수량")
    all_seln_amt: str = Field(title="전체매도대금")
    invr_cls_name: str = Field(title="투자자 구분 명")
    all_shnu_qty: str = Field(title="전체매수수량")
    all_shnu_amt: str = Field(title="전체매수대금")
    all_ntby_amt: str = Field(title="전체순매수대금")
    arbt_seln_qty: str = Field(title="차익매도수량")
    all_ntby_qty: str = Field(title="전체순매수수량")
    arbt_shnu_qty: str = Field(title="차익매수수량")
    arbt_ntby_qty: str = Field(title="차익순매수수량")
    arbt_seln_amt: str = Field(title="차익매도대금")
    arbt_shnu_amt: str = Field(title="차익매수대금")
    arbt_ntby_amt: str = Field(title="차익순매수대금")
    nabt_seln_qty: str = Field(title="비차익매도수량")
    nabt_shnu_qty: str = Field(title="비차익매수수량")
    nabt_ntby_qty: str = Field(title="비차익순매수수량")
    nabt_seln_amt: str = Field(title="비차익매도대금")
    nabt_shnu_amt: str = Field(title="비차익매수대금")
    nabt_ntby_amt: str = Field(title="비차익순매수대금")


class ProgramTradingInvestorTrendToday(BaseModel, KisHttpBody):
    """프로그램매매 투자자매매동향(당일)"""

    output1: Sequence[ProgramTradingInvestorTrendTodayItem] = Field(default_factory=list)


class CreditBalanceTrendDailyItem(BaseModel):
    deal_date: str = Field(title="매매 일자")
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    stlm_date: str = Field(title="결제 일자")
    whol_loan_new_stcn: str = Field(title="전체 융자 신규 주수", description="단위: 주")
    whol_loan_rdmp_stcn: str = Field(title="전체 융자 상환 주수", description="단위: 주")
    whol_loan_rmnd_stcn: str = Field(title="전체 융자 잔고 주수", description="단위: 주")
    whol_loan_new_amt: str = Field(title="전체 융자 신규 금액", description="단위: 만원")
    whol_loan_rdmp_amt: str = Field(title="전체 융자 상환 금액", description="단위: 만원")
    whol_loan_rmnd_amt: str = Field(title="전체 융자 잔고 금액", description="단위: 만원")
    whol_loan_rmnd_rate: str = Field(title="전체 융자 잔고 비율")
    whol_loan_gvrt: str = Field(title="전체 융자 공여율")
    whol_stln_new_stcn: str = Field(title="전체 대주 신규 주수", description="단위: 주")
    whol_stln_rdmp_stcn: str = Field(title="전체 대주 상환 주수", description="단위: 주")
    whol_stln_rmnd_stcn: str = Field(title="전체 대주 잔고 주수", description="단위: 주")
    whol_stln_new_amt: str = Field(title="전체 대주 신규 금액", description="단위: 만원")
    whol_stln_rdmp_amt: str = Field(title="전체 대주 상환 금액", description="단위: 만원")
    whol_stln_rmnd_amt: str = Field(title="전체 대주 잔고 금액", description="단위: 만원")
    whol_stln_rmnd_rate: str = Field(title="전체 대주 잔고 비율")
    whol_stln_gvrt: str = Field(title="전체 대주 공여율")
    stck_oprc: str = Field(title="주식 시가2")
    stck_hgpr: str = Field(title="주식 최고가")
    stck_lwpr: str = Field(title="주식 최저가")


class CreditBalanceTrendDaily(BaseModel, KisHttpBody):
    """국내주식 신용잔고 일별추이"""

    output: Sequence[CreditBalanceTrendDailyItem] = Field(default_factory=list)


class ExpectedPriceTrendItem1(BaseModel):
    rprs_mrkt_kor_name: str = Field(title="대표 시장 한글 명")
    antc_cnpr: str = Field(title="예상 체결가")
    antc_cntg_vrss_sign: str = Field(title="예상 체결 대비 부호")
    antc_cntg_vrss: str = Field(title="예상 체결 대비")
    antc_cntg_prdy_ctrt: str = Field(title="예상 체결 전일 대비율")
    antc_vol: str = Field(title="예상 거래량")
    antc_tr_pbmn: str = Field(title="예상 거래대금")


class ExpectedPriceTrendItem2(BaseModel):
    stck_bsop_date: str = Field(title="주식 영업 일자")
    stck_cntg_hour: str = Field(title="주식 체결 시간")
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")


class ExpectedPriceTrend(BaseModel, KisHttpBody):
    """국내주식 예상체결가 추이"""

    output1: ExpectedPriceTrendItem1 = Field(title="응답상세1")
    output2: Sequence[ExpectedPriceTrendItem2] = Field(default_factory=list)


class ShortSellingTrendDailyItem1(BaseModel):
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    prdy_vol: str = Field(title="전일 거래량")


class ShortSellingTrendDailyItem2(BaseModel):
    stck_bsop_date: str = Field(title="주식 영업 일자")
    stck_clpr: str = Field(title="주식 종가")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    stnd_vol_smtn: str = Field(title="기준 거래량 합계")
    ssts_cntg_qty: str = Field(title="공매도 체결 수량")
    ssts_vol_rlim: str = Field(title="공매도 거래량 비중")
    acml_ssts_cntg_qty: str = Field(title="누적 공매도 체결 수량")
    acml_ssts_cntg_qty_rlim: str = Field(title="누적 공매도 체결 수량 비중")
    acml_tr_pbmn: str = Field(title="누적 거래 대금")
    stnd_tr_pbmn_smtn: str = Field(title="기준 거래대금 합계")
    ssts_tr_pbmn: str = Field(title="공매도 거래 대금")
    ssts_tr_pbmn_rlim: str = Field(title="공매도 거래대금 비중")
    acml_ssts_tr_pbmn: str = Field(title="누적 공매도 거래 대금")
    acml_ssts_tr_pbmn_rlim: str = Field(title="누적 공매도 거래 대금 비중")
    stck_oprc: str = Field(title="주식 시가2")
    stck_hgpr: str = Field(title="주식 최고가")
    stck_lwpr: str = Field(title="주식 최저가")
    avrg_prc: str = Field(title="평균가격")


class ShortSellingTrendDaily(BaseModel, KisHttpBody):
    """국내주식 공매도 일별추이"""

    output1: ShortSellingTrendDailyItem1 = Field(title="응답상세1")
    output2: Sequence[ShortSellingTrendDailyItem2] = Field(default_factory=list)


class AfterHoursExpectedFluctuationItem(BaseModel):
    data_rank: str = Field(title="데이터 순위")
    iscd_stat_cls_code: str = Field(title="종목 상태 구분 코드")
    stck_shrn_iscd: str = Field(title="주식 단축 종목코드")
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    ovtm_untp_antc_cnpr: str = Field(title="시간외 단일가 예상 체결가")
    ovtm_untp_antc_cntg_vrss: str = Field(title="시간외 단일가 예상 체결 대비")
    ovtm_untp_antc_cntg_vrsssign: str = Field(title="시간외 단일가 예상 체결 대비")
    ovtm_untp_antc_cntg_ctrt: str = Field(title="시간외 단일가 예상 체결 대비율")
    ovtm_untp_askp_rsqn1: str = Field(title="시간외 단일가 매도호가 잔량1")
    ovtm_untp_bidp_rsqn1: str = Field(title="시간외 단일가 매수호가 잔량1")
    ovtm_untp_antc_cnqn: str = Field(title="시간외 단일가 예상 체결량")
    itmt_vol: str = Field(title="장중 거래량")
    stck_prpr: str = Field(title="주식 현재가")


class AfterHoursExpectedFluctuation(BaseModel, KisHttpBody):
    """국내주식 시간외예상체결등락율"""

    output: Sequence[AfterHoursExpectedFluctuationItem] = Field(default_factory=list)


class TradingWeightByAmountItem(BaseModel):
    prpr_name: str = Field(title="가격명")
    smtn_avrg_prpr: str = Field(title="합계 평균가격")
    acml_vol: str = Field(title="합계 거래량")
    whol_ntby_qty_rate: str = Field(title="합계 순매수비율")
    ntby_cntg_csnu: str = Field(title="합계 순매수건수")
    seln_cnqn_smtn: str = Field(title="매도 거래량")
    whol_seln_vol_rate: str = Field(title="매도 거래량비율")
    seln_cntg_csnu: str = Field(title="매도 건수")
    shnu_cnqn_smtn: str = Field(title="매수 거래량")
    whol_shun_vol_rate: str = Field(title="매수 거래량비율")
    shnu_cntg_csnu: str = Field(title="매수 건수")


class TradingWeightByAmount(BaseModel, KisHttpBody):
    """국내주식 체결금액별 매매비중"""

    output: Sequence[TradingWeightByAmountItem] = Field(default_factory=list)


class MarketFundSummaryItem(BaseModel):
    bsop_date: str = Field(title="영업일자")
    bstp_nmix_prpr: str = Field(title="업종지수현재가")
    bstp_nmix_prdy_vrss: str = Field(title="업종지수전일대비")
    prdy_vrss_sign: str = Field(title="전일대비부호", description="1. 상한 2. 상승 3. 보합 4. 하한 5. 하락")
    prdy_ctrt: str = Field(title="전일대비율")
    hts_avls: str = Field(title="HTS시가총액", description="단위: 백만원")
    cust_dpmn_amt: str = Field(title="고객예탁금금액", description="단위: 억원")
    cust_dpmn_amt_prdy_vrss: str = Field(title="고객예탁금금액전일대비")
    amt_tnrt: str = Field(title="금액회전율")
    uncl_amt: str = Field(title="미수금액", description="단위: 억원")
    crdt_loan_rmnd: str = Field(title="신용융자잔고", description="단위: 억원")
    futs_tfam_amt: str = Field(title="선물예수금금액", description="단위: 억원")
    sttp_amt: str = Field(title="주식형금액", description="단위: 억원")
    mxtp_amt: str = Field(title="혼합형금액", description="단위: 억원")
    bntp_amt: str = Field(title="채권형금액", description="단위: 억원")
    mmf_amt: str = Field(title="MMF금액", description="단위: 억원")
    secu_lend_amt: str = Field(title="담보대출잔고금액", description="단위: 억원")


class MarketFundSummary(BaseModel, KisHttpBody):
    """국내 증시자금 종합"""

    output: Sequence[MarketFundSummaryItem] = Field(default_factory=list)


class StockLoanTrendDailyItem(BaseModel):
    bsop_date: str = Field(title="일자")
    stck_prpr: str = Field(title="주식 종가")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    new_stcn: str = Field(title="당일 증가 주수 (체결)")
    rdmp_stcn: str = Field(title="당일 감소 주수 (상환)")
    prdy_rmnd_vrss: str = Field(title="대차거래 증감")
    rmnd_stcn: str = Field(title="당일 잔고 주수")
    rmnd_amt: str = Field(title="당일 잔고 금액")


class StockLoanTrendDaily(BaseModel, KisHttpBody):
    """종목별 일별 대차거래추이"""

    output1: Sequence[StockLoanTrendDailyItem] = Field(default_factory=list)


class LimitPriceStocksItem(BaseModel):
    mksc_shrn_iscd: str = Field(title="유가증권단축종목코드")
    hts_kor_isnm: str = Field(title="HTS한글종목명")
    stck_prpr: str = Field(title="주식현재가")
    prdy_vrss_sign: str = Field(title="전일대비부호")
    prdy_vrss: str = Field(title="전일대비")
    prdy_ctrt: str = Field(title="전일대비율")
    acml_vol: str = Field(title="누적거래량")
    total_askp_rsqn: str = Field(title="총매도호가잔량")
    total_bidp_rsqn: str = Field(title="총매수호가잔량")
    askp_rsqn1: str = Field(title="매도호가잔량1")
    bidp_rsqn1: str = Field(title="매수호가잔량1")
    prdy_vol: str = Field(title="전일거래량")
    seln_cnqn: str = Field(title="매도체결량")
    shnu_cnqn: str = Field(title="매수2체결량")
    stck_llam: str = Field(title="주식하한가")
    stck_mxpr: str = Field(title="주식상한가")
    prdy_vrss_vol_rate: str = Field(title="전일대비거래량비율")


class LimitPriceStocks(BaseModel, KisHttpBody):
    """국내주식 상하한가 표착"""

    output: Sequence[LimitPriceStocksItem] = Field(default_factory=list)


class ResistanceLevelTradingWeightItem1(BaseModel):
    rprs_mrkt_kor_name: str = Field(title="대표시장한글명")
    stck_shrn_iscd: str = Field(title="주식단축종목코드")
    hts_kor_isnm: str = Field(title="HTS한글종목명")
    stck_prpr: str = Field(title="주식현재가")
    prdy_vrss_sign: str = Field(title="전일대비부호")
    prdy_vrss: str = Field(title="전일대비")
    prdy_ctrt: str = Field(title="전일대비율")
    acml_vol: str = Field(title="누적거래량")
    prdy_vol: str = Field(title="전일거래량")
    wghn_avrg_stck_prc: str = Field(title="가중평균주식가격")
    lstn_stcn: str = Field(title="상장주수")


class ResistanceLevelTradingWeightItem2(BaseModel):
    data_rank: str = Field(title="데이터순위")
    stck_prpr: str = Field(title="주식현재가")
    cntg_vol: str = Field(title="체결거래량")
    acml_vol_rlim: str = Field(title="누적거래량비중")


class ResistanceLevelTradingWeight(BaseModel, KisHttpBody):
    """국내주식 매물대/거래비중"""

    output1: ResistanceLevelTradingWeightItem1 = Field(title="응답상세1")
    output2: Sequence[ResistanceLevelTradingWeightItem2] = Field(default_factory=list)
