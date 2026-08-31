import { describe, expect, it } from 'vitest';

import { camelizeKeys } from '../../src/core/case-convert';
import type { ApiResponse, NhplugEndpointDefinition } from '../../src/core/types';
import type { NhplugClient } from '../../src/nhplug/client';
import { overseasStockInquiryEndpoints } from '../../src/nhplug/metadata/overseas-stock-inquiry';
import { overseasStockOrderEndpoints } from '../../src/nhplug/metadata/overseas-stock-order';
import { overseasStockQuoteEndpoints } from '../../src/nhplug/metadata/overseas-stock-quote';
import { NhplugOverseasStockInquiry } from '../../src/nhplug/overseas-stock-inquiry';
import { NhplugOverseasStockOrder } from '../../src/nhplug/overseas-stock-order';
import { NhplugOverseasStockQuote } from '../../src/nhplug/overseas-stock-quote';
import type { OverseasStockQuoteCurrentPriceResponse } from '../../src/nhplug/schemas/overseas-stock-quote';

const response: ApiResponse = { headers: {}, body: { ok: true } };

const createClient = (
  calls: Array<{ endpoint: NhplugEndpointDefinition; input: Record<string, unknown> }>,
): NhplugClient =>
  ({
    invokeEndpoint: async (endpoint: NhplugEndpointDefinition, input: Record<string, unknown>) => {
      calls.push({ endpoint, input });
      return response;
    },
  }) as unknown as NhplugClient;

describe('NH PLUG 해외주식(gbstock) domain wrappers', () => {
  it('exposes one method per generated endpoint', () => {
    const calls: Array<{ endpoint: NhplugEndpointDefinition; input: Record<string, unknown> }> = [];
    const client = createClient(calls);

    const domains = [
      { instance: new NhplugOverseasStockOrder(client), endpoints: overseasStockOrderEndpoints },
      { instance: new NhplugOverseasStockInquiry(client), endpoints: overseasStockInquiryEndpoints },
      { instance: new NhplugOverseasStockQuote(client), endpoints: overseasStockQuoteEndpoints },
    ];

    for (const { instance, endpoints } of domains) {
      const methods = instance as unknown as Record<string, unknown>;
      for (const endpoint of endpoints) {
        expect(methods[endpoint.methodName]).toBeTypeOf('function');
      }
    }

    expect(overseasStockOrderEndpoints).toHaveLength(6);
    expect(overseasStockInquiryEndpoints).toHaveLength(8);
    expect(overseasStockQuoteEndpoints).toHaveLength(4);
  });

  it('delegates each call to the client with its own endpoint definition', async () => {
    const calls: Array<{ endpoint: NhplugEndpointDefinition; input: Record<string, unknown> }> = [];
    const client = createClient(calls);

    const quote = new NhplugOverseasStockQuote(client);
    await expect(quote.current({ iemCd: 'AAPL' })).resolves.toBe(response);

    const order = new NhplugOverseasStockOrder(client);
    await expect(order.buy({ actNo: '00000000000' })).resolves.toBe(response);

    const inquiry = new NhplugOverseasStockInquiry(client);
    await expect(inquiry.balance({ actNo: '00000000000' })).resolves.toBe(response);

    expect(calls.map((call) => call.endpoint.path)).toEqual([
      '/gbstock/quote/v1/current',
      '/gbstock/order/v1/buy',
      '/gbstock/inquiry/v1/balance',
    ]);
    expect(calls[0]?.input).toEqual({ iemCd: 'AAPL' });
  });

  it('typed response map lines up with the camelized wire body', async () => {
    const wire = { rsp_cd: '00000', Output_0: { iem_cd: 'AAPL', trdprc: 1 } };
    const client = {
      invokeEndpoint: async (): Promise<ApiResponse> => ({ headers: {}, body: camelizeKeys(wire) }),
    } as unknown as NhplugClient;

    const quote = new NhplugOverseasStockQuote(client);
    const result = await quote.current({ iemCd: 'AAPL' });
    const body: OverseasStockQuoteCurrentPriceResponse = result.body;

    // `Output_0` 은 런타임 camelize 후 `output0` 이 된다 — 타입과 런타임이 같은 키를 가리켜야 한다.
    expect(body.output0?.iemCd).toBe('AAPL');
    expect(body.rspCd).toBe('00000');
  });
});
