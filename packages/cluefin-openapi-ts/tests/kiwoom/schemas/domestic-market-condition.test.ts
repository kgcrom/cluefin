import { describe, expect, it } from 'vitest';

import {
  afterHoursSinglePriceResponseSchema,
  afterMarketTradingByInvestorResponseSchema,
  dailyInstitutionalTradingItemsResponseSchema,
  dailyStockPriceResponseSchema,
  executionIntensityTrendByDateResponseSchema,
  executionIntensityTrendByTimeResponseSchema,
  institutionalTradingTrendByStockResponseSchema,
  intradayTradingByInvestorResponseSchema,
  marketSentimentInfoResponseSchema,
  newStockWarrantPriceResponseSchema,
  programTradingArbitrageBalanceTrendResponseSchema,
  programTradingCumulativeTrendResponseSchema,
  programTradingTrendByDateResponseSchema,
  programTradingTrendByStockAndDateResponseSchema,
  programTradingTrendByStockAndTimeResponseSchema,
  programTradingTrendByTimeResponseSchema,
  securitiesFirmTradingTrendByStockResponseSchema,
  stockPriceResponseSchema,
  stockQuoteByDateResponseSchema,
  stockQuoteResponseSchema,
} from '../../../src/kiwoom/schemas/domestic-market-condition';

describe('domestic-market-condition response schemas', () => {
  describe('minimal responses (envelope only)', () => {
    const minimalEnvelope = { return_code: '0', return_msg: 'OK' };

    it('ka10004: stockQuote', () => {
      const result = stockQuoteResponseSchema.parse(minimalEnvelope);
      expect(result.bid_req_base_tm).toBe('');
      expect(result.tot_sel_req).toBe('');
      expect(result.tot_buy_req).toBe('');
    });

    it('ka10005: stockQuoteByDate', () => {
      const result = stockQuoteByDateResponseSchema.parse(minimalEnvelope);
      expect(result.stk_ddwkmm).toEqual([]);
    });

    it('ka10006: stockPrice', () => {
      const result = stockPriceResponseSchema.parse(minimalEnvelope);
      expect(result.date).toBe('');
      expect(result.close_pric).toBe('');
      expect(result.cntr_str).toBe('');
    });

    it('ka10007: marketSentimentInfo', () => {
      const result = marketSentimentInfoResponseSchema.parse(minimalEnvelope);
      expect(result.stk_nm).toBe('');
      expect(result.stk_cd).toBe('');
      expect(result.tot_buy_req).toBe('');
    });

    it('ka10011: newStockWarrantPrice', () => {
      const result = newStockWarrantPriceResponseSchema.parse(minimalEnvelope);
      expect(result.newstk_recvrht_mrpr).toEqual([]);
    });

    it('ka10044: dailyInstitutionalTradingItems', () => {
      const result = dailyInstitutionalTradingItemsResponseSchema.parse(minimalEnvelope);
      expect(result.daly_orgn_trde_stk).toEqual([]);
    });

    it('ka10045: institutionalTradingTrendByStock', () => {
      const result = institutionalTradingTrendByStockResponseSchema.parse(minimalEnvelope);
      expect(result.stk_orgn_trde_trnsn).toEqual([]);
      expect(result.orgn_prsm_avg_pric).toBe('');
      expect(result.for_prsm_avg_pric).toBe('');
    });

    it('ka10046: executionIntensityTrendByTime', () => {
      const result = executionIntensityTrendByTimeResponseSchema.parse(minimalEnvelope);
      expect(result.cntr_str_tm).toEqual([]);
    });

    it('ka10047: executionIntensityTrendByDate', () => {
      const result = executionIntensityTrendByDateResponseSchema.parse(minimalEnvelope);
      expect(result.cntr_str_daly).toEqual([]);
    });

    it('ka10063: intradayTradingByInvestor', () => {
      const result = intradayTradingByInvestorResponseSchema.parse(minimalEnvelope);
      expect(result.opmr_invsr_trde).toEqual([]);
    });

    it('ka10066: afterMarketTradingByInvestor', () => {
      const result = afterMarketTradingByInvestorResponseSchema.parse(minimalEnvelope);
      expect(result.opaf_invsr_trde).toEqual([]);
    });

    it('ka10078: securitiesFirmTradingTrendByStock', () => {
      const result = securitiesFirmTradingTrendByStockResponseSchema.parse(minimalEnvelope);
      expect(result.sec_stk_trde_trend).toEqual([]);
    });

    it('ka10086: dailyStockPrice', () => {
      const result = dailyStockPriceResponseSchema.parse(minimalEnvelope);
      expect(result.daly_stkpc).toEqual([]);
    });

    it('ka10087: afterHoursSinglePrice', () => {
      const result = afterHoursSinglePriceResponseSchema.parse(minimalEnvelope);
      expect(result.bid_req_base_tm).toBe('');
      expect(result.ovt_sigpric_cur_prc).toBe('');
    });

    it('ka90005: programTradingTrendByTime', () => {
      const result = programTradingTrendByTimeResponseSchema.parse(minimalEnvelope);
      expect(result.prm_trde_trnsn).toEqual([]);
    });

    it('ka90006: programTradingArbitrageBalanceTrend', () => {
      const result = programTradingArbitrageBalanceTrendResponseSchema.parse(minimalEnvelope);
      expect(result.prm_trde_dfrt_remn_trnsn).toEqual([]);
    });

    it('ka90007: programTradingCumulativeTrend', () => {
      const result = programTradingCumulativeTrendResponseSchema.parse(minimalEnvelope);
      expect(result.prm_trde_acc_trnsn).toEqual([]);
    });

    it('ka90008: programTradingTrendByStockAndTime', () => {
      const result = programTradingTrendByStockAndTimeResponseSchema.parse(minimalEnvelope);
      expect(result.stk_tm_prm_trde_trnsn).toEqual([]);
    });

    it('ka90010: programTradingTrendByDate', () => {
      const result = programTradingTrendByDateResponseSchema.parse(minimalEnvelope);
      expect(result.prm_trde_trnsn).toEqual([]);
    });

    it('ka90013: programTradingTrendByStockAndDate', () => {
      const result = programTradingTrendByStockAndDateResponseSchema.parse(minimalEnvelope);
      expect(result.stk_daly_prm_trde_trnsn).toEqual([]);
    });
  });

  describe('full item responses', () => {
    it('ka10005: parses stock quote by date item', () => {
      const input = {
        return_code: '0',
        stk_ddwkmm: [
          {
            date: '20260312',
            open_pric: '186600',
            high_pric: '190000',
            low_pric: '185900',
            close_pric: '-187900',
            pre: '',
            flu_rt: '',
            trde_qty: '20440753',
            trde_prica: '',
            for_poss: '',
            for_wght: '',
            for_netprps: '',
            orgn_netprps: '',
            ind_netprps: '',
            crd_remn_rt: '',
            frgn: '',
            prm: '',
          },
        ],
      };
      const result = stockQuoteByDateResponseSchema.parse(input);
      expect(result.stk_ddwkmm).toHaveLength(1);
      expect(result.stk_ddwkmm[0]?.date).toBe('20260312');
    });

    it('ka10044: parses daily institutional trading item', () => {
      const input = {
        return_code: '0',
        daly_orgn_trde_stk: [
          {
            stk_cd: '005930',
            stk_nm: '삼성전자',
            netprps_qty: '+108855',
            netprps_amt: '+2230468',
            prsm_avg_pric: '204903',
            cur_prc: '-187900',
            avg_pric_pre: '--17003',
            pre_rt: '-8.29',
          },
        ],
      };
      const result = dailyInstitutionalTradingItemsResponseSchema.parse(input);
      expect(result.daly_orgn_trde_stk).toHaveLength(1);
      expect(result.daly_orgn_trde_stk[0]?.stk_cd).toBe('005930');
    });

    it('ka10086: parses daily stock price item', () => {
      const input = {
        return_code: '0',
        daly_stkpc: [
          {
            date: '20260312',
            open_pric: '-186600',
            high_pric: '190000',
            low_pric: '-185900',
            close_pric: '-187900',
            pred_rt: '-2100',
            flu_rt: '-1.11',
            trde_qty: '20440753',
            amt_mn: '3832551',
            crd_rt: '0.00',
            ind: '+4304042',
            orgn: '+406662',
            for_qty: '--6518898',
            frgn: '--4324306',
            prm: '--4438426',
            for_rt: '+49.66',
            for_poss: '+49.66',
            for_wght: '+49.66',
            for_netprps: '--6518898',
            orgn_netprps: '+406662',
            ind_netprps: '+4304042',
            crd_remn_rt: '0.00',
          },
        ],
      };
      const result = dailyStockPriceResponseSchema.parse(input);
      expect(result.daly_stkpc).toHaveLength(1);
      expect(result.daly_stkpc[0]?.date).toBe('20260312');
      expect(result.daly_stkpc[0]?.for_netprps).toBe('--6518898');
    });

    it('ka90007: parses program trading cumulative trend item', () => {
      const input = {
        return_code: '0',
        prm_trde_acc_trnsn: [
          {
            dt: '20260312',
            kospi200: '+827.51',
            basis: '-3.86',
            dfrt_trde_tdy: '--55108',
            dfrt_trde_acc: '--55108',
            ndiffpro_trde_tdy: '--1514901',
            ndiffpro_trde_acc: '--1514901',
            all_tdy: '--1570009',
            all_acc: '--1570009',
          },
        ],
      };
      const result = programTradingCumulativeTrendResponseSchema.parse(input);
      expect(result.prm_trde_acc_trnsn).toHaveLength(1);
      expect(result.prm_trde_acc_trnsn[0]?.kospi200).toBe('+827.51');
    });
  });

  describe('passthrough behavior', () => {
    it('preserves unknown fields in response', () => {
      const input = {
        return_code: '0',
        daly_stkpc: [],
        unknown_field: 'should be preserved',
      };
      const result = dailyStockPriceResponseSchema.parse(input);
      expect((result as Record<string, unknown>).unknown_field).toBe('should be preserved');
    });

    it('preserves unknown fields in items', () => {
      const input = {
        return_code: '0',
        sec_stk_trde_trend: [
          {
            dt: '20260312',
            cur_prc: '-187900',
            pre_sig: '5',
            pred_pre: '-2100',
            flu_rt: '-1.11',
            acc_trde_qty: '20440753',
            netprps_qty: '-4324306',
            buy_qty: '383932',
            sell_qty: '4708238',
            extra_field: 'hello',
          },
        ],
      };
      const result = securitiesFirmTradingTrendByStockResponseSchema.parse(input);
      expect((result.sec_stk_trde_trend[0] as Record<string, unknown>).extra_field).toBe('hello');
    });
  });

  describe('default values for missing fields', () => {
    it('defaults missing item fields to empty string', () => {
      const input = {
        return_code: '0',
        cntr_str_daly: [{}],
      };
      const result = executionIntensityTrendByDateResponseSchema.parse(input);
      const item = result.cntr_str_daly[0];
      expect(item.dt).toBe('');
      expect(item.cur_prc).toBe('');
      expect(item.cntr_str).toBe('');
      expect(item.cntr_str5min).toBe('');
    });

    it('defaults numeric return_code', () => {
      const input = { return_code: 0, return_msg: 'OK' };
      const result = stockQuoteResponseSchema.parse(input);
      expect(result.return_code).toBe(0);
    });
  });
});
