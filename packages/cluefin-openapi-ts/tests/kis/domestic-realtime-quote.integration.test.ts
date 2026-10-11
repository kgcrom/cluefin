import { describe, expect, test } from 'vitest';
import { DomesticRealtimeQuote } from '../../src/kis/domestic-realtime-quote';
import { createKisSocketClient, kisEnv, receiveFirstKisData } from '../_helpers/kis-realtime';
import { isKrxContinuousHours } from '../_helpers/market-hours';

const runIntegration = process.env.CLUEFIN_OPENAPI_TS_RUN_INTEGRATION === '1';
// H0UNCNT0(체결가 통합)는 모의투자 미지원이라 prod 에서만 돈다. 연속매매(09:00–15:20) 동안 005930 은
// 몇 초마다 체결되므로, 그 시간에 데이터가 안 오면 실패다 — Python 실시간 통합 테스트와 같은 기준.
const integrationTest = runIntegration && kisEnv === 'prod' && isKrxContinuousHours() ? test : test.skip;

const STOCK_CODE = '005930';
const RECEIVE_TIMEOUT_MS = 30_000;

describe('DomesticRealtimeQuote integration', () => {
  integrationTest('should receive and parse execution data', async () => {
    const event = await receiveFirstKisData({
      env: 'prod',
      trId: DomesticRealtimeQuote.TR_ID_EXECUTION,
      timeoutMs: RECEIVE_TIMEOUT_MS,
      subscribe: (client) => new DomesticRealtimeQuote(client).subscribeExecution(STOCK_CODE),
    });

    expect(event, `no execution data for ${STOCK_CODE} within ${RECEIVE_TIMEOUT_MS}ms`).toBeDefined();
    const items = DomesticRealtimeQuote.parseExecutionData(event?.data?.values ?? []);
    expect(items.length).toBeGreaterThan(0);
    expect(items[0]?.mkscShrnIscd).toBe(STOCK_CODE);
  });

  integrationTest('should receive and parse orderbook data', async () => {
    const event = await receiveFirstKisData({
      env: 'prod',
      trId: DomesticRealtimeQuote.TR_ID_ORDERBOOK,
      timeoutMs: RECEIVE_TIMEOUT_MS,
      subscribe: (client) => new DomesticRealtimeQuote(client).subscribeOrderbook(STOCK_CODE),
    });

    expect(event, `no orderbook data for ${STOCK_CODE} within ${RECEIVE_TIMEOUT_MS}ms`).toBeDefined();
    const items = DomesticRealtimeQuote.parseOrderbookData(event?.data?.values ?? []);
    expect(items.length).toBeGreaterThan(0);
    expect(items[0]?.mkscShrnIscd).toBe(STOCK_CODE);
  });

  integrationTest('should approve, connect, and disconnect cleanly', async () => {
    const client = await createKisSocketClient('prod');

    const connected = await new Promise<boolean>((resolve) => {
      const timeout = setTimeout(() => {
        client.close();
        resolve(false);
      }, 5_000);

      client.on('connected', () => {
        clearTimeout(timeout);
        expect(client.connected).toBe(true);
        client.close();
        resolve(true);
      });

      client.on('error', () => {
        clearTimeout(timeout);
        client.close();
        resolve(false);
      });

      client.connect();
    });

    expect(connected).toBe(true);
  });
});
