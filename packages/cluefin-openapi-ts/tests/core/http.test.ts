import { describe, expect, it } from 'vitest';

import {
  ApiAuthenticationError,
  ApiAuthorizationError,
  ApiError,
  ApiNetworkError,
  ApiRateLimitError,
  ApiServerError,
  ApiTimeoutError,
  ApiValidationError,
} from '../../src/core/errors';
import { BaseHttpClient } from '../../src/core/http';
import type { FetchLike, HttpClientOptions } from '../../src/core/types';

const clientOptions: HttpClientOptions = {
  timeoutMs: 50,
  retry: { maxRetries: 0, baseDelayMs: 1 },
  rateLimit: { requestsPerSecond: 1_000, burst: 1_000 },
};

const jsonResponse = (body: unknown, status = 200, headers?: HeadersInit): Response =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json', ...headers },
  });

describe('BaseHttpClient', () => {
  it('serializes query and body values before calling fetch', async () => {
    const calls: Array<{ url: URL; init: RequestInit }> = [];
    const fetchMock: FetchLike = async (input, init) => {
      calls.push({ url: new URL(String(input)), init: init ?? {} });
      return jsonResponse({ ok: true });
    };
    const client = new BaseHttpClient(clientOptions, fetchMock);

    await client.request({
      method: 'POST',
      url: 'https://example.test/resource',
      headers: { accept: 'application/json' },
      query: { ticker: '005930', market: 'KRX' },
      body: { price: '1000' },
    });

    expect(calls[0]?.url.searchParams.get('ticker')).toBe('005930');
    expect(calls[0]?.url.searchParams.get('market')).toBe('KRX');
    expect(calls[0]?.init.method).toBe('POST');
    expect(calls[0]?.init.headers).toEqual({ accept: 'application/json' });
    expect(calls[0]?.init.body).toBe(JSON.stringify({ price: '1000' }));
  });

  it('maps HTTP status codes to API error classes', async () => {
    const cases: Array<[number, typeof ApiError, HeadersInit | undefined]> = [
      [400, ApiValidationError, undefined],
      [401, ApiAuthenticationError, undefined],
      [403, ApiAuthorizationError, undefined],
      [429, ApiRateLimitError, { 'retry-after': '7' }],
      [500, ApiServerError, undefined],
      [418, ApiError, undefined],
    ];

    for (const [status, errorClass, headers] of cases) {
      const client = new BaseHttpClient(clientOptions, async () => jsonResponse({ error: status }, status, headers));
      await expect(client.request({ method: 'GET', url: 'https://example.test', headers: {} })).rejects.toBeInstanceOf(
        errorClass,
      );
    }
  });

  it('captures retry-after on rate limit errors', async () => {
    const client = new BaseHttpClient(clientOptions, async () =>
      jsonResponse({ error: 'limited' }, 429, { 'retry-after': '9' }),
    );

    await expect(client.request({ method: 'GET', url: 'https://example.test', headers: {} })).rejects.toMatchObject({
      retryAfter: 9,
      responseData: { error: 'limited' },
    });
  });

  it('falls back to undefined response data when error response JSON cannot be parsed', async () => {
    const client = new BaseHttpClient(clientOptions, async () => new Response('not-json', { status: 400 }));

    await expect(client.request({ method: 'GET', url: 'https://example.test', headers: {} })).rejects.toMatchObject({
      responseData: undefined,
    });
  });

  it('wraps network failures and abort timeouts', async () => {
    const networkClient = new BaseHttpClient(clientOptions, async () => {
      throw new Error('fetch failed');
    });
    await expect(
      networkClient.request({ method: 'GET', url: 'https://example.test', headers: {} }),
    ).rejects.toBeInstanceOf(ApiNetworkError);

    const timeoutClient = new BaseHttpClient({ ...clientOptions, timeoutMs: 1 }, async (_input, init) => {
      await new Promise((_resolve, reject) => {
        init?.signal?.addEventListener('abort', () => reject(new DOMException('aborted', 'AbortError')));
      });
      return jsonResponse({ ok: true });
    });
    await expect(
      timeoutClient.request({ method: 'GET', url: 'https://example.test', headers: {} }),
    ).rejects.toBeInstanceOf(ApiTimeoutError);
  });
});
