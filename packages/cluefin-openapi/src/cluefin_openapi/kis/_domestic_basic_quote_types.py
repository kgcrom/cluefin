from typing import Optional, Sequence, Literal

from pydantic import BaseModel, Field

from cluefin_openapi.kis._model import KisHttpBody


class DomesticStockCurrentPriceItem(BaseModel):
    """국내주식 현재가 시세 아이템"""

    iscd_stat_cls_code: str = Field(title="종목 상태 구분 코드", max_length=3)
    marg_rate: str = Field(title="증거금 비율", max_length=84)
    rprs_mrkt_kor_name: str = Field(title="대표 시장 한글명", max_length=40)
    new_hgpr_lwpr_cls_code: str = Field(title="신 고가 저가 구분 코드", max_length=10)
    bstp_kor_isnm: str = Field(title="업종 한글 종목명", max_length=40)
    temp_stop_yn: str = Field(title="임시 정지 여부", max_length=1)
    oprc_rang_cont_yn: str = Field(title="시가 범위 연장 여부", max_length=1)
    clpr_rang_cont_yn: str = Field(title="종가 범위 연장 여부", max_length=1)
    crdt_able_yn: str = Field(title="신용 가능 여부", max_length=1)
    grmn_rate_cls_code: str = Field(title="보증금 비율 구분 코드", max_length=3)
    elw_pblc_yn: str = Field(title="ELW 발행 여부", max_length=1)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=18)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    prdy_vrss_vol_rate: str = Field(title="전일 대비 거래량 비율", max_length=84)
    stck_oprc: str = Field(title="주식 시가2", max_length=10)
    stck_hgpr: str = Field(title="주식 최고가", max_length=10)
    stck_lwpr: str = Field(title="주식 최저가", max_length=10)
    stck_mxpr: str = Field(title="주식 상한가", max_length=10)
    stck_llam: str = Field(title="주식 하한가", max_length=10)
    stck_sdpr: str = Field(title="주식 기준가", max_length=10)
    wghn_avrg_stck_prc: str = Field(title="가중 평균 주식 가격", max_length=192)
    hts_frgn_ehrt: str = Field(title="HTS 외국인 소진율", max_length=82)
    frgn_ntby_qty: str = Field(title="외국인 순매수 수량", max_length=12)
    pgtr_ntby_qty: str = Field(title="프로그램매매 순매수 수량", max_length=18)
    pvt_scnd_dmrs_prc: str = Field(title="피벗 2차 디저항 가격", max_length=10)
    pvt_frst_dmrs_prc: str = Field(title="피벗 1차 디저항 가격", max_length=10)
    pvt_pont_val: str = Field(title="피벗 포인트 값", max_length=10)
    pvt_frst_dmsp_prc: str = Field(title="피벗 1차 디지지 가격", max_length=10)
    pvt_scnd_dmsp_prc: str = Field(title="피벗 2차 디지지 가격", max_length=10)
    dmrs_val: str = Field(title="디저항 값", max_length=10)
    dmsp_val: str = Field(title="디지지 값", max_length=10)
    cpfn: str = Field(title="자본금", max_length=22)
    rstc_wdth_prc: str = Field(title="제한 폭 가격", max_length=10)
    stck_fcam: str = Field(title="주식 액면가", max_length=11)
    stck_sspr: str = Field(title="주식 대용가", max_length=10)
    aspr_unit: str = Field(title="호가단위", max_length=10)
    hts_deal_qty_unit_val: str = Field(title="HTS 매매 수량 단위 값", max_length=10)
    lstn_stcn: str = Field(title="상장 주수", max_length=18)
    hts_avls: str = Field(title="HTS 시가총액", max_length=18)
    per: str = Field(title="PER", max_length=82)
    pbr: str = Field(title="PBR", max_length=82)
    stac_month: str = Field(title="결산 월", max_length=2)
    vol_tnrt: str = Field(title="거래량 회전율", max_length=82)
    eps: str = Field(title="EPS", max_length=112)
    bps: str = Field(title="BPS", max_length=112)
    d250_hgpr: str = Field(title="250일 최고가", max_length=10)
    d250_hgpr_date: str = Field(title="250일 최고가 일자", max_length=8)
    d250_hgpr_vrss_prpr_rate: str = Field(title="250일 최고가 대비 현재가 비율", max_length=84)
    d250_lwpr: str = Field(title="250일 최저가", max_length=10)
    d250_lwpr_date: str = Field(title="250일 최저가 일자", max_length=8)
    d250_lwpr_vrss_prpr_rate: str = Field(title="250일 최저가 대비 현재가 비율", max_length=84)
    stck_dryy_hgpr: str = Field(title="주식 연중 최고가", max_length=10)
    dryy_hgpr_vrss_prpr_rate: str = Field(title="연중 최고가 대비 현재가 비율", max_length=84)
    dryy_hgpr_date: str = Field(title="연중 최고가 일자", max_length=8)
    stck_dryy_lwpr: str = Field(title="주식 연중 최저가", max_length=10)
    dryy_lwpr_vrss_prpr_rate: str = Field(title="연중 최저가 대비 현재가 비율", max_length=84)
    dryy_lwpr_date: str = Field(title="연중 최저가 일자", max_length=8)
    w52_hgpr: str = Field(title="52주일 최고가", max_length=10)
    w52_hgpr_vrss_prpr_ctrt: str = Field(title="52주일 최고가 대비 현재가 대비", max_length=82)
    w52_hgpr_date: str = Field(title="52주일 최고가 일자", max_length=8)
    w52_lwpr: str = Field(title="52주일 최저가", max_length=10)
    w52_lwpr_vrss_prpr_ctrt: str = Field(title="52주일 최저가 대비 현재가 대비", max_length=82)
    w52_lwpr_date: str = Field(title="52주일 최저가 일자", max_length=8)
    whol_loan_rmnd_rate: str = Field(title="전체 융자 잔고 비율", max_length=84)
    ssts_yn: str = Field(title="공매도가능여부", max_length=1)
    stck_shrn_iscd: str = Field(title="주식 단축 종목코드", max_length=9)
    fcam_cnnm: str = Field(title="액면가 통화명", max_length=20)
    cpfn_cnnm: str = Field(title="자본금 통화명", max_length=20)
    # TODO(typo) 존재하지 않는 필드임
    # apprch_rate: str = Field(title="접근도", max_length=112)
    frgn_hldn_qty: str = Field(title="외국인 보유 수량", max_length=18)
    vi_cls_code: str = Field(title="VI적용구분코드", max_length=1)
    ovtm_vi_cls_code: str = Field(title="시간외단일가VI적용구분코드", max_length=1)
    last_ssts_cntg_qty: str = Field(title="최종 공매도 체결 수량", max_length=12)
    invt_caful_yn: str = Field(title="투자유의여부", max_length=1)
    mrkt_warn_cls_code: str = Field(title="시장경고코드", max_length=2)
    short_over_yn: str = Field(title="단기과열여부", max_length=1)
    sltr_yn: str = Field(title="정리매매여부", max_length=1)
    mang_issu_cls_code: str = Field(title="관리종목여부", max_length=1)


class DomesticStockCurrentPrice(BaseModel, KisHttpBody):
    """국내주식 현재가 시세"""

    output: DomesticStockCurrentPriceItem = Field(title="응답상세")


class DomesticStockCurrentPriceItem2(BaseModel):

    rprs_mrkt_kor_name: str = Field(title="대표 시장 한글명", max_length=40)
    new_hgpr_lwpr_cls_code: Optional[str] = Field(default=None, title="신 고가 저가 구분 코드", max_length=10)
    mxpr_llam_cls_code: Optional[str] = Field(default=None, title="상한하한가 구분코드", max_length=10)
    crdt_able_yn: str = Field(title="신용 가능 여부", max_length=1)
    stck_mxpr: str = Field(title="주식 상한가", max_length=10)
    elw_pblc_yn: str = Field(title="ELW 발행 여부", max_length=1)
    prdy_clpr_vrss_oprc_rate: str = Field(title="전일 종가 대비 시가2 비율", max_length=84)
    crdt_rate: str = Field(title="신용 비율", max_length=84)
    marg_rate: str = Field(title="증거금 비율", max_length=84)
    lwpr_vrss_prpr: str = Field(title="최저가 대비 현재가", max_length=10)
    lwpr_vrss_prpr_sign: str = Field(title="최저가 대비 현재가 부호", max_length=1)
    prdy_clpr_vrss_lwpr_rate: str = Field(title="전일 종가 대비 최저가 비율", max_length=84)
    stck_lwpr: str = Field(title="주식 최저가", max_length=10)
    hgpr_vrss_prpr: str = Field(title="최고가 대비 현재가", max_length=10)
    hgpr_vrss_prpr_sign: str = Field(title="최고가 대비 현재가 부호", max_length=1)
    prdy_clpr_vrss_hgpr_rate: str = Field(title="전일 종가 대비 최고가 비율", max_length=84)
    stck_hgpr: str = Field(title="주식 최고가", max_length=10)
    oprc_vrss_prpr: str = Field(title="시가2 대비 현재가", max_length=10)
    oprc_vrss_prpr_sign: str = Field(title="시가2 대비 현재가 부호", max_length=1)
    mang_issu_yn: str = Field(title="관리 종목 여부", max_length=1)
    divi_app_cls_code: str = Field(title="등시호가배분적용구분코드", max_length=2)
    short_over_yn: str = Field(title="단기과열여부", max_length=1)
    mrkt_warn_cls_code: str = Field(title="시장 경고 구분", max_length=2)
    invt_caful_yn: str = Field(title="투자유의여부", max_length=1)
    stange_runup_yn: str = Field(title="이상급등여부", max_length=1)
    ssts_hot_yn: str = Field(title="공매도과열 여부", max_length=1)
    low_current_yn: str = Field(title="저유동성 중복여부", max_length=1)
    vi_cls_code: str = Field(title="VI적용구분코드", max_length=1)
    short_over_cls_code: str = Field(title="단기과열구분코드", max_length=10)
    stck_llam: str = Field(title="주식 하한가", max_length=10)
    new_lstn_cls_name: str = Field(title="신규 상장 구분명", max_length=40)
    vlnt_deal_cls_name: str = Field(title="임의 매매 구분명", max_length=16)
    flng_cls_name: Optional[str] = Field(default=None, title="락 구분 이름", max_length=40)
    revl_issu_reas_name: Optional[str] = Field(default=None, title="재평가 종목 사유 명", max_length=40)
    mrkt_warn_cls_name: Optional[Literal["투자환기", "투자경고"]] = Field(default=None, title="시장 경고 구분명", max_length=40)
    stck_sdpr: str = Field(title="주식 기준가", max_length=10)
    bstp_cls_code: str = Field(title="업종 구분 코드", max_length=9)
    stck_prdy_clpr: str = Field(title="주식 전일 종가", max_length=10)
    insn_pbnt_yn: str = Field(title="불성실 공시 여부", max_length=1)
    fcam_mod_cls_name: Optional[str] = Field(default=None, title="액면가 변경 구분 명", max_length=10)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=18)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    prdy_vrss_vol_rate: str = Field(title="전일 대비 거래량 비율", max_length=84)
    bstp_kor_isnm: str = Field(title="업종 한글 종목명", max_length=40)
    sltr_yn: str = Field(title="정리매매 여부", max_length=1)
    trht_yn: str = Field(title="거래정지 여부", max_length=1)
    oprc_rang_cont_yn: str = Field(title="시가 범위 연장 여부", max_length=1)
    vlnt_fin_cls_code: str = Field(title="임의 종료 구분 코드", max_length=1)
    stck_oprc: str = Field(title="주식 시가2", max_length=10)
    prdy_vol: str = Field(title="전일 거래량", max_length=18)


class DomesticStockCurrentPrice2(BaseModel, KisHttpBody):
    """국내주식 현재가 시세2"""

    output: DomesticStockCurrentPriceItem2 = Field(title="응답상세")


class DomesticStockCurrentPriceDetailItem(BaseModel):
    """국내주식 현재가 체결 아이템"""

    stck_cntg_hour: str = Field(title="주식 체결 시간", max_length=6)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    cntg_vol: str = Field(title="체결 거래량", max_length=18)
    tday_rltv: str = Field(title="당일 체결강도", max_length=112)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)


class DomesticStockCurrentPriceDetail(BaseModel, KisHttpBody):
    """국내주식 현재가 체결"""

    output: Sequence[DomesticStockCurrentPriceDetailItem] = Field(default_factory=list)


class DomesticStockCurrentPriceDailyItem(BaseModel):
    """국내주식 현재가 일자별 아이템"""

    stck_bsop_date: str = Field(title="주식 영업 일자", max_length=8)
    stck_oprc: str = Field(title="주식 시가2", max_length=10)
    stck_hgpr: str = Field(title="주식 최고가", max_length=10)
    stck_lwpr: str = Field(title="주식 최저가", max_length=10)
    stck_clpr: str = Field(title="주식 종가", max_length=10)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    prdy_vrss_vol_rate: str = Field(title="전일 대비 거래량 비율", max_length=84)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    hts_frgn_ehrt: str = Field(title="HTS 외국인 소진율", max_length=82)
    frgn_ntby_qty: str = Field(title="외국인 순매수 수량", max_length=12)
    flng_cls_code: str = Field(title="락 구분 코드", max_length=2)
    acml_prtt_rate: str = Field(title="누적 분할 비율", max_length=84)


class DomesticStockCurrentPriceDaily(BaseModel, KisHttpBody):
    """국내주식 현재가 일자별"""

    pass


class DomesticStockCurrentPriceAskingExpectedConclusionItem1(BaseModel):
    """국내주식 현재가 호가/예상체결 아이템"""

    aspr_acpt_hour: str = Field(title="호가 접수 시간", max_length=6)
    askp1: str = Field(title="매도호가1", max_length=10)
    askp2: str = Field(title="매도호가2", max_length=10)
    askp3: str = Field(title="매도호가3", max_length=10)
    askp4: str = Field(title="매도호가4", max_length=10)
    askp5: str = Field(title="매도호가5", max_length=10)
    askp6: str = Field(title="매도호가6", max_length=10)
    askp7: str = Field(title="매도호가7", max_length=10)
    askp8: str = Field(title="매도호가8", max_length=10)
    askp9: str = Field(title="매도호가9", max_length=10)
    askp10: str = Field(title="매도호가10", max_length=10)
    bidp1: str = Field(title="매수호가1", max_length=10)
    bidp2: str = Field(title="매수호가2", max_length=10)
    bidp3: str = Field(title="매수호가3", max_length=10)
    bidp4: str = Field(title="매수호가4", max_length=10)
    bidp5: str = Field(title="매수호가5", max_length=10)
    bidp6: str = Field(title="매수호가6", max_length=10)
    bidp7: str = Field(title="매수호가7", max_length=10)
    bidp8: str = Field(title="매수호가8", max_length=10)
    bidp9: str = Field(title="매수호가9", max_length=10)
    bidp10: str = Field(title="매수호가10", max_length=10)
    askp_rsqn1: str = Field(title="매도호가 잔량1", max_length=12)
    askp_rsqn2: str = Field(title="매도호가 잔량2", max_length=12)
    askp_rsqn3: str = Field(title="매도호가 잔량3", max_length=12)
    askp_rsqn4: str = Field(title="매도호가 잔량4", max_length=12)
    askp_rsqn5: str = Field(title="매도호가 잔량5", max_length=12)
    askp_rsqn6: str = Field(title="매도호가 잔량6", max_length=12)
    askp_rsqn7: str = Field(title="매도호가 잔량7", max_length=12)
    askp_rsqn8: str = Field(title="매도호가 잔량8", max_length=12)
    askp_rsqn9: str = Field(title="매도호가 잔량9", max_length=12)
    askp_rsqn10: str = Field(title="매도호가 잔량10", max_length=12)
    bidp_rsqn1: str = Field(title="매수호가 잔량1", max_length=12)
    bidp_rsqn2: str = Field(title="매수호가 잔량2", max_length=12)
    bidp_rsqn3: str = Field(title="매수호가 잔량3", max_length=12)
    bidp_rsqn4: str = Field(title="매수호가 잔량4", max_length=12)
    bidp_rsqn5: str = Field(title="매수호가 잔량5", max_length=12)
    bidp_rsqn6: str = Field(title="매수호가 잔량6", max_length=12)
    bidp_rsqn7: str = Field(title="매수호가 잔량7", max_length=12)
    bidp_rsqn8: str = Field(title="매수호가 잔량8", max_length=12)
    bidp_rsqn9: str = Field(title="매수호가 잔량9", max_length=12)
    bidp_rsqn10: str = Field(title="매수호가 잔량10", max_length=12)
    askp_rsqn_icdc1: str = Field(title="매도호가 잔량 증감1", max_length=10)
    askp_rsqn_icdc2: str = Field(title="매도호가 잔량 증감2", max_length=10)
    askp_rsqn_icdc3: str = Field(title="매도호가 잔량 증감3", max_length=10)
    askp_rsqn_icdc4: str = Field(title="매도호가 잔량 증감4", max_length=10)
    askp_rsqn_icdc5: str = Field(title="매도호가 잔량 증감5", max_length=10)
    askp_rsqn_icdc6: str = Field(title="매도호가 잔량 증감6", max_length=10)
    askp_rsqn_icdc7: str = Field(title="매도호가 잔량 증감7", max_length=10)
    askp_rsqn_icdc8: str = Field(title="매도호가 잔량 증감8", max_length=10)
    askp_rsqn_icdc9: str = Field(title="매도호가 잔량 증감9", max_length=10)
    askp_rsqn_icdc10: str = Field(title="매도호가 잔량 증감10", max_length=10)
    bidp_rsqn_icdc1: str = Field(title="매수호가 잔량 증감1", max_length=10)
    bidp_rsqn_icdc2: str = Field(title="매수호가 잔량 증감2", max_length=10)
    bidp_rsqn_icdc3: str = Field(title="매수호가 잔량 증감3", max_length=10)
    bidp_rsqn_icdc4: str = Field(title="매수호가 잔량 증감4", max_length=10)
    bidp_rsqn_icdc5: str = Field(title="매수호가 잔량 증감5", max_length=10)
    bidp_rsqn_icdc6: str = Field(title="매수호가 잔량 증감6", max_length=10)
    bidp_rsqn_icdc7: str = Field(title="매수호가 잔량 증감7", max_length=10)
    bidp_rsqn_icdc8: str = Field(title="매수호가 잔량 증감8", max_length=10)
    bidp_rsqn_icdc9: str = Field(title="매수호가 잔량 증감9", max_length=10)
    bidp_rsqn_icdc10: str = Field(title="매수호가 잔량 증감10", max_length=10)
    total_askp_rsqn: str = Field(title="총 매도호가 잔량", max_length=12)
    total_bidp_rsqn: str = Field(title="총 매수호가 잔량", max_length=12)
    total_askp_rsqn_icdc: str = Field(title="총 매도호가 잔량 증감", max_length=10)
    total_bidp_rsqn_icdc: str = Field(title="총 매수호가 잔량 증감", max_length=10)
    ovtm_total_askp_icdc: str = Field(title="시간외 총 매도호가 증감", max_length=10)
    ovtm_total_bidp_icdc: str = Field(title="시간외 총 매수호가 증감", max_length=10)
    ovtm_total_askp_rsqn: str = Field(title="시간외 총 매도호가 잔량", max_length=12)
    ovtm_total_bidp_rsqn: str = Field(title="시간외 총 매수호가 잔량", max_length=12)
    ntby_aspr_rsqn: str = Field(title="순매수 호가 잔량", max_length=12)
    new_mkop_cls_code: str = Field(title="신 장운영 구분 코드", max_length=2)


class DomesticStockCurrentPriceAskingExpectedConclusionItem2(BaseModel):

    antc_mkop_cls_code: str = Field(title="예상 장운영 구분 코드", max_length=3)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    stck_oprc: str = Field(title="주식 시가2", max_length=10)
    stck_hgpr: str = Field(title="주식 최고가", max_length=10)
    stck_lwpr: str = Field(title="주식 최저가", max_length=10)
    stck_sdpr: str = Field(title="주식 기준가", max_length=10)
    antc_cnpr: str = Field(title="예상 체결가", max_length=10)
    antc_cntg_vrss_sign: str = Field(title="예상 체결 대비 부호", max_length=1)
    antc_cntg_vrss: str = Field(title="예상 체결 대비", max_length=10)
    antc_cntg_prdy_ctrt: str = Field(title="예상 체결 전일 대비율", max_length=11)
    antc_vol: str = Field(title="예상 거래량", max_length=18)
    stck_shrn_iscd: str = Field(title="주식 단축 종목코드", max_length=9)
    vi_cls_code: str = Field(title="VI적용구분코드", max_length=1)

class DomesticStockCurrentPriceAskingExpectedConclusion(BaseModel, KisHttpBody):
    """국내주식 현재가 호가/예상체결"""

    output1: DomesticStockCurrentPriceAskingExpectedConclusionItem1 = Field(title="응답상세1")
    output2: DomesticStockCurrentPriceAskingExpectedConclusionItem2 = Field(title="응답상세2")


class DomesticStockCurrentPriceInvestorItem(BaseModel):

    stck_bsop_date: str = Field(title="주식 영업 일자", max_length=8)
    stck_clpr: str = Field(title="주식 종가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prsn_ntby_qty: str = Field(title="개인 순매수 수량", max_length=12)
    frgn_ntby_qty: str = Field(title="외국인 순매수 수량", max_length=12)
    orgn_ntby_qty: str = Field(title="기관계 순매수 수량", max_length=18)
    prsn_ntby_tr_pbmn: str = Field(title="개인 순매수 거래 대금", max_length=18)
    frgn_ntby_tr_pbmn: str = Field(title="외국인 순매수 거래 대금", max_length=18)
    orgn_ntby_tr_pbmn: str = Field(title="기관계 순매수 거래 대금", max_length=18)
    prsn_shnu_vol: str = Field(title="개인 매수2 거래량", max_length=18)
    frgn_shnu_vol: str = Field(title="외국인 매수2 거래량", max_length=18)
    orgn_shnu_vol: str = Field(title="기관계 매수2 거래량", max_length=18)
    prsn_shnu_tr_pbmn: str = Field(title="개인 매수2 거래 대금", max_length=18)
    frgn_shnu_tr_pbmn: str = Field(title="외국인 매수2 거래 대금", max_length=18)
    orgn_shnu_tr_pbmn: str = Field(title="기관계 매수2 거래 대금", max_length=18)
    prsn_seln_vol: str = Field(title="개인 매도 거래량", max_length=18)
    frgn_seln_vol: str = Field(title="외국인 매도 거래량", max_length=18)
    orgn_seln_vol: str = Field(title="기관계 매도 거래량", max_length=18)
    prsn_seln_tr_pbmn: str = Field(title="개인 매도 거래 대금", max_length=18)
    frgn_seln_tr_pbmn: str = Field(title="외국인 매도 거래 대금", max_length=18)
    orgn_seln_tr_pbmn: str = Field(title="기관계 매도 거래 대금", max_length=18)


class DomesticStockCurrentPriceInvestor(BaseModel, KisHttpBody):
    """국내주식 현재가 투자자"""

    output: Sequence[DomesticStockCurrentPriceInvestorItem] = Field(default_factory=list)


class DomesticStockCurrentPriceMemberItem(BaseModel):

    # 매도 회원사 정보
    seln_mbcr_no1: str = Field(description="매도 회원사 번호1")
    seln_mbcr_no2: str = Field(description="매도 회원사 번호2")
    seln_mbcr_no3: str = Field(description="매도 회원사 번호3")
    seln_mbcr_no4: str = Field(description="매도 회원사 번호4")
    seln_mbcr_no5: str = Field(description="매도 회원사 번호5")
    seln_mbcr_name1: str = Field(description="매도 회원사 명1")
    seln_mbcr_name2: str = Field(description="매도 회원사 명2")
    seln_mbcr_name3: str = Field(description="매도 회원사 명3")
    seln_mbcr_name4: str = Field(description="매도 회원사 명4")
    seln_mbcr_name5: str = Field(description="매도 회원사 명5")
    total_seln_qty1: str = Field(description="총 매도 수량1")
    total_seln_qty2: str = Field(description="총 매도 수량2")
    total_seln_qty3: str = Field(description="총 매도 수량3")
    total_seln_qty4: str = Field(description="총 매도 수량4")
    total_seln_qty5: str = Field(description="총 매도 수량5")
    seln_mbcr_rlim1: str = Field(description="매도 회원사 비중1")
    seln_mbcr_rlim2: str = Field(description="매도 회원사 비중2")
    seln_mbcr_rlim3: str = Field(description="매도 회원사 비중3")
    seln_mbcr_rlim4: str = Field(description="매도 회원사 비중4")
    seln_mbcr_rlim5: str = Field(description="매도 회원사 비중5")
    seln_qty_icdc1: str = Field(description="매도 수량 증감1")
    seln_qty_icdc2: str = Field(description="매도 수량 증감2")
    seln_qty_icdc3: str = Field(description="매도 수량 증감3")
    seln_qty_icdc4: str = Field(description="매도 수량 증감4")
    seln_qty_icdc5: str = Field(description="매도 수량 증감5")

    # 매수 회원사 정보
    shnu_mbcr_no1: str = Field(description="매수2 회원사 번호1")
    shnu_mbcr_no2: str = Field(description="매수2 회원사 번호2")
    shnu_mbcr_no3: str = Field(description="매수2 회원사 번호3")
    shnu_mbcr_no4: str = Field(description="매수2 회원사 번호4")
    shnu_mbcr_no5: str = Field(description="매수2 회원사 번호5")
    shnu_mbcr_name1: str = Field(description="매수2 회원사 명1")
    shnu_mbcr_name2: str = Field(description="매수2 회원사 명2")
    shnu_mbcr_name3: str = Field(description="매수2 회원사 명3")
    shnu_mbcr_name4: str = Field(description="매수2 회원사 명4")
    shnu_mbcr_name5: str = Field(description="매수2 회원사 명5")
    total_shnu_qty1: str = Field(description="총 매수2 수량1")
    total_shnu_qty2: str = Field(description="총 매수2 수량2")
    total_shnu_qty3: str = Field(description="총 매수2 수량3")
    total_shnu_qty4: str = Field(description="총 매수2 수량4")
    total_shnu_qty5: str = Field(description="총 매수2 수량5")
    shnu_mbcr_rlim1: str = Field(description="매수2 회원사 비중1")
    shnu_mbcr_rlim2: str = Field(description="매수2 회원사 비중2")
    shnu_mbcr_rlim3: str = Field(description="매수2 회원사 비중3")
    shnu_mbcr_rlim4: str = Field(description="매수2 회원사 비중4")
    shnu_mbcr_rlim5: str = Field(description="매수2 회원사 비중5")
    shnu_qty_icdc1: str = Field(description="매수2 수량 증감1")
    shnu_qty_icdc2: str = Field(description="매수2 수량 증감2")
    shnu_qty_icdc3: str = Field(description="매수2 수량 증감3")
    shnu_qty_icdc4: str = Field(description="매수2 수량 증감4")
    shnu_qty_icdc5: str = Field(description="매수2 수량 증감5")

    # 외국계 정보
    glob_total_seln_qty: str = Field(description="외국계 총 매도 수량")
    glob_seln_rlim: str = Field(description="외국계 매도 비중")
    glob_ntby_qty: str = Field(description="외국계 순매수 수량")
    glob_total_shnu_qty: str = Field(description="외국계 총 매수2 수량")
    glob_shnu_rlim: str = Field(description="외국계 매수2 비중")

    # 외국계 여부
    seln_mbcr_glob_yn_1: str = Field(description="매도 회원사 외국계 여부1")
    seln_mbcr_glob_yn_2: str = Field(description="매도 회원사 외국계 여부2")
    seln_mbcr_glob_yn_3: str = Field(description="매도 회원사 외국계 여부3")
    seln_mbcr_glob_yn_4: str = Field(description="매도 회원사 외국계 여부4")
    seln_mbcr_glob_yn_5: str = Field(description="매도 회원사 외국계 여부5")
    shnu_mbcr_glob_yn_1: str = Field(description="매수2 회원사 외국계 여부1")
    shnu_mbcr_glob_yn_2: str = Field(description="매수2 회원사 외국계 여부2")
    shnu_mbcr_glob_yn_3: str = Field(description="매수2 회원사 외국계 여부3")
    shnu_mbcr_glob_yn_4: str = Field(description="매수2 회원사 외국계 여부4")
    shnu_mbcr_glob_yn_5: str = Field(description="매수2 회원사 외국계 여부5")

    # 외국계 증감
    glob_total_seln_qty_icdc: str = Field(description="외국계 총 매도 수량 증감")
    glob_total_shnu_qty_icdc: str = Field(description="외국계 총 매수2 수량 증감")


class DomesticStockCurrentPriceMember(BaseModel, KisHttpBody):
    """국내주식 현재가 회원사"""

    output: DomesticStockCurrentPriceMemberItem = Field(title="응답상세")


class DomesticStockPeriodQuoteItem1(BaseModel):
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=11)
    stck_prdy_clpr: str = Field(title="주식 전일 종가", max_length=10)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=18)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    stck_shrn_iscd: str = Field(title="주식 단축 종목코드", max_length=9)
    prdy_vol: str = Field(title="전일 거래량", max_length=18)
    stck_mxpr: str = Field(title="주식 상한가", max_length=10)
    stck_llam: str = Field(title="주식 하한가", max_length=10)
    stck_oprc: str = Field(title="주식 시가", max_length=10)
    stck_hgpr: str = Field(title="주식 최고가", max_length=10)
    stck_lwpr: str = Field(title="주식 최저가", max_length=10)
    stck_prdy_oprc: str = Field(title="주식 전일 시가", max_length=10)
    stck_prdy_hgpr: str = Field(title="주식 전일 최고가", max_length=10)
    stck_prdy_lwpr: str = Field(title="주식 전일 최저가", max_length=10)
    askp: str = Field(title="매도호가", max_length=10)
    bidp: str = Field(title="매수호가", max_length=10)
    prdy_vrss_vol: str = Field(title="전일 대비 거래량", max_length=18)
    vol_tnrt: str = Field(title="거래량 회전율", max_length=11)
    stck_fcam: str = Field(title="주식 액면가", max_length=11)
    lstn_stcn: str = Field(title="상장 주수", max_length=18)
    cpfn: str = Field(title="자본금", max_length=22)
    hts_avls: str = Field(title="HTS 시가총액", max_length=18)
    per: str = Field(title="PER", max_length=11)
    eps: str = Field(title="EPS", max_length=14)
    pbr: str = Field(title="PBR", max_length=11)
    itewhol_loan_rmnd_rate: str = Field(alias="itewhol_loan_rmnd_ratem name", title="전체 융자 잔고 비율", max_length=13)

class DomesticStockPeriodQuoteItem2(BaseModel):
    stck_bsop_date: str = Field(title="주식 영업 일자", max_length=8)
    stck_clpr: str = Field(title="주식 종가", max_length=10)
    stck_oprc: str = Field(title="주식 시가", max_length=10)
    stck_hgpr: str = Field(title="주식 최고가", max_length=10)
    stck_lwpr: str = Field(title="주식 최저가", max_length=10)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=18)
    flng_cls_code: str = Field(title="락 구분 코드", description="01 : 권리락 02 : 배당락 03 : 분배락 04 : 권배락 05 : 중간(분기)배당락 06 : 권리중간배당락 07 : 권리분기배당락", max_length=2)
    prtt_rate: str = Field(title="분할 비율", description="기준가/전일 종가", max_length=11)
    mod_yn: str = Field(title="변경 여부", max_length=1)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    revl_issu_reas: str = Field(title="재평가사유코드", description="00:해당없음 01:회사분할 02:자본감소 03:장기간정지 04:초과분배 05:대규모배당 06:회사분할합병 07:ETN증권병합/분할 08:신종증권기세조정 99:기타", max_length=2)


class DomesticStockPeriodQuote(BaseModel, KisHttpBody):
    """국내주식 기간별시세"""

    output1: DomesticStockPeriodQuoteItem1 = Field(title="응답상세1")
    output2: Sequence[DomesticStockPeriodQuoteItem2] = Field(default_factory=list)


class DomesticStockTodayMinuteChartItem1(BaseModel):
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=10)
    stck_prdy_clpr: str = Field(title="전일대비 종가", max_length=10)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    acml_tr_pbmn: str = Field(title="누적 거래대금", max_length=18)
    hts_kor_isnm: str = Field(title="한글 종목명", max_length=40)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)

class DomesticStockTodayMinuteChartItem2(BaseModel):
    stck_bsop_date: str = Field(title="주식 영업일자", max_length=8)
    stck_cntg_hour: str = Field(title="주식 체결시간", max_length=6)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    stck_oprc: str = Field(title="주식 시가", max_length=10)
    stck_hgpr: str = Field(title="주식 최고가", max_length=10)
    stck_lwpr: str = Field(title="주식 최저가", max_length=10)
    cntg_vol: str = Field(title="체결 거래량", max_length=18)
    acml_tr_pbmn: str = Field(title="누적 거래대금", max_length=18)


class DomesticStockTodayMinuteChart(BaseModel, KisHttpBody):
    """국내주식 당일분봉조회"""

    output1: DomesticStockTodayMinuteChartItem1 = Field(title="응답상세1")
    output2: Sequence[DomesticStockTodayMinuteChartItem2] = Field(default_factory=list)


class DomesticStockDailyMinuteChartItem1(BaseModel):
    prdy_vrss: str = Field(title="전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_ctrt: str = Field(title="전일 대비율")
    stck_prdy_clpr: str = Field(title="주식 전일 종가")
    acml_vol: str = Field(title="누적 거래량")
    acml_tr_pbmn: str = Field(title="누적 거래 대금")
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    stck_prpr: str = Field(title="주식 현재가")

class DomesticStockDailyMinuteChartItem2(BaseModel):
    stck_bsop_date: str = Field(title="주식 영업 일자")
    stck_cntg_hour: str = Field(title="주식 체결 시간")
    stck_prpr: str = Field(title="주식 현재가")
    stck_oprc: str = Field(title="주식 시가")
    stck_hgpr: str = Field(title="주식 최고가")
    stck_lwpr: str = Field(title="주식 최저가")
    cntg_vol: str = Field(title="체결 거래량")
    acml_tr_pbmn: str = Field(title="누적 거래 대금")


class DomesticStockDailyMinuteChart(BaseModel, KisHttpBody):
    """국내주식 일별분봉조회"""

    output1: DomesticStockDailyMinuteChartItem1 = Field(title="응답상세1")
    output2: Sequence[DomesticStockDailyMinuteChartItem2] = Field(default_factory=list)


class DomesticStockCurrentPriceTimeItemConclusionItem1(BaseModel):
    """국내주식 현재가 당일시간대별체결 응답상세1"""

    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=11)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    prdy_vol: str = Field(title="전일 거래량", max_length=18)
    rprs_mrkt_kor_name: str = Field(title="대표 시장 한글 명", max_length=40)

class DomesticStockCurrentPriceTimeItemConclusionItem2(BaseModel):
    """국내주식 현재가 당일시간대별체결 응답상세2"""

    stck_cntg_hour: str = Field(title="주식 체결 시간", max_length=6)
    # TODO(typo) 문서에는 stck_pbpr 이라고 되어있으나, stck_prpr 오타로 보임
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=11)
    askp: str = Field(title="매도호가", max_length=10)
    bidp: str = Field(title="매수호가", max_length=10)
    tday_rltv: str = Field(title="당일 체결강도", max_length=14)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    cnqn: str = Field(title="체결량", max_length=18)

class DomesticStockCurrentPriceTimeItemConclusion(BaseModel, KisHttpBody):
    """국내주식 현재가 당일시간대별체결"""

    output1: DomesticStockCurrentPriceTimeItemConclusionItem1 = Field(title="응답상세1")
    output2: Sequence[DomesticStockCurrentPriceTimeItemConclusionItem2] = Field(default_factory=list)


class DomesticStockCurrentPriceDailyOvertimePriceItem1(BaseModel):
    ovtm_untp_prpr: str = Field(title="시간외 단일가 현재가", max_length=10)
    ovtm_untp_prdy_vrss: str = Field(title="시간외 단일가 전일 대비", max_length=10)
    ovtm_untp_prdy_vrss_sign: str = Field(title="시간외 단일가 전일 대비 부호", max_length=1)
    ovtm_untp_prdy_ctrt: str = Field(title="시간외 단일가 전일 대비율", max_length=11)
    ovtm_untp_vol: str = Field(title="시간외 단일가 거래량", max_length=18)
    ovtm_untp_tr_pbmn: str = Field(title="시간외 단일가 거래 대금", max_length=18)
    ovtm_untp_mxpr: str = Field(title="시간외 단일가 상한가", max_length=18)
    ovtm_untp_llam: str = Field(title="시간외 단일가 하한가", max_length=18)
    ovtm_untp_oprc: str = Field(title="시간외 단일가 시가2", max_length=10)
    ovtm_untp_hgpr: str = Field(title="시간외 단일가 최고가", max_length=10)
    ovtm_untp_lwpr: str = Field(title="시간외 단일가 최저가", max_length=10)
    ovtm_untp_antc_cnpr: str = Field(title="시간외 단일가 예상 체결가", max_length=10)
    ovtm_untp_antc_cntg_vrss: str = Field(title="시간외 단일가 예상 체결 대비", max_length=10)
    ovtm_untp_antc_cntg_vrss_sign: str = Field(title="시간외 단일가 예상 체결 대비 부호", max_length=1)
    ovtm_untp_antc_cntg_ctrt: str = Field(title="시간외 단일가 예상 체결 대비율", max_length=11)
    ovtm_untp_antc_vol: str = Field(title="시간외 단일가 예상 거래량", max_length=18)


class DomesticStockCurrentPriceDailyOvertimePriceItem2(BaseModel):
    stck_bsop_date: str = Field(title="주식 영업 일자", max_length=8)
    ovtm_untp_prpr: str = Field(title="시간외 단일가 현재가", max_length=10)
    ovtm_untp_prdy_vrss: str = Field(title="시간외 단일가 전일 대비", max_length=10)
    ovtm_untp_prdy_vrss_sign: str = Field(title="시간외 단일가 전일 대비 부호", max_length=1)
    ovtm_untp_prdy_ctrt: str = Field(title="시간외 단일가 전일 대비율", max_length=11)
    ovtm_untp_vol: str = Field(title="시간외 단일가 거래량", max_length=18)
    stck_clpr: str = Field(title="주식 종가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=11)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    ovtm_untp_tr_pbmn: str = Field(title="시간외 단일가 거래대금", max_length=18)


class DomesticStockCurrentPriceDailyOvertimePrice(BaseModel, KisHttpBody):
    """국내주식 현재가 시간외일자별주가"""

    output1: DomesticStockCurrentPriceDailyOvertimePriceItem1 = Field(title="응답상세1")
    output2: Sequence[DomesticStockCurrentPriceDailyOvertimePriceItem2] = Field(default_factory=list)


class DomesticStockCurrentPriceOvertimeConclusionItem1(BaseModel):
    ovtm_untp_prpr: str = Field(title="시간외 단일가 현재가", max_length=10)
    ovtm_untp_prdy_vrss: str = Field(title="시간외 단일가 전일 대비", max_length=10)
    ovtm_untp_prdy_vrss_sign: str = Field(title="시간외 단일가 전일 대비 부호", max_length=1)
    ovtm_untp_prdy_ctrt: str = Field(title="시간외 단일가 전일 대비율", max_length=11)
    ovtm_untp_vol: str = Field(title="시간외 단일가 거래량", max_length=18)
    ovtm_untp_tr_pbmn: str = Field(title="시간외 단일가 거래 대금", max_length=18)
    ovtm_untp_mxpr: str = Field(title="시간외 단일가 상한가", max_length=18)
    ovtm_untp_llam: str = Field(title="시간외 단일가 하한가", max_length=18)
    ovtm_untp_oprc: str = Field(title="시간외 단일가 시가2", max_length=10)
    ovtm_untp_hgpr: str = Field(title="시간외 단일가 최고가", max_length=10)
    ovtm_untp_lwpr: str = Field(title="시간외 단일가 최저가", max_length=10)
    ovtm_untp_antc_cnpr: str = Field(title="시간외 단일가 예상 체결가", max_length=10)
    ovtm_untp_antc_cntg_vrss: str = Field(title="시간외 단일가 예상 체결 대비", max_length=10)
    ovtm_untp_antc_cntg_vrss_sign: str = Field(title="시간외 단일가 예상 체결 대비", max_length=1)
    ovtm_untp_antc_cntg_ctrt: str = Field(title="시간외 단일가 예상 체결 대비율", max_length=11)
    ovtm_untp_antc_vol: str = Field(title="시간외 단일가 예상 거래량", max_length=18)
    uplm_sign: str = Field(title="상한 부호", max_length=1)
    lslm_sign: str = Field(title="하한 부호", max_length=1)

class DomesticStockCurrentPriceOvertimeConclusionItem2(BaseModel):
    stck_cntg_hour: str = Field(title="주식 체결 시간", max_length=6)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=11)
    askp: str = Field(title="매도호가", max_length=10)
    bidp: str = Field(title="매수호가", max_length=10)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    cntg_vol: str = Field(title="체결 거래량", max_length=18)


class DomesticStockCurrentPriceOvertimeConclusion(BaseModel, KisHttpBody):
    """국내주식 현재가 시간외체결"""

    output1: Optional[DomesticStockCurrentPriceOvertimeConclusionItem1] = Field(title="응답상세1", default=None)
    output2: Optional[Sequence[DomesticStockCurrentPriceOvertimeConclusionItem2]] = Field(default_factory=list)


class DomesticStockOvertimeCurrentPriceItem(BaseModel):
    bstp_kor_isnm: str = Field(title="업종 한글 종목명", max_length=40)
    mang_issu_cls_name: Optional[str] = Field(title="관리 종목 구분 명", max_length=40, default=None)
    ovtm_untp_prpr: str = Field(title="시간외 단일가 현재가", max_length=10)
    ovtm_untp_prdy_vrss: str = Field(title="시간외 단일가 전일 대비", max_length=10)
    ovtm_untp_prdy_vrss_sign: str = Field(title="시간외 단일가 전일 대비 부호", max_length=1)
    ovtm_untp_prdy_ctrt: str = Field(title="시간외 단일가 전일 대비율", max_length=82)
    ovtm_untp_vol: str = Field(title="시간외 단일가 거래량", max_length=18)
    ovtm_untp_tr_pbmn: str = Field(title="시간외 단일가 거래 대금", max_length=18)
    ovtm_untp_mxpr: str = Field(title="시간외 단일가 상한가", max_length=18)
    ovtm_untp_llam: str = Field(title="시간외 단일가 하한가", max_length=18)
    ovtm_untp_oprc: str = Field(title="시간외 단일가 시가2", max_length=10)
    ovtm_untp_hgpr: str = Field(title="시간외 단일가 최고가", max_length=10)
    ovtm_untp_lwpr: str = Field(title="시간외 단일가 최저가", max_length=10)
    marg_rate: str = Field(title="증거금 비율", max_length=84)
    ovtm_untp_antc_cnpr: str = Field(title="시간외 단일가 예상 체결가", max_length=10)
    ovtm_untp_antc_cntg_vrss: str = Field(title="시간외 단일가 예상 체결 대비", max_length=10)
    ovtm_untp_antc_cntg_vrss_sign: str = Field(title="시간외 단일가 예상 체결 대비 부호", max_length=1)
    ovtm_untp_antc_cntg_ctrt: str = Field(title="시간외 단일가 예상 체결 대비율", max_length=82)
    ovtm_untp_antc_cnqn: str = Field(title="시간외 단일가 예상 체결량", max_length=18)
    crdt_able_yn: str = Field(title="신용 가능 여부", max_length=1)
    new_lstn_cls_name: str = Field(title="신규 상장 구분 명", max_length=40)
    sltr_yn: str = Field(title="정리매매 여부", max_length=1)
    mang_issu_yn: str = Field(title="관리 종목 여부", max_length=1)
    mrkt_warn_cls_code: Optional[str] = Field(title="시장 경고 구분 코드", max_length=2, default=None)
    trht_yn: str = Field(title="거래정지 여부", max_length=1)
    vlnt_deal_cls_name: str = Field(title="임의 매매 구분 명", max_length=16)
    ovtm_untp_sdpr: str = Field(title="시간외 단일가 기준가", max_length=10)
    # TODO(typo) 문서에는 required Y지만 실제로는 Optional, 한글명도 '시장 경구..'
    mrkt_warn_cls_name: Optional[str] = Field(title="시장 경고 구분 명", max_length=40, default=None)
    revl_issu_reas_name: Optional[str] = Field(title="재평가 종목 사유 명", max_length=40, default=None)
    insn_pbnt_yn: str = Field(title="불성실 공시 여부", max_length=1)
    flng_cls_name: Optional[str] = Field(title="락 구분 이름", max_length=40, default=None)
    rprs_mrkt_kor_name: str = Field(title="대표 시장 한글 명", max_length=40)
    ovtm_vi_cls_code: str = Field(title="시간외단일가VI적용구분코드", max_length=1)
    bidp: str = Field(title="매수호가", max_length=10)
    askp: str = Field(title="매도호가", max_length=10)


class DomesticStockOvertimeCurrentPrice(BaseModel, KisHttpBody):
    """국내주식 시간외현재가"""

    output: DomesticStockOvertimeCurrentPriceItem = Field(title="응답상세")


class DomesticStockOvertimeAskingPriceItem(BaseModel):
    ovtm_untp_last_hour: str = Field(title="시간외 단일가 최종 시간", max_length=6)
    ovtm_untp_askp1: str = Field(title="시간외 단일가 매도호가1", max_length=10)
    ovtm_untp_askp2: str = Field(title="시간외 단일가 매도호가2", max_length=10)
    ovtm_untp_askp3: str = Field(title="시간외 단일가 매도호가3", max_length=10)
    ovtm_untp_askp4: str = Field(title="시간외 단일가 매도호가4", max_length=10)
    ovtm_untp_askp5: str = Field(title="시간외 단일가 매도호가5", max_length=10)
    ovtm_untp_askp6: str = Field(title="시간외 단일가 매도호가6", max_length=10)
    ovtm_untp_askp7: str = Field(title="시간외 단일가 매도호가7", max_length=10)
    ovtm_untp_askp8: str = Field(title="시간외 단일가 매도호가8", max_length=10)
    ovtm_untp_askp9: str = Field(title="시간외 단일가 매도호가9", max_length=10)
    ovtm_untp_askp10: str = Field(title="시간외 단일가 매도호가10", max_length=10)
    ovtm_untp_bidp1: str = Field(title="시간외 단일가 매수호가1", max_length=10)
    ovtm_untp_bidp2: str = Field(title="시간외 단일가 매수호가2", max_length=10)
    ovtm_untp_bidp3: str = Field(title="시간외 단일가 매수호가3", max_length=10)
    ovtm_untp_bidp4: str = Field(title="시간외 단일가 매수호가4", max_length=10)
    ovtm_untp_bidp5: str = Field(title="시간외 단일가 매수호가5", max_length=10)
    ovtm_untp_bidp6: str = Field(title="시간외 단일가 매수호가6", max_length=10)
    ovtm_untp_bidp7: str = Field(title="시간외 단일가 매수호가7", max_length=10)
    ovtm_untp_bidp8: str = Field(title="시간외 단일가 매수호가8", max_length=10)
    ovtm_untp_bidp9: str = Field(title="시간외 단일가 매수호가9", max_length=10)
    ovtm_untp_bidp10: str = Field(title="시간외 단일가 매수호가10", max_length=10)
    ovtm_untp_askp_icdc1: str = Field(title="시간외 단일가 매도호가 증감1", max_length=10)
    ovtm_untp_askp_icdc2: str = Field(title="시간외 단일가 매도호가 증감2", max_length=10)
    ovtm_untp_askp_icdc3: str = Field(title="시간외 단일가 매도호가 증감3", max_length=10)
    # TODO(typo): 문서에는 required Y지만 실제로는 Optional
    ovtm_untp_askp_icdc4: Optional[str] = Field(title="시간외 단일가 매도호가 증감4", max_length=10, default=None)
    ovtm_untp_askp_icdc5: Optional[str] = Field(title="시간외 단일가 매도호가 증감5", max_length=10, default=None)
    ovtm_untp_askp_icdc6: Optional[str] = Field(title="시간외 단일가 매도호가 증감6", max_length=10, default=None)
    ovtm_untp_askp_icdc7: Optional[str] = Field(title="시간외 단일가 매도호가 증감7", max_length=10, default=None)
    ovtm_untp_askp_icdc8: Optional[str] = Field(title="시간외 단일가 매도호가 증감8", max_length=10, default=None)
    ovtm_untp_askp_icdc9: Optional[str] = Field(title="시간외 단일가 매도호가 증감9", max_length=10, default=None)
    ovtm_untp_askp_icdc10: Optional[str] = Field(title="시간외 단일가 매도호가 증감10", max_length=10, default=None)
    ovtm_untp_bidp_icdc1: str = Field(title="시간외 단일가 매수호가 증감1", max_length=10)
    ovtm_untp_bidp_icdc2: str = Field(title="시간외 단일가 매수호가 증감2", max_length=10)
    ovtm_untp_bidp_icdc3: str = Field(title="시간외 단일가 매수호가 증감3", max_length=10)
    ovtm_untp_bidp_icdc4: Optional[str] = Field(title="시간외 단일가 매수호가 증감4", max_length=10, default=None)
    ovtm_untp_bidp_icdc5: Optional[str] = Field(title="시간외 단일가 매수호가 증감5", max_length=10, default=None)
    ovtm_untp_bidp_icdc6: Optional[str] = Field(title="시간외 단일가 매수호가 증감6", max_length=10, default=None)
    ovtm_untp_bidp_icdc7: Optional[str] = Field(title="시간외 단일가 매수호가 증감7", max_length=10, default=None)
    ovtm_untp_bidp_icdc8: Optional[str] = Field(title="시간외 단일가 매수호가 증감8", max_length=10, default=None)
    ovtm_untp_bidp_icdc9: Optional[str] = Field(title="시간외 단일가 매수호가 증감9", max_length=10, default=None)
    ovtm_untp_bidp_icdc10: Optional[str] = Field(title="시간외 단일가 매수호가 증감10", max_length=10, default=None)
    ovtm_untp_askp_rsqn1: str = Field(title="시간외 단일가 매도호가 잔량1", max_length=12)
    ovtm_untp_askp_rsqn2: str = Field(title="시간외 단일가 매도호가 잔량2", max_length=12)
    ovtm_untp_askp_rsqn3: str = Field(title="시간외 단일가 매도호가 잔량3", max_length=12)
    ovtm_untp_askp_rsqn4: str = Field(title="시간외 단일가 매도호가 잔량4", max_length=12)
    ovtm_untp_askp_rsqn5: str = Field(title="시간외 단일가 매도호가 잔량5", max_length=12)
    ovtm_untp_askp_rsqn6: str = Field(title="시간외 단일가 매도호가 잔량6", max_length=12)
    ovtm_untp_askp_rsqn7: str = Field(title="시간외 단일가 매도호가 잔량7", max_length=12)
    ovtm_untp_askp_rsqn8: str = Field(title="시간외 단일가 매도호가 잔량8", max_length=12)
    ovtm_untp_askp_rsqn9: str = Field(title="시간외 단일가 매도호가 잔량9", max_length=12)
    ovtm_untp_askp_rsqn10: str = Field(title="시간외 단일가 매도호가 잔량10", max_length=12)
    ovtm_untp_bidp_rsqn1: str = Field(title="시간외 단일가 매수호가 잔량1", max_length=12)
    ovtm_untp_bidp_rsqn2: str = Field(title="시간외 단일가 매수호가 잔량2", max_length=12)
    ovtm_untp_bidp_rsqn3: str = Field(title="시간외 단일가 매수호가 잔량3", max_length=12)
    ovtm_untp_bidp_rsqn4: str = Field(title="시간외 단일가 매수호가 잔량4", max_length=12)
    ovtm_untp_bidp_rsqn5: str = Field(title="시간외 단일가 매수호가 잔량5", max_length=12)
    ovtm_untp_bidp_rsqn6: str = Field(title="시간외 단일가 매수호가 잔량6", max_length=12)
    ovtm_untp_bidp_rsqn7: str = Field(title="시간외 단일가 매수호가 잔량7", max_length=12)
    ovtm_untp_bidp_rsqn8: str = Field(title="시간외 단일가 매수호가 잔량8", max_length=12)
    ovtm_untp_bidp_rsqn9: str = Field(title="시간외 단일가 매수호가 잔량9", max_length=12)
    ovtm_untp_bidp_rsqn10: str = Field(title="시간외 단일가 매수호가 잔량10", max_length=12)
    ovtm_untp_total_askp_rsqn: str = Field(title="시간외 단일가 총 매도호가 잔량", max_length=12)
    ovtm_untp_total_bidp_rsqn: str = Field(title="시간외 단일가 총 매수호가 잔량", max_length=12)
    ovtm_untp_total_askp_rsqn_icdc: str = Field(title="시간외 단일가 총 매도호가 잔량 증감", max_length=10)
    ovtm_untp_total_bidp_rsqn_icdc: str = Field(title="시간외 단일가 총 매수호가 잔량 증감", max_length=10)
    ovtm_untp_ntby_bidp_rsqn: str = Field(title="시간외 단일가 순매수 호가 잔량", max_length=12)
    total_askp_rsqn: str = Field(title="총 매도호가 잔량", max_length=12)
    total_bidp_rsqn: str = Field(title="총 매수호가 잔량", max_length=12)
    total_askp_rsqn_icdc: str = Field(title="총 매도호가 잔량 증감", max_length=10)
    total_bidp_rsqn_icdc: str = Field(title="총 매수호가 잔량 증감", max_length=10)
    ovtm_total_askp_rsqn: str = Field(title="시간외 총 매도호가 잔량", max_length=12)
    ovtm_total_bidp_rsqn: str = Field(title="시간외 총 매수호가 잔량", max_length=12)
    ovtm_total_askp_icdc: str = Field(title="시간외 총 매도호가 증감", max_length=10)
    ovtm_total_bidp_icdc: str = Field(title="시간외 총 매수호가 증감", max_length=10)


class DomesticStockOvertimeAskingPrice(BaseModel, KisHttpBody):
    """국내주식 시간외호가"""

    # TODO(typo) output이 맞지만 문서에는 output1로 잘못 표기되어 있음.
    output: DomesticStockOvertimeAskingPriceItem = Field(title="응답상세")


class DomesticStockClosingExpectedPriceItem(BaseModel):
    stck_shrn_iscd: str = Field(title="주식 단축 종목코드", max_length=9)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    sdpr_vrss_prpr: str = Field(title="기준가 대비 현재가", max_length=10)
    sdpr_vrss_prpr_rate: str = Field(title="기준가 대비 현재가 비율", max_length=84)
    cntg_vol: str = Field(title="체결 거래량", max_length=18)


class DomesticStockClosingExpectedPrice(BaseModel, KisHttpBody):
    """국내주식 장마감 예상체결가"""

    output1: Sequence[DomesticStockClosingExpectedPriceItem] = Field(default_factory=list)


class DomesticEtfEtnCurrentPriceItem(BaseModel):
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    prdy_vol: str = Field(title="전일 거래량", max_length=18)
    stck_mxpr: str = Field(title="주식 상한가", max_length=10)
    stck_llam: str = Field(title="주식 하한가", max_length=10)
    stck_prdy_clpr: str = Field(title="주식 전일 종가", max_length=10)
    stck_oprc: str = Field(title="주식 시가2", max_length=10)
    prdy_clpr_vrss_oprc_rate: str = Field(title="전일 종가 대비 시가2 비율", max_length=84)
    stck_hgpr: str = Field(title="주식 최고가", max_length=10)
    prdy_clpr_vrss_hgpr_rate: str = Field(title="전일 종가 대비 최고가 비율", max_length=84)
    stck_lwpr: str = Field(title="주식 최저가", max_length=10)
    prdy_clpr_vrss_lwpr_rate: str = Field(title="전일 종가 대비 최저가 비율", max_length=84)
    prdy_last_nav: str = Field(title="전일 최종 NAV", max_length=112)
    nav: str = Field(title="NAV", max_length=112)
    nav_prdy_vrss: str = Field(title="NAV 전일 대비", max_length=112)
    nav_prdy_vrss_sign: str = Field(title="NAV 전일 대비 부호", max_length=1)
    nav_prdy_ctrt: str = Field(title="NAV 전일 대비율", max_length=82)
    trc_errt: str = Field(title="추적 오차율", max_length=82)
    stck_sdpr: str = Field(title="주식 기준가", max_length=10)
    stck_sspr: str = Field(title="주식 대용가", max_length=10)
    # TODO(typo) 존재하지 않는 필드가 문서에 포함되어 있음.
    # nmix_ctrt: str = Field(title="지수 대비율", max_length=135)
    etf_crcl_stcn: str = Field(title="ETF 유통 주수", max_length=18)
    etf_ntas_ttam: str = Field(title="ETF 순자산 총액", max_length=22)
    etf_frcr_ntas_ttam: str = Field(title="ETF 외화 순자산 총액", max_length=22)
    frgn_limt_rate: str = Field(title="외국인 한도 비율", max_length=84)
    frgn_oder_able_qty: str = Field(title="외국인 주문 가능 수량", max_length=18)
    etf_cu_unit_scrt_cnt: str = Field(title="ETF CU 단위 증권 수", max_length=18)
    etf_cnfg_issu_cnt: str = Field(title="ETF 구성 종목 수", max_length=18)
    etf_dvdn_cycl: str = Field(title="ETF 배당 주기", max_length=2)
    crcd: str = Field(title="통화 코드", max_length=4)
    etf_crcl_ntas_ttam: str = Field(title="ETF 유통 순자산 총액", max_length=22)
    etf_frcr_crcl_ntas_ttam: str = Field(title="ETF 외화 유통 순자산 총액", max_length=22)
    etf_frcr_last_ntas_wrth_val: str = Field(title="ETF 외화 최종 순자산 가치 값", max_length=13)
    lp_oder_able_cls_code: str = Field(title="LP 주문 가능 구분 코드", max_length=2)
    stck_dryy_hgpr: str = Field(title="주식 연중 최고가", max_length=10)
    dryy_hgpr_vrss_prpr_rate: str = Field(title="연중 최고가 대비 현재가 비율", max_length=84)
    dryy_hgpr_date: str = Field(title="연중 최고가 일자", max_length=8)
    stck_dryy_lwpr: str = Field(title="주식 연중 최저가", max_length=10)
    dryy_lwpr_vrss_prpr_rate: str = Field(title="연중 최저가 대비 현재가 비율", max_length=84)
    dryy_lwpr_date: str = Field(title="연중 최저가 일자", max_length=8)
    bstp_kor_isnm: str = Field(title="업종 한글 종목명", max_length=40)
    vi_cls_code: str = Field(title="VI적용구분코드", max_length=1)
    lstn_stcn: str = Field(title="상장 주수", max_length=18)
    frgn_hldn_qty: str = Field(title="외국인 보유 수량", max_length=18)
    frgn_hldn_qty_rate: str = Field(title="외국인 보유 수량 비율", max_length=84)
    etf_trc_ert_mltp: str = Field(title="ETF 추적 수익률 배수", max_length=126)
    dprt: str = Field(title="괴리율", max_length=82)
    mbcr_name: str = Field(title="회원사 명", max_length=50)
    stck_lstn_date: str = Field(title="주식 상장 일자", max_length=8)
    mtrt_date: str = Field(title="만기 일자", max_length=8)
    shrg_type_code: str = Field(title="분배금형태코드", max_length=2)
    lp_hldn_rate: str = Field(title="LP 보유 비율", max_length=84)
    etf_trgt_nmix_bstp_code: str = Field(title="ETF대상지수업종코드", max_length=4)
    etf_div_name: str = Field(title="ETF 분류 명", max_length=40)
    etf_rprs_bstp_kor_isnm: str = Field(title="ETF 대표 업종 한글 종목명", max_length=40)
    lp_hldn_vol: str = Field(title="ETN LP 보유량", max_length=18)


class DomesticEtfEtnCurrentPrice(BaseModel, KisHttpBody):
    """국내ETF/ETN 현재가"""

    output: DomesticEtfEtnCurrentPriceItem = Field(title="응답상세")


class DomesticEtfComponentStockPriceItem1(BaseModel):
    """국내ETF 구성종목시세 아이템1"""

    stck_prpr: str = Field(title="매매 일자", max_length=10)
    prdy_vrss: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비", max_length=82)
    etf_cnfg_issu_avls: str = Field(title="전일 대비율", max_length=18)
    nav: str = Field(title="누적 거래량", max_length=112)
    nav_prdy_vrss_sign: str = Field(title="결제 일자", max_length=1)
    nav_prdy_vrss: str = Field(title="전체 융자 신규 주수", max_length=112)
    nav_prdy_ctrt: str = Field(title="전체 융자 상환 주수", max_length=84)
    etf_ntas_ttam: str = Field(title="전체 융자 잔고 주수", max_length=22)
    prdy_clpr_nav: str = Field(title="전체 융자 신규 금액", max_length=112)
    oprc_nav: str = Field(title="전체 융자 상환 금액", max_length=112)
    hprc_nav: str = Field(title="전체 융자 잔고 금액", max_length=112)
    lprc_nav: str = Field(title="전체 융자 잔고 비율", max_length=112)
    etf_cu_unit_scrt_cnt: str = Field(title="전체 융자 공여율", max_length=18)
    etf_cnfg_issu_cnt: str = Field(title="전체 대주 신규 주수", max_length=18)

class DomesticEtfComponentStockPriceItem2(BaseModel):
    """국내ETF 구성종목시세 아이템2"""

    stck_shrn_iscd: str = Field(title="주식 단축 종목코드", max_length=9)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    stck_prpr: str = Field(title="주식 현재가", max_length=10)
    prdy_vrss: str = Field(title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=18)
    tday_rsfl_rate: str = Field(title="당일 등락 비율", max_length=52)
    prdy_vrss_vol: str = Field(title="전일 대비 거래량", max_length=18)
    tr_pbmn_tnrt: str = Field(title="거래대금회전율", max_length=82)
    hts_avls: str = Field(title="HTS 시가총액", max_length=18)
    etf_cnfg_issu_avls: str = Field(title="ETF구성종목시가총액", max_length=18)
    etf_cnfg_issu_rlim: str = Field(title="ETF구성종목비중", max_length=72)
    etf_vltn_amt: str = Field(title="ETF구성종목내평가금액", max_length=18)


class DomesticEtfComponentStockPrice(BaseModel, KisHttpBody):
    """국내ETF 구성종목시세"""

    output1: DomesticEtfComponentStockPriceItem1 = Field(title="응답상세1")
    output2: Sequence[DomesticEtfComponentStockPriceItem2] = Field(default_factory=list)


class DomesticEtfNavComparisonTrendItem1(BaseModel):
    """국내ETF NAV 비교추이(종목) 아이템"""

    stck_prpr: str = Field(title="주식 현재가", max_length=8)
    prdy_vrss: str = Field(title="전일 대비", max_length=8)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=2)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=4)
    acml_vol: str = Field(title="누적 거래량", max_length=12)
    acml_tr_pbmn: str = Field(title="누적 거래 대금", max_length=60)
    stck_prdy_clpr: str = Field(title="주식 전일 종가", max_length=10)
    stck_oprc: str = Field(title="주식 시가2", max_length=10)
    stck_hgpr: str = Field(title="주식 최고가", max_length=10)
    stck_lwpr: str = Field(title="주식 최저가", max_length=10)
    stck_mxpr: str = Field(title="주식 상한가", max_length=10)
    stck_llam: str = Field(title="주식 하한가", max_length=10)

class DomesticEtfNavComparisonTrendItem2(BaseModel):
    """국내ETF NAV 비교추이(종목) 아이템2"""

    nav: str = Field(title="NAV", max_length=11)
    nav_prdy_vrss_sign: str = Field(title="NAV 전일 대비 부호", max_length=1)
    nav_prdy_vrss: str = Field(title="NAV 전일 대비", max_length=11)
    nav_prdy_ctrt: str = Field(title="NAV 전일 대비율", max_length=8)
    prdy_clpr_nav: str = Field(title="NAV전일종가", max_length=11)
    oprc_nav: str = Field(title="NAV시가", max_length=11)
    hprc_nav: str = Field(title="NAV고가", max_length=11)
    lprc_nav: str = Field(title="NAV저가", max_length=11)

class DomesticEtfNavComparisonTrend(BaseModel, KisHttpBody):
    """국내ETF NAV 비교추이(종목)"""

    output1: DomesticEtfNavComparisonTrendItem1 = Field(title="응답상세1")
    output2: DomesticEtfNavComparisonTrendItem2 = Field(title="응답상세2")


class DomesticEtfNavComparisonDailyTrendItem(BaseModel):
    stck_bsop_date: str = Field(alias="stck_bsop_date", title="주식 영업 일자", max_length=8)
    stck_clpr: str = Field(alias="stck_clpr", title="주식 종가", max_length=10)
    prdy_vrss: str = Field(alias="prdy_vrss", title="전일 대비", max_length=10)
    prdy_vrss_sign: str = Field(alias="prdy_vrss_sign", title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(alias="prdy_ctrt", title="전일 대비율", max_length=82)
    acml_vol: str = Field(alias="acml_vol", title="누적 거래량", max_length=18)
    cntg_vol: str = Field(alias="cntg_vol", title="체결 거래량", max_length=18)
    dprt: str = Field(alias="dprt", title="괴리율", max_length=82)
    nav_vrss_prpr: str = Field(alias="nav_vrss_prpr", title="NAV 대비 현재가", max_length=112)
    nav: str = Field(alias="nav", title="NAV", max_length=112)
    nav_prdy_vrss_sign: str = Field(alias="nav_prdy_vrss_sign", title="NAV 전일 대비 부호", max_length=1)
    nav_prdy_vrss: str = Field(alias="nav_prdy_vrss", title="NAV 전일 대비", max_length=112)
    nav_prdy_ctrt: str = Field(alias="nav_prdy_ctrt", title="NAV 전일 대비율", max_length=84)


class DomesticEtfNavComparisonDailyTrend(BaseModel, KisHttpBody):
    """국내ETF NAV 비교추이(일)"""

    output: Sequence[DomesticEtfNavComparisonDailyTrendItem] = Field(default_factory=list)


class DomesticEtfNavComparisonTimeTrendItem(BaseModel):
    """국내ETF NAV 비교추이(시간) 아이템"""

    bsop_hour: str = Field(description="영업 시간")
    nav: str = Field(description="NAV")
    nav_prdy_vrss_sign: str = Field(description="NAV 전일 대비 부호")
    nav_prdy_vrss: str = Field(description="NAV 전일 대비")
    nav_prdy_ctrt: str = Field(description="NAV 전일 대비율")
    nav_vrss_prpr: str = Field(description="NAV 대비 현재가")
    dprt: str = Field(description="괴리율")
    stck_prpr: str = Field(description="주식 현재가")
    prdy_vrss: str = Field(description="전일 대비")
    prdy_vrss_sign: str = Field(description="전일 대비 부호")
    prdy_ctrt: str = Field(description="전일 대비율")
    acml_vol: str = Field(description="누적 거래량")
    cntg_vol: str = Field(description="체결 거래량")


class DomesticEtfNavComparisonTimeTrend(BaseModel, KisHttpBody):
    """국내ETF NAV 비교추이(시간)"""

    output: Sequence[DomesticEtfNavComparisonTimeTrendItem] = Field(default_factory=list)
