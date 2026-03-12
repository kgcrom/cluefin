import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types';

const s = () => z.string().default('');

const envelope = {
  return_code: z.union([z.string(), z.number()]).optional(),
  return_msg: z.string().optional(),
};

// ── ka10001: 종목정보 ──

export const stockInfoResponseSchema = z
  .object({
    ...envelope,
    stk_cd: s(),
    stk_nm: s(),
    setl_mm: s(),
    fav: s(),
    cap: s(),
    flo_stk: s(),
    crd_rt: s(),
    oyr_hgst: s(),
    oyr_lwst: s(),
    mac: s(),
    mac_wght: s(),
    for_exh_rt: s(),
    repl_pric: s(),
    per: s(),
    eps: s(),
    roe: s(),
    pbr: s(),
    ev: s(),
    bps: s(),
    sale_amt: s(),
    bus_pro: s(),
    cup_nga: s(),
    '250hgst': s(),
    '250lwst': s(),
    open_pric: s(),
    high_pric: s(),
    low_pric: s(),
    upl_pric: s(),
    lst_pric: s(),
    base_pric: s(),
    exp_cntr_pric: s(),
    exp_cntr_qty: s(),
    '250hgst_pric_dt': s(),
    '250hgst_pric_pre_rt': s(),
    '250lwst_pric_dt': s(),
    '250lwst_pric_pre_rt': s(),
    cur_prc: s(),
    pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    trde_qty: s(),
    trde_pre: s(),
    fav_unit: s(),
    dstr_stk: s(),
    dstr_rt: s(),
  })
  .passthrough();

// ── ka10002: 종목별거래원 ──

export const stockTradingMemberResponseSchema = z
  .object({
    ...envelope,
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    flu_smbol: s(),
    base_pric: s(),
    pred_pre: s(),
    flu_rt: s(),
    sel_trde_ori_nm1: s(),
    sel_trde_ori1: s(),
    sel_trde_qty1: s(),
    buy_trde_ori_nm1: s(),
    buy_trde_ori1: s(),
    buy_trde_qty1: s(),
    sel_trde_ori_nm2: s(),
    sel_trde_ori2: s(),
    sel_trde_qty2: s(),
    buy_trde_ori_nm2: s(),
    buy_trde_ori2: s(),
    buy_trde_qty2: s(),
    sel_trde_ori_nm3: s(),
    sel_trde_ori3: s(),
    sel_trde_qty3: s(),
    buy_trde_ori_nm3: s(),
    buy_trde_ori3: s(),
    buy_trde_qty3: s(),
    sel_trde_ori_nm4: s(),
    sel_trde_ori4: s(),
    sel_trde_qty4: s(),
    buy_trde_ori_nm4: s(),
    buy_trde_ori4: s(),
    buy_trde_qty4: s(),
    sel_trde_ori_nm5: s(),
    sel_trde_ori5: s(),
    sel_trde_qty5: s(),
    buy_trde_ori_nm5: s(),
    buy_trde_ori5: s(),
    buy_trde_qty5: s(),
  })
  .passthrough();

// ── ka10003: 체결정보 ──

export const executionItemSchema = z
  .object({
    tm: s(),
    cur_prc: s(),
    pred_pre: s(),
    pre_rt: s(),
    pri_sel_bid_unit: s(),
    pri_buy_bid_unit: s(),
    cntr_trde_qty: s(),
    sign: s(),
    acc_trde_qty: s(),
    acc_trde_prica: s(),
    cntr_str: s(),
    stex_tp: s(),
  })
  .passthrough();

export const executionResponseSchema = z
  .object({
    ...envelope,
    cntr_infr: z.array(executionItemSchema).default([]),
  })
  .passthrough();

// ── ka10013: 신용거래추이 ──

export const marginTradingTrendItemSchema = z
  .object({
    dt: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    trde_qty: s(),
    new: s(),
    rpya: s(),
    remn: s(),
    amt: s(),
    pre: s(),
    shr_rt: s(),
    remn_rt: s(),
  })
  .passthrough();

export const marginTradingTrendResponseSchema = z
  .object({
    ...envelope,
    crd_trde_trend: z.array(marginTradingTrendItemSchema).default([]),
  })
  .passthrough();

// ── ka10015: 일별거래상세 ──

export const dailyTradingDetailsItemSchema = z
  .object({
    dt: s(),
    close_pric: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    trde_qty: s(),
    trde_prica: s(),
    bf_mkrt_trde_qty: s(),
    bf_mkrt_trde_wght: s(),
    opmr_trde_qty: s(),
    opmr_trde_wght: s(),
    af_mkrt_trde_qty: s(),
    af_mkrt_trde_wght: s(),
    tot3: s(),
    prid_trde_qty: s(),
    cntr_str: s(),
    for_poss: s(),
    for_wght: s(),
    for_netprps: s(),
    orgn_netprps: s(),
    ind_netprps: s(),
    frgn: s(),
    crd_remn_rt: s(),
    prm: s(),
    bf_mkrt_trde_prica: s(),
    bf_mkrt_trde_prica_wght: s(),
    opmr_trde_prica: s(),
    opmr_trde_prica_wght: s(),
    af_mkrt_trde_prica: s(),
    af_mkrt_trde_prica_wght: s(),
  })
  .passthrough();

export const dailyTradingDetailsResponseSchema = z
  .object({
    ...envelope,
    daly_trde_dtl: z.array(dailyTradingDetailsItemSchema).default([]),
  })
  .passthrough();

// ── ka10016: 신고/신저가 ──

export const newHighLowPriceItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    now_trde_qty: s(),
  })
  .passthrough();

export const newHighLowPriceResponseSchema = z
  .object({
    ...envelope,
    ntl_pric: z.array(newHighLowPriceItemSchema).default([]),
  })
  .passthrough();

// ── ka10017: 상/하한가 ──

export const upperLowerLimitPriceItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    now_trde_qty: s(),
  })
  .passthrough();

export const upperLowerLimitPriceResponseSchema = z
  .object({
    ...envelope,
    updown_pric: z.array(upperLowerLimitPriceItemSchema).default([]),
  })
  .passthrough();

// ── ka10018: 고/저가근접 ──

export const highLowPriceApproachItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    now_trde_qty: s(),
  })
  .passthrough();

export const highLowPriceApproachResponseSchema = z
  .object({
    ...envelope,
    high_low_pric_alacc: z.array(highLowPriceApproachItemSchema).default([]),
  })
  .passthrough();

// ── ka10019: 가격급등락 ──

export const priceVolatilityItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    now_trde_qty: s(),
  })
  .passthrough();

export const priceVolatilityResponseSchema = z
  .object({
    ...envelope,
    pric_jmpflu: z.array(priceVolatilityItemSchema).default([]),
  })
  .passthrough();

// ── ka10024: 거래량갱신 ──

export const tradingVolumeRenewalItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    prev_trde_qty: s(),
    now_trde_qty: s(),
    sel_bid: s(),
    buy_bid: s(),
  })
  .passthrough();

export const tradingVolumeRenewalResponseSchema = z
  .object({
    ...envelope,
    trde_qty_updt: z.array(tradingVolumeRenewalItemSchema).default([]),
  })
  .passthrough();

// ── ka10025: 수급집중 ──

export const supplyDemandConcentrationItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    now_trde_qty: s(),
    pric_strt: s(),
    pric_end: s(),
    prps_qty: s(),
    prps_rt: s(),
  })
  .passthrough();

export const supplyDemandConcentrationResponseSchema = z
  .object({
    ...envelope,
    prps_cnctr: z.array(supplyDemandConcentrationItemSchema).default([]),
  })
  .passthrough();

// ── ka10026: 고/저PER ──

export const highPerItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    per: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    now_trde_qty: s(),
    sel_bid: s(),
  })
  .passthrough();

export const highPerResponseSchema = z
  .object({
    ...envelope,
    high_low_per: z.array(highPerItemSchema).default([]),
  })
  .passthrough();

// ── ka10028: 시가대비등락율 ──

export const changeRateFromOpenItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    open_pric: s(),
    high_pric: s(),
    low_pric: s(),
    open_pric_pre: s(),
    now_trde_qty: s(),
    cntr_str: s(),
  })
  .passthrough();

export const changeRateFromOpenResponseSchema = z
  .object({
    ...envelope,
    open_pric_pre_flu_rt: z.array(changeRateFromOpenItemSchema).default([]),
  })
  .passthrough();

// ── ka10043: 거래원수급분석 ──

export const tradingMemberSupplyDemandAnalysisItemSchema = z
  .object({
    dt: s(),
    close_pric: s(),
    pre_sig: s(),
    pred_pre: s(),
    sel_qty: s(),
    buy_qty: s(),
    netprps_qty: s(),
    trde_qty_sum: s(),
    trde_wght: s(),
  })
  .passthrough();

export const tradingMemberSupplyDemandAnalysisResponseSchema = z
  .object({
    ...envelope,
    trde_ori_prps_anly: z.array(tradingMemberSupplyDemandAnalysisItemSchema).default([]),
  })
  .passthrough();

// ── ka10052: 거래원순간체결량 ──

export const tradingMemberInstantVolumeItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    now_trde_qty: s(),
  })
  .passthrough();

export const tradingMemberInstantVolumeResponseSchema = z
  .object({
    ...envelope,
    trde_ori_mont_trde_qty: z.array(tradingMemberInstantVolumeItemSchema).default([]),
  })
  .passthrough();

// ── ka10054: 변동성완화장치 ──

export const volatilityControlEventItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    acc_trde_qty: s(),
    motn_pric: s(),
    dynm_dispty_rt: s(),
    trde_cntr_proc_time: s(),
    virelis_time: s(),
    viaplc_tp: s(),
    dynm_stdpc: s(),
    static_stdpc: s(),
    static_dispty_rt: s(),
    open_pric_pre_flu_rt: s(),
    vimotn_cnt: s(),
    stex_tp: s(),
  })
  .passthrough();

export const volatilityControlEventResponseSchema = z
  .object({
    ...envelope,
    motn_stk: z.array(volatilityControlEventItemSchema).default([]),
  })
  .passthrough();

// ── ka10055: 당일전일체결량 ──

export const dailyPreviousDayExecutionVolumeItemSchema = z
  .object({
    cntr_tm: s(),
    cntr_pric: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    cntr_qty: s(),
    acc_trde_qty: s(),
    acc_trde_prica: s(),
  })
  .passthrough();

export const dailyPreviousDayExecutionVolumeResponseSchema = z
  .object({
    ...envelope,
    tdy_pred_cntr_qty: z.array(dailyPreviousDayExecutionVolumeItemSchema).default([]),
  })
  .passthrough();

// ── ka10058: 투자자별일별거래종목 ──

export const dailyTradingItemsByInvestorItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    now_trde_qty: s(),
  })
  .passthrough();

export const dailyTradingItemsByInvestorResponseSchema = z
  .object({
    ...envelope,
    invsr_daly_trde_stk: z.array(dailyTradingItemsByInvestorItemSchema).default([]),
  })
  .passthrough();

// ── ka10059: 종목별투자자기관 ──

export const institutionalInvestorByStockItemSchema = z
  .object({
    dt: s(),
    cur_prc: s(),
    pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    acc_trde_qty: s(),
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

export const institutionalInvestorByStockResponseSchema = z
  .object({
    ...envelope,
    stk_invsr_orgn: z.array(institutionalInvestorByStockItemSchema).default([]),
  })
  .passthrough();

// ── ka10061: 종목별투자자기관종합 ──

export const totalInstitutionalInvestorByStockItemSchema = z
  .object({
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

export const totalInstitutionalInvestorByStockResponseSchema = z
  .object({
    ...envelope,
    stk_invsr_orgn_tot: z.array(totalInstitutionalInvestorByStockItemSchema).default([]),
  })
  .passthrough();

// ── ka10084: 당일전일체결 ──

export const dailyPreviousDayConclusionItemSchema = z
  .object({
    tm: s(),
    cur_prc: s(),
    pred_pre: s(),
    pre_rt: s(),
    pri_sel_bid_unit: s(),
    pri_buy_bid_unit: s(),
    cntr_trde_qty: s(),
    sign: s(),
    acc_trde_qty: s(),
    acc_trde_prica: s(),
    cntr_str: s(),
    stex_tp: s(),
  })
  .passthrough();

export const dailyPreviousDayConclusionResponseSchema = z
  .object({
    ...envelope,
    tdy_pred_cntr: z.array(dailyPreviousDayConclusionItemSchema).default([]),
  })
  .passthrough();

// ── ka10095: 관심종목정보 ──

export const interestStockInfoItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    base_pric: s(),
    pred_pre: s(),
    pred_pre_sig: s(),
    flu_rt: s(),
    trde_qty: s(),
    trde_prica: s(),
    cntr_qty: s(),
    cntr_str: s(),
    pred_trde_qty_pre: s(),
    sel_bid: s(),
    buy_bid: s(),
    sel_1th_bid: s(),
    sel_2th_bid: s(),
    sel_3th_bid: s(),
    sel_4th_bid: s(),
    sel_5th_bid: s(),
    buy_1th_bid: s(),
    buy_2th_bid: s(),
    buy_3th_bid: s(),
    buy_4th_bid: s(),
    buy_5th_bid: s(),
    upl_pric: s(),
    lst_pric: s(),
    open_pric: s(),
    high_pric: s(),
    low_pric: s(),
    close_pric: s(),
    cntr_tm: s(),
    exp_cntr_pric: s(),
    exp_cntr_qty: s(),
    cap: s(),
    fav: s(),
    mac: s(),
    stkcnt: s(),
    bid_tm: s(),
    dt: s(),
    pri_sel_req: s(),
    pri_buy_req: s(),
    pri_sel_cnt: s(),
    pri_buy_cnt: s(),
    tot_sel_req: s(),
    tot_buy_req: s(),
    tot_sel_cnt: s(),
    tot_buy_cnt: s(),
    prty: s(),
    gear: s(),
    pl_qutr: s(),
    cap_support: s(),
    elwexec_pric: s(),
    cnvt_rt: s(),
    elwexpr_dt: s(),
    cntr_engg: s(),
    cntr_pred_pre: s(),
    theory_pric: s(),
    innr_vltl: s(),
    delta: s(),
    gam: s(),
    theta: s(),
    vega: s(),
    law: s(),
  })
  .passthrough();

export const interestStockInfoResponseSchema = z
  .object({
    ...envelope,
    atn_stk_infr: z.array(interestStockInfoItemSchema).default([]),
  })
  .passthrough();

// ── ka10099: 종목정보요약 ──

export const stockInfoSummaryItemSchema = z
  .object({
    code: s(),
    name: s(),
    list_count: s(),
    audit_info: s(),
    reg_day: s(),
    last_price: s(),
    state: s(),
    market_code: s(),
    market_name: s(),
    up_name: s(),
    up_size_name: s(),
    company_class_name: s(),
    order_warning: s(),
    nxt_enable: s(),
    kind: s(),
  })
  .passthrough();

export const stockInfoSummaryResponseSchema = z
  .object({
    ...envelope,
    list: z.array(stockInfoSummaryItemSchema).default([]),
  })
  .passthrough();

// ── ka10100: 종목정보V1 ──

export const stockInfoV1ResponseSchema = z
  .object({
    ...envelope,
    code: s(),
    name: s(),
    list_count: s(),
    audit_info: s(),
    reg_day: s(),
    last_price: s(),
    state: s(),
    market_code: s(),
    market_name: s(),
    up_name: s(),
    up_size_name: s(),
    company_class_name: s(),
    order_warning: s(),
    nxt_enable: s(),
    kind: s(),
  })
  .passthrough();

// ── ka10101: 업종코드 ──

export const industryCodeItemSchema = z
  .object({
    market_code: s(),
    code: s(),
    name: s(),
    group: s(),
  })
  .passthrough();

export const industryCodeResponseSchema = z
  .object({
    ...envelope,
    list: z.array(industryCodeItemSchema).default([]),
  })
  .passthrough();

// ── ka10102: 회원사 ──

export const memberCompanyItemSchema = z
  .object({
    code: s(),
    name: s(),
    gb: s(),
  })
  .passthrough();

export const memberCompanyResponseSchema = z
  .object({
    ...envelope,
    list: z.array(memberCompanyItemSchema).default([]),
  })
  .passthrough();

// ── ka90003: 프로그램순매수상위50 ──

export const top50ProgramNetBuyItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pred_pre_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    now_trde_qty: s(),
  })
  .passthrough();

export const top50ProgramNetBuyResponseSchema = z
  .object({
    ...envelope,
    prm_netprps_upper50: z.array(top50ProgramNetBuyItemSchema).default([]),
  })
  .passthrough();

// ── ka90004: 종목별프로그램매매현황 ──

export const programTradingStatusByStockItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    flu_sig: s(),
    pred_pre: s(),
    buy_cntr_qty: s(),
    buy_cntr_amt: s(),
    sel_cntr_qty: s(),
    sel_cntr_amt: s(),
    netprps_prica: s(),
    all_trde_rt: s(),
  })
  .passthrough();

export const programTradingStatusByStockResponseSchema = z
  .object({
    ...envelope,
    tot1: s(),
    tot2: s(),
    tot3: s(),
    tot4: s(),
    tot5: s(),
    tot6: s(),
    stk_prm_trde_prst: z.array(programTradingStatusByStockItemSchema).default([]),
  })
  .passthrough();

// ── Response Types ──

export type StockInfoResponse = CamelizeKeys<z.infer<typeof stockInfoResponseSchema>>;
export type StockTradingMemberResponse = CamelizeKeys<z.infer<typeof stockTradingMemberResponseSchema>>;
export type ExecutionResponse = CamelizeKeys<z.infer<typeof executionResponseSchema>>;
export type MarginTradingTrendResponse = CamelizeKeys<z.infer<typeof marginTradingTrendResponseSchema>>;
export type DailyTradingDetailsResponse = CamelizeKeys<z.infer<typeof dailyTradingDetailsResponseSchema>>;
export type NewHighLowPriceResponse = CamelizeKeys<z.infer<typeof newHighLowPriceResponseSchema>>;
export type UpperLowerLimitPriceResponse = CamelizeKeys<z.infer<typeof upperLowerLimitPriceResponseSchema>>;
export type HighLowPriceApproachResponse = CamelizeKeys<z.infer<typeof highLowPriceApproachResponseSchema>>;
export type PriceVolatilityResponse = CamelizeKeys<z.infer<typeof priceVolatilityResponseSchema>>;
export type TradingVolumeRenewalResponse = CamelizeKeys<z.infer<typeof tradingVolumeRenewalResponseSchema>>;
export type SupplyDemandConcentrationResponse = CamelizeKeys<z.infer<typeof supplyDemandConcentrationResponseSchema>>;
export type HighPerResponse = CamelizeKeys<z.infer<typeof highPerResponseSchema>>;
export type ChangeRateFromOpenResponse = CamelizeKeys<z.infer<typeof changeRateFromOpenResponseSchema>>;
export type TradingMemberSupplyDemandAnalysisResponse = CamelizeKeys<
  z.infer<typeof tradingMemberSupplyDemandAnalysisResponseSchema>
>;
export type TradingMemberInstantVolumeResponse = CamelizeKeys<z.infer<typeof tradingMemberInstantVolumeResponseSchema>>;
export type VolatilityControlEventResponse = CamelizeKeys<z.infer<typeof volatilityControlEventResponseSchema>>;
export type DailyPreviousDayExecutionVolumeResponse = CamelizeKeys<
  z.infer<typeof dailyPreviousDayExecutionVolumeResponseSchema>
>;
export type DailyTradingItemsByInvestorResponse = CamelizeKeys<
  z.infer<typeof dailyTradingItemsByInvestorResponseSchema>
>;
export type InstitutionalInvestorByStockResponse = CamelizeKeys<
  z.infer<typeof institutionalInvestorByStockResponseSchema>
>;
export type TotalInstitutionalInvestorByStockResponse = CamelizeKeys<
  z.infer<typeof totalInstitutionalInvestorByStockResponseSchema>
>;
export type DailyPreviousDayConclusionResponse = CamelizeKeys<z.infer<typeof dailyPreviousDayConclusionResponseSchema>>;
export type InterestStockInfoResponse = CamelizeKeys<z.infer<typeof interestStockInfoResponseSchema>>;
export type StockInfoSummaryResponse = CamelizeKeys<z.infer<typeof stockInfoSummaryResponseSchema>>;
export type StockInfoV1Response = CamelizeKeys<z.infer<typeof stockInfoV1ResponseSchema>>;
export type IndustryCodeResponse = CamelizeKeys<z.infer<typeof industryCodeResponseSchema>>;
export type MemberCompanyResponse = CamelizeKeys<z.infer<typeof memberCompanyResponseSchema>>;
export type Top50ProgramNetBuyResponse = CamelizeKeys<z.infer<typeof top50ProgramNetBuyResponseSchema>>;
export type ProgramTradingStatusByStockResponse = CamelizeKeys<
  z.infer<typeof programTradingStatusByStockResponseSchema>
>;

// ── Response Map ──

export interface DomesticStockInfoResponseMap {
  getStockInfo: StockInfoResponse;
  getStockTradingMember: StockTradingMemberResponse;
  getExecution: ExecutionResponse;
  getMarginTradingTrend: MarginTradingTrendResponse;
  getDailyTradingDetails: DailyTradingDetailsResponse;
  getNewHighLowPrice: NewHighLowPriceResponse;
  getUpperLowerLimitPrice: UpperLowerLimitPriceResponse;
  getHighLowPriceApproach: HighLowPriceApproachResponse;
  getPriceVolatility: PriceVolatilityResponse;
  getTradingVolumeRenewal: TradingVolumeRenewalResponse;
  getSupplyDemandConcentration: SupplyDemandConcentrationResponse;
  getHighPer: HighPerResponse;
  getChangeRateFromOpen: ChangeRateFromOpenResponse;
  getTradingMemberSupplyDemandAnalysis: TradingMemberSupplyDemandAnalysisResponse;
  getTradingMemberInstantVolume: TradingMemberInstantVolumeResponse;
  getVolatilityControlEvent: VolatilityControlEventResponse;
  getDailyPreviousDayExecutionVolume: DailyPreviousDayExecutionVolumeResponse;
  getDailyTradingItemsByInvestor: DailyTradingItemsByInvestorResponse;
  getInstitutionalInvestorByStock: InstitutionalInvestorByStockResponse;
  getTotalInstitutionalInvestorByStock: TotalInstitutionalInvestorByStockResponse;
  getDailyPreviousDayConclusion: DailyPreviousDayConclusionResponse;
  getInterestStockInfo: InterestStockInfoResponse;
  getStockInfoSummary: StockInfoSummaryResponse;
  getStockInfoV1: StockInfoV1Response;
  getIndustryCode: IndustryCodeResponse;
  getMemberCompany: MemberCompanyResponse;
  getTop50ProgramNetBuy: Top50ProgramNetBuyResponse;
  getProgramTradingStatusByStock: ProgramTradingStatusByStockResponse;
}
