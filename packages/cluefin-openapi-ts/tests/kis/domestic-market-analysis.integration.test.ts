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
const userId = process.env.KIS_HTS_USER_ID;
const itWithUserId = runIntegration && userId ? test : test.skip;

describe('KIS DomesticMarketAnalysis', () => {
  it('getInvestorTradingTrendByMarketDaily', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getInvestorTradingTrendByMarketDaily({
      fidCondMrktDivCode: 'U',
      fidInputIscd: '0001',
      fidInputDate1: ONE_MONTH_AGO,
      fidInputIscd1: 'KSP',
      fidInputDate2: TODAY,
      fidInputIscd2: '0001',
    });
    assertKisResponse(res);
  });

  it('getInvestorTradingTrendByMarketIntraday', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getInvestorTradingTrendByMarketIntraday({
      fidInputIscd: '0001',
      fidInputIscd2: '0001',
    });
    assertKisResponse(res);
  });

  it('getInvestorTradingTrendByStockDaily', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getInvestorTradingTrendByStockDaily({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
      fidInputDate1: ONE_MONTH_AGO,
      fidOrgAdjPrc: '0',
      fidEtcClsCode: '',
    });
    assertKisResponse(res);
  });

  it('getForeignNetBuyTrendByStock', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getForeignNetBuyTrendByStock({
      fidInputIscd: SAMSUNG,
      fidInputIscd2: SAMSUNG,
      fidCondMrktDivCode: 'J',
    });
    assertKisResponse(res);
  });

  it('getForeignBrokerageTradingAggregate', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getForeignBrokerageTradingAggregate({
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '20440',
      fidInputIscd: SAMSUNG,
      fidRankSortClsCode: '0',
      fidRankSortClsCode2: '0',
    });
    assertKisResponse(res);
  });

  it('getForeignInstitutionalEstimateByStock', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getForeignInstitutionalEstimateByStock({
      mkscShrnIscd: SAMSUNG,
    });
    assertKisResponse(res);
  });

  it('getMemberTradingTrendByStock', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getMemberTradingTrendByStock({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
      fidInputIscd2: '',
      fidInputDate1: ONE_MONTH_AGO,
      fidInputDate2: TODAY,
      fidSctnClsCode: '0',
    });
    assertKisResponse(res);
  });

  it('getMemberTradingTrendTick', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getMemberTradingTrendTick({
      fidCondScrDivCode: '20432',
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
      fidInputIscd2: '',
      fidMrktClsCode: '0',
      fidVolCnt: '0',
    });
    assertKisResponse(res);
  });

  it('getBuySellVolumeByStockDaily', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getBuySellVolumeByStockDaily({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
      fidInputDate1: ONE_MONTH_AGO,
      fidInputDate2: TODAY,
      fidPeriodDivCode: 'D',
      fidCondMrktDivCode1: 'J',
      fidInputIscd1: SAMSUNG,
    });
    assertKisResponse(res);
  });

  it('getCreditBalanceTrendDaily', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getCreditBalanceTrendDaily({
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '20476',
      fidInputIscd: SAMSUNG,
      fidInputDate1: ONE_MONTH_AGO,
    });
    assertKisResponse(res);
  });

  it('getStockLoanTrendDaily', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getStockLoanTrendDaily({
      mrktDivClsCode: '1',
      mkscShrnIscd: SAMSUNG,
      startDate: ONE_MONTH_AGO,
      endDate: TODAY,
      cts: '',
    });
    assertKisResponse(res);
  });

  it('getProgramTradingSummaryDaily', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getProgramTradingSummaryDaily({
      fidCondMrktDivCode: 'J',
      fidMrktClsCode: '0',
      fidInputDate1: ONE_MONTH_AGO,
      fidInputDate2: TODAY,
    });
    assertKisResponse(res);
  });

  it('getProgramTradingSummaryIntraday', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getProgramTradingSummaryIntraday({
      fidCondMrktDivCode: 'J',
      fidMrktClsCode: '0',
      fidSctnClsCode: '0',
      fidInputIscd: '0001',
      fidCondMrktDivCode1: 'J',
      fidInputHour1: '155000',
    });
    assertKisResponse(res);
  });

  it('getProgramTradingTrendByStockDaily', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getProgramTradingTrendByStockDaily({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
      fidInputDate1: ONE_MONTH_AGO,
    });
    assertKisResponse(res);
  });

  it('getProgramTradingTrendByStockIntraday', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getProgramTradingTrendByStockIntraday({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
  });

  it('getProgramTradingInvestorTrendToday', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getProgramTradingInvestorTrendToday({
      exchDivClsCode: 'J',
      mrktDivClsCode: '1',
    });
    assertKisResponse(res);
  });

  it('getShortSellingTrendDaily', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getShortSellingTrendDaily({
      fidInputDate2: TODAY,
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
      fidInputDate1: ONE_MONTH_AGO,
    });
    assertKisResponse(res);
  });

  it('getExpectedPriceTrend', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getExpectedPriceTrend({
      fidMkopClsCode: '0',
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
  });

  it('getAfterHoursExpectedFluctuation', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getAfterHoursExpectedFluctuation({
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '11186',
      fidInputIscd: '0000',
      fidRankSortClsCode: '0',
      fidDivClsCode: '0',
      fidInputPrice1: '0',
      fidInputPrice2: '0',
      fidInputVol1: '0',
    });
    assertKisResponse(res);
  });

  it('getLimitPriceStocks', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getLimitPriceStocks({
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '11300',
      fidPrcClsCode: '0',
      fidDivClsCode: '0',
      fidInputIscd: '0000',
      fidTrgtClsCode: '0',
      fidTrgtExlsClsCode: '0',
      fidInputPrice1: '0',
      fidInputPrice2: '0',
      fidVolCnt: '0',
    });
    assertKisResponse(res);
  });

  it('getTradingWeightByAmount', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getTradingWeightByAmount({
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '11119',
      fidInputIscd: SAMSUNG,
    });
    assertKisResponse(res);
  });

  it('getResistanceLevelTradingWeight', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getResistanceLevelTradingWeight({
      fidCondMrktDivCode: 'J',
      fidInputIscd: SAMSUNG,
      fidCondScrDivCode: '10113',
      fidInputHour1: '155000',
    });
    assertKisResponse(res);
  });

  it('getMarketFundSummary', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getMarketFundSummary({
      fidInputDate1: TODAY,
    });
    assertKisResponse(res);
  });

  it('getWatchlistMultiQuote', async () => {
    const client = await getKisClient();
    const params: Record<string, string> = {};
    for (let i = 1; i <= 30; i++) {
      params[`fidCondMrktDivCode${i}`] = 'J';
      params[`fidInputIscd${i}`] = i === 1 ? SAMSUNG : i === 2 ? '000660' : '';
    }
    const res = await client.domesticMarketAnalysis.getWatchlistMultiQuote(params);
    assertKisResponse(res);
  });

  // userId 필요 엔드포인트
  itWithUserId('getConditionSearchList', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getConditionSearchList({
      userId,
    });
    assertKisResponse(res);
  });

  itWithUserId('getConditionSearchResult', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getConditionSearchResult({
      userId,
      seq: '0',
    });
    assertKisResponse(res);
  });

  itWithUserId('getWatchlistGroups', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getWatchlistGroups({
      interestType: '0',
      fidEtcClsCode: '',
      userId,
    });
    assertKisResponse(res);
  });

  itWithUserId('getWatchlistStocksByGroup', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getWatchlistStocksByGroup({
      type: '0',
      userId,
      dataRank: '',
      interGrpCode: '',
      interGrpName: '',
      htsKorIsnm: '',
      cntgClsCode: '',
      fidEtcClsCode: '',
    });
    assertKisResponse(res);
  });

  itWithUserId('getInstitutionalForeignTradingAggregate', async () => {
    const client = await getKisClient();
    const res = await client.domesticMarketAnalysis.getInstitutionalForeignTradingAggregate({
      type: '0',
      userId,
      dataRank: '',
      interGrpCode: '',
      interGrpName: '',
      htsKorIsnm: '',
      cntgClsCode: '',
      fidEtcClsCode: '',
    });
    assertKisResponse(res);
  });
});
