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
import { assertKisResponseShapeDeep } from '../_helpers/kis-response-shape';

const it = runIntegration ? test : test.skip;

// 2026-09-27(일) 응답에 없었다. 휴장일이라 빠진 것인지 평일에 재확인 — kis-spec-audit-pending-live.md
const EXPECTED_INDEX_ALL_UNVERIFIED = ['output1.bstp_cls_code'];

describe('KIS DomesticIssueOther', () => {
  it('getSectorCurrentIndex', async () => {
    const client = await getKisClient();
    const res = await client.domesticIssueOther.getSectorCurrentIndex({
      fidCondMrktDivCode: 'U',
      fidInputIscd: '0001',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getSectorCurrentIndexResponseSchema);
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
    assertKisResponseShapeDeep(res.body, getSectorDailyIndexResponseSchema);
    assertResponseShape(res.body, getSectorDailyIndexResponseSchema, 'output2', getSectorDailyIndexOutput2ItemSchema);
  });

  it('getSectorTimeIndexSecond', async () => {
    const client = await getKisClient();
    const res = await client.domesticIssueOther.getSectorTimeIndexSecond({
      fidInputIscd: '0001',
      fidCondMrktDivCode: 'U',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getSectorTimeIndexSecondResponseSchema);
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
    assertKisResponseShapeDeep(res.body, getSectorTimeIndexMinuteResponseSchema);
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
    assertKisResponseShapeDeep(res.body, getSectorMinuteInquiryResponseSchema);
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
    assertKisResponseShapeDeep(res.body, getSectorPeriodQuoteResponseSchema);
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
    assertKisResponseShapeDeep(res.body, getSectorAllQuoteByCategoryResponseSchema);
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
    assertKisResponseShapeDeep(res.body, getExpectedIndexTrendResponseSchema);
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
    assertKisResponseShapeDeep(res.body, getExpectedIndexAllResponseSchema, EXPECTED_INDEX_ALL_UNVERIFIED);
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
    assertKisResponseShapeDeep(res.body, getVolatilityInterruptionStatusResponseSchema);
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
    assertKisResponseShapeDeep(res.body, getInterestRateSummaryResponseSchema);
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
      // 스펙: 전부 "공백 필수" 이거나 공백=현재기준. 날짜·시간을 채우면 형식(00YYYYMMDD)이 달라 빈 결과가 온다
      fidNewsOferEntpCode: '',
      fidCondMrktClsCode: '',
      fidInputIscd: '',
      fidTitlCntt: '',
      fidInputDate1: '',
      fidInputHour1: '',
      fidRankSortClsCode: '',
      fidInputSrno: '',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getMarketAnnouncementScheduleResponseSchema);
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
    assertKisResponseShapeDeep(res.body, getHolidayInquiryResponseSchema);
    assertResponseShape(res.body, getHolidayInquiryResponseSchema, 'output', getHolidayInquiryItemSchema);
  });

  it('getFuturesBusinessDayInquiry', async () => {
    const client = await getKisClient();
    const res = await client.domesticIssueOther.getFuturesBusinessDayInquiry({});
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getFuturesBusinessDayInquiryResponseSchema);
    assertResponseShape(
      res.body,
      getFuturesBusinessDayInquiryResponseSchema,
      'output1',
      getFuturesBusinessDayInquiryItemSchema,
    );
  });
});
