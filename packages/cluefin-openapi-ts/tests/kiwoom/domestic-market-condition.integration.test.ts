import { describe, test } from 'vitest';

import {
  afterHoursSinglePriceResponseSchema,
  afterMarketTradingByInvestorItemSchema,
  afterMarketTradingByInvestorResponseSchema,
  dailyInstitutionalTradingItemsItemSchema,
  dailyInstitutionalTradingItemsResponseSchema,
  dailyStockPriceItemSchema,
  dailyStockPriceResponseSchema,
  executionIntensityTrendByDateItemSchema,
  executionIntensityTrendByDateResponseSchema,
  executionIntensityTrendByTimeItemSchema,
  executionIntensityTrendByTimeResponseSchema,
  institutionalTradingTrendByStockItemSchema,
  institutionalTradingTrendByStockResponseSchema,
  intradayTradingByInvestorItemSchema,
  intradayTradingByInvestorResponseSchema,
  marketSentimentInfoResponseSchema,
  newStockWarrantPriceItemSchema,
  newStockWarrantPriceResponseSchema,
  programTradingArbitrageBalanceTrendItemSchema,
  programTradingArbitrageBalanceTrendResponseSchema,
  programTradingCumulativeTrendItemSchema,
  programTradingCumulativeTrendResponseSchema,
  programTradingTrendByDateResponseSchema,
  programTradingTrendByStockAndDateItemSchema,
  programTradingTrendByStockAndDateResponseSchema,
  programTradingTrendByStockAndTimeItemSchema,
  programTradingTrendByStockAndTimeResponseSchema,
  programTradingTrendByTimeResponseSchema,
  securitiesFirmTradingTrendByStockItemSchema,
  securitiesFirmTradingTrendByStockResponseSchema,
  stockPriceResponseSchema,
  stockQuoteByDateItemSchema,
  stockQuoteByDateResponseSchema,
  stockQuoteResponseSchema,
} from '../../src/kiwoom/schemas/domestic-market-condition';
import {
  assertKiwoomResponse,
  assertResponseShape,
  getKiwoomClient,
  ONE_MONTH_AGO,
  runIntegration,
  SAMSUNG,
  setupKiwoomRateLimit,
  TODAY,
} from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('Kiwoom DomesticMarketCondition', () => {
  setupKiwoomRateLimit();
  it('getStockQuote', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getStockQuote({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, stockQuoteResponseSchema);
  });

  it('getStockQuoteByDate', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getStockQuoteByDate({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, stockQuoteByDateResponseSchema, 'stkDdwkmm', stockQuoteByDateItemSchema);
  });

  it('getStockPrice', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getStockPrice({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, stockPriceResponseSchema);
  });

  it('getMarketSentimentInfo', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getMarketSentimentInfo({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, marketSentimentInfoResponseSchema);
  });

  it('getNewStockWarrantPrice', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getNewStockWarrantPrice({
      newstkRecvrhtTp: '0',
    });
    assertKiwoomResponse(res);
    assertResponseShape(
      res.body,
      newStockWarrantPriceResponseSchema,
      'newstkRecvrhtMrpr',
      newStockWarrantPriceItemSchema,
    );
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
    assertResponseShape(
      res.body,
      dailyInstitutionalTradingItemsResponseSchema,
      'dalyOrgnTrdeStk',
      dailyInstitutionalTradingItemsItemSchema,
    );
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
    assertResponseShape(
      res.body,
      institutionalTradingTrendByStockResponseSchema,
      'stkOrgnTrdeTrnsn',
      institutionalTradingTrendByStockItemSchema,
    );
  });

  it('getExecutionIntensityTrendByTime', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getExecutionIntensityTrendByTime({
      stkCd: SAMSUNG,
    });
    assertKiwoomResponse(res);
    assertResponseShape(
      res.body,
      executionIntensityTrendByTimeResponseSchema,
      'cntrStrTm',
      executionIntensityTrendByTimeItemSchema,
    );
  });

  it('getExecutionIntensityTrendByDate', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getExecutionIntensityTrendByDate({
      stkCd: SAMSUNG,
    });
    assertKiwoomResponse(res);
    assertResponseShape(
      res.body,
      executionIntensityTrendByDateResponseSchema,
      'cntrStrDaly',
      executionIntensityTrendByDateItemSchema,
    );
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
    assertResponseShape(
      res.body,
      intradayTradingByInvestorResponseSchema,
      'opmrInvsrTrde',
      intradayTradingByInvestorItemSchema,
    );
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
    assertResponseShape(
      res.body,
      afterMarketTradingByInvestorResponseSchema,
      'opafInvsrTrde',
      afterMarketTradingByInvestorItemSchema,
    );
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
    assertResponseShape(
      res.body,
      securitiesFirmTradingTrendByStockResponseSchema,
      'secStkTrdeTrend',
      securitiesFirmTradingTrendByStockItemSchema,
    );
  });

  it('getDailyStockPrice', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getDailyStockPrice({
      stkCd: SAMSUNG,
      qryDt: TODAY,
      indcTp: '0',
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, dailyStockPriceResponseSchema, 'dalyStkpc', dailyStockPriceItemSchema);
  });

  it('getAfterHoursSinglePrice', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getAfterHoursSinglePrice({
      stkCd: SAMSUNG,
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, afterHoursSinglePriceResponseSchema);
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
    assertResponseShape(res.body, programTradingTrendByTimeResponseSchema);
  });

  it('getProgramTradingArbitrageBalanceTrend', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getProgramTradingArbitrageBalanceTrend({
      date: TODAY,
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertResponseShape(
      res.body,
      programTradingArbitrageBalanceTrendResponseSchema,
      'prmTrdeDfrtRemnTrnsn',
      programTradingArbitrageBalanceTrendItemSchema,
    );
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
    assertResponseShape(
      res.body,
      programTradingCumulativeTrendResponseSchema,
      'prmTrdeAccTrnsn',
      programTradingCumulativeTrendItemSchema,
    );
  });

  it('getProgramTradingTrendByStockAndTime', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getProgramTradingTrendByStockAndTime({
      amtQtyTp: '1',
      stkCd: SAMSUNG,
      date: TODAY,
    });
    assertKiwoomResponse(res);
    assertResponseShape(
      res.body,
      programTradingTrendByStockAndTimeResponseSchema,
      'stkTmPrmTrdeTrnsn',
      programTradingTrendByStockAndTimeItemSchema,
    );
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
    assertResponseShape(res.body, programTradingTrendByDateResponseSchema);
  });

  it('getProgramTradingTrendByStockAndDate', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getProgramTradingTrendByStockAndDate({
      amtQtyTp: '1',
      stkCd: SAMSUNG,
      date: TODAY,
    });
    assertKiwoomResponse(res);
    assertResponseShape(
      res.body,
      programTradingTrendByStockAndDateResponseSchema,
      'stkDalyPrmTrdeTrnsn',
      programTradingTrendByStockAndDateItemSchema,
    );
  });

  it('getTopIntradayTradingByInvestor', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticMarketCondition.getTopIntradayTradingByInvestor({
      trdeTp: '1',
      mrktTp: '000',
      orgnTp: '9000',
      amtQtyTp: '1',
      invsr: '0',
      frgnAll: '0',
      smtmNetprpsTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertResponseShape(
      res.body,
      intradayTradingByInvestorResponseSchema,
      'opmrInvsrTrde',
      intradayTradingByInvestorItemSchema,
    );
  });
});
