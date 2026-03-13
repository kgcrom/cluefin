import { describe, test } from 'vitest';

import { assertKisResponse, getKisClient, ONE_MONTH_AGO, runIntegration, TODAY } from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

const BOND_CODE = 'KR2033022D33';

describe('KIS OnmarketBondBasicQuote', () => {
  it('getBondPrice', async () => {
    const client = await getKisClient();
    const res = await client.onmarketBondBasicQuote.getBondPrice({
      fidInputIscd: BOND_CODE,
    });
    assertKisResponse(res);
  });

  it('getBondInfo', async () => {
    const client = await getKisClient();
    const res = await client.onmarketBondBasicQuote.getBondInfo({
      pdno: BOND_CODE,
    });
    assertKisResponse(res);
  });

  it('getBondAskingPrice', async () => {
    const client = await getKisClient();
    const res = await client.onmarketBondBasicQuote.getBondAskingPrice({
      fidInputIscd: BOND_CODE,
    });
    assertKisResponse(res);
  });

  it('getBondExecution', async () => {
    const client = await getKisClient();
    const res = await client.onmarketBondBasicQuote.getBondExecution({
      fidInputIscd: BOND_CODE,
    });
    assertKisResponse(res);
  });

  it('getBondDailyPrice', async () => {
    const client = await getKisClient();
    const res = await client.onmarketBondBasicQuote.getBondDailyPrice({
      fidInputIscd: BOND_CODE,
    });
    assertKisResponse(res);
  });

  it('getBondDailyChartPrice', async () => {
    const client = await getKisClient();
    const res = await client.onmarketBondBasicQuote.getBondDailyChartPrice({
      fidInputIscd: BOND_CODE,
    });
    assertKisResponse(res);
  });

  it('getBondAvgUnitPrice', async () => {
    const client = await getKisClient();
    const res = await client.onmarketBondBasicQuote.getBondAvgUnitPrice({
      inqrStrtDt: TODAY,
      inqrEndDt: TODAY,
    });
    assertKisResponse(res);
  });

  it('getBondIssueInfo', async () => {
    const client = await getKisClient();
    const res = await client.onmarketBondBasicQuote.getBondIssueInfo({
      pdno: BOND_CODE,
    });
    assertKisResponse(res);
  });
});
