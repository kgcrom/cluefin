import { describe, test } from 'vitest';

import {
  etfDailyExecutionItemSchema,
  etfDailyExecutionResponseSchema,
  etfDailyTrendItemSchema,
  etfDailyTrendResponseSchema,
  etfFullPriceItemSchema,
  etfFullPriceResponseSchema,
  etfHourlyExecutionItemSchema,
  etfHourlyExecutionResponseSchema,
  etfHourlyExecutionV2ItemSchema,
  etfHourlyExecutionV2ResponseSchema,
  etfHourlyTrendItemSchema,
  etfHourlyTrendResponseSchema,
  etfHourlyTrendV2ItemSchema,
  etfHourlyTrendV2ResponseSchema,
  etfItemInfoResponseSchema,
  etfReturnRateItemSchema,
  etfReturnRateResponseSchema,
} from '../../src/kiwoom/schemas/domestic-etf';
import {
  assertKiwoomResponse,
  assertResponseShape,
  getKiwoomClient,
  KODEX200,
  runIntegration,
  setupKiwoomRateLimit,
} from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('Kiwoom DomesticEtf', () => {
  setupKiwoomRateLimit();
  it('getEtfReturnRate', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfReturnRate({
      stkCd: `KRX:${KODEX200}`,
      etfobjtIdexCd: '001',
      dt: '0',
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, etfReturnRateResponseSchema, 'etfprftRtLst', etfReturnRateItemSchema);
  });

  it('getEtfItemInfo', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfItemInfo({
      stkCd: `KRX:${KODEX200}`,
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, etfItemInfoResponseSchema);
  });

  it('getEtfDailyTrend', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfDailyTrend({
      stkCd: `KRX:${KODEX200}`,
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, etfDailyTrendResponseSchema, 'etfdalyTrnsn', etfDailyTrendItemSchema);
  });

  it('getEtfFullPrice', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfFullPrice({
      txonType: '0',
      navpre: '0',
      mngmcomp: '0000',
      txonYn: '0',
      traceIdex: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, etfFullPriceResponseSchema, 'etfallMrpr', etfFullPriceItemSchema);
  });

  it('getEtfHourlyTrend', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfHourlyTrend({
      stkCd: `KRX:${KODEX200}`,
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, etfHourlyTrendResponseSchema, 'etftislTrnsn', etfHourlyTrendItemSchema);
  });

  it('getEtfHourlyExecution', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfHourlyExecution({
      stkCd: `KRX:${KODEX200}`,
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, etfHourlyExecutionResponseSchema, 'etftislCntrArray', etfHourlyExecutionItemSchema);
  });

  it('getEtfDailyExecution', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfDailyExecution({
      stkCd: `KRX:${KODEX200}`,
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, etfDailyExecutionResponseSchema, 'etfnetprpsQtyArray', etfDailyExecutionItemSchema);
  });

  it('getEtfHourlyExecutionV2', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfHourlyExecutionV2({
      stkCd: `KRX:${KODEX200}`,
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, etfHourlyExecutionV2ResponseSchema, 'etfnavarray', etfHourlyExecutionV2ItemSchema);
  });

  it('getEtfHourlyTrendV2', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfHourlyTrendV2({
      stkCd: `KRX:${KODEX200}`,
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, etfHourlyTrendV2ResponseSchema, 'etftislTrnsn', etfHourlyTrendV2ItemSchema);
  });
});
