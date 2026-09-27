import { describe, test } from 'vitest';

import {
  allIndustryIndexResponseSchema,
  dailyIndustryCurrentPriceResponseSchema,
  industryCurrentPriceResponseSchema,
  industryInvestorNetBuyResponseSchema,
  industryPriceBySectorResponseSchema,
  industryProgramResponseSchema,
} from '../../src/kiwoom/schemas/domestic-sector';
import {
  assertKiwoomResponse,
  getKiwoomClient,
  runIntegration,
  setupKiwoomRateLimit,
  TODAY,
} from '../_helpers/integration-setup';
import { assertKiwoomSpecConformance } from '../_helpers/kiwoom-spec-conformance';

const it = runIntegration ? test : test.skip;

describe('Kiwoom DomesticSector', () => {
  setupKiwoomRateLimit();
  it('getIndustryProgram', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticSector.getIndustryProgram({ stkCd: '001' });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(industryProgramResponseSchema);
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
    assertKiwoomSpecConformance(industryInvestorNetBuyResponseSchema);
  });

  it('getIndustryCurrentPrice', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticSector.getIndustryCurrentPrice({
      mrktTp: '0',
      indsCd: '001',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(industryCurrentPriceResponseSchema);
  });

  it('getIndustryPriceBySector', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticSector.getIndustryPriceBySector({
      mrktTp: '0',
      indsCd: '001',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(industryPriceBySectorResponseSchema);
  });

  it('getAllIndustryIndex', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticSector.getAllIndustryIndex({ indsCd: '001' });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(allIndustryIndexResponseSchema);
  });

  it('getDailyIndustryCurrentPrice', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticSector.getDailyIndustryCurrentPrice({
      mrktTp: '0',
      indsCd: '001',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(dailyIndustryCurrentPriceResponseSchema);
  });
});
