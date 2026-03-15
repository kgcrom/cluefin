import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types';

const s = () => z.string().default('');

const kisEnvelope = {
  rt_cd: z.string().optional(),
  msg_cd: z.string().optional(),
  msg1: z.string().optional(),
};

// ── getBondAskingPrice: Onmarket Bond Asking Price ──

export const getBondAskingPriceItemSchema = z
  .object({
    aspr_acpt_hour: s(),
    bond_askp1: s(),
    bond_askp2: s(),
    bond_askp3: s(),
    bond_askp4: s(),
    bond_askp5: s(),
    bond_bidp1: s(),
    bond_bidp2: s(),
    bond_bidp3: s(),
    bond_bidp4: s(),
    bond_bidp5: s(),
    askp_rsqn1: s(),
    askp_rsqn2: s(),
    askp_rsqn3: s(),
    askp_rsqn4: s(),
    askp_rsqn5: s(),
    bidp_rsqn1: s(),
    bidp_rsqn2: s(),
    bidp_rsqn3: s(),
    bidp_rsqn4: s(),
    bidp_rsqn5: s(),
    total_askp_rsqn: s(),
    total_bidp_rsqn: s(),
    ntby_aspr_rsqn: s(),
    seln_ernn_rate1: s(),
    seln_ernn_rate2: s(),
    seln_ernn_rate3: s(),
    seln_ernn_rate4: s(),
    seln_ernn_rate5: s(),
    shnu_ernn_rate1: s(),
    shnu_ernn_rate2: s(),
    shnu_ernn_rate3: s(),
    shnu_ernn_rate4: s(),
    shnu_ernn_rate5: s(),
  })
  .passthrough();

export const getBondAskingPriceResponseSchema = z
  .object({
    ...kisEnvelope,
    output: getBondAskingPriceItemSchema.optional(),
  })
  .passthrough();

// ── getBondPrice: Onmarket Bond Price ──

export const getBondPriceItemSchema = z
  .object({
    stnd_iscd: s(),
    hts_kor_isnm: s(),
    bond_prpr: s(),
    prdy_vrss_sign: s(),
    bond_prdy_vrss: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    bond_prdy_clpr: s(),
    bond_oprc: s(),
    bond_hgpr: s(),
    bond_lwpr: s(),
    ernn_rate: s(),
    oprc_ert: s(),
    hgpr_ert: s(),
    lwpr_ert: s(),
    bond_mxpr: s(),
    bond_llam: s(),
  })
  .passthrough();

export const getBondPriceResponseSchema = z
  .object({
    ...kisEnvelope,
    output: getBondPriceItemSchema.optional(),
  })
  .passthrough();

// ── getBondExecution: Onmarket Bond Execution ──

export const getBondExecutionItemSchema = z
  .object({
    stck_cntg_hour: s(),
    bond_prpr: s(),
    bond_prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    cntg_vol: s(),
    acml_vol: s(),
  })
  .passthrough();

export const getBondExecutionResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getBondExecutionItemSchema).default([]),
  })
  .passthrough();

// ── getBondDailyPrice: Onmarket Bond Daily Price ──

export const getBondDailyPriceItemSchema = z
  .object({
    stck_bsop_date: s(),
    bond_prpr: s(),
    bond_prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    bond_oprc: s(),
    bond_hgpr: s(),
    bond_lwpr: s(),
  })
  .passthrough();

export const getBondDailyPriceResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getBondDailyPriceItemSchema).default([]),
  })
  .passthrough();

// ── getBondDailyChartPrice: Onmarket Bond Daily Chart Price ──

export const getBondDailyChartPriceItemSchema = z
  .object({
    stck_bsop_date: s(),
    bond_oprc: s(),
    bond_hgpr: s(),
    bond_lwpr: s(),
    bond_prpr: s(),
    acml_vol: s(),
  })
  .passthrough();

export const getBondDailyChartPriceResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getBondDailyChartPriceItemSchema).default([]),
  })
  .passthrough();

// ── getBondAvgUnitPrice: Onmarket Bond Avg Unit Price ──

export const getBondAvgUnitPriceOutput1ItemSchema = z
  .object({
    evlu_dt: s(),
    pdno: s(),
    prdt_type_cd: s(),
    prdt_name: s(),
    kis_unpr: s(),
    kbp_unpr: s(),
    nice_evlu_unpr: s(),
    fnp_unpr: s(),
    avg_evlu_unpr: s(),
    kis_crdt_grad_text: s(),
    kbp_crdt_grad_text: s(),
    nice_crdt_grad_text: s(),
    fnp_crdt_grad_text: s(),
    chng_yn: s(),
    kis_erng_rt: s(),
    kbp_erng_rt: s(),
    nice_evlu_erng_rt: s(),
    fnp_erng_rt: s(),
    avg_evlu_erng_rt: s(),
    kis_rf_unpr: s(),
    kbp_rf_unpr: s(),
    nice_evlu_rf_unpr: s(),
    avg_evlu_rf_unpr: s(),
  })
  .passthrough();

export const getBondAvgUnitPriceOutput2ItemSchema = z
  .object({
    evlu_dt: s(),
    pdno: s(),
    prdt_type_cd: s(),
    prdt_name: s(),
    kis_evlu_amt: s(),
    kbp_evlu_amt: s(),
    nice_evlu_amt: s(),
    fnp_evlu_amt: s(),
    avg_evlu_amt: s(),
    chng_yn: s(),
  })
  .passthrough();

export const getBondAvgUnitPriceOutput3ItemSchema = z
  .object({
    evlu_dt: s(),
    pdno: s(),
    prdt_type_cd: s(),
    prdt_name: s(),
    kis_crcy_cd: s(),
    kis_evlu_unit_pric: s(),
    kis_evlu_pric: s(),
    kbp_crcy_cd: s(),
    kbp_evlu_unit_pric: s(),
    kbp_evlu_pric: s(),
    nice_crcy_cd: s(),
    nice_evlu_unit_pric: s(),
    nice_evlu_pric: s(),
    avg_evlu_unit_pric: s(),
    avg_evlu_pric: s(),
    chng_yn: s(),
  })
  .passthrough();

export const getBondAvgUnitPriceResponseSchema = z
  .object({
    ...kisEnvelope,
    ctx_area_fk100: s(),
    ctx_area_nk30: s(),
    output1: z.array(getBondAvgUnitPriceOutput1ItemSchema).default([]),
    output2: z.array(getBondAvgUnitPriceOutput2ItemSchema).default([]),
    output3: z.array(getBondAvgUnitPriceOutput3ItemSchema).default([]),
  })
  .passthrough();

// ── getBondInfo: Onmarket Bond Info ──

export const getBondInfoItemSchema = z
  .object({
    pdno: s(),
    prdt_type_cd: s(),
    ksd_bond_item_name: s(),
    ksd_bond_item_eng_name: s(),
    ksd_bond_lstg_type_cd: s(),
    ksd_ofrg_dvsn_cd: s(),
    ksd_bond_int_dfrm_dvsn_cd: s(),
    issu_dt: s(),
    rdpt_dt: s(),
    rvnu_dt: s(),
    iso_crcy_cd: s(),
    mdwy_rdpt_dt: s(),
    ksd_rcvg_bond_dsct_rt: s(),
    ksd_rcvg_bond_srfc_inrt: s(),
    bond_expd_rdpt_rt: s(),
    ksd_prca_rdpt_mthd_cd: s(),
    int_caltm_mcnt: s(),
    ksd_int_calc_unit_cd: s(),
    uval_cut_dvsn_cd: s(),
    uval_cut_dcpt_dgit: s(),
    ksd_dydv_caltm_aply_dvsn_cd: s(),
    dydv_calc_dcnt: s(),
    bond_expd_asrc_erng_rt: s(),
    padf_plac_hdof_name: s(),
    lstg_dt: s(),
    lstg_abol_dt: s(),
    ksd_bond_issu_mthd_cd: s(),
    laps_indf_yn: s(),
    ksd_lhdy_pnia_dfrm_mthd_cd: s(),
    frst_int_dfrm_dt: s(),
    ksd_prcm_lnkg_gvbd_yn: s(),
    dpsi_end_dt: s(),
    dpsi_strt_dt: s(),
    dpsi_psbl_yn: s(),
    atyp_rdpt_bond_erlm_yn: s(),
    dshn_occr_yn: s(),
    expd_exts_yn: s(),
    pclr_ptcr_text: s(),
    dpsi_psbl_excp_stat_cd: s(),
    expd_exts_srdp_rcnt: s(),
    expd_exts_srdp_rt: s(),
    expd_rdpt_rt: s(),
    expd_asrc_erng_rt: s(),
    bond_int_dfrm_mthd_cd: s(),
    int_dfrm_day_type_cd: s(),
    prca_dfmt_term_mcnt: s(),
    splt_rdpt_rcnt: s(),
    rgbf_int_dfrm_dt: s(),
    nxtm_int_dfrm_dt: s(),
    sprx_psbl_yn: s(),
    ictx_rt_dvsn_cd: s(),
    bond_clsf_cd: s(),
    bond_clsf_kor_name: s(),
    int_mned_dvsn_cd: s(),
    pnia_int_calc_unpr: s(),
    frn_intr: s(),
    aply_day_prcm_idx_lnkg_cefc: s(),
    ksd_expd_dydv_calc_bass_cd: s(),
    expd_dydv_calc_dcnt: s(),
    ksd_cbbw_dvsn_cd: s(),
    crfd_item_yn: s(),
    pnia_bank_ofdy_dfrm_mthd_cd: s(),
    qib_yn: s(),
    qib_cclc_dt: s(),
    csbd_yn: s(),
    csbd_cclc_dt: s(),
    ksd_opcb_yn: s(),
    ksd_sodn_yn: s(),
    ksd_rqdi_scty_yn: s(),
    elec_scty_yn: s(),
    rght_ecis_mbdy_dvsn_cd: s(),
    int_rkng_mthd_dvsn_cd: s(),
    ofrg_dvsn_cd: s(),
    ksd_tot_issu_amt: s(),
    next_indf_chk_ecls_yn: s(),
    ksd_bond_intr_dvsn_cd: s(),
    ksd_inrt_aply_dvsn_cd: s(),
    krx_issu_istt_cd: s(),
    ksd_indf_frqc_uder_calc_cd: s(),
    ksd_indf_frqc_uder_calc_dcnt: s(),
    tlg_rcvg_dtl_dtime: s(),
  })
  .passthrough();

export const getBondInfoResponseSchema = z
  .object({
    ...kisEnvelope,
    output: getBondInfoItemSchema.optional(),
  })
  .passthrough();

// ── getBondIssueInfo: Onmarket Bond Issue Info ──

export const getBondIssueInfoItemSchema = z
  .object({
    pdno: s(),
    prdt_type_cd: s(),
    prdt_name: s(),
    prdt_eng_name: s(),
    ivst_heed_prdt_yn: s(),
    exts_yn: s(),
    bond_clsf_cd: s(),
    bond_clsf_kor_name: s(),
    papr: s(),
    int_mned_dvsn_cd: s(),
    rvnu_shap_cd: s(),
    issu_amt: s(),
    lstg_rmnd: s(),
    int_dfrm_mcnt: s(),
    bond_int_dfrm_mthd_cd: s(),
    splt_rdpt_rcnt: s(),
    prca_dfmt_term_mcnt: s(),
    int_anap_dvsn_cd: s(),
    bond_rght_dvsn_cd: s(),
    prdt_pclc_text: s(),
    prdt_abrv_name: s(),
    prdt_eng_abrv_name: s(),
    sprx_psbl_yn: s(),
    pbff_pplc_ofrg_mthd_cd: s(),
    cmco_cd: s(),
    issu_istt_cd: s(),
    issu_istt_name: s(),
    pnia_dfrm_agcy_istt_cd: s(),
    dsct_ec_rt: s(),
    srfc_inrt: s(),
    expd_rdpt_rt: s(),
    expd_asrc_erng_rt: s(),
    bond_grte_istt_name: s(),
    int_dfrm_day_type_cd: s(),
    ksd_int_calc_unit_cd: s(),
    int_wunt_uder_prcs_dvsn_cd: s(),
    rvnu_dt: s(),
    issu_dt: s(),
    lstg_dt: s(),
    expd_dt: s(),
    rdpt_dt: s(),
    sbst_pric: s(),
    rgbf_int_dfrm_dt: s(),
    nxtm_int_dfrm_dt: s(),
    frst_int_dfrm_dt: s(),
    ecis_pric: s(),
    rght_stck_std_pdno: s(),
    ecis_opng_dt: s(),
    ecis_end_dt: s(),
    bond_rvnu_mthd_cd: s(),
    oprt_stfno: s(),
    oprt_stff_name: s(),
    rgbf_int_dfrm_wday: s(),
    nxtm_int_dfrm_wday: s(),
    kis_crdt_grad_text: s(),
    kbp_crdt_grad_text: s(),
    nice_crdt_grad_text: s(),
    fnp_crdt_grad_text: s(),
    dpsi_psbl_yn: s(),
    pnia_int_calc_unpr: s(),
    prcm_idx_bond_yn: s(),
    expd_exts_srdp_rcnt: s(),
    expd_exts_srdp_rt: s(),
    loan_psbl_yn: s(),
    grte_dvsn_cd: s(),
    fnrr_rank_dvsn_cd: s(),
    krx_lstg_abol_dvsn_cd: s(),
    asst_rqdi_dvsn_cd: s(),
    opcb_dvsn_cd: s(),
    crfd_item_yn: s(),
    crfd_item_rstc_cclc_dt: s(),
    bond_nmpr_unit_pric: s(),
    ivst_heed_bond_dvsn_name: s(),
    add_erng_rt: s(),
    add_erng_rt_aply_dt: s(),
    bond_tr_stop_dvsn_cd: s(),
    ivst_heed_bond_dvsn_cd: s(),
    pclr_cndt_text: s(),
    hbbd_yn: s(),
    cdtl_cptl_scty_type_cd: s(),
    elec_scty_yn: s(),
    sq1_clop_ecis_opng_dt: s(),
    frst_erlm_stfno: s(),
    frst_erlm_dt: s(),
    frst_erlm_tmd: s(),
    tlg_rcvg_dtl_dtime: s(),
  })
  .passthrough();

export const getBondIssueInfoResponseSchema = z
  .object({
    ...kisEnvelope,
    output: getBondIssueInfoItemSchema.optional(),
  })
  .passthrough();

// ── Response Types ──

export type GetBondAskingPriceResponse = CamelizeKeys<z.infer<typeof getBondAskingPriceResponseSchema>>;

export type GetBondPriceResponse = CamelizeKeys<z.infer<typeof getBondPriceResponseSchema>>;

export type GetBondExecutionResponse = CamelizeKeys<z.infer<typeof getBondExecutionResponseSchema>>;

export type GetBondDailyPriceResponse = CamelizeKeys<z.infer<typeof getBondDailyPriceResponseSchema>>;

export type GetBondDailyChartPriceResponse = CamelizeKeys<z.infer<typeof getBondDailyChartPriceResponseSchema>>;

export type GetBondAvgUnitPriceResponse = CamelizeKeys<z.infer<typeof getBondAvgUnitPriceResponseSchema>>;

export type GetBondInfoResponse = CamelizeKeys<z.infer<typeof getBondInfoResponseSchema>>;

export type GetBondIssueInfoResponse = CamelizeKeys<z.infer<typeof getBondIssueInfoResponseSchema>>;

// ── Response Map ──

export interface OnmarketBondBasicQuoteResponseMap {
  getBondAskingPrice: GetBondAskingPriceResponse;
  getBondPrice: GetBondPriceResponse;
  getBondExecution: GetBondExecutionResponse;
  getBondDailyPrice: GetBondDailyPriceResponse;
  getBondDailyChartPrice: GetBondDailyChartPriceResponse;
  getBondAvgUnitPrice: GetBondAvgUnitPriceResponse;
  getBondInfo: GetBondInfoResponse;
  getBondIssueInfo: GetBondIssueInfoResponse;
}
