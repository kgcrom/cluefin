import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types';

const s = () => z.string().default('');

const kisEnvelope = {
  rt_cd: z.string().optional(),
  msg_cd: z.string().optional(),
  msg1: z.string().optional(),
};

// ── getStockCurrentPriceDetail: Stock Current Price Detail ──

export const getStockCurrentPriceDetailItemSchema = z
  .object({
    rsym: s(),
    pvol: s(),
    open: s(),
    high: s(),
    low: s(),
    last: s(),
    base: s(),
    tomv: s(),
    pamt: s(),
    uplp: s(),
    dnlp: s(),
    h52p: s(),
    h52d: s(),
    l52p: s(),
    l52d: s(),
    perx: s(),
    pbrx: s(),
    epsx: s(),
    bpsx: s(),
    shar: s(),
    mcap: s(),
    curr: s(),
    zdiv: s(),
    vnit: s(),
    t_xprc: s(),
    t_xdif: s(),
    t_xrat: s(),
    p_xprc: s(),
    p_xdif: s(),
    p_xrat: s(),
    t_rate: s(),
    p_rate: s(),
    t_xsgn: s(),
    p_xsng: s(),
    e_ordyn: s(),
    e_hogau: s(),
    e_icod: s(),
    e_parp: s(),
    tvol: s(),
    tamt: s(),
    etyp_nm: s(),
  })
  .passthrough();

export const getStockCurrentPriceDetailResponseSchema = z
  .object({
    ...kisEnvelope,
    output: getStockCurrentPriceDetailItemSchema.optional(),
  })
  .passthrough();

// ── getCurrentPriceFirstQuote: Current Price First Quote ──

export const getCurrentPriceFirstQuoteOutput1ItemSchema = z
  .object({
    rsym: s(),
    zdiv: s(),
    curr: s(),
    base: s(),
    open: s(),
    high: s(),
    low: s(),
    last: s(),
    dymd: s(),
    dhms: s(),
    bvol: s(),
    avol: s(),
    bdvl: s(),
    advl: s(),
    code: s(),
    ropen: s(),
    rhigh: s(),
    rlow: s(),
    rclose: s(),
  })
  .passthrough();

export const getCurrentPriceFirstQuoteOutput2ItemSchema = z
  .object({
    pbid1: s(),
    pask1: s(),
    vbid1: s(),
    vask1: s(),
    dbid1: s(),
    dask1: s(),
  })
  .passthrough();

export const getCurrentPriceFirstQuoteOutput3ItemSchema = z
  .object({
    vstm: z.string().optional(),
    vetm: z.string().optional(),
    csbp: z.string().optional(),
    cshi: z.string().optional(),
    cslo: z.string().optional(),
    iep: z.string().optional(),
    iev: z.string().optional(),
  })
  .passthrough();

export const getCurrentPriceFirstQuoteResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getCurrentPriceFirstQuoteOutput1ItemSchema.optional(),
    output2: getCurrentPriceFirstQuoteOutput2ItemSchema.optional(),
    output3: getCurrentPriceFirstQuoteOutput3ItemSchema.optional(),
  })
  .passthrough();

// ── getStockCurrentPriceConclusion: Stock Current Price Conclusion ──

export const getStockCurrentPriceConclusionItemSchema = z
  .object({
    rsym: s(),
    zdiv: s(),
    base: s(),
    pvol: s(),
    last: s(),
    sign: s(),
    diff: s(),
    rate: s(),
    tvol: s(),
    tamt: s(),
    ordy: s(),
  })
  .passthrough();

export const getStockCurrentPriceConclusionResponseSchema = z
  .object({
    ...kisEnvelope,
    output: getStockCurrentPriceConclusionItemSchema.optional(),
  })
  .passthrough();

// ── getConclusionTrend: Conclusion Trend ──

export const getConclusionTrendOutput1ItemSchema = z
  .object({
    rsym: s(),
    zdiv: s(),
    stat: z.string().optional(),
    crec: z.string().optional(),
    trec: z.string().optional(),
    nrec: s(),
  })
  .passthrough();

export const getConclusionTrendOutput2ItemSchema = z
  .object({
    khms: s(),
    last: s(),
    sign: s(),
    diff: s(),
    rate: s(),
    evol: s(),
    tvol: s(),
    mtyp: s(),
    pbid: s(),
    pask: s(),
    vpow: s(),
  })
  .passthrough();

export const getConclusionTrendResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getConclusionTrendOutput1ItemSchema.optional(),
    output2: z.array(getConclusionTrendOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getStockMinuteChart: Stock Minute Chart ──

export const getStockMinuteChartOutput1ItemSchema = z
  .object({
    rsym: s(),
    zdiv: s(),
    stim: s(),
    etim: s(),
    sktm: s(),
    ektm: s(),
    next: s(),
    more: s(),
    nrec: s(),
  })
  .passthrough();

export const getStockMinuteChartOutput2ItemSchema = z
  .object({
    tymd: s(),
    xymd: s(),
    xhms: s(),
    kymd: s(),
    khms: s(),
    open: s(),
    high: s(),
    low: s(),
    last: s(),
    evol: s(),
    eamt: s(),
  })
  .passthrough();

export const getStockMinuteChartResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getStockMinuteChartOutput1ItemSchema.optional(),
    output2: z.array(getStockMinuteChartOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getIndexMinuteChart: Index Minute Chart ──

export const getIndexMinuteChartOutput1ItemSchema = z
  .object({
    ovrs_nmix_prdy_vrss: s(),
    prdy_vrss_sign: s(),
    hts_kor_isnm: s(),
    prdy_ctrt: s(),
    ovrs_nmix_prdy_clpr: s(),
    acml_vol: s(),
    ovrs_nmix_prpr: s(),
    stck_shrn_iscd: s(),
    ovrs_prod_oprc: s(),
    ovrs_prod_hgpr: s(),
    ovrs_prod_lwpr: s(),
  })
  .passthrough();

export const getIndexMinuteChartOutput2ItemSchema = z
  .object({
    stck_bsop_date: s(),
    stck_cntg_hour: s(),
    optn_prpr: s(),
    optn_oprc: s(),
    optn_hgpr: s(),
    optn_lwpr: s(),
    cntg_vol: s(),
  })
  .passthrough();

export const getIndexMinuteChartResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getIndexMinuteChartOutput1ItemSchema.optional(),
    output2: z.array(getIndexMinuteChartOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getStockPeriodQuote: Stock Period Quote ──

export const getStockPeriodQuoteOutput1ItemSchema = z
  .object({
    rsym: s(),
    zdiv: s(),
    nrec: s(),
  })
  .passthrough();

export const getStockPeriodQuoteOutput2ItemSchema = z
  .object({
    xymd: s(),
    clos: s(),
    sign: s(),
    diff: s(),
    rate: s(),
    open: s(),
    high: s(),
    low: s(),
    tvol: s(),
    tamt: s(),
    pbid: z.string().optional(),
    vbid: z.string().optional(),
    pask: z.string().optional(),
    vask: z.string().optional(),
  })
  .passthrough();

export const getStockPeriodQuoteResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getStockPeriodQuoteOutput1ItemSchema.optional(),
    output2: z.array(getStockPeriodQuoteOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getItemIndexExchangePeriodPrice: Item Index Exchange Period Price ──

export const getItemIndexExchangePeriodPriceOutput1ItemSchema = z
  .object({
    ovrs_nmix_prdy_vrss: z.string().optional(),
    prdy_vrss_sign: z.string().optional(),
    prdy_ctrt: z.string().optional(),
    ovrs_nmix_prdy_clpr: z.string().optional(),
    acml_vol: z.string().optional(),
    hts_kor_isnm: z.string().optional(),
    ovrs_nmix_prpr: z.string().optional(),
    stck_shrn_iscd: z.string().optional(),
    prdy_vol: z.string().optional(),
    ovrs_prod_oprc: z.string().optional(),
    ovrs_prod_hgpr: z.string().optional(),
    ovrs_prod_lwpr: z.string().optional(),
  })
  .passthrough();

export const getItemIndexExchangePeriodPriceOutput2ItemSchema = z
  .object({
    stck_bsop_date: z.string().optional(),
    ovrs_nmix_prpr: z.string().optional(),
    ovrs_nmix_oprc: z.string().optional(),
    ovrs_nmix_hgpr: z.string().optional(),
    ovrs_nmix_lwpr: z.string().optional(),
    acml_vol: z.string().optional(),
    mod_yn: z.string().optional(),
  })
  .passthrough();

export const getItemIndexExchangePeriodPriceResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getItemIndexExchangePeriodPriceOutput1ItemSchema.optional(),
    output2: z.array(getItemIndexExchangePeriodPriceOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── searchByCondition: Search By Condition ──

export const searchByConditionOutput1ItemSchema = z
  .object({
    zdiv: z.string().optional(),
    stat: z.string().optional(),
    crec: z.string().optional(),
    trec: z.string().optional(),
    nrec: z.string().optional(),
  })
  .passthrough();

export const searchByConditionOutput2ItemSchema = z
  .object({
    rsym: z.string().optional(),
    excd: z.string().optional(),
    name: z.string().optional(),
    symb: z.string().optional(),
    last: z.string().optional(),
    shar: z.string().optional(),
    valx: z.string().optional(),
    plow: z.string().optional(),
    phigh: z.string().optional(),
    popen: z.string().optional(),
    tvol: z.string().optional(),
    rate: z.string().optional(),
    diff: z.string().optional(),
    sign: z.string().optional(),
    avol: z.string().optional(),
    eps: z.string().optional(),
    per: z.string().optional(),
    rank: z.string().optional(),
    ename: z.string().optional(),
    e_ordyn: z.string().optional(),
  })
  .passthrough();

export const searchByConditionResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: searchByConditionOutput1ItemSchema.optional(),
    output2: z.array(searchByConditionOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getSettlementDate: Settlement Date ──

export const getSettlementDateItemSchema = z
  .object({
    prdt_type_cd: s(),
    tr_natn_cd: s(),
    tr_natn_name: s(),
    natn_eng_abrv_cd: s(),
    tr_mket_cd: s(),
    tr_mket_name: s(),
    acpl_sttl_dt: s(),
    dmst_sttl_dt: s(),
  })
  .passthrough();

export const getSettlementDateResponseSchema = z
  .object({
    ...kisEnvelope,
    ctx_area_fk: s(),
    ctx_area_nk: s(),
    output: z.array(getSettlementDateItemSchema).default([]),
  })
  .passthrough();

// ── getProductBaseInfo: Product Base Info ──

export const getProductBaseInfoItemSchema = z
  .object({
    std_pdno: s(),
    prdt_eng_name: s(),
    natn_cd: s(),
    natn_name: s(),
    tr_mket_cd: s(),
    tr_mket_name: s(),
    ovrs_excg_cd: s(),
    ovrs_excg_name: s(),
    tr_crcy_cd: s(),
    ovrs_papr: s(),
    crcy_name: s(),
    ovrs_stck_dvsn_cd: s(),
    prdt_clsf_cd: s(),
    prdt_clsf_name: s(),
    sll_unit_qty: s(),
    buy_unit_qty: s(),
    tr_unit_amt: s(),
    lstg_stck_num: s(),
    lstg_dt: s(),
    ovrs_stck_tr_stop_dvsn_cd: s(),
    lstg_abol_item_yn: s(),
    ovrs_stck_prdt_grp_no: s(),
    lstg_yn: s(),
    tax_levy_yn: s(),
    ovrs_stck_erlm_rosn_cd: s(),
    ovrs_stck_hist_rght_dvsn_cd: s(),
    chng_bf_pdno: s(),
    prdt_type_cd_2: s(),
    ovrs_item_name: s(),
    sedol_no: s(),
    blbg_tckr_text: s(),
    ovrs_stck_etf_risk_drtp_cd: s(),
    etp_chas_erng_rt_dbnb: s(),
    istt_usge_isin_cd: s(),
    mint_svc_yn: s(),
    mint_svc_yn_chng_dt: s(),
    prdt_name: s(),
    lei_cd: s(),
    ovrs_stck_stop_rson_cd: s(),
    lstg_abol_dt: s(),
    mini_stk_tr_stat_dvsn_cd: s(),
    mint_frst_svc_erlm_dt: s(),
    mint_dcpt_trad_psbl_yn: s(),
    mint_fnum_trad_psbl_yn: s(),
    mint_cblc_cvsn_ipsb_yn: s(),
    ptp_item_yn: s(),
    ptp_item_trfx_exmt_yn: s(),
    ptp_item_trfx_exmt_strt_dt: s(),
    ptp_item_trfx_exmt_end_dt: s(),
    dtm_tr_psbl_yn: s(),
    sdrf_stop_ecls_yn: s(),
    sdrf_stop_ecls_erlm_dt: s(),
    memo_text1: s(),
    ovrs_now_pric1: s(),
    last_rcvg_dtime: s(),
  })
  .passthrough();

export const getProductBaseInfoResponseSchema = z
  .object({
    ...kisEnvelope,
    output: getProductBaseInfoItemSchema.optional(),
  })
  .passthrough();

// ── getSectorPrice: Sector Price ──

export const getSectorPriceOutput1ItemSchema = z
  .object({
    zdiv: s(),
    stat: s(),
    crec: s(),
    trec: s(),
    nrec: s(),
  })
  .passthrough();

export const getSectorPriceOutput2ItemSchema = z
  .object({
    rsym: s(),
    excd: s(),
    symb: s(),
    name: s(),
    last: s(),
    sign: s(),
    diff: s(),
    rate: s(),
    tvol: s(),
    vask: s(),
    pask: s(),
    pbid: s(),
    vbid: s(),
    seqn: s(),
    ename: s(),
    e_ordyn: s(),
  })
  .passthrough();

export const getSectorPriceResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getSectorPriceOutput1ItemSchema.optional(),
    output2: z.array(getSectorPriceOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getSectorCodes: Sector Codes ──

export const getSectorCodesOutput1ItemSchema = z
  .object({
    nrec: s(),
  })
  .passthrough();

export const getSectorCodesOutput2ItemSchema = z
  .object({
    icod: s(),
    name: s(),
  })
  .passthrough();

export const getSectorCodesResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getSectorCodesOutput1ItemSchema.optional(),
    output2: z.array(getSectorCodesOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── Response Types ──

export type GetStockCurrentPriceDetailResponse = CamelizeKeys<z.infer<typeof getStockCurrentPriceDetailResponseSchema>>;

export type GetCurrentPriceFirstQuoteResponse = CamelizeKeys<z.infer<typeof getCurrentPriceFirstQuoteResponseSchema>>;

export type GetStockCurrentPriceConclusionResponse = CamelizeKeys<
  z.infer<typeof getStockCurrentPriceConclusionResponseSchema>
>;

export type GetConclusionTrendResponse = CamelizeKeys<z.infer<typeof getConclusionTrendResponseSchema>>;

export type GetStockMinuteChartResponse = CamelizeKeys<z.infer<typeof getStockMinuteChartResponseSchema>>;

export type GetIndexMinuteChartResponse = CamelizeKeys<z.infer<typeof getIndexMinuteChartResponseSchema>>;

export type GetStockPeriodQuoteResponse = CamelizeKeys<z.infer<typeof getStockPeriodQuoteResponseSchema>>;

export type GetItemIndexExchangePeriodPriceResponse = CamelizeKeys<
  z.infer<typeof getItemIndexExchangePeriodPriceResponseSchema>
>;

export type SearchByConditionResponse = CamelizeKeys<z.infer<typeof searchByConditionResponseSchema>>;

export type GetSettlementDateResponse = CamelizeKeys<z.infer<typeof getSettlementDateResponseSchema>>;

export type GetProductBaseInfoResponse = CamelizeKeys<z.infer<typeof getProductBaseInfoResponseSchema>>;

export type GetSectorPriceResponse = CamelizeKeys<z.infer<typeof getSectorPriceResponseSchema>>;

export type GetSectorCodesResponse = CamelizeKeys<z.infer<typeof getSectorCodesResponseSchema>>;

// ── Response Map ──

export interface OverseasBasicQuoteResponseMap {
  getStockCurrentPriceDetail: GetStockCurrentPriceDetailResponse;
  getCurrentPriceFirstQuote: GetCurrentPriceFirstQuoteResponse;
  getStockCurrentPriceConclusion: GetStockCurrentPriceConclusionResponse;
  getConclusionTrend: GetConclusionTrendResponse;
  getStockMinuteChart: GetStockMinuteChartResponse;
  getIndexMinuteChart: GetIndexMinuteChartResponse;
  getStockPeriodQuote: GetStockPeriodQuoteResponse;
  getItemIndexExchangePeriodPrice: GetItemIndexExchangePeriodPriceResponse;
  searchByCondition: SearchByConditionResponse;
  getSettlementDate: GetSettlementDateResponse;
  getProductBaseInfo: GetProductBaseInfoResponse;
  getSectorPrice: GetSectorPriceResponse;
  getSectorCodes: GetSectorCodesResponse;
}
