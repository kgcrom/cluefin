import { describe, expect, test } from 'vitest';
import { OnmarketBondRealtimeQuote } from '../../src/kis/onmarket-bond-realtime-quote';
import { receiveFirstKisData } from '../_helpers/kis-realtime';
import { isKrxMarketHours } from '../_helpers/market-hours';

const runIntegration = process.env.CLUEFIN_OPENAPI_TS_RUN_INTEGRATION === '1';
// 장외에는 시세가 오지 않는다 — Python 실시간 통합 테스트와 같은 시간 가드. 채권 한 종목은 장중에도 체결이
// 드물어서, 시간 안에 데이터가 안 오면 실패가 아니라 skip 한다(Python 과 같다).
const integrationTest = runIntegration && isKrxMarketHours() ? test : test.skip;

// 국고01500-5003(20-2). inquire-price 로 실재하는 종목임을 확인(2026-10-11). 예전 값 KR1035010001 은 없는 종목이었다.
const BOND_CODE = 'KR103502GA34';
// H0BICNT0 요청 예시값(KIS 포털). 예전 값 BOND001 은 근거가 없었다.
const BOND_INDEX_CODE = 'KBPR01';
const RECEIVE_TIMEOUT_MS = 30_000;

describe('OnmarketBondRealtimeQuote integration', () => {
  integrationTest('should receive and parse bond execution data', async (ctx) => {
    const event = await receiveFirstKisData({
      env: 'prod',
      trId: OnmarketBondRealtimeQuote.TR_ID_BOND_EXECUTION,
      timeoutMs: RECEIVE_TIMEOUT_MS,
      subscribe: (client) => new OnmarketBondRealtimeQuote(client).subscribeBondExecution(BOND_CODE),
    });
    if (!event) {
      ctx.skip(`no bond execution for ${BOND_CODE} within ${RECEIVE_TIMEOUT_MS}ms (thinly traded)`);
      return;
    }

    const items = OnmarketBondRealtimeQuote.parseBondExecutionData(event.data?.values ?? []);
    expect(items.length).toBeGreaterThan(0);
    expect(items[0]?.stndIscd).toBe(BOND_CODE);
  });

  integrationTest('should receive and parse bond orderbook data', async (ctx) => {
    const event = await receiveFirstKisData({
      env: 'prod',
      trId: OnmarketBondRealtimeQuote.TR_ID_BOND_ORDERBOOK,
      timeoutMs: RECEIVE_TIMEOUT_MS,
      subscribe: (client) => new OnmarketBondRealtimeQuote(client).subscribeBondOrderbook(BOND_CODE),
    });
    if (!event) {
      ctx.skip(`no bond orderbook for ${BOND_CODE} within ${RECEIVE_TIMEOUT_MS}ms (thinly traded)`);
      return;
    }

    const items = OnmarketBondRealtimeQuote.parseBondOrderbookData(event.data?.values ?? []);
    expect(items.length).toBeGreaterThan(0);
    expect(items[0]?.stndIscd).toBe(BOND_CODE);
  });

  integrationTest('should receive and parse bond index execution data', async (ctx) => {
    const event = await receiveFirstKisData({
      env: 'prod',
      trId: OnmarketBondRealtimeQuote.TR_ID_BOND_INDEX_EXECUTION,
      timeoutMs: RECEIVE_TIMEOUT_MS,
      subscribe: (client) => new OnmarketBondRealtimeQuote(client).subscribeBondIndexExecution(BOND_INDEX_CODE),
    });
    if (!event) {
      ctx.skip(`no bond index data for ${BOND_INDEX_CODE} within ${RECEIVE_TIMEOUT_MS}ms`);
      return;
    }

    const items = OnmarketBondRealtimeQuote.parseBondIndexExecutionData(event.data?.values ?? []);
    expect(items.length).toBeGreaterThan(0);
  });
});
