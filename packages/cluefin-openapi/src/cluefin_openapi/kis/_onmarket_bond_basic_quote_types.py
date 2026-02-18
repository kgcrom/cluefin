from typing import Optional, Sequence

from pydantic import BaseModel, Field

from cluefin_openapi.kis._model import KisHttpBody


class OnmarketBondAskingPriceItem(BaseModel):
    """장내채권현재가(호가) 응답 항목"""

    aspr_acpt_hour: str = Field(title="호가 접수 시간", max_length=6)
    bond_askp1: str = Field(title="채권 매도호가1", max_length=20)
    bond_askp2: str = Field(title="채권 매도호가2", max_length=20)
    bond_askp3: str = Field(title="채권 매도호가3", max_length=20)
    bond_askp4: str = Field(title="채권 매도호가4", max_length=20)
    bond_askp5: str = Field(title="채권 매도호가5", max_length=20)
    bond_bidp1: str = Field(title="채권 매수호가1", max_length=20)
    bond_bidp2: str = Field(title="채권 매수호가2", max_length=20)
    bond_bidp3: str = Field(title="채권 매수호가3", max_length=20)
    bond_bidp4: str = Field(title="채권 매수호가4", max_length=20)
    bond_bidp5: str = Field(title="채권 매수호가5", max_length=20)
    askp_rsqn1: str = Field(title="매도호가 잔량1", max_length=12)
    askp_rsqn2: str = Field(title="매도호가 잔량2", max_length=12)
    askp_rsqn3: str = Field(title="매도호가 잔량3", max_length=12)
    askp_rsqn4: str = Field(title="매도호가 잔량4", max_length=12)
    askp_rsqn5: str = Field(title="매도호가 잔량5", max_length=12)
    bidp_rsqn1: str = Field(title="매수호가 잔량1", max_length=12)
    bidp_rsqn2: str = Field(title="매수호가 잔량2", max_length=12)
    bidp_rsqn3: str = Field(title="매수호가 잔량3", max_length=12)
    bidp_rsqn4: str = Field(title="매수호가 잔량4", max_length=12)
    bidp_rsqn5: str = Field(title="매수호가 잔량5", max_length=12)
    total_askp_rsqn: str = Field(title="총 매도호가 잔량", max_length=12)
    total_bidp_rsqn: str = Field(title="총 매수호가 잔량", max_length=12)
    ntby_aspr_rsqn: str = Field(title="순매수 호가 잔량", max_length=12)
    seln_ernn_rate1: str = Field(title="매도 수익비율1", max_length=15)
    seln_ernn_rate2: str = Field(title="매도 수익비율2", max_length=15)
    seln_ernn_rate3: str = Field(title="매도 수익비율3", max_length=15)
    seln_ernn_rate4: str = Field(title="매도 수익비율4", max_length=15)
    seln_ernn_rate5: str = Field(title="매도 수익비율5", max_length=15)
    shnu_ernn_rate1: str = Field(title="매수 수익비율1", max_length=15)
    shnu_ernn_rate2: str = Field(title="매수 수익비율2", max_length=15)
    shnu_ernn_rate3: str = Field(title="매수 수익비율3", max_length=15)
    shnu_ernn_rate4: str = Field(title="매수 수익비율4", max_length=15)
    shnu_ernn_rate5: str = Field(title="매수 수익비율5", max_length=15)


class OnmarketBondAskingPrice(BaseModel, KisHttpBody):
    """장내채권현재가(호가)"""

    output: Optional[OnmarketBondAskingPriceItem] = Field(default=None, title="응답상세")


class OnmarketBondPriceItem(BaseModel):
    """장내채권현재가(시세) 응답 항목"""

    stnd_iscd: str = Field(title="표준종목코드", max_length=12)
    hts_kor_isnm: str = Field(title="HTS한글종목명", max_length=40)
    bond_prpr: str = Field(title="채권현재가", max_length=112)
    prdy_vrss_sign: str = Field(title="전일대비부호", max_length=1)
    bond_prdy_vrss: str = Field(title="채권전일대비", max_length=112)
    prdy_ctrt: str = Field(title="전일대비율", max_length=82)
    acml_vol: str = Field(title="누적거래량", max_length=18)
    bond_prdy_clpr: str = Field(title="채권전일종가", max_length=112)
    bond_oprc: str = Field(title="채권시가2", max_length=112)
    bond_hgpr: str = Field(title="채권고가", max_length=112)
    bond_lwpr: str = Field(title="채권저가", max_length=112)
    ernn_rate: str = Field(title="수익비율", max_length=84)
    oprc_ert: str = Field(title="시가2수익률", max_length=72)
    hgpr_ert: str = Field(title="최고가수익률", max_length=72)
    lwpr_ert: str = Field(title="최저가수익률", max_length=72)
    bond_mxpr: str = Field(title="채권상한가", max_length=112)
    bond_llam: str = Field(title="채권하한가", max_length=112)


class OnmarketBondPrice(BaseModel, KisHttpBody):
    """장내채권현재가(시세)"""

    output: Optional[OnmarketBondPriceItem] = Field(default=None, title="응답상세")


class OnmarketBondExecutionItem(BaseModel):
    """장내채권현재가(체결) 응답 항목"""

    stck_cntg_hour: str = Field(title="주식 체결 시간", max_length=6)
    bond_prpr: str = Field(title="채권 현재가", max_length=112)
    bond_prdy_vrss: str = Field(title="채권 전일 대비", max_length=112)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    cntg_vol: str = Field(title="체결 거래량", max_length=18)
    acml_vol: str = Field(title="누적 거래량", max_length=18)


class OnmarketBondExecution(BaseModel, KisHttpBody):
    """장내채권현재가(체결)"""

    output: Optional[OnmarketBondExecutionItem] = Field(default=None, title="응답상세")


class OnmarketBondDailyPriceItem(BaseModel):
    """장내채권현재가(일별) 응답 항목"""

    stck_bsop_date: str = Field(title="주식 영업 일자", max_length=8)
    bond_prpr: str = Field(title="채권 현재가", max_length=112)
    bond_prdy_vrss: str = Field(title="채권 전일 대비", max_length=112)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    bond_oprc: str = Field(title="채권 시가", max_length=112)
    bond_hgpr: str = Field(title="채권 고가", max_length=112)
    bond_lwpr: str = Field(title="채권 저가", max_length=112)


class OnmarketBondDailyPrice(BaseModel, KisHttpBody):
    """장내채권현재가(일별)"""

    output: Sequence[OnmarketBondDailyPriceItem] = Field(default_factory=list)


class OnmarketBondDailyChartPriceItem(BaseModel):
    """장내채권 기간별시세(일) 응답 항목"""

    stck_bsop_date: str = Field(title="주식영업일자", max_length=8)
    bond_oprc: str = Field(title="채권시가2", max_length=112)
    bond_hgpr: str = Field(title="채권고가", max_length=112)
    bond_lwpr: str = Field(title="채권저가", max_length=112)
    bond_prpr: str = Field(title="채권현재가", max_length=112)
    acml_vol: str = Field(title="누적거래량", max_length=18)


class OnmarketBondDailyChartPrice(BaseModel, KisHttpBody):
    """장내채권 기간별시세(일)"""

    output: list[OnmarketBondDailyChartPriceItem] = Field(default_factory=list, title="응답상세")


class OnmarketBondAvgUnitPriceOutput1Item(BaseModel):
    """장내채권 평균단가조회 output1 항목 (단가/수익율)"""

    evlu_dt: str = Field(title="평가일자", max_length=8)
    pdno: str = Field(title="상품번호", max_length=12)
    prdt_type_cd: str = Field(title="상품유형코드", max_length=3)
    prdt_name: str = Field(title="상품명", max_length=60)
    kis_unpr: str = Field(title="KIS단가", max_length=24)
    kbp_unpr: str = Field(title="KBP단가", max_length=24)
    nice_evlu_unpr: str = Field(title="NICE평가단가", max_length=24)
    fnp_unpr: str = Field(title="FnP단가", max_length=24)
    avg_evlu_unpr: str = Field(title="평균평가단가", max_length=24)
    kis_crdt_grad_text: str = Field(title="KIS신용등급텍스트", max_length=40)
    kbp_crdt_grad_text: str = Field(title="KBP신용등급텍스트", max_length=40)
    nice_crdt_grad_text: str = Field(title="NICE신용등급텍스트", max_length=40)
    fnp_crdt_grad_text: str = Field(title="FnP신용등급텍스트", max_length=40)
    chng_yn: str = Field(title="변경여부", max_length=1)
    kis_erng_rt: str = Field(title="KIS수익률", max_length=24)
    kbp_erng_rt: str = Field(title="KBP수익률", max_length=24)
    nice_evlu_erng_rt: str = Field(title="NICE평가수익률", max_length=24)
    fnp_erng_rt: str = Field(title="FnP수익률", max_length=24)
    avg_evlu_erng_rt: str = Field(title="평균평가수익률", max_length=24)
    kis_rf_unpr: str = Field(title="KIS기준단가", max_length=24)
    kbp_rf_unpr: str = Field(title="KBP기준단가", max_length=24)
    nice_evlu_rf_unpr: str = Field(title="NICE평가기준단가", max_length=24)
    avg_evlu_rf_unpr: str = Field(title="평균평가기준단가", max_length=24)


class OnmarketBondAvgUnitPriceOutput2Item(BaseModel):
    """장내채권 평균단가조회 output2 항목 (평가금액)"""

    evlu_dt: str = Field(title="평가일자", max_length=8)
    pdno: str = Field(title="상품번호", max_length=12)
    prdt_type_cd: str = Field(title="상품유형코드", max_length=3)
    prdt_name: str = Field(title="상품명", max_length=60)
    kis_evlu_amt: str = Field(title="KIS평가금액", max_length=24)
    kbp_evlu_amt: str = Field(title="KBP평가금액", max_length=24)
    nice_evlu_amt: str = Field(title="NICE평가금액", max_length=24)
    fnp_evlu_amt: str = Field(title="FnP평가금액", max_length=24)
    avg_evlu_amt: str = Field(title="평균평가금액", max_length=24)
    chng_yn: str = Field(title="변경여부", max_length=1)


class OnmarketBondAvgUnitPriceOutput3Item(BaseModel):
    """장내채권 평균단가조회 output3 항목 (외화평가)"""

    evlu_dt: str = Field(title="평가일자", max_length=8)
    pdno: str = Field(title="상품번호", max_length=12)
    prdt_type_cd: str = Field(title="상품유형코드", max_length=3)
    prdt_name: str = Field(title="상품명", max_length=60)
    kis_crcy_cd: str = Field(title="KIS통화코드", max_length=3)
    kis_evlu_unit_pric: str = Field(title="KIS평가단위가격", max_length=24)
    kis_evlu_pric: str = Field(title="KIS평가가격", max_length=24)
    kbp_crcy_cd: str = Field(title="KBP통화코드", max_length=3)
    kbp_evlu_unit_pric: str = Field(title="KBP평가단위가격", max_length=24)
    kbp_evlu_pric: str = Field(title="KBP평가가격", max_length=24)
    nice_crcy_cd: str = Field(title="NICE통화코드", max_length=3)
    nice_evlu_unit_pric: str = Field(title="NICE평가단위가격", max_length=24)
    nice_evlu_pric: str = Field(title="NICE평가가격", max_length=24)
    avg_evlu_unit_pric: str = Field(title="평균평가단위가격", max_length=24)
    avg_evlu_pric: str = Field(title="평균평가가격", max_length=24)
    chng_yn: str = Field(title="변경여부", max_length=1)


class OnmarketBondAvgUnitPrice(BaseModel, KisHttpBody):
    """장내채권 평균단가조회"""

    output1: list[OnmarketBondAvgUnitPriceOutput1Item] = Field(default_factory=list, title="단가/수익율")
    output2: list[OnmarketBondAvgUnitPriceOutput2Item] = Field(default_factory=list, title="평가금액")
    output3: list[OnmarketBondAvgUnitPriceOutput3Item] = Field(default_factory=list, title="외화평가")


class OnmarketBondIssueInfoOutput(BaseModel):
    """장내채권 발행정보 응답 항목"""

    pdno: str = Field(title="상품번호", max_length=12)
    prdt_type_cd: str = Field(title="상품유형코드", max_length=3)
    prdt_name: str = Field(title="상품명", max_length=60)
    prdt_eng_name: str = Field(title="상품영문명", max_length=60)
    ivst_heed_prdt_yn: str = Field(title="투자유의상품여부", max_length=1)
    exts_yn: str = Field(title="존재여부", max_length=1)
    bond_clsf_cd: str = Field(title="채권분류코드", max_length=6)
    bond_clsf_kor_name: str = Field(title="채권분류한글명", max_length=60)
    papr: str = Field(title="액면가", max_length=19)
    int_mned_dvsn_cd: str = Field(title="이자지급월구분코드", max_length=1)
    rvnu_shap_cd: str = Field(title="수익형태코드", max_length=1)
    issu_amt: str = Field(title="발행금액", max_length=19)
    lstg_rmnd: str = Field(title="상장잔액", max_length=19)
    int_dfrm_mcnt: str = Field(title="이자지급월수", max_length=6)
    bond_int_dfrm_mthd_cd: str = Field(title="채권이자지급방법코드", max_length=2)
    splt_rdpt_rcnt: str = Field(title="분할상환횟수", max_length=6)
    prca_dfmt_term_mcnt: str = Field(title="원금거치기간월수", max_length=6)
    int_anap_dvsn_cd: str = Field(title="이자선급구분코드", max_length=1)
    bond_rght_dvsn_cd: str = Field(title="채권권리구분코드", max_length=2)
    prdt_pclc_text: str = Field(title="상품특이사항텍스트", max_length=500)
    prdt_abrv_name: str = Field(title="상품약어명", max_length=60)
    prdt_eng_abrv_name: str = Field(title="상품영문약어명", max_length=60)
    sprx_psbl_yn: str = Field(title="분리과세가능여부", max_length=1)
    pbff_pplc_ofrg_mthd_cd: str = Field(title="공모사모공모방법코드", max_length=2)
    cmco_cd: str = Field(title="결제회사코드", max_length=4)
    issu_istt_cd: str = Field(title="발행기관코드", max_length=5)
    issu_istt_name: str = Field(title="발행기관명", max_length=60)
    pnia_dfrm_agcy_istt_cd: str = Field(title="원이지급대행기관코드", max_length=4)
    dsct_ec_rt: str = Field(title="할인경제비율", max_length=238)
    srfc_inrt: str = Field(title="표면이자율", max_length=238)
    expd_rdpt_rt: str = Field(title="만기상환율", max_length=238)
    expd_asrc_erng_rt: str = Field(title="만기보장수익률", max_length=238)
    bond_grte_istt_name: str = Field(title="채권보증기관명", max_length=60)
    int_dfrm_day_type_cd: str = Field(title="이자지급일유형코드", max_length=2)
    ksd_int_calc_unit_cd: str = Field(title="KSD이자계산단위코드", max_length=1)
    int_wunt_uder_prcs_dvsn_cd: str = Field(title="이자원단위미만처리구분코드", max_length=1)
    rvnu_dt: str = Field(title="수익일자", max_length=8)
    issu_dt: str = Field(title="발행일자", max_length=8)
    lstg_dt: str = Field(title="상장일자", max_length=8)
    expd_dt: str = Field(title="만기일자", max_length=8)
    rdpt_dt: str = Field(title="상환일자", max_length=8)
    sbst_pric: str = Field(title="대용가격", max_length=19)
    rgbf_int_dfrm_dt: str = Field(title="직전이자지급일자", max_length=8)
    nxtm_int_dfrm_dt: str = Field(title="차회이자지급일자", max_length=8)
    frst_int_dfrm_dt: str = Field(title="최초이자지급일자", max_length=8)
    ecis_pric: str = Field(title="전환가격", max_length=19)
    rght_stck_std_pdno: str = Field(title="권리주식표준상품번호", max_length=12)
    ecis_opng_dt: str = Field(title="전환개시일자", max_length=8)
    ecis_end_dt: str = Field(title="전환종료일자", max_length=8)
    bond_rvnu_mthd_cd: str = Field(title="채권수익방법코드", max_length=2)
    oprt_stfno: str = Field(title="운용직원번호", max_length=6)
    oprt_stff_name: str = Field(title="운용직원명", max_length=60)
    rgbf_int_dfrm_wday: str = Field(title="직전이자지급요일", max_length=2)
    nxtm_int_dfrm_wday: str = Field(title="차회이자지급요일", max_length=2)
    kis_crdt_grad_text: str = Field(title="KIS신용등급텍스트", max_length=500)
    kbp_crdt_grad_text: str = Field(title="KBP신용등급텍스트", max_length=500)
    nice_crdt_grad_text: str = Field(title="NICE신용등급텍스트", max_length=500)
    fnp_crdt_grad_text: str = Field(title="FnP신용등급텍스트", max_length=500)
    dpsi_psbl_yn: str = Field(title="예탁가능여부", max_length=1)
    pnia_int_calc_unpr: str = Field(title="원이계산단가", max_length=234)
    prcm_idx_bond_yn: str = Field(title="물가연동채권여부", max_length=1)
    expd_exts_srdp_rcnt: str = Field(title="만기연장분할상환횟수", max_length=10)
    expd_exts_srdp_rt: str = Field(title="만기연장분할상환율", max_length=2212)
    loan_psbl_yn: str = Field(title="대출가능여부", max_length=1)
    grte_dvsn_cd: str = Field(title="보증구분코드", max_length=1)
    fnrr_rank_dvsn_cd: str = Field(title="선후순위구분코드", max_length=1)
    krx_lstg_abol_dvsn_cd: str = Field(title="KRX상장폐지구분코드", max_length=1)
    asst_rqdi_dvsn_cd: str = Field(title="자산요구구분코드", max_length=2)
    opcb_dvsn_cd: str = Field(title="옵션부사채구분코드", max_length=1)
    crfd_item_yn: str = Field(title="신용공여대상여부", max_length=1)
    crfd_item_rstc_cclc_dt: str = Field(title="신용공여대상제한해제일자", max_length=8)
    bond_nmpr_unit_pric: str = Field(title="채권액면단위가격", max_length=202)
    ivst_heed_bond_dvsn_name: str = Field(title="투자유의채권구분명", max_length=60)
    add_erng_rt: str = Field(title="추가수익률", max_length=238)
    add_erng_rt_aply_dt: str = Field(title="추가수익률적용일자", max_length=8)
    bond_tr_stop_dvsn_cd: str = Field(title="채권거래정지구분코드", max_length=1)
    ivst_heed_bond_dvsn_cd: str = Field(title="투자유의채권구분코드", max_length=1)
    pclr_cndt_text: str = Field(title="특이조건텍스트", max_length=500)
    hbbd_yn: str = Field(title="하이브리드채권여부", max_length=1)
    cdtl_cptl_scty_type_cd: str = Field(title="조건부자본증권유형코드", max_length=1)
    elec_scty_yn: str = Field(title="전자증권여부", max_length=1)
    sq1_clop_ecis_opng_dt: str = Field(title="SQ1종가전환개시일자", max_length=8)
    frst_erlm_stfno: str = Field(title="최초등록직원번호", max_length=6)
    frst_erlm_dt: str = Field(title="최초등록일자", max_length=8)
    frst_erlm_tmd: str = Field(title="최초등록시각", max_length=6)
    tlg_rcvg_dtl_dtime: str = Field(title="전문수신상세일시", max_length=17)


class OnmarketBondIssueInfo(BaseModel, KisHttpBody):
    """장내채권 발행정보"""

    output: Optional[OnmarketBondIssueInfoOutput] = Field(default=None, title="응답상세")


class OnmarketBondInfoItem(BaseModel):
    """장내채권 기본조회 응답 항목"""

    pdno: str = Field(title="상품번호", max_length=12)
    prdt_type_cd: str = Field(title="상품유형코드", max_length=3)
    ksd_bond_item_name: str = Field(title="증권예탁결제원채권종목명", max_length=100)
    ksd_bond_item_eng_name: str = Field(title="증권예탁결제원채권종목영문명", max_length=100)
    ksd_bond_lstg_type_cd: str = Field(title="증권예탁결제원채권상장유형코드", max_length=2)
    ksd_ofrg_dvsn_cd: str = Field(title="증권예탁결제원모집구분코드", max_length=2)
    ksd_bond_int_dfrm_dvsn_cd: str = Field(title="증권예탁결제원채권이자지급구분", max_length=1)
    issu_dt: str = Field(title="발행일자", max_length=8)
    rdpt_dt: str = Field(title="상환일자", max_length=8)
    rvnu_dt: str = Field(title="매출일자", max_length=8)
    iso_crcy_cd: str = Field(title="통화코드", max_length=3)
    mdwy_rdpt_dt: str = Field(title="중도상환일자", max_length=8)
    ksd_rcvg_bond_dsct_rt: str = Field(title="증권예탁결제원수신채권할인율", max_length=22)
    ksd_rcvg_bond_srfc_inrt: str = Field(title="증권예탁결제원수신채권표면이율", max_length=20)
    bond_expd_rdpt_rt: str = Field(title="채권만기상환율", max_length=22)
    ksd_prca_rdpt_mthd_cd: str = Field(title="증권예탁결제원원금상환방법코드", max_length=2)
    int_caltm_mcnt: str = Field(title="이자계산기간개월수", max_length=10)
    ksd_int_calc_unit_cd: str = Field(title="증권예탁결제원이자계산단위코드", max_length=1)
    uval_cut_dvsn_cd: str = Field(title="절상절사구분코드", max_length=1)
    uval_cut_dcpt_dgit: str = Field(title="절상절사소수점자릿수", max_length=10)
    ksd_dydv_caltm_aply_dvsn_cd: str = Field(title="증권예탁결제원일할계산기간적용구분코드", max_length=1)
    dydv_calc_dcnt: str = Field(title="일할계산일수", max_length=5)
    bond_expd_asrc_erng_rt: str = Field(title="채권만기보장수익율", max_length=22)
    padf_plac_hdof_name: str = Field(title="원리금지급장소본점명", max_length=60)
    lstg_dt: str = Field(title="상장일자", max_length=8)
    lstg_abol_dt: str = Field(title="상장폐지일자", max_length=8)
    ksd_bond_issu_mthd_cd: str = Field(title="증권예탁결제원채권발행방법코드", max_length=1)
    laps_indf_yn: str = Field(title="경과이자지급여부", max_length=1)
    ksd_lhdy_pnia_dfrm_mthd_cd: str = Field(title="증권예탁결제원공휴일원리금지급방법코드", max_length=1)
    frst_int_dfrm_dt: str = Field(title="최초이자지급일자", max_length=8)
    ksd_prcm_lnkg_gvbd_yn: str = Field(title="증권예탁결제원물가연동국고채여부", max_length=1)
    dpsi_end_dt: str = Field(title="예탁종료일자", max_length=8)
    dpsi_strt_dt: str = Field(title="예탁시작일자", max_length=8)
    dpsi_psbl_yn: str = Field(title="예탁가능여부", max_length=1)
    atyp_rdpt_bond_erlm_yn: str = Field(title="비정형상환채권등록여부", max_length=1)
    dshn_occr_yn: str = Field(title="부도발생여부", max_length=1)
    expd_exts_yn: str = Field(title="만기연장여부", max_length=1)
    pclr_ptcr_text: str = Field(title="특이사항내용", max_length=500)
    dpsi_psbl_excp_stat_cd: str = Field(title="예탁가능예외상태코드", max_length=2)
    expd_exts_srdp_rcnt: str = Field(title="만기연장분할상환횟수", max_length=10)
    expd_exts_srdp_rt: str = Field(title="만기연장분할상환율", max_length=22)
    expd_rdpt_rt: str = Field(title="만기상환율", max_length=23)
    expd_asrc_erng_rt: str = Field(title="만기보장수익율", max_length=23)
    bond_int_dfrm_mthd_cd: str = Field(title="채권이자지급방법코드", max_length=2)
    int_dfrm_day_type_cd: str = Field(title="이자지급일유형코드", max_length=2)
    prca_dfmt_term_mcnt: str = Field(title="원금거치기간개월수", max_length=6)
    splt_rdpt_rcnt: str = Field(title="분할상환횟수", max_length=6)
    rgbf_int_dfrm_dt: str = Field(title="직전이자지급일자", max_length=8)
    nxtm_int_dfrm_dt: str = Field(title="차기이자지급일자", max_length=8)
    sprx_psbl_yn: str = Field(title="분리과세가능여부", max_length=1)
    ictx_rt_dvsn_cd: str = Field(title="소득세율구분코드", max_length=2)
    bond_clsf_cd: str = Field(title="채권분류코드", max_length=6)
    bond_clsf_kor_name: str = Field(title="채권분류한글명", max_length=60)
    int_mned_dvsn_cd: str = Field(title="이자월말구분코드", max_length=1)
    pnia_int_calc_unpr: str = Field(title="원리금이자계산단가", max_length=23)
    frn_intr: str = Field(title="FRN금리", max_length=15)
    aply_day_prcm_idx_lnkg_cefc: str = Field(title="적용일물가지수연동계수", max_length=15)
    ksd_expd_dydv_calc_bass_cd: str = Field(title="증권예탁결제원만기일할계산기준코드", max_length=1)
    expd_dydv_calc_dcnt: str = Field(title="만기일할계산일수", max_length=7)
    ksd_cbbw_dvsn_cd: str = Field(title="증권예탁결제원신종사채구분코드", max_length=1)
    crfd_item_yn: str = Field(title="크라우드펀딩종목여부", max_length=1)
    pnia_bank_ofdy_dfrm_mthd_cd: str = Field(title="원리금은행휴무일지급방법코드", max_length=1)
    qib_yn: str = Field(title="QIB여부", max_length=1)
    qib_cclc_dt: str = Field(title="QIB해지일자", max_length=8)
    csbd_yn: str = Field(title="영구채여부", max_length=1)
    csbd_cclc_dt: str = Field(title="영구채해지일자", max_length=8)
    ksd_opcb_yn: str = Field(title="증권예탁결제원옵션부사채여부", max_length=1)
    ksd_sodn_yn: str = Field(title="증권예탁결제원후순위채권여부", max_length=1)
    ksd_rqdi_scty_yn: str = Field(title="증권예탁결제원유동화증권여부", max_length=1)
    elec_scty_yn: str = Field(title="전자증권여부", max_length=1)
    rght_ecis_mbdy_dvsn_cd: str = Field(title="권리행사주체구분코드", max_length=1)
    int_rkng_mthd_dvsn_cd: str = Field(title="이자산정방법구분코드", max_length=1)
    ofrg_dvsn_cd: str = Field(title="모집구분코드", max_length=2)
    ksd_tot_issu_amt: str = Field(title="증권예탁결제원총발행금액", max_length=20)
    next_indf_chk_ecls_yn: str = Field(title="다음이자지급체크제외여부", max_length=1)
    ksd_bond_intr_dvsn_cd: str = Field(title="증권예탁결제원채권금리구분코드", max_length=1)
    ksd_inrt_aply_dvsn_cd: str = Field(title="증권예탁결제원이율적용구분코드", max_length=1)
    krx_issu_istt_cd: str = Field(title="KRX발행기관코드", max_length=5)
    ksd_indf_frqc_uder_calc_cd: str = Field(title="증권예탁결제원이자지급주기미만계산코드", max_length=1)
    ksd_indf_frqc_uder_calc_dcnt: str = Field(title="증권예탁결제원이자지급주기미만계산일수", max_length=4)
    tlg_rcvg_dtl_dtime: str = Field(title="전문수신상세일시", max_length=17)


class OnmarketBondInfo(BaseModel, KisHttpBody):
    """장내채권 기본조회"""

    output: Optional[OnmarketBondInfoItem] = Field(default=None, title="응답상세")
