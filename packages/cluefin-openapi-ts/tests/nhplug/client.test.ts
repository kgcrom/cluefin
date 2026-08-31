import { describe, expect, it } from 'vitest';

import { NhplugApiError, NhplugAuthenticationError } from '../../src/core/errors';
import { silentLogger } from '../../src/core/logger';
import type { NhplugEndpointDefinition } from '../../src/core/types';
import { NhplugClient } from '../../src/nhplug/client';

interface FetchCall {
  url: string;
  init: RequestInit;
}

const createFetchMock = (responder: (call: FetchCall) => Response): { calls: FetchCall[]; fetchMock: typeof fetch } => {
  const calls: FetchCall[] = [];
  const fetchMock: typeof fetch = async (input, init) => {
    const call = { url: String(input), init: init ?? {} };
    calls.push(call);
    return responder(call);
  };
  return { calls, fetchMock };
};

const jsonResponse = (body: unknown, status = 200, headers: Record<string, string> = {}): Response =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json', ...headers },
  });

const endpoint: NhplugEndpointDefinition = {
  methodName: 'getAccountList',
  path: '/n2/acctinfo',
  bodyMap: { actNo: 'actNo', ordDt: 'ordDt' },
  supportsCts: true,
  params: [
    { name: 'actNo', required: true },
    { name: 'ordDt', required: false },
    { name: 'cts', required: false },
  ],
};

const createClient = (fetchMock: typeof fetch): NhplugClient =>
  new NhplugClient({
    token: 'token-value',
    appKey: 'app-key',
    secretKey: 'secret-key',
    fetchImpl: fetchMock,
    logger: silentLogger,
  });

const readBody = (call: FetchCall | undefined): Record<string, unknown> =>
  JSON.parse(String(call?.init.body)) as Record<string, unknown>;

const readHeaders = (call: FetchCall | undefined): Record<string, string> =>
  (call?.init.headers ?? {}) as Record<string, string>;

describe('NhplugClient.invokeEndpoint', () => {
  it('wraps the request body in Input_0 and drops null/undefined params', async () => {
    const { calls, fetchMock } = createFetchMock(() => jsonResponse({ rsp_cd: '00000', rsp_msg: '정상' }));
    const client = createClient(fetchMock);

    await client.invokeEndpoint(endpoint, { actNo: '12345678901', ordDt: undefined });

    expect(calls).toHaveLength(1);
    expect(calls[0]?.url).toBe('https://moapi.nhplug.com:8443/n2/acctinfo');
    expect(calls[0]?.init.method).toBe('POST');
    expect(readBody(calls[0])).toEqual({ Input_0: { actNo: '12345678901' } });
  });

  it('sends the NH auth headers', async () => {
    const { calls, fetchMock } = createFetchMock(() => jsonResponse({ rsp_cd: '00000' }));

    await createClient(fetchMock).invokeEndpoint(endpoint, { actNo: '1' });

    const headers = readHeaders(calls[0]);
    expect(headers.authorization).toBe('Bearer token-value');
    expect(headers['x-client-id']).toBe('app-key');
    expect(headers['x-client-secret']).toBe('secret-key');
  });

  it('uses the prod base url when env is prod', async () => {
    const { calls, fetchMock } = createFetchMock(() => jsonResponse({ rsp_cd: '00000' }));
    const client = new NhplugClient({
      token: 't',
      appKey: 'a',
      secretKey: 's',
      env: 'prod',
      fetchImpl: fetchMock,
      logger: silentLogger,
    });

    await client.invokeEndpoint(endpoint, { actNo: '1' });

    expect(calls[0]?.url).toBe('https://api.nhplug.com:8443/n2/acctinfo');
  });

  it('round-trips cts: request headers go out, response cts/cts_flag come back', async () => {
    const { calls, fetchMock } = createFetchMock(() =>
      jsonResponse({ rsp_cd: '00000' }, 200, { cts: 'next-page-key', cts_flag: 'Y' }),
    );

    const result = await createClient(fetchMock).invokeEndpoint(endpoint, { actNo: '1', cts: 'page-2' });

    const headers = readHeaders(calls[0]);
    expect(headers.cts).toBe('page-2');
    expect(headers.cts_flag).toBe('Y');
    // cts 는 봉투 바디가 아니라 헤더로만 전달된다.
    expect(readBody(calls[0])).toEqual({ Input_0: { actNo: '1' } });

    expect(result.headers.cts).toBe('next-page-key');
    expect(result.headers.ctsFlag).toBe('Y');
  });

  it('omits cts headers when no cts input is supplied', async () => {
    const { calls, fetchMock } = createFetchMock(() => jsonResponse({ rsp_cd: '00000' }));

    await createClient(fetchMock).invokeEndpoint(endpoint, { actNo: '1' });

    const headers = readHeaders(calls[0]);
    expect(headers.cts).toBeUndefined();
    expect(headers.cts_flag).toBeUndefined();
  });

  it('omits cts headers when the endpoint does not support pagination', async () => {
    const { calls, fetchMock } = createFetchMock(() => jsonResponse({ rsp_cd: '00000' }));
    const noCtsEndpoint: NhplugEndpointDefinition = { ...endpoint, supportsCts: false };

    await createClient(fetchMock).invokeEndpoint(noCtsEndpoint, { actNo: '1', cts: 'page-2' });

    expect(readHeaders(calls[0]).cts).toBeUndefined();
  });

  it('raises NhplugApiError when an HTTP 200 carries a failing rsp_cd', async () => {
    const { fetchMock } = createFetchMock(() => jsonResponse({ rsp_cd: '40010', rsp_msg: '계좌번호 오류' }));

    await expect(createClient(fetchMock).invokeEndpoint(endpoint, { actNo: '1' })).rejects.toBeInstanceOf(
      NhplugApiError,
    );
    await expect(createClient(fetchMock).invokeEndpoint(endpoint, { actNo: '1' })).rejects.toThrow(
      'API error 40010: 계좌번호 오류',
    );
  });

  it('treats XA102 as success (모의투자 조회 완료 응답)', async () => {
    const { fetchMock } = createFetchMock(() =>
      jsonResponse({ rsp_cd: 'XA102', rsp_msg: '모의투자 조회가 완료되었습니다', Output_0: [{ act_no: '1' }] }),
    );

    const result = await createClient(fetchMock).invokeEndpoint(endpoint, { actNo: '1' });

    expect(result.body).toEqual({
      rspCd: 'XA102',
      rspMsg: '모의투자 조회가 완료되었습니다',
      output0: [{ actNo: '1' }],
    });
  });

  it('maps transport errors onto the Nhplug error family', async () => {
    const { fetchMock } = createFetchMock(() => jsonResponse({ rsp_cd: '99999' }, 401));

    await expect(createClient(fetchMock).invokeEndpoint(endpoint, { actNo: '1' })).rejects.toBeInstanceOf(
      NhplugAuthenticationError,
    );
  });
});
