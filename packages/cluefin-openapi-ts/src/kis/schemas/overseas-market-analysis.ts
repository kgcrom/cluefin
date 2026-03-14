import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types';

const s = () => z.string().default('');

const kisEnvelope = {
  rt_cd: z.string().optional(),
  msg_cd: z.string().optional(),
  msg1: z.string().optional(),
};

// ── getStockPriceFluctuation: Stock Price Fluctuation ──

export const getStockPriceFluctuationOutput1ItemSchema = z
  .object({
    zdiv: s(),
    stat: s(),
    nrec: s(),
  })
  .passthrough();

export const getStockPriceFluctuationOutput2ItemSchema = z
  .object({
    rsym: s(),
    excd: s(),
    symb: s(),
    knam: s(),
    last: s(),
    sign: s(),
    diff: s(),
    rate: s(),
    tvol: s(),
    pask: s(),
    pbid: s(),
    n_base: s(),
    n_diff: s(),
    n_rate: s(),
    enam: s(),
    e_ordyn: s(),
  })
  .passthrough();

export const getStockPriceFluctuationResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getStockPriceFluctuationOutput1ItemSchema.optional(),
    output2: z.array(getStockPriceFluctuationOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getStockVolumeSurge: Stock Volume Surge ──

export const getStockVolumeSurgeOutput1ItemSchema = z
  .object({
    zdiv: s(),
    stat: s(),
    nrec: s(),
  })
  .passthrough();

export const getStockVolumeSurgeOutput2ItemSchema = z
  .object({
    rsym: s(),
    excd: s(),
    symb: s(),
    knam: s(),
    last: s(),
    sign: s(),
    diff: s(),
    rate: s(),
    tvol: s(),
    pask: s(),
    pbid: s(),
    n_tvol: s(),
    n_diff: s(),
    n_rate: s(),
    enam: s(),
    e_ordyn: s(),
  })
  .passthrough();

export const getStockVolumeSurgeResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getStockVolumeSurgeOutput1ItemSchema.optional(),
    output2: z.array(getStockVolumeSurgeOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getStockBuyExecutionStrengthTop: Stock Buy Execution Strength Top ──

export const getStockBuyExecutionStrengthTopOutput1ItemSchema = z
  .object({
    zdiv: s(),
    stat: s(),
    nrec: s(),
  })
  .passthrough();

export const getStockBuyExecutionStrengthTopOutput2ItemSchema = z
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
    pask: s(),
    pbid: s(),
    tpow: s(),
    powx: s(),
    ename: s(),
    e_ordyn: s(),
  })
  .passthrough();

export const getStockBuyExecutionStrengthTopResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getStockBuyExecutionStrengthTopOutput1ItemSchema.optional(),
    output2: z.array(getStockBuyExecutionStrengthTopOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getStockRiseDeclineRate: Stock Rise Decline Rate ──

export const getStockRiseDeclineRateOutput1ItemSchema = z
  .object({
    zdiv: s(),
    stat: s(),
    crec: s(),
    trec: s(),
    nrec: s(),
  })
  .passthrough();

export const getStockRiseDeclineRateOutput2ItemSchema = z
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
    pask: s(),
    pbid: s(),
    n_base: s(),
    n_diff: s(),
    n_rate: s(),
    rank: s(),
    ename: s(),
    e_ordyn: s(),
  })
  .passthrough();

export const getStockRiseDeclineRateResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getStockRiseDeclineRateOutput1ItemSchema.optional(),
    output2: z.array(getStockRiseDeclineRateOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getStockNewHighLowPrice: Stock New High Low Price ──

export const getStockNewHighLowPriceOutput1ItemSchema = z
  .object({
    zdiv: s(),
    stat: s(),
    nrec: s(),
  })
  .passthrough();

export const getStockNewHighLowPriceOutput2ItemSchema = z
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
    pask: s(),
    pbid: s(),
    n_base: s(),
    n_diff: s(),
    n_rate: s(),
    ename: s(),
    e_ordyn: s(),
  })
  .passthrough();

export const getStockNewHighLowPriceResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getStockNewHighLowPriceOutput1ItemSchema.optional(),
    output2: z.array(getStockNewHighLowPriceOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getStockTradingVolumeRank: Stock Trading Volume Rank ──

export const getStockTradingVolumeRankOutput1ItemSchema = z
  .object({
    zdiv: s(),
    stat: s(),
    crec: s(),
    trec: s(),
    nrec: s(),
  })
  .passthrough();

export const getStockTradingVolumeRankOutput2ItemSchema = z
  .object({
    rsym: s(),
    excd: s(),
    symb: s(),
    name: s(),
    last: s(),
    sign: s(),
    diff: s(),
    rate: s(),
    pask: s(),
    pbid: s(),
    tvol: s(),
    tamt: s(),
    a_tvol: s(),
    rank: s(),
    ename: s(),
    e_ordyn: s(),
  })
  .passthrough();

export const getStockTradingVolumeRankResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getStockTradingVolumeRankOutput1ItemSchema.optional(),
    output2: z.array(getStockTradingVolumeRankOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getStockTradingAmountRank: Stock Trading Amount Rank ──

export const getStockTradingAmountRankOutput1ItemSchema = z
  .object({
    zdiv: s(),
    stat: s(),
    crec: s(),
    trec: s(),
    nrec: s(),
  })
  .passthrough();

export const getStockTradingAmountRankOutput2ItemSchema = z
  .object({
    rsym: s(),
    excd: s(),
    symb: s(),
    name: s(),
    last: s(),
    sign: s(),
    diff: s(),
    rate: s(),
    pask: s(),
    pbid: s(),
    tvol: s(),
    tamt: s(),
    a_tamt: s(),
    rank: s(),
    ename: s(),
    e_ordyn: s(),
  })
  .passthrough();

export const getStockTradingAmountRankResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getStockTradingAmountRankOutput1ItemSchema.optional(),
    output2: z.array(getStockTradingAmountRankOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getStockTradingIncreaseRateRank: Stock Trading Increase Rate Rank ──

export const getStockTradingIncreaseRateRankOutput1ItemSchema = z
  .object({
    zdiv: s(),
    stat: s(),
    crec: s(),
    trec: s(),
    nrec: s(),
  })
  .passthrough();

export const getStockTradingIncreaseRateRankOutput2ItemSchema = z
  .object({
    rsym: s(),
    excd: s(),
    symb: s(),
    name: s(),
    last: s(),
    sign: s(),
    diff: s(),
    rate: s(),
    pask: s(),
    pbid: s(),
    tvol: s(),
    n_tvol: s(),
    n_rate: s(),
    rank: s(),
    ename: s(),
    e_ordyn: s(),
  })
  .passthrough();

export const getStockTradingIncreaseRateRankResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getStockTradingIncreaseRateRankOutput1ItemSchema.optional(),
    output2: z.array(getStockTradingIncreaseRateRankOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getStockTradingTurnoverRateRank: Stock Trading Turnover Rate Rank ──

export const getStockTradingTurnoverRateRankOutput1ItemSchema = z
  .object({
    zdiv: s(),
    stat: s(),
    crec: s(),
    trec: s(),
    nrec: s(),
  })
  .passthrough();

export const getStockTradingTurnoverRateRankOutput2ItemSchema = z
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
    pask: s(),
    pbid: s(),
    shar: s(),
    tover: s(),
    rank: s(),
    ename: s(),
    e_ordyn: s(),
  })
  .passthrough();

export const getStockTradingTurnoverRateRankResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getStockTradingTurnoverRateRankOutput1ItemSchema.optional(),
    output2: z.array(getStockTradingTurnoverRateRankOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getStockMarketCapRank: Stock Market Cap Rank ──

export const getStockMarketCapRankOutput1ItemSchema = z
  .object({
    zdiv: s(),
    stat: s(),
    crec: s(),
    trec: s(),
    nrec: s(),
  })
  .passthrough();

export const getStockMarketCapRankOutput2ItemSchema = z
  .object({
    rsym: s(),
    excd: s(),
    symb: s(),
    name: s(),
    last: s(),
    last_org: s(),
    sign: s(),
    diff: s(),
    diff_org: s(),
    rate: s(),
    tvol: s(),
    shar: s(),
    tomv: s(),
    tomv_org: s(),
    grav: s(),
    rank: s(),
    ename: s(),
    e_ordyn: s(),
  })
  .passthrough();

export const getStockMarketCapRankResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getStockMarketCapRankOutput1ItemSchema.optional(),
    output2: z.array(getStockMarketCapRankOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getStockPeriodRightsInquiry: Stock Period Rights Inquiry ──

export const getStockPeriodRightsInquiryItemSchema = z
  .object({
    bass_dt: s(),
    rght_type_cd: s(),
    pdno: s(),
    prdt_name: s(),
    prdt_type_cd: s(),
    std_pdno: s(),
    acpl_bass_dt: s(),
    sbsc_strt_dt: s(),
    sbsc_end_dt: s(),
    cash_alct_rt: s(),
    stck_alct_rt: s(),
    crcy_cd: s(),
    crcy_cd2: s(),
    crcy_cd3: s(),
    crcy_cd4: s(),
    alct_frcr_unpr: s(),
    stkp_dvdn_frcr_amt2: s(),
    stkp_dvdn_frcr_amt3: s(),
    stkp_dvdn_frcr_amt4: s(),
    dfnt_yn: s(),
  })
  .passthrough();

export const getStockPeriodRightsInquiryResponseSchema = z
  .object({
    ...kisEnvelope,
    ctx_area_fk50: s(),
    ctx_area_nk50: s(),
    output: z.array(getStockPeriodRightsInquiryItemSchema).default([]),
  })
  .passthrough();

// ── getNewsAggregateTitle: News Aggregate Title ──

export const getNewsAggregateTitleResponseSchema = z
  .object({
    ...kisEnvelope,
    outblock1: s(),
  })
  .passthrough();

// ── getStockRightsAggregate: Stock Rights Aggregate ──

export const getStockRightsAggregateItemSchema = z
  .object({
    anno_dt: s(),
    ca_title: s(),
    div_lock_dt: s(),
    pay_dt: s(),
    record_dt: s(),
    validity_dt: s(),
    local_end_dt: s(),
    lock_dt: s(),
    delist_dt: s(),
    redempt_dt: s(),
    early_redempt_dt: s(),
    effective_dt: s(),
  })
  .passthrough();

export const getStockRightsAggregateResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: z.array(getStockRightsAggregateItemSchema).default([]),
  })
  .passthrough();

// ── getStockCollateralLoanEligible: Stock Collateral Loan Eligible ──

export const getStockCollateralLoanEligibleOutput1ItemSchema = z
  .object({
    pdno: s(),
    ovrs_item_name: s(),
    loan_rt: s(),
    mgge_mntn_rt: s(),
    mgge_ensu_rt: s(),
    loan_exec_psbl_yn: s(),
    stff_name: s(),
    erlm_dt: s(),
    tr_mket_name: s(),
    crcy_cd: s(),
    natn_kor_name: s(),
    ovrs_excg_cd: s(),
  })
  .passthrough();

export const getStockCollateralLoanEligibleOutput2ItemSchema = z
  .object({
    loan_psbl_item_num: s(),
  })
  .passthrough();

export const getStockCollateralLoanEligibleResponseSchema = z
  .object({
    ...kisEnvelope,
    ctx_area_fk100: s(),
    ctx_area_nk100: s(),
    output1: z.array(getStockCollateralLoanEligibleOutput1ItemSchema).default([]),
    output2: getStockCollateralLoanEligibleOutput2ItemSchema.optional(),
  })
  .passthrough();

// ── getBreakingNewsTitle: Breaking News Title ──

export const getBreakingNewsTitleItemSchema = z
  .object({
    cntt_usiq_srno: s(),
    news_ofer_entp_code: s(),
    data_dt: s(),
    data_tm: s(),
    hts_pbnt_titl_cntt: s(),
    news_lrdv_code: s(),
    dorg: s(),
    iscd1: s(),
    iscd2: s(),
    iscd3: s(),
    iscd4: s(),
    iscd5: s(),
    iscd6: s(),
    iscd7: s(),
    iscd8: s(),
    iscd9: s(),
    iscd10: s(),
    kor_isnm1: s(),
    kor_isnm2: s(),
    kor_isnm3: s(),
    kor_isnm4: s(),
    kor_isnm5: s(),
    kor_isnm6: s(),
    kor_isnm7: s(),
    kor_isnm8: s(),
    kor_isnm9: s(),
    kor_isnm10: s(),
  })
  .passthrough();

export const getBreakingNewsTitleResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getBreakingNewsTitleItemSchema).default([]),
  })
  .passthrough();

// ── Response Types ──

export type GetStockPriceFluctuationResponse = CamelizeKeys<z.infer<typeof getStockPriceFluctuationResponseSchema>>;

export type GetStockVolumeSurgeResponse = CamelizeKeys<z.infer<typeof getStockVolumeSurgeResponseSchema>>;

export type GetStockBuyExecutionStrengthTopResponse = CamelizeKeys<
  z.infer<typeof getStockBuyExecutionStrengthTopResponseSchema>
>;

export type GetStockRiseDeclineRateResponse = CamelizeKeys<z.infer<typeof getStockRiseDeclineRateResponseSchema>>;

export type GetStockNewHighLowPriceResponse = CamelizeKeys<z.infer<typeof getStockNewHighLowPriceResponseSchema>>;

export type GetStockTradingVolumeRankResponse = CamelizeKeys<z.infer<typeof getStockTradingVolumeRankResponseSchema>>;

export type GetStockTradingAmountRankResponse = CamelizeKeys<z.infer<typeof getStockTradingAmountRankResponseSchema>>;

export type GetStockTradingIncreaseRateRankResponse = CamelizeKeys<
  z.infer<typeof getStockTradingIncreaseRateRankResponseSchema>
>;

export type GetStockTradingTurnoverRateRankResponse = CamelizeKeys<
  z.infer<typeof getStockTradingTurnoverRateRankResponseSchema>
>;

export type GetStockMarketCapRankResponse = CamelizeKeys<z.infer<typeof getStockMarketCapRankResponseSchema>>;

export type GetStockPeriodRightsInquiryResponse = CamelizeKeys<
  z.infer<typeof getStockPeriodRightsInquiryResponseSchema>
>;

export type GetNewsAggregateTitleResponse = CamelizeKeys<z.infer<typeof getNewsAggregateTitleResponseSchema>>;

export type GetStockRightsAggregateResponse = CamelizeKeys<z.infer<typeof getStockRightsAggregateResponseSchema>>;

export type GetStockCollateralLoanEligibleResponse = CamelizeKeys<
  z.infer<typeof getStockCollateralLoanEligibleResponseSchema>
>;

export type GetBreakingNewsTitleResponse = CamelizeKeys<z.infer<typeof getBreakingNewsTitleResponseSchema>>;

// ── Response Map ──

export interface OverseasMarketAnalysisResponseMap {
  getStockPriceFluctuation: GetStockPriceFluctuationResponse;
  getStockVolumeSurge: GetStockVolumeSurgeResponse;
  getStockBuyExecutionStrengthTop: GetStockBuyExecutionStrengthTopResponse;
  getStockRiseDeclineRate: GetStockRiseDeclineRateResponse;
  getStockNewHighLowPrice: GetStockNewHighLowPriceResponse;
  getStockTradingVolumeRank: GetStockTradingVolumeRankResponse;
  getStockTradingAmountRank: GetStockTradingAmountRankResponse;
  getStockTradingIncreaseRateRank: GetStockTradingIncreaseRateRankResponse;
  getStockTradingTurnoverRateRank: GetStockTradingTurnoverRateRankResponse;
  getStockMarketCapRank: GetStockMarketCapRankResponse;
  getStockPeriodRightsInquiry: GetStockPeriodRightsInquiryResponse;
  getNewsAggregateTitle: GetNewsAggregateTitleResponse;
  getStockRightsAggregate: GetStockRightsAggregateResponse;
  getStockCollateralLoanEligible: GetStockCollateralLoanEligibleResponse;
  getBreakingNewsTitle: GetBreakingNewsTitleResponse;
}
