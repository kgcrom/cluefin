import { describe, test } from 'vitest';
import { assertKiwoomResponse, getKiwoomClient, runIntegration } from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('Kiwoom DomesticTheme', () => {
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
  });

  it('getThemeGroupStocks', async () => {
    const client = await getKiwoomClient();
    const res = await client.domesticTheme.getThemeGroupStocks({ themaGrpCd: '0001', stexTp: '1' });
    assertKiwoomResponse(res);
  });
});
