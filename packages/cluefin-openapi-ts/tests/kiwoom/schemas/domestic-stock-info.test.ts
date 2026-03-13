import { describe, expect, it } from 'vitest';

import {
  changeRateFromOpenResponseSchema,
  dailyPreviousDayConclusionResponseSchema,
  dailyPreviousDayExecutionVolumeResponseSchema,
  dailyTradingDetailsResponseSchema,
  dailyTradingItemsByInvestorResponseSchema,
  executionResponseSchema,
  highLowPriceApproachResponseSchema,
  highPerResponseSchema,
  industryCodeResponseSchema,
  institutionalInvestorByStockResponseSchema,
  interestStockInfoResponseSchema,
  marginTradingTrendResponseSchema,
  memberCompanyResponseSchema,
  newHighLowPriceResponseSchema,
  priceVolatilityResponseSchema,
  programTradingStatusByStockResponseSchema,
  stockInfoResponseSchema,
  stockInfoSummaryResponseSchema,
  stockInfoV1ResponseSchema,
  stockTradingMemberResponseSchema,
  supplyDemandConcentrationResponseSchema,
  top50ProgramNetBuyResponseSchema,
  totalInstitutionalInvestorByStockResponseSchema,
  tradingMemberInstantVolumeResponseSchema,
  tradingMemberSupplyDemandAnalysisResponseSchema,
  tradingVolumeRenewalResponseSchema,
  upperLowerLimitPriceResponseSchema,
  volatilityControlEventResponseSchema,
} from '../../../src/kiwoom/schemas/domestic-stock-info';

describe('domestic-stock-info response schemas', () => {
  describe('minimal responses (envelope only)', () => {
    const minimalEnvelope = { return_code: '0', return_msg: 'OK' };

    it('ka10001: stockInfo', () => {
      const result = stockInfoResponseSchema.parse(minimalEnvelope);
      expect(result.stk_cd).toBe('');
      expect(result.stk_nm).toBe('');
    });

    it('ka10002: stockTradingMember', () => {
      const result = stockTradingMemberResponseSchema.parse(minimalEnvelope);
      expect(result.stk_cd).toBe('');
      expect(result.cur_prc).toBe('');
    });

    it('ka10003: execution', () => {
      const result = executionResponseSchema.parse(minimalEnvelope);
      expect(result.cntr_infr).toEqual([]);
    });

    it('ka10013: marginTradingTrend', () => {
      const result = marginTradingTrendResponseSchema.parse(minimalEnvelope);
      expect(result.crd_trde_trend).toEqual([]);
    });

    it('ka10015: dailyTradingDetails', () => {
      const result = dailyTradingDetailsResponseSchema.parse(minimalEnvelope);
      expect(result.daly_trde_dtl).toEqual([]);
    });

    it('ka10016: newHighLowPrice', () => {
      const result = newHighLowPriceResponseSchema.parse(minimalEnvelope);
      expect(result.ntl_pric).toEqual([]);
    });

    it('ka10017: upperLowerLimitPrice', () => {
      const result = upperLowerLimitPriceResponseSchema.parse(minimalEnvelope);
      expect(result.updown_pric).toEqual([]);
    });

    it('ka10018: highLowPriceApproach', () => {
      const result = highLowPriceApproachResponseSchema.parse(minimalEnvelope);
      expect(result.high_low_pric_alacc).toEqual([]);
    });

    it('ka10019: priceVolatility', () => {
      const result = priceVolatilityResponseSchema.parse(minimalEnvelope);
      expect(result.pric_jmpflu).toEqual([]);
    });

    it('ka10024: tradingVolumeRenewal', () => {
      const result = tradingVolumeRenewalResponseSchema.parse(minimalEnvelope);
      expect(result.trde_qty_updt).toEqual([]);
    });

    it('ka10025: supplyDemandConcentration', () => {
      const result = supplyDemandConcentrationResponseSchema.parse(minimalEnvelope);
      expect(result.prps_cnctr).toEqual([]);
    });

    it('ka10026: highPer', () => {
      const result = highPerResponseSchema.parse(minimalEnvelope);
      expect(result.high_low_per).toEqual([]);
    });

    it('ka10028: changeRateFromOpen', () => {
      const result = changeRateFromOpenResponseSchema.parse(minimalEnvelope);
      expect(result.open_pric_pre_flu_rt).toEqual([]);
    });

    it('ka10043: tradingMemberSupplyDemandAnalysis', () => {
      const result = tradingMemberSupplyDemandAnalysisResponseSchema.parse(minimalEnvelope);
      expect(result.trde_ori_prps_anly).toEqual([]);
    });

    it('ka10052: tradingMemberInstantVolume', () => {
      const result = tradingMemberInstantVolumeResponseSchema.parse(minimalEnvelope);
      expect(result.trde_ori_mont_trde_qty).toEqual([]);
    });

    it('ka10054: volatilityControlEvent', () => {
      const result = volatilityControlEventResponseSchema.parse(minimalEnvelope);
      expect(result.motn_stk).toEqual([]);
    });

    it('ka10055: dailyPreviousDayExecutionVolume', () => {
      const result = dailyPreviousDayExecutionVolumeResponseSchema.parse(minimalEnvelope);
      expect(result.tdy_pred_cntr_qty).toEqual([]);
    });

    it('ka10058: dailyTradingItemsByInvestor', () => {
      const result = dailyTradingItemsByInvestorResponseSchema.parse(minimalEnvelope);
      expect(result.invsr_daly_trde_stk).toEqual([]);
    });

    it('ka10059: institutionalInvestorByStock', () => {
      const result = institutionalInvestorByStockResponseSchema.parse(minimalEnvelope);
      expect(result.stk_invsr_orgn).toEqual([]);
    });

    it('ka10061: totalInstitutionalInvestorByStock', () => {
      const result = totalInstitutionalInvestorByStockResponseSchema.parse(minimalEnvelope);
      expect(result.stk_invsr_orgn_tot).toEqual([]);
    });

    it('ka10084: dailyPreviousDayConclusion', () => {
      const result = dailyPreviousDayConclusionResponseSchema.parse(minimalEnvelope);
      expect(result.tdy_pred_cntr).toEqual([]);
    });

    it('ka10095: interestStockInfo', () => {
      const result = interestStockInfoResponseSchema.parse(minimalEnvelope);
      expect(result.atn_stk_infr).toEqual([]);
    });

    it('ka10099: stockInfoSummary', () => {
      const result = stockInfoSummaryResponseSchema.parse(minimalEnvelope);
      expect(result.list).toEqual([]);
    });

    it('ka10100: stockInfoV1', () => {
      const result = stockInfoV1ResponseSchema.parse(minimalEnvelope);
      expect(result.code).toBe('');
      expect(result.name).toBe('');
    });

    it('ka10101: industryCode', () => {
      const result = industryCodeResponseSchema.parse(minimalEnvelope);
      expect(result.list).toEqual([]);
    });

    it('ka10102: memberCompany', () => {
      const result = memberCompanyResponseSchema.parse(minimalEnvelope);
      expect(result.list).toEqual([]);
    });

    it('ka90003: top50ProgramNetBuy', () => {
      const result = top50ProgramNetBuyResponseSchema.parse(minimalEnvelope);
      expect(result.prm_netprps_upper50).toEqual([]);
    });

    it('ka90004: programTradingStatusByStock', () => {
      const result = programTradingStatusByStockResponseSchema.parse(minimalEnvelope);
      expect(result.stk_prm_trde_prst).toEqual([]);
      expect(result.tot1).toBe('');
    });
  });

  describe('full item responses', () => {
    it('ka10003: parses execution item', () => {
      const input = {
        return_code: '0',
        cntr_infr: [
          {
            tm: '153000',
            cur_prc: '-187900',
            pred_pre: '-2100',
            pre_rt: '-1.11',
            pri_sel_bid_unit: '58230',
            pri_buy_bid_unit: '20560',
            cntr_trde_qty: '172',
            sign: '5',
            acc_trde_qty: '20440753',
            acc_trde_prica: '3832551',
            cntr_str: '74',
            stex_tp: '1',
          },
        ],
      };
      const result = executionResponseSchema.parse(input);
      expect(result.cntr_infr).toHaveLength(1);
      expect(result.cntr_infr[0]!.tm).toBe('153000');
      expect(result.cntr_infr[0]!.cur_prc).toBe('-187900');
    });

    it('ka10059: parses institutional investor by stock item', () => {
      const input = {
        return_code: '0',
        stk_invsr_orgn: [
          {
            dt: '20260312',
            cur_prc: '-187900',
            pre_sig: '5',
            pred_pre: '-2100',
            flu_rt: '-1.11',
            acc_trde_qty: '20440753',
            acc_trde_prica: '3832551',
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
      const result = institutionalInvestorByStockResponseSchema.parse(input);
      expect(result.stk_invsr_orgn).toHaveLength(1);
      expect(result.stk_invsr_orgn[0]!.dt).toBe('20260312');
      expect(result.stk_invsr_orgn[0]!.ind_invsr).toBe('805003');
    });

    it('ka90004: parses program trading status by stock item', () => {
      const input = {
        return_code: '0',
        tot1: '100',
        tot2: '200',
        tot3: '300',
        tot4: '400',
        tot5: '500',
        tot6: '600',
        stk_prm_trde_prst: [
          {
            stk_cd: '005930',
            stk_nm: '삼성전자',
            cur_prc: '-187900',
            flu_sig: '5',
            pred_pre: '-2100',
            buy_cntr_qty: '1000',
            buy_cntr_amt: '188000000',
            sel_cntr_qty: '500',
            sel_cntr_amt: '94000000',
            netprps_prica: '94000000',
            all_trde_rt: '0.05',
          },
        ],
      };
      const result = programTradingStatusByStockResponseSchema.parse(input);
      expect(result.tot1).toBe('100');
      expect(result.stk_prm_trde_prst).toHaveLength(1);
      expect(result.stk_prm_trde_prst[0]!.stk_cd).toBe('005930');
    });
  });

  describe('passthrough behavior', () => {
    it('preserves unknown fields in response', () => {
      const input = {
        return_code: '0',
        cntr_infr: [],
        unknown_field: 'should be preserved',
      };
      const result = executionResponseSchema.parse(input);
      expect((result as Record<string, unknown>).unknown_field).toBe('should be preserved');
    });

    it('preserves unknown fields in items', () => {
      const input = {
        return_code: '0',
        cntr_infr: [
          {
            tm: '153000',
            cur_prc: '-187900',
            pred_pre: '-2100',
            pre_rt: '-1.11',
            pri_sel_bid_unit: '58230',
            pri_buy_bid_unit: '20560',
            cntr_trde_qty: '172',
            sign: '5',
            acc_trde_qty: '20440753',
            acc_trde_prica: '3832551',
            cntr_str: '74',
            stex_tp: '1',
            extra_field: 'hello',
          },
        ],
      };
      const result = executionResponseSchema.parse(input);
      expect((result.cntr_infr[0]! as Record<string, unknown>).extra_field).toBe('hello');
    });
  });

  describe('default values for missing fields', () => {
    it('defaults missing item fields to empty string', () => {
      const input = {
        return_code: '0',
        crd_trde_trend: [{}],
      };
      const result = marginTradingTrendResponseSchema.parse(input);
      const item = result.crd_trde_trend[0]!;
      expect(item.dt).toBe('');
      expect(item.cur_prc).toBe('');
      expect(item.pred_pre).toBe('');
      expect(item.remn).toBe('');
    });

    it('defaults numeric return_code', () => {
      const input = { return_code: 0, return_msg: 'OK' };
      const result = executionResponseSchema.parse(input);
      expect(result.return_code).toBe(0);
    });
  });
});
