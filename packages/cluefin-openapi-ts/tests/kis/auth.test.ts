import { describe, expect, it } from 'vitest';

import {
  KisApiError,
  KisAuthenticationError,
  KisNetworkError,
  KisServerError,
  KisValidationError,
} from '../../src/core/errors';
import { KisAuth } from '../../src/kis/auth';
import type { TokenCacheEntry, TokenCacheStore } from '../../src/kis/token-cache';

interface FetchCall {
  input: string;
  init: RequestInit;
}

class TestTokenCacheStore implements TokenCacheStore {
  public entry: TokenCacheEntry | null;
  public setEntries: TokenCacheEntry[] = [];
  public clearCount = 0;

  public constructor(entry: TokenCacheEntry | null = null) {
    this.entry = entry;
  }

  public async get(): Promise<TokenCacheEntry | null> {
    return this.entry;
  }

  public async set(entry: TokenCacheEntry): Promise<void> {
    this.entry = entry;
    this.setEntries.push(entry);
  }

  public async clear(): Promise<void> {
    this.entry = null;
    this.clearCount += 1;
  }
}

const futureIso = (offsetMs = 2 * 60 * 60 * 1000): string => new Date(Date.now() + offsetMs).toISOString();
const pastIso = (): string => new Date(Date.now() - 60 * 1000).toISOString();

const cachedToken = (expiresAt = futureIso()): TokenCacheEntry => ({
  accessToken: 'cached-access-token',
  tokenType: 'Bearer',
  expiresIn: 86_400,
  accessTokenTokenExpired: expiresAt,
  cachedAt: '2026-05-05T00:00:00Z',
});

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
    headers: { 'content-type': 'application/json' },
  });

const createTokenResponse = (): Response =>
  jsonResponse({
    access_token: 'new-access-token',
    token_type: 'Bearer',
    expires_in: '86400',
    access_token_token_expired: futureIso(),
  });

describe('KisAuth', () => {
  it('returns a valid cached token without calling fetch', async () => {
    const cache = new TestTokenCacheStore(cachedToken());
    const { calls, fetchMock } = createFetchMock(createTokenResponse());
    const auth = new KisAuth({
      appKey: 'app-key',
      secretKey: 'secret-key',
      tokenCacheStore: cache,
      fetchImpl: fetchMock,
    });

    await expect(auth.generate()).resolves.toEqual({
      accessToken: 'cached-access-token',
      tokenType: 'Bearer',
      expiresIn: 86_400,
      accessTokenTokenExpired: cache.entry?.accessTokenTokenExpired,
    });
    expect(calls).toHaveLength(0);
  });

  it('generates and caches a token when cache is expired or invalid', async () => {
    for (const cached of [cachedToken(pastIso()), cachedToken('not-a-date')]) {
      const cache = new TestTokenCacheStore(cached);
      const { calls, fetchMock } = createFetchMock(createTokenResponse());
      const auth = new KisAuth({
        appKey: 'app-key',
        secretKey: 'secret-key',
        tokenCacheStore: cache,
        fetchImpl: fetchMock,
      });

      await expect(auth.generate()).resolves.toMatchObject({
        accessToken: 'new-access-token',
        tokenType: 'Bearer',
        expiresIn: 86_400,
      });
      expect(calls[0]?.input).toBe('https://openapivts.koreainvestment.com:29443/oauth2/tokenP');
      expect(calls[0]?.init.method).toBe('POST');
      expect(calls[0]?.init.headers).toEqual({ 'Content-Type': 'application/json;charset=UTF-8' });
      expect(JSON.parse(String(calls[0]?.init.body))).toEqual({
        grant_type: 'client_credentials',
        appkey: 'app-key',
        appsecret: 'secret-key',
      });
      expect(cache.setEntries).toHaveLength(1);
    }
  });

  it('uses production auth endpoints when env is prod', async () => {
    const cache = new TestTokenCacheStore();
    const { calls, fetchMock } = createFetchMock(createTokenResponse());
    const auth = new KisAuth({
      appKey: 'app-key',
      secretKey: 'secret-key',
      env: 'prod',
      tokenCacheStore: cache,
      fetchImpl: fetchMock,
    });

    await auth.generate();

    expect(calls[0]?.input).toBe('https://openapi.koreainvestment.com:9443/oauth2/tokenP');
  });

  it('maps token generation failures to KIS errors', async () => {
    const cases: Array<[number, typeof KisApiError]> = [
      [400, KisValidationError],
      [401, KisAuthenticationError],
      [500, KisServerError],
      [418, KisApiError],
    ];

    for (const [status, errorClass] of cases) {
      const { fetchMock } = createFetchMock(jsonResponse({ message: 'error' }, status));
      const auth = new KisAuth({
        appKey: 'app-key',
        secretKey: 'secret-key',
        tokenCacheStore: new TestTokenCacheStore(),
        fetchImpl: fetchMock,
      });

      await expect(auth.generate()).rejects.toBeInstanceOf(errorClass);
    }
  });

  it('wraps token JSON parse failures as network errors', async () => {
    const { fetchMock } = createFetchMock(new Response('not-json', { status: 200 }));
    const auth = new KisAuth({
      appKey: 'app-key',
      secretKey: 'secret-key',
      tokenCacheStore: new TestTokenCacheStore(),
      fetchImpl: fetchMock,
    });

    await expect(auth.generate()).rejects.toBeInstanceOf(KisNetworkError);
  });

  it('revokes explicit and cached tokens, then clears the cache', async () => {
    for (const token of ['explicit-token', undefined]) {
      const cache = new TestTokenCacheStore(cachedToken());
      const { calls, fetchMock } = createFetchMock(jsonResponse({ ok: true }));
      const auth = new KisAuth({
        appKey: 'app-key',
        secretKey: 'secret-key',
        tokenCacheStore: cache,
        fetchImpl: fetchMock,
      });

      await expect(auth.revoke(token)).resolves.toBe(true);

      expect(calls[0]?.input).toBe('https://openapivts.koreainvestment.com:29443/oauth2/revokeP');
      expect(JSON.parse(String(calls[0]?.init.body))).toMatchObject({
        appkey: 'app-key',
        appsecret: 'secret-key',
        token: token ?? 'cached-access-token',
      });
      expect(cache.clearCount).toBe(1);
    }
  });

  it('rejects revoke before a token exists and maps revoke failures', async () => {
    const emptyCache = new TestTokenCacheStore();
    const okFetch = createFetchMock(jsonResponse({ ok: true })).fetchMock;
    const authWithoutToken = new KisAuth({
      appKey: 'app-key',
      secretKey: 'secret-key',
      tokenCacheStore: emptyCache,
      fetchImpl: okFetch,
    });

    await expect(authWithoutToken.revoke()).rejects.toBeInstanceOf(KisApiError);

    const failingFetch = createFetchMock(jsonResponse({ message: 'error' }, 403)).fetchMock;
    const authWithFailure = new KisAuth({
      appKey: 'app-key',
      secretKey: 'secret-key',
      tokenCacheStore: new TestTokenCacheStore(cachedToken()),
      fetchImpl: failingFetch,
    });

    await expect(authWithFailure.revoke()).rejects.toBeInstanceOf(KisApiError);
  });

  it('requests approval keys and maps approval failures', async () => {
    const { calls, fetchMock } = createFetchMock(jsonResponse({ approval_key: 'approval-key' }));
    const auth = new KisAuth({ appKey: 'app-key', secretKey: 'secret-key', fetchImpl: fetchMock });

    await expect(auth.approve()).resolves.toEqual({ approvalKey: 'approval-key' });
    expect(calls[0]?.input).toBe('https://openapivts.koreainvestment.com:29443/oauth2/Approval');
    expect(JSON.parse(String(calls[0]?.init.body))).toEqual({
      grant_type: 'client_credentials',
      appkey: 'app-key',
      secretkey: 'secret-key',
    });

    const failingAuth = new KisAuth({
      appKey: 'app-key',
      secretKey: 'secret-key',
      fetchImpl: createFetchMock(jsonResponse({ message: 'error' }, 403)).fetchMock,
    });
    await expect(failingAuth.approve()).rejects.toBeInstanceOf(KisApiError);
  });
});
