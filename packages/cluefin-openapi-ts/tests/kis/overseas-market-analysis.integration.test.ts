import { describe, test } from 'vitest';
import {
  getBreakingNewsTitleItemSchema,
  getBreakingNewsTitleResponseSchema,
  getNewsAggregateTitleResponseSchema,
  getStockBuyExecutionStrengthTopOutput2ItemSchema,
  getStockBuyExecutionStrengthTopResponseSchema,
  getStockCollateralLoanEligibleOutput1ItemSchema,
  getStockCollateralLoanEligibleResponseSchema,
  getStockMarketCapRankOutput2ItemSchema,
  getStockMarketCapRankResponseSchema,
  getStockNewHighLowPriceOutput2ItemSchema,
  getStockNewHighLowPriceResponseSchema,
  getStockPeriodRightsInquiryItemSchema,
  getStockPeriodRightsInquiryResponseSchema,
  getStockPriceFluctuationOutput2ItemSchema,
  getStockPriceFluctuationResponseSchema,
  getStockRightsAggregateItemSchema,
  getStockRightsAggregateResponseSchema,
  getStockRiseDeclineRateOutput2ItemSchema,
  getStockRiseDeclineRateResponseSchema,
  getStockTradingAmountRankOutput2ItemSchema,
  getStockTradingAmountRankResponseSchema,
  getStockTradingIncreaseRateRankOutput2ItemSchema,
  getStockTradingIncreaseRateRankResponseSchema,
  getStockTradingTurnoverRateRankOutput2ItemSchema,
  getStockTradingTurnoverRateRankResponseSchema,
  getStockTradingVolumeRankOutput2ItemSchema,
  getStockTradingVolumeRankResponseSchema,
  getStockVolumeSurgeOutput2ItemSchema,
  getStockVolumeSurgeResponseSchema,
} from '../../src/kis/schemas/overseas-market-analysis';
import {
  assertKisResponse,
  assertResponseShape,
  getKisClient,
  ONE_MONTH_AGO,
  runIntegration,
  TODAY,
} from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('KIS OverseasMarketAnalysis', () => {
  // TODO: KIS API 이슈로 비활성화 — Python 참조 코드에서도 동일하게 주석 처리됨 (404 반환)
  test.skip('getStockPriceFluctuation', async () => {
    const client = await getKisClient();
    const res = await client.overseasMarketAnalysis.getStockPriceFluctuation({
      excd: 'NAS',
      gubn: '1',
      mixn: '0',
      volRang: '0',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockPriceFluctuationResponseSchema);
    assertResponseShape(
      res.body,
      getStockPriceFluctuationResponseSchema,
      'output2',
      getStockPriceFluctuationOutput2ItemSchema,
    );
  });

  it('getStockMarketCapRank', async () => {
    const client = await getKisClient();
    const res = await client.overseasMarketAnalysis.getStockMarketCapRank({
      excd: 'NAS',
      volRang: '0',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockMarketCapRankResponseSchema);
    assertResponseShape(
      res.body,
      getStockMarketCapRankResponseSchema,
      'output2',
      getStockMarketCapRankOutput2ItemSchema,
    );
  });

  it('getStockTradingVolumeRank', async () => {
    const client = await getKisClient();
    const res = await client.overseasMarketAnalysis.getStockTradingVolumeRank({
      excd: 'NAS',
      nday: '0',
      prc1: '0',
      prc2: '9999999',
      volRang: '0',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockTradingVolumeRankResponseSchema);
    assertResponseShape(
      res.body,
      getStockTradingVolumeRankResponseSchema,
      'output2',
      getStockTradingVolumeRankOutput2ItemSchema,
    );
  });

  it('getStockVolumeSurge', async () => {
    const client = await getKisClient();
    const res = await client.overseasMarketAnalysis.getStockVolumeSurge({
      excd: 'NAS',
      mixn: '0',
      volRang: '0',
      minx: '0',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockVolumeSurgeResponseSchema);
    assertResponseShape(res.body, getStockVolumeSurgeResponseSchema, 'output2', getStockVolumeSurgeOutput2ItemSchema);
  });

  it('getStockBuyExecutionStrengthTop', async () => {
    const client = await getKisClient();
    const res = await client.overseasMarketAnalysis.getStockBuyExecutionStrengthTop({
      excd: 'NAS',
      nday: '0',
      volRang: '0',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockBuyExecutionStrengthTopResponseSchema);
    assertResponseShape(
      res.body,
      getStockBuyExecutionStrengthTopResponseSchema,
      'output2',
      getStockBuyExecutionStrengthTopOutput2ItemSchema,
    );
  });

  it('getStockRiseDeclineRate', async () => {
    const client = await getKisClient();
    const res = await client.overseasMarketAnalysis.getStockRiseDeclineRate({
      excd: 'NAS',
      gubn: '0',
      nday: '0',
      volRang: '0',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockRiseDeclineRateResponseSchema);
    assertResponseShape(
      res.body,
      getStockRiseDeclineRateResponseSchema,
      'output2',
      getStockRiseDeclineRateOutput2ItemSchema,
    );
  });

  it('getStockNewHighLowPrice', async () => {
    const client = await getKisClient();
    const res = await client.overseasMarketAnalysis.getStockNewHighLowPrice({
      excd: 'NAS',
      gubn: '0',
      gubn2: '0',
      nday: '0',
      volRang: '0',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockNewHighLowPriceResponseSchema);
    assertResponseShape(
      res.body,
      getStockNewHighLowPriceResponseSchema,
      'output2',
      getStockNewHighLowPriceOutput2ItemSchema,
    );
  });

  it('getStockTradingAmountRank', async () => {
    const client = await getKisClient();
    const res = await client.overseasMarketAnalysis.getStockTradingAmountRank({
      excd: 'NAS',
      nday: '0',
      volRang: '0',
      prc1: '0',
      prc2: '9999999',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockTradingAmountRankResponseSchema);
    assertResponseShape(
      res.body,
      getStockTradingAmountRankResponseSchema,
      'output2',
      getStockTradingAmountRankOutput2ItemSchema,
    );
  });

  it('getStockTradingIncreaseRateRank', async () => {
    const client = await getKisClient();
    const res = await client.overseasMarketAnalysis.getStockTradingIncreaseRateRank({
      excd: 'NAS',
      nday: '0',
      volRang: '0',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockTradingIncreaseRateRankResponseSchema);
    assertResponseShape(
      res.body,
      getStockTradingIncreaseRateRankResponseSchema,
      'output2',
      getStockTradingIncreaseRateRankOutput2ItemSchema,
    );
  });

  it('getStockTradingTurnoverRateRank', async () => {
    const client = await getKisClient();
    const res = await client.overseasMarketAnalysis.getStockTradingTurnoverRateRank({
      excd: 'NAS',
      nday: '0',
      volRang: '0',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockTradingTurnoverRateRankResponseSchema);
    assertResponseShape(
      res.body,
      getStockTradingTurnoverRateRankResponseSchema,
      'output2',
      getStockTradingTurnoverRateRankOutput2ItemSchema,
    );
  });

  it('getStockPeriodRightsInquiry', async () => {
    const client = await getKisClient();
    const res = await client.overseasMarketAnalysis.getStockPeriodRightsInquiry({
      rghtTypeCd: '00',
      inqrDvsnCd: '0',
      inqrStrtDt: ONE_MONTH_AGO,
      inqrEndDt: TODAY,
      pdno: 'AAPL',
      prdtTypeCd: '512',
      ctxAreaNk50: '',
      ctxAreaFk50: '',
    });
    assertKisResponse(res);
    assertResponseShape(
      res.body,
      getStockPeriodRightsInquiryResponseSchema,
      'output',
      getStockPeriodRightsInquiryItemSchema,
    );
  });

  it('getNewsAggregateTitle', async () => {
    const client = await getKisClient();
    const res = await client.overseasMarketAnalysis.getNewsAggregateTitle({
      infoGb: '0',
      classCd: '',
      nationCd: '',
      exchangeCd: 'NAS',
      symb: 'AAPL',
      dataDt: '',
      dataTm: '',
      cts: '',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getNewsAggregateTitleResponseSchema);
  });

  it('getStockRightsAggregate', async () => {
    const client = await getKisClient();
    const res = await client.overseasMarketAnalysis.getStockRightsAggregate({
      ncod: 'US',
      symb: 'AAPL',
      stYmd: ONE_MONTH_AGO,
      edYmd: TODAY,
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockRightsAggregateResponseSchema, 'output1', getStockRightsAggregateItemSchema);
  });

  it('getStockCollateralLoanEligible', async () => {
    const client = await getKisClient();
    const res = await client.overseasMarketAnalysis.getStockCollateralLoanEligible({
      pdno: 'AAPL',
      prdtTypeCd: '512',
      inqrStrtDt: ONE_MONTH_AGO,
      inqrEndDt: TODAY,
      inqrDvsn: '0',
      natnCd: '840',
      inqrSqnDvsn: '0',
      rtDvsnCd: '0',
      rt: '0',
      loanPsblYn: '',
      ctxAreaFk100: '',
      ctxAreaNk100: '',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getStockCollateralLoanEligibleResponseSchema);
    assertResponseShape(
      res.body,
      getStockCollateralLoanEligibleResponseSchema,
      'output1',
      getStockCollateralLoanEligibleOutput1ItemSchema,
    );
  });

  it('getBreakingNewsTitle', async () => {
    const client = await getKisClient();
    const res = await client.overseasMarketAnalysis.getBreakingNewsTitle({
      fidNewsOferEntpCode: '',
      fidCondMrktClsCode: '',
      fidInputIscd: 'AAPL',
      fidTitlCntt: '',
      fidInputDate1: ONE_MONTH_AGO,
      fidInputHour1: '',
      fidRankSortClsCode: '0',
      fidInputSrno: '',
      fidCondScrDivCode: 'N',
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getBreakingNewsTitleResponseSchema, 'output', getBreakingNewsTitleItemSchema);
  });
});
