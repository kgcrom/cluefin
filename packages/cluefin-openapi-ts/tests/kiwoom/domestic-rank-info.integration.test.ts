import { describe, test } from 'vitest';

import {
  rapidlyIncreasingRemainingOrderQuantityResponseSchema,
  rapidlyIncreasingTotalSellOrdersResponseSchema,
  rapidlyIncreasingTradingVolumeResponseSchema,
  sameNetBuySellRankingResponseSchema,
  stockSpecificSecuritiesFirmRankingResponseSchema,
  topConsecutiveNetBuySellByForeignersResponseSchema,
  topCurrentDayDeviationSourcesResponseSchema,
  topCurrentDayMajorTradersResponseSchema,
  topCurrentDayTradingVolumeResponseSchema,
  topExpectedConclusionPercentageChangeResponseSchema,
  topForeignAccountGroupTradingResponseSchema,
  topForeignerInstitutionTradingResponseSchema,
  topForeignerPeriodTradingResponseSchema,
  topIntradayTradingByInvestorResponseSchema,
  topLimitExhaustionRateForeignerResponseSchema,
  topMarginRatioResponseSchema,
  topNetBuyTraderRankingResponseSchema,
  topPercentageChangeFromPreviousDayResponseSchema,
  topPreviousDayTradingVolumeResponseSchema,
  topRemainingOrderQuantityResponseSchema,
  topSecuritiesFirmTradingResponseSchema,
  topTransactionValueResponseSchema,
} from '../../src/kiwoom/schemas/domestic-rank-info';
import {
  assertKiwoomResponse,
  getKiwoomClient,
  ONE_MONTH_AGO,
  runIntegration,
  SAMSUNG,
  setupKiwoomRateLimit,
  TODAY,
} from '../_helpers/integration-setup';
import { assertKiwoomSpecConformance } from '../_helpers/kiwoom-spec-conformance';

const it = runIntegration ? test : test.skip;

describe('Kiwoom DomesticRankInfo', () => {
  setupKiwoomRateLimit();
  it('getTopRemainingOrderQuantity', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopRemainingOrderQuantity({
      mrktTp: '001',
      sortTp: '1',
      trdeQtyTp: '0000',
      stkCnd: '0',
      crdCnd: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(topRemainingOrderQuantityResponseSchema);
  });

  it('getRapidlyIncreasingRemainingOrderQuantity', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getRapidlyIncreasingRemainingOrderQuantity({
      mrktTp: '001',
      trdeTp: '1',
      sortTp: '1',
      tmTp: '0',
      trdeQtyTp: '1',
      stkCnd: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(rapidlyIncreasingRemainingOrderQuantityResponseSchema);
  });

  it('getRapidlyIncreasingTotalSellOrders', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getRapidlyIncreasingTotalSellOrders({
      mrktTp: '001',
      rtTp: '1',
      tmTp: '0',
      trdeQtyTp: '5',
      stkCnd: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(rapidlyIncreasingTotalSellOrdersResponseSchema);
  });

  it('getRapidlyIncreasingTradingVolume', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getRapidlyIncreasingTradingVolume({
      mrktTp: '000',
      sortTp: '1',
      tmTp: '2',
      trdeQtyTp: '5',
      stkCnd: '0',
      pricTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(rapidlyIncreasingTradingVolumeResponseSchema);
  });

  it('getTopPercentageChangeFromPreviousDay', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopPercentageChangeFromPreviousDay({
      mrktTp: '000',
      sortTp: '1',
      trdeQtyCnd: '0000',
      stkCnd: '0',
      crdCnd: '0',
      updownIncls: '0',
      pricCnd: '0',
      trdePricaCnd: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(topPercentageChangeFromPreviousDayResponseSchema);
  });

  it('getTopExpectedConclusionPercentageChange', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopExpectedConclusionPercentageChange({
      mrktTp: '000',
      sortTp: '1',
      trdeQtyCnd: '0',
      stkCnd: '0',
      crdCnd: '0',
      pricCnd: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(topExpectedConclusionPercentageChangeResponseSchema);
  });

  it('getTopCurrentDayTradingVolume', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopCurrentDayTradingVolume({
      mrktTp: '000',
      sortTp: '1',
      mangStkIncls: '0',
      crdTp: '0',
      trdeQtyTp: '0',
      pricTp: '0',
      trdePricaTp: '0',
      mrktOpenTp: '0',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(topCurrentDayTradingVolumeResponseSchema);
  });

  it('getTopPreviousDayTradingVolume', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopPreviousDayTradingVolume({
      mrktTp: '101',
      qryTp: '1',
      rankStrt: '1',
      rankEnd: '50',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(topPreviousDayTradingVolumeResponseSchema);
  });

  it('getTopTransactionValue', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopTransactionValue({
      mrktTp: '001',
      mangStkIncls: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(topTransactionValueResponseSchema);
  });

  it('getTopMarginRatio', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopMarginRatio({
      mrktTp: '000',
      trdeQtyTp: '0',
      stkCnd: '0',
      updownIncls: '0',
      crdCnd: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(topMarginRatioResponseSchema);
  });

  it('getTopForeignerPeriodTrading', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopForeignerPeriodTrading({
      mrktTp: '001',
      trdeTp: '2',
      dt: '0', // 기간 코드 — 날짜가 아니다
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(topForeignerPeriodTradingResponseSchema);
  });

  it('getTopConsecutiveNetBuySellByForeigners', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopConsecutiveNetBuySellByForeigners({
      mrktTp: '000',
      trdeTp: '2',
      baseDtTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(topConsecutiveNetBuySellByForeignersResponseSchema);
  });

  it('getTopLimitExhaustionRateForeigner', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopLimitExhaustionRateForeigner({
      mrktTp: '000',
      dt: '0', // 기간 코드 — 날짜가 아니다
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(topLimitExhaustionRateForeignerResponseSchema);
  });

  it('getTopForeignAccountGroupTrading', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopForeignAccountGroupTrading({
      mrktTp: '000',
      dt: '0', // 기간 코드 — 날짜가 아니다
      trdeTp: '1',
      sortTp: '2',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(topForeignAccountGroupTradingResponseSchema);
  });

  it('getStockSpecificSecuritiesFirmRanking', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getStockSpecificSecuritiesFirmRanking({
      stkCd: SAMSUNG,
      strtDt: ONE_MONTH_AGO,
      endDt: TODAY,
      qryTp: '2',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(stockSpecificSecuritiesFirmRankingResponseSchema);
  });

  it('getTopSecuritiesFirmTrading', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopSecuritiesFirmTrading({
      mmcmCd: '001',
      trdeQtyTp: '0',
      trdeTp: '1',
      dt: '1', // 기간 코드 — 날짜가 아니다
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(topSecuritiesFirmTradingResponseSchema);
  });

  it('getTopCurrentDayMajorTraders', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopCurrentDayMajorTraders({
      stkCd: SAMSUNG,
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(topCurrentDayMajorTradersResponseSchema);
  });

  it('getTopNetBuyTraderRanking', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopNetBuyTraderRanking({
      stkCd: SAMSUNG,
      strtDt: ONE_MONTH_AGO,
      endDt: TODAY,
      qryDtTp: '0',
      potTp: '0',
      dt: '5', // 기간 코드 — 날짜가 아니다
      sortBase: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(topNetBuyTraderRankingResponseSchema);
  });

  it('getTopCurrentDayDeviationSources', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopCurrentDayDeviationSources({
      stkCd: SAMSUNG,
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(topCurrentDayDeviationSourcesResponseSchema);
  });

  it('getSameNetBuySellRanking', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getSameNetBuySellRanking({
      strtDt: ONE_MONTH_AGO,
      endDt: TODAY,
      mrktTp: '000',
      trdeTp: '1',
      sortCnd: '1',
      unitTp: '1',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(sameNetBuySellRankingResponseSchema);
  });

  it('getTopForeignerInstitutionTrading', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopForeignerInstitutionTrading({
      mrktTp: '000',
      amtQtyTp: '1',
      qryDtTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    // 실측: 종목명이 문서 Length 20 을 넘는다 — VENDOR_DOC_ERRATA.md. 어느 칸에 긴 이름이 올지는 날마다 다르다
    const names = ['for_netslmt_stk_nm', 'for_netprps_stk_nm', 'orgn_netslmt_stk_nm', 'orgn_netprps_stk_nm'];
    assertKiwoomSpecConformance(topForeignerInstitutionTradingResponseSchema, {
      ignoreLength: names.map((n) => `frgnr_orgn_trde_upper.${n}`),
    });
  });

  it('getTopIntradayTradingByInvestor', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticRankInfo.getTopIntradayTradingByInvestor({
      trdeTp: '1',
      mrktTp: '000',
      orgnTp: '9000',
      amtQtyTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(topIntradayTradingByInvestorResponseSchema);
  });
});
