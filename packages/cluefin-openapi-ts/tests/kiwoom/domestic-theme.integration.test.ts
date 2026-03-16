import { describe, test } from 'vitest';

import {
  themeGroupItemSchema,
  themeGroupResponseSchema,
  themeGroupStocksItemSchema,
  themeGroupStocksResponseSchema,
} from '../../src/kiwoom/schemas/domestic-theme';
import {
  assertKiwoomResponse,
  assertResponseShape,
  getKiwoomClient,
  runIntegration,
  setupKiwoomRateLimit,
} from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('Kiwoom DomesticTheme', () => {
  setupKiwoomRateLimit();
  it('getThemeGroup', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticTheme.getThemeGroup({
      qryTp: '0',
      dateTp: '0',
      themaNm: '',
      fluPlAmtTp: '0',
      stexTp: '1',
    });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, themeGroupResponseSchema, 'themaGrp', themeGroupItemSchema);
  });

  it('getThemeGroupStocks', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticTheme.getThemeGroupStocks({ themaGrpCd: '0001', stexTp: '1' });
    assertKiwoomResponse(res);
    assertResponseShape(res.body, themeGroupStocksResponseSchema, 'themaCompStk', themeGroupStocksItemSchema);
  });
});
