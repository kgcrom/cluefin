import { describe, test } from 'vitest';

import { themeGroupResponseSchema, themeGroupStocksResponseSchema } from '../../src/kiwoom/schemas/domestic-theme';
import {
  assertKiwoomResponse,
  getKiwoomClient,
  runIntegration,
  setupKiwoomRateLimit,
} from '../_helpers/integration-setup';
import { assertKiwoomSpecConformance } from '../_helpers/kiwoom-spec-conformance';

const it = runIntegration ? test : test.skip;

describe('Kiwoom DomesticTheme', () => {
  setupKiwoomRateLimit();
  it('getThemeGroup', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticTheme.getThemeGroup({
      qryTp: '0',
      // 문서 요청 예시값 (n일전, 1~99)
      dateTp: '10',
      themaNm: '',
      fluPlAmtTp: '1',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(themeGroupResponseSchema);
  });

  it('getThemeGroupStocks', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticTheme.getThemeGroupStocks({ themaGrpCd: '0001', stexTp: '1' });
    assertKiwoomResponse(res);
    assertKiwoomSpecConformance(themeGroupStocksResponseSchema);
  });
});
