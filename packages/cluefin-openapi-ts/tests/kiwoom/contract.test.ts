import { expect, test } from 'bun:test';

import { domesticChartEndpoints } from '../../src/kiwoom/metadata/domestic-chart';
import { domesticRankInfoEndpoints } from '../../src/kiwoom/metadata/domestic-rank-info';
import { domesticStockInfoEndpoints } from '../../src/kiwoom/metadata/domestic-stock-info';

const sampleValue = (name: string, fallback?: unknown): string => {
  if (fallback !== undefined) {
    return String(fallback);
  }
  return `v_${name}`;
};

const buildInput = (params: { name: string; required: boolean; defaultValue?: string | number | boolean }[]) =>
  Object.fromEntries(params.map((param) => [param.name, sampleValue(param.name, param.defaultValue)]));

const hasZodDependency = async (): Promise<boolean> => {
  try {
    await import('zod');
    return true;
  } catch {
    return false;
  }
};

test('Kiwoom metadata should expose expected endpoint count', () => {
  expect(domesticChartEndpoints.length).toBe(14);
  expect(domesticStockInfoEndpoints.length).toBe(28);
  expect(domesticRankInfoEndpoints.length).toBe(23);
});

test('Kiwoom endpoint metadata should map request path, headers, and body', async () => {
  if (!(await hasZodDependency())) {
    return;
  }

  const { KiwoomClient } = await import('../../src/kiwoom/client');
  const requests: Array<{ url: URL; init: RequestInit }> = [];
  const fetchMock: typeof fetch = async (input, init) => {
    const url = new URL(String(input));
    requests.push({ url, init: init ?? {} });

    return new Response(
      JSON.stringify({
        return_code: 0,
        return_msg: 'ok',
        sample_value: '1',
      }),
      {
        status: 200,
        headers: {
          'content-type': 'application/json',
          'api-id': 'mock',
        },
      },
    );
  };

  const client = new KiwoomClient({
    token: 'token',
    env: 'dev',
    fetchImpl: fetchMock,
  });

  const domains = [
    {
      instance: client.domesticChart as Record<string, (input: Record<string, unknown>) => Promise<unknown>>,
      defs: domesticChartEndpoints,
    },
    {
      instance: client.domesticStockInfo as Record<string, (input: Record<string, unknown>) => Promise<unknown>>,
      defs: domesticStockInfoEndpoints,
    },
    {
      instance: client.domesticRankInfo as Record<string, (input: Record<string, unknown>) => Promise<unknown>>,
      defs: domesticRankInfoEndpoints,
    },
  ];

  for (const domain of domains) {
    for (const endpoint of domain.defs) {
      const method = domain.instance[endpoint.methodName];
      expect(typeof method).toBe('function');

      const input = buildInput(endpoint.params);
      const response = (await method(input)) as { body: Record<string, unknown> };
      expect(response.body.returnCode).toBe(0);

      const latest = requests.at(-1);
      expect(latest).toBeDefined();
      if (!latest) {
        continue;
      }

      expect(latest.url.pathname).toBe(endpoint.path);

      const headers = latest.init.headers as Record<string, string>;
      expect(headers['api-id']).toBe(endpoint.apiId);
      const body = JSON.parse(String(latest.init.body));

      for (const [apiKey, inputName] of Object.entries(endpoint.bodyMap)) {
        expect(body[apiKey]).toBe(String(input[inputName]));
      }
      for (const [headerName, inputName] of Object.entries(endpoint.headerParamMap)) {
        expect(headers[headerName]).toBe(String(input[inputName]));
      }
    }
  }
});
