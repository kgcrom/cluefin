import { describe, test } from 'vitest';

import { assertKisResponse, getKisClient, ONE_MONTH_AGO, runIntegration, TODAY } from '../_helpers/integration-setup';

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
  });

  it('getStockMarketCapRank', async () => {
    const client = await getKisClient();
    const res = await client.overseasMarketAnalysis.getStockMarketCapRank({
      excd: 'NAS',
      volRang: '0',
    });
    assertKisResponse(res);
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
  });

  it('getStockBuyExecutionStrengthTop', async () => {
    const client = await getKisClient();
    const res = await client.overseasMarketAnalysis.getStockBuyExecutionStrengthTop({
      excd: 'NAS',
      nday: '0',
      volRang: '0',
    });
    assertKisResponse(res);
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
  });

  it('getStockTradingIncreaseRateRank', async () => {
    const client = await getKisClient();
    const res = await client.overseasMarketAnalysis.getStockTradingIncreaseRateRank({
      excd: 'NAS',
      nday: '0',
      volRang: '0',
    });
    assertKisResponse(res);
  });

  it('getStockTradingTurnoverRateRank', async () => {
    const client = await getKisClient();
    const res = await client.overseasMarketAnalysis.getStockTradingTurnoverRateRank({
      excd: 'NAS',
      nday: '0',
      volRang: '0',
    });
    assertKisResponse(res);
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
  });
});
