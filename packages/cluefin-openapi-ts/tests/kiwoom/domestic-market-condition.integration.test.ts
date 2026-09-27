import { describe, test } from 'vitest';

import {
  afterMarketTradingByInvestorResponseSchema,
  dailyInstitutionalTradingItemsResponseSchema,
  dailyStockPriceResponseSchema,
  executionIntensityTrendByDateResponseSchema,
  executionIntensityTrendByTimeResponseSchema,
  institutionalTradingTrendByStockResponseSchema,
  intradayTradingByInvestorResponseSchema,
  marketSentimentInfoResponseSchema,
  newStockWarrantPriceResponseSchema,
  programTradingArbitrageBalanceTrendResponseSchema,
  programTradingCumulativeTrendResponseSchema,
  programTradingTrendByDateResponseSchema,
  programTradingTrendByStockAndDateResponseSchema,
  programTradingTrendByStockAndTimeResponseSchema,
  programTradingTrendByTimeResponseSchema,
  securitiesFirmTradingTrendByStockResponseSchema,
  stockPriceResponseSchema,
  stockQuoteByDateResponseSchema,
  stockQuoteResponseSchema,
} from '../../src/kiwoom/schemas/domestic-market-condition';
import {
  assertKiwoomResponse,
  getKiwoomClient,
  ONE_MONTH_AGO,
  PREV_WEEKDAY,
  runIntegration,
  SAMSUNG,
  setupKiwoomRateLimit,
  TODAY,
} from '../_helpers/integration-setup';
import { assertKiwoomSpecConformance } from '../_helpers/kiwoom-spec-conformance';

const it = runIntegration ? test : test.skip;

describe('Kiwoom DomesticMarketCondition', () => {
  setupKiwoomRateLimit();
  it('getStockQuote', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getStockQuote({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(stockQuoteResponseSchema);
  });

  it('getStockQuoteByDate', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getStockQuoteByDate({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(stockQuoteByDateResponseSchema);
  });

  it('getStockPrice', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getStockPrice({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(stockPriceResponseSchema);
  });

  it('getMarketSentimentInfo', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getMarketSentimentInfo({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(marketSentimentInfoResponseSchema);
  });

  it('getNewStockWarrantPrice', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getNewStockWarrantPrice({
      newstkRecvrhtTp: '00',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(newStockWarrantPriceResponseSchema);
  });

  it('getDailyInstitutionalTradingItems', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getDailyInstitutionalTradingItems({
      strtDt: ONE_MONTH_AGO,
      endDt: TODAY,
      trdeTp: '1',
      mrktTp: '001',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(dailyInstitutionalTradingItemsResponseSchema);
  });

  it('getInstitutionalTradingTrendByStock', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getInstitutionalTradingTrendByStock({
      stkCd: SAMSUNG,
      strtDt: ONE_MONTH_AGO,
      endDt: TODAY,
      orgnPrsmUnpTp: '1',
      forPrsmUnpTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(institutionalTradingTrendByStockResponseSchema);
  });

  it('getExecutionIntensityTrendByTime', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getExecutionIntensityTrendByTime({
      stkCd: SAMSUNG,
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(executionIntensityTrendByTimeResponseSchema);
  });

  it('getExecutionIntensityTrendByDate', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getExecutionIntensityTrendByDate({
      stkCd: SAMSUNG,
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(executionIntensityTrendByDateResponseSchema);
  });

  it('getIntradayTradingByInvestor', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getIntradayTradingByInvestor({
      mrktTp: '000',
      amtQtyTp: '1',
      invsr: '0',
      frgnAll: '0',
      smtmNetprpsTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(intradayTradingByInvestorResponseSchema);
  });

  it('getAfterMarketTradingByInvestor', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getAfterMarketTradingByInvestor({
      mrktTp: '000',
      amtQtyTp: '1',
      trdeTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(afterMarketTradingByInvestorResponseSchema);
  });

  it('getSecuritiesFirmTradingTrendByStock', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getSecuritiesFirmTradingTrendByStock({
      mmcmCd: '001',
      stkCd: SAMSUNG,
      strtDt: ONE_MONTH_AGO,
      endDt: TODAY,
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(securitiesFirmTradingTrendByStockResponseSchema);
  });

  it('getDailyStockPrice', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getDailyStockPrice({
      stkCd: SAMSUNG,
      qryDt: TODAY,
      indcTp: '0',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(dailyStockPriceResponseSchema);
  });

  it('getProgramTradingTrendByTime', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getProgramTradingTrendByTime({
      date: TODAY,
      amtQtyTp: '1',
      mrktTp: 'P00101', // 코스피·KRX (문서 요청 예시값)
      minTicTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(programTradingTrendByTimeResponseSchema);
  });

  it('getProgramTradingArbitrageBalanceTrend', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getProgramTradingArbitrageBalanceTrend({
      date: TODAY,
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(programTradingArbitrageBalanceTrendResponseSchema);
  });

  it('getProgramTradingCumulativeTrend', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getProgramTradingCumulativeTrend({
      date: PREV_WEEKDAY,
      amtQtyTp: '1',
      mrktTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(programTradingCumulativeTrendResponseSchema);
  });

  it('getProgramTradingTrendByStockAndTime', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getProgramTradingTrendByStockAndTime({
      amtQtyTp: '1',
      stkCd: SAMSUNG,
      date: TODAY,
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(programTradingTrendByStockAndTimeResponseSchema);
  });

  it('getProgramTradingTrendByDate', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getProgramTradingTrendByDate({
      date: TODAY,
      amtQtyTp: '1',
      mrktTp: 'P00101', // 코스피·KRX (문서 요청 예시값)
      minTicTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(programTradingTrendByDateResponseSchema);
  });

  it('getProgramTradingTrendByStockAndDate', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getProgramTradingTrendByStockAndDate({
      amtQtyTp: '1',
      stkCd: SAMSUNG,
      date: TODAY,
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(programTradingTrendByStockAndDateResponseSchema);
  });
});
