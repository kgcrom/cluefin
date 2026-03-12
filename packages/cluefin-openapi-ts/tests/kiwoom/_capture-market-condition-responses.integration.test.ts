import { describe, test } from 'vitest';
import { getKiwoomClient, ONE_MONTH_AGO, runIntegration, SAMSUNG, TODAY } from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('Capture DomesticMarketCondition responses', () => {
  it('capture all market condition responses', async () => {
    const client = await getKiwoomClient();

    const calls = [
      ['getStockQuote', { stkCd: SAMSUNG }],
      ['getStockQuoteByDate', { stkCd: SAMSUNG }],
      ['getStockPrice', { stkCd: SAMSUNG }],
      ['getMarketSentimentInfo', { stkCd: SAMSUNG }],
      ['getNewStockWarrantPrice', { newstkRecvrhtTp: '0' }],
      [
        'getDailyInstitutionalTradingItems',
        { strtDt: ONE_MONTH_AGO, endDt: TODAY, trdeTp: '0', mrktTp: '0', stexTp: '1' },
      ],
      [
        'getInstitutionalTradingTrendByStock',
        { stkCd: SAMSUNG, strtDt: ONE_MONTH_AGO, endDt: TODAY, orgnPrsmUnpTp: '0', forPrsmUnpTp: '0' },
      ],
      ['getExecutionIntensityTrendByTime', { stkCd: SAMSUNG }],
      ['getExecutionIntensityTrendByDate', { stkCd: SAMSUNG }],
      [
        'getIntradayTradingByInvestor',
        { mrktTp: '0', amtQtyTp: '1', invsr: '0', frgnAll: '0', smtmNetprpsTp: '0', stexTp: '1' },
      ],
      ['getAfterMarketTradingByInvestor', { mrktTp: '0', amtQtyTp: '1', trdeTp: '0', stexTp: '1' }],
      ['getSecuritiesFirmTradingTrendByStock', { mmcmCd: '0000', stkCd: SAMSUNG, strtDt: ONE_MONTH_AGO, endDt: TODAY }],
      ['getDailyStockPrice', { stkCd: SAMSUNG, qryDt: TODAY, indcTp: '0' }],
      ['getAfterHoursSinglePrice', { stkCd: SAMSUNG }],
      ['getProgramTradingTrendByTime', { date: TODAY, amtQtyTp: '1', mrktTp: '0', minTicTp: '0', stexTp: '1' }],
      ['getProgramTradingArbitrageBalanceTrend', { date: TODAY, stexTp: '1' }],
      ['getProgramTradingCumulativeTrend', { date: TODAY, amtQtyTp: '1', mrktTp: '0', stexTp: '1' }],
      ['getProgramTradingTrendByStockAndTime', { amtQtyTp: '1', stkCd: SAMSUNG, date: TODAY }],
      ['getProgramTradingTrendByDate', { date: TODAY, amtQtyTp: '1', mrktTp: '0', minTicTp: '0', stexTp: '1' }],
      ['getProgramTradingTrendByStockAndDate', { amtQtyTp: '1', stkCd: SAMSUNG, date: TODAY }],
      [
        'getTopIntradayTradingByInvestor',
        {
          trdeTp: '1',
          mrktTp: '000',
          orgnTp: '9000',
          amtQtyTp: '1',
          invsr: '0',
          frgnAll: '0',
          smtmNetprpsTp: '0',
          stexTp: '1',
        },
      ],
    ] as const;

    for (const [method, params] of calls) {
      const fn = (client.domesticMarketCondition as Record<string, Function>)[method];
      const res = await fn.call(client.domesticMarketCondition, params);
      console.log(`\n=== ${method} ===`);
      console.log(JSON.stringify(res.body, null, 2));
    }
  }, 120000);
});
