import { describe, expect, test } from 'vitest';
import type { z } from 'zod';

import { EcosSampleLimitError } from '../../src/core/errors';
import { EcosClient } from '../../src/ecos/client';
import { KTB_10Y } from '../../src/ecos/constants';
import { keyStatisticSchema, statisticItemSchema, statisticTableSchema } from '../../src/ecos/statistic-catalog';
import { statisticMetaItemSchema, statisticWordSchema } from '../../src/ecos/statistic-glossary';
import { statisticObservationSchema } from '../../src/ecos/statistic-search';
import { runIntegration, setupDartRateLimit } from '../_helpers/integration-setup';

// sample 키는 가입 없이 늘 돈다. 실키 경로는 ECOS_AUTH_KEY 가 있을 때만.
const it = runIntegration ? test : test.skip;
const itWithKey = runIntegration && process.env.ECOS_AUTH_KEY ? test : test.skip;

const sample = new EcosClient();

/** 응답 행의 키가 모두 스키마에 있는지 — looseObject 라 명세 밖 필드가 와도 조용히 지나가므로 따로 본다. */
const expectKnownKeys = (rows: readonly object[], schema: z.ZodObject) => {
  const known = new Set(Object.keys(schema.shape));
  for (const row of rows) {
    expect(Object.keys(row).filter((key) => !known.has(key))).toEqual([]);
  }
};

describe('ECOS (sample 키)', () => {
  // DART 와 같은 1초 간격. ECOS 공식 한도는 미확인이다.
  setupDartRateLimit();

  it('StatisticSearch — 웹 명세 예시 200Y101/A/2020/2023/10101', async () => {
    const page = await sample.statisticSearch.search({
      statCode: '200Y101',
      cycle: 'A',
      start: '2020',
      end: '2023',
      itemCodes: ['10101'],
    });
    expect(page.listTotalCount).toBe(4);
    expect(page.rows.map((row) => row.time)).toEqual(['2020', '2021', '2022', '2023']);
    expectKnownKeys(page.rows, statisticObservationSchema);
  });

  it('StatisticSearch — 국고채 10년 2주를 쪽 넘김으로', async () => {
    const page = await sample.statisticSearch.searchSeries(KTB_10Y, '20261001', '20261017');
    expect(page.rows.length).toBe(page.listTotalCount);
    expect(page.rows.every((row) => row.itemCode1 === KTB_10Y.itemCode)).toBe(true);
  });

  it('StatisticSearch — sample 로 10행 넘게 한 쪽을 달라면 EcosSampleLimitError', async () => {
    await expect(
      sample.statisticSearch.search({
        statCode: '817Y002',
        cycle: 'D',
        start: '20261001',
        end: '20261017',
        startRow: 1,
        endRow: 11,
      }),
    ).rejects.toThrow(EcosSampleLimitError);
  });

  it('StatisticSearch — 없는 통계표는 빈 결과(INFO-200)', async () => {
    const page = await sample.statisticSearch.search({ statCode: '000Y000', cycle: 'A', start: '2020', end: '2021' });
    expect(page.rows).toEqual([]);
  });

  it('StatisticTableList', async () => {
    const page = await sample.statisticCatalog.tableList({ startRow: 1, endRow: 10 });
    expect(page.listTotalCount).toBeGreaterThan(800);
    expect(page.rows).toHaveLength(10);
    expectKnownKeys(page.rows, statisticTableSchema);
  });

  it('StatisticItemList — 시장금리 817Y002', async () => {
    const page = await sample.statisticCatalog.itemList({ statCode: '817Y002', startRow: 1, endRow: 10 });
    expect(page.listTotalCount).toBeGreaterThan(20);
    expect(page.rows[0]?.statCode).toBe('817Y002');
    expectKnownKeys(page.rows, statisticItemSchema);
  });

  it('KeyStatisticList — 명세 밖 row_count 가 온다', async () => {
    const page = await sample.statisticCatalog.keyStatisticList({ startRow: 1, endRow: 10 });
    expect(page.listTotalCount).toBeGreaterThan(90);
    expect(page.rowCount).toBe(10);
    expectKnownKeys(page.rows, keyStatisticSchema);
  });

  it('StatisticWord', async () => {
    const page = await sample.statisticGlossary.word({ term: '소비자동향지수' });
    expect(page.rows[0]?.word).toBe('소비자동향지수');
    expectKnownKeys(page.rows, statisticWordSchema);
  });

  it('StatisticMeta — 부분 일치', async () => {
    const page = await sample.statisticGlossary.meta({ dataName: '경제심리지수', startRow: 1, endRow: 10 });
    expect(page.listTotalCount).toBeGreaterThan(0);
    expectKnownKeys(page.rows, statisticMetaItemSchema);
  });
});

describe('ECOS (실키)', () => {
  itWithKey('시장금리 2주 전 항목을 1000행 쪽으로 한 번에', async () => {
    const client = new EcosClient({ authKey: process.env.ECOS_AUTH_KEY });
    expect(client.isSample).toBe(false);
    const page = await client.statisticSearch.search({
      statCode: '817Y002',
      cycle: 'D',
      start: '20261001',
      end: '20261017',
    });
    expect(page.rows.length).toBe(page.listTotalCount);
    expect(page.rows.length).toBeGreaterThan(100);
  });
});
