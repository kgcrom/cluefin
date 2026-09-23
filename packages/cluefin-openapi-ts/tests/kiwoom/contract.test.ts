import { expect, test } from 'vitest';

import { domesticAccountEndpoints } from '../../src/kiwoom/metadata/domestic-account';
import { domesticChartEndpoints } from '../../src/kiwoom/metadata/domestic-chart';
import { domesticEtfEndpoints } from '../../src/kiwoom/metadata/domestic-etf';
import { domesticForeignEndpoints } from '../../src/kiwoom/metadata/domestic-foreign';
import { domesticMarketConditionEndpoints } from '../../src/kiwoom/metadata/domestic-market-condition';
import { domesticOrderEndpoints } from '../../src/kiwoom/metadata/domestic-order';
import { domesticRankInfoEndpoints } from '../../src/kiwoom/metadata/domestic-rank-info';
import { domesticSectorEndpoints } from '../../src/kiwoom/metadata/domestic-sector';
import { domesticStockInfoEndpoints } from '../../src/kiwoom/metadata/domestic-stock-info';
import { domesticThemeEndpoints } from '../../src/kiwoom/metadata/domestic-theme';

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

test('Kiwoom metadata should expose expected endpoint count', () => {
  expect(domesticChartEndpoints.length).toBe(14);
  expect(domesticStockInfoEndpoints.length).toBe(28);
  expect(domesticRankInfoEndpoints.length).toBe(23);
  expect(domesticAccountEndpoints.length).toBe(25);
  expect(domesticEtfEndpoints.length).toBe(9);
  expect(domesticForeignEndpoints.length).toBe(3);
  expect(domesticMarketConditionEndpoints.length).toBe(20);
  expect(domesticOrderEndpoints.length).toBe(4);
  expect(domesticSectorEndpoints.length).toBe(6);
  expect(domesticThemeEndpoints.length).toBe(2);
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
    rateLimitRequestsPerSecond: 1_000,
    rateLimitBurst: 1_000,
    fetchImpl: fetchMock,
  });

  const domains = [
    {
      instance: client.domesticChart as unknown as Record<string, (input: Record<string, unknown>) => Promise<unknown>>,
      defs: domesticChartEndpoints,
    },
    {
      instance: client.domesticStockInfo as unknown as Record<
        string,
        (input: Record<string, unknown>) => Promise<unknown>
      >,
      defs: domesticStockInfoEndpoints,
    },
    {
      instance: client.domesticRankInfo as unknown as Record<
        string,
        (input: Record<string, unknown>) => Promise<unknown>
      >,
      defs: domesticRankInfoEndpoints,
    },
    {
      instance: client.domesticAccount as unknown as Record<
        string,
        (input: Record<string, unknown>) => Promise<unknown>
      >,
      defs: domesticAccountEndpoints,
    },
    {
      instance: client.domesticEtf as unknown as Record<string, (input: Record<string, unknown>) => Promise<unknown>>,
      defs: domesticEtfEndpoints,
    },
    {
      instance: client.domesticForeign as unknown as Record<
        string,
        (input: Record<string, unknown>) => Promise<unknown>
      >,
      defs: domesticForeignEndpoints,
    },
    {
      instance: client.domesticMarketCondition as unknown as Record<
        string,
        (input: Record<string, unknown>) => Promise<unknown>
      >,
      defs: domesticMarketConditionEndpoints,
    },
    {
      instance: client.domesticOrder as unknown as Record<string, (input: Record<string, unknown>) => Promise<unknown>>,
      defs: domesticOrderEndpoints,
    },
    {
      instance: client.domesticSector as unknown as Record<
        string,
        (input: Record<string, unknown>) => Promise<unknown>
      >,
      defs: domesticSectorEndpoints,
    },
    {
      instance: client.domesticTheme as unknown as Record<string, (input: Record<string, unknown>) => Promise<unknown>>,
      defs: domesticThemeEndpoints,
    },
  ];

  for (const domain of domains) {
    for (const endpoint of domain.defs) {
      const method = domain.instance[endpoint.methodName];
      expect(typeof method).toBe('function');

      const input = buildInput(endpoint.params);
      const response = (await method?.(input)) as { body: Record<string, unknown> };
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
