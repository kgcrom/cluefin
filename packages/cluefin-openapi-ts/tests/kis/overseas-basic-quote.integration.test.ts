import { describe, test } from 'vitest';
import {
  getConclusionTrendOutput2ItemSchema,
  getConclusionTrendResponseSchema,
  getCurrentPriceFirstQuoteResponseSchema,
  getIndexMinuteChartOutput2ItemSchema,
  getIndexMinuteChartResponseSchema,
  getItemIndexExchangePeriodPriceOutput2ItemSchema,
  getItemIndexExchangePeriodPriceResponseSchema,
  getProductBaseInfoResponseSchema,
  getSectorCodesOutput2ItemSchema,
  getSectorCodesResponseSchema,
  getSectorPriceOutput2ItemSchema,
  getSectorPriceResponseSchema,
  getSettlementDateItemSchema,
  getSettlementDateResponseSchema,
  getStockCurrentPriceConclusionResponseSchema,
  getStockCurrentPriceDetailResponseSchema,
  getStockMinuteChartOutput2ItemSchema,
  getStockMinuteChartResponseSchema,
  getStockPeriodQuoteOutput2ItemSchema,
  getStockPeriodQuoteResponseSchema,
  searchByConditionOutput2ItemSchema,
  searchByConditionResponseSchema,
} from '../../src/kis/schemas/overseas-basic-quote';
import {
  assertKisResponse,
  assertResponseShape,
  getKisClient,
  ONE_MONTH_AGO,
  runIntegration,
  TODAY,
} from '../_helpers/integration-setup';
import { assertKisResponseShapeDeep } from '../_helpers/kis-response-shape';

const it = runIntegration ? test : test.skip;

// 문서 표에는 있지만 실서버가 보내지 않는다 — VENDOR_DOC_ERRATA.md KIS
const PERIOD_PRICE_DOC_ONLY = ['output1.prdy_vol'];

describe('KIS OverseasBasicQuote', () => {
  it('getStockCurrentPriceDetail', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.getStockCurrentPriceDetail({
      auth: '',
      excd: 'NAS',
      symb: 'AAPL',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getStockCurrentPriceDetailResponseSchema);
  });

  it('getStockPeriodQuote', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.getStockPeriodQuote({
      auth: '',
      excd: 'NAS',
      symb: 'AAPL',
      gubn: '0',
      bymd: TODAY,
      modp: '0',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getStockPeriodQuoteResponseSchema);
    assertResponseShape(res.body, getStockPeriodQuoteResponseSchema, 'output2', getStockPeriodQuoteOutput2ItemSchema);
  });

  it('getProductBaseInfo', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.getProductBaseInfo({
      prdtTypeCd: '512',
      pdno: 'AAPL',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getProductBaseInfoResponseSchema);
  });

  it('getCurrentPriceFirstQuote', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.getCurrentPriceFirstQuote({
      excd: 'NAS',
      symb: 'AAPL',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getCurrentPriceFirstQuoteResponseSchema);
  });

  it('getStockCurrentPriceConclusion', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.getStockCurrentPriceConclusion({
      auth: '',
      excd: 'NAS',
      symb: 'AAPL',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getStockCurrentPriceConclusionResponseSchema);
  });

  it('getConclusionTrend', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.getConclusionTrend({
      excd: 'NAS',
      auth: '',
      keyb: '',
      tday: '1',
      symb: 'AAPL',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getConclusionTrendResponseSchema);
    assertResponseShape(res.body, getConclusionTrendResponseSchema, 'output2', getConclusionTrendOutput2ItemSchema);
  });

  it('getStockMinuteChart', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.getStockMinuteChart({
      auth: '',
      excd: 'NAS',
      symb: 'AAPL',
      nmin: '1',
      pinc: '0',
      next: '',
      nrec: '20',
      fill: '0',
      keyb: '',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getStockMinuteChartResponseSchema);
    assertResponseShape(res.body, getStockMinuteChartResponseSchema, 'output2', getStockMinuteChartOutput2ItemSchema);
  });

  it('getIndexMinuteChart', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.getIndexMinuteChart({
      fidCondMrktDivCode: 'N',
      fidInputIscd: 'COMP',
      fidHourClsCode: '1',
      fidPwDataIncuYn: 'N',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getIndexMinuteChartResponseSchema);
    assertResponseShape(res.body, getIndexMinuteChartResponseSchema, 'output2', getIndexMinuteChartOutput2ItemSchema);
  });

  it('getItemIndexExchangePeriodPrice', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.getItemIndexExchangePeriodPrice({
      fidCondMrktDivCode: 'N',
      fidInputIscd: 'COMP',
      fidInputDate1: ONE_MONTH_AGO,
      fidInputDate2: TODAY,
      fidPeriodDivCode: 'D',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getItemIndexExchangePeriodPriceResponseSchema, PERIOD_PRICE_DOC_ONLY);
    assertResponseShape(
      res.body,
      getItemIndexExchangePeriodPriceResponseSchema,
      'output2',
      getItemIndexExchangePeriodPriceOutput2ItemSchema,
    );
  });

  it('searchByCondition', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.searchByCondition({
      auth: '',
      excd: 'NAS',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, searchByConditionResponseSchema);
    assertResponseShape(res.body, searchByConditionResponseSchema, 'output2', searchByConditionOutput2ItemSchema);
  });

  it('getSettlementDate', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.getSettlementDate({
      tradDt: TODAY,
      ctxAreaNk: '',
      ctxAreaFk: '',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getSettlementDateResponseSchema);
    assertResponseShape(res.body, getSettlementDateResponseSchema, 'output', getSettlementDateItemSchema);
  });

  it('getSectorPrice', async () => {
    const client = await getKisClient();
    // 스펙: ICOD 필수, 업종코드별조회(HHDFS76370100)로 얻은 값. 공백을 주면 빈 결과로 형태 검사가 비었다
    const codes = await client.overseasBasicQuote.getSectorCodes({ auth: '', excd: 'NAS' });
    const icod = (codes.body.output2 as { icod: string }[])[0]?.icod ?? '';
    const res = await client.overseasBasicQuote.getSectorPrice({
      keyb: '',
      auth: '',
      excd: 'NAS',
      icod,
      volRang: '0',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getSectorPriceResponseSchema);
    assertResponseShape(res.body, getSectorPriceResponseSchema, 'output2', getSectorPriceOutput2ItemSchema);
  });

  it('getSectorCodes', async () => {
    const client = await getKisClient();
    const res = await client.overseasBasicQuote.getSectorCodes({
      auth: '',
      excd: 'NAS',
    });
    assertKisResponse(res);
    assertKisResponseShapeDeep(res.body, getSectorCodesResponseSchema);
    assertResponseShape(res.body, getSectorCodesResponseSchema, 'output2', getSectorCodesOutput2ItemSchema);
  });
});
