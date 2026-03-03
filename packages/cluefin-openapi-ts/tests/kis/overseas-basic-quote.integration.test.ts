import { describe, test } from 'vitest';

import { assertKisResponse, getKisClient, runIntegration, TODAY } from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('KIS OverseasBasicQuote', () => {
  it('getStockCurrentPriceDetail', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.getStockCurrentPriceDetail({
      auth: '',
      excd: 'NAS',
      symb: 'AAPL',
    });
    assertKisResponse(res);
  });

  it('getStockPeriodQuote', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.getStockPeriodQuote({
      auth: '',
      excd: 'NAS',
      symb: 'AAPL',
      gubn: '0',
      bymd: TODAY,
      modp: '0',
    });
    assertKisResponse(res);
  });

  it('getProductBaseInfo', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.getProductBaseInfo({
      prdtTypeCd: '512',
      pdno: 'AAPL',
    });
    assertKisResponse(res);
  });
});
