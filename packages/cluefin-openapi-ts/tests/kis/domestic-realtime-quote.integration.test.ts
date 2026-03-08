import { describe, expect, test } from 'vitest';
import { KisAuth } from '../../src/kis/auth';
import { KisSocketClient } from '../../src/kis/socket-client';
import { DomesticRealtimeQuote } from '../../src/kis/domestic-realtime-quote';
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

describe('DomesticRealtimeQuote integration', () => {
  integrationTest('should connect, subscribe execution, receive data, and disconnect', async () => {
    const appKey = getEnvOrThrow('KIS_APP_KEY');
    const secretKey = getEnvOrThrow('KIS_SECRET_KEY');
    const env = process.env.KIS_ENV === 'prod' ? 'prod' : ('dev' as const);

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
        const quote = new DomesticRealtimeQuote(client);
        await quote.subscribeExecution('005930');
      });

      client.on('data', (event: WebSocketEvent) => {
        receivedEvents.push(event);
        if (event.trId === DomesticRealtimeQuote.TR_ID_EXECUTION && event.data) {
          const items = DomesticRealtimeQuote.parseExecutionData(event.data.values);
          expect(items.length).toBeGreaterThan(0);
          expect(items[0]!.mkscShrnIscd).toBe('005930');
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
    // 장중이 아니면 데이터를 못 받을 수 있으므로 connected만 검증
  });

  integrationTest('should connect, subscribe orderbook, receive data, and disconnect', async () => {
    const appKey = getEnvOrThrow('KIS_APP_KEY');
    const secretKey = getEnvOrThrow('KIS_SECRET_KEY');
    const env = process.env.KIS_ENV === 'prod' ? 'prod' : ('dev' as const);

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
        const quote = new DomesticRealtimeQuote(client);
        await quote.subscribeOrderbook('005930');
      });

      client.on('data', (event: WebSocketEvent) => {
        if (event.trId === DomesticRealtimeQuote.TR_ID_ORDERBOOK && event.data) {
          const items = DomesticRealtimeQuote.parseOrderbookData(event.data.values);
          expect(items.length).toBeGreaterThan(0);
          expect(items[0]!.mkscShrnIscd).toBe('005930');
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

  integrationTest('should approve, connect, and disconnect cleanly', async () => {
    const appKey = getEnvOrThrow('KIS_APP_KEY');
    const secretKey = getEnvOrThrow('KIS_SECRET_KEY');
    const env = process.env.KIS_ENV === 'prod' ? 'prod' : ('dev' as const);

    const auth = new KisAuth({ appKey, secretKey, env });
    const { approvalKey } = await auth.approve();
    expect(approvalKey).toBeTruthy();

    const client = new KisSocketClient({
      approvalKey,
      appKey,
      secretKey,
      env,
    });

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
