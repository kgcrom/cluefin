import { describe, expect, it } from 'vitest';

import {
  consecutiveNetBuySellStatusByInstitutionForeignerResponseSchema,
  foreignInvestorTradingTrendByStockResponseSchema,
  stockInstitutionResponseSchema,
} from '../../../src/kiwoom/schemas/domestic-foreign';

describe('domestic-foreign response schemas', () => {
  describe('minimal responses (envelope only)', () => {
    const minimalEnvelope = { return_code: '0', return_msg: 'OK' };

    it('ka10008: foreignInvestorTradingTrendByStock', () => {
      const result = foreignInvestorTradingTrendByStockResponseSchema.parse(minimalEnvelope);
      expect(result.stk_frgnr).toEqual([]);
    });

    it('ka10009: stockInstitution', () => {
      const result = stockInstitutionResponseSchema.parse(minimalEnvelope);
      expect(result.date).toBe('');
      expect(result.close_pric).toBe('');
      expect(result.pre).toBe('');
      expect(result.orgn_dt_acc).toBe('');
      expect(result.orgn_daly_nettrde).toBe('');
      expect(result.frgnr_daly_nettrde).toBe('');
      expect(result.frgnr_qota_rt).toBe('');
    });

    it('ka10131: consecutiveNetBuySellStatusByInstitutionForeigner', () => {
      const result = consecutiveNetBuySellStatusByInstitutionForeignerResponseSchema.parse(minimalEnvelope);
      expect(result.orgn_frgnr_cont_trde_prst).toEqual([]);
    });
  });

  describe('full item responses', () => {
    it('ka10008: parses foreign investor trading trend item', () => {
      const input = {
        return_code: '0',
        stk_frgnr: [
          {
            dt: '20260312',
            close_pric: '187900',
            pred_pre: '-2100',
            trde_qty: '20440753',
            chg_qty: '-916156',
            poss_stkcnt: '3245678901',
            wght: '55.12',
            gain_pos_stkcnt: '2587654321',
            frgnr_limit: '5961845581',
            frgnr_limit_irds: '0',
            limit_exh_rt: '54.44',
          },
        ],
      };
      const result = foreignInvestorTradingTrendByStockResponseSchema.parse(input);
      expect(result.stk_frgnr).toHaveLength(1);
      expect(result.stk_frgnr[0].dt).toBe('20260312');
      expect(result.stk_frgnr[0].close_pric).toBe('187900');
      expect(result.stk_frgnr[0].limit_exh_rt).toBe('54.44');
    });

    it('ka10131: parses consecutive net buy/sell status item', () => {
      const input = {
        return_code: '0',
        orgn_frgnr_cont_trde_prst: [
          {
            rank: '1',
            stk_cd: '005930',
            stk_nm: '삼성전자',
            prid_stkpc_flu_rt: '-1.10',
            orgn_nettrde_amt: '105432',
            orgn_nettrde_qty: '560',
            orgn_cont_netprps_dys: '3',
            orgn_cont_netprps_qty: '1680',
            orgn_cont_netprps_amt: '316296',
            frgnr_nettrde_qty: '-420',
            frgnr_nettrde_amt: '-78960',
            frgnr_cont_netprps_dys: '0',
            frgnr_cont_netprps_qty: '0',
            frgnr_cont_netprps_amt: '0',
            nettrde_qty: '140',
            nettrde_amt: '26472',
            tot_cont_netprps_dys: '2',
            tot_cont_nettrde_qty: '280',
            tot_cont_netprps_amt: '52704',
          },
        ],
      };
      const result = consecutiveNetBuySellStatusByInstitutionForeignerResponseSchema.parse(input);
      expect(result.orgn_frgnr_cont_trde_prst).toHaveLength(1);
      expect(result.orgn_frgnr_cont_trde_prst[0].stk_cd).toBe('005930');
      expect(result.orgn_frgnr_cont_trde_prst[0].stk_nm).toBe('삼성전자');
    });
  });

  describe('passthrough behavior', () => {
    it('preserves unknown fields in response', () => {
      const input = {
        return_code: '0',
        stk_frgnr: [],
        unknown_field: 'should be preserved',
      };
      const result = foreignInvestorTradingTrendByStockResponseSchema.parse(input);
      expect((result as Record<string, unknown>).unknown_field).toBe('should be preserved');
    });

    it('preserves unknown fields in items', () => {
      const input = {
        return_code: '0',
        orgn_frgnr_cont_trde_prst: [
          {
            rank: '1',
            stk_cd: '005930',
            stk_nm: '삼성전자',
            extra_field: 'hello',
          },
        ],
      };
      const result = consecutiveNetBuySellStatusByInstitutionForeignerResponseSchema.parse(input);
      expect((result.orgn_frgnr_cont_trde_prst[0] as Record<string, unknown>).extra_field).toBe('hello');
    });
  });

  describe('default values for missing fields', () => {
    it('defaults missing item fields to empty string', () => {
      const input = {
        return_code: '0',
        stk_frgnr: [{}],
      };
      const result = foreignInvestorTradingTrendByStockResponseSchema.parse(input);
      const item = result.stk_frgnr[0];
      expect(item.dt).toBe('');
      expect(item.close_pric).toBe('');
      expect(item.trde_qty).toBe('');
      expect(item.limit_exh_rt).toBe('');
    });

    it('defaults numeric return_code', () => {
      const input = { return_code: 0, return_msg: 'OK' };
      const result = stockInstitutionResponseSchema.parse(input);
      expect(result.return_code).toBe(0);
    });
  });
});
