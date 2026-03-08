import { describe, test } from 'vitest';

import {
  assertKisResponse,
  getKisClient,
  ONE_MONTH_AGO,
  runIntegration,
  SAMSUNG,
  TODAY,
} from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('KIS DomesticStockInfo', () => {
  it('getProductBasicInfo', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getProductBasicInfo({
      pdno: SAMSUNG,
      prdtTypeCd: '300',
    });
    assertKisResponse(res);
  });

  it('getStockBasicInfo', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getStockBasicInfo({
      prdtTypeCd: '300',
      pdno: SAMSUNG,
    });
    assertKisResponse(res);
  });

  it('getBalanceSheet', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getBalanceSheet({
      fidDivClsCode: '0',
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
  });

  it('getIncomeStatement', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getIncomeStatement({
      fidDivClsCode: '0',
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
  });

  it('getFinancialRatio', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getFinancialRatio({
      fidDivClsCode: '0',
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
  });

  it('getProfitabilityRatio', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getProfitabilityRatio({
      fidInputIscd: SAMSUNG,
      fidDivClsCode: '0',
      fidCondMrktDivCode: 'J',
    });
    assertKisResponse(res);
  });

  it('getOtherKeyRatio', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getOtherKeyRatio({
      fidInputIscd: SAMSUNG,
      fidDivClsCode: '0',
      fidCondMrktDivCode: 'J',
    });
    assertKisResponse(res);
  });

  it('getStabilityRatio', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getStabilityRatio({
      fidInputIscd: SAMSUNG,
      fidDivClsCode: '0',
      fidCondMrktDivCode: 'J',
    });
    assertKisResponse(res);
  });

  it('getGrowthRatio', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getGrowthRatio({
      fidInputIscd: SAMSUNG,
      fidDivClsCode: '0',
      fidCondMrktDivCode: 'J',
    });
    assertKisResponse(res);
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
  });

  it('getEstimatedEarnings', async () => {
    const client = await getKisClient();
    const res = await client.domesticStockInfo.getEstimatedEarnings({
      shtCd: SAMSUNG,
    });
    assertKisResponse(res);
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
  });
});
