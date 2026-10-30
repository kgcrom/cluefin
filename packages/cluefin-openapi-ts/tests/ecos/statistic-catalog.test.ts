import { describe, expect, it } from 'vitest';

import { silentLogger } from '../../src/core/logger';
import { EcosClient } from '../../src/ecos/client';
import { createFetchMock, fixtureRows, jsonResponse, loadFixture, serveRows } from './_server';

const sampleClient = (fetchMock: typeof fetch) => new EcosClient({ fetchImpl: fetchMock, logger: silentLogger });

describe('StatisticCatalog.tableList', () => {
  it('통계표코드를 생략하면 경로에 세그먼트가 없고, 분류 행은 cycle 이 null', async () => {
    const { calls, fetchMock } = serveRows(
      'StatisticTableList',
      fixtureRows('statistic_table_list.json', 'StatisticTableList'),
    );
    const page = await sampleClient(fetchMock).statisticCatalog.tableList();
    expect(calls[0]?.url).toMatch(/\/StatisticTableList\/sample\/json\/kr\/1\/10$/);
    expect(page.rows[0]).toEqual({
      pStatCode: '*',
      statCode: '0000000001',
      statName: '1. 통화/금융',
      cycle: null,
      srchYn: 'N',
      orgName: null,
    });
  });

  it('통계표코드를 주면 경로 끝에 붙는다', async () => {
    const { calls, fetchMock } = serveRows(
      'StatisticTableList',
      fixtureRows('statistic_table_list.json', 'StatisticTableList'),
    );
    await sampleClient(fetchMock).statisticCatalog.tableList({ statCode: '817Y002' });
    expect(calls[0]?.url).toMatch(/\/1\/10\/817Y002$/);
  });
});

describe('StatisticCatalog.itemList', () => {
  it('817Y002 항목 27개를 쪽 넘김으로 받고 자료수는 숫자', async () => {
    const rows = fixtureRows('statistic_item_list_817Y002.json', 'StatisticItemList');
    const { calls, fetchMock } = serveRows('StatisticItemList', rows);
    const page = await sampleClient(fetchMock).statisticCatalog.itemList({ statCode: '817Y002' });
    expect(calls).toHaveLength(Math.ceil(rows.length / 10));
    expect(page.rows).toHaveLength(rows.length);
    expect(page.rows[0]).toMatchObject({
      grpCode: 'Group1',
      itemCode: '010101000',
      itemName: '콜금리(1일, 전체거래)',
      pItemCode: '010100000',
      startTime: '19950103',
      dataCnt: 8068,
      weight: null,
    });
  });
});

describe('StatisticCatalog.keyStatisticList', () => {
  it('명세에 없는 row_count 를 rowCount 로 싣는다(한 쪽만 받을 때)', async () => {
    const { fetchMock } = createFetchMock(() => jsonResponse(loadFixture('key_statistic_list.json')));
    const page = await sampleClient(fetchMock).statisticCatalog.keyStatisticList({ startRow: 1, endRow: 10 });
    expect(page.listTotalCount).toBe(101);
    expect(page.rowCount).toBe(10);
    expect(page.rows[0]).toEqual({
      className: '통화량',
      keystatName: 'M1(협의통화, 평잔)',
      dataValue: '1351852.9',
      cycle: '202608',
      unitName: '십억원',
    });
  });

  it('쪽 넘김으로 받으면 rowCount 는 null', async () => {
    const rows = fixtureRows('key_statistic_list.json', 'KeyStatisticList');
    const { fetchMock } = serveRows('KeyStatisticList', rows, { extra: { row_count: 10 } });
    const page = await sampleClient(fetchMock).statisticCatalog.keyStatisticList();
    expect(page.rows).toHaveLength(rows.length);
    expect(page.rowCount).toBeNull();
  });
});
