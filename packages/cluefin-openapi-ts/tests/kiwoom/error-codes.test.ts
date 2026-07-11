import { describe, expect, test } from 'vitest';

import {
  KiwoomApiError,
  KiwoomAuthenticationError,
  KiwoomAuthorizationError,
  KiwoomRateLimitError,
  KiwoomServerError,
  KiwoomValidationError,
} from '../../src/core/errors';
import type { Logger } from '../../src/core/logger';
import type { KiwoomEndpointDefinition } from '../../src/core/types';
import { KiwoomClient } from '../../src/kiwoom/client';
import { KIWOOM_ERROR_CODES, parseKiwoomReturnCode, resolveKiwoomError } from '../../src/kiwoom/error-codes';

const DOCUMENTED_CODES = [
  1501, 1504, 1505, 1511, 1512, 1513, 1514, 1515, 1516, 1517, 1687, 1700, 1701, 1702, 1901, 1902, 1903, 1999, 8001,
  8002, 8003, 8005, 8006, 8009, 8010, 8011, 8012, 8015, 8016, 8020, 8030, 8031, 8040, 8050, 8103, 8104, 8200,
];

const endpoint: KiwoomEndpointDefinition = {
  methodName: 'stockInfo',
  params: [{ name: 'stockCode', required: true }],
  path: '/api/dostk/stkinfo',
  apiId: 'ka10001',
  bodyMap: { stk_cd: 'stockCode' },
  headerParamMap: {},
};

const createRecordingLogger = (): { logger: Logger; errors: Array<Record<string, unknown> | undefined> } => {
  const errors: Array<Record<string, unknown> | undefined> = [];
  return {
    errors,
    logger: {
      debug: () => undefined,
      warn: () => undefined,
      error: (_message, context) => {
        errors.push(context);
      },
    },
  };
};

const createClient = (fetchImpl: typeof fetch, logger: Logger): KiwoomClient =>
  new KiwoomClient({
    token: 'token',
    env: 'dev',
    maxRetries: 0,
    rateLimitRequestsPerSecond: 1_000,
    rateLimitBurst: 1_000,
    fetchImpl,
    logger,
  });

const jsonResponse = (body: Record<string, unknown>, status = 200): Response =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json' },
  });

describe('KIWOOM_ERROR_CODES registry', () => {
  test('covers every documented API 서버 오류코드', () => {
    expect(Object.keys(KIWOOM_ERROR_CODES).map(Number).sort()).toEqual([...DOCUMENTED_CODES].sort());
  });

  test('parseKiwoomReturnCode coerces numbers and numeric strings', () => {
    expect(parseKiwoomReturnCode(0)).toBe(0);
    expect(parseKiwoomReturnCode('1700')).toBe(1700);
    expect(parseKiwoomReturnCode(' 8005 ')).toBe(8005);
    expect(parseKiwoomReturnCode(undefined)).toBeUndefined();
    expect(parseKiwoomReturnCode('OK')).toBeUndefined();
  });

  test.each([
    [1501, KiwoomValidationError],
    [1902, KiwoomValidationError],
    [1513, KiwoomAuthenticationError],
    [8005, KiwoomAuthenticationError],
    [8104, KiwoomAuthorizationError],
    [8200, KiwoomAuthorizationError],
    [1687, KiwoomRateLimitError],
    [1700, KiwoomRateLimitError],
    [1999, KiwoomServerError],
    [4242, KiwoomApiError],
  ])('resolveKiwoomError maps %i to the expected error class', (code, expectedClass) => {
    const error = resolveKiwoomError(code);
    expect(error).toBeInstanceOf(expectedClass);
    expect(error.errorCode).toBe(code);
  });

  test('resolveKiwoomError prefers the server return_msg over the registry fallback', () => {
    const error = resolveKiwoomError(1511, '필수입력 파라미터=stk_cd');
    expect(error.message).toContain('필수입력 파라미터=stk_cd');

    const fallback = resolveKiwoomError(8005);
    expect(fallback.message).toContain(KIWOOM_ERROR_CODES[8005]);
  });
});

describe('KiwoomClient return_code handling', () => {
  test('throws a typed error and logs when HTTP 200 carries an error return_code', async () => {
    const { logger, errors } = createRecordingLogger();
    const client = createClient(
      async () => jsonResponse({ return_code: 1902, return_msg: '종목 정보가 없습니다. 종목코드=999999' }),
      logger,
    );

    const promise = client.invokeEndpoint(endpoint, { stockCode: '999999' });
    await expect(promise).rejects.toBeInstanceOf(KiwoomValidationError);
    await expect(promise).rejects.toMatchObject({ errorCode: 1902, statusCode: 200 });

    expect(errors).toHaveLength(1);
    expect(errors[0]).toMatchObject({ apiId: 'ka10001', path: '/api/dostk/stkinfo', returnCode: 1902 });
  });

  test('promotes HTTP-status errors to the return_code error type', async () => {
    const { logger, errors } = createRecordingLogger();
    const client = createClient(
      async () => jsonResponse({ return_code: 8005, return_msg: 'Token이 유효하지 않습니다' }, 401),
      logger,
    );

    const promise = client.invokeEndpoint(endpoint, { stockCode: '005930' });
    await expect(promise).rejects.toBeInstanceOf(KiwoomAuthenticationError);
    await expect(promise).rejects.toMatchObject({ errorCode: 8005, statusCode: 401 });
    expect(errors[0]).toMatchObject({ returnCode: 8005 });
  });

  test('resolves normally when return_code is 0', async () => {
    const { logger, errors } = createRecordingLogger();
    const client = createClient(
      async () => jsonResponse({ return_code: 0, return_msg: 'ok', stk_nm: '삼성전자' }),
      logger,
    );

    const response = await client.invokeEndpoint(endpoint, { stockCode: '005930' });
    expect(response.body.returnCode).toBe(0);
    expect(errors).toHaveLength(0);
  });
});
