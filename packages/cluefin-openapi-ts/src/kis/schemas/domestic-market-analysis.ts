import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types';

const s = () => z.string().default('');

const kisEnvelope = {
  rt_cd: z.string().optional(),
  msg_cd: z.string().optional(),
  msg1: z.string().optional(),
};

// ── getConditionSearchList: Condition Search List ──

export const getConditionSearchListItemSchema = z
  .object({
    user_id: s(),
    seq: s(),
    grp_nm: s(),
    condition_nm: s(),
  })
  .passthrough();

export const getConditionSearchListResponseSchema = z
  .object({
    ...kisEnvelope,
    output2: z.array(getConditionSearchListItemSchema).default([]),
  })
  .passthrough();

// ── getConditionSearchResult: Condition Search Result ──

export const getConditionSearchResultItemSchema = z
  .object({
    code: s(),
    name: s(),
    daebi: s(),
    price: s(),
    chgrate: s(),
    acml_vol: s(),
    trade_amt: s(),
    change: s(),
    cttr: s(),
    open: s(),
    high: s(),
    low: s(),
    high52: s(),
    low52: s(),
    expprice: s(),
    expchange: s(),
    expchggrate: s(),
    expcvol: s(),
    chgrate2: s(),
    expdaebi: s(),
    recprice: s(),
    uplmtprice: s(),
    dnlmtprice: s(),
    stotprice: s(),
  })
  .passthrough();

export const getConditionSearchResultResponseSchema = z
  .object({
    ...kisEnvelope,
    output2: z.array(getConditionSearchResultItemSchema).default([]),
  })
  .passthrough();

// ── getWatchlistGroups: Watchlist Groups ──

export const getWatchlistGroupsItemSchema = z
  .object({
    date: s(),
    trnm_hour: s(),
    data_rank: s(),
    inter_grp_code: s(),
    inter_grp_name: s(),
    ask_cnt: s(),
  })
  .passthrough();

export const getWatchlistGroupsResponseSchema = z
  .object({
    ...kisEnvelope,
    output2: z.array(getWatchlistGroupsItemSchema).default([]),
  })
  .passthrough();

// ── getWatchlistMultiQuote: Watchlist Multi Quote ──

export const getWatchlistMultiQuoteItemSchema = z
  .object({
    kospi_kosdaq_cls_name: s(),
    mrkt_trtm_cls_name: s(),
    hour_cls_code: s(),
    inter_shrn_iscd: s(),
    inter_kor_isnm: s(),
    inter2_prpr: s(),
    inter2_prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    inter2_oprc: s(),
    inter2_hgpr: s(),
    inter2_lwpr: s(),
    inter2_llam: s(),
    inter2_mxpr: s(),
    inter2_askp: s(),
    inter2_bidp: s(),
    seln_rsqn: s(),
    shnu_rsqn: s(),
    total_askp_rsqn: s(),
    total_bidp_rsqn: s(),
    acml_tr_pbmn: s(),
    inter2_prdy_clpr: s(),
    oprc_vrss_hgpr_rate: s(),
    intr_antc_cntg_vrss: s(),
    intr_antc_cntg_vrss_sign: s(),
    intr_antc_cntg_prdy_ctrt: s(),
    intr_antc_vol: s(),
    inter2_sdpr: s(),
  })
  .passthrough();

export const getWatchlistMultiQuoteResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getWatchlistMultiQuoteItemSchema).default([]),
  })
  .passthrough();

// ── getWatchlistStocksByGroup: Watchlist Stocks By Group ──

export const getWatchlistStocksByGroupOutput1ItemSchema = z
  .object({
    data_rank: s(),
    inter_grp_name: s(),
  })
  .passthrough();

export const getWatchlistStocksByGroupOutput2ItemSchema = z
  .object({
    fid_mrkt_cls_code: s(),
    data_rank: s(),
    exch_code: s(),
    jong_code: s(),
    color_code: s(),
    memo: z.string().optional(),
    hts_kor_isnm: s(),
    fxdt_ntby_qty: s(),
    cntg_unpr: s(),
    cntg_cls_code: s(),
  })
  .passthrough();

export const getWatchlistStocksByGroupResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getWatchlistStocksByGroupOutput1ItemSchema.optional(),
    output2: z.array(getWatchlistStocksByGroupOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getInstitutionalForeignTradingAggregate: Institutional Foreign Trading Aggregate ──

export const getInstitutionalForeignTradingAggregateItemSchema = z
  .object({
    hts_kor_isnm: s(),
    mksc_shrn_iscd: s(),
    ntby_qty: s(),
    stck_prpr: s(),
    prdy_vrss_sign: s(),
    prdy_vrss: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    frgn_ntby_qty: s(),
    orgn_ntby_qty: s(),
    ivtr_ntby_qty: s(),
    bank_ntby_qty: s(),
    insu_ntby_qty: s(),
    mrbn_ntby_qty: s(),
    fund_ntby_qty: s(),
    etc_orgt_ntby_vol: s(),
    etc_corp_ntby_vol: s(),
    frgn_ntby_tr_pbmn: s(),
    orgn_ntby_tr_pbmn: s(),
    ivtr_ntby_tr_pbmn: s(),
    bank_ntby_tr_pbmn: s(),
    insu_ntby_tr_pbmn: s(),
    mrbn_ntby_tr_pbmn: s(),
    fund_ntby_tr_pbmn: s(),
    etc_orgt_ntby_tr_pbmn: s(),
    etc_corp_ntby_tr_pbmn: s(),
  })
  .passthrough();

export const getInstitutionalForeignTradingAggregateResponseSchema = z
  .object({
    ...kisEnvelope,
    output: getInstitutionalForeignTradingAggregateItemSchema.optional(),
  })
  .passthrough();

// ── getForeignBrokerageTradingAggregate: Foreign Brokerage Trading Aggregate ──

export const getForeignBrokerageTradingAggregateItemSchema = z
  .object({
    stck_shrn_iscd: s(),
    hts_kor_isnm: s(),
    glob_ntsl_qty: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    glob_total_seln_qty: s(),
    glob_total_shnu_qty: s(),
  })
  .passthrough();

export const getForeignBrokerageTradingAggregateResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getForeignBrokerageTradingAggregateItemSchema).default([]),
  })
  .passthrough();

// ── getInvestorTradingTrendByStockDaily: Investor Trading Trend By Stock Daily ──

export const getInvestorTradingTrendByStockDailyOutput1ItemSchema = z
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

export const getInvestorTradingTrendByStockDailyOutput2ItemSchema = z
  .object({
    stck_bsop_date: s(),
    stck_clpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    acml_tr_pbmn: s(),
    stck_oprc: s(),
    stck_hgpr: s(),
    stck_lwpr: s(),
    frgn_ntby_qty: s(),
    frgn_reg_ntby_qty: s(),
    frgn_nreg_ntby_qty: s(),
    prsn_ntby_qty: s(),
    orgn_ntby_qty: s(),
    scrt_ntby_qty: s(),
    ivtr_ntby_qty: s(),
    pe_fund_ntby_vol: s(),
    bank_ntby_qty: s(),
    insu_ntby_qty: s(),
    mrbn_ntby_qty: s(),
    fund_ntby_qty: s(),
    etc_ntby_qty: s(),
    etc_corp_ntby_vol: s(),
    etc_orgt_ntby_vol: s(),
    frgn_reg_ntby_pbmn: s(),
    frgn_ntby_tr_pbmn: s(),
    frgn_nreg_ntby_pbmn: s(),
    prsn_ntby_tr_pbmn: s(),
    orgn_ntby_tr_pbmn: s(),
    scrt_ntby_tr_pbmn: s(),
    pe_fund_ntby_tr_pbmn: s(),
    ivtr_ntby_tr_pbmn: s(),
    bank_ntby_tr_pbmn: s(),
    insu_ntby_tr_pbmn: s(),
    mrbn_ntby_tr_pbmn: s(),
    fund_ntby_tr_pbmn: s(),
    etc_ntby_tr_pbmn: s(),
    etc_corp_ntby_tr_pbmn: s(),
    etc_orgt_ntby_tr_pbmn: s(),
    frgn_seln_vol: s(),
    frgn_shnu_vol: s(),
    frgn_seln_tr_pbmn: s(),
    frgn_shnu_tr_pbmn: s(),
    frgn_reg_askp_qty: s(),
    frgn_reg_bidp_qty: s(),
    frgn_reg_askp_pbmn: s(),
    frgn_reg_bidp_pbmn: s(),
    frgn_nreg_askp_qty: s(),
    frgn_nreg_bidp_qty: s(),
    frgn_nreg_askp_pbmn: s(),
    frgn_nreg_bidp_pbmn: s(),
    prsn_seln_vol: s(),
    prsn_shnu_vol: s(),
    prsn_seln_tr_pbmn: s(),
    prsn_shnu_tr_pbmn: s(),
    orgn_seln_vol: s(),
    orgn_shnu_vol: s(),
    orgn_seln_tr_pbmn: s(),
    orgn_shnu_tr_pbmn: s(),
    scrt_seln_vol: s(),
    scrt_shnu_vol: s(),
    scrt_seln_tr_pbmn: s(),
    scrt_shnu_tr_pbmn: s(),
    ivtr_seln_vol: s(),
    ivtr_shnu_vol: s(),
    ivtr_seln_tr_pbmn: s(),
    ivtr_shnu_tr_pbmn: s(),
    pe_fund_seln_tr_pbmn: s(),
    pe_fund_seln_vol: s(),
    pe_fund_shnu_tr_pbmn: s(),
    pe_fund_shnu_vol: s(),
    bank_seln_vol: s(),
    bank_shnu_vol: s(),
    bank_seln_tr_pbmn: s(),
    bank_shnu_tr_pbmn: s(),
    insu_seln_vol: s(),
    insu_shnu_vol: s(),
    insu_seln_tr_pbmn: s(),
    insu_shnu_tr_pbmn: s(),
    mrbn_seln_vol: s(),
    mrbn_shnu_vol: s(),
    mrbn_seln_tr_pbmn: s(),
    mrbn_shnu_tr_pbmn: s(),
    fund_seln_vol: s(),
    fund_shnu_vol: s(),
    fund_seln_tr_pbmn: s(),
    fund_shnu_tr_pbmn: s(),
    etc_seln_vol: s(),
    etc_shnu_vol: s(),
    etc_seln_tr_pbmn: s(),
    etc_shnu_tr_pbmn: s(),
    etc_orgt_seln_vol: s(),
    etc_orgt_shnu_vol: s(),
    etc_orgt_seln_tr_pbmn: s(),
    etc_orgt_shnu_tr_pbmn: s(),
    etc_corp_seln_vol: s(),
    etc_corp_shnu_vol: s(),
    etc_corp_seln_tr_pbmn: s(),
    etc_corp_shnu_tr_pbmn: s(),
    bold_yn: s(),
  })
  .passthrough();

export const getInvestorTradingTrendByStockDailyResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getInvestorTradingTrendByStockDailyOutput1ItemSchema.optional(),
    output2: z.array(getInvestorTradingTrendByStockDailyOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getInvestorTradingTrendByMarketIntraday: Investor Trading Trend By Market Intraday ──

export const getInvestorTradingTrendByMarketIntradayItemSchema = z
  .object({
    frgn_seln_vol: s(),
    frgn_shnu_vol: s(),
    frgn_ntby_qty: s(),
    frgn_seln_tr_pbmn: s(),
    frgn_shnu_tr_pbmn: s(),
    frgn_ntby_tr_pbmn: s(),
    prsn_seln_vol: s(),
    prsn_shnu_vol: s(),
    prsn_ntby_qty: s(),
    prsn_seln_tr_pbmn: s(),
    prsn_shnu_tr_pbmn: s(),
    prsn_ntby_tr_pbmn: s(),
    orgn_seln_vol: s(),
    orgn_shnu_vol: s(),
    orgn_ntby_qty: s(),
    orgn_seln_tr_pbmn: s(),
    orgn_shnu_tr_pbmn: s(),
    orgn_ntby_tr_pbmn: s(),
    scrt_seln_vol: s(),
    scrt_shnu_vol: s(),
    scrt_ntby_qty: s(),
    scrt_seln_tr_pbmn: s(),
    scrt_shnu_tr_pbmn: s(),
    scrt_ntby_tr_pbmn: s(),
    ivtr_seln_vol: s(),
    ivtr_shnu_vol: s(),
    ivtr_ntby_qty: s(),
    ivtr_seln_tr_pbmn: s(),
    ivtr_shnu_tr_pbmn: s(),
    ivtr_ntby_tr_pbmn: s(),
    pe_fund_seln_tr_pbmn: s(),
    pe_fund_seln_vol: s(),
    pe_fund_ntby_vol: s(),
    pe_fund_shnu_tr_pbmn: s(),
    pe_fund_shnu_vol: s(),
    pe_fund_ntby_tr_pbmn: s(),
    bank_seln_vol: s(),
    bank_shnu_vol: s(),
    bank_ntby_qty: s(),
    bank_seln_tr_pbmn: s(),
    bank_shnu_tr_pbmn: s(),
    bank_ntby_tr_pbmn: s(),
    insu_seln_vol: s(),
    insu_shnu_vol: s(),
    insu_ntby_qty: s(),
    insu_seln_tr_pbmn: s(),
    insu_shnu_tr_pbmn: s(),
    insu_ntby_tr_pbmn: s(),
    mrbn_seln_vol: s(),
    mrbn_shnu_vol: s(),
    mrbn_ntby_qty: s(),
    mrbn_seln_tr_pbmn: s(),
    mrbn_shnu_tr_pbmn: s(),
    mrbn_ntby_tr_pbmn: s(),
    fund_seln_vol: s(),
    fund_shnu_vol: s(),
    fund_ntby_qty: s(),
    fund_seln_tr_pbmn: s(),
    fund_shnu_tr_pbmn: s(),
    fund_ntby_tr_pbmn: s(),
    etc_orgt_seln_vol: s(),
    etc_orgt_shnu_vol: s(),
    etc_orgt_ntby_vol: s(),
    etc_orgt_seln_tr_pbmn: s(),
    etc_orgt_shnu_tr_pbmn: s(),
    etc_orgt_ntby_tr_pbmn: s(),
    etc_corp_seln_vol: s(),
    etc_corp_shnu_vol: s(),
    etc_corp_ntby_vol: s(),
    etc_corp_seln_tr_pbmn: s(),
    etc_corp_shnu_tr_pbmn: s(),
    etc_corp_ntby_tr_pbmn: s(),
  })
  .passthrough();

export const getInvestorTradingTrendByMarketIntradayResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getInvestorTradingTrendByMarketIntradayItemSchema).default([]),
  })
  .passthrough();

// ── getInvestorTradingTrendByMarketDaily: Investor Trading Trend By Market Daily ──

export const getInvestorTradingTrendByMarketDailyItemSchema = z
  .object({
    stck_bsop_date: s(),
    bstp_nmix_prpr: s(),
    bstp_nmix_prdy_vrss: s(),
    prdy_vrss_sign: s(),
    bstp_nmix_prdy_ctrt: s(),
    bstp_nmix_oprc: s(),
    bstp_nmix_hgpr: s(),
    bstp_nmix_lwpr: s(),
    stck_prdy_clpr: s(),
    frgn_ntby_qty: s(),
    frgn_reg_ntby_qty: s(),
    frgn_nreg_ntby_qty: s(),
    prsn_ntby_qty: s(),
    orgn_ntby_qty: s(),
    scrt_ntby_qty: s(),
    ivtr_ntby_qty: s(),
    pe_fund_ntby_vol: s(),
    bank_ntby_qty: s(),
    insu_ntby_qty: s(),
    mrbn_ntby_qty: s(),
    fund_ntby_qty: s(),
    etc_ntby_qty: s(),
    etc_orgt_ntby_vol: s(),
    etc_corp_ntby_vol: s(),
    frgn_ntby_tr_pbmn: s(),
    frgn_reg_ntby_pbmn: s(),
    frgn_nreg_ntby_pbmn: s(),
    prsn_ntby_tr_pbmn: s(),
    orgn_ntby_tr_pbmn: s(),
    scrt_ntby_tr_pbmn: s(),
    ivtr_ntby_tr_pbmn: s(),
    pe_fund_ntby_tr_pbmn: s(),
    bank_ntby_tr_pbmn: s(),
    insu_ntby_tr_pbmn: s(),
    mrbn_ntby_tr_pbmn: s(),
    fund_ntby_tr_pbmn: s(),
    etc_ntby_tr_pbmn: s(),
    etc_orgt_ntby_tr_pbmn: s(),
    etc_corp_ntby_tr_pbmn: s(),
  })
  .passthrough();

export const getInvestorTradingTrendByMarketDailyResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getInvestorTradingTrendByMarketDailyItemSchema).default([]),
  })
  .passthrough();

// ── getForeignNetBuyTrendByStock: Foreign Net Buy Trend By Stock ──

export const getForeignNetBuyTrendByStockItemSchema = z
  .object({
    total_seln_qty: s(),
    total_shnu_qty: s(),
  })
  .passthrough();

export const getForeignNetBuyTrendByStockResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getForeignNetBuyTrendByStockItemSchema).default([]),
  })
  .passthrough();

// ── getMemberTradingTrendTick: Member Trading Trend Tick ──

export const getMemberTradingTrendTickOutput1ItemSchema = z
  .object({
    stck_bsop_date: s(),
    total_seln_qty: s(),
    total_shnu_qty: s(),
    ntby_qty: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
  })
  .passthrough();

export const getMemberTradingTrendTickOutput2ItemSchema = z
  .object({
    stck_bsop_date: s(),
    total_seln_qty: s(),
    total_shnu_qty: s(),
    ntby_qty: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
  })
  .passthrough();

export const getMemberTradingTrendTickResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: z.array(getMemberTradingTrendTickOutput1ItemSchema).default([]),
    output2: z.array(getMemberTradingTrendTickOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getMemberTradingTrendByStock: Member Trading Trend By Stock ──

export const getMemberTradingTrendByStockItemSchema = z
  .object({
    stck_bsop_date: s(),
    total_seln_qty: s(),
    total_shnu_qty: s(),
    ntby_qty: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
  })
  .passthrough();

export const getMemberTradingTrendByStockResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getMemberTradingTrendByStockItemSchema).default([]),
  })
  .passthrough();

// ── getProgramTradingTrendByStockIntraday: Program Trading Trend By Stock Intraday ──

export const getProgramTradingTrendByStockIntradayItemSchema = z
  .object({
    bsop_hour: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    whol_smtn_seln_vol: s(),
    whol_smtn_shnu_vol: s(),
    whol_smtn_ntby_qty: s(),
    whol_smtn_seln_tr_pbmn: s(),
    whol_smtn_shnu_tr_pbmn: s(),
    whol_smtn_ntby_tr_pbmn: s(),
    whol_ntby_vol_icdc: s(),
    whol_ntby_tr_pbmn_icdc: s(),
  })
  .passthrough();

export const getProgramTradingTrendByStockIntradayResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getProgramTradingTrendByStockIntradayItemSchema).default([]),
  })
  .passthrough();

// ── getProgramTradingTrendByStockDaily: Program Trading Trend By Stock Daily ──

export const getProgramTradingTrendByStockDailyItemSchema = z
  .object({
    stck_bsop_date: s(),
    stck_clpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    acml_tr_pbmn: s(),
    whol_smtn_seln_vol: s(),
    whol_smtn_shnu_vol: s(),
    whol_smtn_ntby_qty: s(),
    whol_smtn_seln_tr_pbmn: s(),
    whol_smtn_shnu_tr_pbmn: s(),
    whol_smtn_ntby_tr_pbmn: s(),
    whol_ntby_vol_icdc: s(),
    whol_ntby_tr_pbmn_icdc2: s(),
  })
  .passthrough();

export const getProgramTradingTrendByStockDailyResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getProgramTradingTrendByStockDailyItemSchema).default([]),
  })
  .passthrough();

// ── getForeignInstitutionalEstimateByStock: Foreign Institutional Estimate By Stock ──

export const getForeignInstitutionalEstimateByStockItemSchema = z
  .object({
    bsop_hour_gb: s(),
    frgn_fake_ntby_qty: s(),
    orgn_fake_ntby_qty: s(),
    sum_fake_ntby_qty: s(),
  })
  .passthrough();

export const getForeignInstitutionalEstimateByStockResponseSchema = z
  .object({
    ...kisEnvelope,
    output2: z.array(getForeignInstitutionalEstimateByStockItemSchema).default([]),
  })
  .passthrough();

// ── getBuySellVolumeByStockDaily: Buy Sell Volume By Stock Daily ──

export const getBuySellVolumeByStockDailyOutput1ItemSchema = z
  .object({
    shnu_cnqn_smtn: s(),
    seln_cnqn_smtn: s(),
  })
  .passthrough();

export const getBuySellVolumeByStockDailyOutput2ItemSchema = z
  .object({
    stck_bsop_date: s(),
    total_seln_qty: s(),
    total_shnu_qty: s(),
  })
  .passthrough();

export const getBuySellVolumeByStockDailyResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getBuySellVolumeByStockDailyOutput1ItemSchema.optional(),
    output2: z.array(getBuySellVolumeByStockDailyOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getProgramTradingSummaryIntraday: Program Trading Summary Intraday ──

export const getProgramTradingSummaryIntradayItemSchema = z
  .object({
    bsop_hour: s(),
    arbt_smtn_seln_tr_pbmn: s(),
    arbt_smtm_seln_tr_pbmn_rate: s(),
    arbt_smtn_shnu_tr_pbmn: s(),
    arbt_smtm_shun_tr_pbmn_rate: s(),
    nabt_smtn_seln_tr_pbmn: s(),
    nabt_smtm_seln_tr_pbmn_rate: s(),
    nabt_smtn_shnu_tr_pbmn: s(),
    nabt_smtm_shun_tr_pbmn_rate: s(),
    arbt_smtn_ntby_tr_pbmn: s(),
    arbt_smtm_ntby_tr_pbmn_rate: s(),
    nabt_smtn_ntby_tr_pbmn: s(),
    nabt_smtm_ntby_tr_pbmn_rate: s(),
    whol_smtn_ntby_tr_pbmn: s(),
    whol_ntby_tr_pbmn_rate: s(),
    bstp_nmix_prpr: s(),
    bstp_nmix_prdy_vrss: s(),
    prdy_vrss_sign: s(),
  })
  .passthrough();

export const getProgramTradingSummaryIntradayResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getProgramTradingSummaryIntradayItemSchema).default([]),
  })
  .passthrough();

// ── getProgramTradingSummaryDaily: Program Trading Summary Daily ──

export const getProgramTradingSummaryDailyItemSchema = z
  .object({
    stck_bsop_date: s(),
    nabt_entm_seln_tr_pbmn: s(),
    nabt_onsl_seln_vol: s(),
    whol_onsl_seln_tr_pbmn: s(),
    arbt_smtn_shnu_vol: s(),
    nabt_smtn_shnu_tr_pbmn: s(),
    arbt_entm_ntby_qty: s(),
    nabt_entm_ntby_tr_pbmn: s(),
    arbt_entm_seln_vol: s(),
    nabt_entm_seln_vol_rate: s(),
    nabt_onsl_seln_vol_rate: s(),
    whol_onsl_seln_tr_pbmn_rate: s(),
    arbt_smtm_shun_vol_rate: s(),
    nabt_smtm_shun_tr_pbmn_rate: s(),
    arbt_entm_ntby_qty_rate: s(),
    nabt_entm_ntby_tr_pbmn_rate: s(),
    arbt_entm_seln_vol_rate: s(),
    nabt_entm_seln_tr_pbmn_rate: s(),
    nabt_onsl_seln_tr_pbmn: s(),
    whol_smtn_seln_vol: s(),
    arbt_smtn_shnu_tr_pbmn: s(),
    whol_entm_shnu_vol: s(),
    arbt_entm_ntby_tr_pbmn: s(),
    nabt_onsl_ntby_qty: s(),
    arbt_entm_seln_tr_pbmn: s(),
    nabt_onsl_seln_tr_pbmn_rate: s(),
    whol_seln_vol_rate: s(),
    arbt_smtm_shun_tr_pbmn_rate: s(),
    whol_entm_shnu_vol_rate: s(),
    arbt_entm_ntby_tr_pbmn_rate: s(),
    nabt_onsl_ntby_qty_rate: s(),
    arbt_entm_seln_tr_pbmn_rate: s(),
    nabt_smtn_seln_vol: s(),
    whol_smtn_seln_tr_pbmn: s(),
    nabt_entm_shnu_vol: s(),
    whol_entm_shnu_tr_pbmn: s(),
    arbt_onsl_ntby_qty: s(),
    nabt_onsl_ntby_tr_pbmn: s(),
    arbt_onsl_seln_tr_pbmn: s(),
    nabt_smtm_seln_vol_rate: s(),
    whol_seln_tr_pbmn_rate: s(),
    nabt_entm_shnu_vol_rate: s(),
    whol_entm_shnu_tr_pbmn_rate: s(),
    arbt_onsl_ntby_qty_rate: s(),
    nabt_onsl_ntby_tr_pbmn_rate: s(),
    arbt_onsl_seln_tr_pbmn_rate: s(),
    nabt_smtn_seln_tr_pbmn: s(),
    arbt_entm_shnu_vol: s(),
    nabt_entm_shnu_tr_pbmn: s(),
    whol_onsl_shnu_vol: s(),
    arbt_onsl_ntby_tr_pbmn: s(),
    nabt_smtn_ntby_qty: s(),
    arbt_onsl_seln_vol: s(),
    nabt_smtm_seln_tr_pbmn_rate: s(),
    arbt_entm_shnu_vol_rate: s(),
    nabt_entm_shnu_tr_pbmn_rate: s(),
    whol_onsl_shnu_tr_pbmn: s(),
    arbt_onsl_ntby_tr_pbmn_rate: s(),
    nabt_smtm_ntby_qty_rate: s(),
    arbt_onsl_seln_vol_rate: s(),
    whol_entm_seln_vol: s(),
    arbt_entm_shnu_tr_pbmn: s(),
    nabt_onsl_shnu_vol: s(),
    whol_onsl_shnu_tr_pbmn_rate: s(),
    arbt_smtn_ntby_qty: s(),
    nabt_smtn_ntby_tr_pbmn: s(),
    arbt_smtn_seln_vol: s(),
    whol_entm_seln_tr_pbmn: s(),
    arbt_entm_shnu_tr_pbmn_rate: s(),
    nabt_onsl_shnu_vol_rate: s(),
    whol_onsl_shnu_vol_rate: s(),
    arbt_smtm_ntby_qty_rate: s(),
    nabt_smtm_ntby_tr_pbmn_rate: s(),
    arbt_smtm_seln_vol_rate: s(),
    whol_entm_seln_vol_rate: s(),
    arbt_onsl_shnu_vol: s(),
    nabt_onsl_shnu_tr_pbmn: s(),
    whol_smtn_shnu_vol: s(),
    arbt_smtn_ntby_tr_pbmn: s(),
    whol_entm_ntby_qty: s(),
    arbt_smtn_seln_tr_pbmn: s(),
    whol_entm_seln_tr_pbmn_rate: s(),
    arbt_onsl_shnu_vol_rate: s(),
    nabt_onsl_shnu_tr_pbmn_rate: s(),
    whol_shun_vol_rate: s(),
    arbt_smtm_ntby_tr_pbmn_rate: s(),
    whol_entm_ntby_qty_rate: s(),
    arbt_smtm_seln_tr_pbmn_rate: s(),
    whol_onsl_seln_vol: s(),
    arbt_onsl_shnu_tr_pbmn: s(),
    nabt_smtn_shnu_vol: s(),
    whol_smtn_shnu_tr_pbmn: s(),
    nabt_entm_ntby_qty: s(),
    whol_entm_ntby_tr_pbmn: s(),
    nabt_entm_seln_vol: s(),
    whol_onsl_seln_vol_rate: s(),
    arbt_onsl_shnu_tr_pbmn_rate: s(),
    nabt_smtm_shun_vol_rate: s(),
    whol_shun_tr_pbmn_rate: s(),
    nabt_entm_ntby_qty_rate: s(),
  })
  .passthrough();

export const getProgramTradingSummaryDailyResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getProgramTradingSummaryDailyItemSchema).default([]),
  })
  .passthrough();

// ── getProgramTradingInvestorTrendToday: Program Trading Investor Trend Today ──

export const getProgramTradingInvestorTrendTodayItemSchema = z
  .object({
    invr_cls_code: s(),
    all_seln_qty: s(),
    all_seln_amt: s(),
    invr_cls_name: s(),
    all_shnu_qty: s(),
    all_shnu_amt: s(),
    all_ntby_amt: s(),
    arbt_seln_qty: s(),
    all_ntby_qty: s(),
    arbt_shnu_qty: s(),
    arbt_ntby_qty: s(),
    arbt_seln_amt: s(),
    arbt_shnu_amt: s(),
    arbt_ntby_amt: s(),
    nabt_seln_qty: s(),
    nabt_shnu_qty: s(),
    nabt_ntby_qty: s(),
    nabt_seln_amt: s(),
    nabt_shnu_amt: s(),
    nabt_ntby_amt: s(),
  })
  .passthrough();

export const getProgramTradingInvestorTrendTodayResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: z.array(getProgramTradingInvestorTrendTodayItemSchema).default([]),
  })
  .passthrough();

// ── getCreditBalanceTrendDaily: Credit Balance Trend Daily ──

export const getCreditBalanceTrendDailyItemSchema = z
  .object({
    deal_date: s(),
    stck_prpr: s(),
    prdy_vrss_sign: s(),
    prdy_vrss: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    stlm_date: s(),
    whol_loan_new_stcn: s(),
    whol_loan_rdmp_stcn: s(),
    whol_loan_rmnd_stcn: s(),
    whol_loan_new_amt: s(),
    whol_loan_rdmp_amt: s(),
    whol_loan_rmnd_amt: s(),
    whol_loan_rmnd_rate: s(),
    whol_loan_gvrt: s(),
    whol_stln_new_stcn: s(),
    whol_stln_rdmp_stcn: s(),
    whol_stln_rmnd_stcn: s(),
    whol_stln_new_amt: s(),
    whol_stln_rdmp_amt: s(),
    whol_stln_rmnd_amt: s(),
    whol_stln_rmnd_rate: s(),
    whol_stln_gvrt: s(),
    stck_oprc: s(),
    stck_hgpr: s(),
    stck_lwpr: s(),
  })
  .passthrough();

export const getCreditBalanceTrendDailyResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getCreditBalanceTrendDailyItemSchema).default([]),
  })
  .passthrough();

// ── getExpectedPriceTrend: Expected Price Trend ──

export const getExpectedPriceTrendOutput1ItemSchema = z
  .object({
    rprs_mrkt_kor_name: s(),
    antc_cnpr: s(),
    antc_cntg_vrss_sign: s(),
    antc_cntg_vrss: s(),
    antc_cntg_prdy_ctrt: s(),
    antc_vol: s(),
    antc_tr_pbmn: s(),
  })
  .passthrough();

export const getExpectedPriceTrendOutput2ItemSchema = z
  .object({
    stck_bsop_date: s(),
    stck_cntg_hour: s(),
    stck_prpr: s(),
    prdy_vrss_sign: s(),
    prdy_vrss: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
  })
  .passthrough();

export const getExpectedPriceTrendResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getExpectedPriceTrendOutput1ItemSchema.optional(),
    output2: z.array(getExpectedPriceTrendOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getShortSellingTrendDaily: Short Selling Trend Daily ──

export const getShortSellingTrendDailyOutput1ItemSchema = z
  .object({
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    prdy_vol: s(),
  })
  .passthrough();

export const getShortSellingTrendDailyOutput2ItemSchema = z
  .object({
    stck_bsop_date: s(),
    stck_clpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    stnd_vol_smtn: s(),
    ssts_cntg_qty: s(),
    ssts_vol_rlim: s(),
    acml_ssts_cntg_qty: s(),
    acml_ssts_cntg_qty_rlim: s(),
    acml_tr_pbmn: s(),
    stnd_tr_pbmn_smtn: s(),
    ssts_tr_pbmn: s(),
    ssts_tr_pbmn_rlim: s(),
    acml_ssts_tr_pbmn: s(),
    acml_ssts_tr_pbmn_rlim: s(),
    stck_oprc: s(),
    stck_hgpr: s(),
    stck_lwpr: s(),
    avrg_prc: s(),
  })
  .passthrough();

export const getShortSellingTrendDailyResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getShortSellingTrendDailyOutput1ItemSchema.optional(),
    output2: z.array(getShortSellingTrendDailyOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getAfterHoursExpectedFluctuation: After Hours Expected Fluctuation ──

export const getAfterHoursExpectedFluctuationItemSchema = z
  .object({
    data_rank: s(),
    iscd_stat_cls_code: s(),
    stck_shrn_iscd: s(),
    hts_kor_isnm: s(),
    ovtm_untp_antc_cnpr: s(),
    ovtm_untp_antc_cntg_vrss: s(),
    ovtm_untp_antc_cntg_vrss_sign: s(),
    ovtm_untp_antc_cntg_ctrt: s(),
    ovtm_untp_askp_rsqn1: s(),
    ovtm_untp_bidp_rsqn1: s(),
    ovtm_untp_antc_cnqn: s(),
    itmt_vol: s(),
    stck_prpr: s(),
  })
  .passthrough();

export const getAfterHoursExpectedFluctuationResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getAfterHoursExpectedFluctuationItemSchema).default([]),
  })
  .passthrough();

// ── getTradingWeightByAmount: Trading Weight By Amount ──

export const getTradingWeightByAmountItemSchema = z
  .object({
    prpr_name: s(),
    smtn_avrg_prpr: s(),
    acml_vol: s(),
    whol_ntby_qty_rate: s(),
    ntby_cntg_csnu: s(),
    seln_cnqn_smtn: s(),
    whol_seln_vol_rate: s(),
    seln_cntg_csnu: s(),
    shnu_cnqn_smtn: s(),
    whol_shun_vol_rate: s(),
    shnu_cntg_csnu: s(),
  })
  .passthrough();

export const getTradingWeightByAmountResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getTradingWeightByAmountItemSchema).default([]),
  })
  .passthrough();

// ── getMarketFundSummary: Market Fund Summary ──

export const getMarketFundSummaryItemSchema = z
  .object({
    bsop_date: s(),
    bstp_nmix_prpr: s(),
    bstp_nmix_prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    hts_avls: s(),
    cust_dpmn_amt: s(),
    cust_dpmn_amt_prdy_vrss: s(),
    amt_tnrt: s(),
    uncl_amt: s(),
    crdt_loan_rmnd: s(),
    futs_tfam_amt: s(),
    sttp_amt: s(),
    mxtp_amt: s(),
    bntp_amt: s(),
    mmf_amt: s(),
    secu_lend_amt: s(),
  })
  .passthrough();

export const getMarketFundSummaryResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getMarketFundSummaryItemSchema).default([]),
  })
  .passthrough();

// ── getStockLoanTrendDaily: Stock Loan Trend Daily ──

export const getStockLoanTrendDailyItemSchema = z
  .object({
    bsop_date: s(),
    stck_prpr: s(),
    prdy_vrss_sign: s(),
    prdy_vrss: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    new_stcn: s(),
    rdmp_stcn: s(),
    prdy_rmnd_vrss: s(),
    rmnd_stcn: s(),
    rmnd_amt: s(),
  })
  .passthrough();

export const getStockLoanTrendDailyResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: z.array(getStockLoanTrendDailyItemSchema).default([]),
  })
  .passthrough();

// ── getLimitPriceStocks: Limit Price Stocks ──

export const getLimitPriceStocksItemSchema = z
  .object({
    mksc_shrn_iscd: s(),
    hts_kor_isnm: s(),
    stck_prpr: s(),
    prdy_vrss_sign: s(),
    prdy_vrss: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    total_askp_rsqn: s(),
    total_bidp_rsqn: s(),
    askp_rsqn1: s(),
    bidp_rsqn1: s(),
    prdy_vol: s(),
    seln_cnqn: s(),
    shnu_cnqn: s(),
    stck_llam: s(),
    stck_mxpr: s(),
    prdy_vrss_vol_rate: s(),
  })
  .passthrough();

export const getLimitPriceStocksResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getLimitPriceStocksItemSchema).default([]),
  })
  .passthrough();

// ── getResistanceLevelTradingWeight: Resistance Level Trading Weight ──

export const getResistanceLevelTradingWeightOutput1ItemSchema = z
  .object({
    rprs_mrkt_kor_name: s(),
    stck_shrn_iscd: s(),
    hts_kor_isnm: s(),
    stck_prpr: s(),
    prdy_vrss_sign: s(),
    prdy_vrss: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    prdy_vol: s(),
    wghn_avrg_stck_prc: s(),
    lstn_stcn: s(),
  })
  .passthrough();

export const getResistanceLevelTradingWeightOutput2ItemSchema = z
  .object({
    data_rank: s(),
    stck_prpr: s(),
    cntg_vol: s(),
    acml_vol_rlim: s(),
  })
  .passthrough();

export const getResistanceLevelTradingWeightResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getResistanceLevelTradingWeightOutput1ItemSchema.optional(),
    output2: z.array(getResistanceLevelTradingWeightOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── Response Types ──

export type GetConditionSearchListResponse = CamelizeKeys<z.infer<typeof getConditionSearchListResponseSchema>>;

export type GetConditionSearchResultResponse = CamelizeKeys<z.infer<typeof getConditionSearchResultResponseSchema>>;

export type GetWatchlistGroupsResponse = CamelizeKeys<z.infer<typeof getWatchlistGroupsResponseSchema>>;

export type GetWatchlistMultiQuoteResponse = CamelizeKeys<z.infer<typeof getWatchlistMultiQuoteResponseSchema>>;

export type GetWatchlistStocksByGroupResponse = CamelizeKeys<z.infer<typeof getWatchlistStocksByGroupResponseSchema>>;

export type GetInstitutionalForeignTradingAggregateResponse = CamelizeKeys<
  z.infer<typeof getInstitutionalForeignTradingAggregateResponseSchema>
>;

export type GetForeignBrokerageTradingAggregateResponse = CamelizeKeys<
  z.infer<typeof getForeignBrokerageTradingAggregateResponseSchema>
>;

export type GetInvestorTradingTrendByStockDailyResponse = CamelizeKeys<
  z.infer<typeof getInvestorTradingTrendByStockDailyResponseSchema>
>;

export type GetInvestorTradingTrendByMarketIntradayResponse = CamelizeKeys<
  z.infer<typeof getInvestorTradingTrendByMarketIntradayResponseSchema>
>;

export type GetInvestorTradingTrendByMarketDailyResponse = CamelizeKeys<
  z.infer<typeof getInvestorTradingTrendByMarketDailyResponseSchema>
>;

export type GetForeignNetBuyTrendByStockResponse = CamelizeKeys<
  z.infer<typeof getForeignNetBuyTrendByStockResponseSchema>
>;

export type GetMemberTradingTrendTickResponse = CamelizeKeys<z.infer<typeof getMemberTradingTrendTickResponseSchema>>;

export type GetMemberTradingTrendByStockResponse = CamelizeKeys<
  z.infer<typeof getMemberTradingTrendByStockResponseSchema>
>;

export type GetProgramTradingTrendByStockIntradayResponse = CamelizeKeys<
  z.infer<typeof getProgramTradingTrendByStockIntradayResponseSchema>
>;

export type GetProgramTradingTrendByStockDailyResponse = CamelizeKeys<
  z.infer<typeof getProgramTradingTrendByStockDailyResponseSchema>
>;

export type GetForeignInstitutionalEstimateByStockResponse = CamelizeKeys<
  z.infer<typeof getForeignInstitutionalEstimateByStockResponseSchema>
>;

export type GetBuySellVolumeByStockDailyResponse = CamelizeKeys<
  z.infer<typeof getBuySellVolumeByStockDailyResponseSchema>
>;

export type GetProgramTradingSummaryIntradayResponse = CamelizeKeys<
  z.infer<typeof getProgramTradingSummaryIntradayResponseSchema>
>;

export type GetProgramTradingSummaryDailyResponse = CamelizeKeys<
  z.infer<typeof getProgramTradingSummaryDailyResponseSchema>
>;

export type GetProgramTradingInvestorTrendTodayResponse = CamelizeKeys<
  z.infer<typeof getProgramTradingInvestorTrendTodayResponseSchema>
>;

export type GetCreditBalanceTrendDailyResponse = CamelizeKeys<z.infer<typeof getCreditBalanceTrendDailyResponseSchema>>;

export type GetExpectedPriceTrendResponse = CamelizeKeys<z.infer<typeof getExpectedPriceTrendResponseSchema>>;

export type GetShortSellingTrendDailyResponse = CamelizeKeys<z.infer<typeof getShortSellingTrendDailyResponseSchema>>;

export type GetAfterHoursExpectedFluctuationResponse = CamelizeKeys<
  z.infer<typeof getAfterHoursExpectedFluctuationResponseSchema>
>;

export type GetTradingWeightByAmountResponse = CamelizeKeys<z.infer<typeof getTradingWeightByAmountResponseSchema>>;

export type GetMarketFundSummaryResponse = CamelizeKeys<z.infer<typeof getMarketFundSummaryResponseSchema>>;

export type GetStockLoanTrendDailyResponse = CamelizeKeys<z.infer<typeof getStockLoanTrendDailyResponseSchema>>;

export type GetLimitPriceStocksResponse = CamelizeKeys<z.infer<typeof getLimitPriceStocksResponseSchema>>;

export type GetResistanceLevelTradingWeightResponse = CamelizeKeys<
  z.infer<typeof getResistanceLevelTradingWeightResponseSchema>
>;

// ── Response Map ──

export interface DomesticMarketAnalysisResponseMap {
  getConditionSearchList: GetConditionSearchListResponse;
  getConditionSearchResult: GetConditionSearchResultResponse;
  getWatchlistGroups: GetWatchlistGroupsResponse;
  getWatchlistMultiQuote: GetWatchlistMultiQuoteResponse;
  getWatchlistStocksByGroup: GetWatchlistStocksByGroupResponse;
  getInstitutionalForeignTradingAggregate: GetInstitutionalForeignTradingAggregateResponse;
  getForeignBrokerageTradingAggregate: GetForeignBrokerageTradingAggregateResponse;
  getInvestorTradingTrendByStockDaily: GetInvestorTradingTrendByStockDailyResponse;
  getInvestorTradingTrendByMarketIntraday: GetInvestorTradingTrendByMarketIntradayResponse;
  getInvestorTradingTrendByMarketDaily: GetInvestorTradingTrendByMarketDailyResponse;
  getForeignNetBuyTrendByStock: GetForeignNetBuyTrendByStockResponse;
  getMemberTradingTrendTick: GetMemberTradingTrendTickResponse;
  getMemberTradingTrendByStock: GetMemberTradingTrendByStockResponse;
  getProgramTradingTrendByStockIntraday: GetProgramTradingTrendByStockIntradayResponse;
  getProgramTradingTrendByStockDaily: GetProgramTradingTrendByStockDailyResponse;
  getForeignInstitutionalEstimateByStock: GetForeignInstitutionalEstimateByStockResponse;
  getBuySellVolumeByStockDaily: GetBuySellVolumeByStockDailyResponse;
  getProgramTradingSummaryIntraday: GetProgramTradingSummaryIntradayResponse;
  getProgramTradingSummaryDaily: GetProgramTradingSummaryDailyResponse;
  getProgramTradingInvestorTrendToday: GetProgramTradingInvestorTrendTodayResponse;
  getCreditBalanceTrendDaily: GetCreditBalanceTrendDailyResponse;
  getExpectedPriceTrend: GetExpectedPriceTrendResponse;
  getShortSellingTrendDaily: GetShortSellingTrendDailyResponse;
  getAfterHoursExpectedFluctuation: GetAfterHoursExpectedFluctuationResponse;
  getTradingWeightByAmount: GetTradingWeightByAmountResponse;
  getMarketFundSummary: GetMarketFundSummaryResponse;
  getStockLoanTrendDaily: GetStockLoanTrendDailyResponse;
  getLimitPriceStocks: GetLimitPriceStocksResponse;
  getResistanceLevelTradingWeight: GetResistanceLevelTradingWeightResponse;
}
