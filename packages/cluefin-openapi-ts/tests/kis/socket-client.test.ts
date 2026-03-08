import { describe, expect, it } from 'vitest';
import { BaseWebSocketClient } from '../../src/core/websocket';
import { KisSocketClient } from '../../src/kis/socket-client';

describe('KisSocketClient', () => {
  const defaultOptions = {
    approvalKey: 'test_approval_key',
    appKey: 'test_app_key',
    secretKey: 'test_secret_key',
  };

  describe('initialization', () => {
    it('should use dev URL by default', () => {
      const client = new KisSocketClient(defaultOptions);
      expect(client.env).toBe('dev');
      expect((client as unknown as { url: string }).url).toBe('ws://ops.koreainvestment.com:31000/tryitout');
    });

    it('should use prod URL when env is prod', () => {
      const client = new KisSocketClient({ ...defaultOptions, env: 'prod' });
      expect(client.env).toBe('prod');
      expect((client as unknown as { url: string }).url).toBe('ws://ops.koreainvestment.com:21000/tryitout');
    });

    it('should extend BaseWebSocketClient', () => {
      const client = new KisSocketClient(defaultOptions);
      expect(client).toBeInstanceOf(BaseWebSocketClient);
    });

    it('should start disconnected with empty subscriptions', () => {
      const client = new KisSocketClient(defaultOptions);
      expect(client.connected).toBe(false);
      expect(client.subscriptions.size).toBe(0);
    });
  });

  describe('buildSubscriptionMessage', () => {
    it('should build correct subscribe message', () => {
      const client = new KisSocketClient(defaultOptions);
      const buildMsg = (
        client as unknown as { buildSubscriptionMessage: (a: string, b: string, c: string) => string }
      ).buildSubscriptionMessage.bind(client);
      const raw = buildMsg('H0STASP0', '005930', '1');
      const parsed = JSON.parse(raw);

      expect(parsed.header.approval_key).toBe('test_approval_key');
      expect(parsed.header.custtype).toBe('P');
      expect(parsed.header.tr_type).toBe('1');
      expect(parsed.header['content-type']).toBe('utf-8');
      expect(parsed.body.input.tr_id).toBe('H0STASP0');
      expect(parsed.body.input.tr_key).toBe('005930');
    });

    it('should build correct unsubscribe message', () => {
      const client = new KisSocketClient(defaultOptions);
      const buildMsg = (
        client as unknown as { buildSubscriptionMessage: (a: string, b: string, c: string) => string }
      ).buildSubscriptionMessage.bind(client);
      const raw = buildMsg('H0STASP0', '005930', '2');
      const parsed = JSON.parse(raw);

      expect(parsed.header.tr_type).toBe('2');
      expect(parsed.body.input.tr_id).toBe('H0STASP0');
      expect(parsed.body.input.tr_key).toBe('005930');
    });
  });
});

describe('BaseWebSocketClient message parsing', () => {
  const client = new KisSocketClient({
    approvalKey: 'test',
    appKey: 'test',
    secretKey: 'test',
  });

  describe('parseMessage', () => {
    it('should parse PINGPONG message', () => {
      const msg = client.parseMessage('PINGPONG');
      expect(msg.messageType).toBe('PINGPONG');
      expect(msg.raw).toBe('PINGPONG');
    });

    it('should parse unencrypted data message', () => {
      const raw = '0|H0STASP0|001|123000^124000^122000';
      const msg = client.parseMessage(raw);

      expect(msg.messageType).toBe('DATA');
      expect(msg.trId).toBe('H0STASP0');
      expect(msg.encrypted).toBe(false);
      expect(msg.data).toEqual(['123000', '124000', '122000']);
    });

    it('should parse encrypted data message', () => {
      const raw = '1|H0STCNI0|001|encrypted_data_here';
      const msg = client.parseMessage(raw);

      expect(msg.messageType).toBe('DATA');
      expect(msg.trId).toBe('H0STCNI0');
      expect(msg.encrypted).toBe(true);
      expect(msg.data).toEqual(['encrypted_data_here']);
    });

    it('should parse unknown message as SYSTEM', () => {
      const raw = 'some unknown message format';
      const msg = client.parseMessage(raw);

      expect(msg.messageType).toBe('SYSTEM');
      expect(msg.raw).toBe(raw);
    });

    it('should handle empty data field', () => {
      const raw = '0|H0STASP0|000|';
      const msg = client.parseMessage(raw);

      expect(msg.messageType).toBe('DATA');
      expect(msg.data).toEqual([]);
    });
  });
});
