import { expect, test } from 'vitest';

import { domesticBasicQuoteEndpoints } from '../../src/kis/metadata/domestic-basic-quote';
import { domesticStockInfoEndpoints } from '../../src/kis/metadata/domestic-stock-info';
import { onmarketBondBasicQuoteEndpoints } from '../../src/kis/metadata/onmarket-bond-basic-quote';
import { overseasAccountEndpoints } from '../../src/kis/metadata/overseas-account';
import { overseasBasicQuoteEndpoints } from '../../src/kis/metadata/overseas-basic-quote';
import { overseasMarketAnalysisEndpoints } from '../../src/kis/metadata/overseas-market-analysis';

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

test('KIS metadata should expose expected endpoint count', () => {
  expect(domesticBasicQuoteEndpoints.length).toBe(21);
  expect(domesticStockInfoEndpoints.length).toBe(26);
  expect(overseasAccountEndpoints.length).toBe(18);
  expect(overseasBasicQuoteEndpoints.length).toBe(13);
  expect(overseasMarketAnalysisEndpoints.length).toBe(15);
  expect(onmarketBondBasicQuoteEndpoints.length).toBe(8);
});

test('KIS endpoint metadata should map request path, headers, and query/body', async () => {
  if (!(await hasZodDependency())) {
    return;
  }

  const { KisHttpClient } = await import('../../src/kis/http-client');
  const requests: Array<{ url: URL; init: RequestInit }> = [];
  const fetchMock: typeof fetch = async (input, init) => {
    const url = new URL(String(input));
    requests.push({ url, init: init ?? {} });

    return new Response(
      JSON.stringify({
        rt_cd: '0',
        msg_cd: '0',
        msg1: 'ok',
        output_item: { sample_value: '1' },
      }),
      {
        status: 200,
        headers: {
          'content-type': 'application/json',
          'tr-id': 'mock',
        },
      },
    );
  };

  const client = new KisHttpClient({
    token: 'token',
    appKey: 'app-key',
    secretKey: 'secret-key',
    env: 'dev',
    rateLimitRequestsPerSecond: 1_000,
    rateLimitBurst: 1_000,
    fetchImpl: fetchMock,
  });

  const domains = [
    {
      instance: client.domesticBasicQuote as unknown as Record<
        string,
        (input: Record<string, unknown>) => Promise<unknown>
      >,
      defs: domesticBasicQuoteEndpoints,
    },
    {
      instance: client.domesticStockInfo as unknown as Record<
        string,
        (input: Record<string, unknown>) => Promise<unknown>
      >,
      defs: domesticStockInfoEndpoints,
    },
    {
      instance: client.overseasAccount as unknown as Record<
        string,
        (input: Record<string, unknown>) => Promise<unknown>
      >,
      defs: overseasAccountEndpoints,
    },
    {
      instance: client.overseasBasicQuote as unknown as Record<
        string,
        (input: Record<string, unknown>) => Promise<unknown>
      >,
      defs: overseasBasicQuoteEndpoints,
    },
    {
      instance: client.overseasMarketAnalysis as unknown as Record<
        string,
        (input: Record<string, unknown>) => Promise<unknown>
      >,
      defs: overseasMarketAnalysisEndpoints,
    },
    {
      instance: client.onmarketBondBasicQuote as unknown as Record<
        string,
        (input: Record<string, unknown>) => Promise<unknown>
      >,
      defs: onmarketBondBasicQuoteEndpoints,
    },
  ];

  for (const domain of domains) {
    for (const endpoint of domain.defs) {
      const method = domain.instance[endpoint.methodName];
      expect(typeof method).toBe('function');

      const input = buildInput(endpoint.params);
      const response = (await method!(input)) as { body: Record<string, unknown> };
      expect(response.body.rtCd).toBe('0');

      const latest = requests.at(-1);
      expect(latest).toBeDefined();
      if (!latest) {
        continue;
      }

      expect(latest.url.pathname).toBe(endpoint.path);
      expect((latest.init.headers as Record<string, string>).tr_id).toBe(endpoint.trId);

      for (const [apiKey, inputName] of Object.entries(endpoint.requestMap)) {
        const expected = String(input[inputName]);
        if (endpoint.method === 'GET') {
          expect(latest.url.searchParams.get(apiKey)).toBe(expected);
        } else {
          const body = JSON.parse(String(latest.init.body));
          expect(body[apiKey]).toBe(expected);
        }
      }
    }
  }
});
