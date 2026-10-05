import { describe, expect, test } from 'vitest';

import {
  DART_SAMSUNG_CORP_CODE,
  getDartClient,
  runDartIntegration,
  setupDartRateLimit,
} from '../_helpers/integration-setup';

const it = runDartIntegration ? test : test.skip;

describe('Dart PublicDisclosure', () => {
  setupDartRateLimit();

  it('publicDisclosureSearch', async () => {
    const res = await getDartClient().publicDisclosure.publicDisclosureSearch({
      corpCode: DART_SAMSUNG_CORP_CODE,
      pageCount: 5,
    });

    expect(res.body.status).toBe('000');
    expect(res.body.list?.length).toBeGreaterThan(0);
    expect(res.body.list?.[0]).toHaveProperty('rceptNo');
  });

  it('companyOverview', async () => {
    const res = await getDartClient().publicDisclosure.companyOverview({ corpCode: DART_SAMSUNG_CORP_CODE });

    expect(res.body.status).toBe('000');
    expect(res.body.stockCode).toBe('005930');
  });

  it('disclosureDocumentFile', async () => {
    const client = getDartClient();
    const search = await client.publicDisclosure.publicDisclosureSearch({
      corpCode: DART_SAMSUNG_CORP_CODE,
      pblntfTy: 'A',
      bgnDe: '20240101',
      endDe: '20241231',
      pageCount: 1,
    });
    const rceptNo = search.body.list?.[0]?.rceptNo;
    expect(rceptNo).toBeTruthy();

    const res = await client.publicDisclosure.disclosureDocumentFile({ rceptNo });

    expect(res.body.length).toBeGreaterThan(1000);
    expect(new TextDecoder().decode(res.body.subarray(0, 200))).toContain('<');
  });

  it('disclosureDocumentFiles', async () => {
    const client = getDartClient();
    const search = await client.publicDisclosure.publicDisclosureSearch({
      corpCode: DART_SAMSUNG_CORP_CODE,
      pblntfTy: 'A',
      bgnDe: '20250101',
      endDe: '20251231',
      pageCount: 1,
    });
    const rceptNo = search.body.list?.[0]?.rceptNo;
    expect(rceptNo).toBeTruthy();

    const res = await client.publicDisclosure.disclosureDocumentFiles({ rceptNo });

    expect([...res.body.keys()][0]).toBe(`${rceptNo}.xml`);
    for (const data of res.body.values()) {
      expect(data.length).toBeGreaterThan(1000);
    }
  });

  it('corpCode', async () => {
    const res = await getDartClient().publicDisclosure.corpCode();

    expect(res.body.status).toBe('000');
    expect(res.body.list.length).toBeGreaterThan(50_000);
    const samsung = res.body.list.find((item) => item.corpCode === DART_SAMSUNG_CORP_CODE);
    expect(samsung).toMatchObject({ corpName: '삼성전자', stockCode: '005930' });
  });
});
