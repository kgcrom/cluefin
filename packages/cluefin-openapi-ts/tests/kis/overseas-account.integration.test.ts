import { describe, test } from 'vitest';

import {
  assertKisResponse,
  getKisClient,
  KIS_ACNT_PRDT_CD,
  KIS_CANO,
  runAccountIntegration,
} from '../_helpers/integration-setup';

const it = runAccountIntegration ? test : test.skip;

describe('KIS OverseasAccount', () => {
  it('getBuyTradableAmount', async () => {
    const client = await getKisClient();
    const res = await client.overseasAccount.getBuyTradableAmount({
      cano: KIS_CANO,
      acntPrdtCd: KIS_ACNT_PRDT_CD,
      ovrsExcgCd: 'NASD',
      ovrsOrdUnpr: '150',
      itemCd: 'AAPL',
    });
    assertKisResponse(res);
  });

  it('getStockBalance', async () => {
    const client = await getKisClient();
    const res = await client.overseasAccount.getStockBalance({
      cano: KIS_CANO,
      acntPrdtCd: KIS_ACNT_PRDT_CD,
      ovrsExcgCd: 'NASD',
      trCrcyCd: 'USD',
    });
    assertKisResponse(res);
  });

  it('getStockNotConclusionHistory', async () => {
    const client = await getKisClient();
    const res = await client.overseasAccount.getStockNotConclusionHistory({
      cano: KIS_CANO,
      acntPrdtCd: KIS_ACNT_PRDT_CD,
      ovrsExcgCd: 'NASD',
      sortSqn: 'DS',
    });
    assertKisResponse(res);
  });
});
