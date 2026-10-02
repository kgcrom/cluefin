import { randomUUID } from 'node:crypto';

import { describe, expect, it } from 'vitest';

import {
  DartApiError,
  DartAuthenticationError,
  DartNetworkError,
  DartRateLimitError,
  DartServerError,
  DartValidationError,
} from '../../src/core/errors';
import { silentLogger } from '../../src/core/logger';
import type { DartEndpointDefinition } from '../../src/core/types';
import { DartClient } from '../../src/dart/client';
import { DartDomainBase } from '../../src/dart/domain-base';
import { buildZip } from '../_helpers/zip-builder';

interface FetchCall {
  url: string;
  init: RequestInit;
}

const createFetchMock = (responder: (call: FetchCall, index: number) => Response) => {
  const calls: FetchCall[] = [];
  const fetchMock: typeof fetch = async (input, init) => {
    const call = { url: String(input), init: init ?? {} };
    calls.push(call);
    return responder(call, calls.length - 1);
  };
  return { calls, fetchMock };
};

const jsonResponse = (body: unknown, status = 200, headers: Record<string, string> = {}): Response =>
  new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json', ...headers } });

// 누출 검사용 더미 값 — 하드코딩된 시크릿처럼 보이지 않도록 실행마다 새로 만든다.
const AUTH_KEY = `test-${randomUUID()}`;

const jsonEndpoint: DartEndpointDefinition = {
  methodName: 'companyOverview',
  path: '/api/company.json',
  queryMap: { corp_code: 'corpCode', page_no: 'pageNo' },
  responseKind: 'json',
  params: [
    { name: 'corpCode', required: true },
    { name: 'pageNo', required: false },
  ],
};

const binaryEndpoint: DartEndpointDefinition = {
  methodName: 'corpCode',
  path: '/api/corpCode.xml',
  queryMap: {},
  responseKind: 'binary',
  params: [],
};

const createClient = (fetchMock: typeof fetch, options: { maxRetries?: number } = {}): DartClient =>
  new DartClient({ authKey: AUTH_KEY, fetchImpl: fetchMock, logger: silentLogger, maxRetries: 0, ...options });

describe('DartClient.invokeEndpoint', () => {
  it('GET 쿼리에 crtfc_key 를 붙이고 입력을 와이어 키로 매핑하며 응답을 camelCase 로 바꾼다', async () => {
    const { calls, fetchMock } = createFetchMock(() =>
      jsonResponse({ status: '000', message: '정상', corp_name: '삼성전자', total_count: 1 }),
    );

    const response = await createClient(fetchMock).invokeEndpoint(jsonEndpoint, { corpCode: '00126380', pageNo: 2 });

    const url = new URL(calls[0]?.url ?? '');
    expect(calls[0]?.init.method).toBe('GET');
    expect(calls[0]?.init.body).toBeUndefined();
    expect(url.origin + url.pathname).toBe('https://opendart.fss.or.kr/api/company.json');
    expect(Object.fromEntries(url.searchParams)).toEqual({
      corp_code: '00126380',
      page_no: '2',
      crtfc_key: AUTH_KEY,
    });
    expect(response.body).toEqual({ status: '000', message: '정상', corpName: '삼성전자', totalCount: 1 });
  });

  it('선택 파라미터를 생략하면 쿼리에서 빠진다', async () => {
    const { calls, fetchMock } = createFetchMock(() => jsonResponse({ status: '000', message: '정상' }));

    await createClient(fetchMock).invokeEndpoint(jsonEndpoint, { corpCode: '00126380' });

    expect(new URL(calls[0]?.url ?? '').searchParams.has('page_no')).toBe(false);
  });

  it('body status 가 013 이어도 throw 하지 않고 그대로 돌려준다', async () => {
    const { fetchMock } = createFetchMock(() => jsonResponse({ status: '013', message: '조회된 데이타가 없습니다.' }));

    const response = await createClient(fetchMock).invokeEndpoint(jsonEndpoint, { corpCode: '1' });

    expect(response.body).toEqual({ status: '013', message: '조회된 데이타가 없습니다.' });
  });

  it('필수 파라미터가 없으면 요청 없이 실패한다', async () => {
    const { calls, fetchMock } = createFetchMock(() => jsonResponse({}));

    await expect(createClient(fetchMock).invokeEndpoint(jsonEndpoint, {})).rejects.toBeInstanceOf(DartApiError);
    expect(calls).toHaveLength(0);
  });

  it.each([
    [400, DartValidationError],
    [401, DartAuthenticationError],
    [404, DartApiError],
  ] as const)('HTTP %i 를 Dart 에러로 변환한다', async (status, ErrorType) => {
    const { fetchMock } = createFetchMock(() => jsonResponse({ status: 'x' }, status));

    await expect(createClient(fetchMock).invokeEndpoint(jsonEndpoint, { corpCode: '1' })).rejects.toBeInstanceOf(
      ErrorType,
    );
  });

  it('429·5xx 는 재시도한 뒤 에러로 변환한다', async () => {
    const rateLimited = createFetchMock(() => jsonResponse({}, 429, { 'retry-after': '3' }));
    await expect(
      createClient(rateLimited.fetchMock, { maxRetries: 1 }).invokeEndpoint(jsonEndpoint, { corpCode: '1' }),
    ).rejects.toMatchObject({ constructor: DartRateLimitError, retryAfter: 3 });
    expect(rateLimited.calls).toHaveLength(2);

    const server = createFetchMock((_, index) => (index === 0 ? jsonResponse({}, 503) : jsonResponse({}, 500)));
    await expect(
      createClient(server.fetchMock, { maxRetries: 1 }).invokeEndpoint(jsonEndpoint, { corpCode: '1' }),
    ).rejects.toBeInstanceOf(DartServerError);
    expect(server.calls).toHaveLength(2);
  });

  it('재시도 후 성공하면 결과를 돌려준다', async () => {
    const { calls, fetchMock } = createFetchMock((_, index) =>
      index === 0 ? jsonResponse({}, 503) : jsonResponse({ status: '000', message: '정상' }),
    );

    const response = await createClient(fetchMock, { maxRetries: 2 }).invokeEndpoint(jsonEndpoint, { corpCode: '1' });

    expect(calls).toHaveLength(2);
    expect(response.body.status).toBe('000');
  });

  it('인증키는 에러·로그·requestContext 어디에도 노출되지 않는다', async () => {
    const logs: unknown[] = [];
    const logger = { debug: () => undefined, warn: () => undefined, error: (...args: unknown[]) => logs.push(args) };
    const leaky: typeof fetch = async (input) => {
      throw new Error(`connect ECONNREFUSED ${String(input)}`);
    };
    const client = new DartClient({ authKey: AUTH_KEY, fetchImpl: leaky, logger, maxRetries: 0 });

    const error = await client.invokeEndpoint(jsonEndpoint, { corpCode: '1' }).catch((e: unknown) => e);

    expect(error).toBeInstanceOf(DartNetworkError);
    expect(JSON.stringify(error, Object.getOwnPropertyNames(error))).not.toContain(AUTH_KEY);
    expect(JSON.stringify(logs)).not.toContain(AUTH_KEY);
  });
});

describe('DartClient.invokeBinaryEndpoint', () => {
  it('ZIP 본문은 바이트 그대로 돌려준다', async () => {
    const zip = buildZip([{ name: 'CORPCODE.xml', data: '<result/>' }]);
    const { calls, fetchMock } = createFetchMock(() => new Response(zip, { status: 200 }));

    const response = await createClient(fetchMock).invokeBinaryEndpoint(binaryEndpoint, {});

    expect(new URL(calls[0]?.url ?? '').searchParams.get('crtfc_key')).toBe(AUTH_KEY);
    expect(response.body).toEqual(zip);
  });

  it('에러 XML 본문(status != 000)은 DartApiError 로 바꾼다', async () => {
    const xml =
      '<?xml version="1.0"?><result><status>014</status><message>파일이 존재하지 않습니다.</message></result>';
    const { fetchMock } = createFetchMock(() => new Response(xml, { status: 200 }));

    const error = await createClient(fetchMock)
      .invokeBinaryEndpoint(binaryEndpoint, {})
      .catch((e: unknown) => e);

    expect(error).toBeInstanceOf(DartApiError);
    expect(error).toMatchObject({ message: '파일이 존재하지 않습니다.', errorCode: '014' });
  });

  it('status 없는 XML(공시 원문)은 에러로 보지 않는다', async () => {
    const { fetchMock } = createFetchMock(() => new Response('<DOCUMENT><BODY>x</BODY></DOCUMENT>', { status: 200 }));

    const response = await createClient(fetchMock).invokeBinaryEndpoint(binaryEndpoint, {});

    expect(new TextDecoder().decode(response.body)).toBe('<DOCUMENT><BODY>x</BODY></DOCUMENT>');
  });
});

describe('DartDomainBase', () => {
  it('엔드포인트 메타데이터대로 JSON·바이너리 메서드를 노출한다', async () => {
    const zip = buildZip([{ name: 'a.xml', data: '<a/>' }]);
    const { calls, fetchMock } = createFetchMock((call) =>
      call.url.includes('corpCode') ? new Response(zip) : jsonResponse({ status: '000', message: '정상' }),
    );
    const domain = new DartDomainBase(createClient(fetchMock), [jsonEndpoint, binaryEndpoint]) as DartDomainBase &
      Record<string, (input?: Record<string, unknown>) => Promise<{ body: unknown }>>;

    expect(((await domain.companyOverview?.({ corpCode: '1' })) as { body: unknown }).body).toEqual({
      status: '000',
      message: '정상',
    });
    expect(((await domain.corpCode?.()) as { body: unknown }).body).toEqual(zip);
    expect(calls).toHaveLength(2);
  });
});
