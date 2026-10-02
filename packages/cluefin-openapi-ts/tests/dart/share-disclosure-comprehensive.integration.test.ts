import { describe, expect, test } from 'vitest';

import {
  DART_SAMSUNG_CORP_CODE,
  getDartClient,
  runDartIntegration,
  setupDartRateLimit,
} from '../_helpers/integration-setup';

const it = runDartIntegration ? test : test.skip;

describe('Dart ShareDisclosureComprehensive', () => {
  setupDartRateLimit();

  it('largeHoldingReport', async () => {
    const res = await getDartClient().shareDisclosureComprehensive.largeHoldingReport({
      corpCode: DART_SAMSUNG_CORP_CODE,
    });

    expect(['000', '013']).toContain(res.body.status);
    if (res.body.status === '000') expect(res.body.list?.[0]).toHaveProperty('rceptNo');
  });

  it('executiveMajorShareholderOwnershipReport', async () => {
    const res = await getDartClient().shareDisclosureComprehensive.executiveMajorShareholderOwnershipReport({
      corpCode: DART_SAMSUNG_CORP_CODE,
    });

    expect(['000', '013']).toContain(res.body.status);
    if (res.body.status === '000') expect(res.body.list?.[0]).toHaveProperty('rceptNo');
  });
});
