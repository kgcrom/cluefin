import { describe, test } from 'vitest';

import { assertKisResponse, getKisClient, ONE_MONTH_AGO, runIntegration, TODAY } from '../_helpers/integration-setup';

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
  });

  it('getStockWatchlistRegistrationTop', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockWatchlistRegistrationTop({
      fidInputIscd2: '0000',
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
  });

  it('getStockAfterHoursFluctuationRank', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockAfterHoursFluctuationRank({
      fidCondMrktDivCode: 'J',
      fidMrktClsCode: '0',
      fidCondScrDivCode: '20234',
      fidInputIscd: '0000',
      fidDivClsCode: '0',
      fidInputPrice1: '0',
      fidInputPrice2: '0',
      fidVolCnt: '0',
      fidTrgtClsCode: '0',
      fidTrgtExlsClsCode: '0',
    });
    assertKisResponse(res);
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
  });

  it('getStockCreditBalanceTop', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockCreditBalanceTop({
      fidCondScrDivCode: '17001',
      fidInputIscd: '0000',
      fidOption: '0',
      fidCondMrktDivCode: 'J',
      fidRankSortClsCode: '0',
    });
    assertKisResponse(res);
  });

  it('getStockDividendYieldTop', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockDividendYieldTop({
      ctsArea: '',
      gb1: '0',
      upjong: '0001',
      gb2: '0',
      gb3: '0',
      fDt: ONE_MONTH_AGO,
      tDt: TODAY,
      gb4: '0',
    });
    assertKisResponse(res);
  });

  it('getStockLargeExecutionCountTop', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getStockLargeExecutionCountTop({
      fidAplyRangPrc2: '0',
      fidCondMrktDivCode: 'J',
      fidCondScrDivCode: '19090',
      fidInputIscd: '0000',
      fidRankSortClsCode: '0',
      fidDivClsCode: '0',
      fidInputPrice1: '0',
      fidAplyRangPrc1: '0',
      fidInputIscd2: '0000',
      fidTrgtExlsClsCode: '0',
      fidTrgtClsCode: '0',
      fidVolCnt: '0',
    });
    assertKisResponse(res);
  });

  it('getHtsInquiryTop20', async () => {
    const client = await getKisClient();
    const res = await client.domesticRankingAnalysis.getHtsInquiryTop20({});
    assertKisResponse(res);
  });
});
