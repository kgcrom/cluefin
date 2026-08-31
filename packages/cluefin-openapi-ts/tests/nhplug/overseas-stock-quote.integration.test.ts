/**
 * NH PLUG 해외주식 시세(gbstock quote) 통합 테스트.
 *
 * 시세 조회 API 는 계좌번호가 필요 없다 — 계좌 게이팅을 하지 않는다.
 *
 * **4종 모두 운영 도메인 전용이다.** 모의투자(moapi)는 어떤 종목코드로 호출해도
 * `IGW40019 "종목코드(iem_cd)를 확인해주세요"` 로 거부하는데, 이는 잘못된 코드라는
 * 뜻이 아니라 "모의투자에 제공되지 않는 서비스"라는 뜻이다 (2026-08-22 실측).
 * 따라서 `NHPLUG_ENV=prod` 에서만 실행되고, 모의투자에서는 통째로 skip 된다.
 */
import { describe, test } from 'vitest';

import {
  overseasStockQuoteCurrentPriceResponseSchema,
  overseasStockQuoteExecutionTrendResponseSchema,
  overseasStockQuotePeriodPriceResponseSchema,
  overseasStockQuoteSymbolIndexFxPeriodResponseSchema,
} from '../../src/nhplug/schemas/overseas-stock-quote';
import {
  assertNhplugResponse,
  assertNhplugResponseShape,
  callNhplug,
  getNhplugClient,
  NHPLUG_TEST_GB_IEM_CD,
  NHPLUG_TEST_GB_SYMBOL_CD,
  runNhplugLiveOnlyIntegration,
  setupNhplugRateLimit,
  TODAY,
} from '../_helpers/integration-setup';

/** 모의투자에서는 제공되지 않는다 (IGW40019). 운영(NHPLUG_ENV=prod)에서만 검증 가능. */
const liveOnlyIt = runNhplugLiveOnlyIntegration ? test : test.skip;

describe('Nhplug OverseasStockQuote (운영 전용)', () => {
  setupNhplugRateLimit();

  liveOnlyIt('current', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () => client.overseasStockQuote.current({ iemCd: NHPLUG_TEST_GB_IEM_CD }));
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, overseasStockQuoteCurrentPriceResponseSchema);
  });

  liveOnlyIt('executionTrend', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () =>
      client.overseasStockQuote.executionTrend({
        periodType: '2', // 일별
        reqCnt: '10',
        iemCd: NHPLUG_TEST_GB_IEM_CD,
      }),
    );
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, overseasStockQuoteExecutionTrendResponseSchema);
  });

  liveOnlyIt('period', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () =>
      client.overseasStockQuote.period({
        iemCd: NHPLUG_TEST_GB_IEM_CD,
        endDt: TODAY,
        count: '0030', // 최근 한 달치
        maxavg: '005',
        gubun: '3', // 일
        xtick: '0001',
        todayCls: '1', // 당일조회
        marketCls: '1', // 정규장
      }),
    );
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, overseasStockQuotePeriodPriceResponseSchema);
  });

  liveOnlyIt('symbolIndexFxPeriod', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () =>
      client.overseasStockQuote.symbolIndexFxPeriod({
        iemCd: NHPLUG_TEST_GB_SYMBOL_CD,
        endDt: TODAY,
        arrayCnt: '0030', // 최근 한 달치
        maxavg: '005',
        gubun: '1', // 일
        todayCls: '0', // 전체조회
      }),
    );
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, overseasStockQuoteSymbolIndexFxPeriodResponseSchema);
  });
});
