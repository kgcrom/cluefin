import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types';

const s = () => z.string().default('');

const envelope = {
  return_code: z.union([z.string(), z.number()]).optional(),
  return_msg: z.string().optional(),
};

// ── ka10010: 업종프로그램 ──

export const industryProgramResponseSchema = z
  .object({
    ...envelope,
    dfrt_trst_sell_qty: s(),
    dfrt_trst_sell_amt: s(),
    dfrt_trst_buy_qty: s(),
    dfrt_trst_buy_amt: s(),
    dfrt_trst_netprps_qty: s(),
    dfrt_trst_netprps_amt: s(),
    ndiffpro_trst_sell_qty: s(),
    ndiffpro_trst_sell_amt: s(),
    ndiffpro_trst_buy_qty: s(),
    ndiffpro_trst_buy_amt: s(),
    ndiffpro_trst_netprps_qty: s(),
    ndiffpro_trst_netprps_amt: s(),
    all_dfrt_trst_sell_qty: s(),
    all_dfrt_trst_sell_amt: s(),
    all_dfrt_trst_buy_qty: s(),
    all_dfrt_trst_buy_amt: s(),
    all_dfrt_trst_netprps_qty: s(),
    all_dfrt_trst_netprps_amt: s(),
  })
  .passthrough();

// ── ka10051: 업종투자자순매수 ──

export const industryInvestorNetBuyItemSchema = z
  .object({
    inds_cd: s(),
    inds_nm: s(),
    cur_prc: s(),
    pre_smbol: s(),
    pred_pre: s(),
    flu_rt: s(),
    trde_qty: s(),
    sc_netprps: s(),
    insrnc_netprps: s(),
    invtrt_netprps: s(),
    bank_netprps: s(),
    jnsinkm_netprps: s(),
    endw_netprps: s(),
    etc_corp_netprps: s(),
    ind_netprps: s(),
    frgnr_netprps: s(),
    native_trmt_frgnr_netprps: s(),
    natn_netprps: s(),
    samo_fund_netprps: s(),
    orgn_netprps: s(),
  })
  .passthrough();

export const industryInvestorNetBuyResponseSchema = z
  .object({
    ...envelope,
    inds_netprps: z.array(industryInvestorNetBuyItemSchema).default([]),
  })
  .passthrough();

// ── ka20001: 업종현재가 ──

export const industryCurrentPriceTimeItemSchema = z
  .object({
    tm_n: s(),
    cur_prc_n: s(),
    pred_pre_sig_n: s(),
    pred_pre_n: s(),
    flu_rt_n: s(),
    trde_qty_n: s(),
    acc_trde_qty_n: s(),
  })
  .passthrough();

export const industryCurrentPriceResponseSchema = z
  .object({
    ...envelope,
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    trde_qty: s(),
    trde_prica: s(),
    trde_frmatn_stk_num: s(),
    trde_frmatn_rt: s(),
    open_pric: s(),
    high_pric: s(),
    low_pric: s(),
    upl: s(),
    rising: s(),
    stdns: s(),
    fall: s(),
    lst: s(),
    '52wk_hgst_pric': s(),
    '52wk_hgst_pric_dt': s(),
    '52wk_hgst_pric_pre_rt': s(),
    '52wk_lwst_pric': s(),
    '52wk_lwst_pric_dt': s(),
    '52wk_lwst_pric_pre_rt': s(),
    inds_cur_prc_tm: z.array(industryCurrentPriceTimeItemSchema).default([]),
  })
  .passthrough();

// ── ka20002: 업종별시세 ──

export const industryPriceBySectorItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    now_trde_qty: s(),
    sel_bid: s(),
    buy_bid: s(),
    open_pric: s(),
    high_pric: s(),
    low_pric: s(),
  })
  .passthrough();

export const industryPriceBySectorResponseSchema = z
  .object({
    ...envelope,
    inds_stkpc: z.array(industryPriceBySectorItemSchema).default([]),
  })
  .passthrough();

// ── ka20003: 전업종지수 ──

export const allIndustryIndexItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    trde_qty: s(),
    wght: s(),
    trde_prica: s(),
    upl: s(),
    rising: s(),
    stdns: s(),
    fall: s(),
    lst: s(),
    flo_stk_num: s(),
  })
  .passthrough();

export const allIndustryIndexResponseSchema = z
  .object({
    ...envelope,
    all_inds_idex: z.array(allIndustryIndexItemSchema).default([]),
  })
  .passthrough();

// ── ka20009: 업종현재가일별 ──

export const dailyIndustryCurrentPriceDailyItemSchema = z
  .object({
    dt_n: s(),
    cur_prc_n: s(),
    pred_pre_sig_n: s(),
    pred_pre_n: s(),
    flu_rt_n: s(),
    acc_trde_qty_n: s(),
  })
  .passthrough();

export const dailyIndustryCurrentPriceResponseSchema = z
  .object({
    ...envelope,
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    trde_qty: s(),
    trde_prica: s(),
    trde_frmatn_stk_num: s(),
    trde_frmatn_rt: s(),
    open_pric: s(),
    high_pric: s(),
    low_pric: s(),
    upl: s(),
    rising: s(),
    stdns: s(),
    fall: s(),
    lst: s(),
    '52wk_hgst_pric': s(),
    '52wk_hgst_pric_dt': s(),
    '52wk_hgst_pric_pre_rt': s(),
    '52wk_lwst_pric': s(),
    '52wk_lwst_pric_dt': s(),
    '52wk_lwst_pric_pre_rt': s(),
    inds_cur_prc_daly_rept: z.array(dailyIndustryCurrentPriceDailyItemSchema).default([]),
  })
  .passthrough();

// ── Response Types ──

export type IndustryProgramResponse = CamelizeKeys<z.infer<typeof industryProgramResponseSchema>>;
export type IndustryInvestorNetBuyResponse = CamelizeKeys<z.infer<typeof industryInvestorNetBuyResponseSchema>>;
export type IndustryCurrentPriceResponse = CamelizeKeys<z.infer<typeof industryCurrentPriceResponseSchema>>;
export type IndustryPriceBySectorResponse = CamelizeKeys<z.infer<typeof industryPriceBySectorResponseSchema>>;
export type AllIndustryIndexResponse = CamelizeKeys<z.infer<typeof allIndustryIndexResponseSchema>>;
export type DailyIndustryCurrentPriceResponse = CamelizeKeys<z.infer<typeof dailyIndustryCurrentPriceResponseSchema>>;

// ── Response Map ──

export interface DomesticSectorResponseMap {
  getIndustryProgram: IndustryProgramResponse;
  getIndustryInvestorNetBuy: IndustryInvestorNetBuyResponse;
  getIndustryCurrentPrice: IndustryCurrentPriceResponse;
  getIndustryPriceBySector: IndustryPriceBySectorResponse;
  getAllIndustryIndex: AllIndustryIndexResponse;
  getDailyIndustryCurrentPrice: DailyIndustryCurrentPriceResponse;
}
