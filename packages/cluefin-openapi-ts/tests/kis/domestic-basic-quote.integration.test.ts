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
import { assertKisResponseShapeDeep } from '../_helpers/kis-response-shape';

const it = runIntegration ? test : test.skip;

// 실서버는 값이 없는 조건부 필드(경고·관리·락 구분 등)의 키를 아예 생략한다 — VENDOR_DOC_ERRATA.md KIS
const CURRENT_PRICE_OMITTED = [
  'output.new_hgpr_lwpr_cls_code',
  'output.mxpr_llam_cls_code',
  'output.flng_cls_name',
  'output.revl_issu_reas_name',
  'output.mrkt_warn_cls_name',
  'output.fcam_mod_cls_name',
];

// 실서버는 값이 없는 조건부 필드(경고·관리·락 구분 등)의 키를 아예 생략한다 — VENDOR_DOC_ERRATA.md KIS
const OVERTIME_PRICE_OMITTED = [
  'output.mang_issu_cls_name',
  'output.mrkt_warn_cls_name',
  'output.revl_issu_reas_name',
  'output.flng_cls_name',
];

// 문서는 시간외 단일가 호가 증감을 10단계로 적지만 실서버는 3단계까지만 보낸다 — VENDOR_DOC_ERRATA.md KIS
const OVERTIME_ASKING_OMITTED = [
  'output.ovtm_untp_askp_icdc4',
  'output.ovtm_untp_askp_icdc5',
  'output.ovtm_untp_askp_icdc6',
  'output.ovtm_untp_askp_icdc7',
  'output.ovtm_untp_askp_icdc8',
  'output.ovtm_untp_askp_icdc9',
  'output.ovtm_untp_askp_icdc10',
  'output.ovtm_untp_bidp_icdc4',
  'output.ovtm_untp_bidp_icdc5',
  'output.ovtm_untp_bidp_icdc6',
  'output.ovtm_untp_bidp_icdc7',
  'output.ovtm_untp_bidp_icdc8',
  'output.ovtm_untp_bidp_icdc9',
  'output.ovtm_untp_bidp_icdc10',
];

// 스키마가 문서 키와 실서버 키('itewhol_loan_rmnd_ratem name')를 둘 다 받으므로 한쪽은 항상 없다
const PERIOD_QUOTE_ALIAS = ['output1.itewhol_loan_rmnd_ratem'];

describe('KIS DomesticBasicQuote', () => {
  it('getStockCurrentPrice', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getStockCurrentPrice({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getStockCurrentPriceResponseSchema, CURRENT_PRICE_OMITTED);
  });

  it('getStockCurrentPrice2', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getStockCurrentPrice2({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getStockCurrentPrice2ResponseSchema, CURRENT_PRICE_OMITTED);
  });

  it('getStockCurrentPriceConclusion', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getStockCurrentPriceConclusion({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getStockCurrentPriceConclusionResponseSchema);
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
    assertKisResponseShapeDeep(res.body, getStockCurrentPriceDailyResponseSchema);
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
    assertKisResponseShapeDeep(res.body, getStockCurrentPriceAskingExpectedConclusionResponseSchema);
  });

  it('getStockCurrentPriceInvestor', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getStockCurrentPriceInvestor({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getStockCurrentPriceInvestorResponseSchema);
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
    assertKisResponseShapeDeep(res.body, getStockCurrentPriceMemberResponseSchema);
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
    assertKisResponseShapeDeep(res.body, getStockPeriodQuoteResponseSchema, PERIOD_QUOTE_ALIAS);
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
    assertKisResponseShapeDeep(res.body, getStockTodayMinuteChartResponseSchema);
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
    assertKisResponseShapeDeep(res.body, getStockDailyMinuteChartResponseSchema);
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
    assertKisResponseShapeDeep(res.body, getStockCurrentPriceTimeItemConclusionResponseSchema);
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
    assertKisResponseShapeDeep(res.body, getStockCurrentPriceDailyOvertimePriceResponseSchema);
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
      fidHourClsCode: '1',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getStockCurrentPriceOvertimeConclusionResponseSchema);
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
    assertKisResponseShapeDeep(res.body, getStockOvertimeCurrentPriceResponseSchema, OVERTIME_PRICE_OMITTED);
  });

  it('getStockOvertimeAskingPrice', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getStockOvertimeAskingPrice({
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getStockOvertimeAskingPriceResponseSchema, OVERTIME_ASKING_OMITTED);
  });

  it('getStockClosingExpectedPrice', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getStockClosingExpectedPrice({
      fidRankSortClsCode: '0',
      fidInputIscd: SAMSUNG,
      fidBlngClsCode: '0',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getStockClosingExpectedPriceResponseSchema);
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
    assertKisResponseShapeDeep(res.body, getEtfetnCurrentPriceResponseSchema);
  });

  it('getEtfComponentStockPrice', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getEtfComponentStockPrice({
      fidInputIscd: KODEX200,
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getEtfComponentStockPriceResponseSchema);
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
    assertKisResponseShapeDeep(res.body, getEtfNavComparisonTrendResponseSchema);
  });

  it('getEtfNavComparisonDailyTrend', async () => {
    const client = await getKisClient();
    const res = await client.domesticBasicQuote.getEtfNavComparisonDailyTrend({
      fidInputIscd: KODEX200,
      fidInputDate1: ONE_MONTH_AGO,
      fidInputDate2: TODAY,
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getEtfNavComparisonDailyTrendResponseSchema);
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
    assertKisResponseShapeDeep(res.body, getEtfNavComparisonTimeTrendResponseSchema);
    assertResponseShape(
      res.body,
      getEtfNavComparisonTimeTrendResponseSchema,
      'output',
      getEtfNavComparisonTimeTrendItemSchema,
    );
  });
});
