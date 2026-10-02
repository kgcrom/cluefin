import { describe, expect, it } from 'vitest';

import { silentLogger } from '../../src/core/logger';
import { DartClient } from '../../src/dart/client';

describe('shareDisclosureComprehensive', () => {
  it.each([
    ['largeHoldingReport', '/api/majorstock.json'],
    ['executiveMajorShareholderOwnershipReport', '/api/elestock.json'],
  ] as const)('%s 는 %s 를 corp_code 로 호출한다', async (method, path) => {
    const urls: URL[] = [];
    const fetchMock: typeof fetch = async (input) => {
      urls.push(new URL(String(input)));
      return new Response(
        JSON.stringify({ status: '000', message: '정상', list: [{ rcept_no: '1', isu_main_shrhldr: null }] }),
      );
    };
    const client = new DartClient({ authKey: 'key', fetchImpl: fetchMock, logger: silentLogger, maxRetries: 0 });

    const response = await client.shareDisclosureComprehensive[method]({ corpCode: '00126380' });

    expect(urls[0]?.pathname).toBe(path);
    expect(Object.fromEntries(urls[0]?.searchParams ?? [])).toEqual({ corp_code: '00126380', crtfc_key: 'key' });
    expect(response.body.list?.[0]).toMatchObject({ rceptNo: '1' });
  });
});
