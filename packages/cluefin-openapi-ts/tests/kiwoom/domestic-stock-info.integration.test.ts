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

describe('Kiwoom DomesticStockInfo', () => {
  it('getStockInfo', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getStockInfo({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
  });

  it('getStockTradingMember', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getStockTradingMember({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
  });

  it('getExecution', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getExecution({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
  });

  it('getMarginTradingTrend', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getMarginTradingTrend({
      stkCd: SAMSUNG,
      dt: TODAY,
      qryTp: '0',
    });
    assertKiwoomResponse(res);
  });

  it('getDailyTradingDetails', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getDailyTradingDetails({
      stkCd: SAMSUNG,
      strtDt: ONE_MONTH_AGO,
    });
    assertKiwoomResponse(res);
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
  });

  it('getSupplyDemandConcentration', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getSupplyDemandConcentration({
      mrktTp: '0',
      prpsCnctrRt: '50',
      curPrcEntry: '0',
      prpscnt: '0',
      cycleTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getHighPer', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getHighPer({
      pertp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
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
  });

  it('getVolatilityControlEvent', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getVolatilityControlEvent({
      mrktTp: '0',
      bfMkrtTp: '0',
      motnTp: '0',
      skipStk: '0',
      trdeQtyTp: '0',
      trdePricaTp: '0',
      motnDrc: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });

  it('getDailyPreviousDayExecutionVolume', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getDailyPreviousDayExecutionVolume({
      stkCd: SAMSUNG,
      tdyPred: '0',
    });
    assertKiwoomResponse(res);
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
  });

  it('getDailyPreviousDayConclusion', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getDailyPreviousDayConclusion({
      stkCd: SAMSUNG,
      tdyPred: '0',
    });
    assertKiwoomResponse(res);
  });

  it('getInterestStockInfo', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getInterestStockInfo({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
  });

  it('getStockInfoSummary', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getStockInfoSummary({ mrktTp: '0' });
    assertKiwoomResponse(res);
  });

  it('getStockInfoV1', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getStockInfoV1({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
  });

  it('getIndustryCode', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getIndustryCode({ mrktTp: '0' });
    assertKiwoomResponse(res);
  });

  it('getMemberCompany', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getMemberCompany({});
    assertKiwoomResponse(res);
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
  });

  it('getProgramTradingStatusByStock', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticStockInfo.getProgramTradingStatusByStock({
      dt: TODAY,
      mrktTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
  });
});
