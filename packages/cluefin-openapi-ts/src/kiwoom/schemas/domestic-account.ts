import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types';

const s = () => z.string().default('');

const envelope = {
  return_code: z.union([z.string(), z.number()]).optional(),
  return_msg: z.string().optional(),
};

// ── ka10072: 일자별종목별실현손익(일자) ──

export const dailyStockRealizedProfitLossByDateItemSchema = z
  .object({
    stk_nm: s(),
    cntr_qty: s(),
    buy_uv: s(),
    cntr_pric: s(),
    tdy_sel_pl: s(),
    pl_rt: s(),
    stk_cd: s(),
    tdy_trde_cmsn: s(),
    tdy_trde_tax: s(),
    wthd_alowa: s(),
    loan_dt: s(),
    crd_tp: s(),
    stk_cd_1: s(),
    tdy_sel_pl_1: s(),
  })
  .passthrough();

export const dailyStockRealizedProfitLossByDateResponseSchema = z
  .object({
    ...envelope,
    dt_stk_div_rlzt_pl: z.array(dailyStockRealizedProfitLossByDateItemSchema).default([]),
  })
  .passthrough();

// ── ka10073: 일자별종목별실현손익(기간) ──

export const dailyStockRealizedProfitLossByPeriodItemSchema = z
  .object({
    dt: s(),
    tdy_htssel_cmsn: s(),
    stk_nm: s(),
    cntr_qty: s(),
    buy_uv: s(),
    cntr_pric: s(),
    tdy_sel_pl: s(),
    pl_rt: s(),
    stk_cd: s(),
    tdy_trde_cmsn: s(),
    tdy_trde_tax: s(),
    wthd_alowa: s(),
    loan_dt: s(),
    crd_tp: s(),
  })
  .passthrough();

export const dailyStockRealizedProfitLossByPeriodResponseSchema = z
  .object({
    ...envelope,
    dt_stk_rlzt_pl: z.array(dailyStockRealizedProfitLossByPeriodItemSchema).default([]),
  })
  .passthrough();

// ── ka10074: 일자별실현손익 ──

export const dailyRealizedProfitLossItemSchema = z
  .object({
    dt: s(),
    buy_amt: s(),
    sell_amt: s(),
    tdy_sel_pl: s(),
    tdy_trde_cmsn: s(),
    tdy_trde_tax: s(),
  })
  .passthrough();

export const dailyRealizedProfitLossResponseSchema = z
  .object({
    ...envelope,
    tot_buy_amt: s(),
    tot_sell_amt: s(),
    rlzt_pl: s(),
    trde_cmsn: s(),
    trde_tax: s(),
    dt_rlzt_pl: z.array(dailyRealizedProfitLossItemSchema).default([]),
  })
  .passthrough();

// ── ka10075: 미체결 ──

export const unexecutedItemSchema = z
  .object({
    acnt_no: s(),
    ord_no: s(),
    mang_empno: s(),
    stk_cd: s(),
    tsk_tp: s(),
    ord_stt: s(),
    stk_nm: s(),
    ord_qty: s(),
    ord_pric: s(),
    oso_qty: s(),
    cntr_tot_amt: s(),
    orig_ord_no: s(),
    io_tp_nm: s(),
    trde_tp: s(),
    tm: s(),
    cntr_no: s(),
    cntr_pric: s(),
    cntr_qty: s(),
    cur_prc: s(),
    sel_bid: s(),
    buy_bid: s(),
    unit_cntr_pric: s(),
    unit_cntr_qty: s(),
    tdy_trde_cmsn: s(),
    tdy_trde_tax: s(),
    ind_invsr: s(),
    stex_tp: s(),
    stex_tp_txt: s(),
    sor_yn: s(),
    stop_pric: s(),
  })
  .passthrough();

export const unexecutedResponseSchema = z
  .object({
    ...envelope,
    oso: z.array(unexecutedItemSchema).default([]),
  })
  .passthrough();

// ── ka10076: 체결 ──

export const executedItemSchema = z
  .object({
    ord_no: s(),
    stk_nm: s(),
    io_tp_nm: s(),
    ord_pric: s(),
    ord_qty: s(),
    cntr_pric: s(),
    cntr_qty: s(),
    oso_qty: s(),
    tdy_trde_cmsn: s(),
    tdy_trde_tax: s(),
    ord_stt: s(),
    trde_tp: s(),
    orig_ord_no: s(),
    ord_tm: s(),
    stk_cd: s(),
    stex_tp: s(),
    stex_tp_txt: s(),
    sor_yn: s(),
    stop_pric: s(),
  })
  .passthrough();

export const executedResponseSchema = z
  .object({
    ...envelope,
    cntr: z.array(executedItemSchema).default([]),
  })
  .passthrough();

// ── ka10077: 당일실현손익상세 ──

export const dailyRealizedProfitLossDetailsItemSchema = z
  .object({
    stk_nm: s(),
    cntr_qty: s(),
    buy_uv: s(),
    cntr_pric: s(),
    tdy_sel_pl: s(),
    pl_rt: s(),
    tdy_trde_cmsn: s(),
    tdy_trde_tax: s(),
    stk_cd: s(),
  })
  .passthrough();

export const dailyRealizedProfitLossDetailsResponseSchema = z
  .object({
    ...envelope,
    tdy_rlzt_pl: s(),
    tdy_rlzt_pl_dtl: z.array(dailyRealizedProfitLossDetailsItemSchema).default([]),
  })
  .passthrough();

// ── ka10085: 계좌수익률 ──

export const accountProfitRateItemSchema = z
  .object({
    dt: s(),
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    pur_pric: s(),
    pur_amt: s(),
    rmnd_qty: s(),
    tdy_sel_pl: s(),
    tdy_trde_cmsn: s(),
    tdy_trde_tax: s(),
    crd_tp: s(),
    loan_dt: s(),
    setl_remn: s(),
    clrn_alow_qty: s(),
    crd_amt: s(),
    crd_int: s(),
    expr_dt: s(),
  })
  .passthrough();

export const accountProfitRateResponseSchema = z
  .object({
    ...envelope,
    acnt_prft_rt: z.array(accountProfitRateItemSchema).default([]),
  })
  .passthrough();

// ── ka10088: 미체결분할주문상세 ──

export const unexecutedSplitOrderDetailsItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    ord_no: s(),
    ord_qty: s(),
    ord_pric: s(),
    osop_qty: s(),
    io_tp_nm: s(),
    trde_tp: s(),
    sell_tp: s(),
    cntr_qty: s(),
    ord_stt: s(),
    cur_prc: s(),
    stex_tp: s(),
    stex_tp_txt: s(),
  })
  .passthrough();

export const unexecutedSplitOrderDetailsResponseSchema = z
  .object({
    ...envelope,
    osop: z.array(unexecutedSplitOrderDetailsItemSchema).default([]),
  })
  .passthrough();

// ── ka10170: 당일매매일지 ──

export const currentDayTradingJournalItemSchema = z
  .object({
    stk_nm: s(),
    buy_avg_pric: s(),
    buy_qty: s(),
    sel_avg_pric: s(),
    sell_qty: s(),
    cmsn_alm_tax: s(),
    pl_amt: s(),
    sell_amt: s(),
    buy_amt: s(),
    prft_rt: s(),
    stk_cd: s(),
  })
  .passthrough();

export const currentDayTradingJournalResponseSchema = z
  .object({
    ...envelope,
    tot_sell_amt: s(),
    tot_buy_amt: s(),
    tot_cmsn_tax: s(),
    tot_exct_amt: s(),
    tot_pl_amt: s(),
    tot_prft_rt: s(),
    tdy_trde_diary: z.array(currentDayTradingJournalItemSchema).default([]),
  })
  .passthrough();

// ── kt00001: 예수금상세현황 ──

export const depositBalanceDetailsItemSchema = z
  .object({
    crnc_cd: s(),
    fx_entr: s(),
    fc_krw_repl_evlta: s(),
    fc_trst_profa: s(),
    pymn_alow_amt: s(),
    pymn_alow_amt_entr: s(),
    ord_alow_amt_entr: s(),
    fc_uncla: s(),
    fc_ch_uncla: s(),
    dly_amt: s(),
    d1_fx_entr: s(),
    d2_fx_entr: s(),
    d3_fx_entr: s(),
    d4_fx_entr: s(),
  })
  .passthrough();

export const depositBalanceDetailsResponseSchema = z
  .object({
    ...envelope,
    entr: s(),
    profa_ch: s(),
    bncr_profa_ch: s(),
    nxdy_bncr_sell_exct: s(),
    fc_stk_krw_repl_set_amt: s(),
    crd_grnta_ch: s(),
    crd_grnt_ch: s(),
    add_grnt_ch: s(),
    etc_profa: s(),
    uncl_stk_amt: s(),
    shrts_prica: s(),
    crd_set_grnta: s(),
    chck_ina_amt: s(),
    etc_chck_ina_amt: s(),
    crd_grnt_ruse: s(),
    knx_asset_evltv: s(),
    elwdpst_evlta: s(),
    crd_ls_rght_frcs_amt: s(),
    lvlh_join_amt: s(),
    lvlh_trns_alowa: s(),
    repl_amt: s(),
    remn_repl_evlta: s(),
    trst_remn_repl_evlta: s(),
    bncr_remn_repl_evlta: s(),
    profa_repl: s(),
    crd_grnta_repl: s(),
    crd_grnt_repl: s(),
    add_grnt_repl: s(),
    rght_repl_amt: s(),
    pymn_alow_amt: s(),
    wrap_pymn_alow_amt: s(),
    ord_alow_amt: s(),
    bncr_buy_alowa: s(),
    '20stk_ord_alow_amt': s(),
    '30stk_ord_alow_amt': s(),
    '40stk_ord_alow_amt': s(),
    '100stk_ord_alow_amt': s(),
    ch_uncla: s(),
    ch_uncla_dlfe: s(),
    ch_uncla_tot: s(),
    crd_int_npay: s(),
    int_npay_amt_dlfe: s(),
    int_npay_amt_tot: s(),
    etc_loana: s(),
    etc_loana_dlfe: s(),
    etc_loan_tot: s(),
    nrpy_loan: s(),
    loan_sum: s(),
    ls_sum: s(),
    crd_grnt_rt: s(),
    mdstrm_usfe: s(),
    min_ord_alow_yn: s(),
    loan_remn_evlt_amt: s(),
    dpst_grntl_remn: s(),
    sell_grntl_remn: s(),
    d1_entra: s(),
    d1_slby_exct_amt: s(),
    d1_buy_exct_amt: s(),
    d1_out_rep_mor: s(),
    d1_sel_exct_amt: s(),
    d1_pymn_alow_amt: s(),
    d2_entra: s(),
    d2_slby_exct_amt: s(),
    d2_buy_exct_amt: s(),
    d2_out_rep_mor: s(),
    d2_sel_exct_amt: s(),
    d2_pymn_alow_amt: s(),
    '50stk_ord_alow_amt': s(),
    '60stk_ord_alow_amt': s(),
    stk_entr_prst: z.array(depositBalanceDetailsItemSchema).default([]),
  })
  .passthrough();

// ── kt00002: 일별추정예탁자산현황 ──

export const dailyEstimatedDepositAssetBalanceItemSchema = z
  .object({
    dt: s(),
    entr: s(),
    grnt_use_amt: s(),
    crd_loan: s(),
    ls_grnt: s(),
    repl_amt: s(),
    prsm_dpst_aset_amt: s(),
    prsm_dpst_aset_amt_bncr_skip: s(),
  })
  .passthrough();

export const dailyEstimatedDepositAssetBalanceResponseSchema = z
  .object({
    ...envelope,
    daly_prsm_dpst_aset_amt_prst: z.array(dailyEstimatedDepositAssetBalanceItemSchema).default([]),
  })
  .passthrough();

// ── kt00003: 추정자산조회 ──

export const estimatedAssetBalanceResponseSchema = z
  .object({
    ...envelope,
    prsm_dpst_aset_amt: s(),
  })
  .passthrough();

// ── kt00004: 계좌평가현황 ──

export const accountEvaluationStatusItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    rmnd_qty: s(),
    avg_prc: s(),
    cur_prc: s(),
    evlt_amt: s(),
    pl_amt: s(),
    pl_rt: s(),
    loan_dt: s(),
    pur_amt: s(),
    setl_remn: s(),
    pred_buyq: s(),
    pred_sellq: s(),
    tdy_buyq: s(),
    tdy_sellq: s(),
  })
  .passthrough();

export const accountEvaluationStatusResponseSchema = z
  .object({
    ...envelope,
    acnt_nm: s(),
    brch_nm: s(),
    entr: s(),
    d2_entra: s(),
    tot_est_amt: s(),
    aset_evlt_amt: s(),
    tot_pur_amt: s(),
    prsm_dpst_aset_amt: s(),
    tot_grnt_sella: s(),
    tdy_lspft_amt: s(),
    invt_bsamt: s(),
    lspft_amt: s(),
    tdy_lspft: s(),
    lspft2: s(),
    lspft: s(),
    tdy_lspft_rt: s(),
    lspft_ratio: s(),
    lspft_rt: s(),
    stk_acnt_evlt_prst: z.array(accountEvaluationStatusItemSchema).default([]),
  })
  .passthrough();

// ── kt00005: 체결잔고 ──

export const executionBalanceItemSchema = z
  .object({
    crd_tp: s(),
    loan_dt: s(),
    expr_dt: s(),
    stk_cd: s(),
    stk_nm: s(),
    setl_remn: s(),
    cur_qty: s(),
    cur_prc: s(),
    buy_uv: s(),
    pur_amt: s(),
    evlt_amt: s(),
    evltv_prft: s(),
    pl_rt: s(),
  })
  .passthrough();

export const executionBalanceResponseSchema = z
  .object({
    ...envelope,
    entr: s(),
    entr_d1: s(),
    entr_d2: s(),
    pymn_alow_amt: s(),
    uncl_stk_amt: s(),
    repl_amt: s(),
    rght_repl_amt: s(),
    ord_alowa: s(),
    ch_uncla: s(),
    crd_int_npay_gold: s(),
    etc_loana: s(),
    nrpy_loan: s(),
    profa_ch: s(),
    repl_profa: s(),
    stk_buy_tot_amt: s(),
    evlt_amt_tot: s(),
    tot_pl_tot: s(),
    tot_pl_rt: s(),
    tot_re_buy_alowa: s(),
    '20ord_alow_amt': s(),
    '30ord_alow_amt': s(),
    '40ord_alow_amt': s(),
    '50ord_alow_amt': s(),
    '60ord_alow_amt': s(),
    '100ord_alow_amt': s(),
    crd_loan_tot: s(),
    crd_loan_ls_tot: s(),
    crd_grnt_ch: s(),
    dpst_grnt_use_amt_amt: s(),
    grnt_loan_amt: s(),
    stk_cntr_remn: z.array(executionBalanceItemSchema).default([]),
  })
  .passthrough();

// ── kt00007: 계좌별주문체결내역상세 ──

export const accountOrderExecutionDetailsItemSchema = z
  .object({
    ord_no: s(),
    stk_cd: s(),
    trde_tp: s(),
    crd_tp: s(),
    ord_qty: s(),
    ord_uv: s(),
    cnfm_qty: s(),
    acpt_tp: s(),
    rsrv_tp: s(),
    ord_tm: s(),
    ori_ord: s(),
    stk_nm: s(),
    io_tp_nm: s(),
    loan_dt: s(),
    cntr_qty: s(),
    cntr_uv: s(),
    ord_remnq: s(),
    comm_ord_tp: s(),
    mdfy_cncl: s(),
    cnfm_tm: s(),
    dmst_stex_tp: s(),
    cond_uv: s(),
  })
  .passthrough();

export const accountOrderExecutionDetailsResponseSchema = z
  .object({
    ...envelope,
    acnt_ord_cntr_prps_dtl: z.array(accountOrderExecutionDetailsItemSchema).default([]),
  })
  .passthrough();

// ── kt00008: 계좌별익일결제예정내역 ──

export const accountNextDaySettlementDetailsItemSchema = z
  .object({
    ord_no: s(),
    stk_cd: s(),
    trde_tp: s(),
    crd_tp: s(),
    ord_qty: s(),
    ord_uv: s(),
    cnfm_qty: s(),
    acpt_tp: s(),
    rsrv_tp: s(),
    ord_tm: s(),
    ori_ord: s(),
    stk_nm: s(),
    io_tp_nm: s(),
    loan_dt: s(),
    cntr_qty: s(),
    cntr_uv: s(),
    ord_remnq: s(),
    comm_ord_tp: s(),
    mdfy_cncl: s(),
    cnfm_tm: s(),
    dmst_stex_tp: s(),
    cond_uv: s(),
  })
  .passthrough();

export const accountNextDaySettlementDetailsResponseSchema = z
  .object({
    ...envelope,
    trde_dt: s(),
    setl_dt: s(),
    sell_amt_sum: s(),
    buy_amt_sum: s(),
    acnt_nxdy_setl_frcs_prps_array: z.array(accountNextDaySettlementDetailsItemSchema).default([]),
  })
  .passthrough();

// ── kt00009: 계좌별주문체결현황 ──

export const accountOrderExecutionStatusItemSchema = z
  .object({
    stk_bond_tp: s(),
    ord_no: s(),
    stk_cd: s(),
    trde_tp: s(),
    io_tp_nm: s(),
    ord_qty: s(),
    ord_uv: s(),
    cnfm_qty: s(),
    rsrv_oppo: s(),
    cntr_no: s(),
    acpt_tp: s(),
    orig_ord_no: s(),
    stk_nm: s(),
    setl_tp: s(),
    crd_deal_tp: s(),
    cntr_qty: s(),
    cntr_uv: s(),
    comm_ord_tp: s(),
    mdfy_cncl_tp: s(),
    cntr_tm: s(),
    dmst_stex_tp: s(),
    cond_uv: s(),
  })
  .passthrough();

export const accountOrderExecutionStatusResponseSchema = z
  .object({
    ...envelope,
    sell_grntl_engg_amt: s(),
    buy_engg_amt: s(),
    engg_amt: s(),
    acnt_ord_cntr_prst: z.array(accountOrderExecutionStatusItemSchema).default([]),
  })
  .passthrough();

// ── kt00010: 주문인출가능금액 ──

export const availableWithdrawalAmountResponseSchema = z
  .object({
    ...envelope,
    profa_20ord_alow_amt: s(),
    profa_20ord_alowq: s(),
    profa_30ord_alow_amt: s(),
    profa_30ord_alowq: s(),
    profa_40ord_alow_amt: s(),
    profa_40ord_alowq: s(),
    profa_50ord_alow_amt: s(),
    profa_50ord_alowq: s(),
    profa_60ord_alow_amt: s(),
    profa_60ord_alowq: s(),
    profa_rdex_60ord_alow_amt: s(),
    profa_rdex_60ord_alowq: s(),
    profa_100ord_alow_amt: s(),
    profa_100ord_alowq: s(),
    pred_reu_alowa: s(),
    tdy_reu_alowa: s(),
    entr: s(),
    repl_amt: s(),
    uncla: s(),
    ord_pos_repl: s(),
    ord_alowa: s(),
    wthd_alowa: s(),
    nxdy_wthd_alowa: s(),
    pur_amt: s(),
    cmsn: s(),
    pur_exct_amt: s(),
    d2entra: s(),
    profa_rdex_aplc_tp: s(),
  })
  .passthrough();

// ── kt00011: 증거금율별주문가능수량 ──

export const availableOrderQuantityByMarginRateResponseSchema = z
  .object({
    ...envelope,
    stk_profa_rt: s(),
    profa_rt: s(),
    aplc_rt: s(),
    profa_20ord_alow_amt: s(),
    profa_20ord_alowq: s(),
    profa_20pred_reu_amt: s(),
    profa_20tdy_reu_amt: s(),
    profa_30ord_alow_amt: s(),
    profa_30ord_alowq: s(),
    profa_30pred_reu_amt: s(),
    profa_30tdy_reu_amt: s(),
    profa_40ord_alow_amt: s(),
    profa_40ord_alowq: s(),
    profa_40pred_reu_amt: s(),
    profa_40tdy_reu_amt: s(),
    profa_50ord_alow_amt: s(),
    profa_50ord_alowq: s(),
    profa_50pred_reu_amt: s(),
    profa_50tdy_reu_amt: s(),
    profa_60ord_alow_amt: s(),
    profa_60ord_alowq: s(),
    profa_60pred_reu_amt: s(),
    profa_60tdy_reu_amt: s(),
    profa_100ord_alow_amt: s(),
    profa_100ord_alowq: s(),
    profa_100pred_reu_amt: s(),
    profa_100tdy_reu_amt: s(),
    min_ord_alow_amt: s(),
    min_ord_alowq: s(),
    min_pred_reu_amt: s(),
    min_tdy_reu_amt: s(),
    entr: s(),
    repl_amt: s(),
    uncla: s(),
    ord_pos_repl: s(),
    ord_alowa: s(),
  })
  .passthrough();

// ── kt00012: 신용융자증권별주문가능수량 ──

export const availableOrderQuantityByMarginLoanStockResponseSchema = z
  .object({
    ...envelope,
    stk_assr_rt: s(),
    stk_assr_rt_nm: s(),
    assr_30ord_alow_amt: s(),
    assr_30ord_alowq: s(),
    assr_30pred_reu_amt: s(),
    assr_30tdy_reu_amt: s(),
    assr_40ord_alow_amt: s(),
    assr_40ord_alowq: s(),
    assr_40pred_reu_amt: s(),
    assr_40tdy_reu_amt: s(),
    assr_50ord_alow_amt: s(),
    assr_50ord_alowq: s(),
    assr_50pred_reu_amt: s(),
    assr_50tdy_reu_amt: s(),
    assr_60ord_alow_amt: s(),
    assr_60ord_alowq: s(),
    assr_60pred_reu_amt: s(),
    assr_60tdy_reu_amt: s(),
    entr: s(),
    repl_amt: s(),
    uncla: s(),
    ord_pos_repl: s(),
    ord_alowa: s(),
    out_alowa: s(),
    out_pos_qty: s(),
    min_amt: s(),
    min_qty: s(),
  })
  .passthrough();

// ── kt00013: 증거금세부내역 ──

export const marginDetailsResponseSchema = z
  .object({
    ...envelope,
    tdy_reu_objt_amt: s(),
    tdy_reu_use_amt: s(),
    tdy_reu_alowa: s(),
    tdy_reu_lmtt_amt: s(),
    tdy_reu_alowa_fin: s(),
    pred_reu_objt_amt: s(),
    pred_reu_use_amt: s(),
    pred_reu_alowa: s(),
    pred_reu_lmtt_amt: s(),
    pred_reu_alowa_fin: s(),
    ch_amt: s(),
    ch_profa: s(),
    use_pos_ch: s(),
    ch_use_lmtt_amt: s(),
    use_pos_ch_fin: s(),
    repl_amt_amt: s(),
    repl_profa: s(),
    use_pos_repl: s(),
    repl_use_lmtt_amt: s(),
    use_pos_repl_fin: s(),
    crd_grnta_ch: s(),
    crd_grnta_repl: s(),
    crd_grnt_ch: s(),
    crd_grnt_repl: s(),
    uncla: s(),
    ls_grnt_reu_gold: s(),
    '20ord_alow_amt': s(),
    '30ord_alow_amt': s(),
    '40ord_alow_amt': s(),
    '50ord_alow_amt': s(),
    '60ord_alow_amt': s(),
    '100ord_alow_amt': s(),
    tdy_crd_rpya_loss_amt: s(),
    pred_crd_rpya_loss_amt: s(),
    tdy_ls_rpya_loss_repl_profa: s(),
    pred_ls_rpya_loss_repl_profa: s(),
    evlt_repl_amt_spg_use_skip: s(),
    evlt_repl_rt: s(),
    crd_repl_profa: s(),
    ch_ord_repl_profa: s(),
    crd_ord_repl_profa: s(),
    crd_repl_conv_gold: s(),
    repl_alowa: s(),
    repl_alowa_2: s(),
    ch_repl_lck_gold: s(),
    crd_repl_lck_gold: s(),
    ch_ord_alow_repla: s(),
    crd_ord_alow_repla: s(),
    d2vexct_entr: s(),
    d2ch_ord_alow_amt: s(),
  })
  .passthrough();

// ── kt00015: 위탁종합거래내역 ──

export const consignmentComprehensiveTransactionHistoryItemSchema = z
  .object({
    trde_dt: s(),
    trde_no: s(),
    rmrk_nm: s(),
    crd_deal_tp_nm: s(),
    exct_amt: s(),
    loan_amt_rpya: s(),
    fc_trde_amt: s(),
    fc_exct_amt: s(),
    entra_remn: s(),
    crnc_cd: s(),
    trde_ocr_tp: s(),
    trde_kind_nm: s(),
    stk_nm: s(),
    trde_amt: s(),
    trde_agri_tax: s(),
    rpy_diffa: s(),
    fc_trde_tax: s(),
    dly_sum: s(),
    fc_entra: s(),
    mdia_tp_nm: s(),
    io_tp: s(),
    io_tp_nm: s(),
    orig_deal_no: s(),
    stk_cd: s(),
    trde_qty_jwa_cnt: s(),
    cmsn: s(),
    int_ls_usfe: s(),
    fc_cmsn: s(),
    fc_dly_sum: s(),
    vlbl_nowrm: s(),
    proc_tm: s(),
    isin_cd: s(),
    stex_cd: s(),
    stex_nm: s(),
    trde_unit: s(),
    incm_resi_tax: s(),
    loan_dt: s(),
    uncl_ocr: s(),
    rpym_sum: s(),
    cntr_dt: s(),
    rcpy_no: s(),
    prcsr: s(),
    proc_brch: s(),
    trde_stle: s(),
    txon_base_pric: s(),
    tax_sum_cmsn: s(),
    frgn_pay_txam: s(),
    fc_uncl_ocr: s(),
    rpym_sum_fr: s(),
    rcpmnyer: s(),
    trde_prtc_tp: s(),
  })
  .passthrough();

export const consignmentComprehensiveTransactionHistoryResponseSchema = z
  .object({
    ...envelope,
    acnt_no: s(),
    trst_ovrl_trde_prps_array: z.array(consignmentComprehensiveTransactionHistoryItemSchema).default([]),
  })
  .passthrough();

// ── kt00016: 일별계좌수익률상세현황 ──

export const dailyAccountProfitRateDetailsResponseSchema = z
  .object({
    ...envelope,
    mang_empno: s(),
    mngr_nm: s(),
    dept_nm: s(),
    entr_fr: s(),
    entr_to: s(),
    scrt_evlt_amt_fr: s(),
    scrt_evlt_amt_to: s(),
    ls_grnt_fr: s(),
    ls_grnt_to: s(),
    crd_loan_fr: s(),
    crd_loan_to: s(),
    ch_uncla_fr: s(),
    ch_uncla_to: s(),
    krw_asgna_fr: s(),
    krw_asgna_to: s(),
    ls_evlta_fr: s(),
    ls_evlta_to: s(),
    rght_evlta_fr: s(),
    rght_evlta_to: s(),
    loan_amt_fr: s(),
    loan_amt_to: s(),
    etc_loana_fr: s(),
    etc_loana_to: s(),
    crd_int_npay_gold_fr: s(),
    crd_int_npay_gold_to: s(),
    crd_int_fr: s(),
    crd_int_to: s(),
    tot_amt_fr: s(),
    tot_amt_to: s(),
    invt_bsamt: s(),
    evltv_prft: s(),
    prft_rt: s(),
    tern_rt: s(),
    termin_tot_trns: s(),
    termin_tot_pymn: s(),
    termin_tot_inq: s(),
    termin_tot_outq: s(),
    futr_repl_sella: s(),
    trst_repl_sella: s(),
  })
  .passthrough();

// ── kt00017: 계좌별당일현황 ──

export const accountCurrentDayStatusResponseSchema = z
  .object({
    ...envelope,
    d2_entra: s(),
    crd_int_npay_gold: s(),
    etc_loana: s(),
    gnrl_stk_evlt_amt_d2: s(),
    dpst_grnt_use_amt_d2: s(),
    crd_stk_evlt_amt_d2: s(),
    crd_loan_d2: s(),
    crd_loan_evlta_d2: s(),
    crd_ls_grnt_d2: s(),
    crd_ls_evlta_d2: s(),
    ina_amt: s(),
    outa: s(),
    inq_amt: s(),
    outq_amt: s(),
    sell_amt: s(),
    buy_amt: s(),
    cmsn: s(),
    tax: s(),
    stk_pur_cptal_loan_amt: s(),
    rp_evlt_amt: s(),
    bd_evlt_amt: s(),
    elsevlt_amt: s(),
    crd_int_amt: s(),
    sel_prica_grnt_loan_int_amt_amt: s(),
    dvida_amt: s(),
  })
  .passthrough();

// ── kt00018: 계좌평가잔고내역 ──

export const accountEvaluationBalanceDetailsItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    evltv_prft: s(),
    prft_rt: s(),
    pur_pric: s(),
    pred_close_pric: s(),
    rmnd_qty: s(),
    trde_able_qty: s(),
    cur_prc: s(),
    pred_buyq: s(),
    pred_sellq: s(),
    tdy_buyq: s(),
    tdy_sellq: s(),
    pur_amt: s(),
    pur_cmsn: s(),
    evlt_amt: s(),
    sell_cmsn: s(),
    tax: s(),
    sum_cmsn: s(),
    poss_rt: s(),
    crd_tp: s(),
    crd_tp_nm: s(),
    crd_loan_dt: s(),
  })
  .passthrough();

export const accountEvaluationBalanceDetailsResponseSchema = z
  .object({
    ...envelope,
    tot_pur_amt: s(),
    tot_evlt_amt: s(),
    tot_evlt_pl: s(),
    tot_prft_rt: s(),
    prsm_dpst_aset_amt: s(),
    tot_loan_amt: s(),
    tot_crd_loan_amt: s(),
    tot_crd_ls_amt: s(),
    acnt_evlt_remn_indv_tot: z.array(accountEvaluationBalanceDetailsItemSchema).default([]),
  })
  .passthrough();

// ── Response Types ──

export type DailyStockRealizedProfitLossByDateResponse = CamelizeKeys<
  z.infer<typeof dailyStockRealizedProfitLossByDateResponseSchema>
>;
export type DailyStockRealizedProfitLossByPeriodResponse = CamelizeKeys<
  z.infer<typeof dailyStockRealizedProfitLossByPeriodResponseSchema>
>;
export type DailyRealizedProfitLossResponse = CamelizeKeys<z.infer<typeof dailyRealizedProfitLossResponseSchema>>;
export type UnexecutedResponse = CamelizeKeys<z.infer<typeof unexecutedResponseSchema>>;
export type ExecutedResponse = CamelizeKeys<z.infer<typeof executedResponseSchema>>;
export type DailyRealizedProfitLossDetailsResponse = CamelizeKeys<
  z.infer<typeof dailyRealizedProfitLossDetailsResponseSchema>
>;
export type AccountProfitRateResponse = CamelizeKeys<z.infer<typeof accountProfitRateResponseSchema>>;
export type UnexecutedSplitOrderDetailsResponse = CamelizeKeys<
  z.infer<typeof unexecutedSplitOrderDetailsResponseSchema>
>;
export type CurrentDayTradingJournalResponse = CamelizeKeys<z.infer<typeof currentDayTradingJournalResponseSchema>>;
export type DepositBalanceDetailsResponse = CamelizeKeys<z.infer<typeof depositBalanceDetailsResponseSchema>>;
export type DailyEstimatedDepositAssetBalanceResponse = CamelizeKeys<
  z.infer<typeof dailyEstimatedDepositAssetBalanceResponseSchema>
>;
export type EstimatedAssetBalanceResponse = CamelizeKeys<z.infer<typeof estimatedAssetBalanceResponseSchema>>;
export type AccountEvaluationStatusResponse = CamelizeKeys<z.infer<typeof accountEvaluationStatusResponseSchema>>;
export type ExecutionBalanceResponse = CamelizeKeys<z.infer<typeof executionBalanceResponseSchema>>;
export type AccountOrderExecutionDetailsResponse = CamelizeKeys<
  z.infer<typeof accountOrderExecutionDetailsResponseSchema>
>;
export type AccountNextDaySettlementDetailsResponse = CamelizeKeys<
  z.infer<typeof accountNextDaySettlementDetailsResponseSchema>
>;
export type AccountOrderExecutionStatusResponse = CamelizeKeys<
  z.infer<typeof accountOrderExecutionStatusResponseSchema>
>;
export type AvailableWithdrawalAmountResponse = CamelizeKeys<z.infer<typeof availableWithdrawalAmountResponseSchema>>;
export type AvailableOrderQuantityByMarginRateResponse = CamelizeKeys<
  z.infer<typeof availableOrderQuantityByMarginRateResponseSchema>
>;
export type AvailableOrderQuantityByMarginLoanStockResponse = CamelizeKeys<
  z.infer<typeof availableOrderQuantityByMarginLoanStockResponseSchema>
>;
export type MarginDetailsResponse = CamelizeKeys<z.infer<typeof marginDetailsResponseSchema>>;
export type ConsignmentComprehensiveTransactionHistoryResponse = CamelizeKeys<
  z.infer<typeof consignmentComprehensiveTransactionHistoryResponseSchema>
>;
export type DailyAccountProfitRateDetailsResponse = CamelizeKeys<
  z.infer<typeof dailyAccountProfitRateDetailsResponseSchema>
>;
export type AccountCurrentDayStatusResponse = CamelizeKeys<z.infer<typeof accountCurrentDayStatusResponseSchema>>;
export type AccountEvaluationBalanceDetailsResponse = CamelizeKeys<
  z.infer<typeof accountEvaluationBalanceDetailsResponseSchema>
>;

// ── Response Map ──

export interface DomesticAccountResponseMap {
  getDailyStockRealizedProfitLossByDate: DailyStockRealizedProfitLossByDateResponse;
  getDailyStockRealizedProfitLossByPeriod: DailyStockRealizedProfitLossByPeriodResponse;
  getDailyRealizedProfitLoss: DailyRealizedProfitLossResponse;
  getUnexecuted: UnexecutedResponse;
  getExecuted: ExecutedResponse;
  getDailyRealizedProfitLossDetails: DailyRealizedProfitLossDetailsResponse;
  getAccountProfitRate: AccountProfitRateResponse;
  getUnexecutedSplitOrderDetails: UnexecutedSplitOrderDetailsResponse;
  getCurrentDayTradingJournal: CurrentDayTradingJournalResponse;
  getDepositBalanceDetails: DepositBalanceDetailsResponse;
  getDailyEstimatedDepositAssetBalance: DailyEstimatedDepositAssetBalanceResponse;
  getEstimatedAssetBalance: EstimatedAssetBalanceResponse;
  getAccountEvaluationStatus: AccountEvaluationStatusResponse;
  getExecutionBalance: ExecutionBalanceResponse;
  getAccountOrderExecutionDetails: AccountOrderExecutionDetailsResponse;
  getAccountNextDaySettlementDetails: AccountNextDaySettlementDetailsResponse;
  getAccountOrderExecutionStatus: AccountOrderExecutionStatusResponse;
  getAvailableWithdrawalAmount: AvailableWithdrawalAmountResponse;
  getAvailableOrderQuantityByMarginRate: AvailableOrderQuantityByMarginRateResponse;
  getAvailableOrderQuantityByMarginLoanStock: AvailableOrderQuantityByMarginLoanStockResponse;
  getMarginDetails: MarginDetailsResponse;
  getConsignmentComprehensiveTransactionHistory: ConsignmentComprehensiveTransactionHistoryResponse;
  getDailyAccountProfitRateDetails: DailyAccountProfitRateDetailsResponse;
  getAccountCurrentDayStatus: AccountCurrentDayStatusResponse;
  getAccountEvaluationBalanceDetails: AccountEvaluationBalanceDetailsResponse;
}
