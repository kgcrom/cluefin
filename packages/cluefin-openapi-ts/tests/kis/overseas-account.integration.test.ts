import { describe, test } from 'vitest';

import { assertKisResponse, getKisClient, runIntegration } from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('KIS OverseasAccount', () => {
  it('getBuyTradableAmount', async () => {
    const client = await getKisClient();
    const res = await client.overseasAccount.getBuyTradableAmount({
      cano: process.env.KIS_CANO ?? '',
      acntPrdtCd: process.env.KIS_ACNT_PRDT_CD ?? '01',
      ovrsExcgCd: 'NASD',
      ovrsOrdUnpr: '150',
      itemCd: 'AAPL',
    });
    assertKisResponse(res);
  });

  it('getStockBalance', async () => {
    const client = await getKisClient();
    const res = await client.overseasAccount.getStockBalance({
      cano: process.env.KIS_CANO ?? '',
      acntPrdtCd: process.env.KIS_ACNT_PRDT_CD ?? '01',
      ovrsExcgCd: 'NASD',
      trCrcyCd: 'USD',
    });
    assertKisResponse(res);
  });

  it('getStockNotConclusionHistory', async () => {
    const client = await getKisClient();
    const res = await client.overseasAccount.getStockNotConclusionHistory({
      cano: process.env.KIS_CANO ?? '',
      acntPrdtCd: process.env.KIS_ACNT_PRDT_CD ?? '01',
      ovrsExcgCd: 'NASD',
      sortSqn: 'DS',
    });
    assertKisResponse(res);
  });
});
