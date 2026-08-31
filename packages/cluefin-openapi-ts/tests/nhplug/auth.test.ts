import { describe, expect, it } from 'vitest';

import { NhplugApiError, NhplugAuthenticationError, NhplugValidationError } from '../../src/core/errors';
import { NhplugAuth } from '../../src/nhplug/auth';
import { MemoryTokenCacheStore, type TokenCacheEntry } from '../../src/nhplug/token-cache';

interface FetchCall {
  url: string;
  init: RequestInit;
}

const createFetchMock = (responses: Response[]): { calls: FetchCall[]; fetchMock: typeof fetch } => {
  const calls: FetchCall[] = [];
  const fetchMock: typeof fetch = async (input, init) => {
    calls.push({ url: String(input), init: init ?? {} });
    const next = responses.shift();
    if (!next) {
      throw new Error('Unexpected extra fetch call');
    }
    return next;
  };
  return { calls, fetchMock };
};

const jsonResponse = (body: unknown, status = 200): Response =>
  new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json' } });

const tokenBody = {
  access_token: 'token-value',
  scope: 'oob',
  token_type: 'Bearer',
  expires_in: 86400,
};

describe('NhplugAuth.generate', () => {
  it('issues a form-encoded token request against the prod domain only', async () => {
    const { calls, fetchMock } = createFetchMock([jsonResponse(tokenBody)]);
    const auth = new NhplugAuth({ appKey: 'app-key', secretKey: 'secret-key', fetchImpl: fetchMock });

    await expect(auth.generate()).resolves.toEqual({
      accessToken: 'token-value',
      scope: 'oob',
      tokenType: 'Bearer',
      expiresIn: 86_400,
    });

    expect(calls[0]?.url).toBe('https://api.nhplug.com:8443/oauth2/token');
    expect(calls[0]?.init.method).toBe('POST');
    expect(calls[0]?.init.headers).toEqual({ 'Content-Type': 'application/x-www-form-urlencoded' });
    expect(Object.fromEntries(new URLSearchParams(String(calls[0]?.init.body)))).toEqual({
      appkey: 'app-key',
      appsecretkey: 'secret-key',
      grant_type: 'client_credentials',
      scope: 'oob',
    });
  });

  it('reuses a valid cached token instead of re-issuing', async () => {
    const store = new MemoryTokenCacheStore();
    await store.set({
      accessToken: 'cached-token',
      scope: 'oob',
      tokenType: 'Bearer',
      expiresIn: 86_400,
      cachedAt: new Date().toISOString(),
    });
    const { calls, fetchMock } = createFetchMock([]);
    const auth = new NhplugAuth({
      appKey: 'app-key',
      secretKey: 'secret-key',
      tokenCacheStore: store,
      fetchImpl: fetchMock,
    });

    await expect(auth.generate()).resolves.toMatchObject({ accessToken: 'cached-token' });
    expect(calls).toHaveLength(0);
  });

  it('re-issues when the cached token is inside the 1h expiry buffer', async () => {
    const store = new MemoryTokenCacheStore();
    const expiring: TokenCacheEntry = {
      accessToken: 'cached-token',
      scope: 'oob',
      tokenType: 'Bearer',
      expiresIn: 86_400,
      // 발급 후 23시간 30분 경과 → 남은 유효시간이 버퍼(1h) 미만
      cachedAt: new Date(Date.now() - (86_400 - 1_800) * 1000).toISOString(),
    };
    await store.set(expiring);
    const { calls, fetchMock } = createFetchMock([jsonResponse(tokenBody)]);
    const auth = new NhplugAuth({
      appKey: 'app-key',
      secretKey: 'secret-key',
      tokenCacheStore: store,
      fetchImpl: fetchMock,
    });

    await expect(auth.generate()).resolves.toMatchObject({ accessToken: 'token-value' });
    expect(calls).toHaveLength(1);
    expect((await store.get())?.accessToken).toBe('token-value');
  });

  it('maps token error statuses onto the Nhplug error family', async () => {
    const build = (status: number): NhplugAuth =>
      new NhplugAuth({
        appKey: 'a',
        secretKey: 's',
        fetchImpl: createFetchMock([jsonResponse({}, status)]).fetchMock,
      });

    await expect(build(400).generate()).rejects.toBeInstanceOf(NhplugValidationError);
    await expect(build(401).generate()).rejects.toBeInstanceOf(NhplugAuthenticationError);
  });
});

describe('NhplugAuth.revoke', () => {
  it('revokes the cached token and clears the cache', async () => {
    const store = new MemoryTokenCacheStore();
    const { calls, fetchMock } = createFetchMock([jsonResponse(tokenBody), jsonResponse({ code: 200, message: 'OK' })]);
    const auth = new NhplugAuth({
      appKey: 'app-key',
      secretKey: 'secret-key',
      tokenCacheStore: store,
      fetchImpl: fetchMock,
    });

    await auth.generate();
    await expect(auth.revoke()).resolves.toEqual({
      code: 200,
      message: 'OK',
      errorCode: undefined,
      errorDescription: undefined,
    });

    expect(calls[1]?.url).toBe('https://api.nhplug.com:8443/oauth2/revoke');
    expect(Object.fromEntries(new URLSearchParams(String(calls[1]?.init.body)))).toEqual({
      token: 'token-value',
      token_type_hint: 'access_token',
      appkey: 'app-key',
      appsecretkey: 'secret-key',
    });
    expect(await store.get()).toBeNull();
  });

  it('throws when there is no token to revoke', async () => {
    const auth = new NhplugAuth({ appKey: 'a', secretKey: 's', fetchImpl: createFetchMock([]).fetchMock });

    await expect(auth.revoke()).rejects.toBeInstanceOf(NhplugApiError);
  });
});
