/**
 * NH PLUG 국내주식 시세(krstock quote) 통합 테스트.
 *
 * 시세 조회 API 는 계좌번호가 필요 없다 — 계좌 게이팅을 하지 않는다.
 * 휴일에도 조회된다 (파이썬 스위트 2026-08-22 실측 확인).
 */
import { describe, test } from 'vitest';

import {
  krStockQuoteAfterHoursCurrentResponseSchema,
  krStockQuoteAfterHoursExpectedResponseSchema,
  krStockQuoteCurrentAfterHoursDailyResponseSchema,
  krStockQuoteCurrentAfterHoursExecutionResponseSchema,
  krStockQuoteCurrentDailyResponseSchema,
  krStockQuoteCurrentExecutionResponseSchema,
  krStockQuoteCurrentInvestorResponseSchema,
  krStockQuoteCurrentPriceResponseSchema,
  krStockQuoteEtfComponentsResponseSchema,
  krStockQuoteEtfCurrentResponseSchema,
  krStockQuotePeriodResponseSchema,
} from '../../src/nhplug/schemas/krstock-quote';
import {
  assertNhplugResponse,
  assertNhplugResponseShape,
  callNhplug,
  getNhplugClient,
  NHPLUG_TEST_ETF_IEM_CD,
  NHPLUG_TEST_IEM_CD,
  runNhplugIntegration,
  setupNhplugRateLimit,
  TODAY,
} from '../_helpers/integration-setup';

const it = runNhplugIntegration ? test : test.skip;

describe('Nhplug KrstockQuote', () => {
  setupNhplugRateLimit();

  it('currentPrice', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () =>
      client.krstockQuote.currentPrice({ marketCd: 'KRX', iemCd: NHPLUG_TEST_IEM_CD }),
    );
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, krStockQuoteCurrentPriceResponseSchema);
  });

  it('currentExecution', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () =>
      client.krstockQuote.currentExecution({ marketCd: 'KRX', iemCd: NHPLUG_TEST_IEM_CD }),
    );
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, krStockQuoteCurrentExecutionResponseSchema);
  });

  it('currentDaily', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () =>
      client.krstockQuote.currentDaily({ marketCd: 'KRX', iemCd: NHPLUG_TEST_IEM_CD }),
    );
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, krStockQuoteCurrentDailyResponseSchema);
  });

  it('currentInvestor', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () =>
      client.krstockQuote.currentInvestor({ marketCd: 'KRX', iemCd: NHPLUG_TEST_IEM_CD, arrayCnt: '10' }),
    );
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, krStockQuoteCurrentInvestorResponseSchema);
  });

  it('period', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () =>
      client.krstockQuote.period({
        marketCd: 'KRX',
        iemCd: NHPLUG_TEST_IEM_CD,
        gubun: '1', // 일봉
        edate: TODAY,
        arrayCnt: '30', // 최근 한 달치
      }),
    );
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, krStockQuotePeriodResponseSchema);
  });

  it('afterHoursCurrent', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () => client.krstockQuote.afterHoursCurrent({ iemCd: NHPLUG_TEST_IEM_CD }));
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, krStockQuoteAfterHoursCurrentResponseSchema);
  });

  it('currentAfterHoursDaily', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () =>
      client.krstockQuote.currentAfterHoursDaily({
        iemCd: NHPLUG_TEST_IEM_CD,
        date: TODAY,
        arrayCnt: '10',
        maxavg: '5',
        gubun: '1',
      }),
    );
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, krStockQuoteCurrentAfterHoursDailyResponseSchema);
  });

  it('currentAfterHoursExecution', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () =>
      client.krstockQuote.currentAfterHoursExecution({ iemCd: NHPLUG_TEST_IEM_CD }),
    );
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, krStockQuoteCurrentAfterHoursExecutionResponseSchema);
  });

  it('afterHoursExpected', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () => client.krstockQuote.afterHoursExpected({ iemCd: NHPLUG_TEST_IEM_CD }));
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, krStockQuoteAfterHoursExpectedResponseSchema);
  });

  it('etfCurrent', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () => client.krstockQuote.etfCurrent({ iemCd: NHPLUG_TEST_ETF_IEM_CD }));
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, krStockQuoteEtfCurrentResponseSchema);
  });

  it('etfComponents', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () => client.krstockQuote.etfComponents({ iemCd: NHPLUG_TEST_ETF_IEM_CD }));
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, krStockQuoteEtfComponentsResponseSchema);
  });
});
