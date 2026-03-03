import { describe, test } from 'vitest';

import { assertKisResponse, getKisClient, ONE_MONTH_AGO, runIntegration, TODAY } from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('KIS DomesticIssueOther', () => {
  it('getSectorCurrentIndex', async () => {
    const client = await getKisClient();
    const res = await client.domesticIssueOther.getSectorCurrentIndex({
      fidCondMrktDivCode: 'U',
      fidInputIscd: '0001',
    });
    assertKisResponse(res);
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
  });

  it('getSectorTimeIndexSecond', async () => {
    const client = await getKisClient();
    const res = await client.domesticIssueOther.getSectorTimeIndexSecond({
      fidInputIscd: '0001',
      fidCondMrktDivCode: 'U',
    });
    assertKisResponse(res);
  });

  it('getSectorTimeIndexMinute', async () => {
    const client = await getKisClient();
    const res = await client.domesticIssueOther.getSectorTimeIndexMinute({
      fidInputHour1: '155000',
      fidInputIscd: '0001',
      fidCondMrktDivCode: 'U',
    });
    assertKisResponse(res);
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
  });

  it('getInterestRateSummary', async () => {
    const client = await getKisClient();
    const res = await client.domesticIssueOther.getInterestRateSummary({
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '10702',
      fidDivClsCode: '0',
      fidDivClsCode1: '0',
    });
    assertKisResponse(res);
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
  });

  it('getHolidayInquiry', async () => {
    const client = await getKisClient();
    const res = await client.domesticIssueOther.getHolidayInquiry({
      bassDt: TODAY,
      ctxAreaNk: '',
      ctxAreaFk: '',
    });
    assertKisResponse(res);
  });

  it('getFuturesBusinessDayInquiry', async () => {
    const client = await getKisClient();
    const res = await client.domesticIssueOther.getFuturesBusinessDayInquiry({});
    assertKisResponse(res);
  });
});
