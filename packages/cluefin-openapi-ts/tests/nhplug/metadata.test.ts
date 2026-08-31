import { describe, expect, it } from 'vitest';

import type { NhplugEndpointDefinition } from '../../src/core/types';
import { commonEndpoints } from '../../src/nhplug/metadata/common';
import { krstockInquiryEndpoints } from '../../src/nhplug/metadata/krstock-inquiry';
import { krstockOrderEndpoints } from '../../src/nhplug/metadata/krstock-order';
import { krstockQuoteEndpoints } from '../../src/nhplug/metadata/krstock-quote';
import { overseasStockInquiryEndpoints } from '../../src/nhplug/metadata/overseas-stock-inquiry';
import { overseasStockOrderEndpoints } from '../../src/nhplug/metadata/overseas-stock-order';
import { overseasStockQuoteEndpoints } from '../../src/nhplug/metadata/overseas-stock-quote';

// 파이썬 sibling(`cluefin_openapi/nhplug/_*.py`) 에서 생성되는 메타데이터라,
// 개수가 바뀌면 파이썬 쪽 엔드포인트가 늘거나 파서가 깨진 것이다.
const categories: Array<[string, readonly NhplugEndpointDefinition[], number]> = [
  ['common', commonEndpoints, 2],
  ['krstockOrder', krstockOrderEndpoints, 8],
  ['krstockInquiry', krstockInquiryEndpoints, 12],
  ['krstockQuote', krstockQuoteEndpoints, 11],
  ['overseasStockOrder', overseasStockOrderEndpoints, 6],
  ['overseasStockInquiry', overseasStockInquiryEndpoints, 8],
  ['overseasStockQuote', overseasStockQuoteEndpoints, 4],
];

const allEndpoints = categories.flatMap(([, endpoints]) => endpoints);

describe('nhplug metadata', () => {
  it.each(categories)('%s has %i endpoints', (_name, endpoints, expected) => {
    expect(endpoints).toHaveLength(expected);
  });

  it('has 51 endpoints in total', () => {
    expect(allEndpoints).toHaveLength(51);
  });

  it('gives every endpoint a non-empty path', () => {
    for (const endpoint of allEndpoints) {
      expect(endpoint.path, endpoint.methodName).toMatch(/^\//);
    }
  });

  it('gives every cts-capable endpoint a cts param', () => {
    const ctsEndpoints = allEndpoints.filter((endpoint) => endpoint.supportsCts);
    expect(ctsEndpoints.length).toBeGreaterThan(0);
    for (const endpoint of ctsEndpoints) {
      const ctsParam = endpoint.params.find((param) => param.name === 'cts');
      expect(ctsParam, endpoint.methodName).toBeDefined();
      expect(ctsParam?.required, endpoint.methodName).toBe(false);
    }
  });

  it('never maps cts into the request body', () => {
    for (const endpoint of allEndpoints) {
      // cts 는 헤더로만 나가므로 bodyMap 에 있으면 안 된다.
      expect(Object.values(endpoint.bodyMap), endpoint.methodName).not.toContain('cts');
    }
  });

  it('has unique method names within each category', () => {
    for (const [name, endpoints] of categories) {
      const methodNames = endpoints.map((endpoint) => endpoint.methodName);
      expect(new Set(methodNames).size, name).toBe(methodNames.length);
    }
  });
});
