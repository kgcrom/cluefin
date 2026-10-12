import { describe, expect, test } from 'vitest';
import { OverseasRealtimeQuote } from '../../src/kis/overseas-realtime-quote';
import { receiveFirstKisData } from '../_helpers/kis-realtime';
import { isUsMarketHours } from '../_helpers/market-hours';

const runIntegration = process.env.CLUEFIN_OPENAPI_TS_RUN_INTEGRATION === '1';
// 미국 정규장에만 돈다. 그 시간에 AAPL 은 계속 체결되므로 데이터가 안 오면 실패다.
const integrationTest = runIntegration && isUsMarketHours() ? test : test.skip;

const RECEIVE_TIMEOUT_MS = 30_000;

describe('OverseasRealtimeQuote integration', () => {
  integrationTest('should receive and parse execution data', async () => {
    const event = await receiveFirstKisData({
      env: 'prod',
      trId: OverseasRealtimeQuote.TR_ID_EXECUTION,
      timeoutMs: RECEIVE_TIMEOUT_MS,
      subscribe: (client) => new OverseasRealtimeQuote(client).subscribeExecution('DNASAAPL'),
    });

    expect(event, `no execution data for AAPL within ${RECEIVE_TIMEOUT_MS}ms`).toBeDefined();
    const items = OverseasRealtimeQuote.parseExecutionData(event?.data?.values ?? []);
    expect(items.length).toBeGreaterThan(0);
    expect(items[0]?.symb).toBe('AAPL');
  });

  integrationTest('should receive and parse orderbook data', async () => {
    const event = await receiveFirstKisData({
      env: 'prod',
      trId: OverseasRealtimeQuote.TR_ID_ORDERBOOK,
      timeoutMs: RECEIVE_TIMEOUT_MS,
      subscribe: (client) => new OverseasRealtimeQuote(client).subscribeOrderbook('AAPL', 'NAS'),
    });

    expect(event, `no orderbook data for AAPL within ${RECEIVE_TIMEOUT_MS}ms`).toBeDefined();
    const items = OverseasRealtimeQuote.parseOrderbookData(event?.data?.values ?? []);
    expect(items.length).toBeGreaterThan(0);
    expect(items[0]?.symb).toBe('AAPL');
  });
});
