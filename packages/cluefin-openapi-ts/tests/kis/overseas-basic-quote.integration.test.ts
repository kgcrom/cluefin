import { describe, test } from 'vitest';

import { assertKisResponse, getKisClient, ONE_MONTH_AGO, runIntegration, TODAY } from '../_helpers/integration-setup';

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

  it('getCurrentPriceFirstQuote', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.getCurrentPriceFirstQuote({
      excd: 'NAS',
      symb: 'AAPL',
    });
    assertKisResponse(res);
  });

  it('getStockCurrentPriceConclusion', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.getStockCurrentPriceConclusion({
      auth: '',
      excd: 'NAS',
      symb: 'AAPL',
    });
    assertKisResponse(res);
  });

  it('getConclusionTrend', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.getConclusionTrend({
      excd: 'NAS',
      auth: '',
      keyb: '',
      tday: '1',
      symb: 'AAPL',
    });
    assertKisResponse(res);
  });

  it('getStockMinuteChart', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.getStockMinuteChart({
      auth: '',
      excd: 'NAS',
      symb: 'AAPL',
      nmin: '1',
      pinc: '0',
      next: '',
      nrec: '20',
      fill: '0',
      keyb: '',
    });
    assertKisResponse(res);
  });

  it('getIndexMinuteChart', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.getIndexMinuteChart({
      fidCondMrktDivCode: 'N',
      fidInputIscd: 'COMP',
      fidHourClsCode: '1',
      fidPwDataIncuYn: 'N',
    });
    assertKisResponse(res);
  });

  it('getItemIndexExchangePeriodPrice', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.getItemIndexExchangePeriodPrice({
      fidCondMrktDivCode: 'N',
      fidInputIscd: 'COMP',
      fidInputDate1: ONE_MONTH_AGO,
      fidInputDate2: TODAY,
      fidPeriodDivCode: 'D',
    });
    assertKisResponse(res);
  });

  it('searchByCondition', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.searchByCondition({
      auth: '',
      excd: 'NAS',
    });
    assertKisResponse(res);
  });

  it('getSettlementDate', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.getSettlementDate({
      tradDt: TODAY,
      ctxAreaNk: '',
      ctxAreaFk: '',
    });
    assertKisResponse(res);
  });

  it('getSectorPrice', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.getSectorPrice({
      keyb: '',
      auth: '',
      excd: 'NAS',
      icod: '',
      volRang: '0',
    });
    assertKisResponse(res);
  });

  it('getSectorCodes', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.getSectorCodes({
      auth: '',
      excd: 'NAS',
    });
    assertKisResponse(res);
  });
});
