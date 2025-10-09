from typing import Literal, Optional, Sequence

from pydantic import BaseModel, Field

from cluefin_openapi.kis._model import KisHttpBody


class ConditionSearchListItem(BaseModel):
    user_id: str = Field(title="HTS ID", description="", max_length=40)
    seq: str = Field(
        title="조건키값", description="해당 값을 종목조건검색조회 API의 input으로 사용 (0번부터 시작)", max_length=10
    )
    grp_nm: str = Field(
        title="그룹명",
        description='HTS(eFriend Plus) [0110] "사용자조건검색"화면을 통해 등록한 사용자조건 그룹',
        max_length=40,
    )
    condition_nm: str = Field(title="조건명", description="등록한 사용자 조건명", max_length=40)


class ConditionSearchList(BaseModel, KisHttpBody):
    """종목조건검색 목록조회"""

    output2: Sequence[ConditionSearchListItem] = Field(default_factory=list)


class ConditionSearchResultItem(BaseModel):
    code: str = Field(title="종목코드", max_length=6)
    name: str = Field(title="종목명", max_length=20)
    daebi: str = Field(title="전일대비부호", description="1. 상한 2. 상승 3. 보합 4. 하한 5. 하락", max_length=1)
    price: str = Field(title="현재가", max_length=16)
    chgrate: str = Field(title="등락율", max_length=16)
    acml_vol: str = Field(title="거래량", max_length=16)
    trade_amt: str = Field(title="거래대금", max_length=16)
    change: str = Field(title="전일대비", max_length=16)
    cttr: str = Field(title="체결강도", max_length=16)
    open: str = Field(title="시가", max_length=16)
    high: str = Field(title="고가", max_length=16)
    low: str = Field(title="저가", max_length=16)
    high52: str = Field(title="52주최고가", max_length=16)
    low52: str = Field(title="52주최저가", max_length=16)
    expprice: str = Field(title="예상체결가", max_length=16)
    expchange: str = Field(title="예상대비", max_length=16)
    expchggrate: str = Field(title="예상등락률", max_length=16)
    expcvol: str = Field(title="예상체결수량", max_length=16)
    chgrate2: str = Field(title="전일거래량대비율", max_length=16)
    expdaebi: str = Field(title="예상대비부호", max_length=1)
    recprice: str = Field(title="기준가", max_length=16)
    uplmtprice: str = Field(title="상한가", max_length=16)
    dnlmtprice: str = Field(title="하한가", max_length=16)
    stotprice: str = Field(title="시가총액", max_length=16)


class ConditionSearchResult(BaseModel, KisHttpBody):
    """종목조건검색조회"""

    output2: Sequence[ConditionSearchResultItem] = Field(default_factory=list)


class WatchlistGroupsItem(BaseModel):
    date: str = Field(title="일자", max_length=8)
    trnm_hour: str = Field(title="전송 시간", max_length=6)
    data_rank: str = Field(title="데이터 순위", max_length=10)
    inter_grp_code: str = Field(title="관심 그룹 코드", max_length=3)
    inter_grp_name: str = Field(title="관심 그룹 명", max_length=40)
    ask_cnt: str = Field(title="요청 개수", max_length=4)


class WatchlistGroups(BaseModel, KisHttpBody):
    """관심종목 그룹조회"""

    # TODO(typo): 문서에는 object로 되어있으나, 실제로는 list
    output2: Sequence[WatchlistGroupsItem] = Field(default_factory=list)


class WatchlistMultiQuoteItem(BaseModel):
    kospi_kosdaq_cls_name: str = Field(title="코스피 코스닥 구분 명", max_length=10)
    mrkt_trtm_cls_name: str = Field(title="시장 조치 구분 명", max_length=10)
    hour_cls_code: str = Field(title="시간 구분 코드", max_length=1)
    inter_shrn_iscd: str = Field(title="관심 단축 종목코드", max_length=16)
    inter_kor_isnm: str = Field(title="관심 한글 종목명", max_length=40)
    inter2_prpr: str = Field(title="관심2 현재가", max_length=11)
    inter2_prdy_vrss: str = Field(title="관심2 전일 대비", max_length=11)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    inter2_oprc: str = Field(title="관심2 시가", max_length=11)
    inter2_hgpr: str = Field(title="관심2 고가", max_length=11)
    inter2_lwpr: str = Field(title="관심2 저가", max_length=11)
    inter2_llam: str = Field(title="관심2 하한가", max_length=11)
    inter2_mxpr: str = Field(title="관심2 상한가", max_length=11)
    inter2_askp: str = Field(title="관심2 매도호가", max_length=11)
    inter2_bidp: str = Field(title="관심2 매수호가", max_length=11)
    seln_rsqn: str = Field(title="매도 잔량", max_length=12)
    shnu_rsqn: str = Field(title="매수2 잔량", max_length=12)
    total_askp_rsqn: str = Field(title="총 매도호가 잔량", max_length=12)
    total_bidp_rsqn: str = Field(title="총 매수호가 잔량", max_length=12)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=18)
    inter2_prdy_clpr: str = Field(title="관심2 전일 종가", max_length=11)
    oprc_vrss_hgpr_rate: str = Field(title="시가 대비 최고가 비율", max_length=84)
    intr_antc_cntg_vrss: str = Field(title="관심 예상 체결 대비", max_length=11)
    intr_antc_cntg_vrss_sign: str = Field(title="관심 예상 체결 대비 부호", max_length=1)
    intr_antc_cntg_prdy_ctrt: str = Field(title="관심 예상 체결 전일 대비율", max_length=72)
    intr_antc_vol: str = Field(title="관심 예상 거래량", max_length=18)
    inter2_sdpr: str = Field(title="관심2 기준가", max_length=11)


class WatchlistMultiQuote(BaseModel, KisHttpBody):
    """관심종목(멀티종목) 시세조회"""

    # TODO(typo): 문서에는 object로 되어있으나, 실제로는 list
    output: Sequence[WatchlistMultiQuoteItem] = Field(default_factory=list)


class WatchlistStocksByGroupItem1(BaseModel):
    data_rank: str = Field(title="데이터 순위", max_length=10)
    inter_grp_name: str = Field(title="관심 그룹 명", max_length=40)


class WatchlistStocksByGroupItem2(BaseModel):
    fid_mrkt_cls_code: str = Field(title="FID 시장 구분 코드", max_length=2)
    data_rank: str = Field(title="데이터 순위", max_length=10)
    exch_code: str = Field(title="거래소코드", max_length=4)
    jong_code: str = Field(title="종목코드", max_length=16)
    color_code: str = Field(title="생상 코드", max_length=8)
    memo: Optional[str] = Field(title="메모", max_length=128)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    fxdt_ntby_qty: str = Field(title="기준일 순매수 수량", max_length=12)
    cntg_unpr: str = Field(title="체결단가", max_length=11)
    cntg_cls_code: str = Field(title="체결 구분 코드", max_length=1)


class WatchlistStocksByGroup(BaseModel, KisHttpBody):
    """관심종목 그룹별 종목조회"""

    output1: WatchlistStocksByGroupItem1 = Field(title="응답상세1")
    output2: Sequence[WatchlistStocksByGroupItem2] = Field(default_factory=list)


class InstitutionalForeignTradingAggregateItem(BaseModel):
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드", max_length=9)
    ntby_qty: str = Field(title="순매수 수량", max_length=18)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=8)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    frgn_ntby_qty: str = Field(title="외국인 순매수 수량", max_length=12)
    orgn_ntby_qty: str = Field(title="기관계 순매수 수량", max_length=18)
    ivtr_ntby_qty: str = Field(title="투자신탁 순매수 수량", max_length=12)
    bank_ntby_qty: str = Field(title="은행 순매수 수량", max_length=12)
    insu_ntby_qty: str = Field(title="보험 순매수 수량", max_length=12)
    mrbn_ntby_qty: str = Field(title="종금 순매수 수량", max_length=12)
    fund_ntby_qty: str = Field(title="기금 순매수 수량", max_length=12)
    etc_orgt_ntby_vol: str = Field(title="기타 단체 순매수 거래량", max_length=18)
    etc_corp_ntby_vol: str = Field(title="기타 법인 순매수 거래량", max_length=18)
    frgn_ntby_tr_pbmn: str = Field(title="외국인 순매수 거래 대금", max_length=18)
    orgn_ntby_tr_pbmn: str = Field(title="기관계 순매수 거래 대금", max_length=18)
    ivtr_ntby_tr_pbmn: str = Field(title="투자신탁 순매수 거래 대금", max_length=18)
    bank_ntby_tr_pbmn: str = Field(title="은행 순매수 거래 대금", max_length=18)
    insu_ntby_tr_pbmn: str = Field(title="보험 순매수 거래 대금", max_length=18)
    mrbn_ntby_tr_pbmn: str = Field(title="종금 순매수 거래 대금", max_length=18)
    fund_ntby_tr_pbmn: str = Field(title="기금 순매수 거래 대금", max_length=18)
    etc_orgt_ntby_tr_pbmn: str = Field(title="기타 단체 순매수 거래 대금", max_length=18)
    etc_corp_ntby_tr_pbmn: str = Field(title="기타 법인 순매수 거래 대금", max_length=18)


class InstitutionalForeignTradingAggregate(BaseModel, KisHttpBody):
    """국내기관_외국인 매매종목가집계"""

    output: InstitutionalForeignTradingAggregateItem = Field(title="응답상세")


class ForeignBrokerageTradingAggregateItem(BaseModel):
    stck_shrn_iscd: str = Field(title="주식단축종목코드", max_length=9)
    hts_kor_isnm: str = Field(title="HTS한글종목명", max_length=40)
    glob_ntsl_qty: str = Field(title="외국계순매도수량", max_length=12)
    stck_prpr: str = Field(title="주식현재가", max_length=10)
    prdy_vrss: str = Field(title="전일대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일대비부호", max_length=1)
    prdy_ctrt: str = Field(title="전일대비율", max_length=82)
    acml_vol: str = Field(title="누적거래량", max_length=18)
    glob_total_seln_qty: str = Field(title="외국계총매도수량", max_length=18)
    glob_total_shnu_qty: str = Field(title="외국계총매수2수량", max_length=18)


class ForeignBrokerageTradingAggregate(BaseModel, KisHttpBody):
    """외국계 매매종목 가집계"""

    output: Sequence[ForeignBrokerageTradingAggregateItem] = Field(default_factory=list)


class InvestorTradingTrendByStockDailyItem1(BaseModel):
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    prdy_vol: str = Field(title="전일 거래량", max_length=18)
    rprs_mrkt_kor_name: str = Field(title="대표 시장 한글 명", max_length=40)


class InvestorTradingTrendByStockDailyItem2(BaseModel):
    stck_bsop_date: str = Field(title="주식 영업 일자", max_length=8)
    stck_clpr: str = Field(title="주식 종가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=18)
    stck_oprc: str = Field(title="주식 시가2", max_length=10)
    stck_hgpr: str = Field(title="주식 최고가", max_length=10)
    stck_lwpr: str = Field(title="주식 최저가", max_length=10)
    frgn_ntby_qty: str = Field(title="외국인 순매수 수량", max_length=12)
    frgn_reg_ntby_qty: str = Field(title="외국인 등록 순매수 수량", max_length=18)
    frgn_nreg_ntby_qty: str = Field(title="외국인 비등록 순매수 수량", max_length=18)
    prsn_ntby_qty: str = Field(title="개인 순매수 수량", max_length=12)
    orgn_ntby_qty: str = Field(title="기관계 순매수 수량", max_length=18)
    scrt_ntby_qty: str = Field(title="증권 순매수 수량", max_length=12)
    ivtr_ntby_qty: str = Field(title="투자신탁 순매수 수량", max_length=12)
    pe_fund_ntby_vol: str = Field(title="사모 펀드 순매수 거래량", max_length=18)
    bank_ntby_qty: str = Field(title="은행 순매수 수량", max_length=12)
    insu_ntby_qty: str = Field(title="보험 순매수 수량", max_length=12)
    mrbn_ntby_qty: str = Field(title="종금 순매수 수량", max_length=12)
    fund_ntby_qty: str = Field(title="기금 순매수 수량", max_length=12)
    etc_ntby_qty: str = Field(title="기타 순매수 수량", max_length=12)
    etc_corp_ntby_vol: str = Field(title="기타 법인 순매수 거래량", max_length=18)
    etc_orgt_ntby_vol: str = Field(title="기타 단체 순매수 거래량", max_length=18)
    frgn_reg_ntby_pbmn: str = Field(title="외국인 등록 순매수 대금", max_length=18)
    frgn_ntby_tr_pbmn: str = Field(title="외국인 순매수 거래 대금", max_length=18)
    frgn_nreg_ntby_pbmn: str = Field(title="외국인 비등록 순매수 대금", max_length=18)
    prsn_ntby_tr_pbmn: str = Field(title="개인 순매수 거래 대금", max_length=18)
    orgn_ntby_tr_pbmn: str = Field(title="기관계 순매수 거래 대금", max_length=18)
    scrt_ntby_tr_pbmn: str = Field(title="증권 순매수 거래 대금", max_length=18)
    pe_fund_ntby_tr_pbmn: str = Field(title="사모 펀드 순매수 거래 대금", max_length=18)
    ivtr_ntby_tr_pbmn: str = Field(title="투자신탁 순매수 거래 대금", max_length=18)
    bank_ntby_tr_pbmn: str = Field(title="은행 순매수 거래 대금", max_length=18)
    insu_ntby_tr_pbmn: str = Field(title="보험 순매수 거래 대금", max_length=18)
    mrbn_ntby_tr_pbmn: str = Field(title="종금 순매수 거래 대금", max_length=18)
    fund_ntby_tr_pbmn: str = Field(title="기금 순매수 거래 대금", max_length=18)
    etc_ntby_tr_pbmn: str = Field(title="기타 순매수 거래 대금", max_length=18)
    etc_corp_ntby_tr_pbmn: str = Field(title="기타 법인 순매수 거래 대금", max_length=18)
    etc_orgt_ntby_tr_pbmn: str = Field(title="기타 단체 순매수 거래 대금", max_length=18)
    frgn_seln_vol: str = Field(title="외국인 매도 거래량", max_length=18)
    frgn_shnu_vol: str = Field(title="외국인 매수2 거래량", max_length=18)
    frgn_seln_tr_pbmn: str = Field(title="외국인 매도 거래 대금", max_length=18)
    frgn_shnu_tr_pbmn: str = Field(title="외국인 매수2 거래 대금", max_length=18)
    frgn_reg_askp_qty: str = Field(title="외국인 등록 매도 수량", max_length=18)
    frgn_reg_bidp_qty: str = Field(title="외국인 등록 매수 수량", max_length=18)
    frgn_reg_askp_pbmn: str = Field(title="외국인 등록 매도 대금", max_length=18)
    frgn_reg_bidp_pbmn: str = Field(title="외국인 등록 매수 대금", max_length=18)
    frgn_nreg_askp_qty: str = Field(title="외국인 비등록 매도 수량", max_length=18)
    frgn_nreg_bidp_qty: str = Field(title="외국인 비등록 매수 수량", max_length=18)
    frgn_nreg_askp_pbmn: str = Field(title="외국인 비등록 매도 대금", max_length=18)
    frgn_nreg_bidp_pbmn: str = Field(title="외국인 비등록 매수 대금", max_length=18)
    prsn_seln_vol: str = Field(title="개인 매도 거래량", max_length=18)
    prsn_shnu_vol: str = Field(title="개인 매수2 거래량", max_length=18)
    prsn_seln_tr_pbmn: str = Field(title="개인 매도 거래 대금", max_length=18)
    prsn_shnu_tr_pbmn: str = Field(title="개인 매수2 거래 대금", max_length=18)
    orgn_seln_vol: str = Field(title="기관계 매도 거래량", max_length=18)
    orgn_shnu_vol: str = Field(title="기관계 매수2 거래량", max_length=18)
    orgn_seln_tr_pbmn: str = Field(title="기관계 매도 거래 대금", max_length=18)
    orgn_shnu_tr_pbmn: str = Field(title="기관계 매수2 거래 대금", max_length=18)
    scrt_seln_vol: str = Field(title="증권 매도 거래량", max_length=18)
    scrt_shnu_vol: str = Field(title="증권 매수2 거래량", max_length=18)
    scrt_seln_tr_pbmn: str = Field(title="증권 매도 거래 대금", max_length=18)
    scrt_shnu_tr_pbmn: str = Field(title="증권 매수2 거래 대금", max_length=18)
    ivtr_seln_vol: str = Field(title="투자신탁 매도 거래량", max_length=18)
    ivtr_shnu_vol: str = Field(title="투자신탁 매수2 거래량", max_length=18)
    ivtr_seln_tr_pbmn: str = Field(title="투자신탁 매도 거래 대금", max_length=18)
    ivtr_shnu_tr_pbmn: str = Field(title="투자신탁 매수2 거래 대금", max_length=18)
    pe_fund_seln_tr_pbmn: str = Field(title="사모 펀드 매도 거래 대금", max_length=18)
    pe_fund_seln_vol: str = Field(title="사모 펀드 매도 거래량", max_length=18)
    pe_fund_shnu_tr_pbmn: str = Field(title="사모 펀드 매수2 거래 대금", max_length=18)
    pe_fund_shnu_vol: str = Field(title="사모 펀드 매수2 거래량", max_length=18)
    bank_seln_vol: str = Field(title="은행 매도 거래량", max_length=18)
    bank_shnu_vol: str = Field(title="은행 매수2 거래량", max_length=18)
    bank_seln_tr_pbmn: str = Field(title="은행 매도 거래 대금", max_length=18)
    bank_shnu_tr_pbmn: str = Field(title="은행 매수2 거래 대금", max_length=18)
    insu_seln_vol: str = Field(title="보험 매도 거래량", max_length=18)
    insu_shnu_vol: str = Field(title="보험 매수2 거래량", max_length=18)
    insu_seln_tr_pbmn: str = Field(title="보험 매도 거래 대금", max_length=18)
    insu_shnu_tr_pbmn: str = Field(title="보험 매수2 거래 대금", max_length=18)
    mrbn_seln_vol: str = Field(title="종금 매도 거래량", max_length=18)
    mrbn_shnu_vol: str = Field(title="종금 매수2 거래량", max_length=18)
    mrbn_seln_tr_pbmn: str = Field(title="종금 매도 거래 대금", max_length=18)
    mrbn_shnu_tr_pbmn: str = Field(title="종금 매수2 거래 대금", max_length=18)
    fund_seln_vol: str = Field(title="기금 매도 거래량", max_length=18)
    fund_shnu_vol: str = Field(title="기금 매수2 거래량", max_length=18)
    fund_seln_tr_pbmn: str = Field(title="기금 매도 거래 대금", max_length=18)
    fund_shnu_tr_pbmn: str = Field(title="기금 매수2 거래 대금", max_length=18)
    etc_seln_vol: str = Field(title="기타 매도 거래량", max_length=18)
    etc_shnu_vol: str = Field(title="기타 매수2 거래량", max_length=18)
    etc_seln_tr_pbmn: str = Field(title="기타 매도 거래 대금", max_length=18)
    etc_shnu_tr_pbmn: str = Field(title="기타 매수2 거래 대금", max_length=18)
    etc_orgt_seln_vol: str = Field(title="기타 단체 매도 거래량", max_length=18)
    etc_orgt_shnu_vol: str = Field(title="기타 단체 매수2 거래량", max_length=18)
    etc_orgt_seln_tr_pbmn: str = Field(title="기타 단체 매도 거래 대금", max_length=18)
    etc_orgt_shnu_tr_pbmn: str = Field(title="기타 단체 매수2 거래 대금", max_length=18)
    etc_corp_seln_vol: str = Field(title="기타 법인 매도 거래량", max_length=18)
    etc_corp_shnu_vol: str = Field(title="기타 법인 매수2 거래량", max_length=18)
    etc_corp_seln_tr_pbmn: str = Field(title="기타 법인 매도 거래 대금", max_length=18)
    etc_corp_shnu_tr_pbmn: str = Field(title="기타 법인 매수2 거래 대금", max_length=18)
    bold_yn: str = Field(title="BOLD 여부", max_length=18)


class InvestorTradingTrendByStockDaily(BaseModel, KisHttpBody):
    """종목별 투자자매매동향(일별)"""

    output1: InvestorTradingTrendByStockDailyItem1 = Field(title="응답상세1")
    output2: Sequence[InvestorTradingTrendByStockDailyItem2] = Field(default_factory=list)


class InvestorTradingTrendByMarketIntradayItem(BaseModel):
    frgn_seln_vol: str = Field(title="외국인 매도 거래량", max_length=18)
    frgn_shnu_vol: str = Field(title="외국인 매수 거래량", max_length=18)
    frgn_ntby_qty: str = Field(title="외국인 순매수 수량", max_length=12)
    frgn_seln_tr_pbmn: str = Field(title="외국인 매도 거래 대금", max_length=18)
    frgn_shnu_tr_pbmn: str = Field(title="외국인 매수 거래 대금", max_length=18)
    frgn_ntby_tr_pbmn: str = Field(title="외국인 순매수 거래 대금", max_length=18)
    prsn_seln_vol: str = Field(title="개인 매도 거래량", max_length=18)
    prsn_shnu_vol: str = Field(title="개인 매수 거래량", max_length=18)
    prsn_ntby_qty: str = Field(title="개인 순매수 수량", max_length=12)
    prsn_seln_tr_pbmn: str = Field(title="개인 매도 거래 대금", max_length=18)
    prsn_shnu_tr_pbmn: str = Field(title="개인 매수 거래 대금", max_length=18)
    prsn_ntby_tr_pbmn: str = Field(title="개인 순매수 거래 대금", max_length=18)
    orgn_seln_vol: str = Field(title="기관계 매도 거래량", max_length=18)
    orgn_shnu_vol: str = Field(title="기관계 매수 거래량", max_length=18)
    orgn_ntby_qty: str = Field(title="기관계 순매수 수량", max_length=18)
    orgn_seln_tr_pbmn: str = Field(title="기관계 매도 거래 대금", max_length=18)
    orgn_shnu_tr_pbmn: str = Field(title="기관계 매수 거래 대금", max_length=18)
    orgn_ntby_tr_pbmn: str = Field(title="기관계 순매수 거래 대금", max_length=18)
    scrt_seln_vol: str = Field(title="증권 매도 거래량", max_length=18)
    scrt_shnu_vol: str = Field(title="증권 매수 거래량", max_length=18)
    scrt_ntby_qty: str = Field(title="증권 순매수 수량", max_length=12)
    scrt_seln_tr_pbmn: str = Field(title="증권 매도 거래 대금", max_length=18)
    scrt_shnu_tr_pbmn: str = Field(title="증권 매수 거래 대금", max_length=18)
    scrt_ntby_tr_pbmn: str = Field(title="증권 순매수 거래 대금", max_length=18)
    ivtr_seln_vol: str = Field(title="투자신탁 매도 거래량", max_length=18)
    ivtr_shnu_vol: str = Field(title="투자신탁 매수 거래량", max_length=18)
    ivtr_ntby_qty: str = Field(title="투자신탁 순매수 수량", max_length=12)
    ivtr_seln_tr_pbmn: str = Field(title="투자신탁 매도 거래 대금", max_length=18)
    ivtr_shnu_tr_pbmn: str = Field(title="투자신탁 매수 거래 대금", max_length=18)
    ivtr_ntby_tr_pbmn: str = Field(title="투자신탁 순매수 거래 대금", max_length=18)
    pe_fund_seln_tr_pbmn: str = Field(title="사모 펀드 매도 거래 대금", max_length=18)
    pe_fund_seln_vol: str = Field(title="사모 펀드 매도 거래량", max_length=18)
    pe_fund_ntby_vol: str = Field(title="사모 펀드 순매수 거래량", max_length=18)
    pe_fund_shnu_tr_pbmn: str = Field(title="사모 펀드 매수 거래 대금", max_length=18)
    pe_fund_shnu_vol: str = Field(title="사모 펀드 매수 거래량", max_length=18)
    pe_fund_ntby_tr_pbmn: str = Field(title="사모 펀드 순매수 거래 대금", max_length=18)
    bank_seln_vol: str = Field(title="은행 매도 거래량", max_length=18)
    bank_shnu_vol: str = Field(title="은행 매수 거래량", max_length=18)
    bank_ntby_qty: str = Field(title="은행 순매수 수량", max_length=12)
    bank_seln_tr_pbmn: str = Field(title="은행 매도 거래 대금", max_length=18)
    bank_shnu_tr_pbmn: str = Field(title="은행 매수 거래 대금", max_length=18)
    bank_ntby_tr_pbmn: str = Field(title="은행 순매수 거래 대금", max_length=18)
    insu_seln_vol: str = Field(title="보험 매도 거래량", max_length=18)
    insu_shnu_vol: str = Field(title="보험 매수 거래량", max_length=18)
    insu_ntby_qty: str = Field(title="보험 순매수 수량", max_length=12)
    insu_seln_tr_pbmn: str = Field(title="보험 매도 거래 대금", max_length=18)
    insu_shnu_tr_pbmn: str = Field(title="보험 매수 거래 대금", max_length=18)
    insu_ntby_tr_pbmn: str = Field(title="보험 순매수 거래 대금", max_length=18)
    mrbn_seln_vol: str = Field(title="종금 매도 거래량", max_length=18)
    mrbn_shnu_vol: str = Field(title="종금 매수 거래량", max_length=18)
    mrbn_ntby_qty: str = Field(title="종금 순매수 수량", max_length=12)
    mrbn_seln_tr_pbmn: str = Field(title="종금 매도 거래 대금", max_length=18)
    mrbn_shnu_tr_pbmn: str = Field(title="종금 매수 거래 대금", max_length=18)
    mrbn_ntby_tr_pbmn: str = Field(title="종금 순매수 거래 대금", max_length=18)
    fund_seln_vol: str = Field(title="기금 매도 거래량", max_length=18)
    fund_shnu_vol: str = Field(title="기금 매수 거래량", max_length=18)
    fund_ntby_qty: str = Field(title="기금 순매수 수량", max_length=12)
    fund_seln_tr_pbmn: str = Field(title="기금 매도 거래 대금", max_length=18)
    fund_shnu_tr_pbmn: str = Field(title="기금 매수 거래 대금", max_length=18)
    fund_ntby_tr_pbmn: str = Field(title="기금 순매수 거래 대금", max_length=18)
    etc_orgt_seln_vol: str = Field(title="기타 단체 매도 거래량", max_length=18)
    etc_orgt_shnu_vol: str = Field(title="기타 단체 매수 거래량", max_length=18)
    etc_orgt_ntby_vol: str = Field(title="기타 단체 순매수 거래량", max_length=18)
    etc_orgt_seln_tr_pbmn: str = Field(title="기타 단체 매도 거래 대금", max_length=18)
    etc_orgt_shnu_tr_pbmn: str = Field(title="기타 단체 매수 거래 대금", max_length=18)
    etc_orgt_ntby_tr_pbmn: str = Field(title="기타 단체 순매수 거래 대금", max_length=18)
    etc_corp_seln_vol: str = Field(title="기타 법인 매도 거래량", max_length=18)
    etc_corp_shnu_vol: str = Field(title="기타 법인 매수 거래량", max_length=18)
    etc_corp_ntby_vol: str = Field(title="기타 법인 순매수 거래량", max_length=18)
    etc_corp_seln_tr_pbmn: str = Field(title="기타 법인 매도 거래 대금", max_length=18)
    etc_corp_shnu_tr_pbmn: str = Field(title="기타 법인 매수 거래 대금", max_length=18)
    etc_corp_ntby_tr_pbmn: str = Field(title="기타 법인 순매수 거래 대금", max_length=18)


class InvestorTradingTrendByMarketIntraday(BaseModel, KisHttpBody):
    """시장별 투자자매매동향(시세)"""

    output: Sequence[InvestorTradingTrendByMarketIntradayItem] = Field(default_factory=list)


class InvestorTradingTrendByMarketDailyItem1(BaseModel):
    stck_bsop_date: str = Field(title="주식 영업 일자", max_length=8)
    bstp_nmix_prpr: str = Field(title="업종 지수 현재가", max_length=112)
    bstp_nmix_prdy_vrss: str = Field(title="업종 지수 전일 대비", max_length=112)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    bstp_nmix_prdy_ctrt: str = Field(title="업종 지수 전일 대비율", max_length=82)
    bstp_nmix_oprc: str = Field(title="업종 지수 시가2", max_length=112)
    bstp_nmix_hgpr: str = Field(title="업종 지수 최고가", max_length=112)
    bstp_nmix_lwpr: str = Field(title="업종 지수 최저가", max_length=112)
    stck_prdy_clpr: str = Field(title="주식 전일 종가", max_length=10)
    frgn_ntby_qty: str = Field(title="외국인 순매수 수량", max_length=12)
    frgn_reg_ntby_qty: str = Field(title="외국인 등록 순매수 수량", max_length=18)
    frgn_nreg_ntby_qty: str = Field(title="외국인 비등록 순매수 수량", max_length=18)
    prsn_ntby_qty: str = Field(title="개인 순매수 수량", max_length=12)
    orgn_ntby_qty: str = Field(title="기관계 순매수 수량", max_length=18)
    scrt_ntby_qty: str = Field(title="증권 순매수 수량", max_length=12)
    ivtr_ntby_qty: str = Field(title="투자신탁 순매수 수량", max_length=12)
    pe_fund_ntby_vol: str = Field(title="사모 펀드 순매수 거래량", max_length=18)
    bank_ntby_qty: str = Field(title="은행 순매수 수량", max_length=12)
    insu_ntby_qty: str = Field(title="보험 순매수 수량", max_length=12)
    mrbn_ntby_qty: str = Field(title="종금 순매수 수량", max_length=12)
    fund_ntby_qty: str = Field(title="기금 순매수 수량", max_length=12)
    etc_ntby_qty: str = Field(title="기타 순매수 수량", max_length=12)
    etc_orgt_ntby_vol: str = Field(title="기타 단체 순매수 거래량", max_length=18)
    etc_corp_ntby_vol: str = Field(title="기타 법인 순매수 거래량", max_length=18)
    frgn_ntby_tr_pbmn: str = Field(title="외국인 순매수 거래 대금", max_length=18)
    frgn_reg_ntby_pbmn: str = Field(title="외국인 등록 순매수 대금", max_length=18)
    frgn_nreg_ntby_pbmn: str = Field(title="외국인 비등록 순매수 대금", max_length=18)
    prsn_ntby_tr_pbmn: str = Field(title="개인 순매수 거래 대금", max_length=18)
    orgn_ntby_tr_pbmn: str = Field(title="기관계 순매수 거래 대금", max_length=18)
    scrt_ntby_tr_pbmn: str = Field(title="증권 순매수 거래 대금", max_length=18)
    ivtr_ntby_tr_pbmn: str = Field(title="투자신탁 순매수 거래 대금", max_length=18)
    pe_fund_ntby_tr_pbmn: str = Field(title="사모 펀드 순매수 거래 대금", max_length=18)
    bank_ntby_tr_pbmn: str = Field(title="은행 순매수 거래 대금", max_length=18)
    insu_ntby_tr_pbmn: str = Field(title="보험 순매수 거래 대금", max_length=18)
    mrbn_ntby_tr_pbmn: str = Field(title="종금 순매수 거래 대금", max_length=18)
    fund_ntby_tr_pbmn: str = Field(title="기금 순매수 거래 대금", max_length=18)
    etc_ntby_tr_pbmn: str = Field(title="기타 순매수 거래 대금", max_length=18)
    etc_orgt_ntby_tr_pbmn: str = Field(title="기타 단체 순매수 거래 대금", max_length=18)
    etc_corp_ntby_tr_pbmn: str = Field(title="기타 법인 순매수 거래 대금", max_length=18)


class InvestorTradingTrendByMarketDaily(BaseModel, KisHttpBody):
    """시장별 투자자매매동향(일별)"""

    output: Sequence[InvestorTradingTrendByMarketDailyItem1] = Field(default_factory=list)


class ForeignNetBuyTrendByStockItem1(BaseModel):
    total_seln_qty: str = Field(title="총매도수량", max_length=18)
    total_shnu_qty: str = Field(title="총매수2수량", max_length=18)


class ForeignNetBuyTrendByStockItem2(BaseModel):
    bsop_hour: str = Field(title="영업시간", max_length=6)
    mbcr_name: str = Field(title="회원사명", max_length=50)
    hts_kor_isnm: str = Field(title="HTS한글종목명", max_length=40)
    stck_prpr: str = Field(title="주식현재가", max_length=10)
    prdy_vrss: str = Field(title="전일대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일대비부호", max_length=1)
    cntg_vol: str = Field(title="체결거래량", max_length=18)
    acml_ntby_qty: str = Field(title="누적순매수수량", max_length=18)
    glob_ntby_qty: str = Field(title="외국계순매수수량", max_length=12)
    frgn_ntby_qty_icdc: str = Field(title="외국인순매수수량증감", max_length=10)


class ForeignNetBuyTrendByStock(BaseModel, KisHttpBody):
    """종목별 외국계 순매수추이"""

    output1: Sequence[ForeignNetBuyTrendByStockItem1] = Field(default_factory=list)
    output2: Sequence[ForeignNetBuyTrendByStockItem2] = Field(default_factory=list)


class MemberTradingTrendTickItem(BaseModel):
    stck_bsop_date: str = Field(title="주식영업일자", max_length=8)
    total_seln_qty: str = Field(title="총매도수량", max_length=18)
    total_shnu_qty: str = Field(title="총매수2수량", max_length=18)
    ntby_qty: str = Field(title="순매수수량", max_length=18)
    stck_prpr: str = Field(title="주식현재가", max_length=10)
    prdy_vrss: str = Field(title="전일대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일대비부호", max_length=1)
    prdy_ctrt: str = Field(title="전일대비율", max_length=82)
    acml_vol: str = Field(title="누적거래량", max_length=18)


class MemberTradingTrendTick(BaseModel, KisHttpBody):
    """회원사 실시간 매매동향(틱)"""

    output: Sequence[MemberTradingTrendTickItem] = Field(default_factory=list)


class MemberTradingTrendByStockItem(BaseModel):
    stck_bsop_date: str = Field(title="주식영업일자", max_length=8)
    total_seln_qty: str = Field(title="총매도수량", max_length=18)
    total_shnu_qty: str = Field(title="총매수2수량", max_length=18)
    ntby_qty: str = Field(title="순매수수량", max_length=18)
    stck_prpr: str = Field(title="주식현재가", max_length=10)
    prdy_vrss: str = Field(title="전일대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일대비부호", max_length=1)
    prdy_ctrt: str = Field(title="전일대비율", max_length=82)
    acml_vol: str = Field(title="누적거래량", max_length=18)


class MemberTradingTrendByStock(BaseModel, KisHttpBody):
    """주식현재가 회원사 종목매매동향"""

    output: Sequence[MemberTradingTrendByStockItem] = Field(default_factory=list)


class ProgramTradingTrendByStockIntradayItem(BaseModel):
    bsop_hour: str = Field(title="영업 시간", max_length=6)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    whol_smtn_seln_vol: str = Field(title="전체 합계 매도 거래량", max_length=18)
    whol_smtn_shnu_vol: str = Field(title="전체 합계 매수2 거래량", max_length=18)
    whol_smtn_ntby_qty: str = Field(title="전체 합계 순매수 수량", max_length=18)
    whol_smtn_seln_tr_pbmn: str = Field(title="전체 합계 매도 거래 대금", max_length=18)
    whol_smtn_shnu_tr_pbmn: str = Field(title="전체 합계 매수2 거래 대금", max_length=18)
    whol_smtn_ntby_tr_pbmn: str = Field(title="전체 합계 순매수 거래 대금", max_length=18)
    whol_ntby_vol_icdc: str = Field(title="전체 순매수 거래량 증감", max_length=18)
    whol_ntby_tr_pbmn_icdc: str = Field(title="전체 순매수 거래 대금 증감", max_length=18)


class ProgramTradingTrendByStockIntraday(BaseModel, KisHttpBody):
    """종목별 프로그램매매추이(체결)"""

    output: Sequence[ProgramTradingTrendByStockIntradayItem] = Field(default_factory=list)


class ProgramTradingTrendByStockDailyItem(BaseModel):
    stck_bsop_date: str = Field(title="주식 영업 일자", max_length=8)
    stck_clpr: str = Field(title="주식 종가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=18)
    whol_smtn_seln_vol: str = Field(title="전체 합계 매도 거래량", max_length=18)
    whol_smtn_shnu_vol: str = Field(title="전체 합계 매수2 거래량", max_length=18)
    whol_smtn_ntby_qty: str = Field(title="전체 합계 순매수 수량", max_length=18)
    whol_smtn_seln_tr_pbmn: str = Field(title="전체 합계 매도 거래 대금", max_length=18)
    whol_smtn_shnu_tr_pbmn: str = Field(title="전체 합계 매수2 거래 대금", max_length=18)
    whol_smtn_ntby_tr_pbmn: str = Field(title="전체 합계 순매수 거래 대금", max_length=18)
    whol_ntby_vol_icdc: str = Field(title="전체 순매수 거래량 증감", max_length=10)
    whol_ntby_tr_pbmn_icdc2: str = Field(title="전체 순매수 거래 대금 증감2", max_length=18)


class ProgramTradingTrendByStockDaily(BaseModel, KisHttpBody):
    """종목별 프로그램매매추이(일별)"""

    output: Sequence[ProgramTradingTrendByStockDailyItem] = Field(default_factory=list)


class ForeignInstitutionalEstimateByStockItem(BaseModel):
    bsop_hour_gb: str = Field(
        title="입력구분",
        description="1: 09시 30분 입력\n2: 10시 00분 입력\n3: 11시 20분 입력\n4: 13시 20분 입력\n5: 14시 30분 입력",
        max_length=1,
    )
    frgn_fake_ntby_qty: str = Field(title="외국인수량(가집계)", max_length=18)
    orgn_fake_ntby_qty: str = Field(title="기관수량(가집계)", max_length=18)
    sum_fake_ntby_qty: str = Field(title="합산수량(가집계)", max_length=18)


class ForeignInstitutionalEstimateByStock(BaseModel, KisHttpBody):
    """종목별 외인기관 추정기전계"""

    output2: Sequence[ForeignInstitutionalEstimateByStockItem] = Field(default_factory=list)


class BuySellVolumeByStockDailyItem1(BaseModel):
    shnu_cnqn_smtn: str = Field(title="매수 체결량 합계", max_length=18)
    seln_cnqn_smtn: str = Field(title="매도 체결량 합계", max_length=18)


class BuySellVolumeByStockDailyItem2(BaseModel):
    stck_bsop_date: str = Field(title="거래상태정보", max_length=8)
    total_seln_qty: str = Field(title="총 매도 수량", max_length=18)
    total_shnu_qty: str = Field(title="총 매수 수량", max_length=18)


class BuySellVolumeByStockDaily(BaseModel, KisHttpBody):
    """종목별일별매수매도체결량"""

    output1: BuySellVolumeByStockDailyItem1 = Field(title="응답상세1")
    output2: Sequence[BuySellVolumeByStockDailyItem2] = Field(default_factory=list)


class ProgramTradingSummaryIntradayItem(BaseModel):
    bsop_hour: str = Field(title="영업 시간", max_length=6)
    arbt_smtn_seln_tr_pbmn: str = Field(title="차익 합계 매도 거래 대금", max_length=18)
    arbt_smtm_seln_tr_pbmn_rate: str = Field(title="차익 합계 매도 거래대금 비율", max_length=72)
    arbt_smtn_shnu_tr_pbmn: str = Field(title="차익 합계 매수2 거래 대금", max_length=18)
    arbt_smtm_shun_tr_pbmn_rate: str = Field(title="차익합계매수거래대금비율", max_length=72)
    nabt_smtn_seln_tr_pbmn: str = Field(title="비차익 합계 매도 거래 대금", max_length=18)
    nabt_smtm_seln_tr_pbmn_rate: str = Field(title="비차익 합계 매도 거래대금 비율", max_length=72)
    nabt_smtn_shnu_tr_pbmn: str = Field(title="비차익 합계 매수2 거래 대금", max_length=18)
    nabt_smtm_shun_tr_pbmn_rate: str = Field(title="비차익합계매수거래대금비율", max_length=72)
    arbt_smtn_ntby_tr_pbmn: str = Field(title="차익 합계 순매수 거래 대금", max_length=18)
    arbt_smtm_ntby_tr_pbmn_rate: str = Field(title="차익 합계 순매수 거래대금 비율", max_length=72)
    nabt_smtn_ntby_tr_pbmn: str = Field(title="비차익 합계 순매수 거래 대금", max_length=18)
    nabt_smtm_ntby_tr_pbmn_rate: str = Field(title="비차익 합계 순매수 거래대금 비", max_length=72)
    whol_smtn_ntby_tr_pbmn: str = Field(title="전체 합계 순매수 거래 대금", max_length=18)
    whol_ntby_tr_pbmn_rate: str = Field(title="전체 순매수 거래대금 비율", max_length=72)
    bstp_nmix_prpr: str = Field(title="업종 지수 현재가", max_length=112)
    bstp_nmix_prdy_vrss: str = Field(title="업종 지수 전일 대비", max_length=112)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)


class ProgramTradingSummaryIntraday(BaseModel, KisHttpBody):
    """프로그램매매 종합현황(시간)"""

    output1: Sequence[ProgramTradingSummaryIntradayItem] = Field(default_factory=list)


class ProgramTradingSummaryDailyItem(BaseModel):
    stck_bsop_date: str = Field(title="주식 영업 일자", max_length=8)
    nabt_entm_seln_tr_pbmn: str = Field(title="비차익 위탁 매도 거래 대금", max_length=18)
    nabt_onsl_seln_vol: str = Field(title="비차익 자기 매도 거래량", max_length=18)
    whol_onsl_seln_tr_pbmn: str = Field(title="전체 자기 매도 거래 대금", max_length=18)
    arbt_smtn_shnu_vol: str = Field(title="차익 합계 매수2 거래량", max_length=18)
    nabt_smtn_shnu_tr_pbmn: str = Field(title="비차익 합계 매수2 거래 대금", max_length=18)
    arbt_entm_ntby_qty: str = Field(title="차익 위탁 순매수 수량", max_length=18)
    nabt_entm_ntby_tr_pbmn: str = Field(title="비차익 위탁 순매수 거래 대금", max_length=18)
    arbt_entm_seln_vol: str = Field(title="차익 위탁 매도 거래량", max_length=18)
    nabt_entm_seln_vol_rate: str = Field(title="비차익 위탁 매도 거래량 비율", max_length=82)
    nabt_onsl_seln_vol_rate: str = Field(title="비차익 자기 매도 거래량 비율", max_length=82)
    whol_onsl_seln_tr_pbmn_rate: str = Field(title="전체 자기 매도 거래 대금 비율", max_length=82)
    arbt_smtm_shun_vol_rate: str = Field(title="차익 합계 매수 거래량 비율", max_length=72)
    nabt_smtm_shun_tr_pbmn_rate: str = Field(title="비차익 합계 매수 거래대금 비율", max_length=72)
    arbt_entm_ntby_qty_rate: str = Field(title="차익 위탁 순매수 수량 비율", max_length=82)
    nabt_entm_ntby_tr_pbmn_rate: str = Field(title="비차익 위탁 순매수 거래 대금", max_length=82)
    arbt_entm_seln_vol_rate: str = Field(title="차익 위탁 매도 거래량 비율", max_length=82)
    nabt_entm_seln_tr_pbmn_rate: str = Field(title="비차익 위탁 매도 거래 대금 비", max_length=82)
    nabt_onsl_seln_tr_pbmn: str = Field(title="비차익 자기 매도 거래 대금", max_length=18)
    whol_smtn_seln_vol: str = Field(title="전체 합계 매도 거래량", max_length=18)
    arbt_smtn_shnu_tr_pbmn: str = Field(title="차익 합계 매수2 거래 대금", max_length=18)
    whol_entm_shnu_vol: str = Field(title="전체 위탁 매수2 거래량", max_length=18)
    arbt_entm_ntby_tr_pbmn: str = Field(title="차익 위탁 순매수 거래 대금", max_length=18)
    nabt_onsl_ntby_qty: str = Field(title="비차익 자기 순매수 수량", max_length=18)
    arbt_entm_seln_tr_pbmn: str = Field(title="차익 위탁 매도 거래 대금", max_length=18)
    nabt_onsl_seln_tr_pbmn_rate: str = Field(title="비차익 자기 매도 거래 대금 비", max_length=82)
    whol_seln_vol_rate: str = Field(title="전체 매도 거래량 비율", max_length=72)
    arbt_smtm_shun_tr_pbmn_rate: str = Field(title="차익 합계 매수 거래대금 비율", max_length=72)
    whol_entm_shnu_vol_rate: str = Field(title="전체 위탁 매수 거래량 비율", max_length=82)
    arbt_entm_ntby_tr_pbmn_rate: str = Field(title="차익 위탁 순매수 거래 대금 비", max_length=82)
    nabt_onsl_ntby_qty_rate: str = Field(title="비차익 자기 순매수 수량 비율", max_length=82)
    arbt_entm_seln_tr_pbmn_rate: str = Field(title="차익 위탁 매도 거래 대금 비율", max_length=82)
    nabt_smtn_seln_vol: str = Field(title="비차익 합계 매도 거래량", max_length=18)
    whol_smtn_seln_tr_pbmn: str = Field(title="전체 합계 매도 거래 대금", max_length=18)
    nabt_entm_shnu_vol: str = Field(title="비차익 위탁 매수2 거래량", max_length=18)
    whol_entm_shnu_tr_pbmn: str = Field(title="전체 위탁 매수2 거래 대금", max_length=18)
    arbt_onsl_ntby_qty: str = Field(title="차익 자기 순매수 수량", max_length=18)
    nabt_onsl_ntby_tr_pbmn: str = Field(title="비차익 자기 순매수 거래 대금", max_length=18)
    arbt_onsl_seln_tr_pbmn: str = Field(title="차익 자기 매도 거래 대금", max_length=18)
    nabt_smtm_seln_vol_rate: str = Field(title="비차익 합계 매도 거래량 비율", max_length=72)
    whol_seln_tr_pbmn_rate: str = Field(title="전체 매도 거래대금 비율", max_length=72)
    nabt_entm_shnu_vol_rate: str = Field(title="비차익 위탁 매수 거래량 비율", max_length=82)
    whol_entm_shnu_tr_pbmn_rate: str = Field(title="전체 위탁 매수 거래 대금 비율", max_length=82)
    arbt_onsl_ntby_qty_rate: str = Field(title="차익 자기 순매수 수량 비율", max_length=82)
    nabt_onsl_ntby_tr_pbmn_rate: str = Field(title="비차익 자기 순매수 거래 대금", max_length=82)
    arbt_onsl_seln_tr_pbmn_rate: str = Field(title="차익 자기 매도 거래 대금 비율", max_length=82)
    nabt_smtn_seln_tr_pbmn: str = Field(title="비차익 합계 매도 거래 대금", max_length=18)
    arbt_entm_shnu_vol: str = Field(title="차익 위탁 매수2 거래량", max_length=18)
    nabt_entm_shnu_tr_pbmn: str = Field(title="비차익 위탁 매수2 거래 대금", max_length=18)
    whol_onsl_shnu_vol: str = Field(title="전체 자기 매수2 거래량", max_length=18)
    arbt_onsl_ntby_tr_pbmn: str = Field(title="차익 자기 순매수 거래 대금", max_length=18)
    nabt_smtn_ntby_qty: str = Field(title="비차익 합계 순매수 수량", max_length=18)
    arbt_onsl_seln_vol: str = Field(title="차익 자기 매도 거래량", max_length=18)
    nabt_smtm_seln_tr_pbmn_rate: str = Field(title="비차익 합계 매도 거래대금 비율", max_length=72)
    arbt_entm_shnu_vol_rate: str = Field(title="차익 위탁 매수 거래량 비율", max_length=82)
    nabt_entm_shnu_tr_pbmn_rate: str = Field(title="비차익 위탁 매수 거래 대금 비", max_length=82)
    whol_onsl_shnu_tr_pbmn: str = Field(title="전체 자기 매수2 거래 대금", max_length=18)
    arbt_onsl_ntby_tr_pbmn_rate: str = Field(title="차익 자기 순매수 거래 대금 비", max_length=82)
    nabt_smtm_ntby_qty_rate: str = Field(title="비차익 합계 순매수 수량 비율", max_length=72)
    arbt_onsl_seln_vol_rate: str = Field(title="차익 자기 매도 거래량 비율", max_length=82)
    whol_entm_seln_vol: str = Field(title="전체 위탁 매도 거래량", max_length=18)
    arbt_entm_shnu_tr_pbmn: str = Field(title="차익 위탁 매수2 거래 대금", max_length=18)
    nabt_onsl_shnu_vol: str = Field(title="비차익 자기 매수2 거래량", max_length=18)
    whol_onsl_shnu_tr_pbmn_rate: str = Field(title="전체 자기 매수 거래 대금 비율", max_length=82)
    arbt_smtn_ntby_qty: str = Field(title="차익 합계 순매수 수량", max_length=18)
    nabt_smtn_ntby_tr_pbmn: str = Field(title="비차익 합계 순매수 거래 대금", max_length=18)
    arbt_smtn_seln_vol: str = Field(title="차익 합계 매도 거래량", max_length=18)
    whol_entm_seln_tr_pbmn: str = Field(title="전체 위탁 매도 거래 대금", max_length=18)
    arbt_entm_shnu_tr_pbmn_rate: str = Field(title="차익 위탁 매수 거래 대금 비율", max_length=82)
    nabt_onsl_shnu_vol_rate: str = Field(title="비차익 자기 매수 거래량 비율", max_length=82)
    whol_onsl_shnu_vol_rate: str = Field(title="전체 자기 매수 거래량 비율", max_length=82)
    arbt_smtm_ntby_qty_rate: str = Field(title="차익 합계 순매수 수량 비율", max_length=72)
    nabt_smtm_ntby_tr_pbmn_rate: str = Field(title="비차익 합계 순매수 거래대금 비", max_length=72)
    arbt_smtm_seln_vol_rate: str = Field(title="차익 합계 매도 거래량 비율", max_length=72)
    whol_entm_seln_vol_rate: str = Field(title="전체 위탁 매도 거래량 비율", max_length=82)
    arbt_onsl_shnu_vol: str = Field(title="차익 자기 매수2 거래량", max_length=18)
    nabt_onsl_shnu_tr_pbmn: str = Field(title="비차익 자기 매수2 거래 대금", max_length=18)
    whol_smtn_shnu_vol: str = Field(title="전체 합계 매수2 거래량", max_length=18)
    arbt_smtn_ntby_tr_pbmn: str = Field(title="차익 합계 순매수 거래 대금", max_length=18)
    whol_entm_ntby_qty: str = Field(title="전체 위탁 순매수 수량", max_length=18)
    arbt_smtn_seln_tr_pbmn: str = Field(title="차익 합계 매도 거래 대금", max_length=18)
    whol_entm_seln_tr_pbmn_rate: str = Field(title="전체 위탁 매도 거래 대금 비율", max_length=82)
    arbt_onsl_shnu_vol_rate: str = Field(title="차익 자기 매수 거래량 비율", max_length=82)
    nabt_onsl_shnu_tr_pbmn_rate: str = Field(title="비차익 자기 매수 거래 대금 비", max_length=82)
    whol_shun_vol_rate: str = Field(title="전체 매수 거래량 비율", max_length=72)
    arbt_smtm_ntby_tr_pbmn_rate: str = Field(title="차익 합계 순매수 거래대금 비율", max_length=72)
    whol_entm_ntby_qty_rate: str = Field(title="전체 위탁 순매수 수량 비율", max_length=82)
    arbt_smtm_seln_tr_pbmn_rate: str = Field(title="차익 합계 매도 거래대금 비율", max_length=72)
    whol_onsl_seln_vol: str = Field(title="전체 자기 매도 거래량", max_length=18)
    arbt_onsl_shnu_tr_pbmn: str = Field(title="차익 자기 매수2 거래 대금", max_length=18)
    nabt_smtn_shnu_vol: str = Field(title="비차익 합계 매수2 거래량", max_length=18)
    whol_smtn_shnu_tr_pbmn: str = Field(title="전체 합계 매수2 거래 대금", max_length=18)
    nabt_entm_ntby_qty: str = Field(title="비차익 위탁 순매수 수량", max_length=18)
    whol_entm_ntby_tr_pbmn: str = Field(title="전체 위탁 순매수 거래 대금", max_length=18)
    nabt_entm_seln_vol: str = Field(title="비차익 위탁 매도 거래량", max_length=18)
    whol_onsl_seln_vol_rate: str = Field(title="전체 자기 매도 거래량 비율", max_length=82)
    arbt_onsl_shnu_tr_pbmn_rate: str = Field(title="차익 자기 매수 거래 대금 비율", max_length=82)
    nabt_smtm_shun_vol_rate: str = Field(title="비차익 합계 매수 거래량 비율", max_length=72)
    whol_shun_tr_pbmn_rate: str = Field(title="전체 매수 거래대금 비율", max_length=72)
    nabt_entm_ntby_qty_rate: str = Field(title="비차익 위탁 순매수 수량 비율", max_length=82)


class ProgramTradingSummaryDaily(BaseModel, KisHttpBody):
    """프로그램매매 종합현황(일별)"""

    output: Sequence[ProgramTradingSummaryDailyItem] = Field(default_factory=list)


class ProgramTradingInvestorTrendTodayItem(BaseModel):
    invr_cls_code: str = Field(title="투자자코드", max_length=4)
    all_seln_qty: str = Field(title="전체매도수량", max_length=18)
    all_seln_amt: str = Field(title="전체매도대금", max_length=18)
    invr_cls_name: str = Field(title="투자자 구분 명", max_length=20)
    all_shnu_qty: str = Field(title="전체매수수량", max_length=18)
    all_shnu_amt: str = Field(title="전체매수대금", max_length=18)
    all_ntby_amt: str = Field(title="전체순매수대금", max_length=12)
    arbt_seln_qty: str = Field(title="차익매도수량", max_length=18)
    all_ntby_qty: str = Field(title="전체순매수수량", max_length=12)
    arbt_shnu_qty: str = Field(title="차익매수수량", max_length=18)
    arbt_ntby_qty: str = Field(title="차익순매수수량", max_length=12)
    arbt_seln_amt: str = Field(title="차익매도대금", max_length=18)
    arbt_shnu_amt: str = Field(title="차익매수대금", max_length=18)
    arbt_ntby_amt: str = Field(title="차익순매수대금", max_length=12)
    nabt_seln_qty: str = Field(title="비차익매도수량", max_length=18)
    nabt_shnu_qty: str = Field(title="비차익매수수량", max_length=18)
    nabt_ntby_qty: str = Field(title="비차익순매수수량", max_length=12)
    nabt_seln_amt: str = Field(title="비차익매도대금", max_length=18)
    nabt_shnu_amt: str = Field(title="비차익매수대금", max_length=18)
    nabt_ntby_amt: str = Field(title="비차익순매수대금", max_length=12)


class ProgramTradingInvestorTrendToday(BaseModel, KisHttpBody):
    """프로그램매매 투자자매매동향(당일)"""

    output1: Sequence[ProgramTradingInvestorTrendTodayItem] = Field(default_factory=list)


class CreditBalanceTrendDailyItem(BaseModel):
    deal_date: str = Field(title="매매 일자", max_length=8)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    stlm_date: str = Field(title="결제 일자", max_length=8)
    whol_loan_new_stcn: str = Field(title="전체 융자 신규 주수", max_length=18, description="단위: 주")
    whol_loan_rdmp_stcn: str = Field(title="전체 융자 상환 주수", max_length=18, description="단위: 주")
    whol_loan_rmnd_stcn: str = Field(title="전체 융자 잔고 주수", max_length=18, description="단위: 주")
    whol_loan_new_amt: str = Field(title="전체 융자 신규 금액", max_length=18, description="단위: 만원")
    whol_loan_rdmp_amt: str = Field(title="전체 융자 상환 금액", max_length=18, description="단위: 만원")
    whol_loan_rmnd_amt: str = Field(title="전체 융자 잔고 금액", max_length=18, description="단위: 만원")
    whol_loan_rmnd_rate: str = Field(title="전체 융자 잔고 비율", max_length=84)
    whol_loan_gvrt: str = Field(title="전체 융자 공여율", max_length=82)
    whol_stln_new_stcn: str = Field(title="전체 대주 신규 주수", max_length=18, description="단위: 주")
    whol_stln_rdmp_stcn: str = Field(title="전체 대주 상환 주수", max_length=18, description="단위: 주")
    whol_stln_rmnd_stcn: str = Field(title="전체 대주 잔고 주수", max_length=18, description="단위: 주")
    whol_stln_new_amt: str = Field(title="전체 대주 신규 금액", max_length=18, description="단위: 만원")
    whol_stln_rdmp_amt: str = Field(title="전체 대주 상환 금액", max_length=18, description="단위: 만원")
    whol_stln_rmnd_amt: str = Field(title="전체 대주 잔고 금액", max_length=18, description="단위: 만원")
    whol_stln_rmnd_rate: str = Field(title="전체 대주 잔고 비율", max_length=84)
    whol_stln_gvrt: str = Field(title="전체 대주 공여율", max_length=82)
    stck_oprc: str = Field(title="주식 시가2", max_length=10)
    stck_hgpr: str = Field(title="주식 최고가", max_length=10)
    stck_lwpr: str = Field(title="주식 최저가", max_length=10)


class CreditBalanceTrendDaily(BaseModel, KisHttpBody):
    """국내주식 신용잔고 일별추이"""

    output: Sequence[CreditBalanceTrendDailyItem] = Field(default_factory=list)


class ExpectedPriceTrendItem1(BaseModel):
    rprs_mrkt_kor_name: str = Field(title="대표 시장 한글 명", max_length=40)
    antc_cnpr: str = Field(title="예상 체결가", max_length=10)
    antc_cntg_vrss_sign: str = Field(title="예상 체결 대비 부호", max_length=1)
    antc_cntg_vrss: str = Field(title="예상 체결 대비", max_length=10)
    antc_cntg_prdy_ctrt: str = Field(title="예상 체결 전일 대비율", max_length=82)
    antc_vol: str = Field(title="예상 거래량", max_length=18)
    antc_tr_pbmn: str = Field(title="예상 거래대금", max_length=19)


class ExpectedPriceTrendItem2(BaseModel):
    stck_bsop_date: str = Field(title="주식 영업 일자", max_length=8)
    stck_cntg_hour: str = Field(title="주식 체결 시간", max_length=6)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)


class ExpectedPriceTrend(BaseModel, KisHttpBody):
    """국내주식 예상체결가 추이"""

    output1: ExpectedPriceTrendItem1 = Field(title="응답상세1")
    output2: Sequence[ExpectedPriceTrendItem2] = Field(default_factory=list)


class ShortSellingTrendDailyItem1(BaseModel):
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    prdy_vol: str = Field(title="전일 거래량", max_length=18)


class ShortSellingTrendDailyItem2(BaseModel):
    stck_bsop_date: str = Field(title="주식 영업 일자", max_length=8)
    stck_clpr: str = Field(title="주식 종가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    stnd_vol_smtn: str = Field(title="기준 거래량 합계", max_length=18)
    ssts_cntg_qty: str = Field(title="공매도 체결 수량", max_length=12)
    ssts_vol_rlim: str = Field(title="공매도 거래량 비중", max_length=62)
    acml_ssts_cntg_qty: str = Field(title="누적 공매도 체결 수량", max_length=13)
    acml_ssts_cntg_qty_rlim: str = Field(title="누적 공매도 체결 수량 비중", max_length=72)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=18)
    stnd_tr_pbmn_smtn: str = Field(title="기준 거래대금 합계", max_length=18)
    ssts_tr_pbmn: str = Field(title="공매도 거래 대금", max_length=18)
    ssts_tr_pbmn_rlim: str = Field(title="공매도 거래대금 비중", max_length=62)
    acml_ssts_tr_pbmn: str = Field(title="누적 공매도 거래 대금", max_length=19)
    acml_ssts_tr_pbmn_rlim: str = Field(title="누적 공매도 거래 대금 비중", max_length=72)
    stck_oprc: str = Field(title="주식 시가2", max_length=10)
    stck_hgpr: str = Field(title="주식 최고가", max_length=10)
    stck_lwpr: str = Field(title="주식 최저가", max_length=10)
    avrg_prc: str = Field(title="평균가격", max_length=11)


class ShortSellingTrendDaily(BaseModel, KisHttpBody):
    """국내주식 공매도 일별추이"""

    output1: ShortSellingTrendDailyItem1 = Field(title="응답상세1")
    output2: Sequence[ShortSellingTrendDailyItem2] = Field(default_factory=list)


class AfterHoursExpectedFluctuationItem(BaseModel):
    data_rank: str = Field(title="데이터 순위", max_length=10)
    iscd_stat_cls_code: str = Field(title="종목 상태 구분 코드", max_length=3)
    stck_shrn_iscd: str = Field(title="주식 단축 종목코드", max_length=9)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    ovtm_untp_antc_cnpr: str = Field(title="시간외 단일가 예상 체결가", max_length=10)
    ovtm_untp_antc_cntg_vrss: str = Field(title="시간외 단일가 예상 체결 대비", max_length=10)
    ovtm_untp_antc_cntg_vrsssign: str = Field(title="시간외 단일가 예상 체결 대비", max_length=1)
    ovtm_untp_antc_cntg_ctrt: str = Field(title="시간외 단일가 예상 체결 대비율", max_length=82)
    ovtm_untp_askp_rsqn1: str = Field(title="시간외 단일가 매도호가 잔량1", max_length=12)
    ovtm_untp_bidp_rsqn1: str = Field(title="시간외 단일가 매수호가 잔량1", max_length=12)
    ovtm_untp_antc_cnqn: str = Field(title="시간외 단일가 예상 체결량", max_length=18)
    itmt_vol: str = Field(title="장중 거래량", max_length=18)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)


class AfterHoursExpectedFluctuation(BaseModel, KisHttpBody):
    """국내주식 시간외예상체결등락율"""

    output: Sequence[AfterHoursExpectedFluctuationItem] = Field(default_factory=list)


class TradingWeightByAmountItem(BaseModel):
    prpr_name: str = Field(title="가격명", max_length=40)
    smtn_avrg_prpr: str = Field(title="합계 평균가격", max_length=10)
    acml_vol: str = Field(title="합계 거래량", max_length=18)
    whol_ntby_qty_rate: str = Field(title="합계 순매수비율", max_length=72)
    ntby_cntg_csnu: str = Field(title="합계 순매수건수", max_length=10)
    seln_cnqn_smtn: str = Field(title="매도 거래량", max_length=18)
    whol_seln_vol_rate: str = Field(title="매도 거래량비율", max_length=72)
    seln_cntg_csnu: str = Field(title="매도 건수", max_length=10)
    shnu_cnqn_smtn: str = Field(title="매수 거래량", max_length=18)
    whol_shun_vol_rate: str = Field(title="매수 거래량비율", max_length=72)
    shnu_cntg_csnu: str = Field(title="매수 건수", max_length=10)


class TradingWeightByAmount(BaseModel, KisHttpBody):
    """국내주식 체결금액별 매매비중"""

    output: Sequence[TradingWeightByAmountItem] = Field(default_factory=list)


class MarketFundSummaryItem(BaseModel):
    bsop_date: str = Field(title="영업일자", max_length=8)
    bstp_nmix_prpr: str = Field(title="업종지수현재가", max_length=112)
    bstp_nmix_prdy_vrss: str = Field(title="업종지수전일대비", max_length=112)
    prdy_vrss_sign: str = Field(
        title="전일대비부호", max_length=1, description="1. 상한 2. 상승 3. 보합 4. 하한 5. 하락"
    )
    prdy_ctrt: str = Field(title="전일대비율", max_length=82)
    hts_avls: str = Field(title="HTS시가총액", max_length=18, description="단위: 백만원")
    cust_dpmn_amt: str = Field(title="고객예탁금금액", max_length=18, description="단위: 억원")
    cust_dpmn_amt_prdy_vrss: str = Field(title="고객예탁금금액전일대비", max_length=18)
    amt_tnrt: str = Field(title="금액회전율", max_length=84)
    uncl_amt: str = Field(title="미수금액", max_length=18, description="단위: 억원")
    crdt_loan_rmnd: str = Field(title="신용융자잔고", max_length=18, description="단위: 억원")
    futs_tfam_amt: str = Field(title="선물예수금금액", max_length=18, description="단위: 억원")
    sttp_amt: str = Field(title="주식형금액", max_length=18, description="단위: 억원")
    mxtp_amt: str = Field(title="혼합형금액", max_length=18, description="단위: 억원")
    bntp_amt: str = Field(title="채권형금액", max_length=18, description="단위: 억원")
    mmf_amt: str = Field(title="MMF금액", max_length=18, description="단위: 억원")
    secu_lend_amt: str = Field(title="담보대출잔고금액", max_length=18, description="단위: 억원")


class MarketFundSummary(BaseModel, KisHttpBody):
    """국내 증시자금 종합"""

    output: Sequence[MarketFundSummaryItem] = Field(default_factory=list)


class StockLoanTrendDailyItem(BaseModel):
    bsop_date: str = Field(title="일자", max_length=8)
    stck_prpr: str = Field(title="주식 종가", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=8)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    new_stcn: str = Field(title="당일 증가 주수 (체결)", max_length=16)
    rdmp_stcn: str = Field(title="당일 감소 주수 (상환)", max_length=16)
    prdy_rmnd_vrss: str = Field(title="대차거래 증감", max_length=16)
    rmnd_stcn: str = Field(title="당일 잔고 주수", max_length=16)
    rmnd_amt: str = Field(title="당일 잔고 금액", max_length=20)


class StockLoanTrendDaily(BaseModel, KisHttpBody):
    """종목별 일별 대차거래추이"""

    output: Sequence[StockLoanTrendDailyItem] = Field(default_factory=list)


class LimitPriceStocksItem(BaseModel):
    mksc_shrn_iscd: str = Field(title="유가증권단축종목코드", max_length=9)
    hts_kor_isnm: str = Field(title="HTS한글종목명", max_length=40)
    stck_prpr: str = Field(title="주식현재가", max_length=10)
    prdy_vrss_sign: str = Field(title="전일대비부호", max_length=1)
    prdy_vrss: str = Field(title="전일대비", max_length=10)
    prdy_ctrt: str = Field(title="전일대비율", max_length=82)
    acml_vol: str = Field(title="누적거래량", max_length=18)
    total_askp_rsqn: str = Field(title="총매도호가잔량", max_length=12)
    total_bidp_rsqn: str = Field(title="총매수호가잔량", max_length=12)
    askp_rsqn1: str = Field(title="매도호가잔량1", max_length=12)
    bidp_rsqn1: str = Field(title="매수호가잔량1", max_length=12)
    prdy_vol: str = Field(title="전일거래량", max_length=18)
    seln_cnqn: str = Field(title="매도체결량", max_length=18)
    shnu_cnqn: str = Field(title="매수2체결량", max_length=18)
    stck_llam: str = Field(title="주식하한가", max_length=10)
    stck_mxpr: str = Field(title="주식상한가", max_length=10)
    prdy_vrss_vol_rate: str = Field(title="전일대비거래량비율", max_length=84)


class LimitPriceStocks(BaseModel, KisHttpBody):
    """국내주식 상하한가 표착"""

    output: Sequence[LimitPriceStocksItem] = Field(default_factory=list)


class ResistanceLevelTradingWeightItem1(BaseModel):
    rprs_mrkt_kor_name: str = Field(title="대표시장한글명", max_length=40)
    stck_shrn_iscd: str = Field(title="주식단축종목코드", max_length=9)
    hts_kor_isnm: str = Field(title="HTS한글종목명", max_length=40)
    stck_prpr: str = Field(title="주식현재가", max_length=10)
    prdy_vrss_sign: str = Field(title="전일대비부호", max_length=1)
    prdy_vrss: str = Field(title="전일대비", max_length=10)
    prdy_ctrt: str = Field(title="전일대비율", max_length=82)
    acml_vol: str = Field(title="누적거래량", max_length=18)
    prdy_vol: str = Field(title="전일거래량", max_length=18)
    wghn_avrg_stck_prc: str = Field(title="가중평균주식가격", max_length=192)
    lstn_stcn: str = Field(title="상장주수", max_length=18)


class ResistanceLevelTradingWeightItem2(BaseModel):
    data_rank: str = Field(title="데이터순위", max_length=10)
    stck_prpr: str = Field(title="주식현재가", max_length=10)
    cntg_vol: str = Field(title="체결거래량", max_length=18)
    acml_vol_rlim: str = Field(title="누적거래량비중", max_length=72)


class ResistanceLevelTradingWeight(BaseModel, KisHttpBody):
    """국내주식 매물대/거래비중"""

    output1: ResistanceLevelTradingWeightItem1 = Field(title="응답상세1")
    output2: Sequence[ResistanceLevelTradingWeightItem2] = Field(default_factory=list)
