import { describe, test } from 'vitest';

import {
  consecutiveNetBuySellStatusByInstitutionForeignerResponseSchema,
  foreignInvestorTradingTrendByStockResponseSchema,
  stockInstitutionResponseSchema,
} from '../../src/kiwoom/schemas/domestic-foreign';
import {
  assertKiwoomResponse,
  getKiwoomClient,
  runIntegration,
  SAMSUNG,
  setupKiwoomRateLimit,
} from '../_helpers/integration-setup';
import { assertKiwoomSpecConformance } from '../_helpers/kiwoom-spec-conformance';

const it = runIntegration ? test : test.skip;

describe('Kiwoom DomesticForeign', () => {
  setupKiwoomRateLimit();
  it('getForeignInvestorTradingTrendByStock', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticForeign.getForeignInvestorTradingTrendByStock({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(foreignInvestorTradingTrendByStockResponseSchema);
  });

  it('getStockInstitution', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticForeign.getStockInstitution({ stkCd: SAMSUNG });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(stockInstitutionResponseSchema);
  });

  it('getConsecutiveNetBuySellStatusByInstitutionForeigner', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticForeign.getConsecutiveNetBuySellStatusByInstitutionForeigner({
      dt: '1', // 기간 코드 — 날짜가 아니다
      mrktTp: '001',
      stkIndsTp: '0',
      amtQtyTp: '1',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(consecutiveNetBuySellStatusByInstitutionForeignerResponseSchema);
  });
});
