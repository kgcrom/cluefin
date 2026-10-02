import { describe, expect, test } from 'vitest';

import {
  DART_SAMSUNG_CORP_CODE,
  getDartClient,
  runDartIntegration,
  setupDartRateLimit,
} from '../_helpers/integration-setup';

const it = runDartIntegration ? test : test.skip;

const ACCOUNT = { corpCode: DART_SAMSUNG_CORP_CODE, bsnsYear: '2023', reprtCode: '11011' };

describe('Dart PeriodicReportFinancialStatement', () => {
  setupDartRateLimit();

  it('getSingleCompanyMajorAccounts', async () => {
    const res = await getDartClient().periodicReportFinancialStatement.getSingleCompanyMajorAccounts(ACCOUNT);

    expect(res.body.status).toBe('000');
    expect(res.body.list?.[0]).toHaveProperty('accountNm');
  });

  it('getMultiCompanyMajorAccounts', async () => {
    const res = await getDartClient().periodicReportFinancialStatement.getMultiCompanyMajorAccounts({
      ...ACCOUNT,
      corpCode: `${DART_SAMSUNG_CORP_CODE},00164779`,
    });

    expect(res.body.status).toBe('000');
    expect(res.body.list?.length).toBeGreaterThan(0);
  });

  it('getSingleCompanyFullStatements', async () => {
    const res = await getDartClient().periodicReportFinancialStatement.getSingleCompanyFullStatements({
      ...ACCOUNT,
      fsDiv: 'CFS',
    });

    expect(res.body.status).toBe('000');
    expect(res.body.list?.[0]).toHaveProperty('sjDiv');
  });

  it('getSingleCompanyMajorIndicators', async () => {
    const res = await getDartClient().periodicReportFinancialStatement.getSingleCompanyMajorIndicators({
      ...ACCOUNT,
      idxClCode: 'M210000',
    });

    expect(res.body.status).toBe('000');
    expect(res.body.list?.[0]).toHaveProperty('idxNm');
  });

  it('getMultiCompanyMajorIndicators', async () => {
    const res = await getDartClient().periodicReportFinancialStatement.getMultiCompanyMajorIndicators({
      ...ACCOUNT,
      corpCode: `${DART_SAMSUNG_CORP_CODE},00164779`,
      idxClCode: 'M210000',
    });

    expect(res.body.status).toBe('000');
    expect(res.body.list?.length).toBeGreaterThan(0);
  });

  it('getXbrlTaxonomy', async () => {
    const res = await getDartClient().periodicReportFinancialStatement.getXbrlTaxonomy({ sjDiv: 'BS1' });

    expect(res.body.status).toBe('000');
    expect(res.body.list?.length).toBeGreaterThan(0);
  });

  it('downloadFinancialStatementXbrl', async () => {
    const client = getDartClient();
    const search = await client.publicDisclosure.publicDisclosureSearch({
      corpCode: DART_SAMSUNG_CORP_CODE,
      pblntfDetailTy: 'A001',
      bgnDe: '20240101',
      endDe: '20240430',
      pageCount: 1,
    });
    const rceptNo = search.body.list?.[0]?.rceptNo;
    expect(rceptNo).toBeTruthy();

    const res = await client.periodicReportFinancialStatement.downloadFinancialStatementXbrl({
      rceptNo,
      reprtCode: '11011',
    });

    expect([...res.body.keys()].some((name) => name.endsWith('.xbrl'))).toBe(true);
  });
});
