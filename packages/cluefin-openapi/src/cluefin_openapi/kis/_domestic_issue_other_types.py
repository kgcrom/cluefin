from typing import Sequence, Optional

from pydantic import BaseModel, Field

from cluefin_openapi.kis._model import KisHttpBody


class SectorCurrentIndexItem(BaseModel):
    bstp_nmix_prpr: str = Field(title="업종 지수 현재가", max_length=112)
    bstp_nmix_prdy_vrss: str = Field(title="업종 지수 전일 대비", max_length=112)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    bstp_nmix_prdy_ctrt: str = Field(title="업종 지수 전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    prdy_vol: str = Field(title="전일 거래량", max_length=18)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=18)
    prdy_tr_pbmn: str = Field(title="전일 거래 대금", max_length=18)
    bstp_nmix_oprc: str = Field(title="업종 지수 시가2", max_length=112)
    prdy_nmix_vrss_nmix_oprc: str = Field(title="전일 지수 대비 지수 시가2", max_length=112)
    oprc_vrss_prpr_sign: str = Field(title="시가2 대비 현재가 부호", max_length=1)
    bstp_nmix_oprc_prdy_ctrt: str = Field(title="업종 지수 시가2 전일 대비율", max_length=82)
    bstp_nmix_hgpr: str = Field(title="업종 지수 최고가", max_length=112)
    prdy_nmix_vrss_nmix_hgpr: str = Field(title="전일 지수 대비 지수 최고가", max_length=112)
    hgpr_vrss_prpr_sign: str = Field(title="최고가 대비 현재가 부호", max_length=1)
    bstp_nmix_hgpr_prdy_ctrt: str = Field(title="업종 지수 최고가 전일 대비율", max_length=82)
    bstp_nmix_lwpr: str = Field(title="업종 지수 최저가", max_length=112)
    prdy_clpr_vrss_lwpr: str = Field(title="전일 종가 대비 최저가", max_length=10)
    lwpr_vrss_prpr_sign: str = Field(title="최저가 대비 현재가 부호", max_length=1)
    prdy_clpr_vrss_lwpr_rate: str = Field(title="전일 종가 대비 최저가 비율", max_length=84)
    ascn_issu_cnt: str = Field(title="상승 종목 수", max_length=7)
    uplm_issu_cnt: str = Field(title="상한 종목 수", max_length=7)
    stnr_issu_cnt: str = Field(title="보합 종목 수", max_length=7)
    down_issu_cnt: str = Field(title="하락 종목 수", max_length=7)
    lslm_issu_cnt: str = Field(title="하한 종목 수", max_length=7)
    dryy_bstp_nmix_hgpr: str = Field(title="연중업종지수최고가", max_length=112)
    dryy_hgpr_vrss_prpr_rate: str = Field(title="연중 최고가 대비 현재가 비율", max_length=84)
    dryy_bstp_nmix_hgpr_date: str = Field(title="연중업종지수최고가일자", max_length=8)
    dryy_bstp_nmix_lwpr: str = Field(title="연중업종지수최저가", max_length=112)
    dryy_lwpr_vrss_prpr_rate: str = Field(title="연중 최저가 대비 현재가 비율", max_length=84)
    dryy_bstp_nmix_lwpr_date: str = Field(title="연중업종지수최저가일자", max_length=8)
    total_askp_rsqn: str = Field(title="총 매도호가 잔량", max_length=12)
    total_bidp_rsqn: str = Field(title="총 매수호가 잔량", max_length=12)
    seln_rsqn_rate: str = Field(title="매도 잔량 비율", max_length=84)
    shnu_rsqn_rate: str = Field(title="매수2 잔량 비율", max_length=84)
    ntby_rsqn: str = Field(title="순매수 잔량", max_length=12)

class SectorCurrentIndex(BaseModel, KisHttpBody):
    """국내업종 현재지수 응답"""
    output: SectorCurrentIndexItem = Field(title="응답상세")


class SectorDailyIndexItem1(BaseModel):
    bstp_nmix_prpr: str = Field(title="업종 지수 현재가", max_length=112)
    bstp_nmix_prdy_vrss: str = Field(title="업종 지수 전일 대비", max_length=112)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    bstp_nmix_prdy_ctrt: str = Field(title="업종 지수 전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=18)
    bstp_nmix_oprc: str = Field(title="업종 지수 시가2", max_length=112)
    bstp_nmix_hgpr: str = Field(title="업종 지수 최고가", max_length=112)
    bstp_nmix_lwpr: str = Field(title="업종 지수 최저가", max_length=112)
    prdy_vol: str = Field(title="전일 거래량", max_length=18)
    ascn_issu_cnt: str = Field(title="상승 종목 수", max_length=7)
    down_issu_cnt: str = Field(title="하락 종목 수", max_length=7)
    stnr_issu_cnt: str = Field(title="보합 종목 수", max_length=7)
    uplm_issu_cnt: str = Field(title="상한 종목 수", max_length=7)
    lslm_issu_cnt: str = Field(title="하한 종목 수", max_length=7)
    prdy_tr_pbmn: str = Field(title="전일 거래 대금", max_length=18)
    dryy_bstp_nmix_hgpr_date: str = Field(title="연중업종지수최고가일자", max_length=8)
    dryy_bstp_nmix_hgpr: str = Field(title="연중업종지수최고가", max_length=112)
    dryy_bstp_nmix_lwpr: str = Field(title="연중업종지수최저가", max_length=112)
    dryy_bstp_nmix_lwpr_date: str = Field(title="연중업종지수최저가일자", max_length=8)


class SectorDailyIndexItem2(BaseModel):
    stck_bsop_date: str = Field(title="주식 영업 일자", max_length=8)
    bstp_nmix_prpr: str = Field(title="업종 지수 현재가", max_length=112)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    bstp_nmix_prdy_vrss: str = Field(title="업종 지수 전일 대비", max_length=112)
    bstp_nmix_prdy_ctrt: str = Field(title="업종 지수 전일 대비율", max_length=82)
    bstp_nmix_oprc: str = Field(title="업종 지수 시가2", max_length=112)
    bstp_nmix_hgpr: str = Field(title="업종 지수 최고가", max_length=112)
    bstp_nmix_lwpr: str = Field(title="업종 지수 최저가", max_length=112)
    acml_vol_rlim: str = Field(title="누적 거래량 비중", max_length=72)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=18)
    invt_new_psdg: str = Field(title="투자 신 심리도", max_length=112)
    d20_dsrt: str = Field(title="20일 이격도", max_length=112)

class SectorDailyIndex(BaseModel, KisHttpBody):
    """국내업종 일자별지수 응답"""

    output1: SectorDailyIndexItem1 = Field(title="응답상세1")
    output2: Sequence[SectorDailyIndexItem2] = Field(default_factory=list)


class SectorTimeIndexSecondItem(BaseModel):
    stck_cntg_hour: str = Field(title="주식 체결 시간", max_length=6)
    bstp_nmix_prpr: str = Field(title="업종 지수 현재가", max_length=112)
    bstp_nmix_prdy_vrss: str = Field(title="업종 지수 전일 대비", max_length=112)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    bstp_nmix_prdy_ctrt: str = Field(title="업종 지수 전일 대비율", max_length=82)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=18)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    cntg_vol: str = Field(title="체결 거래량", max_length=18)

class SectorTimeIndexSecond(BaseModel, KisHttpBody):
    """국내업종 시간별지수(초) 응답"""
    output: Sequence[SectorTimeIndexSecondItem] = Field(default_factory=list)


class SectorTimeIndexMinuteItem(BaseModel):
    bsop_hour: str = Field(title="영업 시간", max_length=6)
    bstp_nmix_prpr: str = Field(title="업종 지수 현재가", max_length=112)
    bstp_nmix_prdy_vrss: str = Field(title="업종 지수 전일 대비", max_length=112)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    bstp_nmix_prdy_ctrt: str = Field(title="업종 지수 전일 대비율", max_length=82)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=18)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    cntg_vol: str = Field(title="체결 거래량", max_length=18)

class SectorTimeIndexMinute(BaseModel, KisHttpBody):
    """국내업종 시간별지수(분) 응답"""
    output: Sequence[SectorTimeIndexMinuteItem] = Field(default_factory=list)


class SectorMinuteInquiryItem1(BaseModel):
    bstp_nmix_prdy_vrss: str = Field(title="업종 지수 전일 대비", max_length=112)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    bstp_nmix_prdy_ctrt: str = Field(title="업종 지수 전일 대비율", max_length=82)
    prdy_nmix: str = Field(title="전일 지수", max_length=112)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=18)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    bstp_nmix_prpr: str = Field(title="업종 지수 현재가", max_length=112)
    bstp_cls_code: str = Field(title="업종 구분 코드", max_length=4)
    prdy_vol: str = Field(title="전일 거래량", max_length=18)
    bstp_nmix_oprc: str = Field(title="업종 지수 시가2", max_length=112)
    bstp_nmix_hgpr: str = Field(title="업종 지수 최고가", max_length=112)
    bstp_nmix_lwpr: str = Field(title="업종 지수 최저가", max_length=112)
    futs_prdy_oprc: str = Field(title="선물 전일 시가", max_length=112)
    futs_prdy_hgpr: str = Field(title="선물 전일 최고가", max_length=112)
    futs_prdy_lwpr: str = Field(title="선물 전일 최저가", max_length=112)


class SectorMinuteInquiryItem2(BaseModel):
    stck_bsop_date: str = Field(title="주식 영업 일자", max_length=8)
    stck_cntg_hour: str = Field(title="주식 체결 시간", max_length=6)
    bstp_nmix_prpr: str = Field(title="업종 지수 현재가", max_length=112)
    bstp_nmix_oprc: str = Field(title="업종 지수 시가2", max_length=112)
    bstp_nmix_hgpr: str = Field(title="업종 지수 최고가", max_length=112)
    bstp_nmix_lwpr: str = Field(title="업종 지수 최저가", max_length=112)
    cntg_vol: str = Field(title="체결 거래량", max_length=18)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=18)

class SectorMinuteInquiry(BaseModel, KisHttpBody):
    """업종 분봉조회 응답"""
    output1: SectorMinuteInquiryItem1 = Field(title="응답상세1")
    output2: Sequence[SectorMinuteInquiryItem2] = Field(default_factory=list)


class SectorPeriodQuoteItem1(BaseModel):
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    bstp_nmix_prdy_ctrt: str = Field(title="업종 지수 전일 대비율", max_length=82)
    prdy_nmix: str = Field(title="전일 지수", max_length=112)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=18)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    bstp_nmix_prpr: str = Field(title="업종 지수 현재가", max_length=112)
    bstp_cls_code: str = Field(title="업종 구분 코드", max_length=4)
    prdy_vol: str = Field(title="전일 거래량", max_length=18)
    bstp_nmix_oprc: str = Field(title="업종 지수 시가2", max_length=112)
    bstp_nmix_hgpr: str = Field(title="업종 지수 최고가", max_length=112)
    bstp_nmix_lwpr: str = Field(title="업종 지수 최저가", max_length=112)
    futs_prdy_oprc: str = Field(title="선물 전일 시가", max_length=112)
    futs_prdy_hgpr: str = Field(title="선물 전일 최고가", max_length=112)
    futs_prdy_lwpr: str = Field(title="선물 전일 최저가", max_length=112)


class SectorPeriodQuoteItem2(BaseModel):
    stck_bsop_date: str = Field(title="주식 영업 일자", max_length=8)
    bstp_nmix_prpr: str = Field(title="업종 지수 현재가", max_length=112)
    bstp_nmix_oprc: str = Field(title="업종 지수 시가2", max_length=112)
    bstp_nmix_hgpr: str = Field(title="업종 지수 최고가", max_length=112)
    bstp_nmix_lwpr: str = Field(title="업종 지수 최저가", max_length=112)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=18)
    mod_yn: str = Field(title="변경 여부", max_length=1)

class SectorPeriodQuote(BaseModel, KisHttpBody):
    """국내주식업종기간별시세(일/주/월/년) 응답"""
    output1: SectorPeriodQuoteItem1 = Field(title="응답상세1")
    output2: Sequence[SectorPeriodQuoteItem2] = Field(default_factory=list)


class SectorAllQuoteByCategoryItem1(BaseModel):
    bstp_nmix_prpr: str = Field(title="업종 지수 현재가", max_length=112)
    bstp_nmix_prdy_vrss: str = Field(title="업종 지수 전일 대비", max_length=112)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    bstp_nmix_prdy_ctrt: str = Field(title="업종 지수 전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=18)
    bstp_nmix_oprc: str = Field(title="업종 지수 시가2", max_length=112)
    bstp_nmix_hgpr: str = Field(title="업종 지수 최고가", max_length=112)
    bstp_nmix_lwpr: str = Field(title="업종 지수 최저가", max_length=112)
    prdy_vol: str = Field(title="전일 거래량", max_length=18)
    ascn_issu_cnt: str = Field(title="상승 종목 수", max_length=7)
    down_issu_cnt: str = Field(title="하락 종목 수", max_length=7)
    stnr_issu_cnt: str = Field(title="보합 종목 수", max_length=7)
    uplm_issu_cnt: str = Field(title="상한 종목 수", max_length=7)
    lslm_issu_cnt: str = Field(title="하한 종목 수", max_length=7)
    prdy_tr_pbmn: str = Field(title="전일 거래 대금", max_length=18)
    dryy_bstp_nmix_hgpr_date: str = Field(title="연중업종지수최고가일자", max_length=8)
    dryy_bstp_nmix_hgpr: str = Field(title="연중업종지수최고가", max_length=112)
    dryy_bstp_nmix_lwpr: str = Field(title="연중업종지수최저가", max_length=112)
    dryy_bstp_nmix_lwpr_date: str = Field(title="연중업종지수최저가일자", max_length=8)


class SectorAllQuoteByCategoryItem2(BaseModel):
    bstp_cls_code: str = Field(title="업종 구분 코드", max_length=4)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    bstp_nmix_prpr: str = Field(title="업종 지수 현재가", max_length=112)
    bstp_nmix_prdy_vrss: str = Field(title="업종 지수 전일 대비", max_length=112)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    bstp_nmix_prdy_ctrt: str = Field(title="업종 지수 전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=18)
    acml_vol_rlim: str = Field(title="누적 거래량 비중", max_length=72)
    acml_tr_pbmn_rlim: str = Field(title="누적 거래 대금 비중", max_length=72)

class SectorAllQuoteByCategory(BaseModel, KisHttpBody):
    """국내업종 구분별전체시세 응답"""

    output1: SectorAllQuoteByCategoryItem1 = Field(title="응답상세1")
    output2: Sequence[SectorAllQuoteByCategoryItem2] = Field(default_factory=list)


class ExpectedIndexTrendItem(BaseModel):
    stck_cntg_hour: str = Field(title="주식 단축 종목코드", max_length=6)
    bstp_nmix_prpr: str = Field(title="HTS 한글 종목명", max_length=112)
    prdy_vrss_sign: str = Field(title="주식 현재가", max_length=1)
    bstp_nmix_prdy_vrss: str = Field(title="전일 대비", max_length=112)
    prdy_ctrt: str = Field(title="전일 대비 부호", max_length=82)
    acml_vol: str = Field(title="전일 대비율", max_length=18)
    acml_tr_pbmn: str = Field(title="기준가 대비 현재가", max_length=18)

class ExpectedIndexTrend(BaseModel, KisHttpBody):
    """국내주식 예상체결지수 추이 응답"""
    output: Sequence[ExpectedIndexTrendItem] = Field(default_factory=list)


class ExpectedIndexAllItem1(BaseModel):
    bstp_nmix_prpr: str = Field(title="업종 지수 현재가", max_length=112)
    bstp_nmix_prdy_vrss: str = Field(title="업종 지수 전일 대비", max_length=112)
    # TODO(typo): 문서에는 required Y, 실제로는 Optional
    prdy_vrss_sign: Optional[str] = Field(default=None, title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    ascn_issu_cnt: str = Field(title="상승 종목 수", max_length=7)
    down_issu_cnt: str = Field(title="하락 종목 수", max_length=7)
    stnr_issu_cnt: str = Field(title="보합 종목 수", max_length=7)
    # TODO(typo): 문서에는 required Y, 실제로는 Optional
    bstp_cls_code: Optional[str] = Field(default=None, title="업종 구분 코드", max_length=4)


class ExpectedIndexAllItem2(BaseModel):
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    bstp_nmix_prpr: str = Field(title="업종 지수 현재가", max_length=112)
    bstp_nmix_prdy_vrss: str = Field(title="업종 지수 전일 대비", max_length=112)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    bstp_nmix_prdy_ctrt: str = Field(title="업종 지수 전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    nmix_sdpr: str = Field(title="지수 기준가", max_length=112)
    ascn_issu_cnt: str = Field(title="상승 종목 수", max_length=7)
    stnr_issu_cnt: str = Field(title="보합 종목 수", max_length=7)
    down_issu_cnt: str = Field(title="하락 종목 수", max_length=7)

class ExpectedIndexAll(BaseModel, KisHttpBody):
    """국내주식 예상체결 전체지수 응답"""
    output1: ExpectedIndexAllItem1 = Field(title="응답상세1")
    output2: Sequence[ExpectedIndexAllItem2] = Field(default_factory=list)


class VolatilityInterruptionStatusItem(BaseModel):
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드", max_length=9)
    vi_cls_code: str = Field(title="VI발동상태", max_length=1, description="Y: 발동 / N: 해제")
    bsop_date: str = Field(title="영업 일자", max_length=8)
    cntg_vi_hour: str = Field(title="VI발동시간", max_length=6, description="VI발동시간")
    vi_cncl_hour: str = Field(title="VI해제시간", max_length=6, description="VI해제시간")
    vi_kind_code: str = Field(title="VI종류코드", max_length=1, description="1:정적 2:동적 3:정적&동적")
    vi_prc: str = Field(title="VI발동가격", max_length=10)
    vi_stnd_prc: str = Field(title="정적VI발동기준가격", max_length=10)
    vi_dprt: str = Field(title="정적VI발동괴리율", max_length=82, description="%")
    vi_dmc_stnd_prc: str = Field(title="동적VI발동기준가격", max_length=10)
    vi_dmc_dprt: str = Field(title="동적VI발동괴리율", max_length=82, description="%")
    vi_count: str = Field(title="VI발동횟수", max_length=7)

class VolatilityInterruptionStatus(BaseModel, KisHttpBody):
    """변동성완화장치(VI) 현황 응답"""
    # TODO(typo): 문서에는 object, 실제로는 list
    output: Sequence[VolatilityInterruptionStatusItem] = Field(default_factory=list)


class InterestRateSummaryItem1(BaseModel):
    bcdt_code: str = Field(title="자료코드", max_length=5)
    hts_kor_isnm: str = Field(title="HTS한글종목명", max_length=40)
    bond_mnrt_prpr: str = Field(title="채권금리현재가", max_length=114)
    prdy_vrss_sign: str = Field(title="전일대비부호", max_length=1)
    bond_mnrt_prdy_vrss: str = Field(title="채권금리전일대비", max_length=114)
    prdy_ctrt: str = Field(title="전일대비율", max_length=82)
    stck_bsop_date: str = Field(title="주식영업일자", max_length=8)


class InterestRateSummaryItem2(BaseModel):
    bcdt_code: str = Field(title="자료코드", max_length=5)
    hts_kor_isnm: str = Field(title="HTS한글종목명", max_length=40)
    bond_mnrt_prpr: str = Field(title="채권금리현재가", max_length=114)
    prdy_vrss_sign: str = Field(title="전일대비부호", max_length=1)
    bond_mnrt_prdy_vrss: str = Field(title="채권금리전일대비", max_length=114)
    bstp_nmix_prdy_ctrt: str = Field(title="업종지수전일대비율", max_length=82)
    stck_bsop_date: str = Field(title="주식영업일자", max_length=8)

class InterestRateSummary(BaseModel, KisHttpBody):
    """금리 종합(국내채권/금리) 응답"""
    # TODO(typo): 문서에는 object, 실제로는 list
    output1: Sequence[InterestRateSummaryItem1] = Field(default_factory=list)
    output2: Sequence[InterestRateSummaryItem2] = Field(default_factory=list)

class MarketAnnouncementScheduleItem(BaseModel):
    cntt_usiq_srno: str = Field(title="내용 조회용 일련번호", max_length=20)
    news_ofer_entp_code: str = Field(title="뉴스 제공 업체 코드", max_length=1, description="'2' /* 한경 news */ '3' /* 사용안함 */ '4' /* 이데일리 */ '5' /* 머니투데이 */ '6' /* 연합뉴스 */ '7' /* 인포스탁 */ '8' /* 아시아경제 */ '9' /* 뉴스핌 */ 'A' /* 매일경제 */ 'B' /* 헤럴드경제 */ 'C' /* 파이낸셜 */ 'D' /* 이투데이 */ 'F' /* 장내공시 */ 'G' /* 코스닥공시 */ 'H' /* 프리보드공시*/ 'I' /* 기타공시 */ 'N' /* 코넥스공시 */ 'J' /* 동향 */ /* 'L' 리서치 */ 'K' /* 청약안내 전송 */ 'M' /* 타사 추천종목 */ 'O' /* edaily fx */ 'U' /* 서울 경제 */ 'V' /* 조선 경제 */ 'X' /* CEO스코어 */ 'Y' /* 이프렌드 Air 뉴스 */ 'Z' /* 인베스트조선 */ 'd' /* NSP통신 */")
    data_dt: str = Field(title="작성일자", max_length=8)
    data_tm: str = Field(title="작성시간", max_length=6)
    hts_pbnt_titl_cntt: str = Field(title="HTS 공시 제목 내용", max_length=400)
    news_lrdv_code: str = Field(title="뉴스 대구분", max_length=8, description="1:0:종합 1:FGHIN:공시 2:F:거래소 3:01:수시공시 3:02:공정공시 3:03:시장조치 3:04:신고사항 3:05:정기공시 3:06:특수공시 3:07:발행공시 3:08:지분공시 3:09:워런트공시 3:10:의결권행사공시 3:11:공정위공시 3:12:선물시장공시 3:A1:시장조치안내 3:A2:상장안내 3:A3:안내사항 3:A4:투자유의사항 3:A5:수익증권 3:A6:투자자참고사항 3:A7:뮤츄얼펀드 2:G:코스닥 3:01:수시공시 3:02:공정공시 3:03:시장조치 3:04:신고사항 3:05:정기공시 3:06:특수공시 3:07:발행공시 3:08:지분공시 3:09:워런트공시 3:10:의결권행사공시 3:11:공정위공시 3:12:선물시장공시 3:A1:시장조치안내 3:A2:상장안내 3:A3:안내사항 3:A4:투자유의사항 3:A5:수익증권 3:A6:투자자참고사항 3:A7:뮤츄얼펀드 2:N:코넥스 3:01:수시공시 3:02:공정공시 3:03:시장조치 3:04:신고사항 3:05:정기공시 3:06:특수공시 3:07:발행공시 3:08:지분공시 3:09:워런트공시 3:10:의결권행사공시 3:11:공정위공시 3:12:선물시장공시 3:A1:시장조치안내 3:A2:상장안내 3:A3:안내사항 3:A4:투자유의사항 3:A5:수익증권 3:A6:투자자참고사항 3:A7:뮤츄얼펀드 2:H:K-OTC 2:I:기타 1:6:연합뉴스 3:01:정치 3:02:경제 3:03:증권/금융 3:04:산업 3:05:사회 3:06:사건사고 3:07:문화 3:08:생활건강 3:09:IT. 과학 3:10:북한 3:11:국제 3:12:스포츠 3:13:기타 1:2:한경 3:01:증권 3:04:경제 3:03:부동산 3:07:IT/과학 3:08:정치 3:09:국제 3:10:사회 3:11:생활/문화 3:00:오피니언 3:12:스포츠 3:20:연예 3:18:보도자료 1:A:매경 3:01:경제 3:02:금융 3:03:산업/기업 3:04:중기/벤쳐/과기 3:05:증권 3:06:부동산 3:07:정치 3:08:사회 3:09:인물/동정 3:10:국제 3:11:문화 3:12:레저/스포츠 3:13:사설/칼럼 3:14:기획/분석 3:15:섹션 3:16:English News 3:17:매경이코노미 3:18:mbn 3:90:기타 1:4:이데일리 3:B1:채권시황 3:B2:신종채권 3:F1:외환시황 3:G1:보도자료 3:H1:정책뉴스 3:H2:금융뉴스 3:H3:금융금리/수익율 3:I1:IPO뉴스 3:J1:뉴욕 3:J2:아시아/유럽 3:J3:월드마켓 3:J4:국제기업/산업 3:J5:경제흐름 3:L1:기업뉴스 3:L2:IT 3:L3:벤처 3:L4:e3비즈월드 3:S1:주식시황 3:S2:거래소 3:S3:코스닥&장외 3:S4:루머 3:S5:증권가 1:5:머니투데이 3:A01:주식 3:A02:선물옵션 3:A05:해외증시 3:A06:외환 3:A07:채권 3:A08:펀드 3:B01:경제 3:B02:산업 3:B03:정보과학 3:B04:국제 3:B05:금융보험 3:B07:부동산 3:B08:성공학 3:B09:재테크 3:B10:바이오 1:9:뉴스핌 3:01:주식 3:02:채권 3:03:외환 3:04:국제 3:05:금융/제테크 3:06:산업 3:07:경제 3:08:광장 3:09:전문가기고 3:90:기타 1:8:아시아경제 3:A0:증권 3:B0:금융 3:C0:부동산 3:D0:산업 3:E0:경제 3:F0:정치,사회 3:G0:사설,칼럼 3:H0:인사,동정,부고 3:I0:루머&팩트 3:J0:국내뉴스 3:K0:아시아시각 3:L0:골프 3:M0:모닝브리핑 3:N0:연예 3:10:국제 3:20:중국 3:30:인도 3:40:일본 3:50:이머징마켓 1:B:헤럴드경제 3:01:뉴스 3:02:기업 3:03:재테크 3:04:스타 3:05:문화 3:90:기타 1:C:파이낸셜 3:01:증권 3:02:금융 3:03:부동산 3:04:산업 3:05:경제 3:06:정보과학 3:07:유통 3:08:국제 3:09:정치 3:10:전국/사회 3:11:문화 3:12:스포츠 3:13:교육 3:14:피플 3:15:사설/컬럼 3:16:기획/연재 3:17:fn재테크 3:18:광고 3:90:기타 1:D:이투데이 3:21:증권 3:51:금융 3:22:정치/정책 3:31:글로벌 3:23:산업 3:24:부동산 3:26:라이프 3:25:칼럼/인물 3:41:연예/스포츠 3:90:기타 1:U:서울경제 3:31:증권 3:32:부동산 3:33:경제/금융 3:34:산업/기업 3:35:IT/과학 3:36:정치 3:37:사회 3:38:국제 3:39:칼럼 3:3A:인사/동정/부음 3:3B:문화/건강/레저 3:3C:골프/스포츠 1:V:조선경제i 3:1:뉴스 3:2:Market 3:4:부동산 3:6:글로벌경제 3:8:위클리비즈 3:B:자동차 3:C:녹색BIZ 1:7:인포스탁 3:01:거래소종목 3:02:코스닥종목 3:03:해외증시 3:04:선물동향 3:00:기타 1:X:CEO스코어 3:01:경제 3:02:산업 3:03:금융 3:04:공기업 3:05:전자 3:06:통신 3:07:게임,인터넷 3:08:자동차 3:09:조선,철강 3:10:식음료 3:11:유통 3:12:건설 3:13:제약 3:14:화학,에너지 3:15:생활산업 3:16:기타 1:S:컨슈머타임스 3:01:종합 3:02:파이낸셜컨슈머 3:03:컨슈머리뷰 3:04:정치,사회 3:05:스포츠,연예 3:06:컨슈머뷰티 3:07:오피니언 3:09:기타 1:Z:인베스트조선 3:01:증권/금융 1:d:NSP통신 3:11:IT/과학 3:12:금융/증권 3:13:부동산 3:14:자동차 3:15:연예/문화 3:16:생활경제 3:17:물류/유통 3:18:인사/동정 3:19:정치/사회 3:20:기업 3:21:의학/건강 3:23:신상품/리뷰 3:24:해명/반론 1:a:IRGO 3:10:IR정보 3:20:IR일정 3:50:IR FOCUS 1:Y:eFriend Air 3:01:종목상담 3:02:VOD 1:J:동향 1:L:한투리서치")
    dorg: str = Field(title="자료원", max_length=20)
    iscd1: str = Field(title="종목 코드1", max_length=9)
    iscd2: str = Field(title="종목 코드2", max_length=9)
    iscd3: str = Field(title="종목 코드3", max_length=9)
    iscd4: str = Field(title="종목 코드4", max_length=9)
    iscd5: str = Field(title="종목 코드5", max_length=9)

class MarketAnnouncementSchedule(BaseModel, KisHttpBody):
    """종합 시황/공시(제목) 응답"""
    # TODO(typo): 문서에는 object, 실제로는 list
    output: Sequence[MarketAnnouncementScheduleItem] = Field(default_factory=list)

class HolidayInquiryItem(BaseModel):
    bass_dt: str = Field(title="기준일자", max_length=8, description="기준일자(YYYYMMDD)")
    wday_dvsn_cd: str = Field(title="요일구분코드", max_length=2, description="01:일요일, 02:월요일, 03:화요일, 04:수요일, 05:목요일, 06:금요일, 07:토요일")
    bzdy_yn: str = Field(title="영업일여부", max_length=1, description="Y/N 금융기관이 업무를 하는 날")
    tr_day_yn: str = Field(title="거래일여부", max_length=1, description="Y/N 증권 업무가 가능한 날(입출금, 이체 등의 업무 포함)")
    opnd_yn: str = Field(title="개장일여부", max_length=1, description="Y/N 주식시장이 개장되는 날 * 주문을 넣고자 할 경우 개장일여부(opnd_yn)를 사용")
    sttl_day_yn: str = Field(title="결제일여부", max_length=1, description="Y/N 주식 거래에서 실제로 주식을 인수하고 돈을 지불하는 날")

class HolidayInquiry(BaseModel, KisHttpBody):
    """국내휴장일조회 응답"""
    # TODO(typo): 문서에는 object, 실제로는 list
    output: Sequence[HolidayInquiryItem] = Field(default_factory=list)

class FuturesBusinessDayInquiryItem(BaseModel):
    date1: str = Field(title="영업일1", max_length=8)
    date2: str = Field(title="영업일2", max_length=8)
    date3: str = Field(title="영업일3", max_length=8, description="영업일 당일")
    date4: str = Field(title="영업일4", max_length=8)
    date5: str = Field(title="영업일5", max_length=8)
    today: str = Field(title="오늘일자", max_length=8)
    time: str = Field(title="현재시간", max_length=6)
    s_time: str = Field(title="장시작시간", max_length=6)
    e_time: str = Field(title="장마감시간", max_length=6)

class FuturesBusinessDayInquiry(BaseModel, KisHttpBody):
    """국내선물 영업일조회 응답"""
    output: Sequence[FuturesBusinessDayInquiryItem] = Field(default_factory=list)
