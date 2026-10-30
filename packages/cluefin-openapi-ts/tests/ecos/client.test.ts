import { randomUUID } from 'node:crypto';

import { describe, expect, it } from 'vitest';
import { z } from 'zod';

import {
  ApiNetworkError,
  EcosApiError,
  EcosAuthenticationError,
  EcosNetworkError,
  EcosNotFoundError,
  EcosQueryTimeoutError,
  EcosRateLimitError,
  EcosSampleLimitError,
  EcosServerError,
  EcosValidationError,
} from '../../src/core/errors';
import type { Logger } from '../../src/core/logger';
import { silentLogger } from '../../src/core/logger';
import { camelizeEcosKeys, EcosClient } from '../../src/ecos/client';
import { createFetchMock, jsonResponse, result, SAMPLE_LIMIT_MESSAGE, serveRows } from './_server';

// 누출 검사용 더미 값 — 하드코딩된 시크릿처럼 보이지 않도록 실행마다 새로 만든다.
const REAL_KEY = `test-${randomUUID()}`;

const rowsOf = (n: number) =>
  Array.from({ length: n }, (_, i) => ({
    STAT_CODE: '817Y002',
    STAT_NAME: '시장금리',
    TIME: String(i).padStart(8, '0'),
    DATA_VALUE: String(i),
  }));

const search = (client: EcosClient, options: { startRow?: number; endRow?: number } = {}) =>
  client.statisticSearch.search({ statCode: '817Y002', cycle: 'D', start: '20261001', end: '20261017', ...options });

const realClient = (
  fetchMock: typeof fetch,
  options: { maxRetries?: number; maxPages?: number; logger?: Logger } = {},
) => new EcosClient({ authKey: REAL_KEY, fetchImpl: fetchMock, logger: silentLogger, maxRetries: 0, ...options });

describe('EcosClient 키', () => {
  it('키가 없거나 빈 문자열이면 sample 키(10행 쪽)', () => {
    for (const authKey of [undefined, '']) {
      const client = new EcosClient({ authKey });
      expect(client.authKey).toBe('sample');
      expect(client.isSample).toBe(true);
      expect(client.pageSize).toBe(10);
    }
  });

  it('실키는 1000행 쪽', () => {
    const client = realClient(fetch);
    expect(client.isSample).toBe(false);
    expect(client.pageSize).toBe(1000);
  });
});

describe('EcosClient 경로', () => {
  it('서비스/키/json/언어/시작/끝/세그먼트 순으로 조립하고 세그먼트를 인코딩한다', async () => {
    const { calls, fetchMock } = serveRows('StatisticMeta', rowsOf(1));
    await realClient(fetchMock).getRows('StatisticMeta', [' 경제 심리 '], z.looseObject({}), {
      lang: 'en',
      startRow: 1,
      endRow: 5,
    });
    expect(calls[0]?.url).toBe(
      `https://ecos.bok.or.kr/api/StatisticMeta/${REAL_KEY}/json/en/1/5/${encodeURIComponent('경제 심리')}`,
    );
  });

  it('빈 세그먼트는 요청 전에 거부한다', async () => {
    const { calls, fetchMock } = serveRows('StatisticSearch', rowsOf(1));
    await expect(
      realClient(fetchMock).statisticSearch.search({ statCode: ' ', cycle: 'D', start: '1', end: '2' }),
    ).rejects.toThrow(RangeError);
    expect(calls).toHaveLength(0);
  });

  it.each([
    [0, 5],
    [5, 4],
  ])('행 범위 %i/%i 는 거부한다', async (startRow, endRow) => {
    const { fetchMock } = serveRows('StatisticSearch', rowsOf(1));
    await expect(search(realClient(fetchMock), { startRow, endRow })).rejects.toThrow(RangeError);
  });

  it('와이어 키를 소문자로 내린 뒤 camelCase 로 바꾼다', () => {
    expect(camelizeEcosKeys({ STAT_CODE: 1, P_STAT_CODE: 2, ITEM_CODE1: 3, list_total_count: 4 })).toEqual({
      statCode: 1,
      pStatCode: 2,
      itemCode1: 3,
      listTotalCount: 4,
    });
  });
});

describe('EcosClient 쪽 넘김', () => {
  it('sample 키는 10행씩 끝까지 이어 받는다', async () => {
    const { calls, fetchMock } = serveRows('StatisticSearch', rowsOf(25));
    const page = await search(new EcosClient({ fetchImpl: fetchMock, logger: silentLogger }));
    expect(page.rows).toHaveLength(25);
    expect(page.listTotalCount).toBe(25);
    expect(page.rowCount).toBeNull();
    expect(calls.map((call) => call.url.split('/json/kr/')[1]?.split('/817Y002')[0])).toEqual([
      '1/10',
      '11/20',
      '21/30',
    ]);
  });

  it('실키는 1000행씩 받는다', async () => {
    const { calls, fetchMock } = serveRows('StatisticSearch', rowsOf(1500), { sampleLimit: 10 });
    const page = await search(realClient(fetchMock));
    expect(page.rows).toHaveLength(1500);
    expect(calls).toHaveLength(2);
    expect(calls[1]?.url).toContain('/json/kr/1001/2000/');
  });

  it('행 범위를 주면 그 쪽만 받는다', async () => {
    const { calls, fetchMock } = serveRows('StatisticSearch', rowsOf(25));
    const page = await search(realClient(fetchMock), { startRow: 3, endRow: 4 });
    expect(page.rows.map((row) => row.dataValue)).toEqual(['2', '3']);
    expect(page.listTotalCount).toBe(25);
    expect(calls).toHaveLength(1);
  });

  it('INFO-200 은 예외가 아니라 빈 결과', async () => {
    const { fetchMock } = createFetchMock(() => jsonResponse(result('INFO-200', '해당하는 데이터가 없습니다.')));
    const page = await search(realClient(fetchMock));
    expect(page).toEqual({ listTotalCount: 0, rowCount: null, rows: [] });
  });

  it('쪽 넘김 상한에 닿으면 예외', async () => {
    const { fetchMock } = serveRows('StatisticSearch', rowsOf(35));
    const client = new EcosClient({ fetchImpl: fetchMock, logger: silentLogger, maxPages: 2 });
    await expect(search(client)).rejects.toThrow(/쪽 넘김 상한\(2쪽 × 10행\).*35행 중 20행/);
  });

  it('서비스 블록이 없으면 예외', async () => {
    const { fetchMock } = createFetchMock(() => jsonResponse({ Other: {} }));
    await expect(search(realClient(fetchMock))).rejects.toThrow(EcosApiError);
  });

  it('행이 명세와 다르면 예외', async () => {
    const { fetchMock } = serveRows('StatisticSearch', [{ STAT_NAME: '코드 없음', TIME: '2026' }]);
    await expect(search(realClient(fetchMock))).rejects.toThrow(/명세와 다릅니다/);
  });
});

describe('EcosClient 결과 코드', () => {
  it.each([
    ['INFO-100', EcosAuthenticationError],
    ['ERROR-100', EcosValidationError],
    ['ERROR-101', EcosValidationError],
    ['ERROR-301', EcosValidationError],
    ['ERROR-400', EcosQueryTimeoutError],
    ['ERROR-500', EcosServerError],
    ['ERROR-601', EcosServerError],
    ['ERROR-602', EcosRateLimitError],
    ['ERROR-999', EcosApiError],
  ])('%s → %s', async (code, ErrorCls) => {
    const { fetchMock } = createFetchMock(() => jsonResponse(result(code, '서버 메시지')));
    const error = await search(realClient(fetchMock)).catch((e: unknown) => e);
    expect(error).toBeInstanceOf(ErrorCls);
    expect(error).not.toBeInstanceOf(EcosSampleLimitError);
    expect((error as EcosApiError).errorCode).toBe(code);
    expect((error as Error).message).toContain('서버 메시지');
  });

  it('조치 문구를 메시지에 붙인다', async () => {
    const { fetchMock } = createFetchMock(() => jsonResponse(result('ERROR-101', '날짜 형식 오류')));
    await expect(search(realClient(fetchMock))).rejects.toThrow(/조치: 날짜는 주기 형식을 따릅니다/);
  });

  it('sample 10건 초과는 EcosSampleLimitError', async () => {
    const { fetchMock } = serveRows('StatisticSearch', rowsOf(30));
    const client = new EcosClient({ fetchImpl: fetchMock, logger: silentLogger });
    const error = await search(client, { startRow: 1, endRow: 20 }).catch((e: unknown) => e);
    expect(error).toBeInstanceOf(EcosSampleLimitError);
    expect(error).toBeInstanceOf(EcosValidationError);
    expect((error as Error).message).toContain(SAMPLE_LIMIT_MESSAGE.split('\n')[2]?.trim());
  });

  it('ERROR-600 은 재시도한다', async () => {
    const { calls, fetchMock } = createFetchMock((_, index) =>
      index === 0
        ? jsonResponse(result('ERROR-600', 'DB'))
        : jsonResponse({ StatisticSearch: { list_total_count: 1, row: rowsOf(1) } }),
    );
    const page = await search(realClient(fetchMock, { maxRetries: 1 }));
    expect(page.rows).toHaveLength(1);
    expect(calls).toHaveLength(2);
  });

  it('ERROR-400 은 재시도하지 않는다', async () => {
    const { calls, fetchMock } = createFetchMock(() => jsonResponse(result('ERROR-400', '60초')));
    await expect(search(realClient(fetchMock, { maxRetries: 1 }))).rejects.toThrow(EcosQueryTimeoutError);
    expect(calls).toHaveLength(1);
  });
});

describe('EcosClient HTTP 오류와 키 가리기', () => {
  it('HTTP 404 는 EcosNotFoundError', async () => {
    const { fetchMock } = createFetchMock(() => new Response('<html>503</html>', { status: 404 }));
    await expect(search(realClient(fetchMock))).rejects.toThrow(EcosNotFoundError);
  });

  it('HTTP 5xx 는 EcosServerError', async () => {
    const { fetchMock } = createFetchMock(() => jsonResponse({}, 502));
    await expect(search(realClient(fetchMock))).rejects.toThrow(EcosServerError);
  });

  it('JSON 이 아니면 EcosApiError', async () => {
    const { fetchMock } = createFetchMock(() => new Response('not json', { status: 200 }));
    await expect(search(realClient(fetchMock))).rejects.toThrow(EcosApiError);
  });

  it('연결 오류 메시지·requestContext·로그에 키가 남지 않는다', async () => {
    const fetchMock: typeof fetch = async (input) => {
      throw new TypeError(`fetch failed: ${String(input)}`);
    };
    const logged: unknown[] = [];
    const logger: Logger = { ...silentLogger, error: (message, context) => logged.push(message, context) };
    const error = (await search(realClient(fetchMock, { logger })).catch((e: unknown) => e)) as EcosNetworkError;
    expect(error).toBeInstanceOf(EcosNetworkError);
    expect(error).toBeInstanceOf(ApiNetworkError);
    expect(error.message).toContain('***');
    expect(JSON.stringify([error.message, error.requestContext, logged])).not.toContain(REAL_KEY);
    expect(error.requestContext?.path).toBe('/StatisticSearch/***/json/kr/1/1000/817Y002/D/20261001/20261017');
  });

  it('결과 코드 오류의 requestContext 에도 키가 없다', async () => {
    const { fetchMock } = createFetchMock(() => jsonResponse(result('INFO-100', '인증키가 유효하지 않습니다.')));
    const error = (await search(realClient(fetchMock)).catch((e: unknown) => e)) as EcosAuthenticationError;
    expect(JSON.stringify([error.message, error.requestContext])).not.toContain(REAL_KEY);
  });
});
