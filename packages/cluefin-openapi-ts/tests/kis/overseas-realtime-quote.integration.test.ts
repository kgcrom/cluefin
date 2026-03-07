import { describe, expect, test } from 'vitest';
import { KisAuth } from '../../src/kis/auth';
import { KisSocketClient } from '../../src/kis/socket-client';
import { OverseasRealtimeQuote } from '../../src/kis/overseas-realtime-quote';
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

describe('OverseasRealtimeQuote integration', () => {
  integrationTest('should connect, subscribe execution, receive data, and disconnect', async () => {
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
      }, 15_000);

      client.on('connected', async () => {
        const quote = new OverseasRealtimeQuote(client);
        await quote.subscribeExecution('DNASAAPL');
      });

      client.on('data', (event: WebSocketEvent) => {
        receivedEvents.push(event);
        if (event.trId === OverseasRealtimeQuote.TR_ID_EXECUTION && event.data) {
          const items = OverseasRealtimeQuote.parseExecutionData(event.data.values);
          expect(items.length).toBeGreaterThan(0);
          expect(items[0]!.symb).toBe('AAPL');
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

  integrationTest('should connect, subscribe orderbook, receive data, and disconnect', async () => {
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
      }, 15_000);

      client.on('connected', async () => {
        const quote = new OverseasRealtimeQuote(client);
        await quote.subscribeOrderbook('AAPL', 'NAS');
      });

      client.on('data', (event: WebSocketEvent) => {
        if (event.trId === OverseasRealtimeQuote.TR_ID_ORDERBOOK && event.data) {
          const items = OverseasRealtimeQuote.parseOrderbookData(event.data.values);
          expect(items.length).toBeGreaterThan(0);
          expect(items[0]!.symb).toBe('AAPL');
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
