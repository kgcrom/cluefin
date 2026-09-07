from typing import Sequence

from pydantic import BaseModel, Field

from cluefin_openapi.kis._model import KisHttpBody


class TradingVolumeRankItem(BaseModel):
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드")
    data_rank: str = Field(title="데이터 순위")
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    prdy_vol: str = Field(title="전일 거래량")
    lstn_stcn: str = Field(title="상장 주수")
    avrg_vol: str = Field(title="평균 거래량")
    n_befr_clpr_vrss_prpr_rate: str = Field(title="N일전종가대비현재가대비율")
    vol_inrt: str = Field(title="거래량증가율")
    vol_tnrt: str = Field(title="거래량 회전율")
    nday_vol_tnrt: str = Field(title="N일 거래량 회전율")
    avrg_tr_pbmn: str = Field(title="평균 거래 대금")
    tr_pbmn_tnrt: str = Field(title="거래대금회전율")
    nday_tr_pbmn_tnrt: str = Field(title="N일 거래대금 회전율")
    acml_tr_pbmn: str = Field(title="누적 거래 대금")


class TradingVolumeRank(BaseModel, KisHttpBody):
    """거래량순위"""

    output: Sequence[TradingVolumeRankItem] = Field(default_factory=list)


class StockFluctuationRankItem(BaseModel):
    stck_shrn_iscd: str = Field(title="주식 단축 종목코드")
    data_rank: str = Field(title="데이터 순위")
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    stck_hgpr: str = Field(title="주식 최고가")
    hgpr_hour: str = Field(title="최고가 시간")
    acml_hgpr_date: str = Field(title="누적 최고가 일자")
    stck_lwpr: str = Field(title="주식 최저가")
    lwpr_hour: str = Field(title="최저가 시간")
    acml_lwpr_date: str = Field(title="누적 최저가 일자")
    lwpr_vrss_prpr_rate: str = Field(title="최저가 대비 현재가 비율")
    dsgt_date_clpr_vrss_prpr_rate: str = Field(title="지정 일자 종가 대비 현재가 비")
    cnnt_ascn_dynu: str = Field(title="연속 상승 일수")
    hgpr_vrss_prpr_rate: str = Field(title="최고가 대비 현재가 비율")
    cnnt_down_dynu: str = Field(title="연속 하락 일수")
    oprc_vrss_prpr_sign: str = Field(title="시가2 대비 현재가 부호")
    oprc_vrss_prpr: str = Field(title="시가2 대비 현재가")
    oprc_vrss_prpr_rate: str = Field(title="시가2 대비 현재가 비율")
    prd_rsfl: str = Field(title="기간 등락")
    prd_rsfl_rate: str = Field(title="기간 등락 비율")


class StockFluctuationRank(BaseModel, KisHttpBody):
    """국내주식 등락률 순위"""

    output: Sequence[StockFluctuationRankItem] = Field(default_factory=list)


class StockHogaQuantityRankItem(BaseModel):
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드")
    data_rank: str = Field(title="데이터 순위")
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    total_askp_rsqn: str = Field(title="총 매도호가 잔량")
    total_bidp_rsqn: str = Field(title="총 매수호가 잔량")
    total_ntsl_bidp_rsqn: str = Field(title="총 순 매수호가 잔량")
    shnu_rsqn_rate: str = Field(title="매수 잔량 비율")
    seln_rsqn_rate: str = Field(title="매도 잔량 비율")


class StockHogaQuantityRank(BaseModel, KisHttpBody):
    """국내주식 호가잔량 순위"""

    output: Sequence[StockHogaQuantityRankItem] = Field(default_factory=list)


class StockProfitabilityIndicatorRankItem(BaseModel):
    data_rank: str = Field(title="데이터 순위")
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드")
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    sale_totl_prfi: str = Field(title="매출 총 이익")
    bsop_prti: str = Field(title="영업 이익")
    op_prfi: str = Field(title="경상 이익")
    thtr_ntin: str = Field(title="당기순이익")
    total_aset: str = Field(title="자산총계")
    total_lblt: str = Field(title="부채총계")
    total_cptl: str = Field(title="자본총계")
    stac_month: str = Field(title="결산 월")
    stac_month_cls_code: str = Field(title="결산 월 구분 코드")
    iqry_csnu: str = Field(title="조회 건수")


class StockProfitabilityIndicatorRank(BaseModel, KisHttpBody):
    """국내주식 수익자산지표 순위"""

    output: Sequence[StockProfitabilityIndicatorRankItem] = Field(default_factory=list)


class StockMarketCapTopItem(BaseModel):
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드")
    data_rank: str = Field(title="데이터 순위")
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    lstn_stcn: str = Field(title="상장 주수")
    stck_avls: str = Field(title="시가 총액")
    mrkt_whol_avls_rlim: str = Field(title="시장 전체 시가총액 비중")


class StockMarketCapTop(BaseModel, KisHttpBody):
    """국내주식 시가총액 상위"""

    output: Sequence[StockMarketCapTopItem] = Field(default_factory=list)


class StockFinanceRatioRankItem(BaseModel):
    data_rank: str = Field(title="데이터 순위")
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드")
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    cptl_op_prfi: str = Field(title="총자본경상이익율")
    cptl_ntin_rate: str = Field(title="총자본 순이익율")
    sale_totl_rate: str = Field(title="매출액 총이익율")
    sale_ntin_rate: str = Field(title="매출액 순이익율")
    bis: str = Field(title="자기자본비율")
    lblt_rate: str = Field(title="부채 비율")
    bram_depn: str = Field(title="차입금 의존도")
    rsrv_rate: str = Field(title="유보 비율")
    grs: str = Field(title="매출액 증가율")
    op_prfi_inrt: str = Field(title="경상 이익 증가율")
    bsop_prfi_inrt: str = Field(title="영업 이익 증가율")
    ntin_inrt: str = Field(title="순이익 증가율")
    equt_inrt: str = Field(title="자기자본 증가율")
    cptl_tnrt: str = Field(title="총자본회전율")
    sale_bond_tnrt: str = Field(title="매출 채권 회전율")
    totl_aset_inrt: str = Field(title="총자산 증가율")
    stac_month: str = Field(title="결산 월")
    stac_month_cls_code: str = Field(title="결산 월 구분 코드")
    iqry_csnu: str = Field(title="조회 건수")


class StockFinanceRatioRank(BaseModel, KisHttpBody):
    """국내주식 재무비율 순위"""

    output: Sequence[StockFinanceRatioRankItem] = Field(default_factory=list)


class StockTimeHogaRankItem(BaseModel):
    stck_shrn_iscd: str = Field(title="주식 단축 종목코드")
    data_rank: str = Field(title="데이터 순위")
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_ctrt: str = Field(title="전일 대비율")
    ovtm_total_askp_rsqn: str = Field(title="시간외 총 매도호가 잔량")
    ovtm_total_bidp_rsqn: str = Field(title="시간외 총 매수호가 잔량")
    mkob_otcp_vol: str = Field(title="장개시전 시간외종가 거래량")
    mkfa_otcp_vol: str = Field(title="장종료후 시간외종가 거래량")


class StockTimeHogaRank(BaseModel, KisHttpBody):
    """국내주식 시간외잔량 순위"""

    output: Sequence[StockTimeHogaRankItem] = Field(default_factory=list)


class StockPreferredStockRatioTopItem(BaseModel):
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드")
    data_rank: str = Field(title="데이터 순위")
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    acml_vol: str = Field(title="누적 거래량")
    prst_iscd: str = Field(title="우선주 종목코드")
    prst_kor_isnm: str = Field(title="우선주 한글 종목명")
    prst_prpr: str = Field(title="우선주 현재가")
    prst_prdy_vrss: str = Field(title="우선주 전일대비")
    prst_prdy_vrss_sign: str = Field(title="우선주 전일 대비 부호")
    prst_acml_vol: str = Field(title="우선주 누적 거래량")
    diff_prpr: str = Field(title="차이 현재가")
    dprt: str = Field(title="괴리율")
    prdy_ctrt: str = Field(title="전일 대비율")
    prst_prdy_ctrt: str = Field(title="우선주 전일 대비율")


class StockPreferredStockRatioTop(BaseModel, KisHttpBody):
    """국내주식 우선주/괴리율 상위"""

    output: Sequence[StockPreferredStockRatioTopItem] = Field(default_factory=list)


class StockDisparityIndexRankItem(BaseModel):
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드")
    data_rank: str = Field(title="데이터 순위")
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_ctrt: str = Field(title="전일 대비율")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    acml_vol: str = Field(title="누적 거래량")
    d5_dsrt: str = Field(title="5일 이격도")
    d10_dsrt: str = Field(title="10일 이격도")
    d20_dsrt: str = Field(title="20일 이격도")
    d60_dsrt: str = Field(title="60일 이격도")
    d120_dsrt: str = Field(title="120일 이격도")


class StockDisparityIndexRank(BaseModel, KisHttpBody):
    """국내주식 이격도 순위"""

    output: Sequence[StockDisparityIndexRankItem] = Field(default_factory=list)


class StockMarketPriceRankItem(BaseModel):
    data_rank: str = Field(title="데이터 순위")
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드")
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    per: str = Field(title="PER")
    pbr: str = Field(title="PBR")
    pcr: str = Field(title="PCR")
    psr: str = Field(title="PSR")
    eps: str = Field(title="EPS")
    eva: str = Field(title="EVA")
    ebitda: str = Field(title="EBITDA")
    pv_div_ebitda: str = Field(title="PV DIV EBITDA")
    ebitda_div_fnnc_expn: str = Field(title="EBITDA DIV 금융비용")
    stac_month: str = Field(title="결산 월")
    stac_month_cls_code: str = Field(title="결산 월 구분 코드")
    iqry_csnu: str = Field(title="조회 건수")


class StockMarketPriceRank(BaseModel, KisHttpBody):
    """국내주식 시장가치 순위"""

    output: Sequence[StockMarketPriceRankItem] = Field(default_factory=list)


class StockExecutionStrengthTopItem(BaseModel):
    stck_shrn_iscd: str = Field(title="주식 단축 종목코드")
    data_rank: str = Field(title="데이터 순위")
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    tday_rltv: str = Field(title="당일 체결강도")
    seln_cnqn_smtn: str = Field(title="매도 체결량 합계")
    shnu_cnqn_smtn: str = Field(title="매수2 체결량 합계")


class StockExecutionStrengthTop(BaseModel, KisHttpBody):
    """국내주식 체결강도 상위"""

    output: Sequence[StockExecutionStrengthTopItem] = Field(default_factory=list)


class StockWatchlistRegistrationTopItem(BaseModel):
    mrkt_div_cls_name: str = Field(title="시장 분류 구분 명")
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드")
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    acml_tr_pbmn: str = Field(title="누적 거래 대금")
    askp: str = Field(title="매도호가")
    bidp: str = Field(title="매수호가")
    data_rank: str = Field(title="데이터 순위")
    inter_issu_reg_csnu: str = Field(title="관심 종목 등록 건수")


class StockWatchlistRegistrationTop(BaseModel, KisHttpBody):
    """국내주식 관심종목등록 상위"""

    output: Sequence[StockWatchlistRegistrationTopItem] = Field(default_factory=list)


class StockExpectedExecutionRiseDeclineTopItem(BaseModel):
    stck_shrn_iscd: str = Field(title="주식 단축 종목코드")
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_ctrt: str = Field(title="전일 대비율")
    stck_sdpr: str = Field(title="주식 기준가")
    seln_rsqn: str = Field(title="매도 잔량")
    askp: str = Field(title="매도호가")
    bidp: str = Field(title="매수호가")
    shnu_rsqn: str = Field(title="매수2 잔량")
    cntg_vol: str = Field(title="체결 거래량")
    antc_tr_pbmn: str = Field(title="체결 거래대금")
    total_askp_rsqn: str = Field(title="총 매도호가 잔량")
    total_bidp_rsqn: str = Field(title="총 매수호가 잔량")


class StockExpectedExecutionRiseDeclineTop(BaseModel, KisHttpBody):
    """국내주식 예상체결 상승/하락상위"""

    output: Sequence[StockExpectedExecutionRiseDeclineTopItem] = Field(default_factory=list)


class StockProprietaryTradingTopItem(BaseModel):
    data_rank: str = Field(title="데이터 순위")
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드")
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    acml_tr_pbmn: str = Field(title="누적 거래 대금")
    seln_cnqn_smtn: str = Field(title="매도 체결량 합계")
    shnu_cnqn_smtn: str = Field(title="매수2 체결량 합계")
    ntby_cnqn: str = Field(title="순매수 체결량")


class StockProprietaryTradingTop(BaseModel, KisHttpBody):
    """국내주식 당사매매종목 상위"""

    output: Sequence[StockProprietaryTradingTopItem] = Field(default_factory=list)


class StockNewHighLowApproachingTopItem(BaseModel):
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드")
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_ctrt: str = Field(title="전일 대비율")
    askp: str = Field(title="매도호가")
    askp_rsqn1: str = Field(title="매도호가 잔량1")
    bidp: str = Field(title="매수호가")
    bidp_rsqn1: str = Field(title="매수호가 잔량1")
    acml_vol: str = Field(title="누적 거래량")
    new_hgpr: str = Field(title="신 최고가")
    hprc_near_rate: str = Field(title="고가 근접 비율")
    new_lwpr: str = Field(title="신 최저가")
    lwpr_near_rate: str = Field(title="저가 근접 비율")
    stck_sdpr: str = Field(title="주식 기준가")


class StockNewHighLowApproachingTop(BaseModel, KisHttpBody):
    """국내주식 신고/신저근접종목 상위"""

    output: Sequence[StockNewHighLowApproachingTopItem] = Field(default_factory=list)


class StockDividendYieldTopItem(BaseModel):
    rank: str = Field(title="순위")
    sht_cd: str = Field(title="종목코드")
    isin_name: str = Field(title="종목명")
    record_date: str = Field(title="기준일")
    per_sto_divi_amt: str = Field(title="현금/주식배당금")
    divi_rate: str = Field(title="현금/주식배당률(%)")
    divi_kind: str = Field(title="배당종류")


class StockDividendYieldTop(BaseModel, KisHttpBody):
    """국내주식 배당률 상위"""

    # 공식 문서는 output1이지만 실서버는 output으로 응답한다(실측).
    output: Sequence[StockDividendYieldTopItem] = Field(default_factory=list)


class StockLargeExecutionCountTopItem(BaseModel):
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드")
    data_rank: str = Field(title="데이터 순위")
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    shnu_cntg_csnu: str = Field(title="매수2 체결 건수")
    seln_cntg_csnu: str = Field(title="매도 체결 건수")
    ntby_cnqn: str = Field(title="순매수 체결량")


class StockLargeExecutionCountTop(BaseModel, KisHttpBody):
    """국내주식 대량체결건수 상위"""

    output: Sequence[StockLargeExecutionCountTopItem] = Field(default_factory=list)


class StockCreditBalanceTopItem1(BaseModel):
    bstp_cls_code: str = Field(title="업종 구분 코드")
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    stnd_date1: str = Field(title="기준 일자1")
    stnd_date2: str = Field(title="기준 일자2")


class StockCreditBalanceTopItem2(BaseModel):
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드")
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    whol_loan_rmnd_stcn: str = Field(title="전체 융자 잔고 주수")
    whol_loan_rmnd_amt: str = Field(title="전체 융자 잔고 금액")
    whol_loan_rmnd_rate: str = Field(title="전체 융자 잔고 비율")
    whol_stln_rmnd_stcn: str = Field(title="전체 대주 잔고 주수")
    whol_stln_rmnd_amt: str = Field(title="전체 대주 잔고 금액")
    whol_stln_rmnd_rate: str = Field(title="전체 대주 잔고 비율")
    nday_vrss_loan_rmnd_inrt: str = Field(title="N일 대비 융자 잔고 증가율")
    nday_vrss_stln_rmnd_inrt: str = Field(title="N일 대비 대주 잔고 증가율")


class StockCreditBalanceTop(BaseModel, KisHttpBody):
    """국내주식 신용잔고 상위"""

    output1: Sequence[StockCreditBalanceTopItem1] = Field(default_factory=list)
    output2: Sequence[StockCreditBalanceTopItem2] = Field(default_factory=list)


class StockShortSellingTopItem(BaseModel):
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드")
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    acml_tr_pbmn: str = Field(title="누적 거래 대금")
    ssts_cntg_qty: str = Field(title="공매도 체결 수량")
    ssts_vol_rlim: str = Field(title="공매도 거래량 비중")
    ssts_tr_pbmn: str = Field(title="공매도 거래 대금")
    ssts_tr_pbmn_rlim: str = Field(title="공매도 거래대금 비중")
    stnd_date1: str = Field(title="기준 일자1")
    stnd_date2: str = Field(title="기준 일자2")
    avrg_prc: str = Field(title="평균가격")


class StockShortSellingTop(BaseModel, KisHttpBody):
    """국내주식 공매도 상위종목"""

    output: Sequence[StockShortSellingTopItem] = Field(default_factory=list)


class StockAfterHoursFluctuationRankItem1(BaseModel):
    ovtm_untp_uplm_issu_cnt: str = Field(title="시간외 단일가 상한 종목 수")
    ovtm_untp_ascn_issu_cnt: str = Field(title="시간외 단일가 상승 종목 수")
    ovtm_untp_stnr_issu_cnt: str = Field(title="시간외 단일가 보합 종목 수")
    ovtm_untp_lslm_issu_cnt: str = Field(title="시간외 단일가 하한 종목 수")
    ovtm_untp_down_issu_cnt: str = Field(title="시간외 단일가 하락 종목 수")
    ovtm_untp_acml_vol: str = Field(title="시간외 단일가 누적 거래량")
    ovtm_untp_acml_tr_pbmn: str = Field(title="시간외 단일가 누적 거래대금")
    ovtm_untp_exch_vol: str = Field(title="시간외 단일가 거래소 거래량")
    ovtm_untp_exch_tr_pbmn: str = Field(title="시간외 단일가 거래소 거래대금")
    ovtm_untp_kosdaq_vol: str = Field(title="시간외 단일가 KOSDAQ 거래량")
    ovtm_untp_kosdaq_tr_pbmn: str = Field(title="시간외 단일가 KOSDAQ 거래대금")


class StockAfterHoursFluctuationRankItem2(BaseModel):
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드")
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    ovtm_untp_prpr: str = Field(title="시간외 단일가 현재가")
    ovtm_untp_prdy_vrss: str = Field(title="시간외 단일가 전일 대비")
    ovtm_untp_prdy_vrss_sign: str = Field(title="시간외 단일가 전일 대비 부호")
    ovtm_untp_prdy_ctrt: str = Field(title="시간외 단일가 전일 대비율")
    ovtm_untp_askp1: str = Field(title="시간외 단일가 매도호가1")
    ovtm_untp_seln_rsqn: str = Field(title="시간외 단일가 매도 잔량")
    ovtm_untp_bidp1: str = Field(title="시간외 단일가 매수호가1")
    ovtm_untp_shnu_rsqn: str = Field(title="시간외 단일가 매수 잔량")
    ovtm_untp_vol: str = Field(title="시간외 단일가 거래량")
    ovtm_vrss_acml_vol_rlim: str = Field(title="시간외 대비 누적 거래량 비중")
    stck_prpr: str = Field(title="주식 현재가")
    acml_vol: str = Field(title="누적 거래량")
    bidp: str = Field(title="매수호가")
    askp: str = Field(title="매도호가")


class StockAfterHoursFluctuationRank(BaseModel, KisHttpBody):
    """국내주식 시간외등락율순위"""

    output1: StockAfterHoursFluctuationRankItem1 = Field(title="응답상세1")
    output2: Sequence[StockAfterHoursFluctuationRankItem2] = Field(default_factory=list)


class StockAfterHoursVolumeRankItem1(BaseModel):
    ovtm_untp_exch_vol: str = Field(title="시간외 단일가 거래소 거래량")
    ovtm_untp_exch_tr_pbmn: str = Field(title="시간외 단일가 거래소 거래대금")
    ovtm_untp_kosdaq_vol: str = Field(title="시간외 단일가 KOSDAQ 거래량")
    ovtm_untp_kosdaq_tr_pbmn: str = Field(title="시간외 단일가 KOSDAQ 거래대금")


class StockAfterHoursVolumeRankItem2(BaseModel):
    stck_shrn_iscd: str = Field(title="주식 단축 종목코드")
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    ovtm_untp_prpr: str = Field(title="시간외 단일가 현재가")
    ovtm_untp_prdy_vrss: str = Field(title="시간외 단일가 전일 대비")
    ovtm_untp_prdy_vrss_sign: str = Field(title="시간외 단일가 전일 대비 부호")
    ovtm_untp_prdy_ctrt: str = Field(title="시간외 단일가 전일 대비율")
    ovtm_untp_seln_rsqn: str = Field(title="시간외 단일가 매도 잔량")
    ovtm_untp_shnu_rsqn: str = Field(title="시간외 단일가 매수 잔량")
    ovtm_untp_vol: str = Field(title="시간외 단일가 거래량")
    ovtm_vrss_acml_vol_rlim: str = Field(title="시간외 대비 누적 거래량 비중")
    stck_prpr: str = Field(title="주식 현재가")
    acml_vol: str = Field(title="누적 거래량")
    bidp: str = Field(title="매수호가")
    askp: str = Field(title="매도호가")


class StockAfterHoursVolumeRank(BaseModel, KisHttpBody):
    """국내주식 시간외거래량순위"""

    output1: StockAfterHoursVolumeRankItem1 = Field(title="응답상세1")
    output2: Sequence[StockAfterHoursVolumeRankItem2] = Field(default_factory=list)


class HtsInquiryTop20Item(BaseModel):
    mrkt_div_cls_code: str = Field(title="시장구분", description="J : 코스피, Q : 코스닥")
    mksc_shrn_iscd: str = Field(title="종목코드")


class HtsInquiryTop20(BaseModel, KisHttpBody):
    """HTS조회상위20종목"""

    output1: Sequence[HtsInquiryTop20Item] = Field(default_factory=list)
