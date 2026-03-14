import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types';

const s = () => z.string().default('');

const kisEnvelope = {
  rt_cd: z.string().optional(),
  msg_cd: z.string().optional(),
  msg1: z.string().optional(),
};

// ── requestStockOrder: Stock Quote Current ──

export const requestStockOrderItemSchema = z
  .object({
    krx_fwdg_ord_orgno: s(),
    odno: s(),
    ord_tmd: s(),
  })
  .passthrough();

export const requestStockOrderResponseSchema = z
  .object({
    ...kisEnvelope,
    output: requestStockOrderItemSchema.optional(),
  })
  .passthrough();

// ── requestStockQuoteCorrection: Stock Quote Correction ──

export const requestStockQuoteCorrectionItemSchema = z
  .object({
    krx_fwdg_ord_orgno: s(),
    odno: s(),
    ord_tmd: s(),
  })
  .passthrough();

export const requestStockQuoteCorrectionResponseSchema = z
  .object({
    ...kisEnvelope,
    output: requestStockQuoteCorrectionItemSchema.optional(),
  })
  .passthrough();

// ── requestStockReserveQuote: Stock Reserve Quote ──

export const requestStockReserveQuoteItemSchema = z
  .object({
    odno: s(),
    rsvn_ord_rcit_dt: s(),
    ovrs_rsvn_odno: s(),
  })
  .passthrough();

export const requestStockReserveQuoteResponseSchema = z
  .object({
    ...kisEnvelope,
    output: requestStockReserveQuoteItemSchema.optional(),
  })
  .passthrough();

// ── requestStockReserveQuoteCorrection: Stock Reserve Quote Correction ──

export const requestStockReserveQuoteCorrectionItemSchema = z
  .object({
    ovrs_rsvn_odno: s(),
  })
  .passthrough();

export const requestStockReserveQuoteCorrectionResponseSchema = z
  .object({
    ...kisEnvelope,
    output: requestStockReserveQuoteCorrectionItemSchema.optional(),
  })
  .passthrough();

// ── getBuyTradableAmount: Buy Tradable Amount ──

export const getBuyTradableAmountItemSchema = z
  .object({
    tr_crcy_cd: z.string().optional(),
    ord_psbl_frcr_amt: z.string().optional(),
    sll_ruse_psbl_amt: z.string().optional(),
    ovrs_ord_psbl_amt: z.string().optional(),
    max_ord_psbl_qty: z.string().optional(),
    echm_af_ord_psbl_amt: z.string().optional(),
    echm_af_ord_psbl_qty: z.string().optional(),
    ord_psbl_qty: z.string().optional(),
    exrt: z.string().optional(),
    frcr_ord_psbl_amt1: z.string().optional(),
    ovrs_max_ord_psbl_qty: z.string().optional(),
  })
  .passthrough();

export const getBuyTradableAmountResponseSchema = z
  .object({
    ...kisEnvelope,
    output: getBuyTradableAmountItemSchema.optional(),
  })
  .passthrough();

// ── getStockNotConclusionHistory: Stock Not Conclusion ──

export const getStockNotConclusionHistoryItemSchema = z
  .object({
    ord_dt: s(),
    ord_gno_brno: s(),
    odno: s(),
    orgn_odno: s(),
    pdno: s(),
    prdt_name: s(),
    sll_buy_dvsn_cd: s(),
    sll_buy_dvsn_cd_name: s(),
    rvse_cncl_dvsn_cd: s(),
    rvse_cncl_dvsn_cd_name: s(),
    rjct_rson: s(),
    rjct_rson_name: s(),
    ord_tmd: s(),
    tr_mket_name: s(),
    tr_crcy_cd: s(),
    natn_cd: s(),
    natn_kor_name: s(),
    ft_ord_qty: s(),
    ft_ccld_qty: s(),
    nccs_qty: s(),
    ft_ord_unpr3: s(),
    ft_ccld_unpr3: s(),
    ft_ccld_amt3: s(),
    ovrs_excg_cd: s(),
    prcs_stat_name: s(),
    loan_type_cd: s(),
    loan_dt: s(),
    usa_amk_exts_rqst_yn: s(),
    splt_buy_attr_name: s(),
  })
  .passthrough();

export const getStockNotConclusionHistoryResponseSchema = z
  .object({
    ...kisEnvelope,
    ctx_area_fk200: s(),
    ctx_area_nk200: s(),
    output: z.array(getStockNotConclusionHistoryItemSchema).default([]),
  })
  .passthrough();

// ── getStockBalance: Stock Balance ──

export const getStockBalanceOutput1ItemSchema = z
  .object({
    cano: s(),
    acnt_prdt_cd: s(),
    prdt_type_cd: s(),
    ovrs_pdno: s(),
    ovrs_item_name: s(),
    frcr_evlu_pfls_amt: s(),
    evlu_pfls_rt: s(),
    pchs_avg_pric: s(),
    ovrs_cblc_qty: s(),
    ord_psbl_qty: s(),
    frcr_pchs_amt1: s(),
    ovrs_stck_evlu_amt: s(),
    now_pric2: s(),
    tr_crcy_cd: s(),
    ovrs_excg_cd: s(),
    loan_type_cd: s(),
    loan_dt: s(),
    expd_dt: s(),
  })
  .passthrough();

export const getStockBalanceOutput2ItemSchema = z
  .object({
    frcr_pchs_amt1: s(),
    ovrs_rlzt_pfls_amt: s(),
    ovrs_tot_pfls: s(),
    rlzt_erng_rt: s(),
    tot_evlu_pfls_amt: s(),
    tot_pftrt: s(),
    frcr_buy_amt_smtl1: s(),
    ovrs_rlzt_pfls_amt2: s(),
    frcr_buy_amt_smtl2: s(),
  })
  .passthrough();

export const getStockBalanceResponseSchema = z
  .object({
    ...kisEnvelope,
    ctx_area_fk200: s(),
    ctx_area_nk200: s(),
    output1: z.array(getStockBalanceOutput1ItemSchema).default([]),
    output2: getStockBalanceOutput2ItemSchema.optional(),
  })
  .passthrough();

// ── getStockConclusionHistory: Stock Conclusion History ──

export const getStockConclusionHistoryItemSchema = z
  .object({
    ord_dt: s(),
    ord_gno_brno: s(),
    odno: s(),
    orgn_odno: s(),
    sll_buy_dvsn_cd: s(),
    sll_buy_dvsn_cd_name: s(),
    rvse_cncl_dvsn: s(),
    rvse_cncl_dvsn_name: s(),
    pdno: s(),
    prdt_name: s(),
    ft_ord_qty: s(),
    ft_ord_unpr3: s(),
    ft_ccld_qty: s(),
    ft_ccld_unpr3: s(),
    ft_ccld_amt3: s(),
    nccs_qty: s(),
    prcs_stat_name: s(),
    rjct_rson: s(),
    rjct_rson_name: s(),
    ord_tmd: s(),
    tr_mket_name: s(),
    tr_natn: s(),
    tr_natn_name: s(),
    ovrs_excg_cd: s(),
    tr_crcy_cd: s(),
    dmst_ord_dt: s(),
    thco_ord_tmd: s(),
    loan_type_cd: s(),
    loan_dt: s(),
    mdia_dvsn_name: s(),
    usa_amk_exts_rqst_yn: s(),
    splt_buy_attr_name: s(),
  })
  .passthrough();

export const getStockConclusionHistoryResponseSchema = z
  .object({
    ...kisEnvelope,
    ctx_area_fk200: s(),
    ctx_area_nk200: s(),
    output: z.array(getStockConclusionHistoryItemSchema).default([]),
  })
  .passthrough();

// ── getCurrentBalanceByConclusion: Current Balance By Conclusion ──

export const getCurrentBalanceByConclusionOutput1ItemSchema = z
  .object({
    prdt_name: s(),
    cblc_qty13: s(),
    thdt_buy_ccld_qty1: s(),
    thdt_sll_ccld_qty1: s(),
    ccld_qty_smtl1: s(),
    ord_psbl_qty1: s(),
    frcr_pchs_amt: s(),
    frcr_evlu_amt2: s(),
    evlu_pfls_amt2: s(),
    evlu_pfls_rt1: s(),
    pdno: s(),
    bass_exrt: s(),
    buy_crcy_cd: s(),
    ovrs_now_pric1: s(),
    avg_unpr3: s(),
    tr_mket_name: s(),
    natn_kor_name: s(),
    pchs_rmnd_wcrc_amt: s(),
    thdt_buy_ccld_frcr_amt: s(),
    thdt_sll_ccld_frcr_amt: s(),
    unit_amt: s(),
    std_pdno: s(),
    prdt_type_cd: s(),
    scts_dvsn_name: s(),
    loan_rmnd: s(),
    loan_dt: s(),
    loan_expd_dt: s(),
    ovrs_excg_cd: s(),
    item_lnkg_excg_cd: s(),
  })
  .passthrough();

export const getCurrentBalanceByConclusionOutput2ItemSchema = z
  .object({
    crcy_cd: s(),
    crcy_cd_name: s(),
    frcr_buy_amt_smtl: s(),
    frcr_sll_amt_smtl: s(),
    frcr_dncl_amt_2: s(),
    frst_bltn_exrt: s(),
    frcr_buy_mgn_amt: s(),
    frcr_etc_mgna: s(),
    frcr_drwg_psbl_amt_1: s(),
    frcr_evlu_amt2: s(),
    acpl_cstd_crcy_yn: s(),
    nxdy_frcr_drwg_psbl_amt: s(),
    pchs_amt_smtl: s(),
    evlu_amt_smtl: s(),
    evlu_pfls_amt_smtl: s(),
    dncl_amt: s(),
    cma_evlu_amt: s(),
    tot_dncl_amt: s(),
    etc_mgna: s(),
    wdrw_psbl_tot_amt: s(),
    frcr_evlu_tota: s(),
    evlu_erng_rt1: s(),
    pchs_amt_smtl_amt: s(),
    evlu_amt_smtl_amt: s(),
    tot_evlu_pfls_amt: s(),
    tot_asst_amt: s(),
    buy_mgn_amt: s(),
    mgna_tota: s(),
    frcr_use_psbl_amt: s(),
    ustl_sll_amt_smtl: s(),
    ustl_buy_amt_smtl: s(),
    tot_frcr_cblc_smtl: s(),
    tot_loan_amt: s(),
  })
  .passthrough();

export const getCurrentBalanceByConclusionResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: z.array(getCurrentBalanceByConclusionOutput1ItemSchema).default([]),
    output2: z.array(getCurrentBalanceByConclusionOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getReserveOrders: Reserve Orders ──

export const getReserveOrdersItemSchema = z
  .object({
    cncl_yn: z.string().optional(),
    rsvn_ord_rcit_dt: z.string().optional(),
    ovrs_rsvn_odno: z.string().optional(),
    ord_dt: z.string().optional(),
    ord_gno_brno: z.string().optional(),
    odno: z.string().optional(),
    sll_buy_dvsn_cd: z.string().optional(),
    sll_buy_dvsn_name: z.string().optional(),
    ovrs_rsvn_ord_stat_cd: z.string().optional(),
    ovrs_rsvn_ord_stat_cd_name: z.string().optional(),
    pdno: z.string().optional(),
    prdt_type_cd: z.string().optional(),
    prdt_name: z.string().optional(),
    ord_rcit_tmd: z.string().optional(),
    ord_fwdg_tmd: z.string().optional(),
    tr_dvsn_name: z.string().optional(),
    ovrs_excg_cd: z.string().optional(),
    tr_mket_name: z.string().optional(),
    ord_stfno: z.string().optional(),
    ft_ord_qty: z.string().optional(),
    ft_ord_unpr3: z.string().optional(),
    ft_ccld_qty: z.string().optional(),
    nprc_rson_text: z.string().optional(),
    splt_buy_attr_name: z.string().optional(),
  })
  .passthrough();

export const getReserveOrdersResponseSchema = z
  .object({
    ...kisEnvelope,
    ctx_area_fk200: s(),
    ctx_area_nk200: s(),
    output: getReserveOrdersItemSchema.optional(),
  })
  .passthrough();

// ── getBalanceBySettlement: Balance By Settlement ──

export const getBalanceBySettlementOutput1ItemSchema = z
  .object({
    pdno: s(),
    prdt_name: s(),
    cblc_qty13: s(),
    ord_psbl_qty1: s(),
    avg_unpr3: s(),
    ovrs_now_pric1: s(),
    frcr_pchs_amt: s(),
    frcr_evlu_amt2: s(),
    evlu_pfls_amt2: s(),
    bass_exrt: s(),
    oprt_dtl_dtime: s(),
    buy_crcy_cd: s(),
    thdt_sll_ccld_qty1: s(),
    thdt_buy_ccld_qty1: s(),
    evlu_pfls_rt1: s(),
    tr_mket_name: s(),
    natn_kor_name: s(),
    std_pdno: s(),
    mgge_qty: s(),
    loan_rmnd: s(),
    prdt_type_cd: s(),
    ovrs_excg_cd: s(),
    scts_dvsn_name: s(),
    ldng_cblc_qty: s(),
  })
  .passthrough();

export const getBalanceBySettlementOutput2ItemSchema = z
  .object({
    crcy_cd: s(),
    crcy_cd_name: s(),
    frcr_dncl_amt_2: s(),
    frst_bltn_exrt: s(),
    frcr_evlu_amt2: s(),
    pchs_amt_smtl_amt: s(),
    tot_evlu_pfls_amt: s(),
    evlu_erng_rt1: s(),
    tot_dncl_amt: s(),
    wcrc_evlu_amt_smtl: s(),
    tot_asst_amt2: s(),
    frcr_cblc_wcrc_evlu_amt_smtl: s(),
    tot_loan_amt: s(),
    tot_ldng_evlu_amt: s(),
  })
  .passthrough();

export const getBalanceBySettlementResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: z.array(getBalanceBySettlementOutput1ItemSchema).default([]),
    output2: z.array(getBalanceBySettlementOutput2ItemSchema).default([]),
  })
  .passthrough();

// ── getDailyTransactionHistory: Daily Transaction History ──

export const getDailyTransactionHistoryItemSchema = z
  .object({
    trad_dt: s(),
    sttl_dt: s(),
    sll_buy_dvsn_cd: s(),
    sll_buy_dvsn_name: s(),
    pdno: s(),
    ovrs_item_name: s(),
    ccld_qty: s(),
    amt_unit_ccld_qty: s(),
    ft_ccld_unpr2: s(),
    ovrs_stck_ccld_unpr: s(),
    tr_frcr_amt2: s(),
    tr_amt: s(),
    frcr_excc_amt_1: s(),
    wcrc_excc_amt: s(),
    dmst_frcr_fee1: s(),
    frcr_fee1: s(),
    dmst_wcrc_fee: s(),
    ovrs_wcrc_fee: s(),
    crcy_cd: s(),
    std_pdno: s(),
    erlm_exrt: s(),
    loan_dvsn_cd: s(),
    loan_dvsn_name: s(),
    output2: s(),
    frcr_buy_amt_smtl: s(),
    frcr_sll_amt_smtl: s(),
    dmst_fee_smtl: s(),
    ovrs_fee_smtl: s(),
  })
  .passthrough();

export const getDailyTransactionHistoryResponseSchema = z
  .object({
    ...kisEnvelope,
    ctx_area_fk200: s(),
    ctx_area_nk200: s(),
    output: z.array(getDailyTransactionHistoryItemSchema).default([]),
  })
  .passthrough();

// ── getPeriodProfitLoss: Period Profit Loss ──

export const getPeriodProfitLossOutputItemSchema = z
  .object({
    trad_day: s(),
    ovrs_pdno: s(),
    ovrs_item_name: s(),
    slcl_qty: s(),
    pchs_avg_pric: s(),
    frcr_pchs_amt1: s(),
    avg_sll_unpr: s(),
    frcr_sll_amt_smtl1: s(),
    stck_sll_tlex: s(),
    ovrs_rlzt_pfls_amt: s(),
    pftrt: s(),
    exrt: s(),
    ovrs_excg_cd: s(),
    frst_bltn_exrt: s(),
  })
  .passthrough();

export const getPeriodProfitLossOutput2ItemSchema = z
  .object({
    stck_sll_amt_smtl: s(),
    stck_buy_amt_smtl: s(),
    smtl_fee1: s(),
    excc_dfrm_amt: s(),
    ovrs_rlzt_pfls_tot_amt: s(),
    tot_pftrt: s(),
    bass_dt: s(),
    exrt: s(),
  })
  .passthrough();

export const getPeriodProfitLossResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getPeriodProfitLossOutputItemSchema).default([]),
    output2: getPeriodProfitLossOutput2ItemSchema.optional(),
  })
  .passthrough();

// ── getMarginAggregate: Margin Aggregate ──

export const getMarginAggregateItemSchema = z
  .object({
    natn_name: s(),
    crcy_cd: s(),
    frcr_dncl_amt1: s(),
    ustl_buy_amt: s(),
    ustl_sll_amt: s(),
    frcr_rcvb_amt: s(),
    frcr_mgn_amt: s(),
    frcr_gnrl_ord_psbl_amt: s(),
    frcr_ord_psbl_amt1: s(),
    itgr_ord_psbl_amt: s(),
    bass_exrt: s(),
  })
  .passthrough();

export const getMarginAggregateResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getMarginAggregateItemSchema).default([]),
  })
  .passthrough();

// ── requestOrderAfterDayTime: Order After Day Time ──

export const requestOrderAfterDayTimeItemSchema = z
  .object({
    krx_fwdg_ord_orgno: s(),
    odno: s(),
    ord_tmd: s(),
  })
  .passthrough();

export const requestOrderAfterDayTimeResponseSchema = z
  .object({
    ...kisEnvelope,
    output: requestOrderAfterDayTimeItemSchema.optional(),
  })
  .passthrough();

// ── cancelCorrectAfterDayTime: Correct After Day Time ──

export const cancelCorrectAfterDayTimeItemSchema = z
  .object({
    krx_fwdg_ord_orgno: s(),
    odno: s(),
    ord_tmd: s(),
  })
  .passthrough();

export const cancelCorrectAfterDayTimeResponseSchema = z
  .object({
    ...kisEnvelope,
    output: cancelCorrectAfterDayTimeItemSchema.optional(),
  })
  .passthrough();

// ── getLimitOrderNumber: Limit Order Number ──

export const getLimitOrderNumberItemSchema = z
  .object({
    odno: s(),
    trad_dvsn_name: s(),
    pdno: s(),
    item_name: s(),
    ft_ord_qty: s(),
    ft_ord_unpr3: s(),
    splt_buy_attr_name: s(),
    ft_ccld_qty: s(),
    ord_gno_brno: z.string().optional(),
    rt_cd: s(),
    msg_cd: s(),
    msg1: s(),
    ctx_area_fk200: s(),
    ctx_area_nk200: s(),
  })
  .passthrough();

export const getLimitOrderNumberResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getLimitOrderNumberItemSchema).default([]),
  })
  .passthrough();

// ── getLimitOrderExecutionHistory: Limit Order Execution History ──

export const getLimitOrderExecutionHistoryOutput1ItemSchema = z
  .object({
    ccld_seq: s(),
    ccld_btwn: s(),
    pdno: s(),
    item_name: s(),
    ft_ccld_qty: z.string().optional(),
    ft_ccld_unpr3: s(),
    ft_ccld_amt3: z.string().optional(),
  })
  .passthrough();

export const getLimitOrderExecutionHistoryOutput3ItemSchema = z
  .object({
    odno: s(),
    trad_dvsn_name: s(),
    pdno: s(),
    item_name: s(),
    ft_ord_qty: s(),
    ft_ord_unpr3: s(),
    ord_tmd: s(),
    splt_buy_attr_name: s(),
    ft_ccld_qty: s(),
    tr_crcy: s(),
    ft_ccld_unpr3: s(),
    ft_ccld_amt3: s(),
    ccld_cnt: s(),
  })
  .passthrough();

export const getLimitOrderExecutionHistoryResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: z.array(getLimitOrderExecutionHistoryOutput1ItemSchema).default([]),
    output3: z.array(getLimitOrderExecutionHistoryOutput3ItemSchema).default([]),
  })
  .passthrough();

// ── Response Types ──

export type RequestStockOrderResponse = CamelizeKeys<z.infer<typeof requestStockOrderResponseSchema>>;

export type RequestStockQuoteCorrectionResponse = CamelizeKeys<
  z.infer<typeof requestStockQuoteCorrectionResponseSchema>
>;

export type RequestStockReserveQuoteResponse = CamelizeKeys<z.infer<typeof requestStockReserveQuoteResponseSchema>>;

export type RequestStockReserveQuoteCorrectionResponse = CamelizeKeys<
  z.infer<typeof requestStockReserveQuoteCorrectionResponseSchema>
>;

export type GetBuyTradableAmountResponse = CamelizeKeys<z.infer<typeof getBuyTradableAmountResponseSchema>>;

export type GetStockNotConclusionHistoryResponse = CamelizeKeys<
  z.infer<typeof getStockNotConclusionHistoryResponseSchema>
>;

export type GetStockBalanceResponse = CamelizeKeys<z.infer<typeof getStockBalanceResponseSchema>>;

export type GetStockConclusionHistoryResponse = CamelizeKeys<z.infer<typeof getStockConclusionHistoryResponseSchema>>;

export type GetCurrentBalanceByConclusionResponse = CamelizeKeys<
  z.infer<typeof getCurrentBalanceByConclusionResponseSchema>
>;

export type GetReserveOrdersResponse = CamelizeKeys<z.infer<typeof getReserveOrdersResponseSchema>>;

export type GetBalanceBySettlementResponse = CamelizeKeys<z.infer<typeof getBalanceBySettlementResponseSchema>>;

export type GetDailyTransactionHistoryResponse = CamelizeKeys<z.infer<typeof getDailyTransactionHistoryResponseSchema>>;

export type GetPeriodProfitLossResponse = CamelizeKeys<z.infer<typeof getPeriodProfitLossResponseSchema>>;

export type GetMarginAggregateResponse = CamelizeKeys<z.infer<typeof getMarginAggregateResponseSchema>>;

export type RequestOrderAfterDayTimeResponse = CamelizeKeys<z.infer<typeof requestOrderAfterDayTimeResponseSchema>>;

export type CancelCorrectAfterDayTimeResponse = CamelizeKeys<z.infer<typeof cancelCorrectAfterDayTimeResponseSchema>>;

export type GetLimitOrderNumberResponse = CamelizeKeys<z.infer<typeof getLimitOrderNumberResponseSchema>>;

export type GetLimitOrderExecutionHistoryResponse = CamelizeKeys<
  z.infer<typeof getLimitOrderExecutionHistoryResponseSchema>
>;

// ── Response Map ──

export interface OverseasAccountResponseMap {
  requestStockOrder: RequestStockOrderResponse;
  requestStockQuoteCorrection: RequestStockQuoteCorrectionResponse;
  requestStockReserveQuote: RequestStockReserveQuoteResponse;
  requestStockReserveQuoteCorrection: RequestStockReserveQuoteCorrectionResponse;
  getBuyTradableAmount: GetBuyTradableAmountResponse;
  getStockNotConclusionHistory: GetStockNotConclusionHistoryResponse;
  getStockBalance: GetStockBalanceResponse;
  getStockConclusionHistory: GetStockConclusionHistoryResponse;
  getCurrentBalanceByConclusion: GetCurrentBalanceByConclusionResponse;
  getReserveOrders: GetReserveOrdersResponse;
  getBalanceBySettlement: GetBalanceBySettlementResponse;
  getDailyTransactionHistory: GetDailyTransactionHistoryResponse;
  getPeriodProfitLoss: GetPeriodProfitLossResponse;
  getMarginAggregate: GetMarginAggregateResponse;
  requestOrderAfterDayTime: RequestOrderAfterDayTimeResponse;
  cancelCorrectAfterDayTime: CancelCorrectAfterDayTimeResponse;
  getLimitOrderNumber: GetLimitOrderNumberResponse;
  getLimitOrderExecutionHistory: GetLimitOrderExecutionHistoryResponse;
}
