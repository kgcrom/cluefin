/**
 * NH PLUG 국내주식 시세(krstock quote) 통합 테스트.
 *
 * 시세 조회 API 는 계좌번호가 필요 없다 — 계좌 게이팅을 하지 않는다.
 * 휴일에도 조회된다 (파이썬 스위트 2026-08-22 실측 확인).
 *
 * **11종 모두 운영 도메인 전용이다.** 모의투자(moapi)는 `IGW40023`
 * ("모의투자에서는 제공하지 않는 API입니다. 실전투자 환경을 이용해주세요.")로
 * 거부한다 (2026-09-23 실측, 파이썬 스위트와 동일). 따라서 `NHPLUG_ENV=prod` 에서만
 * 실행되고, 모의투자에서는 통째로 skip 된다.
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
  runNhplugLiveOnlyIntegration,
  setupNhplugRateLimit,
  TODAY,
} from '../_helpers/integration-setup';

/** 모의투자에서는 제공되지 않는다 (IGW40023). 운영(NHPLUG_ENV=prod)에서만 검증 가능. */
const liveOnlyIt = runNhplugLiveOnlyIntegration ? test : test.skip;

describe('Nhplug KrstockQuote (운영 전용)', () => {
  setupNhplugRateLimit();

  liveOnlyIt('currentPrice', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () =>
      client.krstockQuote.currentPrice({ marketCd: 'KRX', iemCd: NHPLUG_TEST_IEM_CD }),
    );
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, krStockQuoteCurrentPriceResponseSchema);
  });

  liveOnlyIt('currentExecution', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () =>
      client.krstockQuote.currentExecution({ marketCd: 'KRX', iemCd: NHPLUG_TEST_IEM_CD }),
    );
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, krStockQuoteCurrentExecutionResponseSchema);
  });

  liveOnlyIt('currentDaily', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () =>
      client.krstockQuote.currentDaily({ marketCd: 'KRX', iemCd: NHPLUG_TEST_IEM_CD }),
    );
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, krStockQuoteCurrentDailyResponseSchema);
  });

  liveOnlyIt('currentInvestor', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () =>
      client.krstockQuote.currentInvestor({ marketCd: 'KRX', iemCd: NHPLUG_TEST_IEM_CD, arrayCnt: '10' }),
    );
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, krStockQuoteCurrentInvestorResponseSchema);
  });

  liveOnlyIt('period', async (ctx) => {
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

  liveOnlyIt('afterHoursCurrent', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () => client.krstockQuote.afterHoursCurrent({ iemCd: NHPLUG_TEST_IEM_CD }));
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, krStockQuoteAfterHoursCurrentResponseSchema);
  });

  liveOnlyIt('currentAfterHoursDaily', async (ctx) => {
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

  liveOnlyIt('currentAfterHoursExecution', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () =>
      client.krstockQuote.currentAfterHoursExecution({ iemCd: NHPLUG_TEST_IEM_CD }),
    );
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, krStockQuoteCurrentAfterHoursExecutionResponseSchema);
  });

  liveOnlyIt('afterHoursExpected', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () => client.krstockQuote.afterHoursExpected({ iemCd: NHPLUG_TEST_IEM_CD }));
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, krStockQuoteAfterHoursExpectedResponseSchema);
  });

  liveOnlyIt('etfCurrent', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () => client.krstockQuote.etfCurrent({ iemCd: NHPLUG_TEST_ETF_IEM_CD }));
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, krStockQuoteEtfCurrentResponseSchema);
  });

  liveOnlyIt('etfComponents', async (ctx) => {
    const client = await getNhplugClient();
    const res = await callNhplug(ctx, () => client.krstockQuote.etfComponents({ iemCd: NHPLUG_TEST_ETF_IEM_CD }));
    assertNhplugResponse(res);
    assertNhplugResponseShape(res.body, krStockQuoteEtfComponentsResponseSchema);
  });
});
