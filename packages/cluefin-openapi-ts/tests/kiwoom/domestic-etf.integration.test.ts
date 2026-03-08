import { describe, test } from 'vitest';
import { assertKiwoomResponse, getKiwoomClient, KODEX200, runIntegration, TODAY } from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('Kiwoom DomesticEtf', () => {
  it('getEtfReturnRate', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfReturnRate({ stkCd: KODEX200, etfobjtIdexCd: '001', dt: TODAY });
    assertKiwoomResponse(res);
  });

  it('getEtfItemInfo', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfItemInfo({ stkCd: KODEX200 });
    assertKiwoomResponse(res);
  });

  it('getEtfDailyTrend', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfDailyTrend({ stkCd: KODEX200 });
    assertKiwoomResponse(res);
  });

  it('getEtfFullPrice', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfFullPrice({
      txonType: '0',
      navpre: '0',
      mngmcomp: '0',
      txonYn: '0',
      traceIdex: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getEtfHourlyTrend', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfHourlyTrend({ stkCd: KODEX200 });
    assertKiwoomResponse(res);
  });

  it('getEtfHourlyExecution', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfHourlyExecution({ stkCd: KODEX200 });
    assertKiwoomResponse(res);
  });

  it('getEtfDailyExecution', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfDailyExecution({ stkCd: KODEX200 });
    assertKiwoomResponse(res);
  });

  it('getEtfHourlyExecutionV2', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfHourlyExecutionV2({ stkCd: KODEX200 });
    assertKiwoomResponse(res);
  });

  it('getEtfHourlyTrendV2', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticEtf.getEtfHourlyTrendV2({ stkCd: KODEX200 });
    assertKiwoomResponse(res);
  });
});
