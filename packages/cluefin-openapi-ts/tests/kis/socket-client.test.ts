import { describe, expect, it } from 'vitest';
import { KisApiError } from '../../src/core/errors';
import type { WebSocketEvent } from '../../src/core/websocket';
import { KisSocketClient, parseKisRejection } from '../../src/kis/socket-client';

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

  describe('server rejection', () => {
    const deliver = (client: KisSocketClient, raw: string): void => {
      (client as unknown as { handleMessage: (raw: string) => void }).handleMessage(raw);
    };
    const invalidApproval = JSON.stringify({
      header: { tr_id: 'H0BJCNT0', tr_key: 'KR103502GA34', encrypt: 'N' },
      body: { rt_cd: '1', msg_cd: 'OPSP0011', msg1: `invalid approval : ${defaultOptions.approvalKey}` },
    });

    it('emits an error event with the approval key masked', () => {
      const client = new KisSocketClient(defaultOptions);
      const events: WebSocketEvent[] = [];
      client.on('error', (event: WebSocketEvent) => events.push(event));

      deliver(client, invalidApproval);

      expect(events).toHaveLength(1);
      const event = events.at(0);
      expect(event?.trId).toBe('H0BJCNT0');
      expect(event?.error).toBeInstanceOf(KisApiError);
      expect(event?.error?.message).toContain('[OPSP0011] invalid approval : ***');
      expect(JSON.stringify(event?.error)).not.toContain(defaultOptions.approvalKey);
      expect(event?.error?.message).not.toContain(defaultOptions.approvalKey);
    });

    it('reports a rejection without tr_id', () => {
      const parsed = parseKisRejection(
        '{"header":{"tr_id":"(null)","tr_key":"","encrypt":"N"},"body":{"rt_cd":"9","msg_cd":"OPSP8996","msg1":"ALREADY IN USE appkey"}}',
        defaultOptions.approvalKey,
      );

      expect(parsed?.error.message).toContain('[OPSP8996] ALREADY IN USE appkey');
      expect(parsed?.error.errorCode).toBe('OPSP8996');
    });

    it.each([
      '{"header":{"tr_id":"H0BJCNT0"},"body":{"rt_cd":"0","msg_cd":"OPSP0000","msg1":"SUBSCRIBE SUCCESS"}}',
      '{"header":{"tr_id":"PINGPONG","datetime":"20261012094000"}}',
      '[1, 2]',
      'some unknown message format',
    ])('ignores a non-rejection message: %s', (raw) => {
      expect(parseKisRejection(raw, defaultOptions.approvalKey)).toBeUndefined();
    });

    it('does not throw when nobody listens for errors', () => {
      const client = new KisSocketClient(defaultOptions);

      expect(() => deliver(client, invalidApproval)).not.toThrow();
    });

    it('names the rejection in the next not-connected error', async () => {
      const client = new KisSocketClient(defaultOptions);
      deliver(client, invalidApproval);

      await expect(client.subscribe('H0BJASP0', 'KR103502GA34')).rejects.toThrow(/not connected .*OPSP0011/);
    });

    it('keeps the plain not-connected error without a rejection', async () => {
      const client = new KisSocketClient(defaultOptions);

      await expect(client.subscribe('H0BJASP0', 'KR103502GA34')).rejects.toThrow(/^WebSocket not connected$/);
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
