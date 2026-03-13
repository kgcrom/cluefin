import { describe, expect, it } from 'vitest';

import {
  afterHoursSinglePriceChangeRateRankingResponseSchema,
  rapidlyIncreasingRemainingOrderQuantityResponseSchema,
  rapidlyIncreasingTotalSellOrdersResponseSchema,
  rapidlyIncreasingTradingVolumeResponseSchema,
  sameNetBuySellRankingResponseSchema,
  stockSpecificSecuritiesFirmRankingResponseSchema,
  topConsecutiveNetBuySellByForeignersResponseSchema,
  topCurrentDayDeviationSourcesResponseSchema,
  topCurrentDayMajorTradersResponseSchema,
  topCurrentDayTradingVolumeResponseSchema,
  topExpectedConclusionPercentageChangeResponseSchema,
  topForeignAccountGroupTradingResponseSchema,
  topForeignerInstitutionTradingResponseSchema,
  topForeignerPeriodTradingResponseSchema,
  topLimitExhaustionRateForeignerResponseSchema,
  topMarginRatioResponseSchema,
  topNetBuyTraderRankingResponseSchema,
  topPercentageChangeFromPreviousDayResponseSchema,
  topPreviousDayTradingVolumeResponseSchema,
  topRemainingOrderQuantityResponseSchema,
  topSecuritiesFirmTradingResponseSchema,
  topTransactionValueResponseSchema,
} from '../../../src/kiwoom/schemas/domestic-rank-info';

describe('domestic-rank-info response schemas', () => {
  describe('minimal responses (envelope only)', () => {
    const minimalEnvelope = { return_code: '0', return_msg: 'OK' };

    it('ka10020: topRemainingOrderQuantity', () => {
      const result = topRemainingOrderQuantityResponseSchema.parse(minimalEnvelope);
      expect(result.bid_req_upper).toEqual([]);
    });

    it('ka10021: rapidlyIncreasingRemainingOrderQuantity', () => {
      const result = rapidlyIncreasingRemainingOrderQuantityResponseSchema.parse(minimalEnvelope);
      expect(result.bid_req_sdnin).toEqual([]);
    });

    it('ka10022: rapidlyIncreasingTotalSellOrders', () => {
      const result = rapidlyIncreasingTotalSellOrdersResponseSchema.parse(minimalEnvelope);
      expect(result.req_rt_sdnin).toEqual([]);
    });

    it('ka10023: rapidlyIncreasingTradingVolume', () => {
      const result = rapidlyIncreasingTradingVolumeResponseSchema.parse(minimalEnvelope);
      expect(result.trde_qty_sdnin).toEqual([]);
    });

    it('ka10027: topPercentageChangeFromPreviousDay', () => {
      const result = topPercentageChangeFromPreviousDayResponseSchema.parse(minimalEnvelope);
      expect(result.pred_pre_flu_rt_upper).toEqual([]);
    });

    it('ka10029: topExpectedConclusionPercentageChange', () => {
      const result = topExpectedConclusionPercentageChangeResponseSchema.parse(minimalEnvelope);
      expect(result.exp_cntr_flu_rt_upper).toEqual([]);
    });

    it('ka10030: topCurrentDayTradingVolume', () => {
      const result = topCurrentDayTradingVolumeResponseSchema.parse(minimalEnvelope);
      expect(result.tdy_trde_qty_upper).toEqual([]);
    });

    it('ka10031: topPreviousDayTradingVolume', () => {
      const result = topPreviousDayTradingVolumeResponseSchema.parse(minimalEnvelope);
      expect(result.pred_trde_qty_upper).toEqual([]);
    });

    it('ka10032: topTransactionValue', () => {
      const result = topTransactionValueResponseSchema.parse(minimalEnvelope);
      expect(result.trde_prica_upper).toEqual([]);
    });

    it('ka10033: topMarginRatio', () => {
      const result = topMarginRatioResponseSchema.parse(minimalEnvelope);
      expect(result.crd_rt_upper).toEqual([]);
    });

    it('ka10034: topForeignerPeriodTrading', () => {
      const result = topForeignerPeriodTradingResponseSchema.parse(minimalEnvelope);
      expect(result.for_dt_trde_upper).toEqual([]);
    });

    it('ka10035: topConsecutiveNetBuySellByForeigners', () => {
      const result = topConsecutiveNetBuySellByForeignersResponseSchema.parse(minimalEnvelope);
      expect(result.for_cont_nettrde_upper).toEqual([]);
    });

    it('ka10036: topLimitExhaustionRateForeigner', () => {
      const result = topLimitExhaustionRateForeignerResponseSchema.parse(minimalEnvelope);
      expect(result.for_limit_exh_rt_incrs_upper).toEqual([]);
    });

    it('ka10037: topForeignAccountGroupTrading', () => {
      const result = topForeignAccountGroupTradingResponseSchema.parse(minimalEnvelope);
      expect(result.frgn_wicket_trde_upper).toEqual([]);
    });

    it('ka10038: stockSpecificSecuritiesFirmRanking', () => {
      const result = stockSpecificSecuritiesFirmRankingResponseSchema.parse(minimalEnvelope);
      expect(result.stk_sec_rank).toEqual([]);
      expect(result.rank_1).toBe('');
      expect(result.rank_2).toBe('');
      expect(result.rank_3).toBe('');
      expect(result.prid_trde_qty).toBe('');
    });

    it('ka10039: topSecuritiesFirmTrading', () => {
      const result = topSecuritiesFirmTradingResponseSchema.parse(minimalEnvelope);
      expect(result.sec_trde_upper).toEqual([]);
    });

    it('ka10040: topCurrentDayMajorTraders', () => {
      const result = topCurrentDayMajorTradersResponseSchema.parse(minimalEnvelope);
      expect(result.tdy_main_trde_ori).toEqual([]);
      expect(result.sel_trde_ori_1).toBe('');
      expect(result.frgn_sel_prsm_sum).toBe('');
    });

    it('ka10042: topNetBuyTraderRanking', () => {
      const result = topNetBuyTraderRankingResponseSchema.parse(minimalEnvelope);
      expect(result.netprps_trde_ori_rank).toEqual([]);
    });

    it('ka10053: topCurrentDayDeviationSources', () => {
      const result = topCurrentDayDeviationSourcesResponseSchema.parse(minimalEnvelope);
      expect(result.tdy_upper_scesn_ori).toEqual([]);
    });

    it('ka10062: sameNetBuySellRanking', () => {
      const result = sameNetBuySellRankingResponseSchema.parse(minimalEnvelope);
      expect(result.eql_nettrde_rank).toEqual([]);
    });

    it('ka10098: afterHoursSinglePriceChangeRateRanking', () => {
      const result = afterHoursSinglePriceChangeRateRankingResponseSchema.parse(minimalEnvelope);
      expect(result.ovt_sigpric_flu_rt_rank).toEqual([]);
    });

    it('ka90009: topForeignerInstitutionTrading', () => {
      const result = topForeignerInstitutionTradingResponseSchema.parse(minimalEnvelope);
      expect(result.frgnr_orgn_trde_upper).toEqual([]);
    });
  });

  describe('full item responses', () => {
    it('ka10020: parses complete item with all fields', () => {
      const input = {
        return_code: '0',
        return_msg: 'OK',
        bid_req_upper: [
          {
            stk_cd: '005930',
            stk_nm: '삼성전자',
            cur_prc: '72000',
            pred_pre_sig: '2',
            pred_pre: '500',
            trde_qty: '10000',
            tot_sel_req: '50000',
            tot_buy_req: '60000',
            netprps_req: '10000',
            buy_rt: '54.55',
          },
        ],
      };
      const result = topRemainingOrderQuantityResponseSchema.parse(input);
      expect(result.bid_req_upper).toHaveLength(1);
      expect(result.bid_req_upper[0]!.stk_cd).toBe('005930');
    });

    it('ka10021: parses item with "int" alias field', () => {
      const input = {
        return_code: '0',
        bid_req_sdnin: [
          {
            stk_cd: '005930',
            stk_nm: '삼성전자',
            cur_prc: '72000',
            pred_pre_sig: '2',
            pred_pre: '500',
            int: '10.5',
            now: '15.2',
            sdnin_qty: '5000',
            sdnin_rt: '45.0',
            tot_buy_qty: '60000',
          },
        ],
      };
      const result = rapidlyIncreasingRemainingOrderQuantityResponseSchema.parse(input);
      expect(result.bid_req_sdnin[0]!.int).toBe('10.5');
    });

    it('ka10038: parses scalar fields + list', () => {
      const input = {
        return_code: '0',
        rank_1: '매수상위',
        rank_2: '매도상위',
        rank_3: '순매수상위',
        prid_trde_qty: '1000000',
        stk_sec_rank: [{ rank: '1', mmcm_nm: '키움증권', buy_qty: '500', sell_qty: '300', acc_netprps_qty: '200' }],
      };
      const result = stockSpecificSecuritiesFirmRankingResponseSchema.parse(input);
      expect(result.rank_1).toBe('매수상위');
      expect(result.stk_sec_rank).toHaveLength(1);
    });
  });

  describe('passthrough behavior', () => {
    it('preserves unknown fields in response', () => {
      const input = {
        return_code: '0',
        return_msg: 'OK',
        bid_req_upper: [],
        unknown_field: 'should be preserved',
      };
      const result = topRemainingOrderQuantityResponseSchema.parse(input);
      expect((result as Record<string, unknown>).unknown_field).toBe('should be preserved');
    });

    it('preserves unknown fields in items', () => {
      const input = {
        return_code: '0',
        bid_req_upper: [
          {
            stk_cd: '005930',
            stk_nm: '삼성전자',
            cur_prc: '72000',
            pred_pre_sig: '2',
            pred_pre: '500',
            trde_qty: '10000',
            tot_sel_req: '50000',
            tot_buy_req: '60000',
            netprps_req: '10000',
            buy_rt: '54.55',
            extra_field: 'hello',
          },
        ],
      };
      const result = topRemainingOrderQuantityResponseSchema.parse(input);
      expect((result.bid_req_upper[0]! as Record<string, unknown>).extra_field).toBe('hello');
    });
  });

  describe('default values for missing fields', () => {
    it('defaults missing item fields to empty string', () => {
      const input = {
        return_code: '0',
        pred_trde_qty_upper: [{}],
      };
      const result = topPreviousDayTradingVolumeResponseSchema.parse(input);
      const item = result.pred_trde_qty_upper[0]!;
      expect(item.stk_cd).toBe('');
      expect(item.stk_nm).toBe('');
      expect(item.cur_prc).toBe('');
      expect(item.pred_pre_sig).toBe('');
      expect(item.pred_pre).toBe('');
      expect(item.trde_qty).toBe('');
    });

    it('defaults numeric return_code', () => {
      const input = { return_code: 0, return_msg: 'OK' };
      const result = topRemainingOrderQuantityResponseSchema.parse(input);
      expect(result.return_code).toBe(0);
    });
  });
});
