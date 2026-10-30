import { describe, expect, it } from 'vitest';

import { silentLogger } from '../../src/core/logger';
import { EcosClient } from '../../src/ecos/client';
import { CPI_TOTAL, KTB_10Y, MARKET_RATES, USD_KRW } from '../../src/ecos/constants';
import { parseEcosValue } from '../../src/ecos/statistic-search';
import { fixtureRows, serveRows } from './_server';

const sampleClient = (fetchMock: typeof fetch) => new EcosClient({ fetchImpl: fetchMock, logger: silentLogger });

describe('StatisticSearch', () => {
  it('817Y002 픽스처를 쪽 넘김으로 다 받아 camelCase 행으로 돌려준다', async () => {
    const rows = fixtureRows('statistic_search_817Y002.json', 'StatisticSearch');
    const { calls, fetchMock } = serveRows('StatisticSearch', rows);
    const page = await sampleClient(fetchMock).statisticSearch.search({
      statCode: '817Y002',
      cycle: 'D',
      start: '20261005',
      end: '20261017',
    });
    expect(page.listTotalCount).toBe(81);
    expect(page.rows).toHaveLength(81);
    expect(calls).toHaveLength(9);
    expect(page.rows[0]).toMatchObject({
      statCode: '817Y002',
      itemCode1: '010190000',
      itemName1: '국고채(1년)',
      unitName: '연%',
      time: '20261006',
      dataValue: '3.737',
      itemCode2: null,
    });
  });

  it('항목코드는 경로 끝에 붙고 4개를 넘으면 거부한다', async () => {
    const { calls, fetchMock } = serveRows(
      'StatisticSearch',
      fixtureRows('statistic_search_731Y001.json', 'StatisticSearch'),
    );
    const search = sampleClient(fetchMock).statisticSearch;
    await search.search({
      statCode: '731Y001',
      cycle: 'D',
      start: '20261010',
      end: '20261017',
      itemCodes: ['0000001'],
    });
    expect(calls[0]?.url).toMatch(/\/json\/kr\/1\/10\/731Y001\/D\/20261010\/20261017\/0000001$/);
    await expect(
      search.search({ statCode: 'X', cycle: 'D', start: '1', end: '2', itemCodes: ['1', '2', '3', '4', '5'] }),
    ).rejects.toThrow(RangeError);
  });

  it('searchSeries 는 상수 계열의 통계표·주기·항목코드로 묻는다', async () => {
    const { calls, fetchMock } = serveRows(
      'StatisticSearch',
      fixtureRows('statistic_search_901Y009.json', 'StatisticSearch'),
    );
    const page = await sampleClient(fetchMock).statisticSearch.searchSeries(CPI_TOTAL, '202509', '202609');
    expect(calls[0]?.url).toMatch(/\/901Y009\/M\/202509\/202609\/0$/);
    // WGT 는 문자열("1000")로 온다. 숫자로 와도 문자열로 둔다.
    expect(page.rows[0]?.wgt).toBe('1000');
    expect(page.rows).toHaveLength(13);
  });

  it('숫자로 온 문자열 필드는 문자열로 바꾼다', async () => {
    const { fetchMock } = serveRows('StatisticSearch', [
      { STAT_CODE: '901Y009', STAT_NAME: 'CPI', TIME: 202609, WGT: 1000, DATA_VALUE: 117.5 },
    ]);
    const page = await sampleClient(fetchMock).statisticSearch.search({
      statCode: '901Y009',
      cycle: 'M',
      start: '202609',
      end: '202609',
    });
    expect(page.rows[0]).toMatchObject({ time: '202609', wgt: '1000', dataValue: '117.5' });
  });
});

describe('상수와 값 변환', () => {
  it('Python _constants 와 같은 코드', () => {
    expect(KTB_10Y).toEqual({ statCode: '817Y002', cycle: 'D', itemCode: '010210000', name: '국고채(10년)' });
    expect(USD_KRW.itemCode).toBe('0000001');
    expect(MARKET_RATES).toHaveLength(10);
    expect(Object.isFrozen(KTB_10Y)).toBe(true);
  });

  it.each([
    ['4.182', 4.182],
    ['-0.5', -0.5],
    ['', null],
    ['  ', null],
    [null, null],
    [undefined, null],
    ['-', null],
  ])('parseEcosValue(%j) = %j', (input, expected) => {
    expect(parseEcosValue(input)).toBe(expected);
  });
});
