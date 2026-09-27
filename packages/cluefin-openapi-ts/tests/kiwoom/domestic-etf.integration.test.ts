import { describe, test } from 'vitest';

import {
  etfDailyExecutionResponseSchema,
  etfDailyTrendResponseSchema,
  etfFullPriceResponseSchema,
  etfHourlyExecutionResponseSchema,
  etfHourlyExecutionV2ResponseSchema,
  etfHourlyTrendResponseSchema,
  etfHourlyTrendV2ResponseSchema,
  etfItemInfoResponseSchema,
  etfReturnRateResponseSchema,
} from '../../src/kiwoom/schemas/domestic-etf';
import {
  assertKiwoomResponse,
  getKiwoomClient,
  KODEX200,
  runIntegration,
  setupKiwoomRateLimit,
} from '../_helpers/integration-setup';
import { assertKiwoomSpecConformance } from '../_helpers/kiwoom-spec-conformance';

const it = runIntegration ? test : test.skip;

describe('Kiwoom DomesticEtf', () => {
  setupKiwoomRateLimit();
  it('getEtfReturnRate', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfReturnRate({
      stkCd: KODEX200,
      etfobjtIdexCd: '001',
      dt: '0',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(etfReturnRateResponseSchema);
  });

  it('getEtfItemInfo', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfItemInfo({
      stkCd: KODEX200,
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(etfItemInfoResponseSchema);
  });

  it('getEtfDailyTrend', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfDailyTrend({
      stkCd: KODEX200,
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(etfDailyTrendResponseSchema);
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
    assertKiwoomSpecConformance(etfFullPriceResponseSchema);
  });

  it('getEtfHourlyTrend', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfHourlyTrend({
      stkCd: KODEX200,
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(etfHourlyTrendResponseSchema);
  });

  it('getEtfHourlyExecution', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfHourlyExecution({
      stkCd: KODEX200,
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(etfHourlyExecutionResponseSchema);
  });

  it('getEtfDailyExecution', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfDailyExecution({
      stkCd: KODEX200,
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(etfDailyExecutionResponseSchema);
  });

  it('getEtfHourlyExecutionV2', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfHourlyExecutionV2({
      stkCd: KODEX200,
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(etfHourlyExecutionV2ResponseSchema);
  });

  it('getEtfHourlyTrendV2', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfHourlyTrendV2({
      stkCd: KODEX200,
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(etfHourlyTrendV2ResponseSchema);
  });
});
