import { describe, expect, it } from 'vitest';

import {
  accountCurrentDayStatusResponseSchema,
  accountEvaluationBalanceDetailsResponseSchema,
  accountEvaluationStatusResponseSchema,
  accountNextDaySettlementDetailsResponseSchema,
  accountOrderExecutionDetailsResponseSchema,
  accountOrderExecutionStatusResponseSchema,
  accountProfitRateResponseSchema,
  availableOrderQuantityByMarginLoanStockResponseSchema,
  availableOrderQuantityByMarginRateResponseSchema,
  availableWithdrawalAmountResponseSchema,
  consignmentComprehensiveTransactionHistoryResponseSchema,
  currentDayTradingJournalResponseSchema,
  dailyAccountProfitRateDetailsResponseSchema,
  dailyEstimatedDepositAssetBalanceResponseSchema,
  dailyRealizedProfitLossDetailsResponseSchema,
  dailyRealizedProfitLossResponseSchema,
  dailyStockRealizedProfitLossByDateResponseSchema,
  dailyStockRealizedProfitLossByPeriodResponseSchema,
  depositBalanceDetailsResponseSchema,
  estimatedAssetBalanceResponseSchema,
  executedResponseSchema,
  executionBalanceResponseSchema,
  marginDetailsResponseSchema,
  unexecutedResponseSchema,
  unexecutedSplitOrderDetailsResponseSchema,
} from '../../../src/kiwoom/schemas/domestic-account';

describe('domestic-account response schemas', () => {
  describe('minimal responses (envelope only)', () => {
    const minimalEnvelope = { return_code: '0', return_msg: 'OK' };

    it('ka10072: dailyStockRealizedProfitLossByDate', () => {
      const result = dailyStockRealizedProfitLossByDateResponseSchema.parse(minimalEnvelope);
      expect(result.dt_stk_div_rlzt_pl).toEqual([]);
    });

    it('ka10073: dailyStockRealizedProfitLossByPeriod', () => {
      const result = dailyStockRealizedProfitLossByPeriodResponseSchema.parse(minimalEnvelope);
      expect(result.dt_stk_rlzt_pl).toEqual([]);
    });

    it('ka10074: dailyRealizedProfitLoss', () => {
      const result = dailyRealizedProfitLossResponseSchema.parse(minimalEnvelope);
      expect(result.dt_rlzt_pl).toEqual([]);
      expect(result.tot_buy_amt).toBe('');
    });

    it('ka10075: unexecuted', () => {
      const result = unexecutedResponseSchema.parse(minimalEnvelope);
      expect(result.oso).toEqual([]);
    });

    it('ka10076: executed', () => {
      const result = executedResponseSchema.parse(minimalEnvelope);
      expect(result.cntr).toEqual([]);
    });

    it('ka10077: dailyRealizedProfitLossDetails', () => {
      const result = dailyRealizedProfitLossDetailsResponseSchema.parse(minimalEnvelope);
      expect(result.tdy_rlzt_pl_dtl).toEqual([]);
      expect(result.tdy_rlzt_pl).toBe('');
    });

    it('ka10085: accountProfitRate', () => {
      const result = accountProfitRateResponseSchema.parse(minimalEnvelope);
      expect(result.acnt_prft_rt).toEqual([]);
    });

    it('ka10088: unexecutedSplitOrderDetails', () => {
      const result = unexecutedSplitOrderDetailsResponseSchema.parse(minimalEnvelope);
      expect(result.osop).toEqual([]);
    });

    it('ka10170: currentDayTradingJournal', () => {
      const result = currentDayTradingJournalResponseSchema.parse(minimalEnvelope);
      expect(result.tdy_trde_diary).toEqual([]);
      expect(result.tot_sell_amt).toBe('');
    });

    it('kt00001: depositBalanceDetails', () => {
      const result = depositBalanceDetailsResponseSchema.parse(minimalEnvelope);
      expect(result.stk_entr_prst).toEqual([]);
      expect(result.entr).toBe('');
    });

    it('kt00002: dailyEstimatedDepositAssetBalance', () => {
      const result = dailyEstimatedDepositAssetBalanceResponseSchema.parse(minimalEnvelope);
      expect(result.daly_prsm_dpst_aset_amt_prst).toEqual([]);
    });

    it('kt00003: estimatedAssetBalance', () => {
      const result = estimatedAssetBalanceResponseSchema.parse(minimalEnvelope);
      expect(result.prsm_dpst_aset_amt).toBe('');
    });

    it('kt00004: accountEvaluationStatus', () => {
      const result = accountEvaluationStatusResponseSchema.parse(minimalEnvelope);
      expect(result.stk_acnt_evlt_prst).toEqual([]);
    });

    it('kt00005: executionBalance', () => {
      const result = executionBalanceResponseSchema.parse(minimalEnvelope);
      expect(result.stk_cntr_remn).toEqual([]);
    });

    it('kt00007: accountOrderExecutionDetails', () => {
      const result = accountOrderExecutionDetailsResponseSchema.parse(minimalEnvelope);
      expect(result.acnt_ord_cntr_prps_dtl).toEqual([]);
    });

    it('kt00008: accountNextDaySettlementDetails', () => {
      const result = accountNextDaySettlementDetailsResponseSchema.parse(minimalEnvelope);
      expect(result.acnt_nxdy_setl_frcs_prps_array).toEqual([]);
      expect(result.trde_dt).toBe('');
    });

    it('kt00009: accountOrderExecutionStatus', () => {
      const result = accountOrderExecutionStatusResponseSchema.parse(minimalEnvelope);
      expect(result.acnt_ord_cntr_prst).toEqual([]);
    });

    it('kt00010: availableWithdrawalAmount', () => {
      const result = availableWithdrawalAmountResponseSchema.parse(minimalEnvelope);
      expect(result.entr).toBe('');
    });

    it('kt00011: availableOrderQuantityByMarginRate', () => {
      const result = availableOrderQuantityByMarginRateResponseSchema.parse(minimalEnvelope);
      expect(result.stk_profa_rt).toBe('');
    });

    it('kt00012: availableOrderQuantityByMarginLoanStock', () => {
      const result = availableOrderQuantityByMarginLoanStockResponseSchema.parse(minimalEnvelope);
      expect(result.stk_assr_rt).toBe('');
    });

    it('kt00013: marginDetails', () => {
      const result = marginDetailsResponseSchema.parse(minimalEnvelope);
      expect(result.tdy_reu_objt_amt).toBe('');
    });

    it('kt00015: consignmentComprehensiveTransactionHistory', () => {
      const result = consignmentComprehensiveTransactionHistoryResponseSchema.parse(minimalEnvelope);
      expect(result.trst_ovrl_trde_prps_array).toEqual([]);
    });

    it('kt00016: dailyAccountProfitRateDetails', () => {
      const result = dailyAccountProfitRateDetailsResponseSchema.parse(minimalEnvelope);
      expect(result.mang_empno).toBe('');
    });

    it('kt00017: accountCurrentDayStatus', () => {
      const result = accountCurrentDayStatusResponseSchema.parse(minimalEnvelope);
      expect(result.d2_entra).toBe('');
    });

    it('kt00018: accountEvaluationBalanceDetails', () => {
      const result = accountEvaluationBalanceDetailsResponseSchema.parse(minimalEnvelope);
      expect(result.acnt_evlt_remn_indv_tot).toEqual([]);
    });
  });

  describe('full item responses', () => {
    it('ka10074: parses dailyRealizedProfitLoss with items', () => {
      const input = {
        return_code: 0,
        tot_buy_amt: '1000000',
        tot_sell_amt: '1100000',
        rlzt_pl: '100000',
        trde_cmsn: '500',
        trde_tax: '200',
        dt_rlzt_pl: [
          {
            dt: '20260312',
            buy_amt: '1000000',
            sell_amt: '1100000',
            tdy_sel_pl: '100000',
            tdy_trde_cmsn: '500',
            tdy_trde_tax: '200',
          },
        ],
      };
      const result = dailyRealizedProfitLossResponseSchema.parse(input);
      expect(result.dt_rlzt_pl).toHaveLength(1);
      expect(result.dt_rlzt_pl[0]!.dt).toBe('20260312');
      expect(result.tot_buy_amt).toBe('1000000');
    });

    it('kt00007: parses accountOrderExecutionDetails with items', () => {
      const input = {
        return_code: 0,
        acnt_ord_cntr_prps_dtl: [
          {
            ord_no: '0000001',
            stk_cd: '005930',
            trde_tp: '매수',
            crd_tp: '',
            ord_qty: '10',
            ord_uv: '50000',
            cnfm_qty: '10',
            acpt_tp: '완료',
            rsrv_tp: '',
            ord_tm: '090000',
            ori_ord: '0000000',
            stk_nm: '삼성전자',
            io_tp_nm: '지정가',
            loan_dt: '',
            cntr_qty: '10',
            cntr_uv: '50000',
            ord_remnq: '0',
            comm_ord_tp: 'HTS',
            mdfy_cncl: '',
            cnfm_tm: '090001',
            dmst_stex_tp: 'SOR',
            cond_uv: '0',
          },
        ],
      };
      const result = accountOrderExecutionDetailsResponseSchema.parse(input);
      expect(result.acnt_ord_cntr_prps_dtl).toHaveLength(1);
      expect(result.acnt_ord_cntr_prps_dtl[0]!.stk_cd).toBe('005930');
    });

    it('kt00001: parses depositBalanceDetails scalars', () => {
      const input = {
        return_code: 0,
        entr: '000000001000',
        profa_ch: '000000000500',
        crd_grnt_rt: '0.00',
        '20stk_ord_alow_amt': '000000001000',
        '50stk_ord_alow_amt': '000000000500',
        stk_entr_prst: [],
      };
      const result = depositBalanceDetailsResponseSchema.parse(input);
      expect(result.entr).toBe('000000001000');
      expect(result.crd_grnt_rt).toBe('0.00');
      expect(result['20stk_ord_alow_amt']).toBe('000000001000');
    });

    it('kt00008: parses accountNextDaySettlementDetails', () => {
      const input = {
        return_code: 0,
        trde_dt: '20260312',
        setl_dt: '20260316',
        sell_amt_sum: '000000001000',
        buy_amt_sum: '000000002000',
        acnt_nxdy_setl_frcs_prps_array: [],
      };
      const result = accountNextDaySettlementDetailsResponseSchema.parse(input);
      expect(result.trde_dt).toBe('20260312');
      expect(result.acnt_nxdy_setl_frcs_prps_array).toEqual([]);
    });
  });

  describe('passthrough behavior', () => {
    it('preserves unknown fields in response', () => {
      const input = {
        return_code: '0',
        prsm_dpst_aset_amt: '100',
        unknown_field: 'should be preserved',
      };
      const result = estimatedAssetBalanceResponseSchema.parse(input);
      expect((result as Record<string, unknown>).unknown_field).toBe('should be preserved');
    });

    it('preserves unknown fields in items', () => {
      const input = {
        return_code: '0',
        dt_rlzt_pl: [
          {
            dt: '20260312',
            buy_amt: '0',
            sell_amt: '0',
            tdy_sel_pl: '0',
            tdy_trde_cmsn: '0',
            tdy_trde_tax: '0',
            extra_field: 'hello',
          },
        ],
      };
      const result = dailyRealizedProfitLossResponseSchema.parse(input);
      expect((result.dt_rlzt_pl[0]! as Record<string, unknown>).extra_field).toBe('hello');
    });
  });

  describe('default values for missing fields', () => {
    it('defaults missing item fields to empty string', () => {
      const input = {
        return_code: '0',
        acnt_prft_rt: [{}],
      };
      const result = accountProfitRateResponseSchema.parse(input);
      const item = result.acnt_prft_rt[0]!;
      expect(item.dt).toBe('');
      expect(item.stk_cd).toBe('');
      expect(item.stk_nm).toBe('');
      expect(item.cur_prc).toBe('');
    });

    it('defaults numeric return_code', () => {
      const input = { return_code: 0, return_msg: 'OK' };
      const result = dailyRealizedProfitLossResponseSchema.parse(input);
      expect(result.return_code).toBe(0);
    });
  });
});
