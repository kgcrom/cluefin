import { describe, test } from 'vitest';

import {
  changeRateFromOpenItemSchema,
  changeRateFromOpenResponseSchema,
  dailyPreviousDayConclusionItemSchema,
  dailyPreviousDayConclusionResponseSchema,
  dailyPreviousDayExecutionVolumeItemSchema,
  dailyPreviousDayExecutionVolumeResponseSchema,
  dailyTradingDetailsItemSchema,
  dailyTradingDetailsResponseSchema,
  dailyTradingItemsByInvestorItemSchema,
  dailyTradingItemsByInvestorResponseSchema,
  executionItemSchema,
  executionResponseSchema,
  highLowPriceApproachItemSchema,
  highLowPriceApproachResponseSchema,
  highPerItemSchema,
  highPerResponseSchema,
  industryCodeItemSchema,
  industryCodeResponseSchema,
  institutionalInvestorByStockItemSchema,
  institutionalInvestorByStockResponseSchema,
  interestStockInfoItemSchema,
  interestStockInfoResponseSchema,
  marginTradingTrendItemSchema,
  marginTradingTrendResponseSchema,
  memberCompanyItemSchema,
  memberCompanyResponseSchema,
  newHighLowPriceItemSchema,
  newHighLowPriceResponseSchema,
  priceVolatilityItemSchema,
  priceVolatilityResponseSchema,
  programTradingStatusByStockItemSchema,
  programTradingStatusByStockResponseSchema,
  stockInfoResponseSchema,
  stockInfoSummaryItemSchema,
  stockInfoSummaryResponseSchema,
  stockInfoV1ResponseSchema,
  stockTradingMemberResponseSchema,
  supplyDemandConcentrationItemSchema,
  supplyDemandConcentrationResponseSchema,
  top50ProgramNetBuyItemSchema,
  top50ProgramNetBuyResponseSchema,
  totalInstitutionalInvestorByStockItemSchema,
  totalInstitutionalInvestorByStockResponseSchema,
  tradingMemberInstantVolumeItemSchema,
  tradingMemberInstantVolumeResponseSchema,
  tradingMemberSupplyDemandAnalysisItemSchema,
  tradingMemberSupplyDemandAnalysisResponseSchema,
  tradingVolumeRenewalItemSchema,
  tradingVolumeRenewalResponseSchema,
  upperLowerLimitPriceItemSchema,
  upperLowerLimitPriceResponseSchema,
  volatilityControlEventItemSchema,
  volatilityControlEventResponseSchema,
} from '../../src/kiwoom/schemas/domestic-stock-info';
import {
  assertKiwoomResponse,
  assertResponseShape,
  getKiwoomClient,
  ONE_MONTH_AGO,
  runIntegration,
  SAMSUNG,
  TODAY,
} from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('Kiwoom DomesticStockInfo', () => {
  it('getStockInfo', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getStockInfo({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, stockInfoResponseSchema);
  });

  it('getStockTradingMember', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getStockTradingMember({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, stockTradingMemberResponseSchema);
  });

  it('getExecution', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getExecution({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, executionResponseSchema, 'cntrInfr', executionItemSchema);
  });

  it('getMarginTradingTrend', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getMarginTradingTrend({
      stkCd: SAMSUNG,
      dt: TODAY,
      qryTp: '0',
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, marginTradingTrendResponseSchema, 'crdTrdeTrend', marginTradingTrendItemSchema);
  });

  it('getDailyTradingDetails', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getDailyTradingDetails({
      stkCd: SAMSUNG,
      strtDt: ONE_MONTH_AGO,
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, dailyTradingDetailsResponseSchema, 'dalyTrdeDtl', dailyTradingDetailsItemSchema);
  });

  it('getNewHighLowPrice', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getNewHighLowPrice({
      mrktTp: '0',
      ntlTp: '0',
      highLowCloseTp: '0',
      stkCnd: '0',
      trdeQtyTp: '0',
      crdCnd: '0',
      updownIncls: '0',
      dt: TODAY,
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, newHighLowPriceResponseSchema, 'ntlPric', newHighLowPriceItemSchema);
  });

  it('getUpperLowerLimitPrice', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getUpperLowerLimitPrice({
      mrktTp: '0',
      updownTp: '0',
      sortTp: '0',
      stkCnd: '0',
      trdeQtyTp: '0',
      crdCnd: '0',
      trdeGoldTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, upperLowerLimitPriceResponseSchema, 'updownPric', upperLowerLimitPriceItemSchema);
  });

  it('getHighLowPriceApproach', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getHighLowPriceApproach({
      highLowTp: '0',
      alaccRt: '5',
      mrktTp: '0',
      trdeQtyTp: '0',
      stkCnd: '0',
      crdCnd: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertResponseShape(
      res.body,
      highLowPriceApproachResponseSchema,
      'highLowPricAlacc',
      highLowPriceApproachItemSchema,
    );
  });

  it('getPriceVolatility', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getPriceVolatility({
      mrktTp: '0',
      fluTp: '0',
      tmTp: '0',
      tm: '5',
      trdeQtyTp: '0',
      stkCnd: '0',
      crdCnd: '0',
      pricCnd: '0',
      updownIncls: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, priceVolatilityResponseSchema, 'pricJmpflu', priceVolatilityItemSchema);
  });

  it('getTradingVolumeRenewal', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getTradingVolumeRenewal({
      mrktTp: '0',
      cycleTp: '0',
      trdeQtyTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, tradingVolumeRenewalResponseSchema, 'trdeQtyUpdt', tradingVolumeRenewalItemSchema);
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
    assertResponseShape(
      res.body,
      supplyDemandConcentrationResponseSchema,
      'prpsCnctr',
      supplyDemandConcentrationItemSchema,
    );
  });

  it('getHighPer', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getHighPer({
      pertp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, highPerResponseSchema, 'highLowPer', highPerItemSchema);
  });

  it('getChangeRateFromOpen', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getChangeRateFromOpen({
      sortTp: '0',
      trdeQtyCnd: '0',
      mrktTp: '0',
      updownIncls: '0',
      stkCnd: '0',
      crdCnd: '0',
      trdePricaCnd: '0',
      fluCnd: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, changeRateFromOpenResponseSchema, 'openPricPreFluRt', changeRateFromOpenItemSchema);
  });

  it('getTradingMemberSupplyDemandAnalysis', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getTradingMemberSupplyDemandAnalysis({
      stkCd: SAMSUNG,
      strtDt: ONE_MONTH_AGO,
      endDt: TODAY,
      qryDtTp: '0',
      potTp: '0',
      dt: TODAY,
      sortBase: '0',
      mmcmCd: '0000',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertResponseShape(
      res.body,
      tradingMemberSupplyDemandAnalysisResponseSchema,
      'trdeOriPrpsAnly',
      tradingMemberSupplyDemandAnalysisItemSchema,
    );
  });

  it('getTradingMemberInstantVolume', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getTradingMemberInstantVolume({
      stkCd: SAMSUNG,
      mmcmCd: '0000',
      mrktTp: '0',
      qtyTp: '0',
      pricTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertResponseShape(
      res.body,
      tradingMemberInstantVolumeResponseSchema,
      'trdeOriMontTrdeQty',
      tradingMemberInstantVolumeItemSchema,
    );
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
    assertResponseShape(res.body, volatilityControlEventResponseSchema, 'motnStk', volatilityControlEventItemSchema);
  });

  it('getDailyPreviousDayExecutionVolume', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getDailyPreviousDayExecutionVolume({
      stkCd: SAMSUNG,
      tdyPred: '1',
    });
    assertKiwoomResponse(res);
    assertResponseShape(
      res.body,
      dailyPreviousDayExecutionVolumeResponseSchema,
      'tdyPredCntrQty',
      dailyPreviousDayExecutionVolumeItemSchema,
    );
  });

  it('getDailyTradingItemsByInvestor', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getDailyTradingItemsByInvestor({
      strtDt: ONE_MONTH_AGO,
      endDt: TODAY,
      trdeTp: '0',
      mrktTp: '0',
      invsrTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertResponseShape(
      res.body,
      dailyTradingItemsByInvestorResponseSchema,
      'invsrDalyTrdeStk',
      dailyTradingItemsByInvestorItemSchema,
    );
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
    assertResponseShape(
      res.body,
      institutionalInvestorByStockResponseSchema,
      'stkInvsrOrgn',
      institutionalInvestorByStockItemSchema,
    );
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
    assertResponseShape(
      res.body,
      totalInstitutionalInvestorByStockResponseSchema,
      'stkInvsrOrgnTot',
      totalInstitutionalInvestorByStockItemSchema,
    );
  });

  it('getDailyPreviousDayConclusion', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getDailyPreviousDayConclusion({
      stkCd: SAMSUNG,
      tdyPred: '1',
      ticMin: '0',
    });
    assertKiwoomResponse(res);
    assertResponseShape(
      res.body,
      dailyPreviousDayConclusionResponseSchema,
      'tdyPredCntr',
      dailyPreviousDayConclusionItemSchema,
    );
  });

  it('getInterestStockInfo', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getInterestStockInfo({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, interestStockInfoResponseSchema, 'atnStkInfr', interestStockInfoItemSchema);
  });

  it('getStockInfoSummary', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getStockInfoSummary({ mrktTp: '0' });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, stockInfoSummaryResponseSchema, 'list', stockInfoSummaryItemSchema);
  });

  it('getStockInfoV1', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getStockInfoV1({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, stockInfoV1ResponseSchema);
  });

  it('getIndustryCode', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getIndustryCode({ mrktTp: '0' });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, industryCodeResponseSchema, 'list', industryCodeItemSchema);
  });

  it('getMemberCompany', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getMemberCompany({});
    assertKiwoomResponse(res);
    assertResponseShape(res.body, memberCompanyResponseSchema, 'list', memberCompanyItemSchema);
  });

  it('getTop50ProgramNetBuy', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getTop50ProgramNetBuy({
      trdeUpperTp: '0',
      amtQtyTp: '1',
      mrktTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, top50ProgramNetBuyResponseSchema, 'prmNetprpsUpper50', top50ProgramNetBuyItemSchema);
  });

  it('getProgramTradingStatusByStock', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getProgramTradingStatusByStock({
      dt: TODAY,
      mrktTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertResponseShape(
      res.body,
      programTradingStatusByStockResponseSchema,
      'stkPrmTrdePrst',
      programTradingStatusByStockItemSchema,
    );
  });
});
