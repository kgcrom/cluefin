import { describe, expect, it } from 'vitest';

import {
  KiwoomApiError,
  KiwoomAuthenticationError,
  KiwoomServerError,
  KiwoomValidationError,
} from '../../src/core/errors';
import { KiwoomAuth } from '../../src/kiwoom/auth';

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
});
