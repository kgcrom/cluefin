import { describe, expect, it } from 'vitest';

import {
  individualStockInstitutionalChartResponseSchema,
  industryDailyResponseSchema,
  industryMinuteResponseSchema,
  industryMonthlyResponseSchema,
  industryTickResponseSchema,
  industryWeeklyResponseSchema,
  industryYearlyResponseSchema,
  intradayInvestorTradingResponseSchema,
  stockDailyResponseSchema,
  stockMinuteResponseSchema,
  stockMonthlyResponseSchema,
  stockTickResponseSchema,
  stockWeeklyResponseSchema,
  stockYearlyResponseSchema,
} from '../../../src/kiwoom/schemas/domestic-chart';

describe('domestic-chart response schemas', () => {
  describe('minimal responses (envelope only)', () => {
    const minimalEnvelope = { return_code: '0', return_msg: 'OK' };

    it('ka10060: individualStockInstitutionalChart', () => {
      const result = individualStockInstitutionalChartResponseSchema.parse(minimalEnvelope);
      expect(result.stk_invsr_orgn_chart).toEqual([]);
    });

    it('ka10064: intradayInvestorTrading', () => {
      const result = intradayInvestorTradingResponseSchema.parse(minimalEnvelope);
      expect(result.opmr_invsr_trde_chart).toEqual([]);
    });

    it('ka10079: stockTick', () => {
      const result = stockTickResponseSchema.parse(minimalEnvelope);
      expect(result.stk_tic_chart_qry).toEqual([]);
      expect(result.stk_cd).toBe('');
      expect(result.last_tic_cnt).toBe('');
    });

    it('ka10080: stockMinute', () => {
      const result = stockMinuteResponseSchema.parse(minimalEnvelope);
      expect(result.stk_min_pole_chart_qry).toEqual([]);
      expect(result.stk_cd).toBe('');
    });

    it('ka10081: stockDaily', () => {
      const result = stockDailyResponseSchema.parse(minimalEnvelope);
      expect(result.stk_dt_pole_chart_qry).toEqual([]);
      expect(result.stk_cd).toBe('');
    });

    it('ka10082: stockWeekly', () => {
      const result = stockWeeklyResponseSchema.parse(minimalEnvelope);
      expect(result.stk_stk_pole_chart_qry).toEqual([]);
      expect(result.stk_cd).toBe('');
    });

    it('ka10083: stockMonthly', () => {
      const result = stockMonthlyResponseSchema.parse(minimalEnvelope);
      expect(result.stk_mth_pole_chart_qry).toEqual([]);
      expect(result.stk_cd).toBe('');
    });

    it('ka10094: stockYearly', () => {
      const result = stockYearlyResponseSchema.parse(minimalEnvelope);
      expect(result.stk_yr_pole_chart_qry).toEqual([]);
      expect(result.stk_cd).toBe('');
    });

    it('ka20004: industryTick', () => {
      const result = industryTickResponseSchema.parse(minimalEnvelope);
      expect(result.inds_tic_chart_qry).toEqual([]);
      expect(result.inds_cd).toBe('');
    });

    it('ka20005: industryMinute', () => {
      const result = industryMinuteResponseSchema.parse(minimalEnvelope);
      expect(result.inds_min_pole_qry).toEqual([]);
      expect(result.inds_cd).toBe('');
    });

    it('ka20006: industryDaily', () => {
      const result = industryDailyResponseSchema.parse(minimalEnvelope);
      expect(result.inds_dt_pole_qry).toEqual([]);
      expect(result.inds_cd).toBe('');
    });

    it('ka20007: industryWeekly', () => {
      const result = industryWeeklyResponseSchema.parse(minimalEnvelope);
      expect(result.inds_stk_pole_qry).toEqual([]);
      expect(result.inds_cd).toBe('');
    });

    it('ka20008: industryMonthly', () => {
      const result = industryMonthlyResponseSchema.parse(minimalEnvelope);
      expect(result.inds_mth_pole_qry).toEqual([]);
      expect(result.inds_cd).toBe('');
    });

    it('ka20019: industryYearly', () => {
      const result = industryYearlyResponseSchema.parse(minimalEnvelope);
      expect(result.inds_yr_pole_qry).toEqual([]);
      expect(result.inds_cd).toBe('');
    });
  });

  describe('full item responses', () => {
    it('ka10060: parses institutional chart item', () => {
      const input = {
        return_code: '0',
        stk_invsr_orgn_chart: [
          {
            dt: '20260312',
            cur_prc: '187900',
            pred_pre: '-2100',
            acc_trde_prica: '20440753',
            ind_invsr: '805003',
            frgnr_invsr: '-916156',
            orgn: '77668',
            fnnc_invt: '-33438',
            insrnc: '4329',
            invtrt: '216',
            etc_fnnc: '-28372',
            bank: '651',
            penfnd_etc: '19291',
            samo_fund: '114992',
            natn: '0',
            etc_corp: '29568',
            natfor: '3917',
          },
        ],
      };
      const result = individualStockInstitutionalChartResponseSchema.parse(input);
      expect(result.stk_invsr_orgn_chart).toHaveLength(1);
      expect(result.stk_invsr_orgn_chart[0]!.dt).toBe('20260312');
    });

    it('ka10081: parses stock daily OHLCV item', () => {
      const input = {
        return_code: '0',
        stk_cd: '005930',
        stk_dt_pole_chart_qry: [
          {
            cur_prc: '187900',
            trde_qty: '20440753',
            trde_prica: '3832551',
            dt: '20260312',
            open_pric: '186600',
            high_pric: '190000',
            low_pric: '185900',
            pred_pre: '-2100',
            pred_pre_sig: '5',
            trde_tern_rt: '+0.35',
          },
        ],
      };
      const result = stockDailyResponseSchema.parse(input);
      expect(result.stk_cd).toBe('005930');
      expect(result.stk_dt_pole_chart_qry).toHaveLength(1);
      expect(result.stk_dt_pole_chart_qry[0]!.open_pric).toBe('186600');
    });

    it('ka20006: parses industry daily item', () => {
      const input = {
        return_code: '0',
        inds_cd: '001',
        inds_dt_pole_qry: [
          {
            cur_prc: '558325',
            trde_qty: '801306',
            dt: '20260312',
            open_pric: '556765',
            high_pric: '562907',
            low_pric: '552747',
            trde_prica: '23698184',
          },
        ],
      };
      const result = industryDailyResponseSchema.parse(input);
      expect(result.inds_cd).toBe('001');
      expect(result.inds_dt_pole_qry).toHaveLength(1);
    });
  });

  describe('passthrough behavior', () => {
    it('preserves unknown fields in response', () => {
      const input = {
        return_code: '0',
        stk_cd: '005930',
        stk_dt_pole_chart_qry: [],
        unknown_field: 'should be preserved',
      };
      const result = stockDailyResponseSchema.parse(input);
      expect((result as Record<string, unknown>).unknown_field).toBe('should be preserved');
    });

    it('preserves unknown fields in items', () => {
      const input = {
        return_code: '0',
        stk_cd: '005930',
        stk_dt_pole_chart_qry: [
          {
            cur_prc: '187900',
            trde_qty: '20440753',
            trde_prica: '3832551',
            dt: '20260312',
            open_pric: '186600',
            high_pric: '190000',
            low_pric: '185900',
            pred_pre: '-2100',
            pred_pre_sig: '5',
            trde_tern_rt: '+0.35',
            extra_field: 'hello',
          },
        ],
      };
      const result = stockDailyResponseSchema.parse(input);
      expect((result.stk_dt_pole_chart_qry[0]! as Record<string, unknown>).extra_field).toBe('hello');
    });
  });

  describe('default values for missing fields', () => {
    it('defaults missing item fields to empty string', () => {
      const input = {
        return_code: '0',
        stk_cd: '005930',
        stk_yr_pole_chart_qry: [{}],
      };
      const result = stockYearlyResponseSchema.parse(input);
      const item = result.stk_yr_pole_chart_qry[0]!;
      expect(item.cur_prc).toBe('');
      expect(item.trde_qty).toBe('');
      expect(item.dt).toBe('');
      expect(item.open_pric).toBe('');
      expect(item.high_pric).toBe('');
      expect(item.low_pric).toBe('');
    });

    it('defaults numeric return_code', () => {
      const input = { return_code: 0, return_msg: 'OK' };
      const result = stockDailyResponseSchema.parse(input);
      expect(result.return_code).toBe(0);
    });
  });
});
