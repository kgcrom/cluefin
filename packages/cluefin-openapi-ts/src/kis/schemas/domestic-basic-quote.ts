import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types';

const s = () => z.string().default('');

const kisEnvelope = {
  rt_cd: z.string().optional(),
  msg_cd: z.string().optional(),
  msg1: z.string().optional(),
};

// ── getStockCurrentPrice: Domestic Stock Current Price ──

export const getStockCurrentPriceItemSchema = z
  .object({
    iscd_stat_cls_code: s(),
    marg_rate: s(),
    rprs_mrkt_kor_name: s(),
    new_hgpr_lwpr_cls_code: z.string().optional(),
    bstp_kor_isnm: s(),
    temp_stop_yn: s(),
    oprc_rang_cont_yn: s(),
    clpr_rang_cont_yn: s(),
    crdt_able_yn: s(),
    grmn_rate_cls_code: s(),
    elw_pblc_yn: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_tr_pbmn: s(),
    acml_vol: s(),
    prdy_vrss_vol_rate: s(),
    stck_oprc: s(),
    stck_hgpr: s(),
    stck_lwpr: s(),
    stck_mxpr: s(),
    stck_llam: s(),
    stck_sdpr: s(),
    wghn_avrg_stck_prc: s(),
    hts_frgn_ehrt: s(),
    frgn_ntby_qty: s(),
    pgtr_ntby_qty: s(),
    pvt_scnd_dmrs_prc: s(),
    pvt_frst_dmrs_prc: s(),
    pvt_pont_val: s(),
    pvt_frst_dmsp_prc: s(),
    pvt_scnd_dmsp_prc: s(),
    dmrs_val: s(),
    dmsp_val: s(),
    cpfn: s(),
    rstc_wdth_prc: s(),
    stck_fcam: s(),
    stck_sspr: s(),
    aspr_unit: s(),
    hts_deal_qty_unit_val: s(),
    lstn_stcn: s(),
    hts_avls: s(),
    per: s(),
    pbr: s(),
    stac_month: s(),
    vol_tnrt: s(),
    eps: s(),
    bps: s(),
    d250_hgpr: s(),
    d250_hgpr_date: s(),
    d250_hgpr_vrss_prpr_rate: s(),
    d250_lwpr: s(),
    d250_lwpr_date: s(),
    d250_lwpr_vrss_prpr_rate: s(),
    stck_dryy_hgpr: s(),
    dryy_hgpr_vrss_prpr_rate: s(),
    dryy_hgpr_date: s(),
    stck_dryy_lwpr: s(),
    dryy_lwpr_vrss_prpr_rate: s(),
    dryy_lwpr_date: s(),
    w52_hgpr: s(),
    w52_hgpr_vrss_prpr_ctrt: s(),
    w52_hgpr_date: s(),
    w52_lwpr: s(),
    w52_lwpr_vrss_prpr_ctrt: s(),
    w52_lwpr_date: s(),
    whol_loan_rmnd_rate: s(),
    ssts_yn: s(),
    stck_shrn_iscd: s(),
    fcam_cnnm: s(),
    cpfn_cnnm: s(),
    frgn_hldn_qty: s(),
    vi_cls_code: s(),
    ovtm_vi_cls_code: s(),
    last_ssts_cntg_qty: s(),
    invt_caful_yn: s(),
    mrkt_warn_cls_code: s(),
    short_over_yn: s(),
    sltr_yn: s(),
    mang_issu_cls_code: s(),
  })
  .passthrough();

export const getStockCurrentPriceResponseSchema = z
  .object({
    ...kisEnvelope,
    output: getStockCurrentPriceItemSchema.optional(),
  })
  .passthrough();

// ── getStockCurrentPrice2: Domestic Stock Current Price2 ──

export const getStockCurrentPrice2ItemSchema = z
  .object({
    rprs_mrkt_kor_name: s(),
    new_hgpr_lwpr_cls_code: z.string().optional(),
    mxpr_llam_cls_code: z.string().optional(),
    crdt_able_yn: s(),
    stck_mxpr: s(),
    elw_pblc_yn: s(),
    prdy_clpr_vrss_oprc_rate: s(),
    crdt_rate: s(),
    marg_rate: s(),
    lwpr_vrss_prpr: s(),
    lwpr_vrss_prpr_sign: s(),
    prdy_clpr_vrss_lwpr_rate: s(),
    stck_lwpr: s(),
    hgpr_vrss_prpr: s(),
    hgpr_vrss_prpr_sign: s(),
    prdy_clpr_vrss_hgpr_rate: s(),
    stck_hgpr: s(),
    oprc_vrss_prpr: s(),
    oprc_vrss_prpr_sign: s(),
    mang_issu_yn: s(),
    divi_app_cls_code: s(),
    short_over_yn: s(),
    mrkt_warn_cls_code: s(),
    invt_caful_yn: s(),
    stange_runup_yn: s(),
    ssts_hot_yn: s(),
    low_current_yn: s(),
    vi_cls_code: s(),
    short_over_cls_code: s(),
    stck_llam: s(),
    new_lstn_cls_name: s(),
    vlnt_deal_cls_name: s(),
    flng_cls_name: z.string().optional(),
    revl_issu_reas_name: z.string().optional(),
    mrkt_warn_cls_name: z.string().optional(),
    stck_sdpr: s(),
    bstp_cls_code: s(),
    stck_prdy_clpr: s(),
    insn_pbnt_yn: s(),
    fcam_mod_cls_name: z.string().optional(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_tr_pbmn: s(),
    acml_vol: s(),
    prdy_vrss_vol_rate: s(),
    bstp_kor_isnm: s(),
    sltr_yn: s(),
    trht_yn: s(),
    oprc_rang_cont_yn: s(),
    vlnt_fin_cls_code: s(),
    stck_oprc: s(),
    prdy_vol: s(),
  })
  .passthrough();

export const getStockCurrentPrice2ResponseSchema = z
  .object({
    ...kisEnvelope,
    output: getStockCurrentPrice2ItemSchema.optional(),
  })
  .passthrough();

// ── getStockCurrentPriceConclusion: Domestic Stock Current Price Conclusion ──

export const getStockCurrentPriceConclusionItemSchema = z
  .object({
    stck_cntg_hour: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    cntg_vol: s(),
    tday_rltv: s(),
    prdy_ctrt: s(),
  })
  .passthrough();

export const getStockCurrentPriceConclusionResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getStockCurrentPriceConclusionItemSchema).default([]),
  })
  .passthrough();

// ── getStockCurrentPriceDaily: Domestic Stock Current Price Daily ──

export const getStockCurrentPriceDailyItemSchema = z
  .object({
    stck_bsop_date: s(),
    stck_oprc: s(),
    stck_hgpr: s(),
    stck_lwpr: s(),
    stck_clpr: s(),
    acml_vol: s(),
    prdy_vrss_vol_rate: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    hts_frgn_ehrt: s(),
    frgn_ntby_qty: s(),
    flng_cls_code: s(),
    acml_prtt_rate: s(),
  })
  .passthrough();

export const getStockCurrentPriceDailyResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getStockCurrentPriceDailyItemSchema).default([]),
  })
  .passthrough();

// ── getStockCurrentPriceAskingExpectedConclusion: Domestic Stock Current Price Asking Expected Conclusion ──

export const getStockCurrentPriceAskingExpectedConclusionOutput1ItemSchema = z
  .object({
    aspr_acpt_hour: s(),
    askp1: s(),
    askp2: s(),
    askp3: s(),
    askp4: s(),
    askp5: s(),
    askp6: s(),
    askp7: s(),
    askp8: s(),
    askp9: s(),
    askp10: s(),
    bidp1: s(),
    bidp2: s(),
    bidp3: s(),
    bidp4: s(),
    bidp5: s(),
    bidp6: s(),
    bidp7: s(),
    bidp8: s(),
    bidp9: s(),
    bidp10: s(),
    askp_rsqn1: s(),
    askp_rsqn2: s(),
    askp_rsqn3: s(),
    askp_rsqn4: s(),
    askp_rsqn5: s(),
    askp_rsqn6: s(),
    askp_rsqn7: s(),
    askp_rsqn8: s(),
    askp_rsqn9: s(),
    askp_rsqn10: s(),
    bidp_rsqn1: s(),
    bidp_rsqn2: s(),
    bidp_rsqn3: s(),
    bidp_rsqn4: s(),
    bidp_rsqn5: s(),
    bidp_rsqn6: s(),
    bidp_rsqn7: s(),
    bidp_rsqn8: s(),
    bidp_rsqn9: s(),
    bidp_rsqn10: s(),
    askp_rsqn_icdc1: s(),
    askp_rsqn_icdc2: s(),
    askp_rsqn_icdc3: s(),
    askp_rsqn_icdc4: s(),
    askp_rsqn_icdc5: s(),
    askp_rsqn_icdc6: s(),
    askp_rsqn_icdc7: s(),
    askp_rsqn_icdc8: s(),
    askp_rsqn_icdc9: s(),
    askp_rsqn_icdc10: s(),
    bidp_rsqn_icdc1: s(),
    bidp_rsqn_icdc2: s(),
    bidp_rsqn_icdc3: s(),
    bidp_rsqn_icdc4: s(),
    bidp_rsqn_icdc5: s(),
    bidp_rsqn_icdc6: s(),
    bidp_rsqn_icdc7: s(),
    bidp_rsqn_icdc8: s(),
    bidp_rsqn_icdc9: s(),
    bidp_rsqn_icdc10: s(),
    total_askp_rsqn: s(),
    total_bidp_rsqn: s(),
    total_askp_rsqn_icdc: s(),
    total_bidp_rsqn_icdc: s(),
    ovtm_total_askp_icdc: s(),
    ovtm_total_bidp_icdc: s(),
    ovtm_total_askp_rsqn: s(),
    ovtm_total_bidp_rsqn: s(),
    ntby_aspr_rsqn: s(),
    new_mkop_cls_code: s(),
  })
  .passthrough();

export const getStockCurrentPriceAskingExpectedConclusionOutput2ItemSchema = z
  .object({
    antc_mkop_cls_code: s(),
    stck_prpr: s(),
    stck_oprc: s(),
    stck_hgpr: s(),
    stck_lwpr: s(),
    stck_sdpr: s(),
    antc_cnpr: s(),
    antc_cntg_vrss_sign: s(),
    antc_cntg_vrss: s(),
    antc_cntg_prdy_ctrt: s(),
    antc_vol: s(),
    stck_shrn_iscd: s(),
    vi_cls_code: s(),
  })
  .passthrough();

export const getStockCurrentPriceAskingExpectedConclusionResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getStockCurrentPriceAskingExpectedConclusionOutput1ItemSchema.optional(),
    output2: getStockCurrentPriceAskingExpectedConclusionOutput2ItemSchema.optional(),
  })
  .passthrough();

// ── getStockCurrentPriceInvestor: Domestic Stock Current Price Investor ──

export const getStockCurrentPriceInvestorItemSchema = z
  .object({
    stck_bsop_date: s(),
    stck_clpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prsn_ntby_qty: s(),
    frgn_ntby_qty: s(),
    orgn_ntby_qty: s(),
    prsn_ntby_tr_pbmn: s(),
    frgn_ntby_tr_pbmn: s(),
    orgn_ntby_tr_pbmn: s(),
    prsn_shnu_vol: s(),
    frgn_shnu_vol: s(),
    orgn_shnu_vol: s(),
    prsn_shnu_tr_pbmn: s(),
    frgn_shnu_tr_pbmn: s(),
    orgn_shnu_tr_pbmn: s(),
    prsn_seln_vol: s(),
    frgn_seln_vol: s(),
    orgn_seln_vol: s(),
    prsn_seln_tr_pbmn: s(),
    frgn_seln_tr_pbmn: s(),
    orgn_seln_tr_pbmn: s(),
  })
  .passthrough();

export const getStockCurrentPriceInvestorResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getStockCurrentPriceInvestorItemSchema).default([]),
  })
  .passthrough();

// ── getStockCurrentPriceMember: Domestic Stock Current Price Member ──

export const getStockCurrentPriceMemberItemSchema = z
  .object({
    seln_mbcr_no1: s(),
    seln_mbcr_no2: s(),
    seln_mbcr_no3: s(),
    seln_mbcr_no4: s(),
    seln_mbcr_no5: s(),
    seln_mbcr_name1: s(),
    seln_mbcr_name2: s(),
    seln_mbcr_name3: s(),
    seln_mbcr_name4: s(),
    seln_mbcr_name5: s(),
    total_seln_qty1: s(),
    total_seln_qty2: s(),
    total_seln_qty3: s(),
    total_seln_qty4: s(),
    total_seln_qty5: s(),
    seln_mbcr_rlim1: s(),
    seln_mbcr_rlim2: s(),
    seln_mbcr_rlim3: s(),
    seln_mbcr_rlim4: s(),
    seln_mbcr_rlim5: s(),
    seln_qty_icdc1: s(),
    seln_qty_icdc2: s(),
    seln_qty_icdc3: s(),
    seln_qty_icdc4: s(),
    seln_qty_icdc5: s(),
    shnu_mbcr_no1: s(),
    shnu_mbcr_no2: s(),
    shnu_mbcr_no3: s(),
    shnu_mbcr_no4: s(),
    shnu_mbcr_no5: s(),
    shnu_mbcr_name1: s(),
    shnu_mbcr_name2: s(),
    shnu_mbcr_name3: s(),
    shnu_mbcr_name4: s(),
    shnu_mbcr_name5: s(),
    total_shnu_qty1: s(),
    total_shnu_qty2: s(),
    total_shnu_qty3: s(),
    total_shnu_qty4: s(),
    total_shnu_qty5: s(),
    shnu_mbcr_rlim1: s(),
    shnu_mbcr_rlim2: s(),
    shnu_mbcr_rlim3: s(),
    shnu_mbcr_rlim4: s(),
    shnu_mbcr_rlim5: s(),
    shnu_qty_icdc1: s(),
    shnu_qty_icdc2: s(),
    shnu_qty_icdc3: s(),
    shnu_qty_icdc4: s(),
    shnu_qty_icdc5: s(),
    acml_vol: s(),
    glob_total_seln_qty: s(),
    glob_seln_rlim: s(),
    glob_ntby_qty: s(),
    glob_total_shnu_qty: s(),
    glob_shnu_rlim: s(),
    seln_mbcr_glob_yn_1: s(),
    seln_mbcr_glob_yn_2: s(),
    seln_mbcr_glob_yn_3: s(),
    seln_mbcr_glob_yn_4: s(),
    seln_mbcr_glob_yn_5: s(),
    shnu_mbcr_glob_yn_1: s(),
    shnu_mbcr_glob_yn_2: s(),
    shnu_mbcr_glob_yn_3: s(),
    shnu_mbcr_glob_yn_4: s(),
    shnu_mbcr_glob_yn_5: s(),
    glob_total_seln_qty_icdc: s(),
    glob_total_shnu_qty_icdc: s(),
  })
  .passthrough();

export const getStockCurrentPriceMemberResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getStockCurrentPriceMemberItemSchema).default([]),
  })
  .passthrough();

// ── getStockPeriodQuote: Domestic Stock Period Quote ──

export const getStockPeriodQuoteOutput1ItemSchema = z
  .object({
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    stck_prdy_clpr: s(),
    acml_vol: s(),
    acml_tr_pbmn: s(),
    hts_kor_isnm: s(),
    stck_prpr: s(),
    stck_shrn_iscd: s(),
    prdy_vol: s(),
    stck_mxpr: s(),
    stck_llam: s(),
    stck_oprc: s(),
    stck_hgpr: s(),
    stck_lwpr: s(),
    stck_prdy_oprc: s(),
    stck_prdy_hgpr: s(),
    stck_prdy_lwpr: s(),
    askp: s(),
    bidp: s(),
    prdy_vrss_vol: s(),
    vol_tnrt: s(),
    stck_fcam: s(),
    lstn_stcn: s(),
    cpfn: s(),
    hts_avls: s(),
    per: s(),
    eps: s(),
    pbr: s(),
    itewhol_loan_rmnd_rate: s(),
  })
  .passthrough();

export const getStockPeriodQuoteOutput2ItemSchema = z
  .object({
    stck_bsop_date: s(),
    stck_clpr: s(),
    stck_oprc: s(),
    stck_hgpr: s(),
    stck_lwpr: s(),
    acml_vol: s(),
    acml_tr_pbmn: s(),
    flng_cls_code: s(),
    prtt_rate: s(),
    mod_yn: s(),
    prdy_vrss_sign: s(),
    prdy_vrss: s(),
    revl_issu_reas: s(),
  })
  .passthrough();

export const getStockPeriodQuoteResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getStockPeriodQuoteOutput1ItemSchema.optional(),
    output2: z.array(getStockPeriodQuoteOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getStockTodayMinuteChart: Domestic Stock Today Minute Chart ──

export const getStockTodayMinuteChartOutput1ItemSchema = z
  .object({
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    stck_prdy_clpr: s(),
    acml_vol: s(),
    acml_tr_pbmn: s(),
    hts_kor_isnm: s(),
    stck_prpr: s(),
  })
  .passthrough();

export const getStockTodayMinuteChartOutput2ItemSchema = z
  .object({
    stck_bsop_date: s(),
    stck_cntg_hour: s(),
    stck_prpr: s(),
    stck_oprc: s(),
    stck_hgpr: s(),
    stck_lwpr: s(),
    cntg_vol: s(),
    acml_tr_pbmn: s(),
  })
  .passthrough();

export const getStockTodayMinuteChartResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getStockTodayMinuteChartOutput1ItemSchema.optional(),
    output2: z.array(getStockTodayMinuteChartOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getStockDailyMinuteChart: Domestic Stock Today Minute Chart ──

export const getStockDailyMinuteChartOutput1ItemSchema = z
  .object({
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    stck_prdy_clpr: s(),
    acml_vol: s(),
    acml_tr_pbmn: s(),
    hts_kor_isnm: s(),
    stck_prpr: s(),
  })
  .passthrough();

export const getStockDailyMinuteChartOutput2ItemSchema = z
  .object({
    stck_bsop_date: s(),
    stck_cntg_hour: s(),
    stck_prpr: s(),
    stck_oprc: s(),
    stck_hgpr: s(),
    stck_lwpr: s(),
    cntg_vol: s(),
    acml_tr_pbmn: s(),
  })
  .passthrough();

export const getStockDailyMinuteChartResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getStockDailyMinuteChartOutput1ItemSchema.optional(),
    output2: z.array(getStockDailyMinuteChartOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getStockCurrentPriceTimeItemConclusion: Domestic Stock Current Price Time Item Conclusion ──

export const getStockCurrentPriceTimeItemConclusionOutput1ItemSchema = z
  .object({
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    prdy_vol: s(),
    rprs_mrkt_kor_name: s(),
  })
  .passthrough();

export const getStockCurrentPriceTimeItemConclusionOutput2ItemSchema = z
  .object({
    stck_cntg_hour: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    askp: s(),
    bidp: s(),
    tday_rltv: s(),
    acml_vol: s(),
    cnqn: s(),
  })
  .passthrough();

export const getStockCurrentPriceTimeItemConclusionResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getStockCurrentPriceTimeItemConclusionOutput1ItemSchema.optional(),
    output2: z.array(getStockCurrentPriceTimeItemConclusionOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getStockCurrentPriceDailyOvertimePrice: Domestic Stock Current Price Daily Overtime Price ──

export const getStockCurrentPriceDailyOvertimePriceOutput1ItemSchema = z
  .object({
    ovtm_untp_prpr: s(),
    ovtm_untp_prdy_vrss: s(),
    ovtm_untp_prdy_vrss_sign: s(),
    ovtm_untp_prdy_ctrt: s(),
    ovtm_untp_vol: s(),
    ovtm_untp_tr_pbmn: s(),
    ovtm_untp_mxpr: s(),
    ovtm_untp_llam: s(),
    ovtm_untp_oprc: s(),
    ovtm_untp_hgpr: s(),
    ovtm_untp_lwpr: s(),
    ovtm_untp_antc_cnpr: s(),
    ovtm_untp_antc_cntg_vrss: s(),
    ovtm_untp_antc_cntg_vrss_sign: s(),
    ovtm_untp_antc_cntg_ctrt: s(),
    ovtm_untp_antc_vol: s(),
  })
  .passthrough();

export const getStockCurrentPriceDailyOvertimePriceOutput2ItemSchema = z
  .object({
    stck_bsop_date: s(),
    ovtm_untp_prpr: s(),
    ovtm_untp_prdy_vrss: s(),
    ovtm_untp_prdy_vrss_sign: s(),
    ovtm_untp_prdy_ctrt: s(),
    ovtm_untp_vol: s(),
    stck_clpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    ovtm_untp_tr_pbmn: s(),
  })
  .passthrough();

export const getStockCurrentPriceDailyOvertimePriceResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getStockCurrentPriceDailyOvertimePriceOutput1ItemSchema.optional(),
    output2: z.array(getStockCurrentPriceDailyOvertimePriceOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getStockCurrentPriceOvertimeConclusion: Domestic Stock Current Price Overtime Conclusion ──

export const getStockCurrentPriceOvertimeConclusionOutput1ItemSchema = z
  .object({
    ovtm_untp_prpr: s(),
    ovtm_untp_prdy_vrss: s(),
    ovtm_untp_prdy_vrss_sign: s(),
    ovtm_untp_prdy_ctrt: s(),
    ovtm_untp_vol: s(),
    ovtm_untp_tr_pbmn: s(),
    ovtm_untp_mxpr: s(),
    ovtm_untp_llam: s(),
    ovtm_untp_oprc: s(),
    ovtm_untp_hgpr: s(),
    ovtm_untp_lwpr: s(),
    ovtm_untp_antc_cnpr: s(),
    ovtm_untp_antc_cntg_vrss: s(),
    ovtm_untp_antc_cntg_vrss_sign: s(),
    ovtm_untp_antc_cntg_ctrt: s(),
    ovtm_untp_antc_vol: s(),
    uplm_sign: s(),
    lslm_sign: s(),
  })
  .passthrough();

export const getStockCurrentPriceOvertimeConclusionOutput2ItemSchema = z
  .object({
    stck_cntg_hour: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    askp: s(),
    bidp: s(),
    acml_vol: s(),
    cntg_vol: s(),
  })
  .passthrough();

export const getStockCurrentPriceOvertimeConclusionResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getStockCurrentPriceOvertimeConclusionOutput1ItemSchema.optional(),
    output2: z.array(getStockCurrentPriceOvertimeConclusionOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getStockOvertimeCurrentPrice: Domestic Stock Overtime Current Price ──

export const getStockOvertimeCurrentPriceItemSchema = z
  .object({
    bstp_kor_isnm: s(),
    mang_issu_cls_name: z.string().optional(),
    ovtm_untp_prpr: s(),
    ovtm_untp_prdy_vrss: s(),
    ovtm_untp_prdy_vrss_sign: s(),
    ovtm_untp_prdy_ctrt: s(),
    ovtm_untp_vol: s(),
    ovtm_untp_tr_pbmn: s(),
    ovtm_untp_mxpr: s(),
    ovtm_untp_llam: s(),
    ovtm_untp_oprc: s(),
    ovtm_untp_hgpr: s(),
    ovtm_untp_lwpr: s(),
    marg_rate: s(),
    ovtm_untp_antc_cnpr: s(),
    ovtm_untp_antc_cntg_vrss: s(),
    ovtm_untp_antc_cntg_vrss_sign: s(),
    ovtm_untp_antc_cntg_ctrt: s(),
    ovtm_untp_antc_cnqn: s(),
    crdt_able_yn: s(),
    new_lstn_cls_name: s(),
    sltr_yn: s(),
    mang_issu_yn: s(),
    mrkt_warn_cls_code: z.string().optional(),
    trht_yn: s(),
    vlnt_deal_cls_name: s(),
    ovtm_untp_sdpr: s(),
    mrkt_warn_cls_name: z.string().optional(),
    revl_issu_reas_name: z.string().optional(),
    insn_pbnt_yn: s(),
    flng_cls_name: z.string().optional(),
    rprs_mrkt_kor_name: s(),
    ovtm_vi_cls_code: s(),
    bidp: s(),
    askp: s(),
  })
  .passthrough();

export const getStockOvertimeCurrentPriceResponseSchema = z
  .object({
    ...kisEnvelope,
    output: getStockOvertimeCurrentPriceItemSchema.optional(),
  })
  .passthrough();

// ── getStockOvertimeAskingPrice: Domestic Stock Overtime Asking Price ──

export const getStockOvertimeAskingPriceItemSchema = z
  .object({
    ovtm_untp_last_hour: s(),
    ovtm_untp_askp1: s(),
    ovtm_untp_askp2: s(),
    ovtm_untp_askp3: s(),
    ovtm_untp_askp4: s(),
    ovtm_untp_askp5: s(),
    ovtm_untp_askp6: s(),
    ovtm_untp_askp7: s(),
    ovtm_untp_askp8: s(),
    ovtm_untp_askp9: s(),
    ovtm_untp_askp10: s(),
    ovtm_untp_bidp1: s(),
    ovtm_untp_bidp2: s(),
    ovtm_untp_bidp3: s(),
    ovtm_untp_bidp4: s(),
    ovtm_untp_bidp5: s(),
    ovtm_untp_bidp6: s(),
    ovtm_untp_bidp7: s(),
    ovtm_untp_bidp8: s(),
    ovtm_untp_bidp9: s(),
    ovtm_untp_bidp10: s(),
    ovtm_untp_askp_icdc1: s(),
    ovtm_untp_askp_icdc2: s(),
    ovtm_untp_askp_icdc3: s(),
    ovtm_untp_askp_icdc4: z.string().optional(),
    ovtm_untp_askp_icdc5: z.string().optional(),
    ovtm_untp_askp_icdc6: z.string().optional(),
    ovtm_untp_askp_icdc7: z.string().optional(),
    ovtm_untp_askp_icdc8: z.string().optional(),
    ovtm_untp_askp_icdc9: z.string().optional(),
    ovtm_untp_askp_icdc10: z.string().optional(),
    ovtm_untp_bidp_icdc1: s(),
    ovtm_untp_bidp_icdc2: s(),
    ovtm_untp_bidp_icdc3: s(),
    ovtm_untp_bidp_icdc4: z.string().optional(),
    ovtm_untp_bidp_icdc5: z.string().optional(),
    ovtm_untp_bidp_icdc6: z.string().optional(),
    ovtm_untp_bidp_icdc7: z.string().optional(),
    ovtm_untp_bidp_icdc8: z.string().optional(),
    ovtm_untp_bidp_icdc9: z.string().optional(),
    ovtm_untp_bidp_icdc10: z.string().optional(),
    ovtm_untp_askp_rsqn1: s(),
    ovtm_untp_askp_rsqn2: s(),
    ovtm_untp_askp_rsqn3: s(),
    ovtm_untp_askp_rsqn4: s(),
    ovtm_untp_askp_rsqn5: s(),
    ovtm_untp_askp_rsqn6: s(),
    ovtm_untp_askp_rsqn7: s(),
    ovtm_untp_askp_rsqn8: s(),
    ovtm_untp_askp_rsqn9: s(),
    ovtm_untp_askp_rsqn10: s(),
    ovtm_untp_bidp_rsqn1: s(),
    ovtm_untp_bidp_rsqn2: s(),
    ovtm_untp_bidp_rsqn3: s(),
    ovtm_untp_bidp_rsqn4: s(),
    ovtm_untp_bidp_rsqn5: s(),
    ovtm_untp_bidp_rsqn6: s(),
    ovtm_untp_bidp_rsqn7: s(),
    ovtm_untp_bidp_rsqn8: s(),
    ovtm_untp_bidp_rsqn9: s(),
    ovtm_untp_bidp_rsqn10: s(),
    ovtm_untp_total_askp_rsqn: s(),
    ovtm_untp_total_bidp_rsqn: s(),
    ovtm_untp_total_askp_rsqn_icdc: s(),
    ovtm_untp_total_bidp_rsqn_icdc: s(),
    ovtm_untp_ntby_bidp_rsqn: s(),
    total_askp_rsqn: s(),
    total_bidp_rsqn: s(),
    total_askp_rsqn_icdc: s(),
    total_bidp_rsqn_icdc: s(),
    ovtm_total_askp_rsqn: s(),
    ovtm_total_bidp_rsqn: s(),
    ovtm_total_askp_icdc: s(),
    ovtm_total_bidp_icdc: s(),
  })
  .passthrough();

export const getStockOvertimeAskingPriceResponseSchema = z
  .object({
    ...kisEnvelope,
    output: getStockOvertimeAskingPriceItemSchema.optional(),
  })
  .passthrough();

// ── getStockClosingExpectedPrice: Domestic Stock Closing Expected Price ──

export const getStockClosingExpectedPriceItemSchema = z
  .object({
    stck_shrn_iscd: s(),
    hts_kor_isnm: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    sdpr_vrss_prpr: s(),
    sdpr_vrss_prpr_rate: s(),
    cntg_vol: s(),
  })
  .passthrough();

export const getStockClosingExpectedPriceResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getStockClosingExpectedPriceItemSchema).default([]),
  })
  .passthrough();

// ── getEtfetnCurrentPrice: Domestic Etf Etn Current Price ──

export const getEtfetnCurrentPriceItemSchema = z
  .object({
    stck_prpr: s(),
    prdy_vrss_sign: s(),
    prdy_vrss: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    prdy_vol: s(),
    stck_mxpr: s(),
    stck_llam: s(),
    stck_prdy_clpr: s(),
    stck_oprc: s(),
    prdy_clpr_vrss_oprc_rate: s(),
    stck_hgpr: s(),
    prdy_clpr_vrss_hgpr_rate: s(),
    stck_lwpr: s(),
    prdy_clpr_vrss_lwpr_rate: s(),
    prdy_last_nav: s(),
    nav: s(),
    nav_prdy_vrss: s(),
    nav_prdy_vrss_sign: s(),
    nav_prdy_ctrt: s(),
    trc_errt: s(),
    stck_sdpr: s(),
    stck_sspr: s(),
    etf_crcl_stcn: s(),
    etf_ntas_ttam: s(),
    etf_frcr_ntas_ttam: s(),
    frgn_limt_rate: s(),
    frgn_oder_able_qty: s(),
    etf_cu_unit_scrt_cnt: s(),
    etf_cnfg_issu_cnt: s(),
    etf_dvdn_cycl: s(),
    crcd: s(),
    etf_crcl_ntas_ttam: s(),
    etf_frcr_crcl_ntas_ttam: s(),
    etf_frcr_last_ntas_wrth_val: s(),
    lp_oder_able_cls_code: s(),
    stck_dryy_hgpr: s(),
    dryy_hgpr_vrss_prpr_rate: s(),
    dryy_hgpr_date: s(),
    stck_dryy_lwpr: s(),
    dryy_lwpr_vrss_prpr_rate: s(),
    dryy_lwpr_date: s(),
    bstp_kor_isnm: s(),
    vi_cls_code: s(),
    lstn_stcn: s(),
    frgn_hldn_qty: s(),
    frgn_hldn_qty_rate: s(),
    etf_trc_ert_mltp: s(),
    dprt: s(),
    mbcr_name: s(),
    stck_lstn_date: s(),
    mtrt_date: s(),
    shrg_type_code: s(),
    lp_hldn_rate: s(),
    etf_trgt_nmix_bstp_code: s(),
    etf_div_name: s(),
    etf_rprs_bstp_kor_isnm: s(),
    lp_hldn_vol: s(),
  })
  .passthrough();

export const getEtfetnCurrentPriceResponseSchema = z
  .object({
    ...kisEnvelope,
    output: getEtfetnCurrentPriceItemSchema.optional(),
  })
  .passthrough();

// ── getEtfComponentStockPrice: Domestic Etf Component Stock Price ──

export const getEtfComponentStockPriceOutput1ItemSchema = z
  .object({
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    etf_cnfg_issu_avls: s(),
    nav: s(),
    nav_prdy_vrss_sign: s(),
    nav_prdy_vrss: s(),
    nav_prdy_ctrt: s(),
    etf_ntas_ttam: s(),
    prdy_clpr_nav: s(),
    oprc_nav: s(),
    hprc_nav: s(),
    lprc_nav: s(),
    etf_cu_unit_scrt_cnt: s(),
    etf_cnfg_issu_cnt: s(),
  })
  .passthrough();

export const getEtfComponentStockPriceOutput2ItemSchema = z
  .object({
    stck_shrn_iscd: s(),
    hts_kor_isnm: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    acml_tr_pbmn: s(),
    tday_rsfl_rate: s(),
    prdy_vrss_vol: s(),
    tr_pbmn_tnrt: s(),
    hts_avls: s(),
    etf_cnfg_issu_avls: s(),
    etf_cnfg_issu_rlim: s(),
    etf_cu_unit_scrt_cnt: s(),
    etf_vltn_amt: s(),
  })
  .passthrough();

export const getEtfComponentStockPriceResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getEtfComponentStockPriceOutput1ItemSchema.optional(),
    output2: z.array(getEtfComponentStockPriceOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getEtfNavComparisonTrend: Domestic Etf Nav Comparison Trend ──

export const getEtfNavComparisonTrendOutput1ItemSchema = z
  .object({
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    acml_tr_pbmn: s(),
    stck_prdy_clpr: s(),
    stck_oprc: s(),
    stck_hgpr: s(),
    stck_lwpr: s(),
    stck_mxpr: s(),
    stck_llam: s(),
  })
  .passthrough();

export const getEtfNavComparisonTrendOutput2ItemSchema = z
  .object({
    nav: s(),
    nav_prdy_vrss_sign: s(),
    nav_prdy_vrss: s(),
    nav_prdy_ctrt: s(),
    prdy_clpr_nav: s(),
    oprc_nav: s(),
    hprc_nav: s(),
    lprc_nav: s(),
  })
  .passthrough();

export const getEtfNavComparisonTrendResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getEtfNavComparisonTrendOutput1ItemSchema.optional(),
    output2: getEtfNavComparisonTrendOutput2ItemSchema.optional(),
  })
  .passthrough();

// ── getEtfNavComparisonDailyTrend: Domestic Etf Nav Comparison Daily Trend ──

export const getEtfNavComparisonDailyTrendItemSchema = z
  .object({
    stck_bsop_date: s(),
    stck_clpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    cntg_vol: s(),
    dprt: s(),
    nav_vrss_prpr: s(),
    nav: s(),
    nav_prdy_vrss_sign: s(),
    nav_prdy_vrss: s(),
    nav_prdy_ctrt: s(),
  })
  .passthrough();

export const getEtfNavComparisonDailyTrendResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getEtfNavComparisonDailyTrendItemSchema).default([]),
  })
  .passthrough();

// ── getEtfNavComparisonTimeTrend: Domestic Etf Nav Comparison Time Trend ──

export const getEtfNavComparisonTimeTrendItemSchema = z
  .object({
    bsop_hour: s(),
    nav: s(),
    nav_prdy_vrss_sign: s(),
    nav_prdy_vrss: s(),
    nav_prdy_ctrt: s(),
    nav_vrss_prpr: s(),
    dprt: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    cntg_vol: s(),
  })
  .passthrough();

export const getEtfNavComparisonTimeTrendResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getEtfNavComparisonTimeTrendItemSchema).default([]),
  })
  .passthrough();

// ── Response Types ──

export type GetStockCurrentPriceResponse = CamelizeKeys<z.infer<typeof getStockCurrentPriceResponseSchema>>;

export type GetStockCurrentPrice2Response = CamelizeKeys<z.infer<typeof getStockCurrentPrice2ResponseSchema>>;

export type GetStockCurrentPriceConclusionResponse = CamelizeKeys<
  z.infer<typeof getStockCurrentPriceConclusionResponseSchema>
>;

export type GetStockCurrentPriceDailyResponse = CamelizeKeys<z.infer<typeof getStockCurrentPriceDailyResponseSchema>>;

export type GetStockCurrentPriceAskingExpectedConclusionResponse = CamelizeKeys<
  z.infer<typeof getStockCurrentPriceAskingExpectedConclusionResponseSchema>
>;

export type GetStockCurrentPriceInvestorResponse = CamelizeKeys<
  z.infer<typeof getStockCurrentPriceInvestorResponseSchema>
>;

export type GetStockCurrentPriceMemberResponse = CamelizeKeys<z.infer<typeof getStockCurrentPriceMemberResponseSchema>>;

export type GetStockPeriodQuoteResponse = CamelizeKeys<z.infer<typeof getStockPeriodQuoteResponseSchema>>;

export type GetStockTodayMinuteChartResponse = CamelizeKeys<z.infer<typeof getStockTodayMinuteChartResponseSchema>>;

export type GetStockDailyMinuteChartResponse = CamelizeKeys<z.infer<typeof getStockDailyMinuteChartResponseSchema>>;

export type GetStockCurrentPriceTimeItemConclusionResponse = CamelizeKeys<
  z.infer<typeof getStockCurrentPriceTimeItemConclusionResponseSchema>
>;

export type GetStockCurrentPriceDailyOvertimePriceResponse = CamelizeKeys<
  z.infer<typeof getStockCurrentPriceDailyOvertimePriceResponseSchema>
>;

export type GetStockCurrentPriceOvertimeConclusionResponse = CamelizeKeys<
  z.infer<typeof getStockCurrentPriceOvertimeConclusionResponseSchema>
>;

export type GetStockOvertimeCurrentPriceResponse = CamelizeKeys<
  z.infer<typeof getStockOvertimeCurrentPriceResponseSchema>
>;

export type GetStockOvertimeAskingPriceResponse = CamelizeKeys<
  z.infer<typeof getStockOvertimeAskingPriceResponseSchema>
>;

export type GetStockClosingExpectedPriceResponse = CamelizeKeys<
  z.infer<typeof getStockClosingExpectedPriceResponseSchema>
>;

export type GetEtfetnCurrentPriceResponse = CamelizeKeys<z.infer<typeof getEtfetnCurrentPriceResponseSchema>>;

export type GetEtfComponentStockPriceResponse = CamelizeKeys<z.infer<typeof getEtfComponentStockPriceResponseSchema>>;

export type GetEtfNavComparisonTrendResponse = CamelizeKeys<z.infer<typeof getEtfNavComparisonTrendResponseSchema>>;

export type GetEtfNavComparisonDailyTrendResponse = CamelizeKeys<
  z.infer<typeof getEtfNavComparisonDailyTrendResponseSchema>
>;

export type GetEtfNavComparisonTimeTrendResponse = CamelizeKeys<
  z.infer<typeof getEtfNavComparisonTimeTrendResponseSchema>
>;

// ── Response Map ──

export interface DomesticBasicQuoteResponseMap {
  getStockCurrentPrice: GetStockCurrentPriceResponse;
  getStockCurrentPrice2: GetStockCurrentPrice2Response;
  getStockCurrentPriceConclusion: GetStockCurrentPriceConclusionResponse;
  getStockCurrentPriceDaily: GetStockCurrentPriceDailyResponse;
  getStockCurrentPriceAskingExpectedConclusion: GetStockCurrentPriceAskingExpectedConclusionResponse;
  getStockCurrentPriceInvestor: GetStockCurrentPriceInvestorResponse;
  getStockCurrentPriceMember: GetStockCurrentPriceMemberResponse;
  getStockPeriodQuote: GetStockPeriodQuoteResponse;
  getStockTodayMinuteChart: GetStockTodayMinuteChartResponse;
  getStockDailyMinuteChart: GetStockDailyMinuteChartResponse;
  getStockCurrentPriceTimeItemConclusion: GetStockCurrentPriceTimeItemConclusionResponse;
  getStockCurrentPriceDailyOvertimePrice: GetStockCurrentPriceDailyOvertimePriceResponse;
  getStockCurrentPriceOvertimeConclusion: GetStockCurrentPriceOvertimeConclusionResponse;
  getStockOvertimeCurrentPrice: GetStockOvertimeCurrentPriceResponse;
  getStockOvertimeAskingPrice: GetStockOvertimeAskingPriceResponse;
  getStockClosingExpectedPrice: GetStockClosingExpectedPriceResponse;
  getEtfetnCurrentPrice: GetEtfetnCurrentPriceResponse;
  getEtfComponentStockPrice: GetEtfComponentStockPriceResponse;
  getEtfNavComparisonTrend: GetEtfNavComparisonTrendResponse;
  getEtfNavComparisonDailyTrend: GetEtfNavComparisonDailyTrendResponse;
  getEtfNavComparisonTimeTrend: GetEtfNavComparisonTimeTrendResponse;
}
