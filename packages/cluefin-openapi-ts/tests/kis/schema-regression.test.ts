import { describe, expect, test } from 'vitest';

import { getFuturesBusinessDayInquiryResponseSchema } from '../../src/kis/schemas/domestic-issue-other';
import {
  getForeignNetBuyTrendByStockResponseSchema,
  getMemberTradingTrendTickResponseSchema,
  getProgramTradingSummaryIntradayResponseSchema,
} from '../../src/kis/schemas/domestic-market-analysis';

describe('KIS schema regression', () => {
  test('getForeignNetBuyTrendByStock matches live output schema', () => {
    const payload = {
      rt_cd: '0',
      msg_cd: '0000',
      msg1: 'OK',
      output: [
        {
          bsop_hour: '153049',
          stck_prpr: '179700',
          prdy_vrss: '-400',
          prdy_vrss_sign: '5',
          prdy_ctrt: '-0.22',
          acml_vol: '29102559',
          frgn_seln_vol: '9155337',
          frgn_shnu_vol: '511586',
          glob_ntby_qty: '-8643751',
          frgn_ntby_qty_icdc: '-596817',
        },
      ],
    };

    const body = getForeignNetBuyTrendByStockResponseSchema.parse(payload);

    expect(body.output).toHaveLength(1);
    expect(body.output[0]?.bsop_hour).toBe('153049');
    expect(body.output[0]?.acml_vol).toBe('29102559');
    expect(body.output[0]?.glob_ntby_qty).toBe('-8643751');
  });

  test('getMemberTradingTrendTick matches live output schema', () => {
    const payload = {
      rt_cd: '0',
      msg_cd: '0000',
      msg1: 'OK',
      output1: [
        {
          total_seln_qty: '9155337',
          total_shnu_qty: '511586',
        },
      ],
      output2: [
        {
          bsop_hour: '153049',
          mbcr_name: 'UBS',
          hts_kor_isnm: '삼성전자',
          stck_prpr: '179700',
          prdy_vrss: '-400',
          prdy_vrss_sign: '5',
          cntg_vol: '-596817',
          acml_ntby_qty: '-1904542',
          glob_ntby_qty: '-8643751',
          frgn_ntby_qty_icdc: '-596817',
        },
      ],
    };

    const body = getMemberTradingTrendTickResponseSchema.parse(payload);

    expect(body.output1).toHaveLength(1);
    expect(body.output1[0]?.total_seln_qty).toBe('9155337');
    expect(body.output2).toHaveLength(1);
    expect(body.output2[0]?.mbcr_name).toBe('UBS');
    expect(body.output2[0]?.acml_ntby_qty).toBe('-1904542');
  });

  test('getProgramTradingSummaryIntraday matches live output schema', () => {
    const payload = {
      rt_cd: '0',
      msg_cd: '0000',
      msg1: 'OK',
      output: [
        {
          bsop_hour: '180500',
          arbt_smtn_seln_tr_pbmn: '317582',
          arbt_smtn_shnu_tr_pbmn: '340577',
          nabt_smtn_seln_tr_pbmn: '8118891',
          nabt_smtn_shnu_tr_pbmn: '6179753',
          arbt_smtn_ntby_tr_pbmn: '22996',
          nabt_smtn_ntby_tr_pbmn: '-1939137',
          whol_smtn_ntby_tr_pbmn: '-1916142',
          bstp_nmix_prpr: '',
          bstp_nmix_prdy_vrss: '',
          prdy_vrss_sign: '',
        },
      ],
    };

    const body = getProgramTradingSummaryIntradayResponseSchema.parse(payload);

    expect(body.output).toHaveLength(1);
    expect(body.output[0]?.bsop_hour).toBe('180500');
    expect(body.output[0]?.nabt_smtn_ntby_tr_pbmn).toBe('-1939137');
    expect(body.output[0]?.prdy_vrss_sign).toBe('');
  });

  test('getFuturesBusinessDayInquiry matches live output schema', () => {
    const payload = {
      rt_cd: '0',
      msg_cd: '0000',
      msg1: 'OK',
      output1: {
        date1: '20260101',
        date2: '20260102',
        date3: '20260103',
        date4: '20260104',
        date5: '20260105',
        today: '20260101',
        time: '085000',
        s_time: '090000',
        e_time: '153000',
      },
    };

    const body = getFuturesBusinessDayInquiryResponseSchema.parse(payload);

    expect(body.output1?.today).toBe('20260101');
    expect(body.output1?.e_time).toBe('153000');
  });
});
