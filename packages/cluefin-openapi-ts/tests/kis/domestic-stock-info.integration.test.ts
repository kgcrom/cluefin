import { describe, test } from 'vitest';
import {
  getBalanceSheetItemSchema,
  getBalanceSheetResponseSchema,
  getEstimatedEarningsOutput2ItemSchema,
  getEstimatedEarningsOutput3ItemSchema,
  getEstimatedEarningsOutput4ItemSchema,
  getEstimatedEarningsResponseSchema,
  getFinancialRatioItemSchema,
  getFinancialRatioResponseSchema,
  getGrowthRatioItemSchema,
  getGrowthRatioResponseSchema,
  getIncomeStatementItemSchema,
  getIncomeStatementResponseSchema,
  getInvestmentOpinionByBrokerageItemSchema,
  getInvestmentOpinionByBrokerageResponseSchema,
  getInvestmentOpinionItemSchema,
  getInvestmentOpinionResponseSchema,
  getKsdCapitalReductionScheduleItemSchema,
  getKsdCapitalReductionScheduleResponseSchema,
  getKsdDepositScheduleItemSchema,
  getKsdDepositScheduleResponseSchema,
  getKsdDividendDecisionItemSchema,
  getKsdDividendDecisionResponseSchema,
  getKsdForfeitedShareScheduleItemSchema,
  getKsdForfeitedShareScheduleResponseSchema,
  getKsdIpoSubscriptionScheduleItemSchema,
  getKsdIpoSubscriptionScheduleResponseSchema,
  getKsdListingInfoScheduleItemSchema,
  getKsdListingInfoScheduleResponseSchema,
  getKsdMergerSplitDecisionItemSchema,
  getKsdMergerSplitDecisionResponseSchema,
  getKsdPaidInCapitalIncreaseScheduleItemSchema,
  getKsdPaidInCapitalIncreaseScheduleResponseSchema,
  getKsdParValueChangeDecisionItemSchema,
  getKsdParValueChangeDecisionResponseSchema,
  getKsdShareholderMeetingScheduleItemSchema,
  getKsdShareholderMeetingScheduleResponseSchema,
  getKsdStockDividendDecisionItemSchema,
  getKsdStockDividendDecisionResponseSchema,
  getKsdStockDividendScheduleItemSchema,
  getKsdStockDividendScheduleResponseSchema,
  getMarginTradableStocksItemSchema,
  getMarginTradableStocksResponseSchema,
  getOtherKeyRatioItemSchema,
  getOtherKeyRatioResponseSchema,
  getProductBasicInfoResponseSchema,
  getProfitabilityRatioItemSchema,
  getProfitabilityRatioResponseSchema,
  getStabilityRatioItemSchema,
  getStabilityRatioResponseSchema,
  getStockBasicInfoResponseSchema,
  getStockLoanableListOutput1ItemSchema,
  getStockLoanableListResponseSchema,
} from '../../src/kis/schemas/domestic-stock-info';
import {
  assertKisResponse,
  assertResponseShape,
  getKisClient,
  ONE_MONTH_AGO,
  runIntegration,
  SAMSUNG,
  TODAY,
} from '../_helpers/integration-setup';
import { assertKisResponseShapeDeep } from '../_helpers/kis-response-shape';

const it = runIntegration ? test : test.skip;

describe('KIS DomesticStockInfo', () => {
  it('getProductBasicInfo', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getProductBasicInfo({
      pdno: SAMSUNG,
      prdtTypeCd: '300',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getProductBasicInfoResponseSchema);
  });

  it('getStockBasicInfo', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getStockBasicInfo({
      prdtTypeCd: '300',
      pdno: SAMSUNG,
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getStockBasicInfoResponseSchema);
  });

  it('getBalanceSheet', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getBalanceSheet({
      fidDivClsCode: '0',
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getBalanceSheetResponseSchema);
    assertResponseShape(res.body, getBalanceSheetResponseSchema, 'output', getBalanceSheetItemSchema);
  });

  it('getIncomeStatement', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getIncomeStatement({
      fidDivClsCode: '0',
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getIncomeStatementResponseSchema);
    assertResponseShape(res.body, getIncomeStatementResponseSchema, 'output', getIncomeStatementItemSchema);
  });

  it('getFinancialRatio', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getFinancialRatio({
      fidDivClsCode: '0',
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getFinancialRatioResponseSchema);
    assertResponseShape(res.body, getFinancialRatioResponseSchema, 'output', getFinancialRatioItemSchema);
  });

  it('getProfitabilityRatio', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getProfitabilityRatio({
      fidInputIscd: SAMSUNG,
      fidDivClsCode: '0',
      fidCondMrktDivCode: 'J',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getProfitabilityRatioResponseSchema);
    assertResponseShape(res.body, getProfitabilityRatioResponseSchema, 'output', getProfitabilityRatioItemSchema);
  });

  it('getOtherKeyRatio', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getOtherKeyRatio({
      fidInputIscd: SAMSUNG,
      fidDivClsCode: '0',
      fidCondMrktDivCode: 'J',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getOtherKeyRatioResponseSchema);
    assertResponseShape(res.body, getOtherKeyRatioResponseSchema, 'output', getOtherKeyRatioItemSchema);
  });

  it('getStabilityRatio', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getStabilityRatio({
      fidInputIscd: SAMSUNG,
      fidDivClsCode: '0',
      fidCondMrktDivCode: 'J',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getStabilityRatioResponseSchema);
    assertResponseShape(res.body, getStabilityRatioResponseSchema, 'output', getStabilityRatioItemSchema);
  });

  it('getGrowthRatio', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getGrowthRatio({
      fidInputIscd: SAMSUNG,
      fidDivClsCode: '0',
      fidCondMrktDivCode: 'J',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getGrowthRatioResponseSchema);
    assertResponseShape(res.body, getGrowthRatioResponseSchema, 'output', getGrowthRatioItemSchema);
  });

  it('getMarginTradableStocks', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getMarginTradableStocks({
      fidRankSortClsCode: '0',
      fidSlctYn: 'N',
      fidInputIscd: SAMSUNG,
      fidCondScrDivCode: '20477',
      fidCondMrktDivCode: 'J',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getMarginTradableStocksResponseSchema);
    assertResponseShape(res.body, getMarginTradableStocksResponseSchema, 'output', getMarginTradableStocksItemSchema);
  });

  it('getKsdDividendDecision', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getKsdDividendDecision({
      cts: '',
      gb1: '0',
      fDt: ONE_MONTH_AGO,
      tDt: TODAY,
      shtCd: '',
      highGb: '0',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getKsdDividendDecisionResponseSchema);
    assertResponseShape(res.body, getKsdDividendDecisionResponseSchema, 'output1', getKsdDividendDecisionItemSchema);
  });

  it('getKsdStockDividendDecision', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getKsdStockDividendDecision({
      shtCd: '',
      tDt: TODAY,
      fDt: ONE_MONTH_AGO,
      cts: '',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getKsdStockDividendDecisionResponseSchema);
    assertResponseShape(
      res.body,
      getKsdStockDividendDecisionResponseSchema,
      'output1',
      getKsdStockDividendDecisionItemSchema,
    );
  });

  it('getKsdMergerSplitDecision', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getKsdMergerSplitDecision({
      cts: '',
      fDt: ONE_MONTH_AGO,
      tDt: TODAY,
      shtCd: '',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getKsdMergerSplitDecisionResponseSchema);
    assertResponseShape(
      res.body,
      getKsdMergerSplitDecisionResponseSchema,
      'output1',
      getKsdMergerSplitDecisionItemSchema,
    );
  });

  it('getKsdParValueChangeDecision', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getKsdParValueChangeDecision({
      shtCd: '',
      cts: '',
      fDt: ONE_MONTH_AGO,
      tDt: TODAY,
      marketGb: '0',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getKsdParValueChangeDecisionResponseSchema);
    assertResponseShape(
      res.body,
      getKsdParValueChangeDecisionResponseSchema,
      'output1',
      getKsdParValueChangeDecisionItemSchema,
    );
  });

  it('getKsdCapitalReductionSchedule', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getKsdCapitalReductionSchedule({
      cts: '',
      fDt: ONE_MONTH_AGO,
      tDt: TODAY,
      shtCd: '',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getKsdCapitalReductionScheduleResponseSchema);
    assertResponseShape(
      res.body,
      getKsdCapitalReductionScheduleResponseSchema,
      'output1',
      getKsdCapitalReductionScheduleItemSchema,
    );
  });

  it('getKsdListingInfoSchedule', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getKsdListingInfoSchedule({
      shtCd: '',
      tDt: TODAY,
      fDt: ONE_MONTH_AGO,
      cts: '',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getKsdListingInfoScheduleResponseSchema);
    assertResponseShape(
      res.body,
      getKsdListingInfoScheduleResponseSchema,
      'output1',
      getKsdListingInfoScheduleItemSchema,
    );
  });

  it('getKsdIpoSubscriptionSchedule', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getKsdIpoSubscriptionSchedule({
      shtCd: '',
      cts: '',
      fDt: ONE_MONTH_AGO,
      tDt: TODAY,
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getKsdIpoSubscriptionScheduleResponseSchema);
    assertResponseShape(
      res.body,
      getKsdIpoSubscriptionScheduleResponseSchema,
      'output1',
      getKsdIpoSubscriptionScheduleItemSchema,
    );
  });

  it('getKsdForfeitedShareSchedule', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getKsdForfeitedShareSchedule({
      shtCd: '',
      tDt: TODAY,
      fDt: ONE_MONTH_AGO,
      cts: '',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getKsdForfeitedShareScheduleResponseSchema);
    assertResponseShape(
      res.body,
      getKsdForfeitedShareScheduleResponseSchema,
      'output1',
      getKsdForfeitedShareScheduleItemSchema,
    );
  });

  it('getKsdDepositSchedule', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getKsdDepositSchedule({
      tDt: TODAY,
      shtCd: '',
      fDt: ONE_MONTH_AGO,
      cts: '',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getKsdDepositScheduleResponseSchema);
    assertResponseShape(res.body, getKsdDepositScheduleResponseSchema, 'output1', getKsdDepositScheduleItemSchema);
  });

  it('getKsdPaidInCapitalIncreaseSchedule', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getKsdPaidInCapitalIncreaseSchedule({
      cts: '',
      gb1: '0',
      fDt: ONE_MONTH_AGO,
      tDt: TODAY,
      shtCd: '',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getKsdPaidInCapitalIncreaseScheduleResponseSchema);
    assertResponseShape(
      res.body,
      getKsdPaidInCapitalIncreaseScheduleResponseSchema,
      'output1',
      getKsdPaidInCapitalIncreaseScheduleItemSchema,
    );
  });

  it('getKsdStockDividendSchedule', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getKsdStockDividendSchedule({
      cts: '',
      fDt: ONE_MONTH_AGO,
      tDt: TODAY,
      shtCd: '',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getKsdStockDividendScheduleResponseSchema);
    assertResponseShape(
      res.body,
      getKsdStockDividendScheduleResponseSchema,
      'output1',
      getKsdStockDividendScheduleItemSchema,
    );
  });

  it('getKsdShareholderMeetingSchedule', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getKsdShareholderMeetingSchedule({
      cts: '',
      fDt: ONE_MONTH_AGO,
      tDt: TODAY,
      shtCd: '',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getKsdShareholderMeetingScheduleResponseSchema);
    assertResponseShape(
      res.body,
      getKsdShareholderMeetingScheduleResponseSchema,
      'output1',
      getKsdShareholderMeetingScheduleItemSchema,
    );
  });

  it('getEstimatedEarnings', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getEstimatedEarnings({
      shtCd: SAMSUNG,
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getEstimatedEarningsResponseSchema);
    assertResponseShape(res.body, getEstimatedEarningsResponseSchema, 'output2', getEstimatedEarningsOutput2ItemSchema);
    assertResponseShape(res.body, getEstimatedEarningsResponseSchema, 'output3', getEstimatedEarningsOutput3ItemSchema);
    assertResponseShape(res.body, getEstimatedEarningsResponseSchema, 'output4', getEstimatedEarningsOutput4ItemSchema);
  });

  it('getStockLoanableList', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getStockLoanableList({
      excgDvsnCd: '01',
      pdno: SAMSUNG,
      thcoStlnPsblYn: '',
      inqrDvsn1: '0',
      ctxAreaFk200: '',
      ctxAreaNk100: '',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getStockLoanableListResponseSchema);
    assertResponseShape(res.body, getStockLoanableListResponseSchema, 'output1', getStockLoanableListOutput1ItemSchema);
  });

  it('getInvestmentOpinion', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getInvestmentOpinion({
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '16633',
      fidInputIscd: SAMSUNG,
      fidInputDate1: ONE_MONTH_AGO,
      fidInputDate2: TODAY,
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getInvestmentOpinionResponseSchema);
    assertResponseShape(res.body, getInvestmentOpinionResponseSchema, 'output', getInvestmentOpinionItemSchema);
  });

  it('getInvestmentOpinionByBrokerage', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getInvestmentOpinionByBrokerage({
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '16634',
      fidInputIscd: SAMSUNG,
      fidDivClsCode: '0',
      fidInputDate1: ONE_MONTH_AGO,
      fidInputDate2: TODAY,
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getInvestmentOpinionByBrokerageResponseSchema);
    assertResponseShape(
      res.body,
      getInvestmentOpinionByBrokerageResponseSchema,
      'output',
      getInvestmentOpinionByBrokerageItemSchema,
    );
  });
});
