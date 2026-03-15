import { describe, expect, it } from 'vitest';

import { themeGroupResponseSchema, themeGroupStocksResponseSchema } from '../../../src/kiwoom/schemas/domestic-theme';

describe('domestic-theme response schemas', () => {
  describe('minimal responses (envelope only)', () => {
    const minimalEnvelope = { return_code: '0', return_msg: 'OK' };

    it('ka90001: themeGroup', () => {
      const result = themeGroupResponseSchema.parse(minimalEnvelope);
      expect(result.themaGrp).toEqual([]);
    });

    it('ka90002: themeGroupStocks', () => {
      const result = themeGroupStocksResponseSchema.parse(minimalEnvelope);
      expect(result.themaCompStk).toEqual([]);
      expect(result.fluRt).toBe('');
      expect(result.dtPrftRt).toBe('');
    });
  });

  describe('full item responses', () => {
    it('ka90001: parses theme group item', () => {
      const input = {
        return_code: '0',
        themaGrp: [
          {
            themaGrpCd: '103',
            themaNm: '태양광_발전/설치/운영',
            stkNum: '3',
            fluSig: '2',
            fluRt: '+9.72',
            risingStkNum: '3',
            fallStkNum: '0',
            dtPrftRt: '+9.72',
            mainStk: '에스에너지, SDN',
          },
        ],
      };
      const result = themeGroupResponseSchema.parse(input);
      expect(result.themaGrp).toHaveLength(1);
      expect(result.themaGrp[0]?.themaGrpCd).toBe('103');
      expect(result.themaGrp[0]?.themaNm).toBe('태양광_발전/설치/운영');
    });

    it('ka90002: parses theme group stocks item', () => {
      const input = {
        return_code: '0',
        fluRt: '+1.23',
        dtPrftRt: '+1.23',
        themaCompStk: [
          {
            stkCd: '005930',
            stkNm: '삼성전자',
            curPrc: '187900',
            fluSig: '2',
            predPre: '-2100',
            fluRt: '+1.23',
            accTrdeQty: '20440753',
            selBid: '187800',
            selReq: '1000',
            buyBid: '187900',
            buyReq: '2000',
            dtPrftRtN: '+1.23',
          },
        ],
      };
      const result = themeGroupStocksResponseSchema.parse(input);
      expect(result.themaCompStk).toHaveLength(1);
      expect(result.themaCompStk[0]?.stkCd).toBe('005930');
      expect(result.fluRt).toBe('+1.23');
    });
  });

  describe('passthrough behavior', () => {
    it('preserves unknown fields in response', () => {
      const input = {
        return_code: '0',
        themaGrp: [],
        unknown_field: 'should be preserved',
      };
      const result = themeGroupResponseSchema.parse(input);
      expect((result as Record<string, unknown>).unknown_field).toBe('should be preserved');
    });

    it('preserves unknown fields in items', () => {
      const input = {
        return_code: '0',
        themaGrp: [
          {
            themaGrpCd: '103',
            themaNm: '태양광',
            stkNum: '3',
            fluSig: '2',
            fluRt: '+9.72',
            risingStkNum: '3',
            fallStkNum: '0',
            dtPrftRt: '+9.72',
            mainStk: '에스에너지',
            extra_field: 'hello',
          },
        ],
      };
      const result = themeGroupResponseSchema.parse(input);
      expect((result.themaGrp[0] as Record<string, unknown>).extra_field).toBe('hello');
    });
  });

  describe('default values for missing fields', () => {
    it('defaults missing item fields to empty string', () => {
      const input = {
        return_code: '0',
        themaCompStk: [{}],
      };
      const result = themeGroupStocksResponseSchema.parse(input);
      const item = result.themaCompStk[0];
      expect(item.stkCd).toBe('');
      expect(item.stkNm).toBe('');
      expect(item.curPrc).toBe('');
      expect(item.fluSig).toBe('');
      expect(item.predPre).toBe('');
      expect(item.fluRt).toBe('');
      expect(item.accTrdeQty).toBe('');
      expect(item.selBid).toBe('');
      expect(item.selReq).toBe('');
      expect(item.buyBid).toBe('');
      expect(item.buyReq).toBe('');
      expect(item.dtPrftRtN).toBe('');
    });

    it('defaults numeric return_code', () => {
      const input = { return_code: 0, return_msg: 'OK' };
      const result = themeGroupResponseSchema.parse(input);
      expect(result.return_code).toBe(0);
    });
  });
});
