import { describe, expect, it } from 'vitest';

import { silentLogger } from '../../src/core/logger';
import { EcosClient } from '../../src/ecos/client';
import { fixtureRows, serveRows } from './_server';

const sampleClient = (fetchMock: typeof fetch) => new EcosClient({ fetchImpl: fetchMock, logger: silentLogger });

describe('StatisticGlossary.word', () => {
  it('한글 용어를 경로에 인코딩해 넣고 용어설명을 돌려준다', async () => {
    const { calls, fetchMock } = serveRows('StatisticWord', fixtureRows('statistic_word.json', 'StatisticWord'));
    const page = await sampleClient(fetchMock).statisticGlossary.word({ term: '소비자동향지수' });
    expect(calls[0]?.url).toBe(
      `https://ecos.bok.or.kr/api/StatisticWord/sample/json/kr/1/10/${encodeURIComponent('소비자동향지수')}`,
    );
    expect(page.listTotalCount).toBe(1);
    expect(page.rows[0]?.word).toBe('소비자동향지수');
    expect(page.rows[0]?.content).toContain('소비자들이 느끼는 경기');
  });
});

describe('StatisticGlossary.meta', () => {
  it('메타 트리 노드를 camelCase 로 돌려준다', async () => {
    const { fetchMock } = serveRows('StatisticMeta', fixtureRows('statistic_meta.json', 'StatisticMeta'));
    const page = await sampleClient(fetchMock).statisticGlossary.meta({ dataName: '경제심리', startRow: 1, endRow: 3 });
    expect(page.listTotalCount).toBeGreaterThan(0);
    expect(page.rows[0]).toEqual({
      lvl: '2',
      pContCode: '0000000108',
      contCode: 'N13',
      contName: '참고 자료',
      metaData: null,
    });
    expect(page.rows[2]?.pContCode).toBeNull();
  });
});
