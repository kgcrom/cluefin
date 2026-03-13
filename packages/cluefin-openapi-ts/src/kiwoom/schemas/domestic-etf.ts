import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types';

const s = () => z.string().default('');

const envelope = {
  return_code: z.union([z.string(), z.number()]).optional(),
  return_msg: z.string().optional(),
};

// ── ka40001: ETF수익율 ──

export const etfReturnRateItemSchema = z
  .object({
    etfprft_rt: s(),
    cntr_prft_rt: s(),
    for_netprps_qty: s(),
    orgn_netprps_qty: s(),
  })
  .passthrough();

export const etfReturnRateResponseSchema = z
  .object({
    ...envelope,
    etfprft_rt_lst: z.array(etfReturnRateItemSchema).default([]),
  })
  .passthrough();

// ── ka40002: ETF종목정보 ──

export const etfItemInfoResponseSchema = z
  .object({
    ...envelope,
    stk_nm: s(),
    etfobjt_idex_nm: s(),
    wonju_pric: s(),
    etftxon_type: s(),
    etntxon_type: s(),
  })
  .passthrough();

// ── ka40003: ETF일별추이 ──

export const etfDailyTrendItemSchema = z
  .object({
    cntr_dt: s(),
    cur_prc: s(),
    pre_sig: s(),
    pred_pre: s(),
    pre_rt: s(),
    trde_qty: s(),
    nav: s(),
    acc_trde_prica: s(),
    navidex_dispty_rt: s(),
    navetfdispty_rt: s(),
    trace_eor_rt: s(),
    trace_cur_prc: s(),
    trace_pred_pre: s(),
    trace_pre_sig: s(),
  })
  .passthrough();

export const etfDailyTrendResponseSchema = z
  .object({
    ...envelope,
    etfdaly_trnsn: z.array(etfDailyTrendItemSchema).default([]),
  })
  .passthrough();

// ── ka40004: ETF전체시세 ──

export const etfFullPriceItemSchema = z
  .object({
    stk_cd: s(),
    stk_cls: s(),
    stk_nm: s(),
    close_pric: s(),
    pre_sig: s(),
    pred_pre: s(),
    pre_rt: s(),
    trde_qty: s(),
    nav: s(),
    trace_eor_rt: s(),
    txbs: s(),
    dvid_bf_base: s(),
    pred_dvida: s(),
    trace_idex_nm: s(),
    drng: s(),
    trace_idex_cd: s(),
    trace_idex: s(),
    trace_flu_rt: s(),
  })
  .passthrough();

export const etfFullPriceResponseSchema = z
  .object({
    ...envelope,
    etfall_mrpr: z.array(etfFullPriceItemSchema).default([]),
  })
  .passthrough();

// ── ka40006: ETF시간대별추이 ──

export const etfHourlyTrendItemSchema = z
  .object({
    tm: s(),
    close_pric: s(),
    pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    trde_qty: s(),
    nav: s(),
    trde_prica: s(),
    navidex: s(),
    navetf: s(),
    trace: s(),
    trace_idex: s(),
    trace_idex_pred_pre: s(),
    trace_idex_pred_pre_sig: s(),
  })
  .passthrough();

export const etfHourlyTrendResponseSchema = z
  .object({
    ...envelope,
    stk_nm: s(),
    etfobjt_idex_nm: s(),
    wonju_pric: s(),
    etftxon_type: s(),
    etntxon_type: s(),
    etftisl_trnsn: z.array(etfHourlyTrendItemSchema).default([]),
  })
  .passthrough();

// ── ka40007: ETF시간대별체결 ──

export const etfHourlyExecutionItemSchema = z
  .object({
    cntr_tm: s(),
    cur_prc: s(),
    pre_sig: s(),
    pred_pre: s(),
    trde_qty: s(),
    stex_tp: s(),
  })
  .passthrough();

export const etfHourlyExecutionResponseSchema = z
  .object({
    ...envelope,
    stk_cls: s(),
    stk_nm: s(),
    etfobjt_idex_nm: s(),
    etfobjt_idex_cd: s(),
    objt_idex_pre_rt: s(),
    wonju_pric: s(),
    etftisl_cntr_array: z.array(etfHourlyExecutionItemSchema).default([]),
  })
  .passthrough();

// ── ka40008: ETF일별체결 ──

export const etfDailyExecutionItemSchema = z
  .object({
    dt: s(),
    cur_prc_n: s(),
    pre_sig_n: s(),
    pred_pre_n: s(),
    acc_trde_qty: s(),
    for_netprps_qty: s(),
    orgn_netprps_qty: s(),
  })
  .passthrough();

export const etfDailyExecutionResponseSchema = z
  .object({
    ...envelope,
    cntr_tm: s(),
    cur_prc: s(),
    pre_sig: s(),
    pred_pre: s(),
    trde_qty: s(),
    etfnetprps_qty_array: z.array(etfDailyExecutionItemSchema).default([]),
  })
  .passthrough();

// ── ka40009: ETF시간대별체결V2 ──

export const etfHourlyExecutionV2ItemSchema = z
  .object({
    nav: s(),
    navpred_pre: s(),
    navflu_rt: s(),
    trace_eor_rt: s(),
    dispty_rt: s(),
    stkcnt: s(),
    base_pric: s(),
    for_rmnd_qty: s(),
    repl_pric: s(),
    conv_pric: s(),
    drstk: s(),
    wonju_pric: s(),
  })
  .passthrough();

export const etfHourlyExecutionV2ResponseSchema = z
  .object({
    ...envelope,
    etfnavarray: z.array(etfHourlyExecutionV2ItemSchema).default([]),
  })
  .passthrough();

// ── ka40010: ETF시간대별추이V2 ──

export const etfHourlyTrendV2ItemSchema = z
  .object({
    cntr_tm: s(),
    cur_prc: s(),
    pre_sig: s(),
    pred_pre: s(),
    trde_qty: s(),
    for_netprps: s(),
  })
  .passthrough();

export const etfHourlyTrendV2ResponseSchema = z
  .object({
    ...envelope,
    etftisl_trnsn: z.array(etfHourlyTrendV2ItemSchema).default([]),
  })
  .passthrough();

// ── Response Types ──

export type EtfReturnRateResponse = CamelizeKeys<z.infer<typeof etfReturnRateResponseSchema>>;
export type EtfItemInfoResponse = CamelizeKeys<z.infer<typeof etfItemInfoResponseSchema>>;
export type EtfDailyTrendResponse = CamelizeKeys<z.infer<typeof etfDailyTrendResponseSchema>>;
export type EtfFullPriceResponse = CamelizeKeys<z.infer<typeof etfFullPriceResponseSchema>>;
export type EtfHourlyTrendResponse = CamelizeKeys<z.infer<typeof etfHourlyTrendResponseSchema>>;
export type EtfHourlyExecutionResponse = CamelizeKeys<z.infer<typeof etfHourlyExecutionResponseSchema>>;
export type EtfDailyExecutionResponse = CamelizeKeys<z.infer<typeof etfDailyExecutionResponseSchema>>;
export type EtfHourlyExecutionV2Response = CamelizeKeys<z.infer<typeof etfHourlyExecutionV2ResponseSchema>>;
export type EtfHourlyTrendV2Response = CamelizeKeys<z.infer<typeof etfHourlyTrendV2ResponseSchema>>;

// ── Response Map ──

export interface DomesticEtfResponseMap {
  getEtfReturnRate: EtfReturnRateResponse;
  getEtfItemInfo: EtfItemInfoResponse;
  getEtfDailyTrend: EtfDailyTrendResponse;
  getEtfFullPrice: EtfFullPriceResponse;
  getEtfHourlyTrend: EtfHourlyTrendResponse;
  getEtfHourlyExecution: EtfHourlyExecutionResponse;
  getEtfDailyExecution: EtfDailyExecutionResponse;
  getEtfHourlyExecutionV2: EtfHourlyExecutionV2Response;
  getEtfHourlyTrendV2: EtfHourlyTrendV2Response;
}
