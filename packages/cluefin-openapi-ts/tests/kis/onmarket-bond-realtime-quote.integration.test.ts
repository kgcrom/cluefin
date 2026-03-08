import { describe, expect, test } from 'vitest';
import { KisAuth } from '../../src/kis/auth';
import { KisSocketClient } from '../../src/kis/socket-client';
import { OnmarketBondRealtimeQuote } from '../../src/kis/onmarket-bond-realtime-quote';
import type { WebSocketEvent } from '../../src/core/websocket';

const runIntegration = process.env.CLUEFIN_OPENAPI_TS_RUN_INTEGRATION === '1';
const integrationTest = runIntegration ? test : test.skip;

const getEnvOrThrow = (key: string): string => {
  const value = process.env[key];
  if (!value) {
    throw new Error(`${key} is required for integration tests`);
  }
  return value;
};

describe('OnmarketBondRealtimeQuote integration', () => {
  integrationTest('should connect, subscribe bond execution, receive data, and disconnect', async () => {
    const appKey = getEnvOrThrow('KIS_APP_KEY');
    const secretKey = getEnvOrThrow('KIS_SECRET_KEY');
    const env = 'prod' as const;

    const auth = new KisAuth({ appKey, secretKey, env });
    const { approvalKey } = await auth.approve();

    const client = new KisSocketClient({
      approvalKey,
      appKey,
      secretKey,
      env,
    });

    const receivedEvents: WebSocketEvent[] = [];

    const result = await new Promise<{ connected: boolean; dataReceived: boolean }>((resolve) => {
      const timeout = setTimeout(() => {
        client.close();
        resolve({ connected: true, dataReceived: receivedEvents.length > 0 });
      }, 10_000);

      client.on('connected', async () => {
        const quote = new OnmarketBondRealtimeQuote(client);
        await quote.subscribeBondExecution('KR1035010001');
      });

      client.on('data', (event: WebSocketEvent) => {
        receivedEvents.push(event);
        if (event.trId === OnmarketBondRealtimeQuote.TR_ID_BOND_EXECUTION && event.data) {
          const items = OnmarketBondRealtimeQuote.parseBondExecutionData(event.data.values);
          expect(items.length).toBeGreaterThan(0);
          expect(items[0]!.stndIscd).toBe('KR1035010001');
          clearTimeout(timeout);
          client.close();
          resolve({ connected: true, dataReceived: true });
        }
      });

      client.on('error', (event: WebSocketEvent) => {
        clearTimeout(timeout);
        client.close();
        throw event.error ?? new Error('WebSocket error');
      });

      client.connect();
    });

    expect(result.connected).toBe(true);
  });

  integrationTest('should connect, subscribe bond orderbook, receive data, and disconnect', async () => {
    const appKey = getEnvOrThrow('KIS_APP_KEY');
    const secretKey = getEnvOrThrow('KIS_SECRET_KEY');
    const env = 'prod' as const;

    const auth = new KisAuth({ appKey, secretKey, env });
    const { approvalKey } = await auth.approve();

    const client = new KisSocketClient({
      approvalKey,
      appKey,
      secretKey,
      env,
    });

    const result = await new Promise<{ connected: boolean; dataReceived: boolean }>((resolve) => {
      const timeout = setTimeout(() => {
        client.close();
        resolve({ connected: true, dataReceived: false });
      }, 10_000);

      client.on('connected', async () => {
        const quote = new OnmarketBondRealtimeQuote(client);
        await quote.subscribeBondOrderbook('KR1035010001');
      });

      client.on('data', (event: WebSocketEvent) => {
        if (event.trId === OnmarketBondRealtimeQuote.TR_ID_BOND_ORDERBOOK && event.data) {
          const items = OnmarketBondRealtimeQuote.parseBondOrderbookData(event.data.values);
          expect(items.length).toBeGreaterThan(0);
          expect(items[0]!.stndIscd).toBe('KR1035010001');
          clearTimeout(timeout);
          client.close();
          resolve({ connected: true, dataReceived: true });
        }
      });

      client.on('error', (event: WebSocketEvent) => {
        clearTimeout(timeout);
        client.close();
        throw event.error ?? new Error('WebSocket error');
      });

      client.connect();
    });

    expect(result.connected).toBe(true);
  });

  integrationTest('should connect, subscribe bond index execution, receive data, and disconnect', async () => {
    const appKey = getEnvOrThrow('KIS_APP_KEY');
    const secretKey = getEnvOrThrow('KIS_SECRET_KEY');
    const env = 'prod' as const;

    const auth = new KisAuth({ appKey, secretKey, env });
    const { approvalKey } = await auth.approve();

    const client = new KisSocketClient({
      approvalKey,
      appKey,
      secretKey,
      env,
    });

    const result = await new Promise<{ connected: boolean; dataReceived: boolean }>((resolve) => {
      const timeout = setTimeout(() => {
        client.close();
        resolve({ connected: true, dataReceived: false });
      }, 10_000);

      client.on('connected', async () => {
        const quote = new OnmarketBondRealtimeQuote(client);
        await quote.subscribeBondIndexExecution('BOND001');
      });

      client.on('data', (event: WebSocketEvent) => {
        if (event.trId === OnmarketBondRealtimeQuote.TR_ID_BOND_INDEX_EXECUTION && event.data) {
          const items = OnmarketBondRealtimeQuote.parseBondIndexExecutionData(event.data.values);
          expect(items.length).toBeGreaterThan(0);
          clearTimeout(timeout);
          client.close();
          resolve({ connected: true, dataReceived: true });
        }
      });

      client.on('error', (event: WebSocketEvent) => {
        clearTimeout(timeout);
        client.close();
        throw event.error ?? new Error('WebSocket error');
      });

      client.connect();
    });

    expect(result.connected).toBe(true);
  });
});
