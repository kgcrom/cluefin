import { describe, test } from 'vitest';

import {
  changeRateFromOpenResponseSchema,
  dailyPreviousDayConclusionResponseSchema,
  dailyPreviousDayExecutionVolumeResponseSchema,
  dailyTradingDetailsResponseSchema,
  dailyTradingItemsByInvestorResponseSchema,
  executionResponseSchema,
  highLowPriceApproachResponseSchema,
  highPerResponseSchema,
  industryCodeResponseSchema,
  institutionalInvestorByStockResponseSchema,
  interestStockInfoResponseSchema,
  marginTradingTrendResponseSchema,
  memberCompanyResponseSchema,
  newHighLowPriceResponseSchema,
  priceVolatilityResponseSchema,
  programTradingStatusByStockResponseSchema,
  stockInfoResponseSchema,
  stockInfoSummaryResponseSchema,
  stockInfoV1ResponseSchema,
  stockTradingMemberResponseSchema,
  supplyDemandConcentrationResponseSchema,
  top50ProgramNetBuyResponseSchema,
  totalInstitutionalInvestorByStockResponseSchema,
  tradingMemberInstantVolumeResponseSchema,
  tradingMemberSupplyDemandAnalysisResponseSchema,
  tradingVolumeRenewalResponseSchema,
  upperLowerLimitPriceResponseSchema,
  volatilityControlEventResponseSchema,
} from '../../src/kiwoom/schemas/domestic-stock-info';
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

describe('Kiwoom DomesticStockInfo', () => {
  setupKiwoomRateLimit();
  it('getStockInfo', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getStockInfo({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(stockInfoResponseSchema);
  });

  it('getStockTradingMember', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getStockTradingMember({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(stockTradingMemberResponseSchema);
  });

  it('getExecution', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getExecution({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(executionResponseSchema);
  });

  it('getMarginTradingTrend', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getMarginTradingTrend({
      stkCd: SAMSUNG,
      dt: TODAY,
      qryTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(marginTradingTrendResponseSchema);
  });

  it('getDailyTradingDetails', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getDailyTradingDetails({
      stkCd: SAMSUNG,
      strtDt: ONE_MONTH_AGO,
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(dailyTradingDetailsResponseSchema);
  });

  it('getNewHighLowPrice', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getNewHighLowPrice({
      mrktTp: '001',
      ntlTp: '1',
      highLowCloseTp: '1',
      stkCnd: '0',
      trdeQtyTp: '00000',
      crdCnd: '0',
      updownIncls: '0',
      dt: '5', // 기간(일수) — 날짜가 아니다
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(newHighLowPriceResponseSchema);
  });

  it('getUpperLowerLimitPrice', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getUpperLowerLimitPrice({
      mrktTp: '001',
      updownTp: '2', // 상승 — 상한(1)은 해당 종목이 없는 날이 많아 빈 결과로 통과했다
      sortTp: '0',
      stkCnd: '0',
      trdeQtyTp: '00000',
      crdCnd: '0',
      trdeGoldTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(upperLowerLimitPriceResponseSchema);
  });

  it('getHighLowPriceApproach', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getHighLowPriceApproach({
      highLowTp: '1',
      alaccRt: '05',
      mrktTp: '001',
      trdeQtyTp: '00000',
      stkCnd: '0',
      crdCnd: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(highLowPriceApproachResponseSchema);
  });

  it('getPriceVolatility', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getPriceVolatility({
      mrktTp: '000',
      fluTp: '1',
      tmTp: '1',
      tm: '5',
      trdeQtyTp: '00000',
      stkCnd: '0',
      crdCnd: '0',
      pricCnd: '0',
      updownIncls: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    // 실측: 문서 Length 4 인데 문서 자신의 허용값이 5자("00000") — VENDOR_DOC_ERRATA.md
    assertKiwoomSpecConformance(priceVolatilityResponseSchema, { ignoreLength: ['trde_qty_tp'] });
  });

  it('getTradingVolumeRenewal', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getTradingVolumeRenewal({
      mrktTp: '001',
      cycleTp: '5',
      trdeQtyTp: '5',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(tradingVolumeRenewalResponseSchema);
  });

  it('getSupplyDemandConcentration', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getSupplyDemandConcentration({
      mrktTp: '001',
      prpsCnctrRt: '50',
      curPrcEntry: '0',
      prpscnt: '10',
      cycleTp: '100',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    // 실측: 문서 Length 2 인데 문서 자신의 허용값이 3자("100") — VENDOR_DOC_ERRATA.md
    assertKiwoomSpecConformance(supplyDemandConcentrationResponseSchema, { ignoreLength: ['cycle_tp'] });
  });

  it('getHighPer', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getHighPer({
      pertp: '4',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(highPerResponseSchema);
  });

  it('getChangeRateFromOpen', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getChangeRateFromOpen({
      sortTp: '1',
      trdeQtyCnd: '0000',
      mrktTp: '001',
      updownIncls: '0',
      stkCnd: '0',
      crdCnd: '0',
      trdePricaCnd: '0',
      fluCnd: '1',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(changeRateFromOpenResponseSchema);
  });

  it('getTradingMemberSupplyDemandAnalysis', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getTradingMemberSupplyDemandAnalysis({
      stkCd: SAMSUNG,
      strtDt: ONE_MONTH_AGO,
      endDt: TODAY,
      qryDtTp: '0',
      potTp: '0',
      dt: '10', // 기간(일수) — 날짜가 아니다
      sortBase: '1',
      mmcmCd: '001',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(tradingMemberSupplyDemandAnalysisResponseSchema);
  });

  it('getTradingMemberInstantVolume', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getTradingMemberInstantVolume({
      stkCd: '', // 문서 요청 예시값 — 종목 지정 시 빈 결과가 잦다
      mmcmCd: '888',
      mrktTp: '0',
      qtyTp: '0',
      pricTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(tradingMemberInstantVolumeResponseSchema);
  });

  it('getVolatilityControlEvent', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getVolatilityControlEvent({
      mrktTp: '000',
      bfMkrtTp: '0',
      motnTp: '0',
      skipStk: '000000000',
      trdeQtyTp: '0',
      trdePricaTp: '0',
      motnDrc: '0',
      stexTp: '1',
      minTrdeQty: '0',
      maxTrdeQty: '100000000',
      minTrdePrica: '0',
      maxTrdePrica: '100000000',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(volatilityControlEventResponseSchema);
  });

  it('getDailyPreviousDayExecutionVolume', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getDailyPreviousDayExecutionVolume({
      stkCd: SAMSUNG,
      tdyPred: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(dailyPreviousDayExecutionVolumeResponseSchema);
  });

  it('getDailyTradingItemsByInvestor', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getDailyTradingItemsByInvestor({
      strtDt: ONE_MONTH_AGO,
      endDt: TODAY,
      trdeTp: '0',
      mrktTp: '001',
      invsrTp: '8000',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(dailyTradingItemsByInvestorResponseSchema);
  });

  it('getInstitutionalInvestorByStock', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getInstitutionalInvestorByStock({
      dt: TODAY,
      stkCd: SAMSUNG,
      amtQtyTp: '1',
      trdeTp: '0',
      unitTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(institutionalInvestorByStockResponseSchema);
  });

  it('getTotalInstitutionalInvestorByStock', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getTotalInstitutionalInvestorByStock({
      stkCd: SAMSUNG,
      strtDt: ONE_MONTH_AGO,
      endDt: TODAY,
      amtQtyTp: '1',
      trdeTp: '0',
      unitTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(totalInstitutionalInvestorByStockResponseSchema);
  });

  it('getDailyPreviousDayConclusion', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getDailyPreviousDayConclusion({
      stkCd: SAMSUNG,
      tdyPred: '1',
      ticMin: '0',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(dailyPreviousDayConclusionResponseSchema);
  });

  it('getInterestStockInfo', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getInterestStockInfo({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(interestStockInfoResponseSchema);
  });

  it('getStockInfoSummary', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getStockInfoSummary({ mrktTp: '0' });
    assertKiwoomResponse(res);
    // 실측: 종목상태 state 가 문서 Length 20 을 넘는다 — VENDOR_DOC_ERRATA.md
    assertKiwoomSpecConformance(stockInfoSummaryResponseSchema, { ignoreLength: ['list.state'] });
  });

  it('getStockInfoV1', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getStockInfoV1({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(stockInfoV1ResponseSchema);
  });

  it('getIndustryCode', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getIndustryCode({ mrktTp: '0' });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(industryCodeResponseSchema);
  });

  it('getMemberCompany', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getMemberCompany({});
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(memberCompanyResponseSchema);
  });

  it('getTop50ProgramNetBuy', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getTop50ProgramNetBuy({
      trdeUpperTp: '2',
      amtQtyTp: '1',
      mrktTp: 'P00101',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(top50ProgramNetBuyResponseSchema);
  });

  it('getProgramTradingStatusByStock', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getProgramTradingStatusByStock({
      dt: TODAY,
      mrktTp: 'P00101',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(programTradingStatusByStockResponseSchema);
  });
});
