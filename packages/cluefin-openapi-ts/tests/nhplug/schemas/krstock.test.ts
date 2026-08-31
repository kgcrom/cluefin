import { describe, expect, it } from 'vitest';

import { accountListResponseSchema, websocketCloseResponseSchema } from '../../../src/nhplug/schemas/common';
import {
  krStockInquiryBalanceResponseSchema,
  krStockInquiryDailyOrderExecutionResponseSchema,
  krStockInquiryRightsScheduledResponseSchema,
} from '../../../src/nhplug/schemas/krstock-inquiry';
import {
  krStockOrderCashBuyResponseSchema,
  krStockOrderReservedCancelResponseSchema,
} from '../../../src/nhplug/schemas/krstock-order';
import {
  krStockQuoteCurrentExecutionResponseSchema,
  krStockQuoteEtfCurrentResponseSchema,
} from '../../../src/nhplug/schemas/krstock-quote';

describe('nhplug common schemas', () => {
  it('parses the account list with its Output_0 array', () => {
    const parsed = accountListResponseSchema.parse({
      rsp_cd: '00000',
      rsp_msg: '정상',
      cust_no: '123',
      Output_0: [{ acct_no: '12345678901', acct_type: '03' }],
    });

    expect(parsed.Output_0?.[0]?.acct_no).toBe('12345678901');
  });

  it('accepts a websocket close response that only carries the envelope', () => {
    expect(websocketCloseResponseSchema.parse({ rsp_cd: '00000', rsp_msg: '정상' })).toEqual({
      rsp_cd: '00000',
      rsp_msg: '정상',
    });
  });
});

describe('nhplug krstock order schemas', () => {
  it('parses a cash-buy acknowledgement and coerces numeric strings', () => {
    const parsed = krStockOrderCashBuyResponseSchema.parse({
      rsp_cd: '00000',
      rsp_msg: '정상',
      message: null,
      Output_0: { orr_gno_tab_cd: '0001', mkt_orr_no: '123456', orr_qty1: 10 },
    });

    // 스펙은 int 지만 실서버가 문자열을 줄 수 있어 coerce 로 받는다.
    expect(parsed.Output_0?.mkt_orr_no).toBe(123456);
    expect(parsed.Output_0?.orr_qty1).toBe(10);
  });

  it('keeps undocumented live fields through passthrough', () => {
    const parsed = krStockOrderReservedCancelResponseSchema.parse({
      rsp_cd: '00000',
      Output_0: { act_no: '12345678901', bkg_orr_no: 7, undocumented_field: 'kept' },
    }) as { Output_0?: Record<string, unknown> };

    expect(parsed.Output_0?.undocumented_field).toBe('kept');
  });

  it('tolerates a response with no Output block at all', () => {
    expect(() => krStockOrderCashBuyResponseSchema.parse({ rsp_cd: '00000', rsp_msg: '정상' })).not.toThrow();
  });
});

describe('nhplug krstock inquiry schemas', () => {
  it('reads balance as Output_0 object + Output_1 array', () => {
    const parsed = krStockInquiryBalanceResponseSchema.parse({
      rsp_cd: '00000',
      Output_0: { dca: 1_000_000, act_no: '12345678901' },
      Output_1: [{ iem_cd: '005930', iem_nm: '삼성전자', now_pr: 70_000 }],
    });

    expect(parsed.Output_0?.dca).toBe(1_000_000);
    expect(parsed.Output_1?.[0]?.iem_cd).toBe('005930');
  });

  it('keeps int|str union fields as-is when they are not numeric', () => {
    const parsed = krStockInquiryBalanceResponseSchema.parse({
      rsp_cd: '00000',
      Output_0: { fc_dca: '', orr_pbl_amt: 5000 },
    });

    expect(parsed.Output_0?.fc_dca).toBe('');
    expect(parsed.Output_0?.orr_pbl_amt).toBe(5000);
  });

  it('accepts dailyOrderExecution Output_0 as both object and array', () => {
    const asObject = krStockInquiryDailyOrderExecutionResponseSchema.parse({
      rsp_cd: 'XA102',
      Output_0: { cus_fnm: '홍길동' },
    });
    const asArray = krStockInquiryDailyOrderExecutionResponseSchema.parse({
      rsp_cd: 'XA102',
      Output_0: [{ cus_fnm: '홍길동' }],
    });

    expect(Array.isArray(asObject.Output_0)).toBe(false);
    expect(Array.isArray(asArray.Output_0)).toBe(true);
  });

  it('reads rightsScheduled as a bare Output_0 array', () => {
    const parsed = krStockInquiryRightsScheduledResponseSchema.parse({
      rsp_cd: '00000',
      Output_0: [{ iem_cd: '005930' }],
    });

    expect(parsed.Output_0).toHaveLength(1);
  });
});

describe('nhplug krstock quote schemas', () => {
  it('reads currentExecution as Output_0 array + Output_1 summary object', () => {
    const parsed = krStockQuoteCurrentExecutionResponseSchema.parse({
      rsp_cd: '00000',
      Output_0: [{ iem_cd: '005930' }, { iem_cd: '005930' }],
      Output_1: { iem_cd: '005930' },
    });

    expect(parsed.Output_0).toHaveLength(2);
    expect(Array.isArray(parsed.Output_1)).toBe(false);
  });

  it('reads etfCurrent five Output blocks with only Output_1 as an array', () => {
    const parsed = krStockQuoteEtfCurrentResponseSchema.parse({
      rsp_cd: '00000',
      Output_0: {},
      Output_1: [{}],
      Output_2: {},
      Output_3: {},
      Output_4: {},
    });

    expect(Array.isArray(parsed.Output_1)).toBe(true);
    expect(Array.isArray(parsed.Output_3)).toBe(false);
  });
});
