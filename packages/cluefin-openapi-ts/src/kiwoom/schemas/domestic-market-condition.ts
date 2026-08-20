import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types';

const s = () => z.string().default('');

const envelope = {
  return_code: z.union([z.string(), z.number()]).optional(),
  return_msg: z.string().optional(),
};

// ── ka10004: 주식호가 ──

export const stockQuoteResponseSchema = z
  .object({
    ...envelope,
    bid_req_base_tm: s(),
    sel_10th_pre_req_pre: s(),
    sel_10th_pre_req: s(),
    sel_10th_pre_bid: s(),
    sel_9th_pre_req_pre: s(),
    sel_9th_pre_req: s(),
    sel_9th_pre_bid: s(),
    sel_8th_pre_req_pre: s(),
    sel_8th_pre_req: s(),
    sel_8th_pre_bid: s(),
    sel_7th_pre_req_pre: s(),
    sel_7th_pre_req: s(),
    sel_7th_pre_bid: s(),
    sel_6th_pre_req_pre: s(),
    sel_6th_pre_req: s(),
    sel_6th_pre_bid: s(),
    sel_5th_pre_req_pre: s(),
    sel_5th_pre_req: s(),
    sel_5th_pre_bid: s(),
    sel_4th_pre_req_pre: s(),
    sel_4th_pre_req: s(),
    sel_4th_pre_bid: s(),
    sel_3th_pre_req_pre: s(),
    sel_3th_pre_req: s(),
    sel_3th_pre_bid: s(),
    sel_2th_pre_req_pre: s(),
    sel_2th_pre_req: s(),
    sel_2th_pre_bid: s(),
    sel_1th_pre_req_pre: s(),
    sel_fpr_req: s(),
    sel_fpr_bid: s(),
    buy_fpr_bid: s(),
    buy_fpr_req: s(),
    buy_1th_pre_req_pre: s(),
    buy_2th_pre_bid: s(),
    buy_2th_pre_req: s(),
    buy_2th_pre_req_pre: s(),
    buy_3th_pre_bid: s(),
    buy_3th_pre_req: s(),
    buy_3th_pre_req_pre: s(),
    buy_4th_pre_bid: s(),
    buy_4th_pre_req: s(),
    buy_4th_pre_req_pre: s(),
    buy_5th_pre_bid: s(),
    buy_5th_pre_req: s(),
    buy_5th_pre_req_pre: s(),
    buy_6th_pre_bid: s(),
    buy_6th_pre_req: s(),
    buy_6th_pre_req_pre: s(),
    buy_7th_pre_bid: s(),
    buy_7th_pre_req: s(),
    buy_7th_pre_req_pre: s(),
    buy_8th_pre_bid: s(),
    buy_8th_pre_req: s(),
    buy_8th_pre_req_pre: s(),
    buy_9th_pre_bid: s(),
    buy_9th_pre_req: s(),
    buy_9th_pre_req_pre: s(),
    buy_10th_pre_bid: s(),
    buy_10th_pre_req: s(),
    buy_10th_pre_req_pre: s(),
    tot_sel_req_jub_pre: s(),
    tot_sel_req: s(),
    tot_buy_req: s(),
    tot_buy_req_jub_pre: s(),
    ovt_sel_req_pre: s(),
    ovt_sel_req: s(),
    ovt_buy_req: s(),
    ovt_buy_req_pre: s(),
  })
  .passthrough();

// ── ka10005: 주식일별시세 ──

export const stockQuoteByDateItemSchema = z
  .object({
    date: s(),
    open_pric: s(),
    high_pric: s(),
    low_pric: s(),
    close_pric: s(),
    pre: s(),
    flu_rt: s(),
    trde_qty: s(),
    trde_prica: s(),
    for_poss: s(),
    for_wght: s(),
    for_netprps: s(),
    orgn_netprps: s(),
    ind_netprps: s(),
    crd_remn_rt: s(),
    frgn: s(),
    prm: s(),
  })
  .passthrough();

export const stockQuoteByDateResponseSchema = z
  .object({
    ...envelope,
    stk_ddwkmm: z.array(stockQuoteByDateItemSchema).default([]),
  })
  .passthrough();

// ── ka10006: 주식현재가 ──

export const stockPriceResponseSchema = z
  .object({
    ...envelope,
    date: s(),
    open_pric: s(),
    high_pric: s(),
    low_pric: s(),
    close_pric: s(),
    pre: s(),
    flu_rt: s(),
    trde_qty: s(),
    trde_prica: s(),
    cntr_str: s(),
  })
  .passthrough();

// ── ka10007: 시장투심정보 ──

export const marketSentimentInfoResponseSchema = z
  .object({
    ...envelope,
    stk_nm: s(),
    stk_cd: s(),
    date: s(),
    tm: s(),
    pred_close_pric: s(),
    pred_trde_qty: s(),
    upl_pric: s(),
    lst_pric: s(),
    pred_trde_prica: s(),
    flo_stkcnt: s(),
    cur_prc: s(),
    smbol: s(),
    flu_rt: s(),
    pred_rt: s(),
    open_pric: s(),
    high_pric: s(),
    low_pric: s(),
    cntr_qty: s(),
    trde_qty: s(),
    trde_prica: s(),
    exp_cntr_pric: s(),
    exp_cntr_qty: s(),
    exp_sel_pri_bid: s(),
    exp_buy_pri_bid: s(),
    trde_strt_dt: s(),
    exec_pric: s(),
    hgst_pric: s(),
    lwst_pric: s(),
    hgst_pric_dt: s(),
    lwst_pric_dt: s(),
    sel_1bid: s(),
    sel_2bid: s(),
    sel_3bid: s(),
    sel_4bid: s(),
    sel_5bid: s(),
    sel_6bid: s(),
    sel_7bid: s(),
    sel_8bid: s(),
    sel_9bid: s(),
    sel_10bid: s(),
    buy_1bid: s(),
    buy_2bid: s(),
    buy_3bid: s(),
    buy_4bid: s(),
    buy_5bid: s(),
    buy_6bid: s(),
    buy_7bid: s(),
    buy_8bid: s(),
    buy_9bid: s(),
    buy_10bid: s(),
    sel_1bid_req: s(),
    sel_2bid_req: s(),
    sel_3bid_req: s(),
    sel_4bid_req: s(),
    sel_5bid_req: s(),
    sel_6bid_req: s(),
    sel_7bid_req: s(),
    sel_8bid_req: s(),
    sel_9bid_req: s(),
    sel_10bid_req: s(),
    buy_1bid_req: s(),
    buy_2bid_req: s(),
    buy_3bid_req: s(),
    buy_4bid_req: s(),
    buy_5bid_req: s(),
    buy_6bid_req: s(),
    buy_7bid_req: s(),
    buy_8bid_req: s(),
    buy_9bid_req: s(),
    buy_10bid_req: s(),
    sel_1bid_jub_pre: s(),
    sel_2bid_jub_pre: s(),
    sel_3bid_jub_pre: s(),
    sel_4bid_jub_pre: s(),
    sel_5bid_jub_pre: s(),
    sel_6bid_jub_pre: s(),
    sel_7bid_jub_pre: s(),
    sel_8bid_jub_pre: s(),
    sel_9bid_jub_pre: s(),
    sel_10bid_jub_pre: s(),
    buy_1bid_jub_pre: s(),
    buy_2bid_jub_pre: s(),
    buy_3bid_jub_pre: s(),
    buy_4bid_jub_pre: s(),
    buy_5bid_jub_pre: s(),
    buy_6bid_jub_pre: s(),
    buy_7bid_jub_pre: s(),
    buy_8bid_jub_pre: s(),
    buy_9bid_jub_pre: s(),
    buy_10bid_jub_pre: s(),
    sel_1bid_cnt: s(),
    sel_2bid_cnt: s(),
    sel_3bid_cnt: s(),
    sel_4bid_cnt: s(),
    sel_5bid_cnt: s(),
    buy_1bid_cnt: s(),
    buy_2bid_cnt: s(),
    buy_3bid_cnt: s(),
    buy_4bid_cnt: s(),
    buy_5bid_cnt: s(),
    lpsel_1bid_req: s(),
    lpsel_2bid_req: s(),
    lpsel_3bid_req: s(),
    lpsel_4bid_req: s(),
    lpsel_5bid_req: s(),
    lpsel_6bid_req: s(),
    lpsel_7bid_req: s(),
    lpsel_8bid_req: s(),
    lpsel_9bid_req: s(),
    lpsel_10bid_req: s(),
    lpbuy_1bid_req: s(),
    lpbuy_2bid_req: s(),
    lpbuy_3bid_req: s(),
    lpbuy_4bid_req: s(),
    lpbuy_5bid_req: s(),
    lpbuy_6bid_req: s(),
    lpbuy_7bid_req: s(),
    lpbuy_8bid_req: s(),
    lpbuy_9bid_req: s(),
    lpbuy_10bid_req: s(),
    tot_buy_req: s(),
    tot_sel_req: s(),
    tot_buy_cnt: s(),
    tot_sel_cnt: s(),
  })
  .passthrough();

// ── ka10011: 신주인수권시세 ──

export const newStockWarrantPriceItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    fpr_sel_bid: s(),
    fpr_buy_bid: s(),
    acc_trde_qty: s(),
    open_pric: s(),
    high_pric: s(),
    low_pric: s(),
  })
  .passthrough();

export const newStockWarrantPriceResponseSchema = z
  .object({
    ...envelope,
    newstk_recvrht_mrpr: z.array(newStockWarrantPriceItemSchema).default([]),
  })
  .passthrough();

// ── ka10044: 일별기관매매종목 ──

export const dailyInstitutionalTradingItemsItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    netprps_qty: s(),
    netprps_amt: s(),
    // 아래 4개는 공식 문서에 없지만 실서버가 반환함 (2026-08 실측)
    prsm_avg_pric: s(),
    cur_prc: s(),
    avg_pric_pre: s(),
    pre_rt: s(),
  })
  .passthrough();

export const dailyInstitutionalTradingItemsResponseSchema = z
  .object({
    ...envelope,
    daly_orgn_trde_stk: z.array(dailyInstitutionalTradingItemsItemSchema).default([]),
  })
  .passthrough();

// ── ka10045: 종목별기관매매추이 ──

export const institutionalTradingTrendByStockItemSchema = z
  .object({
    dt: s(),
    close_pric: s(),
    pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    trde_qty: s(),
    orgn_dt_acc: s(),
    orgn_daly_nettrde_qty: s(),
    for_dt_acc: s(),
    for_daly_nettrde_qty: s(),
    limit_exh_rt: s(),
  })
  .passthrough();

export const institutionalTradingTrendByStockResponseSchema = z
  .object({
    ...envelope,
    orgn_prsm_avg_pric: s(),
    for_prsm_avg_pric: s(),
    stk_orgn_trde_trnsn: z.array(institutionalTradingTrendByStockItemSchema).default([]),
  })
  .passthrough();

// ── ka10046: 시간별체결강도추이 ──

export const executionIntensityTrendByTimeItemSchema = z
  .object({
    cntr_tm: s(),
    cur_prc: s(),
    pred_pre: s(),
    pred_pre_sig: s(),
    flu_rt: s(),
    trde_qty: s(),
    acc_trde_prica: s(),
    acc_trde_qty: s(),
    cntr_str: s(),
    cntr_str_5min: s(),
    cntr_str_20min: s(),
    cntr_str_60min: s(),
    stex_tp: s(),
  })
  .passthrough();

export const executionIntensityTrendByTimeResponseSchema = z
  .object({
    ...envelope,
    cntr_str_tm: z.array(executionIntensityTrendByTimeItemSchema).default([]),
  })
  .passthrough();

// ── ka10047: 일별체결강도추이 ──

export const executionIntensityTrendByDateItemSchema = z
  .object({
    dt: s(),
    cur_prc: s(),
    pred_pre: s(),
    pred_pre_sig: s(),
    flu_rt: s(),
    trde_qty: s(),
    acc_trde_prica: s(),
    acc_trde_qty: s(),
    cntr_str: s(),
    cntr_str_5min: s(),
    cntr_str_20min: s(),
    cntr_str_60min: s(),
  })
  .passthrough();

export const executionIntensityTrendByDateResponseSchema = z
  .object({
    ...envelope,
    cntr_str_daly: z.array(executionIntensityTrendByDateItemSchema).default([]),
  })
  .passthrough();

// ── ka10063: 장중투자자매매동향 ──

export const intradayTradingByInvestorItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    acc_trde_qty: s(),
    netprps_amt: s(),
    prev_netprps_amt: s(),
    buy_amt: s(),
    netprps_amt_irds: s(),
    buy_amt_irds: s(),
    sell_amt: s(),
    sell_amt_irds: s(),
    netprps_qty: s(),
    prev_pot_netprps_qty: s(),
    netprps_irds: s(),
    buy_qty: s(),
    buy_qty_irds: s(),
    sell_qty: s(),
    sell_qty_irds: s(),
  })
  .passthrough();

export const intradayTradingByInvestorResponseSchema = z
  .object({
    ...envelope,
    opmr_invsr_trde: z.array(intradayTradingByInvestorItemSchema).default([]),
  })
  .passthrough();

// ── ka10066: 장마감후투자자매매동향 ──

export const afterMarketTradingByInvestorItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    trde_qty: s(),
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
  })
  .passthrough();

export const afterMarketTradingByInvestorResponseSchema = z
  .object({
    ...envelope,
    opaf_invsr_trde: z.array(afterMarketTradingByInvestorItemSchema).default([]),
  })
  .passthrough();

// ── ka10078: 증권사별종목매매추이 ──

export const securitiesFirmTradingTrendByStockItemSchema = z
  .object({
    dt: s(),
    cur_prc: s(),
    pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    acc_trde_qty: s(),
    netprps_qty: s(),
    buy_qty: s(),
    sell_qty: s(),
  })
  .passthrough();

export const securitiesFirmTradingTrendByStockResponseSchema = z
  .object({
    ...envelope,
    sec_stk_trde_trend: z.array(securitiesFirmTradingTrendByStockItemSchema).default([]),
  })
  .passthrough();

// ── ka10086: 일별주가 ──

export const dailyStockPriceItemSchema = z
  .object({
    date: s(),
    open_pric: s(),
    high_pric: s(),
    low_pric: s(),
    close_pric: s(),
    pred_rt: s(),
    flu_rt: s(),
    trde_qty: s(),
    amt_mn: s(),
    crd_rt: s(),
    ind: s(),
    orgn: s(),
    for_qty: s(),
    frgn: s(),
    prm: s(),
    for_rt: s(),
    for_poss: s(),
    for_wght: s(),
    for_netprps: s(),
    orgn_netprps: s(),
    ind_netprps: s(),
    crd_remn_rt: s(),
  })
  .passthrough();

export const dailyStockPriceResponseSchema = z
  .object({
    ...envelope,
    daly_stkpc: z.array(dailyStockPriceItemSchema).default([]),
  })
  .passthrough();

// ── ka10087: 시간외단일가 ──

export const afterHoursSinglePriceResponseSchema = z
  .object({
    ...envelope,
    bid_req_base_tm: s(),
    ovt_sigpric_sel_bid_jub_pre_5: s(),
    ovt_sigpric_sel_bid_jub_pre_4: s(),
    ovt_sigpric_sel_bid_jub_pre_3: s(),
    ovt_sigpric_sel_bid_jub_pre_2: s(),
    ovt_sigpric_sel_bid_jub_pre_1: s(),
    ovt_sigpric_sel_bid_qty_5: s(),
    ovt_sigpric_sel_bid_qty_4: s(),
    ovt_sigpric_sel_bid_qty_3: s(),
    ovt_sigpric_sel_bid_qty_2: s(),
    ovt_sigpric_sel_bid_qty_1: s(),
    ovt_sigpric_sel_bid_5: s(),
    ovt_sigpric_sel_bid_4: s(),
    ovt_sigpric_sel_bid_3: s(),
    ovt_sigpric_sel_bid_2: s(),
    ovt_sigpric_sel_bid_1: s(),
    ovt_sigpric_buy_bid_1: s(),
    ovt_sigpric_buy_bid_2: s(),
    ovt_sigpric_buy_bid_3: s(),
    ovt_sigpric_buy_bid_4: s(),
    ovt_sigpric_buy_bid_5: s(),
    ovt_sigpric_buy_bid_qty_1: s(),
    ovt_sigpric_buy_bid_qty_2: s(),
    ovt_sigpric_buy_bid_qty_3: s(),
    ovt_sigpric_buy_bid_qty_4: s(),
    ovt_sigpric_buy_bid_qty_5: s(),
    ovt_sigpric_buy_bid_jub_pre_1: s(),
    ovt_sigpric_buy_bid_jub_pre_2: s(),
    ovt_sigpric_buy_bid_jub_pre_3: s(),
    ovt_sigpric_buy_bid_jub_pre_4: s(),
    ovt_sigpric_buy_bid_jub_pre_5: s(),
    ovt_sigpric_sel_bid_tot_req: s(),
    ovt_sigpric_buy_bid_tot_req: s(),
    sel_bid_tot_req_jub_pre: s(),
    sel_bid_tot_req: s(),
    buy_bid_tot_req: s(),
    buy_bid_tot_req_jub_pre: s(),
    ovt_sel_bid_tot_req_jub_pre: s(),
    ovt_sel_bid_tot_req: s(),
    ovt_buy_bid_tot_req: s(),
    ovt_buy_bid_tot_req_jub_pre: s(),
    ovt_sigpric_cur_prc: s(),
    ovt_sigpric_pred_pre_sig: s(),
    ovt_sigpric_pred_pre: s(),
    ovt_sigpric_flu_rt: s(),
    ovt_sigpric_acc_trde_qty: s(),
  })
  .passthrough();

// ── ka90005/ka90010: 프로그램매매추이(시간별/일별) ──

export const programTradingTrendItemSchema = z
  .object({
    cntr_tm: s(),
    dfrt_trde_sel: s(),
    dfrt_trde_buy: s(),
    dfrt_trde_netprps: s(),
    ndiffpro_trde_sel: s(),
    ndiffpro_trde_buy: s(),
    ndiffpro_trde_netprps: s(),
    dfrt_trde_sell_qty: s(),
    dfrt_trde_buy_qty: s(),
    dfrt_trde_netprps_qty: s(),
    ndiffpro_trde_sell_qty: s(),
    ndiffpro_trde_buy_qty: s(),
    ndiffpro_trde_netprps_qty: s(),
    all_sel: s(),
    all_buy: s(),
    all_netprps: s(),
    kospi200: s(),
    basis: s(),
  })
  .passthrough();

export const programTradingTrendByTimeResponseSchema = z
  .object({
    ...envelope,
    prm_trde_trnsn: z.array(programTradingTrendItemSchema).default([]),
  })
  .passthrough();

export const programTradingTrendByDateResponseSchema = z
  .object({
    ...envelope,
    prm_trde_trnsn: z.array(programTradingTrendItemSchema).default([]),
  })
  .passthrough();

// ── ka90006: 프로그램매매차익잔고추이 ──

export const programTradingArbitrageBalanceTrendItemSchema = z
  .object({
    dt: s(),
    buy_dfrt_trde_qty: s(),
    buy_dfrt_trde_amt: s(),
    buy_dfrt_trde_irds_amt: s(),
    sel_dfrt_trde_qty: s(),
    sel_dfrt_trde_amt: s(),
    sel_dfrt_trde_irds_amt: s(),
  })
  .passthrough();

export const programTradingArbitrageBalanceTrendResponseSchema = z
  .object({
    ...envelope,
    prm_trde_dfrt_remn_trnsn: z.array(programTradingArbitrageBalanceTrendItemSchema).default([]),
  })
  .passthrough();

// ── ka90007: 프로그램매매누적추이 ──

export const programTradingCumulativeTrendItemSchema = z
  .object({
    dt: s(),
    kospi200: s(),
    basis: s(),
    dfrt_trde_tdy: s(),
    dfrt_trde_acc: s(),
    ndiffpro_trde_tdy: s(),
    ndiffpro_trde_acc: s(),
    all_tdy: s(),
    all_acc: s(),
  })
  .passthrough();

export const programTradingCumulativeTrendResponseSchema = z
  .object({
    ...envelope,
    prm_trde_acc_trnsn: z.array(programTradingCumulativeTrendItemSchema).default([]),
  })
  .passthrough();

// ── ka90008: 종목별시간별프로그램매매추이 ──

export const programTradingTrendByStockAndTimeItemSchema = z
  .object({
    tm: s(),
    cur_prc: s(),
    pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    trde_qty: s(),
    prm_sell_amt: s(),
    prm_buy_amt: s(),
    prm_netprps_amt: s(),
    prm_netprps_amt_irds: s(),
    prm_sell_qty: s(),
    prm_buy_qty: s(),
    prm_netprps_qty: s(),
    prm_netprps_qty_irds: s(),
    base_pric_tm: s(),
    dbrt_trde_rpy_sum: s(),
    remn_rcvord_sum: s(),
    stex_tp: s(),
  })
  .passthrough();

export const programTradingTrendByStockAndTimeResponseSchema = z
  .object({
    ...envelope,
    stk_tm_prm_trde_trnsn: z.array(programTradingTrendByStockAndTimeItemSchema).default([]),
  })
  .passthrough();

// ── ka90013: 종목별일별프로그램매매추이 ──

export const programTradingTrendByStockAndDateItemSchema = z
  .object({
    dt: s(),
    cur_prc: s(),
    pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    trde_qty: s(),
    prm_sell_amt: s(),
    prm_buy_amt: s(),
    prm_netprps_amt: s(),
    prm_netprps_amt_irds: s(),
    prm_sell_qty: s(),
    prm_buy_qty: s(),
    prm_netprps_qty: s(),
    prm_netprps_qty_irds: s(),
    base_pric_tm: s(),
    dbrt_trde_rpy_sum: s(),
    remn_rcvord_sum: s(),
    stex_tp: s(),
  })
  .passthrough();

export const programTradingTrendByStockAndDateResponseSchema = z
  .object({
    ...envelope,
    stk_daly_prm_trde_trnsn: z.array(programTradingTrendByStockAndDateItemSchema).default([]),
  })
  .passthrough();

// ── Response Types ──

export type StockQuoteResponse = CamelizeKeys<z.infer<typeof stockQuoteResponseSchema>>;
export type StockQuoteByDateResponse = CamelizeKeys<z.infer<typeof stockQuoteByDateResponseSchema>>;
export type StockPriceResponse = CamelizeKeys<z.infer<typeof stockPriceResponseSchema>>;
export type MarketSentimentInfoResponse = CamelizeKeys<z.infer<typeof marketSentimentInfoResponseSchema>>;
export type NewStockWarrantPriceResponse = CamelizeKeys<z.infer<typeof newStockWarrantPriceResponseSchema>>;
export type DailyInstitutionalTradingItemsResponse = CamelizeKeys<
  z.infer<typeof dailyInstitutionalTradingItemsResponseSchema>
>;
export type InstitutionalTradingTrendByStockResponse = CamelizeKeys<
  z.infer<typeof institutionalTradingTrendByStockResponseSchema>
>;
export type ExecutionIntensityTrendByTimeResponse = CamelizeKeys<
  z.infer<typeof executionIntensityTrendByTimeResponseSchema>
>;
export type ExecutionIntensityTrendByDateResponse = CamelizeKeys<
  z.infer<typeof executionIntensityTrendByDateResponseSchema>
>;
export type IntradayTradingByInvestorResponse = CamelizeKeys<z.infer<typeof intradayTradingByInvestorResponseSchema>>;
export type AfterMarketTradingByInvestorResponse = CamelizeKeys<
  z.infer<typeof afterMarketTradingByInvestorResponseSchema>
>;
export type SecuritiesFirmTradingTrendByStockResponse = CamelizeKeys<
  z.infer<typeof securitiesFirmTradingTrendByStockResponseSchema>
>;
export type DailyStockPriceResponse = CamelizeKeys<z.infer<typeof dailyStockPriceResponseSchema>>;
export type AfterHoursSinglePriceResponse = CamelizeKeys<z.infer<typeof afterHoursSinglePriceResponseSchema>>;
export type ProgramTradingTrendByTimeResponse = CamelizeKeys<z.infer<typeof programTradingTrendByTimeResponseSchema>>;
export type ProgramTradingArbitrageBalanceTrendResponse = CamelizeKeys<
  z.infer<typeof programTradingArbitrageBalanceTrendResponseSchema>
>;
export type ProgramTradingCumulativeTrendResponse = CamelizeKeys<
  z.infer<typeof programTradingCumulativeTrendResponseSchema>
>;
export type ProgramTradingTrendByStockAndTimeResponse = CamelizeKeys<
  z.infer<typeof programTradingTrendByStockAndTimeResponseSchema>
>;
export type ProgramTradingTrendByDateResponse = CamelizeKeys<z.infer<typeof programTradingTrendByDateResponseSchema>>;
export type ProgramTradingTrendByStockAndDateResponse = CamelizeKeys<
  z.infer<typeof programTradingTrendByStockAndDateResponseSchema>
>;
// ── Response Map ──

export interface DomesticMarketConditionResponseMap {
  getStockQuote: StockQuoteResponse;
  getStockQuoteByDate: StockQuoteByDateResponse;
  getStockPrice: StockPriceResponse;
  getMarketSentimentInfo: MarketSentimentInfoResponse;
  getNewStockWarrantPrice: NewStockWarrantPriceResponse;
  getDailyInstitutionalTradingItems: DailyInstitutionalTradingItemsResponse;
  getInstitutionalTradingTrendByStock: InstitutionalTradingTrendByStockResponse;
  getExecutionIntensityTrendByTime: ExecutionIntensityTrendByTimeResponse;
  getExecutionIntensityTrendByDate: ExecutionIntensityTrendByDateResponse;
  getIntradayTradingByInvestor: IntradayTradingByInvestorResponse;
  getAfterMarketTradingByInvestor: AfterMarketTradingByInvestorResponse;
  getSecuritiesFirmTradingTrendByStock: SecuritiesFirmTradingTrendByStockResponse;
  getDailyStockPrice: DailyStockPriceResponse;
  getAfterHoursSinglePrice: AfterHoursSinglePriceResponse;
  getProgramTradingTrendByTime: ProgramTradingTrendByTimeResponse;
  getProgramTradingArbitrageBalanceTrend: ProgramTradingArbitrageBalanceTrendResponse;
  getProgramTradingCumulativeTrend: ProgramTradingCumulativeTrendResponse;
  getProgramTradingTrendByStockAndTime: ProgramTradingTrendByStockAndTimeResponse;
  getProgramTradingTrendByDate: ProgramTradingTrendByDateResponse;
  getProgramTradingTrendByStockAndDate: ProgramTradingTrendByStockAndDateResponse;
}
