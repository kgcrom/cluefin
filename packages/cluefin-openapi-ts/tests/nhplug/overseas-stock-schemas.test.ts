import { describe, expect, it } from 'vitest';

import {
  overseasStockInquiryBalanceResponseSchema,
  overseasStockInquiryDailyTransactionResponseSchema,
  overseasStockInquiryMarginResponseSchema,
  overseasStockInquiryPeriodPnlResponseSchema,
} from '../../src/nhplug/schemas/overseas-stock-inquiry';
import {
  overseasStockOrderBuyResponseSchema,
  overseasStockOrderReservedSubmitResponseSchema,
} from '../../src/nhplug/schemas/overseas-stock-order';
import {
  overseasStockQuoteCurrentPriceResponseSchema,
  overseasStockQuotePeriodPriceResponseSchema,
  overseasStockQuoteSymbolIndexFxPeriodResponseSchema,
} from '../../src/nhplug/schemas/overseas-stock-quote';

describe('NH PLUG 해외주식(gbstock) 응답 스키마', () => {
  it('빈 봉투(Output 블록 없음)도 통과한다', () => {
    for (const schema of [
      overseasStockOrderBuyResponseSchema,
      overseasStockInquiryBalanceResponseSchema,
      overseasStockQuoteCurrentPriceResponseSchema,
    ]) {
      expect(schema.parse({ rsp_cd: '00000', rsp_msg: '정상처리 되었습니다.', message: null })).toMatchObject({
        rsp_cd: '00000',
      });
    }
  });

  it('스펙상 `message` 봉투를 파싱한다', () => {
    const parsed = overseasStockOrderBuyResponseSchema.parse({
      message: { msg_code: 'XA102', usr_msg: '모의투자 조회가 완료되었습니다', msg_lv_code: 'I', dvlp_msg_yn: 'N' },
    });
    expect(parsed.message?.msg_code).toBe('XA102');
  });

  it('주문 응답의 Output_0 은 객체이며 키 이름을 원문 그대로 유지한다', () => {
    const parsed = overseasStockOrderBuyResponseSchema.parse({
      rsp_cd: '00000',
      Output_0: { amn_tab_cd: '0001', orr_no: 12345 },
    });
    expect(parsed.Output_0?.orr_no).toBe(12345);

    const reserved = overseasStockOrderReservedSubmitResponseSchema.parse({
      Output_0: { bkg_rtn_orr_no: '778899' },
    });
    expect(reserved.Output_0?.bkg_rtn_orr_no).toBe(778899);
  });

  it('블록별 객체/배열 구조가 파이썬 타입과 같다', () => {
    // balance: Output_0 = 객체(잔고 요약), Output_1 = 배열(종목별)
    const balance = overseasStockInquiryBalanceResponseSchema.parse({
      Output_0: { tot_aet_amt: 1000 },
      Output_1: [{ iem_cd: 'AAPL', cns_bse_bnc_qty: 3 }],
    });
    expect(balance.Output_0?.tot_aet_amt).toBe(1000);
    expect(balance.Output_1?.[0]?.iem_cd).toBe('AAPL');

    // dailyTransaction: Output_0 = 배열(내역), Output_1 = 객체(요약) — balance 와 순서가 반대다.
    const daily = overseasStockInquiryDailyTransactionResponseSchema.parse({
      Output_0: [{ trd_dt: '20260822' }],
      Output_1: { amt_sum: 10 },
    });
    expect(daily.Output_0?.[0]?.trd_dt).toBe('20260822');
    expect(daily.Output_1?.amt_sum).toBe(10);

    // periodPnl: Output_0 = 객체(요약), Output_1 = 배열(일자별)
    const pnl = overseasStockInquiryPeriodPnlResponseSchema.parse({
      Output_0: { byn_qty_sum: 1 },
      Output_1: [{ orr_dt: '20260822' }],
    });
    expect(pnl.Output_0?.byn_qty_sum).toBe(1);
    expect(pnl.Output_1?.[0]?.orr_dt).toBe('20260822');

    // margin: Output_0 만 있고 배열이다.
    const margin = overseasStockInquiryMarginResponseSchema.parse({ Output_0: [{ cur_cd: 'USD', dca: 10 }] });
    expect(margin.Output_0).toHaveLength(1);

    // period: Output_0 / Output_1 둘 다 배열이다.
    const period = overseasStockQuotePeriodPriceResponseSchema.parse({
      Output_0: [{ iem_cd: 'AAPL' }],
      Output_1: [{ trade_date: '20260822', close_prc: 231.5 }],
    });
    expect(period.Output_1?.[0]?.close_prc).toBe(231.5);

    // symbolIndexFxPeriod: Output_0 = 객체, Output_1 = 배열
    const fx = overseasStockQuoteSymbolIndexFxPeriodResponseSchema.parse({
      Output_0: { iem_cd: 'SPX' },
      Output_1: [{ bsop_date: '20260822', vol: 12 }],
    });
    expect(fx.Output_0?.iem_cd).toBe('SPX');
    expect(fx.Output_1?.[0]?.vol).toBe(12);
  });

  it('숫자 필드가 문자열로 와도 숫자로 강제 변환한다', () => {
    const parsed = overseasStockQuoteCurrentPriceResponseSchema.parse({
      Output_0: { iem_cd: 'AAPL', trdprc: '231.55', acvol: '1234567' },
    });
    expect(parsed.Output_0?.trdprc).toBe(231.55);
    expect(parsed.Output_0?.acvol).toBe(1234567);
  });

  it('값 없는 숫자 필드의 빈 문자열은 null 로 접는다', () => {
    const parsed = overseasStockQuoteSymbolIndexFxPeriodResponseSchema.parse({
      Output_0: { iem_cd: 'SPX', ovrs_prpr: '', acml_vol: '' },
    });
    expect(parsed.Output_0?.ovrs_prpr).toBeNull();
    expect(parsed.Output_0?.acml_vol).toBeNull();
  });

  it('문서에 없는 실서버 필드는 passthrough 로 살아남는다', () => {
    const parsed = overseasStockQuoteCurrentPriceResponseSchema.parse({
      undocumented_top_level: 'keep',
      Output_0: { iem_cd: 'AAPL', undocumented_field: 'keep' },
    });
    expect(parsed).toMatchObject({ undocumented_top_level: 'keep' });
    expect(parsed.Output_0).toMatchObject({ undocumented_field: 'keep' });
  });

  it('모든 필드가 optional 이라 부분 응답도 통과한다', () => {
    expect(overseasStockInquiryMarginResponseSchema.parse({ Output_0: [{}] }).Output_0?.[0]).toEqual({});
  });
});
