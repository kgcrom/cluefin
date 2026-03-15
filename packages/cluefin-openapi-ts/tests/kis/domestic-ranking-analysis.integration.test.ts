import { describe, test } from 'vitest';
import {
  getHtsInquiryTop20ItemSchema,
  getHtsInquiryTop20ResponseSchema,
  getStockAfterHoursFluctuationRankOutput2ItemSchema,
  getStockAfterHoursFluctuationRankResponseSchema,
  getStockAfterHoursVolumeRankOutput2ItemSchema,
  getStockAfterHoursVolumeRankResponseSchema,
  getStockCreditBalanceTopItemSchema,
  getStockCreditBalanceTopResponseSchema,
  getStockDisparityIndexRankItemSchema,
  getStockDisparityIndexRankResponseSchema,
  getStockDividendYieldTopItemSchema,
  getStockDividendYieldTopResponseSchema,
  getStockExecutionStrengthTopItemSchema,
  getStockExecutionStrengthTopResponseSchema,
  getStockExpectedExecutionRiseDeclineTopItemSchema,
  getStockExpectedExecutionRiseDeclineTopResponseSchema,
  getStockFinanceRatioRankItemSchema,
  getStockFinanceRatioRankResponseSchema,
  getStockFluctuationRankItemSchema,
  getStockFluctuationRankResponseSchema,
  getStockHogaQuantityRankItemSchema,
  getStockHogaQuantityRankResponseSchema,
  getStockLargeExecutionCountTopItemSchema,
  getStockLargeExecutionCountTopResponseSchema,
  getStockMarketCapTopItemSchema,
  getStockMarketCapTopResponseSchema,
  getStockMarketPriceRankItemSchema,
  getStockMarketPriceRankResponseSchema,
  getStockNewHighLowApproachingTopItemSchema,
  getStockNewHighLowApproachingTopResponseSchema,
  getStockPreferredStockRatioTopItemSchema,
  getStockPreferredStockRatioTopResponseSchema,
  getStockProfitabilityIndicatorRankItemSchema,
  getStockProfitabilityIndicatorRankResponseSchema,
  getStockProprietaryTradingTopItemSchema,
  getStockProprietaryTradingTopResponseSchema,
  getStockShortSellingTopItemSchema,
  getStockShortSellingTopResponseSchema,
  getStockTimeHogaRankItemSchema,
  getStockTimeHogaRankResponseSchema,
  getStockWatchlistRegistrationTopItemSchema,
  getStockWatchlistRegistrationTopResponseSchema,
  getTradingVolumeRankItemSchema,
  getTradingVolumeRankResponseSchema,
} from '../../src/kis/schemas/domestic-ranking-analysis';
import {
  assertKisResponse,
  assertResponseShape,
  getKisClient,
  ONE_MONTH_AGO,
  runIntegration,
  TODAY,
} from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('KIS DomesticRankingAnalysis', () => {
  it('getTradingVolumeRank', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getTradingVolumeRank({
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '20171',
      fidInputIscd: '0000',
      fidDivClsCode: '0',
      fidBlngClsCode: '0',
      fidTrgtClsCode: '111111111',
      fidTrgtExlsClsCode: '000000',
      fidInputPrice1: '0',
      fidInputPrice2: '0',
      fidVolCnt: '0',
      fidInputDate1: '',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getTradingVolumeRankResponseSchema, 'output', getTradingVolumeRankItemSchema);
  });

  it('getStockFluctuationRank', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockFluctuationRank({
      fidRsflRate2: '',
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '20170',
      fidInputIscd: '0000',
      fidRankSortClsCode: '0',
      fidInputCnt1: '0',
      fidPrcClsCode: '0',
      fidInputPrice1: '0',
      fidInputPrice2: '0',
      fidVolCnt: '0',
      fidTrgtClsCode: '0',
      fidTrgtExlsClsCode: '0',
      fidDivClsCode: '0',
      fidRsflRate1: '',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockFluctuationRankResponseSchema, 'output', getStockFluctuationRankItemSchema);
  });

  it('getStockHogaQuantityRank', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockHogaQuantityRank({
      fidVolCnt: '0',
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '20172',
      fidInputIscd: '0000',
      fidRankSortClsCode: '0',
      fidDivClsCode: '0',
      fidTrgtClsCode: '0',
      fidTrgtExlsClsCode: '0',
      fidInputPrice1: '0',
      fidInputPrice2: '0',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockHogaQuantityRankResponseSchema, 'output', getStockHogaQuantityRankItemSchema);
  });

  it('getStockProfitabilityIndicatorRank', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockProfitabilityIndicatorRank({
      fidCondMrktDivCode: 'J',
      fidTrgtClsCode: '0',
      fidCondScrDivCode: '20173',
      fidInputIscd: '0000',
      fidDivClsCode: '0',
      fidInputPrice1: '0',
      fidInputPrice2: '0',
      fidVolCnt: '0',
      fidInputOption1: '',
      fidInputOption2: '',
      fidRankSortClsCode: '0',
      fidBlngClsCode: '0',
      fidTrgtExlsClsCode: '0',
    });
    assertKisResponse(res);
    assertResponseShape(
      res.body,
      getStockProfitabilityIndicatorRankResponseSchema,
      'output',
      getStockProfitabilityIndicatorRankItemSchema,
    );
  });

  it('getStockMarketCapTop', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockMarketCapTop({
      fidInputPrice2: '0',
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '20174',
      fidDivClsCode: '0',
      fidInputIscd: '0000',
      fidTrgtClsCode: '0',
      fidTrgtExlsClsCode: '0',
      fidInputPrice1: '0',
      fidVolCnt: '0',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockMarketCapTopResponseSchema, 'output', getStockMarketCapTopItemSchema);
  });

  it('getStockFinanceRatioRank', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockFinanceRatioRank({
      fidTrgtClsCode: '0',
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '20175',
      fidInputIscd: '0000',
      fidDivClsCode: '0',
      fidInputPrice1: '0',
      fidInputPrice2: '0',
      fidVolCnt: '0',
      fidInputOption1: '',
      fidInputOption2: '',
      fidRankSortClsCode: '0',
      fidBlngClsCode: '0',
      fidTrgtExlsClsCode: '0',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockFinanceRatioRankResponseSchema, 'output', getStockFinanceRatioRankItemSchema);
  });

  it('getStockTimeHogaRank', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockTimeHogaRank({
      fidInputPrice1: '0',
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '20176',
      fidRankSortClsCode: '0',
      fidDivClsCode: '0',
      fidInputIscd: '0000',
      fidTrgtExlsClsCode: '0',
      fidTrgtClsCode: '0',
      fidVolCnt: '0',
      fidInputPrice2: '0',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockTimeHogaRankResponseSchema, 'output', getStockTimeHogaRankItemSchema);
  });

  it('getStockPreferredStockRatioTop', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockPreferredStockRatioTop({
      fidVolCnt: '0',
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '20177',
      fidDivClsCode: '0',
      fidInputIscd: '0000',
      fidTrgtClsCode: '0',
      fidTrgtExlsClsCode: '0',
      fidInputPrice1: '0',
      fidInputPrice2: '0',
    });
    assertKisResponse(res);
    assertResponseShape(
      res.body,
      getStockPreferredStockRatioTopResponseSchema,
      'output',
      getStockPreferredStockRatioTopItemSchema,
    );
  });

  it('getStockDisparityIndexRank', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockDisparityIndexRank({
      fidInputPrice2: '0',
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '20178',
      fidDivClsCode: '0',
      fidRankSortClsCode: '0',
      fidHourClsCode: '5',
      fidInputIscd: '0000',
      fidTrgtClsCode: '0',
      fidTrgtExlsClsCode: '0',
      fidInputPrice1: '0',
      fidVolCnt: '0',
    });
    assertKisResponse(res);
    assertResponseShape(
      res.body,
      getStockDisparityIndexRankResponseSchema,
      'output',
      getStockDisparityIndexRankItemSchema,
    );
  });

  it('getStockMarketPriceRank', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockMarketPriceRank({
      fidTrgtClsCode: '0',
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '20179',
      fidInputIscd: '0000',
      fidDivClsCode: '0',
      fidInputPrice1: '0',
      fidInputPrice2: '0',
      fidVolCnt: '0',
      fidInputOption1: '',
      fidInputOption2: '',
      fidRankSortClsCode: '0',
      fidBlngClsCode: '0',
      fidTrgtExlsClsCode: '0',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockMarketPriceRankResponseSchema, 'output', getStockMarketPriceRankItemSchema);
  });

  it('getStockExecutionStrengthTop', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockExecutionStrengthTop({
      fidTrgtExlsClsCode: '0',
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '20168',
      fidInputIscd: '0000',
      fidDivClsCode: '0',
      fidInputPrice1: '0',
      fidInputPrice2: '0',
      fidVolCnt: '0',
      fidTrgtClsCode: '0',
    });
    assertKisResponse(res);
    assertResponseShape(
      res.body,
      getStockExecutionStrengthTopResponseSchema,
      'output',
      getStockExecutionStrengthTopItemSchema,
    );
  });

  it('getStockWatchlistRegistrationTop', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockWatchlistRegistrationTop({
      fidInputIscd2: '000000',
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '20180',
      fidInputIscd: '0000',
      fidTrgtClsCode: '0',
      fidTrgtExlsClsCode: '0',
      fidInputPrice1: '0',
      fidInputPrice2: '0',
      fidVolCnt: '0',
      fidDivClsCode: '0',
      fidInputCnt1: '0',
    });
    assertKisResponse(res);
    assertResponseShape(
      res.body,
      getStockWatchlistRegistrationTopResponseSchema,
      'output',
      getStockWatchlistRegistrationTopItemSchema,
    );
  });

  it('getStockExpectedExecutionRiseDeclineTop', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockExpectedExecutionRiseDeclineTop({
      fidRankSortClsCode: '0',
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '20182',
      fidInputIscd: '0000',
      fidDivClsCode: '0',
      fidAplyRangPrc1: '0',
      fidVolCnt: '0',
      fidPbmn: '0',
      fidBlngClsCode: '0',
      fidMkopClsCode: '0',
    });
    assertKisResponse(res);
    assertResponseShape(
      res.body,
      getStockExpectedExecutionRiseDeclineTopResponseSchema,
      'output',
      getStockExpectedExecutionRiseDeclineTopItemSchema,
    );
  });

  it('getStockProprietaryTradingTop', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockProprietaryTradingTop({
      fidTrgtExlsClsCode: '0',
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '20186',
      fidDivClsCode: '0',
      fidRankSortClsCode: '0',
      fidInputDate1: ONE_MONTH_AGO,
      fidInputDate2: TODAY,
      fidInputIscd: '0000',
      fidTrgtClsCode: '0',
      fidAplyRangVol: '0',
      fidAplyRangPrc2: '0',
      fidAplyRangPrc1: '0',
    });
    assertKisResponse(res);
    assertResponseShape(
      res.body,
      getStockProprietaryTradingTopResponseSchema,
      'output',
      getStockProprietaryTradingTopItemSchema,
    );
  });

  it('getStockNewHighLowApproachingTop', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockNewHighLowApproachingTop({
      fidAplyRangVol: '0',
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '20187',
      fidDivClsCode: '0',
      fidInputCnt1: '0',
      fidInputCnt2: '0',
      fidPrcClsCode: '0',
      fidInputIscd: '0000',
      fidTrgtClsCode: '0',
      fidTrgtExlsClsCode: '0',
      fidAplyRangPrc1: '0',
      fidAplyRangPrc2: '0',
    });
    assertKisResponse(res);
    assertResponseShape(
      res.body,
      getStockNewHighLowApproachingTopResponseSchema,
      'output',
      getStockNewHighLowApproachingTopItemSchema,
    );
  });

  it('getStockShortSellingTop', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockShortSellingTop({
      fidAplyRangVol: '0',
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '20482',
      fidInputIscd: '0000',
      fidPeriodDivCode: 'D',
      fidInputCnt1: '0',
      fidTrgtExlsClsCode: '0',
      fidTrgtClsCode: '0',
      fidAplyRangPrc1: '0',
      fidAplyRangPrc2: '0',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockShortSellingTopResponseSchema, 'output', getStockShortSellingTopItemSchema);
  });

  it('getStockAfterHoursFluctuationRank', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockAfterHoursFluctuationRank({
      fidCondMrktDivCode: 'J',
      fidMrktClsCode: '',
      fidCondScrDivCode: '20234',
      fidInputIscd: '0000',
      fidDivClsCode: '2',
      fidInputPrice1: '0',
      fidInputPrice2: '0',
      fidVolCnt: '0',
      fidTrgtClsCode: '',
      fidTrgtExlsClsCode: '',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockAfterHoursFluctuationRankResponseSchema);
    assertResponseShape(
      res.body,
      getStockAfterHoursFluctuationRankResponseSchema,
      'output2',
      getStockAfterHoursFluctuationRankOutput2ItemSchema,
    );
  });

  it('getStockAfterHoursVolumeRank', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockAfterHoursVolumeRank({
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '20235',
      fidInputIscd: '0000',
      fidRankSortClsCode: '0',
      fidInputPrice1: '0',
      fidInputPrice2: '0',
      fidVolCnt: '0',
      fidTrgtClsCode: '0',
      fidTrgtExlsClsCode: '0',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockAfterHoursVolumeRankResponseSchema);
    assertResponseShape(
      res.body,
      getStockAfterHoursVolumeRankResponseSchema,
      'output2',
      getStockAfterHoursVolumeRankOutput2ItemSchema,
    );
  });

  // HHKST17010000 tr_id는 API 구독 플랜에 따라 사용 불가할 수 있음
  it.skip('getStockCreditBalanceTop', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockCreditBalanceTop({
      fidCondScrDivCode: '11701',
      fidInputIscd: '0001',
      fidOption: '7',
      fidCondMrktDivCode: 'J',
      fidRankSortClsCode: '0',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockCreditBalanceTopResponseSchema, 'output', getStockCreditBalanceTopItemSchema);
  });

  it('getStockDividendYieldTop', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockDividendYieldTop({
      ctsArea: '',
      gb1: '0',
      upjong: '0001',
      gb2: '0',
      gb3: '2',
      fDt: ONE_MONTH_AGO,
      tDt: TODAY,
      gb4: '0',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockDividendYieldTopResponseSchema, 'output', getStockDividendYieldTopItemSchema);
  });

  // HHKST1909000C0 tr_id는 API 구독 플랜에 따라 사용 불가할 수 있음
  it.skip('getStockLargeExecutionCountTop', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockLargeExecutionCountTop({
      fidAplyRangPrc2: '',
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '11909',
      fidInputIscd: '0001',
      fidRankSortClsCode: '0',
      fidDivClsCode: '0',
      fidInputPrice1: '',
      fidAplyRangPrc1: '',
      fidInputIscd2: '',
      fidTrgtExlsClsCode: '0',
      fidTrgtClsCode: '0',
      fidVolCnt: '',
    });
    assertKisResponse(res);
    assertResponseShape(
      res.body,
      getStockLargeExecutionCountTopResponseSchema,
      'output',
      getStockLargeExecutionCountTopItemSchema,
    );
  });

  it('getHtsInquiryTop20', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getHtsInquiryTop20({});
    assertKisResponse(res);
    assertResponseShape(res.body, getHtsInquiryTop20ResponseSchema, 'output1', getHtsInquiryTop20ItemSchema);
  });
});
