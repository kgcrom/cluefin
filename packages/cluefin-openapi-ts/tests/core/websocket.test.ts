import { describe, expect, it } from 'vitest';

import { BaseWebSocketClient, type SubscriptionType, type WebSocketEvent } from '../../src/core/websocket';

class TestWebSocketClient extends BaseWebSocketClient {
  public constructor() {
    super({ url: 'ws://example.test', rateLimitBurst: 10, rateLimitRequestsPerSecond: 10 });
  }

  protected buildSubscriptionMessage(trId: string, trKey: string, trType: SubscriptionType): string {
    return JSON.stringify({ trId, trKey, trType });
  }
}

interface MutableClient {
  ws: { sent: string[]; send: (message: string) => void; close: () => void } | null;
  _connected: boolean;
  handleMessage(raw: string): void;
}

const attachSocket = (client: TestWebSocketClient): MutableClient['ws'] => {
  const socket = {
    sent: [] as string[],
    send(message: string) {
      this.sent.push(message);
    },
    close() {
      this.sent.push('closed');
    },
  };
  const mutable = client as unknown as MutableClient;
  mutable.ws = socket;
  mutable._connected = true;
  return socket;
};

describe('BaseWebSocketClient', () => {
  it('rejects subscribe and unsubscribe while disconnected', async () => {
    const client = new TestWebSocketClient();

    await expect(client.subscribe('TR', 'KEY')).rejects.toThrow('WebSocket not connected');
    await expect(client.unsubscribe('TR', 'KEY')).rejects.toThrow('WebSocket not connected');
  });

  it('subscribes once, emits events, and skips duplicate subscriptions', async () => {
    const client = new TestWebSocketClient();
    const socket = attachSocket(client);
    const events: WebSocketEvent[] = [];
    client.on('subscribed', (event) => events.push(event));

    await client.subscribe('TR', 'KEY');
    await client.subscribe('TR', 'KEY');

    expect(socket.sent).toEqual([JSON.stringify({ trId: 'TR', trKey: 'KEY', trType: '1' })]);
    expect(client.subscriptions.get('TR:KEY')).toBe('KEY');
    expect(events).toEqual([{ eventType: 'subscribed', trId: 'TR', trKey: 'KEY' }]);
  });

  it('unsubscribes existing subscriptions and skips missing subscriptions', async () => {
    const client = new TestWebSocketClient();
    const socket = attachSocket(client);
    const events: WebSocketEvent[] = [];
    client.on('unsubscribed', (event) => events.push(event));

    await client.subscribe('TR', 'KEY');
    socket.sent = [];

    await client.unsubscribe('TR', 'KEY');
    await client.unsubscribe('TR', 'KEY');

    expect(socket.sent).toEqual([JSON.stringify({ trId: 'TR', trKey: 'KEY', trType: '2' })]);
    expect(client.subscriptions.size).toBe(0);
    expect(events).toEqual([{ eventType: 'unsubscribed', trId: 'TR', trKey: 'KEY' }]);
  });

  it('handles ping and data messages', () => {
    const client = new TestWebSocketClient();
    const socket = attachSocket(client);
    const dataEvents: WebSocketEvent[] = [];
    client.on('data', (event) => dataEvents.push(event));
    const mutable = client as unknown as MutableClient;

    mutable.handleMessage('PINGPONG');
    mutable.handleMessage('0|H0STASP0|001|123^456');

    expect(socket.sent).toEqual(['PINGPONG']);
    expect(dataEvents).toEqual([
      {
        eventType: 'data',
        trId: 'H0STASP0',
        data: { values: ['123', '456'], encrypted: false },
        raw: '0|H0STASP0|001|123^456',
      },
    ]);
  });

  it('closes the active socket and clears connected state', () => {
    const client = new TestWebSocketClient();
    const socket = attachSocket(client);

    client.close();

    expect(client.connected).toBe(false);
    expect(socket.sent).toEqual(['closed']);
  });
});
