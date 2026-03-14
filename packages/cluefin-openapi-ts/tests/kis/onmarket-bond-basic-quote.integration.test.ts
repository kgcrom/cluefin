import { describe, test } from 'vitest';
import {
  getBondAskingPriceResponseSchema,
  getBondAvgUnitPriceOutput1ItemSchema,
  getBondAvgUnitPriceOutput2ItemSchema,
  getBondAvgUnitPriceOutput3ItemSchema,
  getBondAvgUnitPriceResponseSchema,
  getBondDailyChartPriceItemSchema,
  getBondDailyChartPriceResponseSchema,
  getBondDailyPriceItemSchema,
  getBondDailyPriceResponseSchema,
  getBondExecutionItemSchema,
  getBondExecutionResponseSchema,
  getBondInfoResponseSchema,
  getBondIssueInfoResponseSchema,
  getBondPriceResponseSchema,
} from '../../src/kis/schemas/onmarket-bond-basic-quote';
import {
  assertKisResponse,
  assertResponseShape,
  getKisClient,
  runIntegration,
  TODAY,
} from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

const BOND_CODE = 'KR2033022D33';

describe('KIS OnmarketBondBasicQuote', () => {
  it('getBondPrice', async () => {
    const client = await getKisClient();
    const res = await client.onmarketBondBasicQuote.getBondPrice({
      fidInputIscd: BOND_CODE,
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getBondPriceResponseSchema);
  });

  it('getBondInfo', async () => {
    const client = await getKisClient();
    const res = await client.onmarketBondBasicQuote.getBondInfo({
      pdno: BOND_CODE,
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getBondInfoResponseSchema);
  });

  it('getBondAskingPrice', async () => {
    const client = await getKisClient();
    const res = await client.onmarketBondBasicQuote.getBondAskingPrice({
      fidInputIscd: BOND_CODE,
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getBondAskingPriceResponseSchema);
  });

  it('getBondExecution', async () => {
    const client = await getKisClient();
    const res = await client.onmarketBondBasicQuote.getBondExecution({
      fidInputIscd: BOND_CODE,
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getBondExecutionResponseSchema, 'output', getBondExecutionItemSchema);
  });

  it('getBondDailyPrice', async () => {
    const client = await getKisClient();
    const res = await client.onmarketBondBasicQuote.getBondDailyPrice({
      fidInputIscd: BOND_CODE,
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getBondDailyPriceResponseSchema, 'output', getBondDailyPriceItemSchema);
  });

  it('getBondDailyChartPrice', async () => {
    const client = await getKisClient();
    const res = await client.onmarketBondBasicQuote.getBondDailyChartPrice({
      fidInputIscd: BOND_CODE,
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getBondDailyChartPriceResponseSchema, 'output', getBondDailyChartPriceItemSchema);
  });

  it('getBondAvgUnitPrice', async () => {
    const client = await getKisClient();
    const res = await client.onmarketBondBasicQuote.getBondAvgUnitPrice({
      inqrStrtDt: TODAY,
      inqrEndDt: TODAY,
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getBondAvgUnitPriceResponseSchema);
    assertResponseShape(res.body, getBondAvgUnitPriceResponseSchema, 'output1', getBondAvgUnitPriceOutput1ItemSchema);
    assertResponseShape(res.body, getBondAvgUnitPriceResponseSchema, 'output2', getBondAvgUnitPriceOutput2ItemSchema);
    assertResponseShape(res.body, getBondAvgUnitPriceResponseSchema, 'output3', getBondAvgUnitPriceOutput3ItemSchema);
  });

  it('getBondIssueInfo', async () => {
    const client = await getKisClient();
    const res = await client.onmarketBondBasicQuote.getBondIssueInfo({
      pdno: BOND_CODE,
    });
    assertKisResponse(res);
    assertResponseShape(res.body, getBondIssueInfoResponseSchema);
  });
});
