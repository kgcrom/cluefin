import { expect, test } from 'vitest';

import { commonEndpoints } from '../../src/nhplug/metadata/common';
import { krstockInquiryEndpoints } from '../../src/nhplug/metadata/krstock-inquiry';
import { krstockOrderEndpoints } from '../../src/nhplug/metadata/krstock-order';
import { krstockQuoteEndpoints } from '../../src/nhplug/metadata/krstock-quote';
import { overseasStockInquiryEndpoints } from '../../src/nhplug/metadata/overseas-stock-inquiry';
import { overseasStockOrderEndpoints } from '../../src/nhplug/metadata/overseas-stock-order';
import { overseasStockQuoteEndpoints } from '../../src/nhplug/metadata/overseas-stock-quote';

const sampleValue = (name: string, fallback?: unknown): string => {
  if (fallback !== undefined) {
    return String(fallback);
  }
  return `v_${name}`;
};

const buildInput = (
  params: { name: string; required: boolean; defaultValue?: string | number | boolean | undefined }[],
) => Object.fromEntries(params.map((param) => [param.name, sampleValue(param.name, param.defaultValue)]));

const hasZodDependency = async (): Promise<boolean> => {
  try {
    await import('zod');
    return true;
  } catch {
    return false;
  }
};

test('NH PLUG metadata should expose expected endpoint count', () => {
  expect(commonEndpoints.length).toBe(2);
  expect(krstockInquiryEndpoints.length).toBe(12);
  expect(krstockOrderEndpoints.length).toBe(8);
  expect(krstockQuoteEndpoints.length).toBe(11);
  expect(overseasStockInquiryEndpoints.length).toBe(8);
  expect(overseasStockOrderEndpoints.length).toBe(6);
  expect(overseasStockQuoteEndpoints.length).toBe(4);
});

test('NH PLUG endpoint metadata should map request path, headers, and Input_0 body', async () => {
  if (!(await hasZodDependency())) {
    return;
  }

  const { NhplugClient } = await import('../../src/nhplug/client');
  const requests: Array<{ url: URL; init: RequestInit }> = [];
  const fetchMock: typeof fetch = async (input, init) => {
    const url = new URL(String(input));
    requests.push({ url, init: init ?? {} });

    return new Response(JSON.stringify({ rsp_cd: '00000', rsp_msg: 'ok', Output_0: { sample_value: '1' } }), {
      status: 200,
      headers: {
        'content-type': 'application/json',
      },
    });
  };

  const client = new NhplugClient({
    token: 'token',
    appKey: 'app-key',
    secretKey: 'secret-key',
    env: 'dev',
    fetchImpl: fetchMock,
  });

  const domains = [
    {
      instance: client.common as unknown as Record<string, (input: Record<string, unknown>) => Promise<unknown>>,
      defs: commonEndpoints,
    },
    {
      instance: client.krstockInquiry as unknown as Record<
        string,
        (input: Record<string, unknown>) => Promise<unknown>
      >,
      defs: krstockInquiryEndpoints,
    },
    {
      instance: client.krstockOrder as unknown as Record<string, (input: Record<string, unknown>) => Promise<unknown>>,
      defs: krstockOrderEndpoints,
    },
    {
      instance: client.krstockQuote as unknown as Record<string, (input: Record<string, unknown>) => Promise<unknown>>,
      defs: krstockQuoteEndpoints,
    },
    {
      instance: client.overseasStockInquiry as unknown as Record<
        string,
        (input: Record<string, unknown>) => Promise<unknown>
      >,
      defs: overseasStockInquiryEndpoints,
    },
    {
      instance: client.overseasStockOrder as unknown as Record<
        string,
        (input: Record<string, unknown>) => Promise<unknown>
      >,
      defs: overseasStockOrderEndpoints,
    },
    {
      instance: client.overseasStockQuote as unknown as Record<
        string,
        (input: Record<string, unknown>) => Promise<unknown>
      >,
      defs: overseasStockQuoteEndpoints,
    },
  ];

  for (const domain of domains) {
    for (const endpoint of domain.defs) {
      const method = domain.instance[endpoint.methodName];
      expect(typeof method).toBe('function');

      const input = buildInput(endpoint.params);
      const response = (await method?.(input)) as { body: Record<string, unknown> };
      expect(response.body.rspCd).toBe('00000');

      const latest = requests.at(-1);
      expect(latest).toBeDefined();
      if (!latest) {
        continue;
      }

      expect(latest.url.pathname).toBe(endpoint.path);
      expect(latest.init.method).toBe('POST');

      const headers = latest.init.headers as Record<string, string>;
      expect(headers.authorization).toBe('Bearer token');
      expect(headers['x-client-id']).toBe('app-key');
      expect(headers['x-client-secret']).toBe('secret-key');

      const parsedBody = JSON.parse(String(latest.init.body)) as { Input_0: Record<string, unknown> };
      for (const [apiKey, inputName] of Object.entries(endpoint.bodyMap)) {
        expect(parsedBody.Input_0[apiKey]).toBe(String(input[inputName]));
      }
    }
  }
});
