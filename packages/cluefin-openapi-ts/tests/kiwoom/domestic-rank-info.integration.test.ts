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

describe('Kiwoom DomesticRankInfo', () => {
  it('getTopRemainingOrderQuantity', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopRemainingOrderQuantity({
      mrktTp: '0',
      sortTp: '0',
      trdeQtyTp: '0',
      stkCnd: '0',
      crdCnd: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getRapidlyIncreasingRemainingOrderQuantity', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getRapidlyIncreasingRemainingOrderQuantity({
      mrktTp: '0',
      trdeTp: '0',
      sortTp: '0',
      tmTp: '0',
      trdeQtyTp: '0',
      stkCnd: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getRapidlyIncreasingTotalSellOrders', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getRapidlyIncreasingTotalSellOrders({
      mrktTp: '0',
      rtTp: '0',
      tmTp: '0',
      trdeQtyTp: '0',
      stkCnd: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getRapidlyIncreasingTradingVolume', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getRapidlyIncreasingTradingVolume({
      mrktTp: '0',
      sortTp: '0',
      tmTp: '0',
      trdeQtyTp: '0',
      stkCnd: '0',
      pricTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getTopPercentageChangeFromPreviousDay', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopPercentageChangeFromPreviousDay({
      mrktTp: '0',
      sortTp: '1',
      trdeQtyCnd: '0',
      stkCnd: '0',
      crdCnd: '0',
      updownIncls: '0',
      pricCnd: '0',
      trdePricaCnd: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getTopExpectedConclusionPercentageChange', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopExpectedConclusionPercentageChange({
      mrktTp: '0',
      sortTp: '0',
      trdeQtyCnd: '0',
      stkCnd: '0',
      crdCnd: '0',
      pricCnd: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getTopCurrentDayTradingVolume', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopCurrentDayTradingVolume({
      mrktTp: '0',
      sortTp: '1',
      mangStkIncls: '0',
      crdTp: '0',
      trdeQtyTp: '0',
      pricTp: '0',
      trdePricaTp: '0',
      mrktOpenTp: '0',
    });
    assertKiwoomResponse(res);
  });

  it('getTopPreviousDayTradingVolume', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopPreviousDayTradingVolume({
      mrktTp: '0',
      qryTp: '0',
      rankStrt: '1',
      rankEnd: '50',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getTopTransactionValue', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopTransactionValue({
      mrktTp: '0',
      mangStkIncls: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getTopMarginRatio', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopMarginRatio({
      mrktTp: '0',
      trdeQtyTp: '0',
      stkCnd: '0',
      updownIncls: '0',
      crdCnd: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getTopForeignerPeriodTrading', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopForeignerPeriodTrading({
      mrktTp: '0',
      trdeTp: '0',
      dt: TODAY,
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getTopConsecutiveNetBuySellByForeigners', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopConsecutiveNetBuySellByForeigners({
      mrktTp: '0',
      trdeTp: '0',
      baseDtTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getTopLimitExhaustionRateForeigner', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopLimitExhaustionRateForeigner({
      mrktTp: '0',
      dt: TODAY,
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getTopForeignAccountGroupTrading', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopForeignAccountGroupTrading({
      mrktTp: '0',
      dt: TODAY,
      trdeTp: '0',
      sortTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getStockSpecificSecuritiesFirmRanking', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getStockSpecificSecuritiesFirmRanking({
      stkCd: SAMSUNG,
      strtDt: ONE_MONTH_AGO,
      endDt: TODAY,
      qryTp: '0',
    });
    assertKiwoomResponse(res);
  });

  it('getTopSecuritiesFirmTrading', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopSecuritiesFirmTrading({
      mmcmCd: '0000',
      trdeQtyTp: '0',
      trdeTp: '0',
      dt: TODAY,
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getTopCurrentDayMajorTraders', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopCurrentDayMajorTraders({
      stkCd: SAMSUNG,
    });
    assertKiwoomResponse(res);
  });

  it('getTopNetBuyTraderRanking', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopNetBuyTraderRanking({
      stkCd: SAMSUNG,
      strtDt: ONE_MONTH_AGO,
      endDt: TODAY,
      qryDtTp: '0',
      potTp: '0',
      dt: TODAY,
      sortBase: '0',
    });
    assertKiwoomResponse(res);
  });

  it('getTopCurrentDayDeviationSources', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopCurrentDayDeviationSources({
      stkCd: SAMSUNG,
    });
    assertKiwoomResponse(res);
  });

  it('getSameNetBuySellRanking', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getSameNetBuySellRanking({
      strtDt: ONE_MONTH_AGO,
      endDt: TODAY,
      mrktTp: '0',
      trdeTp: '0',
      sortCnd: '0',
      unitTp: '1',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getAfterHoursSinglePriceChangeRateRanking', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getAfterHoursSinglePriceChangeRateRanking({
      mrktTp: '0',
      sortBase: '0',
      stkCnd: '0',
      trdeQtyCnd: '0',
      crdCnd: '0',
      trdePrica: '0',
    });
    assertKiwoomResponse(res);
  });

  it('getTopForeignerLimitExhaustionRate', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopForeignerLimitExhaustionRate({
      mrktTp: '0',
      dt: TODAY,
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });
});
