import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types';

const s = () => z.string().default('');

const kisEnvelope = {
  rt_cd: z.string().optional(),
  msg_cd: z.string().optional(),
  msg1: z.string().optional(),
};

// ── getProductBasicInfo: Product Basic Info ──

export const getProductBasicInfoItemSchema = z
  .object({
    pdno: s(),
    prdt_type_cd: s(),
    prdt_name: s(),
    prdt_name120: s(),
    prdt_abrv_name: s(),
    prdt_eng_name: s(),
    prdt_eng_name120: s(),
    prdt_eng_abrv_name: s(),
    std_pdno: s(),
    shtn_pdno: s(),
    prdt_sale_stat_cd: s(),
    prdt_risk_grad_cd: s(),
    prdt_clsf_cd: s(),
    prdt_clsf_name: s(),
    sale_strt_dt: s(),
    sale_end_dt: s(),
    wrap_asst_type_cd: s(),
    ivst_prdt_type_cd: s(),
    ivst_prdt_type_cd_name: s(),
    frst_erlm_dt: s(),
  })
  .passthrough();

export const getProductBasicInfoResponseSchema = z
  .object({
    ...kisEnvelope,
    output: getProductBasicInfoItemSchema.optional(),
  })
  .passthrough();

// ── getStockBasicInfo: Stock Basic Info ──

export const getStockBasicInfoItemSchema = z
  .object({
    pdno: s(),
    prdt_type_cd: s(),
    mket_id_cd: s(),
    scty_grp_id_cd: s(),
    excg_dvsn_cd: s(),
    setl_mmdd: s(),
    lstg_stqt: s(),
    lstg_cptl_amt: s(),
    cpta: s(),
    papr: s(),
    issu_pric: s(),
    kospi200_item_yn: s(),
    scts_mket_lstg_dt: s(),
    scts_mket_lstg_abol_dt: s(),
    kosdaq_mket_lstg_dt: s(),
    kosdaq_mket_lstg_abol_dt: s(),
    frbd_mket_lstg_dt: s(),
    frbd_mket_lstg_abol_dt: s(),
    reits_kind_cd: s(),
    etf_dvsn_cd: s(),
    oilf_fund_yn: s(),
    idx_bztp_lcls_cd: s(),
    idx_bztp_mcls_cd: s(),
    idx_bztp_scls_cd: s(),
    stck_kind_cd: s(),
    mfnd_opng_dt: s(),
    mfnd_end_dt: s(),
    dpsi_erlm_cncl_dt: s(),
    etf_cu_qty: s(),
    prdt_name: s(),
    prdt_name120: s(),
    prdt_abrv_name: s(),
    std_pdno: s(),
    prdt_eng_name: s(),
    prdt_eng_name120: s(),
    prdt_eng_abrv_name: s(),
    dpsi_aptm_erlm_yn: s(),
    etf_txtn_type_cd: s(),
    etf_type_cd: s(),
    lstg_abol_dt: s(),
    nwst_odst_dvsn_cd: s(),
    sbst_pric: s(),
    thco_sbst_pric: s(),
    thco_sbst_pric_chng_dt: s(),
    tr_stop_yn: s(),
    admn_item_yn: s(),
    thdt_clpr: s(),
    bfdy_clpr: s(),
    clpr_chng_dt: s(),
    std_idst_clsf_cd: s(),
    std_idst_clsf_cd_name: s(),
    idx_bztp_lcls_cd_name: s(),
    idx_bztp_mcls_cd_name: s(),
    idx_bztp_scls_cd_name: s(),
    ocr_no: s(),
    crfd_item_yn: s(),
    elec_scty_yn: s(),
    issu_istt_cd: s(),
    etf_chas_erng_rt_dbnb: s(),
    etf_etn_ivst_heed_item_yn: s(),
    stln_int_rt_dvsn_cd: s(),
    frnr_psnl_lmt_rt: s(),
    lstg_rqsr_issu_istt_cd: s(),
    lstg_rqsr_item_cd: s(),
    trst_istt_issu_istt_cd: s(),
    cptt_trad_tr_psbl_yn: s(),
    nxt_tr_stop_yn: s(),
  })
  .passthrough();

export const getStockBasicInfoResponseSchema = z
  .object({
    ...kisEnvelope,
    output: getStockBasicInfoItemSchema.optional(),
  })
  .passthrough();

// ── getBalanceSheet: Balance Sheet ──

export const getBalanceSheetItemSchema = z
  .object({
    stac_yymm: s(),
    cras: s(),
    fxas: s(),
    total_aset: s(),
    flow_lblt: s(),
    fix_lblt: s(),
    total_lblt: s(),
    cpfn: s(),
    cfp_surp: s(),
    prfi_surp: s(),
    total_cptl: s(),
  })
  .passthrough();

export const getBalanceSheetResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getBalanceSheetItemSchema).default([]),
  })
  .passthrough();

// ── getIncomeStatement: Income Statement ──

export const getIncomeStatementItemSchema = z
  .object({
    stac_yymm: s(),
    sale_account: s(),
    sale_cost: s(),
    sale_totl_prfi: s(),
    depr_cost: s(),
    sell_mang: s(),
    bsop_prti: s(),
    bsop_non_ernn: s(),
    bsop_non_expn: s(),
    op_prfi: s(),
    spec_prfi: s(),
    spec_loss: s(),
    thtr_ntin: s(),
  })
  .passthrough();

export const getIncomeStatementResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getIncomeStatementItemSchema).default([]),
  })
  .passthrough();

// ── getFinancialRatio: Financial Ratio ──

export const getFinancialRatioItemSchema = z
  .object({
    stac_yymm: s(),
    grs: s(),
    bsop_prfi_inrt: s(),
    ntin_inrt: s(),
    roe_val: s(),
    eps: s(),
    sps: s(),
    bps: s(),
    rsrv_rate: s(),
    lblt_rate: s(),
  })
  .passthrough();

export const getFinancialRatioResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getFinancialRatioItemSchema).default([]),
  })
  .passthrough();

// ── getProfitabilityRatio: Profitability Ratio ──

export const getProfitabilityRatioItemSchema = z
  .object({
    stac_yymm: s(),
    cptl_ntin_rate: s(),
    self_cptl_ntin_inrt: s(),
    sale_ntin_rate: s(),
    sale_totl_rate: s(),
  })
  .passthrough();

export const getProfitabilityRatioResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getProfitabilityRatioItemSchema).default([]),
  })
  .passthrough();

// ── getOtherKeyRatio: Other Key Ratio ──

export const getOtherKeyRatioItemSchema = z
  .object({
    stac_yymm: s(),
    payout_rate: s(),
    eva: s(),
    ebitda: s(),
    ev_ebitda: s(),
  })
  .passthrough();

export const getOtherKeyRatioResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getOtherKeyRatioItemSchema).default([]),
  })
  .passthrough();

// ── getStabilityRatio: Stability Ratio ──

export const getStabilityRatioItemSchema = z
  .object({
    stac_yymm: s(),
    lblt_rate: s(),
    bram_depn: s(),
    crnt_rate: s(),
    quck_rate: s(),
  })
  .passthrough();

export const getStabilityRatioResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getStabilityRatioItemSchema).default([]),
  })
  .passthrough();

// ── getGrowthRatio: Growth Ratio ──

export const getGrowthRatioItemSchema = z
  .object({
    stac_yymm: s(),
    grs: s(),
    bsop_prfi_inrt: s(),
    equt_inrt: s(),
    totl_aset_inrt: s(),
  })
  .passthrough();

export const getGrowthRatioResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getGrowthRatioItemSchema).default([]),
  })
  .passthrough();

// ── getMarginTradableStocks: Margin Tradable Stocks ──

export const getMarginTradableStocksItemSchema = z
  .object({
    stck_shrn_iscd: s(),
    hts_kor_isnm: s(),
    crdt_rate: s(),
  })
  .passthrough();

export const getMarginTradableStocksResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getMarginTradableStocksItemSchema).default([]),
  })
  .passthrough();

// ── getKsdDividendDecision: Ksd Dividend Decision ──

export const getKsdDividendDecisionItemSchema = z
  .object({
    record_date: s(),
    sht_cd: s(),
    isin_name: s(),
    divi_kind: s(),
    face_val: s(),
    per_sto_divi_amt: s(),
    divi_rate: s(),
    stk_divi_rate: s(),
    divi_pay_dt: s(),
    stk_div_pay_dt: s(),
    odd_pay_dt: s(),
    stk_kind: s(),
    high_divi_gb: s(),
  })
  .passthrough();

export const getKsdDividendDecisionResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: z.array(getKsdDividendDecisionItemSchema).default([]),
  })
  .passthrough();

// ── getKsdStockDividendDecision: Ksd Stock Dividend Decision ──

export const getKsdStockDividendDecisionItemSchema = z
  .object({
    record_date: s(),
    sht_cd: s(),
    isin_name: s(),
    stk_kind: s(),
    opp_opi_rcpt_term: s(),
    buy_req_rcpt_term: s(),
    buy_req_price: s(),
    buy_amt_pay_dt: s(),
    get_meet_dt: s(),
  })
  .passthrough();

export const getKsdStockDividendDecisionResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: z.array(getKsdStockDividendDecisionItemSchema).default([]),
  })
  .passthrough();

// ── getKsdMergerSplitDecision: Ksd Merger Split Decision ──

export const getKsdMergerSplitDecisionItemSchema = z
  .object({
    record_date: s(),
    sht_cd: s(),
    opp_cust_cd: s(),
    opp_cust_nm: s(),
    cust_cd: s(),
    cust_nm: s(),
    merge_type: s(),
    merge_rate: s(),
    td_stop_dt: s(),
    list_dt: s(),
    odd_amt_pay_dt: s(),
    tot_issue_stk_qty: s(),
    issue_stk_qty: s(),
    seq: s(),
  })
  .passthrough();

export const getKsdMergerSplitDecisionResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: z.array(getKsdMergerSplitDecisionItemSchema).default([]),
  })
  .passthrough();

// ── getKsdParValueChangeDecision: Ksd Par Value Change Decision ──

export const getKsdParValueChangeDecisionItemSchema = z
  .object({
    record_date: s(),
    sht_cd: s(),
    isin_name: s(),
    inter_bf_face_amt: s(),
    inter_af_face_amt: s(),
    td_stop_dt: s(),
    list_dt: s(),
  })
  .passthrough();

export const getKsdParValueChangeDecisionResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: z.array(getKsdParValueChangeDecisionItemSchema).default([]),
  })
  .passthrough();

// ── getKsdCapitalReductionSchedule: Ksd Capital Reduction Schedule ──

export const getKsdCapitalReductionScheduleItemSchema = z
  .object({
    record_date: s(),
    sht_cd: s(),
    isin_name: s(),
    stk_kind: s(),
    reduce_cap_type: s(),
    reduce_cap_rate: s(),
    comp_way: s(),
    td_stop_dt: s(),
    list_dt: s(),
  })
  .passthrough();

export const getKsdCapitalReductionScheduleResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: z.array(getKsdCapitalReductionScheduleItemSchema).default([]),
  })
  .passthrough();

// ── getKsdListingInfoSchedule: Ksd Listing Info Schedule ──

export const getKsdListingInfoScheduleItemSchema = z
  .object({
    list_dt: s(),
    sht_cd: s(),
    isin_name: s(),
    stk_kind: s(),
    issue_type: s(),
    issue_stk_qty: s(),
    tot_issue_stk_qty: s(),
    issue_price: s(),
  })
  .passthrough();

export const getKsdListingInfoScheduleResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: z.array(getKsdListingInfoScheduleItemSchema).default([]),
  })
  .passthrough();

// ── getKsdIpoSubscriptionSchedule: Ksd Ipo Subscription Schedule ──

export const getKsdIpoSubscriptionScheduleItemSchema = z
  .object({
    record_date: s(),
    sht_cd: s(),
    isin_name: s(),
    fix_subscr_pri: s(),
    face_value: s(),
    subscr_dt: s(),
    pay_dt: s(),
    refund_dt: s(),
    list_dt: s(),
    lead_mgr: s(),
    pub_bf_cap: s(),
    pub_af_cap: s(),
    assign_stk_qty: s(),
  })
  .passthrough();

export const getKsdIpoSubscriptionScheduleResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: z.array(getKsdIpoSubscriptionScheduleItemSchema).default([]),
  })
  .passthrough();

// ── getKsdForfeitedShareSchedule: Ksd Forfeited Share Schedule ──

export const getKsdForfeitedShareScheduleItemSchema = z
  .object({
    record_date: s(),
    sht_cd: s(),
    isin_name: s(),
    subscr_dt: s(),
    subscr_price: s(),
    subscr_stk_qty: s(),
    refund_dt: s(),
    list_dt: s(),
    lead_mgr: s(),
  })
  .passthrough();

export const getKsdForfeitedShareScheduleResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: z.array(getKsdForfeitedShareScheduleItemSchema).default([]),
  })
  .passthrough();

// ── getKsdDepositSchedule: Ksd Deposit Schedule ──

export const getKsdDepositScheduleItemSchema = z
  .object({
    sht_cd: s(),
    isin_name: s(),
    stk_qty: s(),
    depo_date: s(),
    depo_reason: s(),
    tot_issue_qty_per_rate: s(),
  })
  .passthrough();

export const getKsdDepositScheduleResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: z.array(getKsdDepositScheduleItemSchema).default([]),
  })
  .passthrough();

// ── getKsdPaidInCapitalIncreaseSchedule: Ksd Paid In Capital Increase Schedule ──

export const getKsdPaidInCapitalIncreaseScheduleItemSchema = z
  .object({
    record_date: s(),
    sht_cd: s(),
    isin_name: s(),
    tot_issue_stk_qty: s(),
    issue_stk_qty: s(),
    fix_rate: s(),
    disc_rate: s(),
    fix_price: s(),
    right_dt: s(),
    sub_term_ft: s(),
    sub_term: s(),
    list_date: s(),
    stk_kind: s(),
  })
  .passthrough();

export const getKsdPaidInCapitalIncreaseScheduleResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: z.array(getKsdPaidInCapitalIncreaseScheduleItemSchema).default([]),
  })
  .passthrough();

// ── getKsdStockDividendSchedule: Ksd Stock Dividend Schedule ──

export const getKsdStockDividendScheduleItemSchema = z
  .object({
    record_date: s(),
    sht_cd: s(),
    isin_name: s(),
    fix_rate: s(),
    odd_rec_price: s(),
    right_dt: s(),
    odd_pay_dt: s(),
    list_date: s(),
    tot_issue_stk_qty: s(),
    issue_stk_qty: s(),
    stk_kind: s(),
  })
  .passthrough();

export const getKsdStockDividendScheduleResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: z.array(getKsdStockDividendScheduleItemSchema).default([]),
  })
  .passthrough();

// ── getKsdShareholderMeetingSchedule: Ksd Shareholder Meeting Schedule ──

export const getKsdShareholderMeetingScheduleItemSchema = z
  .object({
    record_date: s(),
    sht_cd: s(),
    isin_name: s(),
    gen_meet_dt: s(),
    gen_meet_type: s(),
    agenda: s(),
    vote_tot_qty: s(),
  })
  .passthrough();

export const getKsdShareholderMeetingScheduleResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: z.array(getKsdShareholderMeetingScheduleItemSchema).default([]),
  })
  .passthrough();

// ── getEstimatedEarnings: Estimated Earnings ──

export const getEstimatedEarningsOutput1ItemSchema = z
  .object({
    sht_cd: s(),
    item_kor_nm: s(),
    name1: s(),
    name2: s(),
    estdate: s(),
    rcmd_name: s(),
    capital: s(),
    forn_item_lmtrt: s(),
  })
  .passthrough();

export const getEstimatedEarningsOutput2ItemSchema = z
  .object({
    data1: s(),
    data2: s(),
    data3: s(),
    data4: s(),
    data5: s(),
  })
  .passthrough();

export const getEstimatedEarningsOutput3ItemSchema = z
  .object({
    data1: s(),
    data2: s(),
    data3: s(),
    data4: s(),
    data5: s(),
  })
  .passthrough();

export const getEstimatedEarningsOutput4ItemSchema = z
  .object({
    dt: s(),
  })
  .passthrough();

export const getEstimatedEarningsResponseSchema = z
  .object({
    ...kisEnvelope,
    output1: getEstimatedEarningsOutput1ItemSchema.optional(),
    output2: z.array(getEstimatedEarningsOutput2ItemSchema).default([]),
    output3: z.array(getEstimatedEarningsOutput3ItemSchema).default([]),
    output4: z.array(getEstimatedEarningsOutput4ItemSchema).default([]),
  })
  .passthrough();

// ── getStockLoanableList: Stock Loanable List ──

export const getStockLoanableListOutput1ItemSchema = z
  .object({
    pdno: s(),
    prdt_name: s(),
    papr: s(),
    bfdy_clpr: s(),
    sbst_prvs: s(),
    tr_stop_dvsn_name: s(),
    psbl_yn_name: s(),
    lmt_qty1: s(),
    use_qty1: s(),
    trad_psbl_qty2: s(),
    rght_type_cd: s(),
    bass_dt: s(),
    psbl_yn: s(),
  })
  .passthrough();

export const getStockLoanableListOutput2ItemSchema = z
  .object({
    tot_stup_lmt_qty: s(),
    brch_lmt_qty: s(),
    rqst_psbl_qty: s(),
  })
  .passthrough();

export const getStockLoanableListResponseSchema = z
  .object({
    ...kisEnvelope,
    ctx_area_fk200: s(),
    ctx_area_nk100: s(),
    output1: z.array(getStockLoanableListOutput1ItemSchema).default([]),
    output2: getStockLoanableListOutput2ItemSchema.optional(),
  })
  .passthrough();

// ── getInvestmentOpinion: Investment Opinion ──

export const getInvestmentOpinionItemSchema = z
  .object({
    stck_bsop_date: s(),
    invt_opnn: s(),
    invt_opnn_cls_code: s(),
    rgbf_invt_opnn: s(),
    rgbf_invt_opnn_cls_code: s(),
    mbcr_name: s(),
    hts_goal_prc: s(),
    stck_prdy_clpr: s(),
    stck_nday_esdg: s(),
    nday_dprt: s(),
    stft_esdg: s(),
    dprt: s(),
  })
  .passthrough();

export const getInvestmentOpinionResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getInvestmentOpinionItemSchema).default([]),
  })
  .passthrough();

// ── getInvestmentOpinionByBrokerage: Investment Opinion By Brokerage ──

export const getInvestmentOpinionByBrokerageItemSchema = z
  .object({
    stck_bsop_date: s(),
    stck_shrn_iscd: s(),
    hts_kor_isnm: s(),
    invt_opnn: s(),
    invt_opnn_cls_code: s(),
    rgbf_invt_opnn: s(),
    rgbf_invt_opnn_cls_code: s(),
    mbcr_name: s(),
    stck_prpr: s(),
    prdy_vrss: s(),
    prdy_vrss_sign: s(),
    prdy_ctrt: s(),
    hts_goal_prc: s(),
    stck_prdy_clpr: s(),
    stft_esdg: s(),
    dprt: s(),
  })
  .passthrough();

export const getInvestmentOpinionByBrokerageResponseSchema = z
  .object({
    ...kisEnvelope,
    output: z.array(getInvestmentOpinionByBrokerageItemSchema).default([]),
  })
  .passthrough();

// ── Response Types ──

export type GetProductBasicInfoResponse = CamelizeKeys<z.infer<typeof getProductBasicInfoResponseSchema>>;

export type GetStockBasicInfoResponse = CamelizeKeys<z.infer<typeof getStockBasicInfoResponseSchema>>;

export type GetBalanceSheetResponse = CamelizeKeys<z.infer<typeof getBalanceSheetResponseSchema>>;

export type GetIncomeStatementResponse = CamelizeKeys<z.infer<typeof getIncomeStatementResponseSchema>>;

export type GetFinancialRatioResponse = CamelizeKeys<z.infer<typeof getFinancialRatioResponseSchema>>;

export type GetProfitabilityRatioResponse = CamelizeKeys<z.infer<typeof getProfitabilityRatioResponseSchema>>;

export type GetOtherKeyRatioResponse = CamelizeKeys<z.infer<typeof getOtherKeyRatioResponseSchema>>;

export type GetStabilityRatioResponse = CamelizeKeys<z.infer<typeof getStabilityRatioResponseSchema>>;

export type GetGrowthRatioResponse = CamelizeKeys<z.infer<typeof getGrowthRatioResponseSchema>>;

export type GetMarginTradableStocksResponse = CamelizeKeys<z.infer<typeof getMarginTradableStocksResponseSchema>>;

export type GetKsdDividendDecisionResponse = CamelizeKeys<z.infer<typeof getKsdDividendDecisionResponseSchema>>;

export type GetKsdStockDividendDecisionResponse = CamelizeKeys<
  z.infer<typeof getKsdStockDividendDecisionResponseSchema>
>;

export type GetKsdMergerSplitDecisionResponse = CamelizeKeys<z.infer<typeof getKsdMergerSplitDecisionResponseSchema>>;

export type GetKsdParValueChangeDecisionResponse = CamelizeKeys<
  z.infer<typeof getKsdParValueChangeDecisionResponseSchema>
>;

export type GetKsdCapitalReductionScheduleResponse = CamelizeKeys<
  z.infer<typeof getKsdCapitalReductionScheduleResponseSchema>
>;

export type GetKsdListingInfoScheduleResponse = CamelizeKeys<z.infer<typeof getKsdListingInfoScheduleResponseSchema>>;

export type GetKsdIpoSubscriptionScheduleResponse = CamelizeKeys<
  z.infer<typeof getKsdIpoSubscriptionScheduleResponseSchema>
>;

export type GetKsdForfeitedShareScheduleResponse = CamelizeKeys<
  z.infer<typeof getKsdForfeitedShareScheduleResponseSchema>
>;

export type GetKsdDepositScheduleResponse = CamelizeKeys<z.infer<typeof getKsdDepositScheduleResponseSchema>>;

export type GetKsdPaidInCapitalIncreaseScheduleResponse = CamelizeKeys<
  z.infer<typeof getKsdPaidInCapitalIncreaseScheduleResponseSchema>
>;

export type GetKsdStockDividendScheduleResponse = CamelizeKeys<
  z.infer<typeof getKsdStockDividendScheduleResponseSchema>
>;

export type GetKsdShareholderMeetingScheduleResponse = CamelizeKeys<
  z.infer<typeof getKsdShareholderMeetingScheduleResponseSchema>
>;

export type GetEstimatedEarningsResponse = CamelizeKeys<z.infer<typeof getEstimatedEarningsResponseSchema>>;

export type GetStockLoanableListResponse = CamelizeKeys<z.infer<typeof getStockLoanableListResponseSchema>>;

export type GetInvestmentOpinionResponse = CamelizeKeys<z.infer<typeof getInvestmentOpinionResponseSchema>>;

export type GetInvestmentOpinionByBrokerageResponse = CamelizeKeys<
  z.infer<typeof getInvestmentOpinionByBrokerageResponseSchema>
>;

// ── Response Map ──

export interface DomesticStockInfoResponseMap {
  getProductBasicInfo: GetProductBasicInfoResponse;
  getStockBasicInfo: GetStockBasicInfoResponse;
  getBalanceSheet: GetBalanceSheetResponse;
  getIncomeStatement: GetIncomeStatementResponse;
  getFinancialRatio: GetFinancialRatioResponse;
  getProfitabilityRatio: GetProfitabilityRatioResponse;
  getOtherKeyRatio: GetOtherKeyRatioResponse;
  getStabilityRatio: GetStabilityRatioResponse;
  getGrowthRatio: GetGrowthRatioResponse;
  getMarginTradableStocks: GetMarginTradableStocksResponse;
  getKsdDividendDecision: GetKsdDividendDecisionResponse;
  getKsdStockDividendDecision: GetKsdStockDividendDecisionResponse;
  getKsdMergerSplitDecision: GetKsdMergerSplitDecisionResponse;
  getKsdParValueChangeDecision: GetKsdParValueChangeDecisionResponse;
  getKsdCapitalReductionSchedule: GetKsdCapitalReductionScheduleResponse;
  getKsdListingInfoSchedule: GetKsdListingInfoScheduleResponse;
  getKsdIpoSubscriptionSchedule: GetKsdIpoSubscriptionScheduleResponse;
  getKsdForfeitedShareSchedule: GetKsdForfeitedShareScheduleResponse;
  getKsdDepositSchedule: GetKsdDepositScheduleResponse;
  getKsdPaidInCapitalIncreaseSchedule: GetKsdPaidInCapitalIncreaseScheduleResponse;
  getKsdStockDividendSchedule: GetKsdStockDividendScheduleResponse;
  getKsdShareholderMeetingSchedule: GetKsdShareholderMeetingScheduleResponse;
  getEstimatedEarnings: GetEstimatedEarningsResponse;
  getStockLoanableList: GetStockLoanableListResponse;
  getInvestmentOpinion: GetInvestmentOpinionResponse;
  getInvestmentOpinionByBrokerage: GetInvestmentOpinionByBrokerageResponse;
}
