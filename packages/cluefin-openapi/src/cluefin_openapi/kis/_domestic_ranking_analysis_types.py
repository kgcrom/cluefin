from pydantic import BaseModel, Field
from typing import Sequence
from cluefin_openapi.kis._model import KisHttpBody


class TradingVolumeRankItem(BaseModel):
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드", max_length=9)
    data_rank: str = Field(title="데이터 순위", max_length=10)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    prdy_vol: str = Field(title="전일 거래량", max_length=18)
    lstn_stcn: str = Field(title="상장 주수", max_length=18)
    avrg_vol: str = Field(title="평균 거래량", max_length=18)
    n_befr_clpr_vrss_prpr_rate: str = Field(title="N일전종가대비현재가대비율", max_length=82)
    vol_inrt: str = Field(title="거래량증가율", max_length=84)
    vol_tnrt: str = Field(title="거래량 회전율", max_length=82)
    nday_vol_tnrt: str = Field(title="N일 거래량 회전율", max_length=8)
    avrg_tr_pbmn: str = Field(title="평균 거래 대금", max_length=18)
    tr_pbmn_tnrt: str = Field(title="거래대금회전율", max_length=82)
    nday_tr_pbmn_tnrt: str = Field(title="N일 거래대금 회전율", max_length=8)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=18)


class TradingVolumeRank(BaseModel, KisHttpBody):
    """거래량순위"""

    output: Sequence[TradingVolumeRankItem] = Field(default_factory=list)


class StockFluctuationRankItem(BaseModel):
    stck_shrn_iscd: str = Field(title="주식 단축 종목코드", max_length=9)
    data_rank: str = Field(title="데이터 순위", max_length=10)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    stck_hgpr: str = Field(title="주식 최고가", max_length=10)
    hgpr_hour: str = Field(title="최고가 시간", max_length=6)
    acml_hgpr_date: str = Field(title="누적 최고가 일자", max_length=8)
    stck_lwpr: str = Field(title="주식 최저가", max_length=10)
    lwpr_hour: str = Field(title="최저가 시간", max_length=6)
    acml_lwpr_date: str = Field(title="누적 최저가 일자", max_length=8)
    lwpr_vrss_prpr_rate: str = Field(title="최저가 대비 현재가 비율", max_length=84)
    dsgt_date_clpr_vrss_prpr_rate: str = Field(title="지정 일자 종가 대비 현재가 비", max_length=84)
    cnnt_ascn_dynu: str = Field(title="연속 상승 일수", max_length=5)
    hgpr_vrss_prpr_rate: str = Field(title="최고가 대비 현재가 비율", max_length=84)
    cnnt_down_dynu: str = Field(title="연속 하락 일수", max_length=5)
    oprc_vrss_prpr_sign: str = Field(title="시가2 대비 현재가 부호", max_length=1)
    oprc_vrss_prpr: str = Field(title="시가2 대비 현재가", max_length=10)
    oprc_vrss_prpr_rate: str = Field(title="시가2 대비 현재가 비율", max_length=84)
    prd_rsfl: str = Field(title="기간 등락", max_length=10)
    prd_rsfl_rate: str = Field(title="기간 등락 비율", max_length=84)


class StockFluctuationRank(BaseModel, KisHttpBody):
    """국내주식 등락률 순위"""

    output: Sequence[StockFluctuationRankItem] = Field(default_factory=list)


class StockHogaQuantityRankItem(BaseModel):
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드", max_length=9)
    data_rank: str = Field(title="데이터 순위", max_length=10)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    total_askp_rsqn: str = Field(title="총 매도호가 잔량", max_length=12)
    total_bidp_rsqn: str = Field(title="총 매수호가 잔량", max_length=12)
    total_ntsl_bidp_rsqn: str = Field(title="총 순 매수호가 잔량", max_length=12)
    shnu_rsqn_rate: str = Field(title="매수 잔량 비율", max_length=84)
    seln_rsqn_rate: str = Field(title="매도 잔량 비율", max_length=84)


class StockHogaQuantityRank(BaseModel, KisHttpBody):
    """국내주식 호가잔량 순위"""

    output: Sequence[StockHogaQuantityRankItem] = Field(default_factory=list)


class StockProfitabilityIndicatorRankItem(BaseModel):
    data_rank: str = Field(title="데이터 순위", max_length=10)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드", max_length=9)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    sale_totl_prfi: str = Field(title="매출 총 이익", max_length=182)
    bsop_prti: str = Field(title="영업 이익", max_length=182)
    op_prfi: str = Field(title="경상 이익", max_length=182)
    thtr_ntin: str = Field(title="당기순이익", max_length=102)
    total_aset: str = Field(title="자산총계", max_length=102)
    total_lblt: str = Field(title="부채총계", max_length=102)
    total_cptl: str = Field(title="자본총계", max_length=102)
    stac_month: str = Field(title="결산 월", max_length=2)
    stac_month_cls_code: str = Field(title="결산 월 구분 코드", max_length=2)
    iqry_csnu: str = Field(title="조회 건수", max_length=10)


class StockProfitabilityIndicatorRank(BaseModel, KisHttpBody):
    """국내주식 수익자산지표 순위"""

    output: Sequence[StockProfitabilityIndicatorRankItem] = Field(default_factory=list) 


class StockMarketCapTopItem(BaseModel):
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드", max_length=9)
    data_rank: str = Field(title="데이터 순위", max_length=10)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    lstn_stcn: str = Field(title="상장 주수", max_length=18)
    stck_avls: str = Field(title="시가 총액", max_length=18)
    mrkt_whol_avls_rlim: str = Field(title="시장 전체 시가총액 비중", max_length=52)


class StockMarketCapTop(BaseModel, KisHttpBody):
    """국내주식 시가총액 상위"""

    output: Sequence[StockMarketCapTopItem] = Field(default_factory=list)


class StockFinanceRatioRankItem(BaseModel):
    data_rank: str = Field(title="데이터 순위", max_length=10)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드", max_length=9)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    cptl_op_prfi: str = Field(title="총자본경상이익율", max_length=92)
    cptl_ntin_rate: str = Field(title="총자본 순이익율", max_length=92)
    sale_totl_rate: str = Field(title="매출액 총이익율", max_length=92)
    sale_ntin_rate: str = Field(title="매출액 순이익율", max_length=92)
    bis: str = Field(title="자기자본비율", max_length=92)
    lblt_rate: str = Field(title="부채 비율", max_length=84)
    bram_depn: str = Field(title="차입금 의존도", max_length=92)
    rsrv_rate: str = Field(title="유보 비율", max_length=124)
    grs: str = Field(title="매출액 증가율", max_length=124)
    op_prfi_inrt: str = Field(title="경상 이익 증가율", max_length=124)
    bsop_prfi_inrt: str = Field(title="영업 이익 증가율", max_length=124)
    ntin_inrt: str = Field(title="순이익 증가율", max_length=124)
    equt_inrt: str = Field(title="자기자본 증가율", max_length=92)
    cptl_tnrt: str = Field(title="총자본회전율", max_length=92)
    sale_bond_tnrt: str = Field(title="매출 채권 회전율", max_length=92)
    totl_aset_inrt: str = Field(title="총자산 증가율", max_length=92)
    stac_month: str = Field(title="결산 월", max_length=2)
    stac_month_cls_code: str = Field(title="결산 월 구분 코드", max_length=2)
    iqry_csnu: str = Field(title="조회 건수", max_length=10)


class StockFinanceRatioRank(BaseModel, KisHttpBody):
    """국내주식 재무비율 순위"""

    output: Sequence[StockFinanceRatioRankItem] = Field(default_factory=list)

class StockTimeHogaRankItem(BaseModel):
    stck_shrn_iscd: str = Field(title="주식 단축 종목코드", max_length=9)
    data_rank: str = Field(title="데이터 순위", max_length=10)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    ovtm_total_askp_rsqn: str = Field(title="시간외 총 매도호가 잔량", max_length=12)
    ovtm_total_bidp_rsqn: str = Field(title="시간외 총 매수호가 잔량", max_length=12)
    mkob_otcp_vol: str = Field(title="장개시전 시간외종가 거래량", max_length=18)
    mkfa_otcp_vol: str = Field(title="장종료후 시간외종가 거래량", max_length=18)


class StockTimeHogaRank(BaseModel,  KisHttpBody):
    """국내주식 시간외잔량 순위"""

    output: Sequence[StockTimeHogaRankItem] = Field(default_factory=list)



class StockPreferredStockRatioTopItem(BaseModel):
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드", max_length=9)
    data_rank: str = Field(title="데이터 순위", max_length=10)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=10)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=10)
    acml_vol: str = Field(title="누적 거래량", max_length=10)
    prst_iscd: str = Field(title="우선주 종목코드", max_length=10)
    prst_kor_isnm: str = Field(title="우선주 한글 종목명", max_length=10)
    prst_prpr: str = Field(title="우선주 현재가", max_length=10)
    prst_prdy_vrss: str = Field(title="우선주 전일대비", max_length=10)
    prst_prdy_vrss_sign: str = Field(title="우선주 전일 대비 부호", max_length=10)
    prst_acml_vol: str = Field(title="우선주 누적 거래량", max_length=40)
    diff_prpr: str = Field(title="차이 현재가", max_length=10)
    dprt: str = Field(title="괴리율", max_length=10)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    prst_prdy_ctrt: str = Field(title="우선주 전일 대비율", max_length=82)


class StockPreferredStockRatioTop(BaseModel, KisHttpBody):
    """국내주식 우선주/괴리율 상위"""

    output: Sequence[StockPreferredStockRatioTopItem] = Field(default_factory=list)

class StockDisparityIndexRankItem(BaseModel):
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드", max_length=9)
    data_rank: str = Field(title="데이터 순위", max_length=10)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    d5_dsrt: str = Field(title="5일 이격도", max_length=112)
    d10_dsrt: str = Field(title="10일 이격도", max_length=112)
    d20_dsrt: str = Field(title="20일 이격도", max_length=112)
    d60_dsrt: str = Field(title="60일 이격도", max_length=112)
    d120_dsrt: str = Field(title="120일 이격도", max_length=112)


class StockDisparityIndexRank(BaseModel, KisHttpBody):
    """국내주식 이격도 순위"""

    output: Sequence[StockDisparityIndexRankItem] = Field(default_factory=list)

class StockMarketPriceRankItem(BaseModel):
    data_rank: str = Field(title="데이터 순위", max_length=10)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드", max_length=9)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    per: str = Field(title="PER", max_length=82)
    pbr: str = Field(title="PBR", max_length=82)
    pcr: str = Field(title="PCR", max_length=82)
    psr: str = Field(title="PSR", max_length=82)
    eps: str = Field(title="EPS", max_length=112)
    eva: str = Field(title="EVA", max_length=82)
    ebitda: str = Field(title="EBITDA", max_length=82)
    pv_div_ebitda: str = Field(title="PV DIV EBITDA", max_length=82)
    ebitda_div_fnnc_expn: str = Field(title="EBITDA DIV 금융비용", max_length=82)
    stac_month: str = Field(title="결산 월", max_length=2)
    stac_month_cls_code: str = Field(title="결산 월 구분 코드", max_length=2)
    iqry_csnu: str = Field(title="조회 건수", max_length=10)


class StockMarketPriceRank(BaseModel, KisHttpBody):
    """국내주식 시장가치 순위"""

    output: Sequence[StockMarketPriceRankItem] = Field(default_factory=list)

class StockExecutionStrengthTopItem(BaseModel):
    stck_shrn_iscd: str = Field(title="주식 단축 종목코드", max_length=9)
    data_rank: str = Field(title="데이터 순위", max_length=10)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    tday_rltv: str = Field(title="당일 체결강도", max_length=112)
    seln_cnqn_smtn: str = Field(title="매도 체결량 합계", max_length=18)
    shnu_cnqn_smtn: str = Field(title="매수2 체결량 합계", max_length=18)


class StockExecutionStrengthTop(BaseModel, KisHttpBody):
    """국내주식 체결강도 상위"""

    output: Sequence[StockExecutionStrengthTopItem] = Field(default_factory=list)

class StockWatchlistRegistrationTopItem(BaseModel):
    mrkt_div_cls_name: str = Field(title="시장 분류 구분 명", max_length=40)
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드", max_length=9)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=18)
    askp: str = Field(title="매도호가", max_length=10)
    bidp: str = Field(title="매수호가", max_length=10)
    data_rank: str = Field(title="데이터 순위", max_length=10)
    inter_issu_reg_csnu: str = Field(title="관심 종목 등록 건수", max_length=10)


class StockWatchlistRegistrationTop(BaseModel, KisHttpBody):
    """국내주식 관심종목등록 상위"""

    output: Sequence[StockWatchlistRegistrationTopItem] = Field(default_factory=list)

class StockExpectedExecutionRiseDeclineTopItem(BaseModel):
    stck_shrn_iscd: str = Field(title="주식 단축 종목코드", max_length=9)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    stck_sdpr: str = Field(title="주식 기준가", max_length=10)
    seln_rsqn: str = Field(title="매도 잔량", max_length=12)
    askp: str = Field(title="매도호가", max_length=10)
    bidp: str = Field(title="매수호가", max_length=10)
    shnu_rsqn: str = Field(title="매수2 잔량", max_length=12)
    cntg_vol: str = Field(title="체결 거래량", max_length=18)
    antc_tr_pbmn: str = Field(title="체결 거래대금", max_length=18)
    total_askp_rsqn: str = Field(title="총 매도호가 잔량", max_length=12)
    total_bidp_rsqn: str = Field(title="총 매수호가 잔량", max_length=12)


class StockExpectedExecutionRiseDeclineTop(BaseModel, KisHttpBody):
    """국내주식 예상체결 상승/하락상위"""

    output: Sequence[StockExpectedExecutionRiseDeclineTopItem] = Field(default_factory=list)


class StockProprietaryTradingTopItem(BaseModel):
    data_rank: str = Field(title="데이터 순위", max_length=10)
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드", max_length=9)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=18)
    seln_cnqn_smtn: str = Field(title="매도 체결량 합계", max_length=18)
    shnu_cnqn_smtn: str = Field(title="매수2 체결량 합계", max_length=18)
    ntby_cnqn: str = Field(title="순매수 체결량", max_length=18)


class StockProprietaryTradingTop(BaseModel, KisHttpBody):
    """국내주식 당사매매종목 상위"""

    output: Sequence[StockProprietaryTradingTopItem] = Field(default_factory=list)


class StockNewHighLowApproachingTopItem(BaseModel):
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드", max_length=9)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    askp: str = Field(title="매도호가", max_length=10)
    askp_rsqn1: str = Field(title="매도호가 잔량1", max_length=12)
    bidp: str = Field(title="매수호가", max_length=10)
    bidp_rsqn1: str = Field(title="매수호가 잔량1", max_length=12)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    new_hgpr: str = Field(title="신 최고가", max_length=10)
    hprc_near_rate: str = Field(title="고가 근접 비율", max_length=84)
    new_lwpr: str = Field(title="신 최저가", max_length=10)
    lwpr_near_rate: str = Field(title="저가 근접 비율", max_length=84)
    stck_sdpr: str = Field(title="주식 기준가", max_length=10)


class StockNewHighLowApproachingTop(BaseModel, KisHttpBody):
    """국내주식 신고/신저근접종목 상위"""

    output: Sequence[StockNewHighLowApproachingTopItem] = Field(default_factory=list)

class StockDividendYieldTopItem(BaseModel):
    rank: str = Field(title="순위", max_length=4)
    sht_cd: str = Field(title="종목코드", max_length=9)
    isin_name: str = Field(title="종목명", max_length=40)
    record_date: str = Field(title="기준일", max_length=8)
    per_sto_divi_amt: str = Field(title="현금/주식배당금", max_length=12)
    divi_rate: str = Field(title="현금/주식배당률(%)", max_length=62)
    divi_kind: str = Field(title="배당종류", max_length=8)


class StockDividendYieldTop(BaseModel, KisHttpBody):
    """국내주식 배당률 상위"""

    output1: Sequence[StockDividendYieldTopItem] = Field(default_factory=list)

class StockLargeExecutionCountTopItem(BaseModel):
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드", max_length=9)
    data_rank: str = Field(title="데이터 순위", max_length=10)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    shnu_cntg_csnu: str = Field(title="매수2 체결 건수", max_length=10)
    seln_cntg_csnu: str = Field(title="매도 체결 건수", max_length=10)
    ntby_cnqn: str = Field(title="순매수 체결량", max_length=18)


class StockLargeExecutionCountTop(BaseModel, KisHttpBody):
    """국내주식 대량체결건수 상위"""

    output: Sequence[StockLargeExecutionCountTopItem] = Field(default_factory=list)

class StockCreditBalanceTopItem(BaseModel):
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드", max_length=9)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=18)
    ssts_cntg_qty: str = Field(title="공매도 체결 수량", max_length=12)
    ssts_vol_rlim: str = Field(title="공매도 거래량 비중", max_length=62)
    ssts_tr_pbmn: str = Field(title="공매도 거래 대금", max_length=18)
    ssts_tr_pbmn_rlim: str = Field(title="공매도 거래대금 비중", max_length=62)
    stnd_date1: str = Field(title="기준 일자1", max_length=8)
    stnd_date2: str = Field(title="기준 일자2", max_length=8)
    avrg_prc: str = Field(title="평균가격", max_length=11)


class StockCreditBalanceTop(BaseModel, KisHttpBody):
    """국내주식 신용잔고 상위"""

    output: Sequence[StockCreditBalanceTopItem] = Field(default_factory=list)


class StockShortSellingTopItem1(BaseModel):
    ovtm_untp_uplm_issu_cnt: str = Field(title="시간외 단일가 상한 종목 수", max_length=7)
    ovtm_untp_ascn_issu_cnt: str = Field(title="시간외 단일가 상승 종목 수", max_length=7)
    ovtm_untp_stnr_issu_cnt: str = Field(title="시간외 단일가 보합 종목 수", max_length=7)
    ovtm_untp_lslm_issu_cnt: str = Field(title="시간외 단일가 하한 종목 수", max_length=7)
    ovtm_untp_down_issu_cnt: str = Field(title="시간외 단일가 하락 종목 수", max_length=7)
    ovtm_untp_acml_vol: str = Field(title="시간외 단일가 누적 거래량", max_length=19)
    ovtm_untp_acml_tr_pbmn: str = Field(title="시간외 단일가 누적 거래대금", max_length=19)
    ovtm_untp_exch_vol: str = Field(title="시간외 단일가 거래소 거래량", max_length=18)
    ovtm_untp_exch_tr_pbmn: str = Field(title="시간외 단일가 거래소 거래대금", max_length=18)
    ovtm_untp_kosdaq_vol: str = Field(title="시간외 단일가 KOSDAQ 거래량", max_length=18)
    ovtm_untp_kosdaq_tr_pbmn: str = Field(title="시간외 단일가 KOSDAQ 거래대금", max_length=18)

class StockShortSellingTopItem2(BaseModel):
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드", max_length=9)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    ovtm_untp_prpr: str = Field(title="시간외 단일가 현재가", max_length=10)
    ovtm_untp_prdy_vrss: str = Field(title="시간외 단일가 전일 대비", max_length=10)
    ovtm_untp_prdy_vrss_sign: str = Field(title="시간외 단일가 전일 대비 부호", max_length=1)
    ovtm_untp_prdy_ctrt: str = Field(title="시간외 단일가 전일 대비율", max_length=82)
    ovtm_untp_askp1: str = Field(title="시간외 단일가 매도호가1", max_length=10)
    ovtm_untp_seln_rsqn: str = Field(title="시간외 단일가 매도 잔량", max_length=12)
    ovtm_untp_bidp1: str = Field(title="시간외 단일가 매수호가1", max_length=10)
    ovtm_untp_shnu_rsqn: str = Field(title="시간외 단일가 매수 잔량", max_length=12)
    ovtm_untp_vol: str = Field(title="시간외 단일가 거래량", max_length=18)
    ovtm_vrss_acml_vol_rlim: str = Field(title="시간외 대비 누적 거래량 비중", max_length=52)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    bidp: str = Field(title="매수호가", max_length=10)
    askp: str = Field(title="매도호가", max_length=10)

class StockShortSellingTop(BaseModel, KisHttpBody):
    """국내주식 공매도 상위종목"""

    output: Sequence[StockCreditBalanceTopItem] = Field(default_factory=list)

class StockAfterHoursFluctuationRankItem1(BaseModel):
    ovtm_untp_uplm_issu_cnt: str = Field(title="시간외 단일가 상한 종목 수", max_length=7)
    ovtm_untp_ascn_issu_cnt: str = Field(title="시간외 단일가 상승 종목 수", max_length=7)
    ovtm_untp_stnr_issu_cnt: str = Field(title="시간외 단일가 보합 종목 수", max_length=7)
    ovtm_untp_lslm_issu_cnt: str = Field(title="시간외 단일가 하한 종목 수", max_length=7)
    ovtm_untp_down_issu_cnt: str = Field(title="시간외 단일가 하락 종목 수", max_length=7)
    ovtm_untp_acml_vol: str = Field(title="시간외 단일가 누적 거래량", max_length=19)
    ovtm_untp_acml_tr_pbmn: str = Field(title="시간외 단일가 누적 거래대금", max_length=19)
    ovtm_untp_exch_vol: str = Field(title="시간외 단일가 거래소 거래량", max_length=18)
    ovtm_untp_exch_tr_pbmn: str = Field(title="시간외 단일가 거래소 거래대금", max_length=18)
    ovtm_untp_kosdaq_vol: str = Field(title="시간외 단일가 KOSDAQ 거래량", max_length=18)
    ovtm_untp_kosdaq_tr_pbmn: str = Field(title="시간외 단일가 KOSDAQ 거래대금", max_length=18)

class StockAfterHoursFluctuationRankItem2(BaseModel):
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드", max_length=9)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    ovtm_untp_prpr: str = Field(title="시간외 단일가 현재가", max_length=10)
    ovtm_untp_prdy_vrss: str = Field(title="시간외 단일가 전일 대비", max_length=10)
    ovtm_untp_prdy_vrss_sign: str = Field(title="시간외 단일가 전일 대비 부호", max_length=1)
    ovtm_untp_prdy_ctrt: str = Field(title="시간외 단일가 전일 대비율", max_length=82)
    ovtm_untp_askp1: str = Field(title="시간외 단일가 매도호가1", max_length=10)
    ovtm_untp_seln_rsqn: str = Field(title="시간외 단일가 매도 잔량", max_length=12)
    ovtm_untp_bidp1: str = Field(title="시간외 단일가 매수호가1", max_length=10)
    ovtm_untp_shnu_rsqn: str = Field(title="시간외 단일가 매수 잔량", max_length=12)
    ovtm_untp_vol: str = Field(title="시간외 단일가 거래량", max_length=18)
    ovtm_vrss_acml_vol_rlim: str = Field(title="시간외 대비 누적 거래량 비중", max_length=52)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    bidp: str = Field(title="매수호가", max_length=10)
    askp: str = Field(title="매도호가", max_length=10)

class StockAfterHoursFluctuationRank(BaseModel, KisHttpBody):
    """국내주식 시간외등락율순위"""

    output1: StockAfterHoursFluctuationRankItem1 = Field(title="응답상세1")
    output2: Sequence[StockAfterHoursFluctuationRankItem2] = Field(default_factory=list)


class StockAfterHoursVolumeRankItem1(BaseModel):
    ovtm_untp_exch_vol: str = Field(title="시간외 단일가 거래소 거래량", max_length=18)
    ovtm_untp_exch_tr_pbmn: str = Field(title="시간외 단일가 거래소 거래대금", max_length=18)
    ovtm_untp_kosdaq_vol: str = Field(title="시간외 단일가 KOSDAQ 거래량", max_length=18)
    ovtm_untp_kosdaq_tr_pbmn: str = Field(title="시간외 단일가 KOSDAQ 거래대금", max_length=18)

class StockAfterHoursVolumeRankItem2(BaseModel):
    stck_shrn_iscd: str = Field(title="주식 단축 종목코드", max_length=9)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    ovtm_untp_prpr: str = Field(title="시간외 단일가 현재가", max_length=10)
    ovtm_untp_prdy_vrss: str = Field(title="시간외 단일가 전일 대비", max_length=10)
    ovtm_untp_prdy_vrss_sign: str = Field(title="시간외 단일가 전일 대비 부호", max_length=1)
    ovtm_untp_prdy_ctrt: str = Field(title="시간외 단일가 전일 대비율", max_length=82)
    ovtm_untp_seln_rsqn: str = Field(title="시간외 단일가 매도 잔량", max_length=12)
    ovtm_untp_shnu_rsqn: str = Field(title="시간외 단일가 매수 잔량", max_length=12)
    ovtm_untp_vol: str = Field(title="시간외 단일가 거래량", max_length=18)
    ovtm_vrss_acml_vol_rlim: str = Field(title="시간외 대비 누적 거래량 비중", max_length=52)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    bidp: str = Field(title="매수호가", max_length=10)
    askp: str = Field(title="매도호가", max_length=10)


class StockAfterHoursVolumeRank(BaseModel, KisHttpBody):
    """국내주식 시간외거래량순위"""

    output1: StockAfterHoursVolumeRankItem1 = Field(title="응답상세1")
    output2: Sequence[StockAfterHoursVolumeRankItem2] = Field(default_factory=list)

class HtsInquiryTop20Item(BaseModel):
    mrkt_div_cls_code: str = Field(
        title="시장구분",
        max_length=9,
        description="J : 코스피, Q : 코스닥"
    )
    mksc_shrn_iscd: str = Field(
        title="종목코드",
        max_length=9
    )


class HtsInquiryTop20(BaseModel, KisHttpBody):
    """HTS조회상위20종목"""

    output1: Sequence[HtsInquiryTop20Item] = Field(default_factory=list)
