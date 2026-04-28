import { describe, expect, test } from 'vitest';
import {
  getExpectedIndexAllOutput2ItemSchema,
  getExpectedIndexAllResponseSchema,
  getExpectedIndexTrendItemSchema,
  getExpectedIndexTrendResponseSchema,
  getFuturesBusinessDayInquiryItemSchema,
  getFuturesBusinessDayInquiryResponseSchema,
  getHolidayInquiryItemSchema,
  getHolidayInquiryResponseSchema,
  getInterestRateSummaryOutput1ItemSchema,
  getInterestRateSummaryOutput2ItemSchema,
  getInterestRateSummaryResponseSchema,
  getMarketAnnouncementScheduleItemSchema,
  getMarketAnnouncementScheduleResponseSchema,
  getSectorAllQuoteByCategoryOutput2ItemSchema,
  getSectorAllQuoteByCategoryResponseSchema,
  getSectorCurrentIndexResponseSchema,
  getSectorDailyIndexOutput2ItemSchema,
  getSectorDailyIndexResponseSchema,
  getSectorMinuteInquiryOutput2ItemSchema,
  getSectorMinuteInquiryResponseSchema,
  getSectorPeriodQuoteOutput2ItemSchema,
  getSectorPeriodQuoteResponseSchema,
  getSectorTimeIndexMinuteItemSchema,
  getSectorTimeIndexMinuteResponseSchema,
  getSectorTimeIndexSecondItemSchema,
  getSectorTimeIndexSecondResponseSchema,
  getVolatilityInterruptionStatusItemSchema,
  getVolatilityInterruptionStatusResponseSchema,
} from '../../src/kis/schemas/domestic-issue-other';
import {
  assertKisResponse,
  assertResponseShape,
  getKisClient,
  ONE_MONTH_AGO,
  runIntegration,
  TODAY,
} from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('KIS DomesticIssueOther', () => {
  it('getSectorCurrentIndex', async () => {
    const client = await getKisClient();
    const res = await client.domesticIssueOther.getSectorCurrentIndex({
      fidCondMrktDivCode: 'U',
      fidInputIscd: '0001',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getSectorCurrentIndexResponseSchema);
  });

  it('getSectorDailyIndex', async () => {
    const client = await getKisClient();
    const res = await client.domesticIssueOther.getSectorDailyIndex({
      fidPeriodDivCode: 'D',
      fidCondMrktDivCode: 'U',
      fidInputIscd: '0001',
      fidInputDate1: ONE_MONTH_AGO,
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getSectorDailyIndexResponseSchema);
    assertResponseShape(res.body, getSectorDailyIndexResponseSchema, 'output2', getSectorDailyIndexOutput2ItemSchema);
  });

  it('getSectorTimeIndexSecond', async () => {
    const client = await getKisClient();
    const res = await client.domesticIssueOther.getSectorTimeIndexSecond({
      fidInputIscd: '0001',
      fidCondMrktDivCode: 'U',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getSectorTimeIndexSecondResponseSchema, 'output', getSectorTimeIndexSecondItemSchema);
  });

  it('getSectorTimeIndexMinute', async () => {
    const client = await getKisClient();
    const res = await client.domesticIssueOther.getSectorTimeIndexMinute({
      fidInputHour1: '155000',
      fidInputIscd: '0001',
      fidCondMrktDivCode: 'U',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getSectorTimeIndexMinuteResponseSchema, 'output', getSectorTimeIndexMinuteItemSchema);
  });

  it('getSectorMinuteInquiry', async () => {
    const client = await getKisClient();
    const res = await client.domesticIssueOther.getSectorMinuteInquiry({
      fidCondMrktDivCode: 'U',
      fidEtcClsCode: '',
      fidInputIscd: '0001',
      fidInputHour1: '155000',
      fidPwDataIncuYn: 'Y',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getSectorMinuteInquiryResponseSchema);
    assertResponseShape(
      res.body,
      getSectorMinuteInquiryResponseSchema,
      'output2',
      getSectorMinuteInquiryOutput2ItemSchema,
    );
  });

  it('getSectorPeriodQuote', async () => {
    const client = await getKisClient();
    const res = await client.domesticIssueOther.getSectorPeriodQuote({
      fidCondMrktDivCode: 'U',
      fidInputIscd: '0001',
      fidInputDate1: ONE_MONTH_AGO,
      fidInputDate2: TODAY,
      fidPeriodDivCode: 'D',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getSectorPeriodQuoteResponseSchema);
    assertResponseShape(res.body, getSectorPeriodQuoteResponseSchema, 'output2', getSectorPeriodQuoteOutput2ItemSchema);
  });

  it('getSectorAllQuoteByCategory', async () => {
    const client = await getKisClient();
    const res = await client.domesticIssueOther.getSectorAllQuoteByCategory({
      fidCondMrktDivCode: 'U',
      fidInputIscd: '0001',
      fidCondScrDivCode: '20214',
      fidMrktClsCode: '0',
      fidBlngClsCode: '0',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getSectorAllQuoteByCategoryResponseSchema);
    assertResponseShape(
      res.body,
      getSectorAllQuoteByCategoryResponseSchema,
      'output2',
      getSectorAllQuoteByCategoryOutput2ItemSchema,
    );
  });

  it('getExpectedIndexTrend', async () => {
    const client = await getKisClient();
    const res = await client.domesticIssueOther.getExpectedIndexTrend({
      fidMkopClsCode: '0',
      fidInputHour1: '155000',
      fidInputIscd: '0001',
      fidCondMrktDivCode: 'U',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getExpectedIndexTrendResponseSchema, 'output', getExpectedIndexTrendItemSchema);
  });

  it('getExpectedIndexAll', async () => {
    const client = await getKisClient();
    const res = await client.domesticIssueOther.getExpectedIndexAll({
      fidMrktClsCode: '0',
      fidCondMrktDivCode: 'U',
      fidCondScrDivCode: '11175',
      fidInputIscd: '0001',
      fidMkopClsCode: '0',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getExpectedIndexAllResponseSchema);
    assertResponseShape(res.body, getExpectedIndexAllResponseSchema, 'output2', getExpectedIndexAllOutput2ItemSchema);
  });

  it('getVolatilityInterruptionStatus', async () => {
    const client = await getKisClient();
    const res = await client.domesticIssueOther.getVolatilityInterruptionStatus({
      fidDivClsCode: '0',
      fidCondScrDivCode: '20139',
      fidMrktClsCode: '0',
      fidInputIscd: '0000',
      fidRankSortClsCode: '0',
      fidInputDate1: TODAY,
      fidTrgtClsCode: '0',
      fidTrgtExlsClsCode: '0',
    });
    assertKisResponse(res);
    assertResponseShape(
      res.body,
      getVolatilityInterruptionStatusResponseSchema,
      'output',
      getVolatilityInterruptionStatusItemSchema,
    );
  });

  it('getInterestRateSummary', async () => {
    const client = await getKisClient();
    const res = await client.domesticIssueOther.getInterestRateSummary({
      fidCondMrktDivCode: 'I',
      fidCondScrDivCode: '20702',
      fidDivClsCode: '1',
      fidDivClsCode1: '',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getInterestRateSummaryResponseSchema);
    assertResponseShape(
      res.body,
      getInterestRateSummaryResponseSchema,
      'output1',
      getInterestRateSummaryOutput1ItemSchema,
    );
    expect(getInterestRateSummaryOutput2ItemSchema.parse({}).stck_bsop_date).toBe('');
    if (res.body.output2.length > 0) {
      expect(Object.keys(res.body.output2[0]).sort()).toEqual(
        expect.arrayContaining([
          'bcdtCode',
          'htsKorIsnm',
          'bondMnrtPrpr',
          'prdyVrssSign',
          'bondMnrtPrdyVrss',
          'bstpNmixPrdyCtrt',
        ]),
      );
    }
  });

  it('getMarketAnnouncementSchedule', async () => {
    const client = await getKisClient();
    const res = await client.domesticIssueOther.getMarketAnnouncementSchedule({
      fidNewsOferEntpCode: '',
      fidCondMrktClsCode: '0',
      fidInputIscd: '0000',
      fidTitlCntt: '',
      fidInputDate1: TODAY,
      fidInputHour1: '000000',
      fidRankSortClsCode: '0',
      fidInputSrno: '',
    });
    assertKisResponse(res);
    assertResponseShape(
      res.body,
      getMarketAnnouncementScheduleResponseSchema,
      'output',
      getMarketAnnouncementScheduleItemSchema,
    );
  });

  it('getHolidayInquiry', async () => {
    const client = await getKisClient();
    const res = await client.domesticIssueOther.getHolidayInquiry({
      bassDt: TODAY,
      ctxAreaNk: '',
      ctxAreaFk: '',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getHolidayInquiryResponseSchema, 'output', getHolidayInquiryItemSchema);
  });

  it('getFuturesBusinessDayInquiry', async () => {
    const client = await getKisClient();
    const res = await client.domesticIssueOther.getFuturesBusinessDayInquiry({});
    assertKisResponse(res);
    assertResponseShape(
      res.body,
      getFuturesBusinessDayInquiryResponseSchema,
      'output1',
      getFuturesBusinessDayInquiryItemSchema,
    );
  });
});
