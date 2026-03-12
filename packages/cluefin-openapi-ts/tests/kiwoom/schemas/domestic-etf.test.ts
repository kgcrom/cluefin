import { describe, expect, it } from 'vitest';

import {
  etfDailyExecutionResponseSchema,
  etfDailyTrendResponseSchema,
  etfFullPriceResponseSchema,
  etfHourlyExecutionResponseSchema,
  etfHourlyExecutionV2ResponseSchema,
  etfHourlyTrendResponseSchema,
  etfHourlyTrendV2ResponseSchema,
  etfItemInfoResponseSchema,
  etfReturnRateResponseSchema,
} from '../../../src/kiwoom/schemas/domestic-etf';

describe('domestic-etf response schemas', () => {
  describe('minimal responses (envelope only)', () => {
    const minimalEnvelope = { return_code: '0', return_msg: 'OK' };

    it('ka40001: etfReturnRate', () => {
      const result = etfReturnRateResponseSchema.parse(minimalEnvelope);
      expect(result.etfprft_rt_lst).toEqual([]);
    });

    it('ka40002: etfItemInfo', () => {
      const result = etfItemInfoResponseSchema.parse(minimalEnvelope);
      expect(result.stk_nm).toBe('');
      expect(result.etfobjt_idex_nm).toBe('');
      expect(result.wonju_pric).toBe('');
      expect(result.etftxon_type).toBe('');
      expect(result.etntxon_type).toBe('');
    });

    it('ka40003: etfDailyTrend', () => {
      const result = etfDailyTrendResponseSchema.parse(minimalEnvelope);
      expect(result.etfdaly_trnsn).toEqual([]);
    });

    it('ka40004: etfFullPrice', () => {
      const result = etfFullPriceResponseSchema.parse(minimalEnvelope);
      expect(result.etfall_mrpr).toEqual([]);
    });

    it('ka40006: etfHourlyTrend', () => {
      const result = etfHourlyTrendResponseSchema.parse(minimalEnvelope);
      expect(result.etftisl_trnsn).toEqual([]);
      expect(result.stk_nm).toBe('');
      expect(result.etfobjt_idex_nm).toBe('');
      expect(result.wonju_pric).toBe('');
      expect(result.etftxon_type).toBe('');
      expect(result.etntxon_type).toBe('');
    });

    it('ka40007: etfHourlyExecution', () => {
      const result = etfHourlyExecutionResponseSchema.parse(minimalEnvelope);
      expect(result.etftisl_cntr_array).toEqual([]);
      expect(result.stk_cls).toBe('');
      expect(result.stk_nm).toBe('');
      expect(result.etfobjt_idex_nm).toBe('');
      expect(result.etfobjt_idex_cd).toBe('');
      expect(result.objt_idex_pre_rt).toBe('');
      expect(result.wonju_pric).toBe('');
    });

    it('ka40008: etfDailyExecution', () => {
      const result = etfDailyExecutionResponseSchema.parse(minimalEnvelope);
      expect(result.etfnetprps_qty_array).toEqual([]);
      expect(result.cntr_tm).toBe('');
      expect(result.cur_prc).toBe('');
      expect(result.pre_sig).toBe('');
      expect(result.pred_pre).toBe('');
      expect(result.trde_qty).toBe('');
    });

    it('ka40009: etfHourlyExecutionV2', () => {
      const result = etfHourlyExecutionV2ResponseSchema.parse(minimalEnvelope);
      expect(result.etfnavarray).toEqual([]);
    });

    it('ka40010: etfHourlyTrendV2', () => {
      const result = etfHourlyTrendV2ResponseSchema.parse(minimalEnvelope);
      expect(result.etftisl_trnsn).toEqual([]);
    });
  });

  describe('full item responses', () => {
    it('ka40003: parses daily trend item', () => {
      const input = {
        return_code: '0',
        etfdaly_trnsn: [
          {
            cntr_dt: '20260313',
            cur_prc: '57230',
            pre_sig: '2',
            pred_pre: '310',
            pre_rt: '0.54',
            trde_qty: '3456789',
            nav: '57250',
            acc_trde_prica: '197654321',
            navidex_dispty_rt: '0.01',
            navetfdispty_rt: '0.03',
            trace_eor_rt: '0.02',
            trace_cur_prc: '2850',
            trace_pred_pre: '15',
            trace_pre_sig: '2',
          },
        ],
      };
      const result = etfDailyTrendResponseSchema.parse(input);
      expect(result.etfdaly_trnsn).toHaveLength(1);
      expect(result.etfdaly_trnsn[0].cntr_dt).toBe('20260313');
      expect(result.etfdaly_trnsn[0].nav).toBe('57250');
    });

    it('ka40004: parses full price item', () => {
      const input = {
        return_code: '0',
        etfall_mrpr: [
          {
            stk_cd: '069500',
            stk_cls: 'ETF',
            stk_nm: 'KODEX 200',
            close_pric: '57230',
            pre_sig: '2',
            pred_pre: '310',
            pre_rt: '0.54',
            trde_qty: '3456789',
            nav: '57250',
            trace_eor_rt: '0.02',
            txbs: '57100',
            dvid_bf_base: '57000',
            pred_dvida: '0',
            trace_idex_nm: 'KOSPI200',
            drng: '1',
            trace_idex_cd: '001',
            trace_idex: '385.50',
            trace_flu_rt: '0.55',
          },
        ],
      };
      const result = etfFullPriceResponseSchema.parse(input);
      expect(result.etfall_mrpr).toHaveLength(1);
      expect(result.etfall_mrpr[0].stk_nm).toBe('KODEX 200');
      expect(result.etfall_mrpr[0].trace_idex_nm).toBe('KOSPI200');
    });

    it('ka40008: parses daily execution with scalar fields', () => {
      const input = {
        return_code: '0',
        cntr_tm: '153000',
        cur_prc: '57230',
        pre_sig: '2',
        pred_pre: '310',
        trde_qty: '3456789',
        etfnetprps_qty_array: [
          {
            dt: '20260313',
            cur_prc_n: '57230',
            pre_sig_n: '2',
            pred_pre_n: '310',
            acc_trde_qty: '3456789',
            for_netprps_qty: '123456',
            orgn_netprps_qty: '-78901',
          },
        ],
      };
      const result = etfDailyExecutionResponseSchema.parse(input);
      expect(result.cntr_tm).toBe('153000');
      expect(result.etfnetprps_qty_array).toHaveLength(1);
      expect(result.etfnetprps_qty_array[0].for_netprps_qty).toBe('123456');
    });
  });

  describe('passthrough behavior', () => {
    it('preserves unknown fields in response', () => {
      const input = {
        return_code: '0',
        etfprft_rt_lst: [],
        unknown_field: 'should be preserved',
      };
      const result = etfReturnRateResponseSchema.parse(input);
      expect((result as Record<string, unknown>).unknown_field).toBe('should be preserved');
    });

    it('preserves unknown fields in items', () => {
      const input = {
        return_code: '0',
        etfdaly_trnsn: [
          {
            cntr_dt: '20260313',
            cur_prc: '57230',
            pre_sig: '2',
            pred_pre: '310',
            pre_rt: '0.54',
            trde_qty: '3456789',
            nav: '57250',
            acc_trde_prica: '197654321',
            navidex_dispty_rt: '0.01',
            navetfdispty_rt: '0.03',
            trace_eor_rt: '0.02',
            trace_cur_prc: '2850',
            trace_pred_pre: '15',
            trace_pre_sig: '2',
            extra_field: 'hello',
          },
        ],
      };
      const result = etfDailyTrendResponseSchema.parse(input);
      expect((result.etfdaly_trnsn[0] as Record<string, unknown>).extra_field).toBe('hello');
    });
  });

  describe('default values for missing fields', () => {
    it('defaults missing item fields to empty string', () => {
      const input = {
        return_code: '0',
        etfprft_rt_lst: [{}],
      };
      const result = etfReturnRateResponseSchema.parse(input);
      const item = result.etfprft_rt_lst[0];
      expect(item.etfprft_rt).toBe('');
      expect(item.cntr_prft_rt).toBe('');
      expect(item.for_netprps_qty).toBe('');
      expect(item.orgn_netprps_qty).toBe('');
    });

    it('defaults numeric return_code', () => {
      const input = { return_code: 0, return_msg: 'OK' };
      const result = etfReturnRateResponseSchema.parse(input);
      expect(result.return_code).toBe(0);
    });
  });
});
