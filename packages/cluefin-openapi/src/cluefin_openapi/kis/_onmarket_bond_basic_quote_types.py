from typing import Optional

from pydantic import BaseModel, Field

from cluefin_openapi.kis._model import KisHttpBody


class OnmarketBondAskingPriceItem(BaseModel):
    """장내채권현재가(호가) 응답 항목"""

    aspr_acpt_hour: str = Field(title="호가 접수 시간")
    bond_askp1: str = Field(title="채권 매도호가1")
    bond_askp2: str = Field(title="채권 매도호가2")
    bond_askp3: str = Field(title="채권 매도호가3")
    bond_askp4: str = Field(title="채권 매도호가4")
    bond_askp5: str = Field(title="채권 매도호가5")
    bond_bidp1: str = Field(title="채권 매수호가1")
    bond_bidp2: str = Field(title="채권 매수호가2")
    bond_bidp3: str = Field(title="채권 매수호가3")
    bond_bidp4: str = Field(title="채권 매수호가4")
    bond_bidp5: str = Field(title="채권 매수호가5")
    askp_rsqn1: str = Field(title="매도호가 잔량1")
    askp_rsqn2: str = Field(title="매도호가 잔량2")
    askp_rsqn3: str = Field(title="매도호가 잔량3")
    askp_rsqn4: str = Field(title="매도호가 잔량4")
    askp_rsqn5: str = Field(title="매도호가 잔량5")
    bidp_rsqn1: str = Field(title="매수호가 잔량1")
    bidp_rsqn2: str = Field(title="매수호가 잔량2")
    bidp_rsqn3: str = Field(title="매수호가 잔량3")
    bidp_rsqn4: str = Field(title="매수호가 잔량4")
    bidp_rsqn5: str = Field(title="매수호가 잔량5")
    total_askp_rsqn: str = Field(title="총 매도호가 잔량")
    total_bidp_rsqn: str = Field(title="총 매수호가 잔량")
    ntby_aspr_rsqn: str = Field(title="순매수 호가 잔량")
    seln_ernn_rate1: str = Field(title="매도 수익비율1")
    seln_ernn_rate2: str = Field(title="매도 수익비율2")
    seln_ernn_rate3: str = Field(title="매도 수익비율3")
    seln_ernn_rate4: str = Field(title="매도 수익비율4")
    seln_ernn_rate5: str = Field(title="매도 수익비율5")
    shnu_ernn_rate1: str = Field(title="매수 수익비율1")
    shnu_ernn_rate2: str = Field(title="매수 수익비율2")
    shnu_ernn_rate3: str = Field(title="매수 수익비율3")
    shnu_ernn_rate4: str = Field(title="매수 수익비율4")
    shnu_ernn_rate5: str = Field(title="매수 수익비율5")


class OnmarketBondAskingPrice(BaseModel, KisHttpBody):
    """장내채권현재가(호가)"""

    output: Optional[OnmarketBondAskingPriceItem] = Field(default=None, title="응답상세")


class OnmarketBondPriceItem(BaseModel):
    """장내채권현재가(시세) 응답 항목"""

    stnd_iscd: str = Field(title="표준종목코드")
    hts_kor_isnm: str = Field(title="HTS한글종목명")
    bond_prpr: str = Field(title="채권현재가")
    prdy_vrss_sign: str = Field(title="전일대비부호")
    bond_prdy_vrss: str = Field(title="채권전일대비")
    prdy_ctrt: str = Field(title="전일대비율")
    acml_vol: str = Field(title="누적거래량")
    bond_prdy_clpr: str = Field(title="채권전일종가")
    bond_oprc: str = Field(title="채권시가2")
    bond_hgpr: str = Field(title="채권고가")
    bond_lwpr: str = Field(title="채권저가")
    ernn_rate: str = Field(title="수익비율")
    oprc_ert: str = Field(title="시가2수익률")
    hgpr_ert: str = Field(title="최고가수익률")
    lwpr_ert: str = Field(title="최저가수익률")
    bond_mxpr: str = Field(title="채권상한가")
    bond_llam: str = Field(title="채권하한가")


class OnmarketBondPrice(BaseModel, KisHttpBody):
    """장내채권현재가(시세)"""

    output: Optional[OnmarketBondPriceItem] = Field(default=None, title="응답상세")


class OnmarketBondExecutionItem(BaseModel):
    """장내채권현재가(체결) 응답 항목"""

    stck_cntg_hour: str = Field(title="주식 체결 시간")
    bond_prpr: str = Field(title="채권 현재가")
    bond_prdy_vrss: str = Field(title="채권 전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_ctrt: str = Field(title="전일 대비율")
    cntg_vol: str = Field(title="체결 거래량")
    acml_vol: str = Field(title="누적 거래량")


class OnmarketBondExecution(BaseModel, KisHttpBody):
    """장내채권현재가(체결)"""

    output: list[OnmarketBondExecutionItem] = Field(default_factory=list, title="응답상세")


class OnmarketBondDailyPriceItem(BaseModel):
    """장내채권현재가(일별) 응답 항목"""

    stck_bsop_date: str = Field(title="주식 영업 일자")
    bond_prpr: str = Field(title="채권 현재가")
    bond_prdy_vrss: str = Field(title="채권 전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_ctrt: str = Field(title="전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    bond_oprc: str = Field(title="채권 시가")
    bond_hgpr: str = Field(title="채권 고가")
    bond_lwpr: str = Field(title="채권 저가")


class OnmarketBondDailyPrice(BaseModel, KisHttpBody):
    """장내채권현재가(일별)"""

    output: list[OnmarketBondDailyPriceItem] = Field(default_factory=list, title="응답상세")


class OnmarketBondDailyChartPriceItem(BaseModel):
    """장내채권 기간별시세(일) 응답 항목"""

    stck_bsop_date: str = Field(title="주식영업일자")
    bond_oprc: str = Field(title="채권시가2")
    bond_hgpr: str = Field(title="채권고가")
    bond_lwpr: str = Field(title="채권저가")
    bond_prpr: str = Field(title="채권현재가")
    acml_vol: str = Field(title="누적거래량")


class OnmarketBondDailyChartPrice(BaseModel, KisHttpBody):
    """장내채권 기간별시세(일)"""

    output: list[OnmarketBondDailyChartPriceItem] = Field(default_factory=list, title="응답상세")


class OnmarketBondAvgUnitPriceOutput1Item(BaseModel):
    """장내채권 평균단가조회 output1 항목 (단가/수익율)"""

    evlu_dt: str = Field(title="평가일자")
    pdno: str = Field(title="상품번호")
    prdt_type_cd: str = Field(title="상품유형코드")
    prdt_name: str = Field(title="상품명")
    kis_unpr: str = Field(title="KIS단가")
    kbp_unpr: str = Field(title="KBP단가")
    nice_evlu_unpr: str = Field(title="NICE평가단가")
    fnp_unpr: str = Field(title="FnP단가")
    avg_evlu_unpr: str = Field(title="평균평가단가")
    kis_crdt_grad_text: str = Field(title="KIS신용등급텍스트")
    kbp_crdt_grad_text: str = Field(title="KBP신용등급텍스트")
    nice_crdt_grad_text: str = Field(title="NICE신용등급텍스트")
    fnp_crdt_grad_text: str = Field(title="FnP신용등급텍스트")
    chng_yn: str = Field(title="변경여부")
    kis_erng_rt: str = Field(title="KIS수익률")
    kbp_erng_rt: str = Field(title="KBP수익률")
    nice_evlu_erng_rt: str = Field(title="NICE평가수익률")
    fnp_erng_rt: str = Field(title="FnP수익률")
    avg_evlu_erng_rt: str = Field(title="평균평가수익률")
    kis_rf_unpr: str = Field(title="KIS기준단가")
    kbp_rf_unpr: str = Field(title="KBP기준단가")
    nice_evlu_rf_unpr: str = Field(title="NICE평가기준단가")
    avg_evlu_rf_unpr: str = Field(title="평균평가기준단가")


class OnmarketBondAvgUnitPriceOutput2Item(BaseModel):
    """장내채권 평균단가조회 output2 항목 (평가금액)"""

    evlu_dt: str = Field(title="평가일자")
    pdno: str = Field(title="상품번호")
    prdt_type_cd: str = Field(title="상품유형코드")
    prdt_name: str = Field(title="상품명")
    kis_evlu_amt: str = Field(title="KIS평가금액")
    kbp_evlu_amt: str = Field(title="KBP평가금액")
    nice_evlu_amt: str = Field(title="NICE평가금액")
    fnp_evlu_amt: str = Field(title="FnP평가금액")
    avg_evlu_amt: str = Field(title="평균평가금액")
    chng_yn: str = Field(title="변경여부")


class OnmarketBondAvgUnitPriceOutput3Item(BaseModel):
    """장내채권 평균단가조회 output3 항목 (외화평가)"""

    evlu_dt: str = Field(title="평가일자")
    pdno: str = Field(title="상품번호")
    prdt_type_cd: str = Field(title="상품유형코드")
    prdt_name: str = Field(title="상품명")
    kis_crcy_cd: str = Field(title="KIS통화코드")
    kis_evlu_unit_pric: str = Field(title="KIS평가단위가격")
    kis_evlu_pric: str = Field(title="KIS평가가격")
    kbp_crcy_cd: str = Field(title="KBP통화코드")
    kbp_evlu_unit_pric: str = Field(title="KBP평가단위가격")
    kbp_evlu_pric: str = Field(title="KBP평가가격")
    nice_crcy_cd: str = Field(title="NICE통화코드")
    nice_evlu_unit_pric: str = Field(title="NICE평가단위가격")
    nice_evlu_pric: str = Field(title="NICE평가가격")
    avg_evlu_unit_pric: str = Field(title="평균평가단위가격")
    avg_evlu_pric: str = Field(title="평균평가가격")
    chng_yn: str = Field(title="변경여부")


class OnmarketBondAvgUnitPrice(BaseModel, KisHttpBody):
    """장내채권 평균단가조회"""

    ctx_area_fk100: str = Field(default="", title="연속조회검색조건100")
    ctx_area_nk30: str = Field(default="", title="연속조회키30")
    output1: list[OnmarketBondAvgUnitPriceOutput1Item] = Field(default_factory=list, title="단가/수익율")
    output2: list[OnmarketBondAvgUnitPriceOutput2Item] = Field(default_factory=list, title="평가금액")
    output3: list[OnmarketBondAvgUnitPriceOutput3Item] = Field(default_factory=list, title="외화평가")


class OnmarketBondIssueInfoOutput(BaseModel):
    """장내채권 발행정보 응답 항목"""

    pdno: str = Field(title="상품번호")
    prdt_type_cd: str = Field(title="상품유형코드")
    prdt_name: str = Field(title="상품명")
    prdt_eng_name: str = Field(title="상품영문명")
    ivst_heed_prdt_yn: str = Field(title="투자유의상품여부")
    exts_yn: str = Field(title="존재여부")
    bond_clsf_cd: str = Field(title="채권분류코드")
    bond_clsf_kor_name: str = Field(title="채권분류한글명")
    papr: str = Field(title="액면가")
    int_mned_dvsn_cd: str = Field(title="이자지급월구분코드")
    rvnu_shap_cd: str = Field(title="수익형태코드")
    issu_amt: str = Field(title="발행금액")
    lstg_rmnd: str = Field(title="상장잔액")
    int_dfrm_mcnt: str = Field(title="이자지급월수")
    bond_int_dfrm_mthd_cd: str = Field(title="채권이자지급방법코드")
    splt_rdpt_rcnt: str = Field(title="분할상환횟수")
    prca_dfmt_term_mcnt: str = Field(title="원금거치기간월수")
    int_anap_dvsn_cd: str = Field(title="이자선급구분코드")
    bond_rght_dvsn_cd: str = Field(title="채권권리구분코드")
    prdt_pclc_text: str = Field(title="상품특이사항텍스트")
    prdt_abrv_name: str = Field(title="상품약어명")
    prdt_eng_abrv_name: str = Field(title="상품영문약어명")
    sprx_psbl_yn: str = Field(title="분리과세가능여부")
    pbff_pplc_ofrg_mthd_cd: str = Field(title="공모사모공모방법코드")
    cmco_cd: str = Field(title="결제회사코드")
    issu_istt_cd: str = Field(title="발행기관코드")
    issu_istt_name: str = Field(title="발행기관명")
    pnia_dfrm_agcy_istt_cd: str = Field(title="원이지급대행기관코드")
    dsct_ec_rt: str = Field(title="할인경제비율")
    srfc_inrt: str = Field(title="표면이자율")
    expd_rdpt_rt: str = Field(title="만기상환율")
    expd_asrc_erng_rt: str = Field(title="만기보장수익률")
    bond_grte_istt_name: str = Field(title="채권보증기관명")
    int_dfrm_day_type_cd: str = Field(title="이자지급일유형코드")
    ksd_int_calc_unit_cd: str = Field(title="KSD이자계산단위코드")
    int_wunt_uder_prcs_dvsn_cd: str = Field(title="이자원단위미만처리구분코드")
    rvnu_dt: str = Field(title="수익일자")
    issu_dt: str = Field(title="발행일자")
    lstg_dt: str = Field(title="상장일자")
    expd_dt: str = Field(title="만기일자")
    rdpt_dt: str = Field(title="상환일자")
    sbst_pric: str = Field(title="대용가격")
    rgbf_int_dfrm_dt: str = Field(title="직전이자지급일자")
    nxtm_int_dfrm_dt: str = Field(title="차회이자지급일자")
    frst_int_dfrm_dt: str = Field(title="최초이자지급일자")
    ecis_pric: str = Field(title="전환가격")
    rght_stck_std_pdno: str = Field(title="권리주식표준상품번호")
    ecis_opng_dt: str = Field(title="전환개시일자")
    ecis_end_dt: str = Field(title="전환종료일자")
    bond_rvnu_mthd_cd: str = Field(title="채권수익방법코드")
    oprt_stfno: str = Field(title="운용직원번호")
    oprt_stff_name: str = Field(title="운용직원명")
    rgbf_int_dfrm_wday: str = Field(title="직전이자지급요일")
    nxtm_int_dfrm_wday: str = Field(title="차회이자지급요일")
    kis_crdt_grad_text: str = Field(title="KIS신용등급텍스트")
    kbp_crdt_grad_text: str = Field(title="KBP신용등급텍스트")
    nice_crdt_grad_text: str = Field(title="NICE신용등급텍스트")
    fnp_crdt_grad_text: str = Field(title="FnP신용등급텍스트")
    dpsi_psbl_yn: str = Field(title="예탁가능여부")
    pnia_int_calc_unpr: str = Field(title="원이계산단가")
    prcm_idx_bond_yn: str = Field(title="물가연동채권여부")
    expd_exts_srdp_rcnt: str = Field(title="만기연장분할상환횟수")
    expd_exts_srdp_rt: str = Field(title="만기연장분할상환율")
    loan_psbl_yn: str = Field(title="대출가능여부")
    grte_dvsn_cd: str = Field(title="보증구분코드")
    fnrr_rank_dvsn_cd: str = Field(title="선후순위구분코드")
    krx_lstg_abol_dvsn_cd: str = Field(title="KRX상장폐지구분코드")
    asst_rqdi_dvsn_cd: str = Field(title="자산요구구분코드")
    opcb_dvsn_cd: str = Field(title="옵션부사채구분코드")
    crfd_item_yn: str = Field(title="신용공여대상여부")
    crfd_item_rstc_cclc_dt: str = Field(title="신용공여대상제한해제일자")
    bond_nmpr_unit_pric: str = Field(title="채권액면단위가격")
    ivst_heed_bond_dvsn_name: str = Field(title="투자유의채권구분명")
    add_erng_rt: str = Field(title="추가수익률")
    add_erng_rt_aply_dt: str = Field(title="추가수익률적용일자")
    bond_tr_stop_dvsn_cd: str = Field(title="채권거래정지구분코드")
    ivst_heed_bond_dvsn_cd: str = Field(title="투자유의채권구분코드")
    pclr_cndt_text: str = Field(title="특이조건텍스트")
    hbbd_yn: str = Field(title="하이브리드채권여부")
    cdtl_cptl_scty_type_cd: str = Field(title="조건부자본증권유형코드")
    elec_scty_yn: str = Field(title="전자증권여부")
    sq1_clop_ecis_opng_dt: str = Field(title="SQ1종가전환개시일자")
    frst_erlm_stfno: str = Field(title="최초등록직원번호")
    frst_erlm_dt: str = Field(title="최초등록일자")
    frst_erlm_tmd: str = Field(title="최초등록시각")
    tlg_rcvg_dtl_dtime: str = Field(title="전문수신상세일시")


class OnmarketBondIssueInfo(BaseModel, KisHttpBody):
    """장내채권 발행정보"""

    output: Optional[OnmarketBondIssueInfoOutput] = Field(default=None, title="응답상세")


class OnmarketBondInfoItem(BaseModel):
    """장내채권 기본조회 응답 항목"""

    pdno: str = Field(title="상품번호")
    prdt_type_cd: str = Field(title="상품유형코드")
    ksd_bond_item_name: str = Field(title="증권예탁결제원채권종목명")
    ksd_bond_item_eng_name: str = Field(title="증권예탁결제원채권종목영문명")
    ksd_bond_lstg_type_cd: str = Field(title="증권예탁결제원채권상장유형코드")
    ksd_ofrg_dvsn_cd: str = Field(title="증권예탁결제원모집구분코드")
    ksd_bond_int_dfrm_dvsn_cd: str = Field(title="증권예탁결제원채권이자지급구분")
    issu_dt: str = Field(title="발행일자")
    rdpt_dt: str = Field(title="상환일자")
    rvnu_dt: str = Field(title="매출일자")
    iso_crcy_cd: str = Field(title="통화코드")
    mdwy_rdpt_dt: str = Field(title="중도상환일자")
    ksd_rcvg_bond_dsct_rt: str = Field(title="증권예탁결제원수신채권할인율")
    ksd_rcvg_bond_srfc_inrt: str = Field(title="증권예탁결제원수신채권표면이율")
    bond_expd_rdpt_rt: str = Field(title="채권만기상환율")
    ksd_prca_rdpt_mthd_cd: str = Field(title="증권예탁결제원원금상환방법코드")
    int_caltm_mcnt: str = Field(title="이자계산기간개월수")
    ksd_int_calc_unit_cd: str = Field(title="증권예탁결제원이자계산단위코드")
    uval_cut_dvsn_cd: str = Field(title="절상절사구분코드")
    uval_cut_dcpt_dgit: str = Field(title="절상절사소수점자릿수")
    ksd_dydv_caltm_aply_dvsn_cd: str = Field(title="증권예탁결제원일할계산기간적용구분코드")
    dydv_calc_dcnt: str = Field(title="일할계산일수")
    bond_expd_asrc_erng_rt: str = Field(title="채권만기보장수익율")
    padf_plac_hdof_name: str = Field(title="원리금지급장소본점명")
    lstg_dt: str = Field(title="상장일자")
    lstg_abol_dt: str = Field(title="상장폐지일자")
    ksd_bond_issu_mthd_cd: str = Field(title="증권예탁결제원채권발행방법코드")
    laps_indf_yn: str = Field(title="경과이자지급여부")
    ksd_lhdy_pnia_dfrm_mthd_cd: str = Field(title="증권예탁결제원공휴일원리금지급방법코드")
    frst_int_dfrm_dt: str = Field(title="최초이자지급일자")
    ksd_prcm_lnkg_gvbd_yn: str = Field(title="증권예탁결제원물가연동국고채여부")
    dpsi_end_dt: str = Field(title="예탁종료일자")
    dpsi_strt_dt: str = Field(title="예탁시작일자")
    dpsi_psbl_yn: str = Field(title="예탁가능여부")
    atyp_rdpt_bond_erlm_yn: str = Field(title="비정형상환채권등록여부")
    dshn_occr_yn: str = Field(title="부도발생여부")
    expd_exts_yn: str = Field(title="만기연장여부")
    pclr_ptcr_text: str = Field(title="특이사항내용")
    dpsi_psbl_excp_stat_cd: str = Field(title="예탁가능예외상태코드")
    expd_exts_srdp_rcnt: str = Field(title="만기연장분할상환횟수")
    expd_exts_srdp_rt: str = Field(title="만기연장분할상환율")
    expd_rdpt_rt: str = Field(title="만기상환율")
    expd_asrc_erng_rt: str = Field(title="만기보장수익율")
    bond_int_dfrm_mthd_cd: str = Field(title="채권이자지급방법코드")
    int_dfrm_day_type_cd: str = Field(title="이자지급일유형코드")
    prca_dfmt_term_mcnt: str = Field(title="원금거치기간개월수")
    splt_rdpt_rcnt: str = Field(title="분할상환횟수")
    rgbf_int_dfrm_dt: str = Field(title="직전이자지급일자")
    nxtm_int_dfrm_dt: str = Field(title="차기이자지급일자")
    sprx_psbl_yn: str = Field(title="분리과세가능여부")
    ictx_rt_dvsn_cd: str = Field(title="소득세율구분코드")
    bond_clsf_cd: str = Field(title="채권분류코드")
    bond_clsf_kor_name: str = Field(title="채권분류한글명")
    int_mned_dvsn_cd: str = Field(title="이자월말구분코드")
    pnia_int_calc_unpr: str = Field(title="원리금이자계산단가")
    frn_intr: str = Field(title="FRN금리")
    aply_day_prcm_idx_lnkg_cefc: str = Field(title="적용일물가지수연동계수")
    ksd_expd_dydv_calc_bass_cd: str = Field(title="증권예탁결제원만기일할계산기준코드")
    expd_dydv_calc_dcnt: str = Field(title="만기일할계산일수")
    ksd_cbbw_dvsn_cd: str = Field(title="증권예탁결제원신종사채구분코드")
    crfd_item_yn: str = Field(title="크라우드펀딩종목여부")
    pnia_bank_ofdy_dfrm_mthd_cd: str = Field(title="원리금은행휴무일지급방법코드")
    qib_yn: str = Field(title="QIB여부")
    qib_cclc_dt: str = Field(title="QIB해지일자")
    csbd_yn: str = Field(title="영구채여부")
    csbd_cclc_dt: str = Field(title="영구채해지일자")
    ksd_opcb_yn: str = Field(title="증권예탁결제원옵션부사채여부")
    ksd_sodn_yn: str = Field(title="증권예탁결제원후순위채권여부")
    ksd_rqdi_scty_yn: str = Field(title="증권예탁결제원유동화증권여부")
    elec_scty_yn: str = Field(title="전자증권여부")
    rght_ecis_mbdy_dvsn_cd: str = Field(title="권리행사주체구분코드")
    int_rkng_mthd_dvsn_cd: str = Field(title="이자산정방법구분코드")
    ofrg_dvsn_cd: str = Field(title="모집구분코드")
    ksd_tot_issu_amt: str = Field(title="증권예탁결제원총발행금액")
    next_indf_chk_ecls_yn: str = Field(title="다음이자지급체크제외여부")
    ksd_bond_intr_dvsn_cd: str = Field(title="증권예탁결제원채권금리구분코드")
    ksd_inrt_aply_dvsn_cd: str = Field(title="증권예탁결제원이율적용구분코드")
    krx_issu_istt_cd: str = Field(title="KRX발행기관코드")
    ksd_indf_frqc_uder_calc_cd: str = Field(title="증권예탁결제원이자지급주기미만계산코드")
    ksd_indf_frqc_uder_calc_dcnt: str = Field(title="증권예탁결제원이자지급주기미만계산일수")
    tlg_rcvg_dtl_dtime: str = Field(title="전문수신상세일시")


class OnmarketBondInfo(BaseModel, KisHttpBody):
    """장내채권 기본조회"""

    output: Optional[OnmarketBondInfoItem] = Field(default=None, title="응답상세")
