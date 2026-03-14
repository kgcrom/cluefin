import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types';

const s = () => z.string().default('');

const kisEnvelope = {
  rt_cd: z.string().optional(),
  msg_cd: z.string().optional(),
  msg1: z.string().optional(),
};

// ── getSectorCurrentIndex: Sector Current Index ──

export const getSectorCurrentIndexItemSchema = z
  .object({
    bstp_nmix_prpr: s(),
    bstp_nmix_prdy_vrss: s(),
    prdy_vrss_sign: s(),
    bstp_nmix_prdy_ctrt: s(),
    acml_vol: s(),
    prdy_vol: s(),
    acml_tr_pbmn: s(),
    prdy_tr_pbmn: s(),
    bstp_nmix_oprc: s(),
    prdy_nmix_vrss_nmix_oprc: s(),
    oprc_vrss_prpr_sign: s(),
    bstp_nmix_oprc_prdy_ctrt: s(),
    bstp_nmix_hgpr: s(),
    prdy_nmix_vrss_nmix_hgpr: s(),
    hgpr_vrss_prpr_sign: s(),
    bstp_nmix_hgpr_prdy_ctrt: s(),
    bstp_nmix_lwpr: s(),
    prdy_clpr_vrss_lwpr: s(),
    lwpr_vrss_prpr_sign: s(),
    prdy_clpr_vrss_lwpr_rate: s(),
    ascn_issu_cnt: s(),
    uplm_issu_cnt: s(),
    stnr_issu_cnt: s(),
    down_issu_cnt: s(),
    lslm_issu_cnt: s(),
    dryy_bstp_nmix_hgpr: s(),
    dryy_hgpr_vrss_prpr_rate: s(),
    dryy_bstp_nmix_hgpr_date: s(),
    dryy_bstp_nmix_lwpr: s(),
    dryy_lwpr_vrss_prpr_rate: s(),
    dryy_bstp_nmix_lwpr_date: s(),
    total_askp_rsqn: s(),
    total_bidp_rsqn: s(),
    seln_rsqn_rate: s(),
    shnu_rsqn_rate: s(),
    ntby_rsqn: s(),
  })
  .passthrough();

export const getSectorCurrentIndexResponseSchema = z
  .object({
    ...kisEnvelope,
    output: getSectorCurrentIndexItemSchema.optional(),
  })
  .passthrough();

// ── getSectorDailyIndex: Sector Daily Index ──

export const getSectorDailyIndexOutput1ItemSchema = z
  .object({
    bstp_nmix_prpr: s(),
    bstp_nmix_prdy_vrss: s(),
    prdy_vrss_sign: s(),
    bstp_nmix_prdy_ctrt: s(),
    acml_vol: s(),
    acml_tr_pbmn: s(),
    bstp_nmix_oprc: s(),
    bstp_nmix_hgpr: s(),
    bstp_nmix_lwpr: s(),
    prdy_vol: s(),
    ascn_issu_cnt: s(),
    down_issu_cnt: s(),
    stnr_issu_cnt: s(),
    uplm_issu_cnt: s(),
    lslm_issu_cnt: s(),
    prdy_tr_pbmn: s(),
    dryy_bstp_nmix_hgpr_date: s(),
    dryy_bstp_nmix_hgpr: s(),
    dryy_bstp_nmix_lwpr: s(),
    dryy_bstp_nmix_lwpr_date: s(),
  })
  .passthrough();

export const getSectorDailyIndexOutput2ItemSchema = z
  .object({
    stck_bsop_date: s(),
    bstp_nmix_prpr: s(),
    prdy_vrss_sign: s(),
    bstp_nmix_prdy_vrss: s(),
    bstp_nmix_prdy_ctrt: s(),
    bstp_nmix_oprc: s(),
    bstp_nmix_hgpr: s(),
    bstp_nmix_lwpr: s(),
    acml_vol_rlim: s(),
    acml_vol: s(),
    acml_tr_pbmn: s(),
    invt_new_psdg: s(),
    d20_dsrt: s(),
  })
  .passthrough();

export const getSectorDailyIndexResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getSectorDailyIndexOutput1ItemSchema.optional(),
    output2: z.array(getSectorDailyIndexOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getSectorTimeIndexSecond: Sector Time Index Second ──

export const getSectorTimeIndexSecondItemSchema = z
  .object({
    stck_cntg_hour: s(),
    bstp_nmix_prpr: s(),
    bstp_nmix_prdy_vrss: s(),
    prdy_vrss_sign: s(),
    bstp_nmix_prdy_ctrt: s(),
    acml_tr_pbmn: s(),
    acml_vol: s(),
    cntg_vol: s(),
  })
  .passthrough();

export const getSectorTimeIndexSecondResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getSectorTimeIndexSecondItemSchema).default([]),
  })
  .passthrough();

// ── getSectorTimeIndexMinute: Sector Time Index Minute ──

export const getSectorTimeIndexMinuteItemSchema = z
  .object({
    bsop_hour: s(),
    bstp_nmix_prpr: s(),
    bstp_nmix_prdy_vrss: s(),
    prdy_vrss_sign: s(),
    bstp_nmix_prdy_ctrt: s(),
    acml_tr_pbmn: s(),
    acml_vol: s(),
    cntg_vol: s(),
  })
  .passthrough();

export const getSectorTimeIndexMinuteResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getSectorTimeIndexMinuteItemSchema).default([]),
  })
  .passthrough();

// ── getSectorMinuteInquiry: Sector Minute Inquiry ──

export const getSectorMinuteInquiryOutput1ItemSchema = z
  .object({
    bstp_nmix_prdy_vrss: s(),
    prdy_vrss_sign: s(),
    bstp_nmix_prdy_ctrt: s(),
    prdy_nmix: s(),
    acml_vol: s(),
    acml_tr_pbmn: s(),
    hts_kor_isnm: s(),
    bstp_nmix_prpr: s(),
    bstp_cls_code: s(),
    prdy_vol: s(),
    bstp_nmix_oprc: s(),
    bstp_nmix_hgpr: s(),
    bstp_nmix_lwpr: s(),
    futs_prdy_oprc: s(),
    futs_prdy_hgpr: s(),
    futs_prdy_lwpr: s(),
  })
  .passthrough();

export const getSectorMinuteInquiryOutput2ItemSchema = z
  .object({
    stck_bsop_date: s(),
    stck_cntg_hour: s(),
    bstp_nmix_prpr: s(),
    bstp_nmix_oprc: s(),
    bstp_nmix_hgpr: s(),
    bstp_nmix_lwpr: s(),
    cntg_vol: s(),
    acml_tr_pbmn: s(),
  })
  .passthrough();

export const getSectorMinuteInquiryResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getSectorMinuteInquiryOutput1ItemSchema.optional(),
    output2: z.array(getSectorMinuteInquiryOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getSectorPeriodQuote: Sector Period Quote ──

export const getSectorPeriodQuoteOutput1ItemSchema = z
  .object({
    prdy_vrss_sign: s(),
    bstp_nmix_prdy_ctrt: s(),
    prdy_nmix: s(),
    acml_vol: s(),
    acml_tr_pbmn: s(),
    hts_kor_isnm: s(),
    bstp_nmix_prpr: s(),
    bstp_cls_code: s(),
    prdy_vol: s(),
    bstp_nmix_oprc: s(),
    bstp_nmix_hgpr: s(),
    bstp_nmix_lwpr: s(),
    futs_prdy_oprc: s(),
    futs_prdy_hgpr: s(),
    futs_prdy_lwpr: s(),
  })
  .passthrough();

export const getSectorPeriodQuoteOutput2ItemSchema = z
  .object({
    stck_bsop_date: s(),
    bstp_nmix_prpr: s(),
    bstp_nmix_oprc: s(),
    bstp_nmix_hgpr: s(),
    bstp_nmix_lwpr: s(),
    acml_vol: s(),
    acml_tr_pbmn: s(),
    mod_yn: s(),
  })
  .passthrough();

export const getSectorPeriodQuoteResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getSectorPeriodQuoteOutput1ItemSchema.optional(),
    output2: z.array(getSectorPeriodQuoteOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getSectorAllQuoteByCategory: Sector All Quote By Category ──

export const getSectorAllQuoteByCategoryOutput1ItemSchema = z
  .object({
    bstp_nmix_prpr: s(),
    bstp_nmix_prdy_vrss: s(),
    prdy_vrss_sign: s(),
    bstp_nmix_prdy_ctrt: s(),
    acml_vol: s(),
    acml_tr_pbmn: s(),
    bstp_nmix_oprc: s(),
    bstp_nmix_hgpr: s(),
    bstp_nmix_lwpr: s(),
    prdy_vol: s(),
    ascn_issu_cnt: s(),
    down_issu_cnt: s(),
    stnr_issu_cnt: s(),
    uplm_issu_cnt: s(),
    lslm_issu_cnt: s(),
    prdy_tr_pbmn: s(),
    dryy_bstp_nmix_hgpr_date: s(),
    dryy_bstp_nmix_hgpr: s(),
    dryy_bstp_nmix_lwpr: s(),
    dryy_bstp_nmix_lwpr_date: s(),
  })
  .passthrough();

export const getSectorAllQuoteByCategoryOutput2ItemSchema = z
  .object({
    bstp_cls_code: s(),
    hts_kor_isnm: s(),
    bstp_nmix_prpr: s(),
    bstp_nmix_prdy_vrss: s(),
    prdy_vrss_sign: s(),
    bstp_nmix_prdy_ctrt: s(),
    acml_vol: s(),
    acml_tr_pbmn: s(),
    acml_vol_rlim: s(),
    acml_tr_pbmn_rlim: s(),
  })
  .passthrough();

export const getSectorAllQuoteByCategoryResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getSectorAllQuoteByCategoryOutput1ItemSchema.optional(),
    output2: z.array(getSectorAllQuoteByCategoryOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getExpectedIndexTrend: Expected Index Trend ──

export const getExpectedIndexTrendItemSchema = z
  .object({
    stck_cntg_hour: s(),
    bstp_nmix_prpr: s(),
    prdy_vrss_sign: s(),
    bstp_nmix_prdy_vrss: s(),
    prdy_ctrt: s(),
    acml_vol: s(),
    acml_tr_pbmn: s(),
  })
  .passthrough();

export const getExpectedIndexTrendResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getExpectedIndexTrendItemSchema).default([]),
  })
  .passthrough();

// ── getExpectedIndexAll: Expected Index All ──

export const getExpectedIndexAllOutput1ItemSchema = z
  .object({
    bstp_nmix_prpr: s(),
    bstp_nmix_prdy_vrss: s(),
    prdy_vrss_sign: z.string().optional(),
    prdy_ctrt: s(),
    acml_vol: s(),
    ascn_issu_cnt: s(),
    down_issu_cnt: s(),
    stnr_issu_cnt: s(),
    bstp_cls_code: z.string().optional(),
  })
  .passthrough();

export const getExpectedIndexAllOutput2ItemSchema = z
  .object({
    bstp_cls_code: s(),
    hts_kor_isnm: s(),
    bstp_nmix_prpr: s(),
    bstp_nmix_prdy_vrss: s(),
    prdy_vrss_sign: s(),
    bstp_nmix_prdy_ctrt: s(),
    acml_vol: s(),
    nmix_sdpr: s(),
    ascn_issu_cnt: s(),
    stnr_issu_cnt: s(),
    down_issu_cnt: s(),
  })
  .passthrough();

export const getExpectedIndexAllResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getExpectedIndexAllOutput1ItemSchema.optional(),
    output2: z.array(getExpectedIndexAllOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getVolatilityInterruptionStatus: Volatility Interruption Status ──

export const getVolatilityInterruptionStatusItemSchema = z
  .object({
    hts_kor_isnm: s(),
    mksc_shrn_iscd: s(),
    vi_cls_code: s(),
    bsop_date: s(),
    cntg_vi_hour: s(),
    vi_cncl_hour: s(),
    vi_kind_code: s(),
    vi_prc: s(),
    vi_stnd_prc: s(),
    vi_dprt: s(),
    vi_dmc_stnd_prc: s(),
    vi_dmc_dprt: s(),
    vi_count: s(),
  })
  .passthrough();

export const getVolatilityInterruptionStatusResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getVolatilityInterruptionStatusItemSchema).default([]),
  })
  .passthrough();

// ── getInterestRateSummary: Interest Rate Summary ──

export const getInterestRateSummaryOutput1ItemSchema = z
  .object({
    bcdt_code: s(),
    hts_kor_isnm: s(),
    bond_mnrt_prpr: s(),
    prdy_vrss_sign: s(),
    bond_mnrt_prdy_vrss: s(),
    prdy_ctrt: s(),
    stck_bsop_date: s(),
  })
  .passthrough();

export const getInterestRateSummaryOutput2ItemSchema = z
  .object({
    bcdt_code: s(),
    hts_kor_isnm: s(),
    bond_mnrt_prpr: s(),
    prdy_vrss_sign: s(),
    bond_mnrt_prdy_vrss: s(),
    bstp_nmix_prdy_ctrt: s(),
    stck_bsop_date: s(),
  })
  .passthrough();

export const getInterestRateSummaryResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: z.array(getInterestRateSummaryOutput1ItemSchema).default([]),
    output2: z.array(getInterestRateSummaryOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getMarketAnnouncementSchedule: Market Announcement Schedule ──

export const getMarketAnnouncementScheduleItemSchema = z
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
  })
  .passthrough();

export const getMarketAnnouncementScheduleResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getMarketAnnouncementScheduleItemSchema).default([]),
  })
  .passthrough();

// ── getHolidayInquiry: Holiday Inquiry ──

export const getHolidayInquiryItemSchema = z
  .object({
    bass_dt: s(),
    wday_dvsn_cd: s(),
    bzdy_yn: s(),
    tr_day_yn: s(),
    opnd_yn: s(),
    sttl_day_yn: s(),
  })
  .passthrough();

export const getHolidayInquiryResponseSchema = z
  .object({
    ...kisEnvelope,
    ctx_area_fk: s(),
    ctx_area_nk: s(),
    output: z.array(getHolidayInquiryItemSchema).default([]),
  })
  .passthrough();

// ── getFuturesBusinessDayInquiry: Futures Business Day Inquiry ──

export const getFuturesBusinessDayInquiryItemSchema = z
  .object({
    date1: s(),
    date2: s(),
    date3: s(),
    date4: s(),
    date5: s(),
    today: s(),
    time: s(),
    s_time: s(),
    e_time: s(),
  })
  .passthrough();

export const getFuturesBusinessDayInquiryResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: z.array(getFuturesBusinessDayInquiryItemSchema).default([]),
  })
  .passthrough();

// ── Response Types ──

export type GetSectorCurrentIndexResponse = CamelizeKeys<z.infer<typeof getSectorCurrentIndexResponseSchema>>;

export type GetSectorDailyIndexResponse = CamelizeKeys<z.infer<typeof getSectorDailyIndexResponseSchema>>;

export type GetSectorTimeIndexSecondResponse = CamelizeKeys<z.infer<typeof getSectorTimeIndexSecondResponseSchema>>;

export type GetSectorTimeIndexMinuteResponse = CamelizeKeys<z.infer<typeof getSectorTimeIndexMinuteResponseSchema>>;

export type GetSectorMinuteInquiryResponse = CamelizeKeys<z.infer<typeof getSectorMinuteInquiryResponseSchema>>;

export type GetSectorPeriodQuoteResponse = CamelizeKeys<z.infer<typeof getSectorPeriodQuoteResponseSchema>>;

export type GetSectorAllQuoteByCategoryResponse = CamelizeKeys<
  z.infer<typeof getSectorAllQuoteByCategoryResponseSchema>
>;

export type GetExpectedIndexTrendResponse = CamelizeKeys<z.infer<typeof getExpectedIndexTrendResponseSchema>>;

export type GetExpectedIndexAllResponse = CamelizeKeys<z.infer<typeof getExpectedIndexAllResponseSchema>>;

export type GetVolatilityInterruptionStatusResponse = CamelizeKeys<
  z.infer<typeof getVolatilityInterruptionStatusResponseSchema>
>;

export type GetInterestRateSummaryResponse = CamelizeKeys<z.infer<typeof getInterestRateSummaryResponseSchema>>;

export type GetMarketAnnouncementScheduleResponse = CamelizeKeys<
  z.infer<typeof getMarketAnnouncementScheduleResponseSchema>
>;

export type GetHolidayInquiryResponse = CamelizeKeys<z.infer<typeof getHolidayInquiryResponseSchema>>;

export type GetFuturesBusinessDayInquiryResponse = CamelizeKeys<
  z.infer<typeof getFuturesBusinessDayInquiryResponseSchema>
>;

// ── Response Map ──

export interface DomesticIssueOtherResponseMap {
  getSectorCurrentIndex: GetSectorCurrentIndexResponse;
  getSectorDailyIndex: GetSectorDailyIndexResponse;
  getSectorTimeIndexSecond: GetSectorTimeIndexSecondResponse;
  getSectorTimeIndexMinute: GetSectorTimeIndexMinuteResponse;
  getSectorMinuteInquiry: GetSectorMinuteInquiryResponse;
  getSectorPeriodQuote: GetSectorPeriodQuoteResponse;
  getSectorAllQuoteByCategory: GetSectorAllQuoteByCategoryResponse;
  getExpectedIndexTrend: GetExpectedIndexTrendResponse;
  getExpectedIndexAll: GetExpectedIndexAllResponse;
  getVolatilityInterruptionStatus: GetVolatilityInterruptionStatusResponse;
  getInterestRateSummary: GetInterestRateSummaryResponse;
  getMarketAnnouncementSchedule: GetMarketAnnouncementScheduleResponse;
  getHolidayInquiry: GetHolidayInquiryResponse;
  getFuturesBusinessDayInquiry: GetFuturesBusinessDayInquiryResponse;
}
