import { describe, expect, it } from 'vitest';

import {
  allIndustryIndexResponseSchema,
  dailyIndustryCurrentPriceResponseSchema,
  industryCurrentPriceResponseSchema,
  industryInvestorNetBuyResponseSchema,
  industryPriceBySectorResponseSchema,
  industryProgramResponseSchema,
} from '../../../src/kiwoom/schemas/domestic-sector';

describe('domestic-sector response schemas', () => {
  describe('minimal responses (envelope only)', () => {
    const minimalEnvelope = { return_code: '0', return_msg: 'OK' };

    it('ka10010: industryProgram — flat fields default to empty string', () => {
      const result = industryProgramResponseSchema.parse(minimalEnvelope);
      expect(result.dfrt_trst_sell_qty).toBe('');
      expect(result.all_dfrt_trst_netprps_amt).toBe('');
    });

    it('ka10051: industryInvestorNetBuy — array defaults to []', () => {
      const result = industryInvestorNetBuyResponseSchema.parse(minimalEnvelope);
      expect(result.inds_netprps).toEqual([]);
    });

    it('ka20001: industryCurrentPrice — array defaults to []', () => {
      const result = industryCurrentPriceResponseSchema.parse(minimalEnvelope);
      expect(result.inds_cur_prc_tm).toEqual([]);
      expect(result.cur_prc).toBe('');
    });

    it('ka20002: industryPriceBySector — array defaults to []', () => {
      const result = industryPriceBySectorResponseSchema.parse(minimalEnvelope);
      expect(result.inds_stkpc).toEqual([]);
    });

    it('ka20003: allIndustryIndex — array defaults to []', () => {
      const result = allIndustryIndexResponseSchema.parse(minimalEnvelope);
      expect(result.all_inds_idex).toEqual([]);
    });

    it('ka20009: dailyIndustryCurrentPrice — array defaults to []', () => {
      const result = dailyIndustryCurrentPriceResponseSchema.parse(minimalEnvelope);
      expect(result.inds_cur_prc_daly_rept).toEqual([]);
      expect(result.cur_prc).toBe('');
    });
  });

  describe('full item responses', () => {
    it('ka10010: parses industryProgram flat fields', () => {
      const input = {
        return_code: '0',
        dfrt_trst_sell_qty: '100',
        dfrt_trst_sell_amt: '200',
        dfrt_trst_buy_qty: '300',
        dfrt_trst_buy_amt: '400',
        dfrt_trst_netprps_qty: '500',
        dfrt_trst_netprps_amt: '600',
        ndiffpro_trst_sell_qty: '10',
        ndiffpro_trst_sell_amt: '20',
        ndiffpro_trst_buy_qty: '30',
        ndiffpro_trst_buy_amt: '40',
        ndiffpro_trst_netprps_qty: '50',
        ndiffpro_trst_netprps_amt: '60',
        all_dfrt_trst_sell_qty: '1000',
        all_dfrt_trst_sell_amt: '2000',
        all_dfrt_trst_buy_qty: '3000',
        all_dfrt_trst_buy_amt: '4000',
        all_dfrt_trst_netprps_qty: '5000',
        all_dfrt_trst_netprps_amt: '6000',
      };
      const result = industryProgramResponseSchema.parse(input);
      expect(result.dfrt_trst_sell_qty).toBe('100');
      expect(result.all_dfrt_trst_netprps_amt).toBe('6000');
    });

    it('ka10051: parses industryInvestorNetBuy items', () => {
      const input = {
        return_code: '0',
        inds_netprps: [
          {
            inds_cd: '001',
            inds_nm: '종합(KOSPI)',
            cur_prc: '-558325',
            pre_smbol: '5',
            pred_pre: '-2670',
            flu_rt: '-48',
            trde_qty: '801306',
            sc_netprps: '+6807',
            insrnc_netprps: '+87',
            invtrt_netprps: '+1034',
            bank_netprps: '+80',
            jnsinkm_netprps: '+272',
            endw_netprps: '+1057',
            etc_corp_netprps: '+90',
            ind_netprps: '+25760',
            frgnr_netprps: '-36952',
            native_trmt_frgnr_netprps: '+1346',
            natn_netprps: '+0',
            samo_fund_netprps: '+420',
            orgn_netprps: '+9757',
          },
        ],
      };
      const result = industryInvestorNetBuyResponseSchema.parse(input);
      expect(result.inds_netprps).toHaveLength(1);
      expect(result.inds_netprps[0]?.inds_cd).toBe('001');
      expect(result.inds_netprps[0]?.orgn_netprps).toBe('+9757');
    });

    it('ka20001: parses industryCurrentPrice with time items', () => {
      const input = {
        return_code: '0',
        cur_prc: '-5583.25',
        pred_pre_sig: '5',
        pred_pre: '-26.70',
        flu_rt: '-0.48',
        trde_qty: '801306',
        trde_prica: '23698184',
        trde_frmatn_stk_num: '926',
        trde_frmatn_rt: '+97.38',
        open_pric: '-5567.65',
        high_pric: '+5629.07',
        low_pric: '-5527.47',
        upl: '1',
        rising: '572',
        stdns: '32',
        fall: '322',
        lst: '0',
        '52wk_hgst_pric': '+6347.41',
        '52wk_hgst_pric_dt': '20260227',
        '52wk_hgst_pric_pre_rt': '-12.04',
        '52wk_lwst_pric': '-2284.72',
        '52wk_lwst_pric_dt': '20250409',
        '52wk_lwst_pric_pre_rt': '+144.37',
        inds_cur_prc_tm: [
          {
            tm_n: '153250',
            cur_prc_n: '-5583.16',
            pred_pre_sig_n: '5',
            pred_pre_n: '-26.79',
            flu_rt_n: '-0.48',
            trde_qty_n: '520',
            acc_trde_qty_n: '794130',
          },
        ],
      };
      const result = industryCurrentPriceResponseSchema.parse(input);
      expect(result.cur_prc).toBe('-5583.25');
      expect(result.inds_cur_prc_tm).toHaveLength(1);
      expect(result.inds_cur_prc_tm[0]?.tm_n).toBe('153250');
    });

    it('ka20002: parses industryPriceBySector items', () => {
      const input = {
        return_code: '0',
        inds_stkpc: [
          {
            stk_cd: '000020',
            stk_nm: '동화약품',
            cur_prc: '+6100',
            pred_pre_sig: '2',
            pred_pre: '+40',
            flu_rt: '+0.66',
            now_trde_qty: '49084',
            sel_bid: '+6100',
            buy_bid: '+6090',
            open_pric: '+6070',
            high_pric: '+6120',
            low_pric: '-6050',
          },
        ],
      };
      const result = industryPriceBySectorResponseSchema.parse(input);
      expect(result.inds_stkpc).toHaveLength(1);
      expect(result.inds_stkpc[0]?.stk_cd).toBe('000020');
    });

    it('ka20003: parses allIndustryIndex items', () => {
      const input = {
        return_code: '0',
        all_inds_idex: [
          {
            stk_cd: '001',
            stk_nm: '종합(KOSPI)',
            cur_prc: '-5583.25',
            pre_sig: '5',
            pred_pre: '-26.70',
            flu_rt: '-0.48',
            trde_qty: '801306',
            wght: '',
            trde_prica: '23698184',
            upl: '1',
            rising: '572',
            stdns: '32',
            fall: '322',
            lst: '0',
            flo_stk_num: '951',
          },
        ],
      };
      const result = allIndustryIndexResponseSchema.parse(input);
      expect(result.all_inds_idex).toHaveLength(1);
      expect(result.all_inds_idex[0]?.stk_cd).toBe('001');
      expect(result.all_inds_idex[0]?.flo_stk_num).toBe('951');
    });

    it('ka20009: parses dailyIndustryCurrentPrice with daily items', () => {
      const input = {
        return_code: '0',
        cur_prc: '-5583.25',
        pred_pre_sig: '5',
        pred_pre: '-26.70',
        flu_rt: '-0.48',
        trde_qty: '801306',
        trde_prica: '23698184',
        trde_frmatn_stk_num: '926',
        trde_frmatn_rt: '+97.38',
        open_pric: '-5567.65',
        high_pric: '+5629.07',
        low_pric: '-5527.47',
        upl: '1',
        rising: '572',
        stdns: '32',
        fall: '322',
        lst: '0',
        '52wk_hgst_pric': '+6347.41',
        '52wk_hgst_pric_dt': '20260227',
        '52wk_hgst_pric_pre_rt': '-12.04',
        '52wk_lwst_pric': '-2284.72',
        '52wk_lwst_pric_dt': '20250409',
        '52wk_lwst_pric_pre_rt': '+144.37',
        inds_cur_prc_daly_rept: [
          {
            dt_n: '20260312',
            cur_prc_n: '-5583.25',
            pred_pre_sig_n: '5',
            pred_pre_n: '-26.70',
            flu_rt_n: '-0.48',
            acc_trde_qty_n: '801306',
          },
        ],
      };
      const result = dailyIndustryCurrentPriceResponseSchema.parse(input);
      expect(result.cur_prc).toBe('-5583.25');
      expect(result.inds_cur_prc_daly_rept).toHaveLength(1);
      expect(result.inds_cur_prc_daly_rept[0]?.dt_n).toBe('20260312');
    });
  });

  describe('passthrough behavior', () => {
    it('preserves unknown fields in response', () => {
      const input = {
        return_code: '0',
        inds_stkpc: [],
        unknown_field: 'should be preserved',
      };
      const result = industryPriceBySectorResponseSchema.parse(input);
      expect((result as Record<string, unknown>).unknown_field).toBe('should be preserved');
    });

    it('preserves unknown fields in items', () => {
      const input = {
        return_code: '0',
        all_inds_idex: [
          {
            stk_cd: '001',
            stk_nm: 'test',
            cur_prc: '100',
            pre_sig: '2',
            pred_pre: '1',
            flu_rt: '0.1',
            trde_qty: '100',
            wght: '',
            trde_prica: '100',
            upl: '0',
            rising: '0',
            stdns: '0',
            fall: '0',
            lst: '0',
            flo_stk_num: '0',
            extra_field: 'hello',
          },
        ],
      };
      const result = allIndustryIndexResponseSchema.parse(input);
      expect((result.all_inds_idex[0] as Record<string, unknown>).extra_field).toBe('hello');
    });
  });

  describe('default values for missing fields', () => {
    it('defaults missing item fields to empty string', () => {
      const input = {
        return_code: '0',
        all_inds_idex: [{}],
      };
      const result = allIndustryIndexResponseSchema.parse(input);
      const item = result.all_inds_idex[0];
      expect(item.stk_cd).toBe('');
      expect(item.stk_nm).toBe('');
      expect(item.cur_prc).toBe('');
      expect(item.flo_stk_num).toBe('');
    });

    it('defaults numeric return_code', () => {
      const input = { return_code: 0, return_msg: 'OK' };
      const result = industryProgramResponseSchema.parse(input);
      expect(result.return_code).toBe(0);
    });
  });
});
