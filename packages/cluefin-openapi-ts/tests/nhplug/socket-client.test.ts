import { describe, expect, it } from 'vitest';

import { BaseWebSocketClient, type WebSocketEvent } from '../../src/core/websocket';
import { NhplugSocketClient } from '../../src/nhplug/socket-client';

const defaultOptions = { token: 'test_access_token' };

const urlOf = (client: NhplugSocketClient): string => (client as unknown as { url: string }).url;

const buildMsg = (client: NhplugSocketClient, trCd: string, trKey: string, trType: '1' | '2') =>
  JSON.parse(
    (
      client as unknown as { buildSubscriptionMessage: (a: string, b: string, c: string) => string }
    ).buildSubscriptionMessage.call(client, trCd, trKey, trType),
  );

interface MutableClient {
  ws: { sent: string[]; send: (message: string) => void; close: () => void } | null;
  _connected: boolean;
  handleMessage(raw: string): void;
}

const attachSocket = (client: NhplugSocketClient): NonNullable<MutableClient['ws']> => {
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

describe('NhplugSocketClient', () => {
  describe('initialization', () => {
    it('extends BaseWebSocketClient and starts disconnected', () => {
      const client = new NhplugSocketClient(defaultOptions);
      expect(client).toBeInstanceOf(BaseWebSocketClient);
      expect(client.connected).toBe(false);
      expect(client.subscriptions.size).toBe(0);
    });

    it('defaults to dev + kr', () => {
      const client = new NhplugSocketClient(defaultOptions);
      expect(client.env).toBe('dev');
      expect(client.market).toBe('kr');
    });
  });

  describe('URL selection across env x market', () => {
    it('uses the domestic prod URL for prod + kr', () => {
      const client = new NhplugSocketClient({ ...defaultOptions, env: 'prod', market: 'kr' });
      expect(urlOf(client)).toBe('wss://api.nhplug.com:7070');
    });

    it('uses the overseas prod URL for prod + gb', () => {
      const client = new NhplugSocketClient({ ...defaultOptions, env: 'prod', market: 'gb' });
      expect(urlOf(client)).toBe('wss://api.nhplug.com:7080');
    });

    it('uses the single moapi URL for dev regardless of market', () => {
      expect(urlOf(new NhplugSocketClient({ ...defaultOptions, env: 'dev', market: 'kr' }))).toBe(
        'wss://moapi.nhplug.com:17070',
      );
      expect(urlOf(new NhplugSocketClient({ ...defaultOptions, env: 'dev', market: 'gb' }))).toBe(
        'wss://moapi.nhplug.com:17070',
      );
    });
  });

  describe('buildSubscriptionMessage', () => {
    it('carries the access token in header.token with tr_type 1 for subscribe', () => {
      const client = new NhplugSocketClient(defaultOptions);
      const parsed = buildMsg(client, 'mc', '005930', '1');

      expect(parsed).toEqual({
        header: { token: 'test_access_token', tr_type: '1' },
        body: { tr_cd: 'mc', tr_key: '005930' },
      });
      // KIS 와 달리 approval key 는 존재하지 않는다.
      expect(parsed.header.approval_key).toBeUndefined();
    });

    it('uses tr_type 2 for unsubscribe', () => {
      const client = new NhplugSocketClient(defaultOptions);
      const parsed = buildMsg(client, 'RC', 'AAPL', '2');

      expect(parsed).toEqual({
        header: { token: 'test_access_token', tr_type: '2' },
        body: { tr_cd: 'RC', tr_key: 'AAPL' },
      });
    });

    it('sends the built messages through subscribe/unsubscribe', async () => {
      const client = new NhplugSocketClient(defaultOptions);
      const socket = attachSocket(client);

      await client.subscribe('mc', '005930');
      expect(client.subscriptions.get('mc:005930')).toBe('005930');
      await client.unsubscribe('mc', '005930');
      expect(client.subscriptions.size).toBe(0);

      expect(socket.sent.map((raw) => JSON.parse(raw))).toEqual([
        { header: { token: 'test_access_token', tr_type: '1' }, body: { tr_cd: 'mc', tr_key: '005930' } },
        { header: { token: 'test_access_token', tr_type: '2' }, body: { tr_cd: 'mc', tr_key: '005930' } },
      ]);
    });
  });

  describe('parseMessage', () => {
    const client = new NhplugSocketClient(defaultOptions);

    it('parses a JSON push into tr_cd / tr_key / body', () => {
      const raw = JSON.stringify({
        header: { tr_cd: 'mc', tr_key: '005930' },
        body: { stck_prpr: '70000', cntg_vol: '10' },
      });
      const msg = client.parseMessage(raw);

      expect(msg.messageType).toBe('DATA');
      expect(msg.trId).toBe('mc');
      expect(msg.trKey).toBe('005930');
      expect(msg.body).toEqual({ stck_prpr: '70000', cntg_vol: '10' });
      expect(msg.encrypted).toBe(false);
      expect(msg.raw).toBe(raw);
    });

    it('treats a push without tr_cd as SYSTEM', () => {
      const raw = JSON.stringify({ header: { rsp_cd: '00000' }, body: {} });
      expect(client.parseMessage(raw).messageType).toBe('SYSTEM');
    });

    it('treats non-JSON and non-object payloads as SYSTEM', () => {
      expect(client.parseMessage('not json at all').messageType).toBe('SYSTEM');
      expect(client.parseMessage('[1,2,3]').messageType).toBe('SYSTEM');
      expect(client.parseMessage('"plain"').messageType).toBe('SYSTEM');
    });

    it('drops a non-object body', () => {
      const raw = JSON.stringify({ header: { tr_cd: 'mc', tr_key: '005930' }, body: 'oops' });
      const msg = client.parseMessage(raw);
      expect(msg.messageType).toBe('DATA');
      expect(msg.body).toBeUndefined();
    });
  });

  describe('handleMessage', () => {
    it('emits a data event carrying tr_cd / tr_key / body', () => {
      const client = new NhplugSocketClient(defaultOptions);
      const events: WebSocketEvent[] = [];
      client.on('data', (event) => events.push(event));

      const raw = JSON.stringify({
        header: { tr_cd: 'RC', tr_key: 'AAPL' },
        body: { last: '190.11' },
      });
      (client as unknown as MutableClient).handleMessage(raw);

      expect(events).toEqual([{ eventType: 'data', trId: 'RC', trKey: 'AAPL', body: { last: '190.11' }, raw }]);
    });

    it('emits a system event for messages without tr_cd', () => {
      const client = new NhplugSocketClient(defaultOptions);
      const events: WebSocketEvent[] = [];
      client.on('system', (event) => events.push(event));
      client.on('data', () => {
        throw new Error('should not emit data');
      });

      const raw = JSON.stringify({ header: { rsp_cd: '00000', rsp_msg: 'OK' } });
      (client as unknown as MutableClient).handleMessage(raw);

      expect(events).toEqual([{ eventType: 'system', raw }]);
    });
  });
});
