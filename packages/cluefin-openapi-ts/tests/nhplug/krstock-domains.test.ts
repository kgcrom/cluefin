import { describe, expect, it } from 'vitest';

import type { ApiResponse, NhplugEndpointDefinition } from '../../src/core/types';
import type { NhplugClient } from '../../src/nhplug/client';
import { NhplugCommon } from '../../src/nhplug/common';
import { NhplugKrstockInquiry } from '../../src/nhplug/krstock-inquiry';
import { NhplugKrstockOrder } from '../../src/nhplug/krstock-order';
import { NhplugKrstockQuote } from '../../src/nhplug/krstock-quote';
import { commonEndpoints } from '../../src/nhplug/metadata/common';
import { krstockInquiryEndpoints } from '../../src/nhplug/metadata/krstock-inquiry';
import { krstockOrderEndpoints } from '../../src/nhplug/metadata/krstock-order';
import { krstockQuoteEndpoints } from '../../src/nhplug/metadata/krstock-quote';

const response: ApiResponse = { headers: {}, body: { rspCd: '00000' } };

const createClientStub = (): { client: NhplugClient; calls: NhplugEndpointDefinition[] } => {
  const calls: NhplugEndpointDefinition[] = [];
  const client = {
    invokeEndpoint: async (endpoint: NhplugEndpointDefinition) => {
      calls.push(endpoint);
      return response;
    },
  } as unknown as NhplugClient;
  return { client, calls };
};

const cases = [
  { name: 'NhplugCommon', build: (c: NhplugClient) => new NhplugCommon(c), endpoints: commonEndpoints, count: 2 },
  {
    name: 'NhplugKrstockOrder',
    build: (c: NhplugClient) => new NhplugKrstockOrder(c),
    endpoints: krstockOrderEndpoints,
    count: 8,
  },
  {
    name: 'NhplugKrstockInquiry',
    build: (c: NhplugClient) => new NhplugKrstockInquiry(c),
    endpoints: krstockInquiryEndpoints,
    count: 12,
  },
  {
    name: 'NhplugKrstockQuote',
    build: (c: NhplugClient) => new NhplugKrstockQuote(c),
    endpoints: krstockQuoteEndpoints,
    count: 11,
  },
] as const;

describe.each(cases)('$name', ({ build, endpoints, count }) => {
  it('exposes exactly the endpoints declared in its metadata', () => {
    expect(endpoints).toHaveLength(count);

    const { client } = createClientStub();
    const domain = build(client) as unknown as Record<string, unknown>;

    for (const endpoint of endpoints) {
      expect(domain[endpoint.methodName]).toBeTypeOf('function');
    }
  });

  it('delegates every method to the client with its own endpoint definition', async () => {
    const { client, calls } = createClientStub();
    const domain = build(client) as unknown as Record<string, (input: Record<string, unknown>) => Promise<ApiResponse>>;

    for (const endpoint of endpoints) {
      await expect(domain[endpoint.methodName]?.({})).resolves.toBe(response);
    }

    expect(calls.map((call) => call.methodName)).toEqual(endpoints.map((endpoint) => endpoint.methodName));
  });
});

describe('krstock quote typing', () => {
  it('keeps the generated method names available on the typed surface', async () => {
    const { client } = createClientStub();
    const quote = new NhplugKrstockQuote(client);

    const result = await quote.currentPrice({ marketCd: 'J', iemCd: '005930' });

    expect(result.body).toEqual({ rspCd: '00000' });
  });
});
