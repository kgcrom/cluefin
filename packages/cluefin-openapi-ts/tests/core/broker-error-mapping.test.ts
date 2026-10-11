import { randomUUID } from 'node:crypto';
import { afterEach, describe, expect, test, vi } from 'vitest';

import {
  ApiError,
  KisApiError,
  KisAuthenticationError,
  KisAuthorizationError,
  KisNetworkError,
  KisRateLimitError,
  KisServerError,
  KisTimeoutError,
  KisValidationError,
  KiwoomApiError,
  KiwoomAuthenticationError,
  KiwoomAuthorizationError,
  KiwoomNetworkError,
  KiwoomRateLimitError,
  KiwoomServerError,
  KiwoomTimeoutError,
  KiwoomValidationError,
  NhplugApiError,
  NhplugAuthenticationError,
  NhplugAuthorizationError,
  NhplugNetworkError,
  NhplugRateLimitError,
  NhplugServerError,
  NhplugTimeoutError,
  NhplugValidationError,
} from '../../src/core/errors';
import { silentLogger } from '../../src/core/logger';
import { KisHttpClient } from '../../src/kis/http-client';
import { KiwoomClient } from '../../src/kiwoom/client';
import { NhplugClient } from '../../src/nhplug/client';

/**
 * 증권사 클라이언트가 BaseHttpClient 의 공통 에러(ApiXError)를 자기 타입(KisXError 등)으로
 * 바꿔 던지는지 본다. 공개 API 의 에러 계약이라, 갈래 하나가 엉뚱한 타입으로 바뀌면
 * `instanceof KisRateLimitError` 로 재시도하던 호출자가 조용히 깨진다.
 *
 * 조회 엔드포인트만 쓴다 — 주문 등 mutation 은 테스트를 만들지 않는다.
 * 응답 본문에는 키움 return_code / NH rsp_cd 를 넣지 않는다(그 승격 경로는 각 브로커 테스트가 본다).
 */

type ErrorClass = abstract new (...args: never[]) => ApiError;
type Invoke = (fetchImpl: typeof fetch, timeoutMs: number) => Promise<unknown>;

interface Scenario {
  name: string;
  fetchImpl: typeof fetch;
  statusCode: number | undefined;
  message: string;
  retryAfter?: number;
}

interface Broker {
  name: string;
  invoke: Invoke;
  /** 시나리오 이름 → 기대 클래스. 순서는 `scenarios` 와 같다. */
  expected: ReadonlyArray<readonly [string, ErrorClass]>;
  /** 입력 검증(zod) 등 ApiError 가 아닌 에러가 떨어지는 최종 갈래. */
  fallback: ErrorClass;
  invokeWithInvalidInput: (fetchImpl: typeof fetch) => Promise<unknown>;
}

const credential = (): string => `test-${randomUUID()}`;
const ERROR_BODY = { error: 'mocked failure' };
const TIMEOUT_MS = 50;

const respondWith =
  (status: number, headers: Record<string, string> = {}): typeof fetch =>
  async () =>
    new Response(JSON.stringify(ERROR_BODY), {
      status,
      headers: { 'content-type': 'application/json', ...headers },
    });

// 실제 타임아웃 경로: 응답을 주지 않다가 BaseHttpClient 가 abort 하면 AbortError 로 끝난다.
const hangUntilAborted: typeof fetch = (_input, init) =>
  new Promise((_resolve, reject) => {
    init?.signal?.addEventListener('abort', () => {
      reject(new DOMException('The operation was aborted.', 'AbortError'));
    });
  });

const failConnection: typeof fetch = async () => {
  throw new TypeError('fetch failed');
};

const scenarios: Scenario[] = [
  { name: 'HTTP 400', fetchImpl: respondWith(400), statusCode: 400, message: 'Bad request' },
  { name: 'HTTP 401', fetchImpl: respondWith(401), statusCode: 401, message: 'Authentication failed' },
  { name: 'HTTP 403', fetchImpl: respondWith(403), statusCode: 403, message: 'Authorization failed' },
  {
    name: 'HTTP 429',
    fetchImpl: respondWith(429, { 'retry-after': '7' }),
    statusCode: 429,
    message: 'Rate limit exceeded',
    retryAfter: 7,
  },
  { name: 'HTTP 503', fetchImpl: respondWith(503), statusCode: 503, message: 'Server error' },
  { name: 'HTTP 404', fetchImpl: respondWith(404), statusCode: 404, message: 'Unexpected status code 404' },
  { name: 'timeout', fetchImpl: hangUntilAborted, statusCode: undefined, message: 'Request timeout' },
  { name: 'network failure', fetchImpl: failConnection, statusCode: undefined, message: 'fetch failed' },
];

const httpErrorScenarioNames = new Set(['HTTP 400', 'HTTP 401', 'HTTP 403', 'HTTP 429', 'HTTP 503', 'HTTP 404']);

const brokers: Broker[] = [
  {
    name: 'KIS',
    invoke: (fetchImpl, timeoutMs) =>
      new KisHttpClient({
        token: credential(),
        appKey: credential(),
        secretKey: credential(),
        env: 'dev',
        maxRetries: 0,
        timeoutMs,
        fetchImpl,
      }).domesticBasicQuote.getStockCurrentPrice({ fidCondMrktDivCode: 'J', fidInputIscd: '005930' }),
    expected: [
      ['HTTP 400', KisValidationError],
      ['HTTP 401', KisAuthenticationError],
      ['HTTP 403', KisAuthorizationError],
      ['HTTP 429', KisRateLimitError],
      ['HTTP 503', KisServerError],
      ['HTTP 404', KisApiError],
      ['timeout', KisTimeoutError],
      ['network failure', KisNetworkError],
    ],
    fallback: KisApiError,
    invokeWithInvalidInput: (fetchImpl) =>
      new KisHttpClient({
        token: credential(),
        appKey: credential(),
        secretKey: credential(),
        env: 'dev',
        maxRetries: 0,
        fetchImpl,
      }).domesticBasicQuote.getStockCurrentPrice({ fidCondMrktDivCode: 'J' }),
  },
  {
    name: 'Kiwoom',
    invoke: (fetchImpl, timeoutMs) =>
      new KiwoomClient({
        token: credential(),
        env: 'dev',
        maxRetries: 0,
        timeoutMs,
        fetchImpl,
        logger: silentLogger,
      }).domesticStockInfo.getStockInfo({ stkCd: '005930' }),
    expected: [
      ['HTTP 400', KiwoomValidationError],
      ['HTTP 401', KiwoomAuthenticationError],
      ['HTTP 403', KiwoomAuthorizationError],
      ['HTTP 429', KiwoomRateLimitError],
      ['HTTP 503', KiwoomServerError],
      ['HTTP 404', KiwoomApiError],
      ['timeout', KiwoomTimeoutError],
      ['network failure', KiwoomNetworkError],
    ],
    fallback: KiwoomApiError,
    invokeWithInvalidInput: (fetchImpl) =>
      new KiwoomClient({
        token: credential(),
        env: 'dev',
        maxRetries: 0,
        fetchImpl,
        logger: silentLogger,
      }).domesticStockInfo.getStockInfo({}),
  },
  {
    name: 'NH PLUG',
    invoke: (fetchImpl, timeoutMs) =>
      new NhplugClient({
        token: credential(),
        appKey: credential(),
        secretKey: credential(),
        env: 'dev',
        maxRetries: 0,
        timeoutMs,
        fetchImpl,
        logger: silentLogger,
      }).krstockQuote.currentPrice({ marketCd: 'KRX', iemCd: '005930' }),
    expected: [
      ['HTTP 400', NhplugValidationError],
      ['HTTP 401', NhplugAuthenticationError],
      ['HTTP 403', NhplugAuthorizationError],
      ['HTTP 429', NhplugRateLimitError],
      ['HTTP 503', NhplugServerError],
      ['HTTP 404', NhplugApiError],
      ['timeout', NhplugTimeoutError],
      ['network failure', NhplugNetworkError],
    ],
    fallback: NhplugApiError,
    invokeWithInvalidInput: (fetchImpl) =>
      new NhplugClient({
        token: credential(),
        appKey: credential(),
        secretKey: credential(),
        env: 'dev',
        maxRetries: 0,
        fetchImpl,
        logger: silentLogger,
      }).krstockQuote.currentPrice({ marketCd: 'KRX' }),
  },
];

const captureRejection = async (promise: Promise<unknown>): Promise<ApiError> => {
  try {
    await promise;
  } catch (error) {
    if (error instanceof ApiError) {
      return error;
    }
    throw error;
  }
  throw new Error('expected the call to reject');
};

// `name` 은 생성자 이름이라, 부모(ApiXError)나 형제 클래스로 바뀐 매핑도 잡는다.
const expectExactClass = (error: ApiError, expected: ErrorClass): void => {
  expect(error).toBeInstanceOf(expected);
  expect(error.name).toBe(expected.name);
};

const cases = brokers.flatMap((broker) =>
  broker.expected.map(([scenarioName, expectedClass]) => {
    const scenario = scenarios.find((candidate) => candidate.name === scenarioName);
    if (!scenario) {
      throw new Error(`unknown scenario: ${scenarioName}`);
    }
    return { broker: broker.name, invoke: broker.invoke, scenario, expectedClass };
  }),
);

afterEach(() => {
  vi.restoreAllMocks();
});

describe('broker clients map transport errors to their own error types', () => {
  test('every broker covers every scenario', () => {
    for (const broker of brokers) {
      expect(broker.expected.map(([name]) => name)).toEqual(scenarios.map((scenario) => scenario.name));
    }
  });

  test.each(cases)('$broker — $scenario.name → $expectedClass.name', async ({ invoke, scenario, expectedClass }) => {
    // KIS 는 ApiError 를 console.error 로 남긴다 — 출력만 막는다.
    vi.spyOn(console, 'error').mockImplementation(() => undefined);

    const error = await captureRejection(invoke(scenario.fetchImpl, TIMEOUT_MS));

    expectExactClass(error, expectedClass);
    expect(error.message).toBe(scenario.message);
    expect(error.statusCode).toBe(scenario.statusCode);
    if (httpErrorScenarioNames.has(scenario.name)) {
      expect(error.responseData).toEqual(ERROR_BODY);
    }
    if (scenario.retryAfter !== undefined) {
      expect(error).toMatchObject({ retryAfter: scenario.retryAfter });
    }
  });

  test.each(brokers)('$name — invalid input never reaches fetch and becomes $fallback.name', async (broker) => {
    vi.spyOn(console, 'error').mockImplementation(() => undefined);
    const fetchImpl = vi.fn<typeof fetch>();

    const error = await captureRejection(broker.invokeWithInvalidInput(fetchImpl));

    expectExactClass(error, broker.fallback);
    expect(error.statusCode).toBeUndefined();
    expect(fetchImpl).not.toHaveBeenCalled();
  });
});
