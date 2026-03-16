import { describe, test } from 'vitest';

import {
  allIndustryIndexItemSchema,
  allIndustryIndexResponseSchema,
  dailyIndustryCurrentPriceDailyItemSchema,
  dailyIndustryCurrentPriceResponseSchema,
  industryCurrentPriceResponseSchema,
  industryCurrentPriceTimeItemSchema,
  industryInvestorNetBuyItemSchema,
  industryInvestorNetBuyResponseSchema,
  industryPriceBySectorItemSchema,
  industryPriceBySectorResponseSchema,
  industryProgramResponseSchema,
} from '../../src/kiwoom/schemas/domestic-sector';
import {
  assertKiwoomResponse,
  assertResponseShape,
  getKiwoomClient,
  runIntegration,
  setupKiwoomRateLimit,
  TODAY,
} from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('Kiwoom DomesticSector', () => {
  setupKiwoomRateLimit();
  it('getIndustryProgram', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticSector.getIndustryProgram({ stkCode: '001' });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, industryProgramResponseSchema);
  });

  it('getIndustryInvestorNetBuy', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticSector.getIndustryInvestorNetBuy({
      mrktTp: '0',
      amtQtyTp: '1',
      baseDt: TODAY,
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertResponseShape(
      res.body,
      industryInvestorNetBuyResponseSchema,
      'indsNetprps',
      industryInvestorNetBuyItemSchema,
    );
  });

  it('getIndustryCurrentPrice', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticSector.getIndustryCurrentPrice({
      mrktTp: '0',
      indsCd: '001',
    });
    assertKiwoomResponse(res);
    assertResponseShape(
      res.body,
      industryCurrentPriceResponseSchema,
      'indsCurPrcTm',
      industryCurrentPriceTimeItemSchema,
    );
  });

  it('getIndustryPriceBySector', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticSector.getIndustryPriceBySector({
      mrktTp: '0',
      indsCd: '001',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, industryPriceBySectorResponseSchema, 'indsStkpc', industryPriceBySectorItemSchema);
  });

  it('getAllIndustryIndex', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticSector.getAllIndustryIndex({ indsCd: '001' });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, allIndustryIndexResponseSchema, 'allIndsIdex', allIndustryIndexItemSchema);
  });

  it('getDailyIndustryCurrentPrice', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticSector.getDailyIndustryCurrentPrice({
      mrktTp: '0',
      indsCd: '001',
    });
    assertKiwoomResponse(res);
    assertResponseShape(
      res.body,
      dailyIndustryCurrentPriceResponseSchema,
      'indsCurPrcDalyRept',
      dailyIndustryCurrentPriceDailyItemSchema,
    );
  });
});
