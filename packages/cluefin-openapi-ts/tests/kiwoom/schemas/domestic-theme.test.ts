import { describe, expect, it } from 'vitest';

import { themeGroupResponseSchema, themeGroupStocksResponseSchema } from '../../../src/kiwoom/schemas/domestic-theme';

describe('domestic-theme response schemas', () => {
  describe('minimal responses (envelope only)', () => {
    const minimalEnvelope = { return_code: '0', return_msg: 'OK' };

    it('ka90001: themeGroup', () => {
      const result = themeGroupResponseSchema.parse(minimalEnvelope);
      expect(result.thema_grp).toEqual([]);
    });

    it('ka90002: themeGroupStocks', () => {
      const result = themeGroupStocksResponseSchema.parse(minimalEnvelope);
      expect(result.thema_comp_stk).toEqual([]);
      expect(result.flu_rt).toBe('');
      expect(result.dt_prft_rt).toBe('');
    });
  });

  describe('full item responses', () => {
    it('ka90001: parses theme group item', () => {
      const input = {
        return_code: '0',
        thema_grp: [
          {
            thema_grp_cd: '103',
            thema_nm: '태양광_발전/설치/운영',
            stk_num: '3',
            flu_sig: '2',
            flu_rt: '+9.72',
            rising_stk_num: '3',
            fall_stk_num: '0',
            dt_prft_rt: '+9.72',
            main_stk: '에스에너지, SDN',
          },
        ],
      };
      const result = themeGroupResponseSchema.parse(input);
      expect(result.thema_grp).toHaveLength(1);
      expect(result.thema_grp[0]?.thema_grp_cd).toBe('103');
      expect(result.thema_grp[0]?.thema_nm).toBe('태양광_발전/설치/운영');
    });

    it('ka90002: parses theme group stocks item', () => {
      const input = {
        return_code: '0',
        flu_rt: '+1.23',
        dt_prft_rt: '+1.23',
        thema_comp_stk: [
          {
            stk_cd: '005930',
            stk_nm: '삼성전자',
            cur_prc: '187900',
            flu_sig: '2',
            pred_pre: '-2100',
            flu_rt: '+1.23',
            acc_trde_qty: '20440753',
            sel_bid: '187800',
            sel_req: '1000',
            buy_bid: '187900',
            buy_req: '2000',
            dt_prft_rt_n: '+1.23',
          },
        ],
      };
      const result = themeGroupStocksResponseSchema.parse(input);
      expect(result.thema_comp_stk).toHaveLength(1);
      expect(result.thema_comp_stk[0]?.stk_cd).toBe('005930');
      expect(result.flu_rt).toBe('+1.23');
    });
  });

  describe('passthrough behavior', () => {
    it('preserves unknown fields in response', () => {
      const input = {
        return_code: '0',
        thema_grp: [],
        unknown_field: 'should be preserved',
      };
      const result = themeGroupResponseSchema.parse(input);
      expect((result as Record<string, unknown>).unknown_field).toBe('should be preserved');
    });

    it('preserves unknown fields in items', () => {
      const input = {
        return_code: '0',
        thema_grp: [
          {
            thema_grp_cd: '103',
            thema_nm: '태양광',
            stk_num: '3',
            flu_sig: '2',
            flu_rt: '+9.72',
            rising_stk_num: '3',
            fall_stk_num: '0',
            dt_prft_rt: '+9.72',
            main_stk: '에스에너지',
            extra_field: 'hello',
          },
        ],
      };
      const result = themeGroupResponseSchema.parse(input);
      expect((result.thema_grp[0] as Record<string, unknown>).extra_field).toBe('hello');
    });
  });

  describe('default values for missing fields', () => {
    it('defaults missing item fields to empty string', () => {
      const input = {
        return_code: '0',
        thema_comp_stk: [{}],
      };
      const result = themeGroupStocksResponseSchema.parse(input);
      const item = result.thema_comp_stk[0];
      expect(item.stk_cd).toBe('');
      expect(item.stk_nm).toBe('');
      expect(item.cur_prc).toBe('');
      expect(item.flu_sig).toBe('');
      expect(item.pred_pre).toBe('');
      expect(item.flu_rt).toBe('');
      expect(item.acc_trde_qty).toBe('');
      expect(item.sel_bid).toBe('');
      expect(item.sel_req).toBe('');
      expect(item.buy_bid).toBe('');
      expect(item.buy_req).toBe('');
      expect(item.dt_prft_rt_n).toBe('');
    });

    it('defaults numeric return_code', () => {
      const input = { return_code: 0, return_msg: 'OK' };
      const result = themeGroupResponseSchema.parse(input);
      expect(result.return_code).toBe(0);
    });
  });
});
