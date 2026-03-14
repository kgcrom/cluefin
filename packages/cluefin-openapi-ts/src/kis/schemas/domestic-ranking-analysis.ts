import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types';

const s = () => z.string().default('');

const kisEnvelope = {
  rt_cd: z.string().optional(),
  msg_cd: z.string().optional(),
  msg1: z.string().optional(),
};

// ── getTradingVolumeRank: Trading Volume Rank ──

export const getTradingVolumeRankItemSchema = z
  .object({
    hts_kor_isnm: s(),
    mksc_shrn_iscd: s(),
    data_rank: s(),
    stck_prpr: s(),
    prdy_vrss_sign: s(),
    prdy_vrss: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    prdy_vol: s(),
    lstn_stcn: s(),
    avrg_vol: s(),
    n_befr_clpr_vrss_prpr_rate: s(),
    vol_inrt: s(),
    vol_tnrt: s(),
    nday_vol_tnrt: s(),
    avrg_tr_pbmn: s(),
    tr_pbmn_tnrt: s(),
    nday_tr_pbmn_tnrt: s(),
    acml_tr_pbmn: s(),
  })
  .passthrough();

export const getTradingVolumeRankResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getTradingVolumeRankItemSchema).default([]),
  })
  .passthrough();

// ── getStockFluctuationRank: Stock Fluctuation Rank ──

export const getStockFluctuationRankItemSchema = z
  .object({
    stck_shrn_iscd: s(),
    data_rank: s(),
    hts_kor_isnm: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    stck_hgpr: s(),
    hgpr_hour: s(),
    acml_hgpr_date: s(),
    stck_lwpr: s(),
    lwpr_hour: s(),
    acml_lwpr_date: s(),
    lwpr_vrss_prpr_rate: s(),
    dsgt_date_clpr_vrss_prpr_rate: s(),
    cnnt_ascn_dynu: s(),
    hgpr_vrss_prpr_rate: s(),
    cnnt_down_dynu: s(),
    oprc_vrss_prpr_sign: s(),
    oprc_vrss_prpr: s(),
    oprc_vrss_prpr_rate: s(),
    prd_rsfl: s(),
    prd_rsfl_rate: s(),
  })
  .passthrough();

export const getStockFluctuationRankResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getStockFluctuationRankItemSchema).default([]),
  })
  .passthrough();

// ── getStockHogaQuantityRank: Stock Hoga Quantity Rank ──

export const getStockHogaQuantityRankItemSchema = z
  .object({
    mksc_shrn_iscd: s(),
    data_rank: s(),
    hts_kor_isnm: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    total_askp_rsqn: s(),
    total_bidp_rsqn: s(),
    total_ntsl_bidp_rsqn: s(),
    shnu_rsqn_rate: s(),
    seln_rsqn_rate: s(),
  })
  .passthrough();

export const getStockHogaQuantityRankResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getStockHogaQuantityRankItemSchema).default([]),
  })
  .passthrough();

// ── getStockProfitabilityIndicatorRank: Stock Profitability Indicator Rank ──

export const getStockProfitabilityIndicatorRankItemSchema = z
  .object({
    data_rank: s(),
    hts_kor_isnm: s(),
    prdy_vrss_sign: s(),
    mksc_shrn_iscd: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    sale_totl_prfi: s(),
    bsop_prti: s(),
    op_prfi: s(),
    thtr_ntin: s(),
    total_aset: s(),
    total_lblt: s(),
    total_cptl: s(),
    stac_month: s(),
    stac_month_cls_code: s(),
    iqry_csnu: s(),
  })
  .passthrough();

export const getStockProfitabilityIndicatorRankResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getStockProfitabilityIndicatorRankItemSchema).default([]),
  })
  .passthrough();

// ── getStockMarketCapTop: Stock Market Cap Top ──

export const getStockMarketCapTopItemSchema = z
  .object({
    mksc_shrn_iscd: s(),
    data_rank: s(),
    hts_kor_isnm: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    lstn_stcn: s(),
    stck_avls: s(),
    mrkt_whol_avls_rlim: s(),
  })
  .passthrough();

export const getStockMarketCapTopResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getStockMarketCapTopItemSchema).default([]),
  })
  .passthrough();

// ── getStockFinanceRatioRank: Stock Finance Ratio Rank ──

export const getStockFinanceRatioRankItemSchema = z
  .object({
    data_rank: s(),
    hts_kor_isnm: s(),
    mksc_shrn_iscd: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    cptl_op_prfi: s(),
    cptl_ntin_rate: s(),
    sale_totl_rate: s(),
    sale_ntin_rate: s(),
    bis: s(),
    lblt_rate: s(),
    bram_depn: s(),
    rsrv_rate: s(),
    grs: s(),
    op_prfi_inrt: s(),
    bsop_prfi_inrt: s(),
    ntin_inrt: s(),
    equt_inrt: s(),
    cptl_tnrt: s(),
    sale_bond_tnrt: s(),
    totl_aset_inrt: s(),
    stac_month: s(),
    stac_month_cls_code: s(),
    iqry_csnu: s(),
  })
  .passthrough();

export const getStockFinanceRatioRankResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getStockFinanceRatioRankItemSchema).default([]),
  })
  .passthrough();

// ── getStockTimeHogaRank: Stock Time Hoga Rank ──

export const getStockTimeHogaRankItemSchema = z
  .object({
    stck_shrn_iscd: s(),
    data_rank: s(),
    hts_kor_isnm: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    ovtm_total_askp_rsqn: s(),
    ovtm_total_bidp_rsqn: s(),
    mkob_otcp_vol: s(),
    mkfa_otcp_vol: s(),
  })
  .passthrough();

export const getStockTimeHogaRankResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getStockTimeHogaRankItemSchema).default([]),
  })
  .passthrough();

// ── getStockPreferredStockRatioTop: Stock Preferred Stock Ratio Top ──

export const getStockPreferredStockRatioTopItemSchema = z
  .object({
    mksc_shrn_iscd: s(),
    data_rank: s(),
    hts_kor_isnm: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    acml_vol: s(),
    prst_iscd: s(),
    prst_kor_isnm: s(),
    prst_prpr: s(),
    prst_prdy_vrss: s(),
    prst_prdy_vrss_sign: s(),
    prst_acml_vol: s(),
    diff_prpr: s(),
    dprt: s(),
    prdy_ctrt: s(),
    prst_prdy_ctrt: s(),
  })
  .passthrough();

export const getStockPreferredStockRatioTopResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getStockPreferredStockRatioTopItemSchema).default([]),
  })
  .passthrough();

// ── getStockDisparityIndexRank: Stock Disparity Index Rank ──

export const getStockDisparityIndexRankItemSchema = z
  .object({
    mksc_shrn_iscd: s(),
    data_rank: s(),
    hts_kor_isnm: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_ctrt: s(),
    prdy_vrss_sign: s(),
    acml_vol: s(),
    d5_dsrt: s(),
    d10_dsrt: s(),
    d20_dsrt: s(),
    d60_dsrt: s(),
    d120_dsrt: s(),
  })
  .passthrough();

export const getStockDisparityIndexRankResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getStockDisparityIndexRankItemSchema).default([]),
  })
  .passthrough();

// ── getStockMarketPriceRank: Stock Market Price Rank ──

export const getStockMarketPriceRankItemSchema = z
  .object({
    data_rank: s(),
    hts_kor_isnm: s(),
    mksc_shrn_iscd: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    per: s(),
    pbr: s(),
    pcr: s(),
    psr: s(),
    eps: s(),
    eva: s(),
    ebitda: s(),
    pv_div_ebitda: s(),
    ebitda_div_fnnc_expn: s(),
    stac_month: s(),
    stac_month_cls_code: s(),
    iqry_csnu: s(),
  })
  .passthrough();

export const getStockMarketPriceRankResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getStockMarketPriceRankItemSchema).default([]),
  })
  .passthrough();

// ── getStockExecutionStrengthTop: Stock Execution Strength Top ──

export const getStockExecutionStrengthTopItemSchema = z
  .object({
    stck_shrn_iscd: s(),
    data_rank: s(),
    hts_kor_isnm: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    tday_rltv: s(),
    seln_cnqn_smtn: s(),
    shnu_cnqn_smtn: s(),
  })
  .passthrough();

export const getStockExecutionStrengthTopResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getStockExecutionStrengthTopItemSchema).default([]),
  })
  .passthrough();

// ── getStockWatchlistRegistrationTop: Stock Watchlist Registration Top ──

export const getStockWatchlistRegistrationTopItemSchema = z
  .object({
    mrkt_div_cls_name: s(),
    mksc_shrn_iscd: s(),
    hts_kor_isnm: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    acml_tr_pbmn: s(),
    askp: s(),
    bidp: s(),
    data_rank: s(),
    inter_issu_reg_csnu: s(),
  })
  .passthrough();

export const getStockWatchlistRegistrationTopResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getStockWatchlistRegistrationTopItemSchema).default([]),
  })
  .passthrough();

// ── getStockExpectedExecutionRiseDeclineTop: Stock Expected Execution Rise Decline Top ──

export const getStockExpectedExecutionRiseDeclineTopItemSchema = z
  .object({
    stck_shrn_iscd: s(),
    hts_kor_isnm: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    stck_sdpr: s(),
    seln_rsqn: s(),
    askp: s(),
    bidp: s(),
    shnu_rsqn: s(),
    cntg_vol: s(),
    antc_tr_pbmn: s(),
    total_askp_rsqn: s(),
    total_bidp_rsqn: s(),
  })
  .passthrough();

export const getStockExpectedExecutionRiseDeclineTopResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getStockExpectedExecutionRiseDeclineTopItemSchema).default([]),
  })
  .passthrough();

// ── getStockProprietaryTradingTop: Stock Proprietary Trading Top ──

export const getStockProprietaryTradingTopItemSchema = z
  .object({
    data_rank: s(),
    mksc_shrn_iscd: s(),
    hts_kor_isnm: s(),
    stck_prpr: s(),
    prdy_vrss_sign: s(),
    prdy_vrss: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    acml_tr_pbmn: s(),
    seln_cnqn_smtn: s(),
    shnu_cnqn_smtn: s(),
    ntby_cnqn: s(),
  })
  .passthrough();

export const getStockProprietaryTradingTopResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getStockProprietaryTradingTopItemSchema).default([]),
  })
  .passthrough();

// ── getStockNewHighLowApproachingTop: Stock New High Low Approaching Top ──

export const getStockNewHighLowApproachingTopItemSchema = z
  .object({
    hts_kor_isnm: s(),
    mksc_shrn_iscd: s(),
    stck_prpr: s(),
    prdy_vrss_sign: s(),
    prdy_vrss: s(),
    prdy_ctrt: s(),
    askp: s(),
    askp_rsqn1: s(),
    bidp: s(),
    bidp_rsqn1: s(),
    acml_vol: s(),
    new_hgpr: s(),
    hprc_near_rate: s(),
    new_lwpr: s(),
    lwpr_near_rate: s(),
    stck_sdpr: s(),
  })
  .passthrough();

export const getStockNewHighLowApproachingTopResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getStockNewHighLowApproachingTopItemSchema).default([]),
  })
  .passthrough();

// ── getStockDividendYieldTop: Stock Dividend Yield Top ──

export const getStockDividendYieldTopItemSchema = z
  .object({
    rank: s(),
    sht_cd: s(),
    isin_name: s(),
    record_date: s(),
    per_sto_divi_amt: s(),
    divi_rate: s(),
    divi_kind: s(),
  })
  .passthrough();

export const getStockDividendYieldTopResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getStockDividendYieldTopItemSchema).default([]),
  })
  .passthrough();

// ── getStockLargeExecutionCountTop: Stock Large Execution Count Top ──

export const getStockLargeExecutionCountTopItemSchema = z
  .object({
    mksc_shrn_iscd: s(),
    data_rank: s(),
    hts_kor_isnm: s(),
    stck_prpr: s(),
    prdy_vrss_sign: s(),
    prdy_vrss: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    shnu_cntg_csnu: s(),
    seln_cntg_csnu: s(),
    ntby_cnqn: s(),
  })
  .passthrough();

export const getStockLargeExecutionCountTopResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getStockLargeExecutionCountTopItemSchema).default([]),
  })
  .passthrough();

// ── getStockCreditBalanceTop: Stock Credit Balance Top ──

export const getStockCreditBalanceTopItemSchema = z
  .object({
    mksc_shrn_iscd: s(),
    hts_kor_isnm: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    acml_tr_pbmn: s(),
    ssts_cntg_qty: s(),
    ssts_vol_rlim: s(),
    ssts_tr_pbmn: s(),
    ssts_tr_pbmn_rlim: s(),
    stnd_date1: s(),
    stnd_date2: s(),
    avrg_prc: s(),
  })
  .passthrough();

export const getStockCreditBalanceTopResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getStockCreditBalanceTopItemSchema).default([]),
  })
  .passthrough();

// ── getStockShortSellingTop: Stock Short Selling Top ──

export const getStockShortSellingTopItemSchema = z
  .object({
    mksc_shrn_iscd: s(),
    hts_kor_isnm: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    acml_tr_pbmn: s(),
    ssts_cntg_qty: s(),
    ssts_vol_rlim: s(),
    ssts_tr_pbmn: s(),
    ssts_tr_pbmn_rlim: s(),
    stnd_date1: s(),
    stnd_date2: s(),
    avrg_prc: s(),
  })
  .passthrough();

export const getStockShortSellingTopResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getStockShortSellingTopItemSchema).default([]),
  })
  .passthrough();

// ── getStockAfterHoursFluctuationRank: Stock After Hours Fluctuation Rank ──

export const getStockAfterHoursFluctuationRankOutput1ItemSchema = z
  .object({
    ovtm_untp_uplm_issu_cnt: s(),
    ovtm_untp_ascn_issu_cnt: s(),
    ovtm_untp_stnr_issu_cnt: s(),
    ovtm_untp_lslm_issu_cnt: s(),
    ovtm_untp_down_issu_cnt: s(),
    ovtm_untp_acml_vol: s(),
    ovtm_untp_acml_tr_pbmn: s(),
    ovtm_untp_exch_vol: s(),
    ovtm_untp_exch_tr_pbmn: s(),
    ovtm_untp_kosdaq_vol: s(),
    ovtm_untp_kosdaq_tr_pbmn: s(),
  })
  .passthrough();

export const getStockAfterHoursFluctuationRankOutput2ItemSchema = z
  .object({
    mksc_shrn_iscd: s(),
    hts_kor_isnm: s(),
    ovtm_untp_prpr: s(),
    ovtm_untp_prdy_vrss: s(),
    ovtm_untp_prdy_vrss_sign: s(),
    ovtm_untp_prdy_ctrt: s(),
    ovtm_untp_askp1: s(),
    ovtm_untp_seln_rsqn: s(),
    ovtm_untp_bidp1: s(),
    ovtm_untp_shnu_rsqn: s(),
    ovtm_untp_vol: s(),
    ovtm_vrss_acml_vol_rlim: s(),
    stck_prpr: s(),
    acml_vol: s(),
    bidp: s(),
    askp: s(),
  })
  .passthrough();

export const getStockAfterHoursFluctuationRankResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getStockAfterHoursFluctuationRankOutput1ItemSchema.optional(),
    output2: z.array(getStockAfterHoursFluctuationRankOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getStockAfterHoursVolumeRank: Stock After Hours Volume Rank ──

export const getStockAfterHoursVolumeRankOutput1ItemSchema = z
  .object({
    ovtm_untp_exch_vol: s(),
    ovtm_untp_exch_tr_pbmn: s(),
    ovtm_untp_kosdaq_vol: s(),
    ovtm_untp_kosdaq_tr_pbmn: s(),
  })
  .passthrough();

export const getStockAfterHoursVolumeRankOutput2ItemSchema = z
  .object({
    stck_shrn_iscd: s(),
    hts_kor_isnm: s(),
    ovtm_untp_prpr: s(),
    ovtm_untp_prdy_vrss: s(),
    ovtm_untp_prdy_vrss_sign: s(),
    ovtm_untp_prdy_ctrt: s(),
    ovtm_untp_seln_rsqn: s(),
    ovtm_untp_shnu_rsqn: s(),
    ovtm_untp_vol: s(),
    ovtm_vrss_acml_vol_rlim: s(),
    stck_prpr: s(),
    acml_vol: s(),
    bidp: s(),
    askp: s(),
  })
  .passthrough();

export const getStockAfterHoursVolumeRankResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getStockAfterHoursVolumeRankOutput1ItemSchema.optional(),
    output2: z.array(getStockAfterHoursVolumeRankOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getHtsInquiryTop20: Hts Inquiry Top20 ──

export const getHtsInquiryTop20ItemSchema = z
  .object({
    mrkt_div_cls_code: s(),
    mksc_shrn_iscd: s(),
  })
  .passthrough();

export const getHtsInquiryTop20ResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: z.array(getHtsInquiryTop20ItemSchema).default([]),
  })
  .passthrough();

// ── Response Types ──

export type GetTradingVolumeRankResponse = CamelizeKeys<z.infer<typeof getTradingVolumeRankResponseSchema>>;

export type GetStockFluctuationRankResponse = CamelizeKeys<z.infer<typeof getStockFluctuationRankResponseSchema>>;

export type GetStockHogaQuantityRankResponse = CamelizeKeys<z.infer<typeof getStockHogaQuantityRankResponseSchema>>;

export type GetStockProfitabilityIndicatorRankResponse = CamelizeKeys<
  z.infer<typeof getStockProfitabilityIndicatorRankResponseSchema>
>;

export type GetStockMarketCapTopResponse = CamelizeKeys<z.infer<typeof getStockMarketCapTopResponseSchema>>;

export type GetStockFinanceRatioRankResponse = CamelizeKeys<z.infer<typeof getStockFinanceRatioRankResponseSchema>>;

export type GetStockTimeHogaRankResponse = CamelizeKeys<z.infer<typeof getStockTimeHogaRankResponseSchema>>;

export type GetStockPreferredStockRatioTopResponse = CamelizeKeys<
  z.infer<typeof getStockPreferredStockRatioTopResponseSchema>
>;

export type GetStockDisparityIndexRankResponse = CamelizeKeys<z.infer<typeof getStockDisparityIndexRankResponseSchema>>;

export type GetStockMarketPriceRankResponse = CamelizeKeys<z.infer<typeof getStockMarketPriceRankResponseSchema>>;

export type GetStockExecutionStrengthTopResponse = CamelizeKeys<
  z.infer<typeof getStockExecutionStrengthTopResponseSchema>
>;

export type GetStockWatchlistRegistrationTopResponse = CamelizeKeys<
  z.infer<typeof getStockWatchlistRegistrationTopResponseSchema>
>;

export type GetStockExpectedExecutionRiseDeclineTopResponse = CamelizeKeys<
  z.infer<typeof getStockExpectedExecutionRiseDeclineTopResponseSchema>
>;

export type GetStockProprietaryTradingTopResponse = CamelizeKeys<
  z.infer<typeof getStockProprietaryTradingTopResponseSchema>
>;

export type GetStockNewHighLowApproachingTopResponse = CamelizeKeys<
  z.infer<typeof getStockNewHighLowApproachingTopResponseSchema>
>;

export type GetStockDividendYieldTopResponse = CamelizeKeys<z.infer<typeof getStockDividendYieldTopResponseSchema>>;

export type GetStockLargeExecutionCountTopResponse = CamelizeKeys<
  z.infer<typeof getStockLargeExecutionCountTopResponseSchema>
>;

export type GetStockCreditBalanceTopResponse = CamelizeKeys<z.infer<typeof getStockCreditBalanceTopResponseSchema>>;

export type GetStockShortSellingTopResponse = CamelizeKeys<z.infer<typeof getStockShortSellingTopResponseSchema>>;

export type GetStockAfterHoursFluctuationRankResponse = CamelizeKeys<
  z.infer<typeof getStockAfterHoursFluctuationRankResponseSchema>
>;

export type GetStockAfterHoursVolumeRankResponse = CamelizeKeys<
  z.infer<typeof getStockAfterHoursVolumeRankResponseSchema>
>;

export type GetHtsInquiryTop20Response = CamelizeKeys<z.infer<typeof getHtsInquiryTop20ResponseSchema>>;

// ── Response Map ──

export interface DomesticRankingAnalysisResponseMap {
  getTradingVolumeRank: GetTradingVolumeRankResponse;
  getStockFluctuationRank: GetStockFluctuationRankResponse;
  getStockHogaQuantityRank: GetStockHogaQuantityRankResponse;
  getStockProfitabilityIndicatorRank: GetStockProfitabilityIndicatorRankResponse;
  getStockMarketCapTop: GetStockMarketCapTopResponse;
  getStockFinanceRatioRank: GetStockFinanceRatioRankResponse;
  getStockTimeHogaRank: GetStockTimeHogaRankResponse;
  getStockPreferredStockRatioTop: GetStockPreferredStockRatioTopResponse;
  getStockDisparityIndexRank: GetStockDisparityIndexRankResponse;
  getStockMarketPriceRank: GetStockMarketPriceRankResponse;
  getStockExecutionStrengthTop: GetStockExecutionStrengthTopResponse;
  getStockWatchlistRegistrationTop: GetStockWatchlistRegistrationTopResponse;
  getStockExpectedExecutionRiseDeclineTop: GetStockExpectedExecutionRiseDeclineTopResponse;
  getStockProprietaryTradingTop: GetStockProprietaryTradingTopResponse;
  getStockNewHighLowApproachingTop: GetStockNewHighLowApproachingTopResponse;
  getStockDividendYieldTop: GetStockDividendYieldTopResponse;
  getStockLargeExecutionCountTop: GetStockLargeExecutionCountTopResponse;
  getStockCreditBalanceTop: GetStockCreditBalanceTopResponse;
  getStockShortSellingTop: GetStockShortSellingTopResponse;
  getStockAfterHoursFluctuationRank: GetStockAfterHoursFluctuationRankResponse;
  getStockAfterHoursVolumeRank: GetStockAfterHoursVolumeRankResponse;
  getHtsInquiryTop20: GetHtsInquiryTop20Response;
}
