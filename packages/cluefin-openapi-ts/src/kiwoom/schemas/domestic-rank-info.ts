import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types';

const s = () => z.string().default('');

const envelope = {
  return_code: z.union([z.string(), z.number()]).optional(),
  return_msg: z.string().optional(),
};

// ── ka10020: 호가잔량상위 ──

export const topRemainingOrderQuantityItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    trde_qty: s(),
    tot_sel_req: s(),
    tot_buy_req: s(),
    netprps_req: s(),
    buy_rt: s(),
  })
  .passthrough();

export const topRemainingOrderQuantityResponseSchema = z
  .object({
    ...envelope,
    bid_req_upper: z.array(topRemainingOrderQuantityItemSchema).default([]),
  })
  .passthrough();

// ── ka10021: 호가잔량급증 ──

export const rapidlyIncreasingRemainingOrderQuantityItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    int: s(),
    now: s(),
    sdnin_qty: s(),
    sdnin_rt: s(),
    tot_buy_qty: s(),
  })
  .passthrough();

export const rapidlyIncreasingRemainingOrderQuantityResponseSchema = z
  .object({
    ...envelope,
    bid_req_sdnin: z.array(rapidlyIncreasingRemainingOrderQuantityItemSchema).default([]),
  })
  .passthrough();

// ── ka10022: 잔량율급증 ──

export const rapidlyIncreasingTotalSellOrdersItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    int: s(),
    now_rt: s(),
    sdnin_rt: s(),
    tot_sel_req: s(),
    tot_buy_req: s(),
  })
  .passthrough();

export const rapidlyIncreasingTotalSellOrdersResponseSchema = z
  .object({
    ...envelope,
    req_rt_sdnin: z.array(rapidlyIncreasingTotalSellOrdersItemSchema).default([]),
  })
  .passthrough();

// ── ka10023: 거래량급증 ──

export const rapidlyIncreasingTradingVolumeItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    prev_trde_qty: s(),
    now_trde_qty: s(),
    sdnin_qty: s(),
    sdnin_rt: s(),
  })
  .passthrough();

export const rapidlyIncreasingTradingVolumeResponseSchema = z
  .object({
    ...envelope,
    trde_qty_sdnin: z.array(rapidlyIncreasingTradingVolumeItemSchema).default([]),
  })
  .passthrough();

// ── ka10027: 전일대비상위 ──

export const topPercentageChangeFromPreviousDayItemSchema = z
  .object({
    stk_cls: s(),
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    sel_req: s(),
    buy_req: s(),
    now_trde_qty: s(),
    cntr_str: s(),
    cnt: s(),
  })
  .passthrough();

export const topPercentageChangeFromPreviousDayResponseSchema = z
  .object({
    ...envelope,
    pred_pre_flu_rt_upper: z.array(topPercentageChangeFromPreviousDayItemSchema).default([]),
  })
  .passthrough();

// ── ka10029: 예상체결률상위 ──

export const topExpectedConclusionPercentageChangeItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    exp_cntr_pric: s(),
    base_pric: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    exp_cntr_qty: s(),
    sel_req: s(),
    sel_bid: s(),
    buy_bid: s(),
    buy_req: s(),
  })
  .passthrough();

export const topExpectedConclusionPercentageChangeResponseSchema = z
  .object({
    ...envelope,
    exp_cntr_flu_rt_upper: z.array(topExpectedConclusionPercentageChangeItemSchema).default([]),
  })
  .passthrough();

// ── ka10030: 당일거래량상위 ──

export const topCurrentDayTradingVolumeItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    trde_qty: s(),
    pred_rt: s(),
    trde_tern_rt: s(),
    trde_amt: s(),
    opmr_trde_qty: s(),
    opmr_pred_rt: s(),
    opmr_trde_rt: s(),
    opmr_trde_amt: s(),
    af_mkrt_trde_qty: s(),
    af_mkrt_pred_rt: s(),
    af_mkrt_trde_rt: s(),
    af_mkrt_trde_amt: s(),
    bf_mkrt_trde_qty: s(),
    bf_mkrt_pred_rt: s(),
    bf_mkrt_trde_rt: s(),
    bf_mkrt_trde_amt: s(),
  })
  .passthrough();

export const topCurrentDayTradingVolumeResponseSchema = z
  .object({
    ...envelope,
    tdy_trde_qty_upper: z.array(topCurrentDayTradingVolumeItemSchema).default([]),
  })
  .passthrough();

// ── ka10031: 전일거래량상위 ──

export const topPreviousDayTradingVolumeItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    trde_qty: s(),
  })
  .passthrough();

export const topPreviousDayTradingVolumeResponseSchema = z
  .object({
    ...envelope,
    pred_trde_qty_upper: z.array(topPreviousDayTradingVolumeItemSchema).default([]),
  })
  .passthrough();

// ── ka10032: 거래대금상위 ──

export const topTransactionValueItemSchema = z
  .object({
    stk_cd: s(),
    now_rank: s(),
    pred_rank: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    sel_bid: s(),
    buy_bid: s(),
    now_trde_qty: s(),
    pred_trde_qty: s(),
    trde_prica: s(),
  })
  .passthrough();

export const topTransactionValueResponseSchema = z
  .object({
    ...envelope,
    trde_prica_upper: z.array(topTransactionValueItemSchema).default([]),
  })
  .passthrough();

// ── ka10033: 신용비율상위 ──

export const topMarginRatioItemSchema = z
  .object({
    stk_infr: s(),
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    crd_rt: s(),
    sel_req: s(),
    buy_req: s(),
    now_trde_qty: s(),
  })
  .passthrough();

export const topMarginRatioResponseSchema = z
  .object({
    ...envelope,
    crd_rt_upper: z.array(topMarginRatioItemSchema).default([]),
  })
  .passthrough();

// ── ka10034: 외인기간별매매상위 ──

export const topForeignerPeriodTradingItemSchema = z
  .object({
    rank: s(),
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    sel_bid: s(),
    buy_bid: s(),
    trde_qty: s(),
    netprps_qty: s(),
    gain_pos_stkcnt: s(),
  })
  .passthrough();

export const topForeignerPeriodTradingResponseSchema = z
  .object({
    ...envelope,
    for_dt_trde_upper: z.array(topForeignerPeriodTradingItemSchema).default([]),
  })
  .passthrough();

// ── ka10035: 외인연속순매수매도상위 ──

export const topConsecutiveNetBuySellByForeignersItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    dm1: s(),
    dm2: s(),
    dm3: s(),
    tot: s(),
    limit_exh_rt: s(),
    pred_pre_1: s(),
    pred_pre_2: s(),
    pred_pre_3: s(),
  })
  .passthrough();

export const topConsecutiveNetBuySellByForeignersResponseSchema = z
  .object({
    ...envelope,
    for_cont_nettrde_upper: z.array(topConsecutiveNetBuySellByForeignersItemSchema).default([]),
  })
  .passthrough();

// ── ka10036: 외인한도소진율상위 ──

export const topLimitExhaustionRateForeignerItemSchema = z
  .object({
    rank: s(),
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    trde_qty: s(),
    poss_stkcnt: s(),
    gain_pos_stkcnt: s(),
    base_limit_exh_rt: s(),
    limit_exh_rt: s(),
    exh_rt_incrs: s(),
  })
  .passthrough();

export const topLimitExhaustionRateForeignerResponseSchema = z
  .object({
    ...envelope,
    for_limit_exh_rt_incrs_upper: z.array(topLimitExhaustionRateForeignerItemSchema).default([]),
  })
  .passthrough();

// ── ka10037: 외인계좌그룹별매매상위 ──

export const topForeignAccountGroupTradingItemSchema = z
  .object({
    rank: s(),
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    sel_trde_qty: s(),
    buy_trde_qty: s(),
    netprps_trde_qty: s(),
    netprps_prica: s(),
    trde_qty: s(),
    trde_prica: s(),
  })
  .passthrough();

export const topForeignAccountGroupTradingResponseSchema = z
  .object({
    ...envelope,
    frgn_wicket_trde_upper: z.array(topForeignAccountGroupTradingItemSchema).default([]),
  })
  .passthrough();

// ── ka10038: 종목별증권사순위 ──

export const stockSpecificSecuritiesFirmRankingItemSchema = z
  .object({
    rank: s(),
    mmcm_nm: s(),
    buy_qty: s(),
    sell_qty: s(),
    acc_netprps_qty: s(),
  })
  .passthrough();

export const stockSpecificSecuritiesFirmRankingResponseSchema = z
  .object({
    ...envelope,
    rank_1: s(),
    rank_2: s(),
    rank_3: s(),
    prid_trde_qty: s(),
    stk_sec_rank: z.array(stockSpecificSecuritiesFirmRankingItemSchema).default([]),
  })
  .passthrough();

// ── ka10039: 증권사별매매상위 ──

export const topSecuritiesFirmTradingItemSchema = z
  .object({
    rank: s(),
    stk_cd: s(),
    stk_nm: s(),
    prid_stkpc_flu: s(),
    flu_rt: s(),
    prid_trde_qty: s(),
    netprps: s(),
    buy_trde_qty: s(),
    sel_trde_qty: s(),
  })
  .passthrough();

export const topSecuritiesFirmTradingResponseSchema = z
  .object({
    ...envelope,
    sec_trde_upper: z.array(topSecuritiesFirmTradingItemSchema).default([]),
  })
  .passthrough();

// ── ka10040: 당일주요거래원 ──

export const topCurrentDayMajorTradersItemSchema = z
  .object({
    sel_scesn_tm: s(),
    sell_qty: s(),
    sel_upper_scesn_ori: s(),
    buy_scesn_tm: s(),
    buy_qty: s(),
    buy_upper_scesn_ori: s(),
    qry_dt: s(),
    qry_tm: s(),
  })
  .passthrough();

export const topCurrentDayMajorTradersResponseSchema = z
  .object({
    ...envelope,
    sel_trde_ori_irds_1: s(),
    sel_trde_ori_qty_1: s(),
    sel_trde_ori_1: s(),
    sel_trde_ori_cd_1: s(),
    buy_trde_ori_1: s(),
    buy_trde_ori_cd_1: s(),
    buy_trde_ori_qty_1: s(),
    buy_trde_ori_irds_1: s(),
    sel_trde_ori_irds_2: s(),
    sel_trde_ori_qty_2: s(),
    sel_trde_ori_2: s(),
    sel_trde_ori_cd_2: s(),
    buy_trde_ori_2: s(),
    buy_trde_ori_cd_2: s(),
    buy_trde_ori_qty_2: s(),
    buy_trde_ori_irds_2: s(),
    sel_trde_ori_irds_3: s(),
    sel_trde_ori_qty_3: s(),
    sel_trde_ori_3: s(),
    sel_trde_ori_cd_3: s(),
    buy_trde_ori_3: s(),
    buy_trde_ori_cd_3: s(),
    buy_trde_ori_qty_3: s(),
    buy_trde_ori_irds_3: s(),
    sel_trde_ori_irds_4: s(),
    sel_trde_ori_qty_4: s(),
    sel_trde_ori_4: s(),
    sel_trde_ori_cd_4: s(),
    buy_trde_ori_4: s(),
    buy_trde_ori_cd_4: s(),
    buy_trde_ori_qty_4: s(),
    buy_trde_ori_irds_4: s(),
    sel_trde_ori_irds_5: s(),
    sel_trde_ori_qty_5: s(),
    sel_trde_ori_5: s(),
    sel_trde_ori_cd_5: s(),
    buy_trde_ori_5: s(),
    buy_trde_ori_cd_5: s(),
    buy_trde_ori_qty_5: s(),
    buy_trde_ori_irds_5: s(),
    frgn_sel_prsm_sum_chang: s(),
    frgn_sel_prsm_sum: s(),
    frgn_buy_prsm_sum: s(),
    frgn_buy_prsm_sum_chang: s(),
    tdy_main_trde_ori: z.array(topCurrentDayMajorTradersItemSchema).default([]),
  })
  .passthrough();

// ── ka10042: 순매수거래원순위 ──

export const topNetBuyTraderRankingItemSchema = z
  .object({
    rank: s(),
    mmcm_cd: s(),
    mmcm_nm: s(),
  })
  .passthrough();

export const topNetBuyTraderRankingResponseSchema = z
  .object({
    ...envelope,
    netprps_trde_ori_rank: z.array(topNetBuyTraderRankingItemSchema).default([]),
  })
  .passthrough();

// ── ka10053: 당일상위이탈원천 ──

export const topCurrentDayDeviationSourcesItemSchema = z
  .object({
    sel_scesn_tm: s(),
    sell_qty: s(),
    sel_upper_scesn_ori: s(),
    buy_scesn_tm: s(),
    buy_qty: s(),
    buy_upper_scesn_ori: s(),
    qry_dt: s(),
    qry_tm: s(),
  })
  .passthrough();

export const topCurrentDayDeviationSourcesResponseSchema = z
  .object({
    ...envelope,
    tdy_upper_scesn_ori: z.array(topCurrentDayDeviationSourcesItemSchema).default([]),
  })
  .passthrough();

// ── ka10062: 동일순매매상위 ──

export const sameNetBuySellRankingItemSchema = z
  .object({
    stk_cd: s(),
    rank: s(),
    stk_nm: s(),
    cur_prc: s(),
    pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    acc_trde_qty: s(),
    orgn_nettrde_qty: s(),
    orgn_nettrde_amt: s(),
    orgn_nettrde_avg_pric: s(),
    for_nettrde_qty: s(),
    for_nettrde_amt: s(),
    for_nettrde_avg_pric: s(),
    nettrde_qty: s(),
    nettrde_amt: s(),
  })
  .passthrough();

export const sameNetBuySellRankingResponseSchema = z
  .object({
    ...envelope,
    eql_nettrde_rank: z.array(sameNetBuySellRankingItemSchema).default([]),
  })
  .passthrough();

// ── ka10098: 시간외단일가등락율순위 ──

export const afterHoursSinglePriceChangeRateRankingItemSchema = z
  .object({
    rank: s(),
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    sel_tot_req: s(),
    buy_tot_req: s(),
    acc_trde_qty: s(),
    acc_trde_prica: s(),
    tdy_close_pric: s(),
    tdy_close_pric_flu_rt: s(),
  })
  .passthrough();

export const afterHoursSinglePriceChangeRateRankingResponseSchema = z
  .object({
    ...envelope,
    ovt_sigpric_flu_rt_rank: z.array(afterHoursSinglePriceChangeRateRankingItemSchema).default([]),
  })
  .passthrough();

// ── ka90009: 외국인기관매매상위 ──

export const topForeignerInstitutionTradingItemSchema = z
  .object({
    for_netslmt_stk_cd: s(),
    for_netslmt_stk_nm: s(),
    for_netslmt_amt: s(),
    for_netslmt_qty: s(),
    for_netprps_stk_cd: s(),
    for_netprps_stk_nm: s(),
    for_netprps_amt: s(),
    for_netprps_qty: s(),
    orgn_netslmt_stk_cd: s(),
    orgn_netslmt_stk_nm: s(),
    orgn_netslmt_amt: s(),
    orgn_netslmt_qty: s(),
    orgn_netprps_stk_cd: s(),
    orgn_netprps_stk_nm: s(),
    orgn_netprps_amt: s(),
    orgn_netprps_qty: s(),
    pipe1: s(),
    pipe2: s(),
    pipe3: s(),
  })
  .passthrough();

export const topForeignerInstitutionTradingResponseSchema = z
  .object({
    ...envelope,
    frgnr_orgn_trde_upper: z.array(topForeignerInstitutionTradingItemSchema).default([]),
  })
  .passthrough();

// ── Response Types ──

export type TopRemainingOrderQuantityResponse = CamelizeKeys<z.infer<typeof topRemainingOrderQuantityResponseSchema>>;
export type RapidlyIncreasingRemainingOrderQuantityResponse = CamelizeKeys<
  z.infer<typeof rapidlyIncreasingRemainingOrderQuantityResponseSchema>
>;
export type RapidlyIncreasingTotalSellOrdersResponse = CamelizeKeys<
  z.infer<typeof rapidlyIncreasingTotalSellOrdersResponseSchema>
>;
export type RapidlyIncreasingTradingVolumeResponse = CamelizeKeys<
  z.infer<typeof rapidlyIncreasingTradingVolumeResponseSchema>
>;
export type TopPercentageChangeFromPreviousDayResponse = CamelizeKeys<
  z.infer<typeof topPercentageChangeFromPreviousDayResponseSchema>
>;
export type TopExpectedConclusionPercentageChangeResponse = CamelizeKeys<
  z.infer<typeof topExpectedConclusionPercentageChangeResponseSchema>
>;
export type TopCurrentDayTradingVolumeResponse = CamelizeKeys<z.infer<typeof topCurrentDayTradingVolumeResponseSchema>>;
export type TopPreviousDayTradingVolumeResponse = CamelizeKeys<
  z.infer<typeof topPreviousDayTradingVolumeResponseSchema>
>;
export type TopTransactionValueResponse = CamelizeKeys<z.infer<typeof topTransactionValueResponseSchema>>;
export type TopMarginRatioResponse = CamelizeKeys<z.infer<typeof topMarginRatioResponseSchema>>;
export type TopForeignerPeriodTradingResponse = CamelizeKeys<z.infer<typeof topForeignerPeriodTradingResponseSchema>>;
export type TopConsecutiveNetBuySellByForeignersResponse = CamelizeKeys<
  z.infer<typeof topConsecutiveNetBuySellByForeignersResponseSchema>
>;
export type TopLimitExhaustionRateForeignerResponse = CamelizeKeys<
  z.infer<typeof topLimitExhaustionRateForeignerResponseSchema>
>;
export type TopForeignAccountGroupTradingResponse = CamelizeKeys<
  z.infer<typeof topForeignAccountGroupTradingResponseSchema>
>;
export type StockSpecificSecuritiesFirmRankingResponse = CamelizeKeys<
  z.infer<typeof stockSpecificSecuritiesFirmRankingResponseSchema>
>;
export type TopSecuritiesFirmTradingResponse = CamelizeKeys<z.infer<typeof topSecuritiesFirmTradingResponseSchema>>;
export type TopCurrentDayMajorTradersResponse = CamelizeKeys<z.infer<typeof topCurrentDayMajorTradersResponseSchema>>;
export type TopNetBuyTraderRankingResponse = CamelizeKeys<z.infer<typeof topNetBuyTraderRankingResponseSchema>>;
export type TopCurrentDayDeviationSourcesResponse = CamelizeKeys<
  z.infer<typeof topCurrentDayDeviationSourcesResponseSchema>
>;
export type SameNetBuySellRankingResponse = CamelizeKeys<z.infer<typeof sameNetBuySellRankingResponseSchema>>;
export type AfterHoursSinglePriceChangeRateRankingResponse = CamelizeKeys<
  z.infer<typeof afterHoursSinglePriceChangeRateRankingResponseSchema>
>;
export type TopForeignerInstitutionTradingResponse = CamelizeKeys<
  z.infer<typeof topForeignerInstitutionTradingResponseSchema>
>;

// ── Response Map ──

export interface DomesticRankInfoResponseMap {
  getTopRemainingOrderQuantity: TopRemainingOrderQuantityResponse;
  getRapidlyIncreasingRemainingOrderQuantity: RapidlyIncreasingRemainingOrderQuantityResponse;
  getRapidlyIncreasingTotalSellOrders: RapidlyIncreasingTotalSellOrdersResponse;
  getRapidlyIncreasingTradingVolume: RapidlyIncreasingTradingVolumeResponse;
  getTopPercentageChangeFromPreviousDay: TopPercentageChangeFromPreviousDayResponse;
  getTopExpectedConclusionPercentageChange: TopExpectedConclusionPercentageChangeResponse;
  getTopCurrentDayTradingVolume: TopCurrentDayTradingVolumeResponse;
  getTopPreviousDayTradingVolume: TopPreviousDayTradingVolumeResponse;
  getTopTransactionValue: TopTransactionValueResponse;
  getTopMarginRatio: TopMarginRatioResponse;
  getTopForeignerPeriodTrading: TopForeignerPeriodTradingResponse;
  getTopConsecutiveNetBuySellByForeigners: TopConsecutiveNetBuySellByForeignersResponse;
  getTopLimitExhaustionRateForeigner: TopLimitExhaustionRateForeignerResponse;
  getTopForeignAccountGroupTrading: TopForeignAccountGroupTradingResponse;
  getStockSpecificSecuritiesFirmRanking: StockSpecificSecuritiesFirmRankingResponse;
  getTopSecuritiesFirmTrading: TopSecuritiesFirmTradingResponse;
  getTopCurrentDayMajorTraders: TopCurrentDayMajorTradersResponse;
  getTopNetBuyTraderRanking: TopNetBuyTraderRankingResponse;
  getTopCurrentDayDeviationSources: TopCurrentDayDeviationSourcesResponse;
  getSameNetBuySellRanking: SameNetBuySellRankingResponse;
  getAfterHoursSinglePriceChangeRateRanking: AfterHoursSinglePriceChangeRateRankingResponse;
  getTopForeignerInstitutionTrading: TopForeignerInstitutionTradingResponse;
}
