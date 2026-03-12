import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types';

const s = () => z.string().default('');

const envelope = {
  return_code: z.union([z.string(), z.number()]).optional(),
  return_msg: z.string().optional(),
};

// ── ka10060: 종목별투자자기관차트 ──

export const individualStockInstitutionalChartItemSchema = z
  .object({
    dt: s(),
    cur_prc: s(),
    pred_pre: s(),
    acc_trde_prica: s(),
    ind_invsr: s(),
    frgnr_invsr: s(),
    orgn: s(),
    fnnc_invt: s(),
    insrnc: s(),
    invtrt: s(),
    etc_fnnc: s(),
    bank: s(),
    penfnd_etc: s(),
    samo_fund: s(),
    natn: s(),
    etc_corp: s(),
    natfor: s(),
  })
  .passthrough();

export const individualStockInstitutionalChartResponseSchema = z
  .object({
    ...envelope,
    stk_invsr_orgn_chart: z.array(individualStockInstitutionalChartItemSchema).default([]),
  })
  .passthrough();

// ── ka10064: 장중투자자매매동향 ──

export const intradayInvestorTradingItemSchema = z
  .object({
    tm: s(),
    frgnr_invsr: s(),
    orgn: s(),
    invtrt: s(),
    insrnc: s(),
    bank: s(),
    penfnd_etc: s(),
    etc_corp: s(),
    natn: s(),
  })
  .passthrough();

export const intradayInvestorTradingResponseSchema = z
  .object({
    ...envelope,
    opmr_invsr_trde_chart: z.array(intradayInvestorTradingItemSchema).default([]),
  })
  .passthrough();

// ── ka10079: 주식틱차트 ──

export const stockTickItemSchema = z
  .object({
    cur_prc: s(),
    trde_qty: s(),
    cntr_tm: s(),
    open_pric: s(),
    high_pric: s(),
    low_pric: s(),
    pred_pre: s(),
    pred_pre_sig: s(),
  })
  .passthrough();

export const stockTickResponseSchema = z
  .object({
    ...envelope,
    stk_cd: s(),
    last_tic_cnt: s(),
    stk_tic_chart_qry: z.array(stockTickItemSchema).default([]),
  })
  .passthrough();

// ── ka10080: 주식분봉차트 ──

export const stockMinuteItemSchema = z
  .object({
    cur_prc: s(),
    trde_qty: s(),
    cntr_tm: s(),
    open_pric: s(),
    high_pric: s(),
    low_pric: s(),
    acc_trde_qty: s(),
    pred_pre: s(),
    pred_pre_sig: s(),
  })
  .passthrough();

export const stockMinuteResponseSchema = z
  .object({
    ...envelope,
    stk_cd: s(),
    stk_min_pole_chart_qry: z.array(stockMinuteItemSchema).default([]),
  })
  .passthrough();

// ── ka10081: 주식일봉차트 ──

export const stockDailyItemSchema = z
  .object({
    cur_prc: s(),
    trde_qty: s(),
    trde_prica: s(),
    dt: s(),
    open_pric: s(),
    high_pric: s(),
    low_pric: s(),
    pred_pre: s(),
    pred_pre_sig: s(),
    trde_tern_rt: s(),
  })
  .passthrough();

export const stockDailyResponseSchema = z
  .object({
    ...envelope,
    stk_cd: s(),
    stk_dt_pole_chart_qry: z.array(stockDailyItemSchema).default([]),
  })
  .passthrough();

// ── ka10082: 주식주봉차트 ──

export const stockWeeklyItemSchema = z
  .object({
    cur_prc: s(),
    trde_qty: s(),
    trde_prica: s(),
    dt: s(),
    open_pric: s(),
    high_pric: s(),
    low_pric: s(),
    pred_pre: s(),
    pred_pre_sig: s(),
    trde_tern_rt: s(),
  })
  .passthrough();

export const stockWeeklyResponseSchema = z
  .object({
    ...envelope,
    stk_cd: s(),
    stk_stk_pole_chart_qry: z.array(stockWeeklyItemSchema).default([]),
  })
  .passthrough();

// ── ka10083: 주식월봉차트 ──

export const stockMonthlyItemSchema = z
  .object({
    cur_prc: s(),
    trde_qty: s(),
    trde_prica: s(),
    dt: s(),
    open_pric: s(),
    high_pric: s(),
    low_pric: s(),
    pred_pre: s(),
    pred_pre_sig: s(),
    trde_tern_rt: s(),
  })
  .passthrough();

export const stockMonthlyResponseSchema = z
  .object({
    ...envelope,
    stk_cd: s(),
    stk_mth_pole_chart_qry: z.array(stockMonthlyItemSchema).default([]),
  })
  .passthrough();

// ── ka10094: 주식년봉차트 ──

export const stockYearlyItemSchema = z
  .object({
    cur_prc: s(),
    trde_qty: s(),
    trde_prica: s(),
    dt: s(),
    open_pric: s(),
    high_pric: s(),
    low_pric: s(),
  })
  .passthrough();

export const stockYearlyResponseSchema = z
  .object({
    ...envelope,
    stk_cd: s(),
    stk_yr_pole_chart_qry: z.array(stockYearlyItemSchema).default([]),
  })
  .passthrough();

// ── ka20004: 업종틱차트 ──

export const industryTickItemSchema = z
  .object({
    cur_prc: s(),
    trde_qty: s(),
    cntr_tm: s(),
    open_pric: s(),
    high_pric: s(),
    low_pric: s(),
    pred_pre: s(),
    pred_pre_sig: s(),
  })
  .passthrough();

export const industryTickResponseSchema = z
  .object({
    ...envelope,
    inds_cd: s(),
    inds_tic_chart_qry: z.array(industryTickItemSchema).default([]),
  })
  .passthrough();

// ── ka20005: 업종분봉차트 ──

export const industryMinuteItemSchema = z
  .object({
    cur_prc: s(),
    trde_qty: s(),
    cntr_tm: s(),
    open_pric: s(),
    high_pric: s(),
    low_pric: s(),
    acc_trde_qty: s(),
    pred_pre: s(),
    pred_pre_sig: s(),
  })
  .passthrough();

export const industryMinuteResponseSchema = z
  .object({
    ...envelope,
    inds_cd: s(),
    inds_min_pole_qry: z.array(industryMinuteItemSchema).default([]),
  })
  .passthrough();

// ── ka20006: 업종일봉차트 ──

export const industryDailyItemSchema = z
  .object({
    cur_prc: s(),
    trde_qty: s(),
    dt: s(),
    open_pric: s(),
    high_pric: s(),
    low_pric: s(),
    trde_prica: s(),
  })
  .passthrough();

export const industryDailyResponseSchema = z
  .object({
    ...envelope,
    inds_cd: s(),
    inds_dt_pole_qry: z.array(industryDailyItemSchema).default([]),
  })
  .passthrough();

// ── ka20007: 업종주봉차트 ──

export const industryWeeklyItemSchema = z
  .object({
    cur_prc: s(),
    trde_qty: s(),
    dt: s(),
    open_pric: s(),
    high_pric: s(),
    low_pric: s(),
    trde_prica: s(),
  })
  .passthrough();

export const industryWeeklyResponseSchema = z
  .object({
    ...envelope,
    inds_cd: s(),
    inds_stk_pole_qry: z.array(industryWeeklyItemSchema).default([]),
  })
  .passthrough();

// ── ka20008: 업종월봉차트 ──

export const industryMonthlyItemSchema = z
  .object({
    cur_prc: s(),
    trde_qty: s(),
    dt: s(),
    open_pric: s(),
    high_pric: s(),
    low_pric: s(),
    trde_prica: s(),
  })
  .passthrough();

export const industryMonthlyResponseSchema = z
  .object({
    ...envelope,
    inds_cd: s(),
    inds_mth_pole_qry: z.array(industryMonthlyItemSchema).default([]),
  })
  .passthrough();

// ── ka20019: 업종년봉차트 ──

export const industryYearlyItemSchema = z
  .object({
    cur_prc: s(),
    trde_qty: s(),
    dt: s(),
    open_pric: s(),
    high_pric: s(),
    low_pric: s(),
    trde_prica: s(),
  })
  .passthrough();

export const industryYearlyResponseSchema = z
  .object({
    ...envelope,
    inds_cd: s(),
    inds_yr_pole_qry: z.array(industryYearlyItemSchema).default([]),
  })
  .passthrough();

// ── Response Types ──

export type IndividualStockInstitutionalChartResponse = CamelizeKeys<
  z.infer<typeof individualStockInstitutionalChartResponseSchema>
>;
export type IntradayInvestorTradingResponse = CamelizeKeys<z.infer<typeof intradayInvestorTradingResponseSchema>>;
export type StockTickResponse = CamelizeKeys<z.infer<typeof stockTickResponseSchema>>;
export type StockMinuteResponse = CamelizeKeys<z.infer<typeof stockMinuteResponseSchema>>;
export type StockDailyResponse = CamelizeKeys<z.infer<typeof stockDailyResponseSchema>>;
export type StockWeeklyResponse = CamelizeKeys<z.infer<typeof stockWeeklyResponseSchema>>;
export type StockMonthlyResponse = CamelizeKeys<z.infer<typeof stockMonthlyResponseSchema>>;
export type StockYearlyResponse = CamelizeKeys<z.infer<typeof stockYearlyResponseSchema>>;
export type IndustryTickResponse = CamelizeKeys<z.infer<typeof industryTickResponseSchema>>;
export type IndustryMinuteResponse = CamelizeKeys<z.infer<typeof industryMinuteResponseSchema>>;
export type IndustryDailyResponse = CamelizeKeys<z.infer<typeof industryDailyResponseSchema>>;
export type IndustryWeeklyResponse = CamelizeKeys<z.infer<typeof industryWeeklyResponseSchema>>;
export type IndustryMonthlyResponse = CamelizeKeys<z.infer<typeof industryMonthlyResponseSchema>>;
export type IndustryYearlyResponse = CamelizeKeys<z.infer<typeof industryYearlyResponseSchema>>;

// ── Response Map ──

export interface DomesticChartResponseMap {
  getIndividualStockInstitutionalChart: IndividualStockInstitutionalChartResponse;
  getIntradayInvestorTrading: IntradayInvestorTradingResponse;
  getStockTick: StockTickResponse;
  getStockMinute: StockMinuteResponse;
  getStockDaily: StockDailyResponse;
  getStockWeekly: StockWeeklyResponse;
  getStockMonthly: StockMonthlyResponse;
  getStockYearly: StockYearlyResponse;
  getIndustryTick: IndustryTickResponse;
  getIndustryMinute: IndustryMinuteResponse;
  getIndustryDaily: IndustryDailyResponse;
  getIndustryWeekly: IndustryWeeklyResponse;
  getIndustryMonthly: IndustryMonthlyResponse;
  getIndustryYearly: IndustryYearlyResponse;
}
