import { describe, test } from 'vitest';

import {
  assertKisResponse,
  getKisClient,
  KODEX200,
  ONE_MONTH_AGO,
  runIntegration,
  SAMSUNG,
  TODAY,
} from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('KIS DomesticBasicQuote', () => {
  it('getStockCurrentPrice', async () => {
    const client = await getKisClient();
    const res = await (client.domesticBasicQuote as any).getStockCurrentPrice({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
  });

  it('getStockCurrentPrice2', async () => {
    const client = await getKisClient();
    const res = await (client.domesticBasicQuote as any).getStockCurrentPrice2({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
  });

  it('getStockCurrentPriceConclusion', async () => {
    const client = await getKisClient();
    const res = await (client.domesticBasicQuote as any).getStockCurrentPriceConclusion({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
  });

  it('getStockCurrentPriceDaily', async () => {
    const client = await getKisClient();
    const res = await (client.domesticBasicQuote as any).getStockCurrentPriceDaily({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
      fidPeriodDivCode: 'D',
      fidOrgAdjPrc: '0',
    });
    assertKisResponse(res);
  });

  it('getStockCurrentPriceAskingExpectedConclusion', async () => {
    const client = await getKisClient();
    const res = await (client.domesticBasicQuote as any).getStockCurrentPriceAskingExpectedConclusion({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
  });

  it('getStockCurrentPriceInvestor', async () => {
    const client = await getKisClient();
    const res = await (client.domesticBasicQuote as any).getStockCurrentPriceInvestor({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
  });

  it('getStockCurrentPriceMember', async () => {
    const client = await getKisClient();
    const res = await (client.domesticBasicQuote as any).getStockCurrentPriceMember({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
  });

  it('getStockPeriodQuote', async () => {
    const client = await getKisClient();
    const res = await (client.domesticBasicQuote as any).getStockPeriodQuote({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
      fidInputDate1: ONE_MONTH_AGO,
      fidInputDate2: TODAY,
      fidPeriodDivCode: 'D',
      fidOrgAdjPrc: '0',
    });
    assertKisResponse(res);
  });

  it('getStockTodayMinuteChart', async () => {
    const client = await getKisClient();
    const res = await (client.domesticBasicQuote as any).getStockTodayMinuteChart({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
      fidInputHour1: '155000',
      fidPwDataIncuYn: 'Y',
      fidEtcClsCode: '',
    });
    assertKisResponse(res);
  });

  it('getStockDailyMinuteChart', async () => {
    const client = await getKisClient();
    const res = await (client.domesticBasicQuote as any).getStockDailyMinuteChart({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
      fidInputHour1: '155000',
      fidInputDate1: TODAY,
      fidPwDataIncuYn: 'Y',
    });
    assertKisResponse(res);
  });

  it('getStockCurrentPriceTimeItemConclusion', async () => {
    const client = await getKisClient();
    const res = await (client.domesticBasicQuote as any).getStockCurrentPriceTimeItemConclusion({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
      fidInputHour1: '155000',
    });
    assertKisResponse(res);
  });

  it('getStockCurrentPriceDailyOvertimePrice', async () => {
    const client = await getKisClient();
    const res = await (client.domesticBasicQuote as any).getStockCurrentPriceDailyOvertimePrice({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
  });

  it('getStockCurrentPriceOvertimeConclusion', async () => {
    const client = await getKisClient();
    const res = await (client.domesticBasicQuote as any).getStockCurrentPriceOvertimeConclusion({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
  });

  it('getStockOvertimeCurrentPrice', async () => {
    const client = await getKisClient();
    const res = await (client.domesticBasicQuote as any).getStockOvertimeCurrentPrice({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
  });

  it('getStockOvertimeAskingPrice', async () => {
    const client = await getKisClient();
    const res = await (client.domesticBasicQuote as any).getStockOvertimeAskingPrice({
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
  });

  it('getStockClosingExpectedPrice', async () => {
    const client = await getKisClient();
    const res = await (client.domesticBasicQuote as any).getStockClosingExpectedPrice({
      fidRankSortClsCode: '0',
      fidInputIscd: SAMSUNG,
      fidBlngClsCode: '0',
    });
    assertKisResponse(res);
  });

  it('getEtfetnCurrentPrice', async () => {
    const client = await getKisClient();
    const res = await (client.domesticBasicQuote as any).getEtfetnCurrentPrice({
      fidInputIscd: KODEX200,
    });
    assertKisResponse(res);
  });

  it('getEtfComponentStockPrice', async () => {
    const client = await getKisClient();
    const res = await (client.domesticBasicQuote as any).getEtfComponentStockPrice({
      fidInputIscd: KODEX200,
    });
    assertKisResponse(res);
  });

  it('getEtfNavComparisonTrend', async () => {
    const client = await getKisClient();
    const res = await (client.domesticBasicQuote as any).getEtfNavComparisonTrend({
      fidInputIscd: KODEX200,
    });
    assertKisResponse(res);
  });

  it('getEtfNavComparisonDailyTrend', async () => {
    const client = await getKisClient();
    const res = await (client.domesticBasicQuote as any).getEtfNavComparisonDailyTrend({
      fidInputIscd: KODEX200,
      fidInputDate1: ONE_MONTH_AGO,
      fidInputDate2: TODAY,
    });
    assertKisResponse(res);
  });

  it('getEtfNavComparisonTimeTrend', async () => {
    const client = await getKisClient();
    const res = await (client.domesticBasicQuote as any).getEtfNavComparisonTimeTrend({
      fidHourClsCode: '0',
      fidInputIscd: KODEX200,
    });
    assertKisResponse(res);
  });
});
