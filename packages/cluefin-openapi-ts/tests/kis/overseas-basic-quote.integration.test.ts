import { describe, test } from 'vitest';

import { assertKisResponse, getKisClient, runIntegration, TODAY } from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('KIS OverseasBasicQuote', () => {
  it('getStockCurrentPriceDetail', async () => {
    const client = await getKisClient();
    const res = await (client.overseasBasicQuote as any).getStockCurrentPriceDetail({
      auth: '',
      excd: 'NAS',
      symb: 'AAPL',
    });
    assertKisResponse(res);
  });

  it('getStockPeriodQuote', async () => {
    const client = await getKisClient();
    const res = await (client.overseasBasicQuote as any).getStockPeriodQuote({
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
    const res = await (client.overseasBasicQuote as any).getProductBaseInfo({
      prdtTypeCd: '512',
      pdno: 'AAPL',
    });
    assertKisResponse(res);
  });
});
