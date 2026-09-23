import { describe, expect, it } from 'vitest';

import {
  KiwoomApiError,
  KiwoomAuthenticationError,
  KiwoomServerError,
  KiwoomValidationError,
} from '../../src/core/errors';
import { KiwoomAuth } from '../../src/kiwoom/auth';
import { MemoryTokenCacheStore, type TokenCacheEntry } from '../../src/kiwoom/token-cache';

interface FetchCall {
  input: string;
  init: RequestInit;
}

const createFetchMock = (response: Response): { calls: FetchCall[]; fetchMock: typeof fetch } => {
  const calls: FetchCall[] = [];
  const fetchMock: typeof fetch = async (input, init) => {
    calls.push({ input: String(input), init: init ?? {} });
    return response;
  };
  return { calls, fetchMock };
};

const jsonResponse = (body: unknown, status = 200): Response =>
  new Response(JSON.stringify(body), {
    status,
    headers: {
      'content-type': 'application/json',
    },
  });

describe('KiwoomAuth', () => {
  it('generates a token with a dev request and camelizes the response', async () => {
    const { calls, fetchMock } = createFetchMock(
      jsonResponse({
        token_type: 'Bearer',
        token: 'token-value',
        expires_dt: '20260505120000',
      }),
    );
    const auth = new KiwoomAuth({ appKey: 'app-key', secretKey: 'secret-key', fetchImpl: fetchMock });

    await expect(auth.generateToken()).resolves.toEqual({
      tokenType: 'Bearer',
      token: 'token-value',
      expiresDt: '20260505120000',
    });

    expect(calls).toHaveLength(1);
    expect(calls[0]?.input).toBe('https://mockapi.kiwoom.com/oauth2/token');
    expect(calls[0]?.init.method).toBe('POST');
    expect(calls[0]?.init.headers).toEqual({ 'Content-Type': 'application/json;charset=UTF-8' });
    expect(JSON.parse(String(calls[0]?.init.body))).toEqual({
      grant_type: 'client_credentials',
      appkey: 'app-key',
      secretkey: 'secret-key',
    });
  });

  it('uses the production token endpoint when env is prod', async () => {
    const { calls, fetchMock } = createFetchMock(
      jsonResponse({
        token_type: 'Bearer',
        token: 'token-value',
        expires_dt: '20260505120000',
      }),
    );
    const auth = new KiwoomAuth({ appKey: 'app-key', secretKey: 'secret-key', env: 'prod', fetchImpl: fetchMock });

    await auth.generateToken();

    expect(calls[0]?.input).toBe('https://api.kiwoom.com/oauth2/token');
  });

  it('maps token generation error statuses to Kiwoom errors', async () => {
    const cases: Array<[number, typeof KiwoomApiError]> = [
      [400, KiwoomValidationError],
      [401, KiwoomAuthenticationError],
      [500, KiwoomServerError],
      [418, KiwoomApiError],
    ];

    for (const [status, errorClass] of cases) {
      const { fetchMock } = createFetchMock(jsonResponse({ message: 'error' }, status));
      const auth = new KiwoomAuth({ appKey: 'app-key', secretKey: 'secret-key', fetchImpl: fetchMock });

      await expect(auth.generateToken()).rejects.toBeInstanceOf(errorClass);
    }
  });

  it('rejects an HTTP 200 response without a token and does not cache it', async () => {
    const { fetchMock } = createFetchMock(jsonResponse({ return_code: 3, return_msg: '인증에 실패했습니다' }));
    const tokenCacheStore = new MemoryTokenCacheStore();
    const auth = new KiwoomAuth({ appKey: 'app-key', secretKey: 'secret-key', tokenCacheStore, fetchImpl: fetchMock });

    await expect(auth.generateToken()).rejects.toBeInstanceOf(KiwoomAuthenticationError);
    await expect(tokenCacheStore.get()).resolves.toBeNull();
  });

  it('revokes a token with the expected request body', async () => {
    const { calls, fetchMock } = createFetchMock(jsonResponse({ ok: true }));
    const auth = new KiwoomAuth({ appKey: 'app-key', secretKey: 'secret-key', fetchImpl: fetchMock });

    await expect(auth.revokeToken('token-value')).resolves.toBe(true);

    expect(calls[0]?.input).toBe('https://mockapi.kiwoom.com/oauth2/revoke');
    expect(calls[0]?.init.method).toBe('POST');
    expect(calls[0]?.init.headers).toEqual({ 'Content-Type': 'application/json;charset=UTF-8' });
    expect(JSON.parse(String(calls[0]?.init.body))).toEqual({
      appkey: 'app-key',
      secretkey: 'secret-key',
      token: 'token-value',
    });
  });

  it('throws KiwoomApiError when token revocation fails', async () => {
    const { fetchMock } = createFetchMock(jsonResponse({ message: 'error' }, 403));
    const auth = new KiwoomAuth({ appKey: 'app-key', secretKey: 'secret-key', fetchImpl: fetchMock });

    await expect(auth.revokeToken('token-value')).rejects.toBeInstanceOf(KiwoomApiError);
  });

  it('reuses a fresh cached token instead of calling the API', async () => {
    const { calls, fetchMock } = createFetchMock(jsonResponse({ message: 'should not be called' }, 500));
    const tokenCacheStore = new MemoryTokenCacheStore();
    const farFutureExpiry = new Date(Date.now() + 12 * 60 * 60 * 1000).toISOString();
    await tokenCacheStore.set({
      token: 'cached-token',
      tokenType: 'Bearer',
      expiresDt: farFutureExpiry,
      cachedAt: new Date().toISOString(),
    });
    const auth = new KiwoomAuth({ appKey: 'app-key', secretKey: 'secret-key', tokenCacheStore, fetchImpl: fetchMock });

    await expect(auth.generateToken()).resolves.toEqual({
      token: 'cached-token',
      tokenType: 'Bearer',
      expiresDt: farFutureExpiry,
    });
    expect(calls).toHaveLength(0);
  });

  it('re-issues when the cached token is past the 1h expiry buffer', async () => {
    const { calls, fetchMock } = createFetchMock(
      jsonResponse({ token_type: 'Bearer', token: 'fresh-token', expires_dt: '20260505120000' }),
    );
    const tokenCacheStore = new MemoryTokenCacheStore();
    const soonExpiry = new Date(Date.now() + 30 * 60 * 1000).toISOString(); // within the 1h buffer
    await tokenCacheStore.set({
      token: 'cached-token',
      tokenType: 'Bearer',
      expiresDt: soonExpiry,
      cachedAt: new Date().toISOString(),
    });
    const auth = new KiwoomAuth({ appKey: 'app-key', secretKey: 'secret-key', tokenCacheStore, fetchImpl: fetchMock });

    await expect(auth.generateToken()).resolves.toEqual({
      tokenType: 'Bearer',
      token: 'fresh-token',
      expiresDt: '20260505120000',
    });
    expect(calls).toHaveLength(1);
  });

  it('re-issues when the cache is older than the 6h max age even if the token has not expired', async () => {
    const { calls, fetchMock } = createFetchMock(
      jsonResponse({ token_type: 'Bearer', token: 'fresh-token', expires_dt: '20260505120000' }),
    );
    const tokenCacheStore = new MemoryTokenCacheStore();
    const farFutureExpiry = new Date(Date.now() + 12 * 60 * 60 * 1000).toISOString();
    const staleCachedAt = new Date(Date.now() - 7 * 60 * 60 * 1000).toISOString(); // older than MAX_CACHE_AGE
    await tokenCacheStore.set({
      token: 'cached-token',
      tokenType: 'Bearer',
      expiresDt: farFutureExpiry,
      cachedAt: staleCachedAt,
    });
    const auth = new KiwoomAuth({ appKey: 'app-key', secretKey: 'secret-key', tokenCacheStore, fetchImpl: fetchMock });

    await expect(auth.generateToken()).resolves.toEqual({
      tokenType: 'Bearer',
      token: 'fresh-token',
      expiresDt: '20260505120000',
    });
    expect(calls).toHaveLength(1);
  });

  it('caches a freshly issued token converted to the Python-compatible ISO expiry format', async () => {
    const { fetchMock } = createFetchMock(
      jsonResponse({ token_type: 'Bearer', token: 'fresh-token', expires_dt: '20260505120000' }),
    );
    const tokenCacheStore = new MemoryTokenCacheStore();
    const auth = new KiwoomAuth({ appKey: 'app-key', secretKey: 'secret-key', tokenCacheStore, fetchImpl: fetchMock });

    await auth.generateToken();

    const cached = (await tokenCacheStore.get()) as TokenCacheEntry;
    expect(cached.token).toBe('fresh-token');
    expect(cached.expiresDt).toBe('2026-05-05T12:00:00');
  });
});
