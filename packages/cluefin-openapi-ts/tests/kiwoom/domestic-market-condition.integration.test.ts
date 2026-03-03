import { describe, test } from 'vitest';

import {
  assertKiwoomResponse,
  getKiwoomClient,
  ONE_MONTH_AGO,
  runIntegration,
  SAMSUNG,
  TODAY,
} from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('Kiwoom DomesticMarketCondition', () => {
  it('getStockQuote', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getStockQuote({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
  });

  it('getStockQuoteByDate', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getStockQuoteByDate({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
  });

  it('getStockPrice', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getStockPrice({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
  });

  it('getMarketSentimentInfo', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getMarketSentimentInfo({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
  });

  it('getNewStockWarrantPrice', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getNewStockWarrantPrice({
      newstkRecvrhtTp: '0',
    });
    assertKiwoomResponse(res);
  });

  it('getDailyInstitutionalTradingItems', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getDailyInstitutionalTradingItems({
      strtDt: ONE_MONTH_AGO,
      endDt: TODAY,
      trdeTp: '0',
      mrktTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getInstitutionalTradingTrendByStock', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getInstitutionalTradingTrendByStock({
      stkCd: SAMSUNG,
      strtDt: ONE_MONTH_AGO,
      endDt: TODAY,
      orgnPrsmUnpTp: '0',
      forPrsmUnpTp: '0',
    });
    assertKiwoomResponse(res);
  });

  it('getExecutionIntensityTrendByTime', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getExecutionIntensityTrendByTime({
      stkCd: SAMSUNG,
    });
    assertKiwoomResponse(res);
  });

  it('getExecutionIntensityTrendByDate', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getExecutionIntensityTrendByDate({
      stkCd: SAMSUNG,
    });
    assertKiwoomResponse(res);
  });

  it('getIntradayTradingByInvestor', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getIntradayTradingByInvestor({
      mrktTp: '0',
      amtQtyTp: '1',
      invsr: '0',
      frgnAll: '0',
      smtmNetprpsTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getAfterMarketTradingByInvestor', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getAfterMarketTradingByInvestor({
      mrktTp: '0',
      amtQtyTp: '1',
      trdeTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getSecuritiesFirmTradingTrendByStock', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getSecuritiesFirmTradingTrendByStock({
      mmcmCd: '0000',
      stkCd: SAMSUNG,
      strtDt: ONE_MONTH_AGO,
      endDt: TODAY,
    });
    assertKiwoomResponse(res);
  });

  it('getDailyStockPrice', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getDailyStockPrice({
      stkCd: SAMSUNG,
      qryDt: TODAY,
      indcTp: '0',
    });
    assertKiwoomResponse(res);
  });

  it('getAfterHoursSinglePrice', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getAfterHoursSinglePrice({
      stkCd: SAMSUNG,
    });
    assertKiwoomResponse(res);
  });

  it('getProgramTradingTrendByTime', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getProgramTradingTrendByTime({
      date: TODAY,
      amtQtyTp: '1',
      mrktTp: '0',
      minTicTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getProgramTradingArbitrageBalanceTrend', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getProgramTradingArbitrageBalanceTrend({
      date: TODAY,
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getProgramTradingCumulativeTrend', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getProgramTradingCumulativeTrend({
      date: TODAY,
      amtQtyTp: '1',
      mrktTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getProgramTradingTrendByStockAndTime', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getProgramTradingTrendByStockAndTime({
      amtQtyTp: '1',
      stkCd: SAMSUNG,
      date: TODAY,
    });
    assertKiwoomResponse(res);
  });

  it('getProgramTradingTrendByDate', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getProgramTradingTrendByDate({
      date: TODAY,
      amtQtyTp: '1',
      mrktTp: '0',
      minTicTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getProgramTradingTrendByStockAndDate', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getProgramTradingTrendByStockAndDate({
      amtQtyTp: '1',
      stkCd: SAMSUNG,
      date: TODAY,
    });
    assertKiwoomResponse(res);
  });
});
