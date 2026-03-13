import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types';

const s = () => z.string().default('');

const envelope = {
  return_code: z.union([z.string(), z.number()]).optional(),
  return_msg: z.string().optional(),
};

// ── ka10008: 주식외국인종목별매매동향 ──

export const foreignInvestorTradingTrendByStockItemSchema = z
  .object({
    dt: s(),
    close_pric: s(),
    pred_pre: s(),
    trde_qty: s(),
    chg_qty: s(),
    poss_stkcnt: s(),
    wght: s(),
    gain_pos_stkcnt: s(),
    frgnr_limit: s(),
    frgnr_limit_irds: s(),
    limit_exh_rt: s(),
  })
  .passthrough();

export const foreignInvestorTradingTrendByStockResponseSchema = z
  .object({
    ...envelope,
    stk_frgnr: z.array(foreignInvestorTradingTrendByStockItemSchema).default([]),
  })
  .passthrough();

// ── ka10009: 주식기관 ──

export const stockInstitutionResponseSchema = z
  .object({
    ...envelope,
    date: s(),
    close_pric: s(),
    pre: s(),
    orgn_dt_acc: s(),
    orgn_daly_nettrde: s(),
    frgnr_daly_nettrde: s(),
    frgnr_qota_rt: s(),
  })
  .passthrough();

// ── ka10131: 기관외국인연속순매수매도현황 ──

export const consecutiveNetBuySellStatusByInstitutionForeignerItemSchema = z
  .object({
    rank: s(),
    stk_cd: s(),
    stk_nm: s(),
    prid_stkpc_flu_rt: s(),
    orgn_nettrde_amt: s(),
    orgn_nettrde_qty: s(),
    orgn_cont_netprps_dys: s(),
    orgn_cont_netprps_qty: s(),
    orgn_cont_netprps_amt: s(),
    frgnr_nettrde_qty: s(),
    frgnr_nettrde_amt: s(),
    frgnr_cont_netprps_dys: s(),
    frgnr_cont_netprps_qty: s(),
    frgnr_cont_netprps_amt: s(),
    nettrde_qty: s(),
    nettrde_amt: s(),
    tot_cont_netprps_dys: s(),
    tot_cont_nettrde_qty: s(),
    tot_cont_netprps_amt: s(),
  })
  .passthrough();

export const consecutiveNetBuySellStatusByInstitutionForeignerResponseSchema = z
  .object({
    ...envelope,
    orgn_frgnr_cont_trde_prst: z.array(consecutiveNetBuySellStatusByInstitutionForeignerItemSchema).default([]),
  })
  .passthrough();

// ── Response Types ──

export type ForeignInvestorTradingTrendByStockResponse = CamelizeKeys<
  z.infer<typeof foreignInvestorTradingTrendByStockResponseSchema>
>;
export type StockInstitutionResponse = CamelizeKeys<z.infer<typeof stockInstitutionResponseSchema>>;
export type ConsecutiveNetBuySellStatusByInstitutionForeignerResponse = CamelizeKeys<
  z.infer<typeof consecutiveNetBuySellStatusByInstitutionForeignerResponseSchema>
>;

// ── Response Map ──

export interface DomesticForeignResponseMap {
  getForeignInvestorTradingTrendByStock: ForeignInvestorTradingTrendByStockResponse;
  getStockInstitution: StockInstitutionResponse;
  getConsecutiveNetBuySellStatusByInstitutionForeigner: ConsecutiveNetBuySellStatusByInstitutionForeignerResponse;
}
