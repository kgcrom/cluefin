import { describe, expect, test } from 'vitest';

import { NhplugClient } from '../../src/nhplug/client';
import { commonEndpoints } from '../../src/nhplug/metadata/common';
import { krstockInquiryEndpoints } from '../../src/nhplug/metadata/krstock-inquiry';
import { krstockOrderEndpoints } from '../../src/nhplug/metadata/krstock-order';
import { krstockQuoteEndpoints } from '../../src/nhplug/metadata/krstock-quote';
import { overseasStockInquiryEndpoints } from '../../src/nhplug/metadata/overseas-stock-inquiry';
import { overseasStockOrderEndpoints } from '../../src/nhplug/metadata/overseas-stock-order';
import { overseasStockQuoteEndpoints } from '../../src/nhplug/metadata/overseas-stock-quote';

const createClient = (): NhplugClient =>
  new NhplugClient({
    token: 'test-token',
    appKey: 'test-app-key',
    secretKey: 'test-secret-key',
    fetchImpl: (async () => {
      throw new Error('네트워크 호출이 발생하면 안 된다');
    }) as unknown as typeof fetch,
  });

const domains = [
  ['common', commonEndpoints],
  ['krstockOrder', krstockOrderEndpoints],
  ['krstockInquiry', krstockInquiryEndpoints],
  ['krstockQuote', krstockQuoteEndpoints],
  ['overseasStockOrder', overseasStockOrderEndpoints],
  ['overseasStockInquiry', overseasStockInquiryEndpoints],
  ['overseasStockQuote', overseasStockQuoteEndpoints],
] as const;

describe('NhplugClient 도메인 getter', () => {
  test.each(domains)('%s 는 메타데이터의 모든 메서드를 노출한다', (prop, endpoints) => {
    const domain = createClient()[prop] as unknown as Record<string, unknown>;
    for (const endpoint of endpoints) {
      expect(typeof domain[endpoint.methodName]).toBe('function');
    }
  });

  test.each(domains)('%s 는 같은 인스턴스를 재사용한다', (prop) => {
    const client = createClient();
    expect(client[prop]).toBe(client[prop]);
  });

  test('7개 도메인 51종을 모두 노출한다', () => {
    const total = domains.reduce((sum, [, endpoints]) => sum + endpoints.length, 0);
    expect(total).toBe(51);
  });
});
