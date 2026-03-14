import { describe, test } from 'vitest';
import {
  getEtfComponentStockPriceOutput2ItemSchema,
  getEtfComponentStockPriceResponseSchema,
  getEtfetnCurrentPriceResponseSchema,
  getEtfNavComparisonDailyTrendItemSchema,
  getEtfNavComparisonDailyTrendResponseSchema,
  getEtfNavComparisonTimeTrendItemSchema,
  getEtfNavComparisonTimeTrendResponseSchema,
  getEtfNavComparisonTrendResponseSchema,
  getStockClosingExpectedPriceItemSchema,
  getStockClosingExpectedPriceResponseSchema,
  getStockCurrentPrice2ResponseSchema,
  getStockCurrentPriceAskingExpectedConclusionResponseSchema,
  getStockCurrentPriceConclusionItemSchema,
  getStockCurrentPriceConclusionResponseSchema,
  getStockCurrentPriceDailyItemSchema,
  getStockCurrentPriceDailyOvertimePriceOutput2ItemSchema,
  getStockCurrentPriceDailyOvertimePriceResponseSchema,
  getStockCurrentPriceDailyResponseSchema,
  getStockCurrentPriceInvestorItemSchema,
  getStockCurrentPriceInvestorResponseSchema,
  getStockCurrentPriceMemberItemSchema,
  getStockCurrentPriceMemberResponseSchema,
  getStockCurrentPriceOvertimeConclusionOutput2ItemSchema,
  getStockCurrentPriceOvertimeConclusionResponseSchema,
  getStockCurrentPriceResponseSchema,
  getStockCurrentPriceTimeItemConclusionOutput2ItemSchema,
  getStockCurrentPriceTimeItemConclusionResponseSchema,
  getStockDailyMinuteChartOutput2ItemSchema,
  getStockDailyMinuteChartResponseSchema,
  getStockOvertimeAskingPriceResponseSchema,
  getStockOvertimeCurrentPriceResponseSchema,
  getStockPeriodQuoteOutput2ItemSchema,
  getStockPeriodQuoteResponseSchema,
  getStockTodayMinuteChartOutput2ItemSchema,
  getStockTodayMinuteChartResponseSchema,
} from '../../src/kis/schemas/domestic-basic-quote';
import {
  assertKisResponse,
  assertResponseShape,
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
    const res = await client.domesticBasicQuote.getStockCurrentPrice({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockCurrentPriceResponseSchema);
  });

  it('getStockCurrentPrice2', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getStockCurrentPrice2({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockCurrentPrice2ResponseSchema);
  });

  it('getStockCurrentPriceConclusion', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getStockCurrentPriceConclusion({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
    assertResponseShape(
      res.body,
      getStockCurrentPriceConclusionResponseSchema,
      'output',
      getStockCurrentPriceConclusionItemSchema,
    );
  });

  it('getStockCurrentPriceDaily', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getStockCurrentPriceDaily({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
      fidPeriodDivCode: 'D',
      fidOrgAdjPrc: '0',
    });
    assertKisResponse(res);
    assertResponseShape(
      res.body,
      getStockCurrentPriceDailyResponseSchema,
      'output',
      getStockCurrentPriceDailyItemSchema,
    );
  });

  it('getStockCurrentPriceAskingExpectedConclusion', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getStockCurrentPriceAskingExpectedConclusion({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockCurrentPriceAskingExpectedConclusionResponseSchema);
  });

  it('getStockCurrentPriceInvestor', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getStockCurrentPriceInvestor({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
    assertResponseShape(
      res.body,
      getStockCurrentPriceInvestorResponseSchema,
      'output',
      getStockCurrentPriceInvestorItemSchema,
    );
  });

  it('getStockCurrentPriceMember', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getStockCurrentPriceMember({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
    assertResponseShape(
      res.body,
      getStockCurrentPriceMemberResponseSchema,
      'output',
      getStockCurrentPriceMemberItemSchema,
    );
  });

  it('getStockPeriodQuote', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getStockPeriodQuote({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
      fidInputDate1: ONE_MONTH_AGO,
      fidInputDate2: TODAY,
      fidPeriodDivCode: 'D',
      fidOrgAdjPrc: '0',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockPeriodQuoteResponseSchema);
    assertResponseShape(res.body, getStockPeriodQuoteResponseSchema, 'output2', getStockPeriodQuoteOutput2ItemSchema);
  });

  it('getStockTodayMinuteChart', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getStockTodayMinuteChart({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
      fidInputHour1: '155000',
      fidPwDataIncuYn: 'Y',
      fidEtcClsCode: '',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockTodayMinuteChartResponseSchema);
    assertResponseShape(
      res.body,
      getStockTodayMinuteChartResponseSchema,
      'output2',
      getStockTodayMinuteChartOutput2ItemSchema,
    );
  });

  it('getStockDailyMinuteChart', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getStockDailyMinuteChart({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
      fidInputHour1: '155000',
      fidInputDate1: TODAY,
      fidPwDataIncuYn: 'Y',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockDailyMinuteChartResponseSchema);
    assertResponseShape(
      res.body,
      getStockDailyMinuteChartResponseSchema,
      'output2',
      getStockDailyMinuteChartOutput2ItemSchema,
    );
  });

  it('getStockCurrentPriceTimeItemConclusion', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getStockCurrentPriceTimeItemConclusion({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
      fidInputHour1: '155000',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockCurrentPriceTimeItemConclusionResponseSchema);
    assertResponseShape(
      res.body,
      getStockCurrentPriceTimeItemConclusionResponseSchema,
      'output2',
      getStockCurrentPriceTimeItemConclusionOutput2ItemSchema,
    );
  });

  it('getStockCurrentPriceDailyOvertimePrice', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getStockCurrentPriceDailyOvertimePrice({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockCurrentPriceDailyOvertimePriceResponseSchema);
    assertResponseShape(
      res.body,
      getStockCurrentPriceDailyOvertimePriceResponseSchema,
      'output2',
      getStockCurrentPriceDailyOvertimePriceOutput2ItemSchema,
    );
  });

  it('getStockCurrentPriceOvertimeConclusion', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getStockCurrentPriceOvertimeConclusion({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockCurrentPriceOvertimeConclusionResponseSchema);
    assertResponseShape(
      res.body,
      getStockCurrentPriceOvertimeConclusionResponseSchema,
      'output2',
      getStockCurrentPriceOvertimeConclusionOutput2ItemSchema,
    );
  });

  it('getStockOvertimeCurrentPrice', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getStockOvertimeCurrentPrice({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockOvertimeCurrentPriceResponseSchema);
  });

  it('getStockOvertimeAskingPrice', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getStockOvertimeAskingPrice({
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockOvertimeAskingPriceResponseSchema);
  });

  it('getStockClosingExpectedPrice', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getStockClosingExpectedPrice({
      fidRankSortClsCode: '0',
      fidInputIscd: SAMSUNG,
      fidBlngClsCode: '0',
    });
    assertKisResponse(res);
    assertResponseShape(
      res.body,
      getStockClosingExpectedPriceResponseSchema,
      'output',
      getStockClosingExpectedPriceItemSchema,
    );
  });

  it('getEtfetnCurrentPrice', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getEtfetnCurrentPrice({
      fidInputIscd: KODEX200,
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getEtfetnCurrentPriceResponseSchema);
  });

  it('getEtfComponentStockPrice', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getEtfComponentStockPrice({
      fidInputIscd: KODEX200,
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getEtfComponentStockPriceResponseSchema);
    assertResponseShape(
      res.body,
      getEtfComponentStockPriceResponseSchema,
      'output2',
      getEtfComponentStockPriceOutput2ItemSchema,
    );
  });

  it('getEtfNavComparisonTrend', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getEtfNavComparisonTrend({
      fidInputIscd: KODEX200,
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getEtfNavComparisonTrendResponseSchema);
  });

  it('getEtfNavComparisonDailyTrend', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getEtfNavComparisonDailyTrend({
      fidInputIscd: KODEX200,
      fidInputDate1: ONE_MONTH_AGO,
      fidInputDate2: TODAY,
    });
    assertKisResponse(res);
    assertResponseShape(
      res.body,
      getEtfNavComparisonDailyTrendResponseSchema,
      'output',
      getEtfNavComparisonDailyTrendItemSchema,
    );
  });

  it('getEtfNavComparisonTimeTrend', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getEtfNavComparisonTimeTrend({
      fidHourClsCode: '0',
      fidInputIscd: KODEX200,
    });
    assertKisResponse(res);
    assertResponseShape(
      res.body,
      getEtfNavComparisonTimeTrendResponseSchema,
      'output',
      getEtfNavComparisonTimeTrendItemSchema,
    );
  });
});
