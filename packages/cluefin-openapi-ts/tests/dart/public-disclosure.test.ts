import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { DartApiError } from '../../src/core/errors';
import { silentLogger } from '../../src/core/logger';
import { DartClient } from '../../src/dart/client';
import { buildZip } from '../_helpers/zip-builder';

interface FetchCall {
  url: URL;
}

const setup = (responder: (url: URL) => Response) => {
  const calls: FetchCall[] = [];
  const fetchMock: typeof fetch = async (input) => {
    const url = new URL(String(input));
    calls.push({ url });
    return responder(url);
  };
  const client = new DartClient({ authKey: 'key', fetchImpl: fetchMock, logger: silentLogger, maxRetries: 0 });
  return { calls, client };
};

const json = (body: unknown): Response =>
  new Response(JSON.stringify(body), { status: 200, headers: { 'content-type': 'application/json' } });

const params = (call: FetchCall | undefined): Record<string, string> =>
  Object.fromEntries(call?.url.searchParams ?? []);

describe('publicDisclosure.publicDisclosureSearch', () => {
  beforeEach(() => {
    vi.useFakeTimers({ toFake: ['Date'] });
    vi.setSystemTime(new Date(2026, 9, 2, 12, 0, 0)); // 2026-10-02 (로컬)
  });
  afterEach(() => {
    vi.useRealTimers();
  });

  it('기간을 생략하면 오늘까지 89일 윈도우를 채운다', async () => {
    const { calls, client } = setup(() => json({ status: '000', message: '정상', list: [] }));

    await client.publicDisclosure.publicDisclosureSearch({ pageCount: 5 });

    expect(params(calls[0])).toEqual({
      bgn_de: '20260705',
      end_de: '20261002',
      last_reprt_at: 'N',
      page_count: '5',
      crtfc_key: 'key',
    });
    expect(calls[0]?.url.pathname).toBe('/api/list.json');
  });

  it('corpCode 만 줘도 기간 기본값을 채운다 (파이썬과 동일)', async () => {
    const { calls, client } = setup(() => json({ status: '000', message: '정상' }));

    await client.publicDisclosure.publicDisclosureSearch({ corpCode: '00126380' });

    expect(params(calls[0])).toMatchObject({ corp_code: '00126380', bgn_de: '20260705', end_de: '20261002' });
  });

  it('기간을 하나라도 주면 덮어쓰지 않는다', async () => {
    const { calls, client } = setup(() => json({ status: '000', message: '정상' }));

    await client.publicDisclosure.publicDisclosureSearch({ bgnDe: '20240101' });

    const query = params(calls[0]);
    expect(query.bgn_de).toBe('20240101');
    expect(query).not.toHaveProperty('end_de');
  });

  it('응답을 camelCase 로 돌려준다', async () => {
    const { client } = setup(() =>
      json({
        status: '000',
        message: '정상',
        page_no: 1,
        total_count: 1,
        list: [{ corp_cls: 'Y', corp_name: '삼성전자', rcept_no: '20260101000001' }],
      }),
    );

    const response = await client.publicDisclosure.publicDisclosureSearch({ corpCode: '00126380' });

    expect(response.body.list?.[0]).toMatchObject({ corpCls: 'Y', corpName: '삼성전자', rceptNo: '20260101000001' });
    expect(response.body.totalCount).toBe(1);
  });
});

describe('publicDisclosure.companyOverview', () => {
  it('corpCode 를 필수로 받아 /api/company.json 을 호출한다', async () => {
    const { calls, client } = setup(() => json({ status: '000', message: '정상', corp_name: '삼성전자' }));

    const response = await client.publicDisclosure.companyOverview({ corpCode: '00126380' });

    expect(calls[0]?.url.pathname).toBe('/api/company.json');
    expect(params(calls[0])).toEqual({ corp_code: '00126380', crtfc_key: 'key' });
    expect(response.body.corpName).toBe('삼성전자');
    await expect(client.publicDisclosure.companyOverview({})).rejects.toBeInstanceOf(DartApiError);
  });
});

describe('publicDisclosure.disclosureDocumentFile', () => {
  it('ZIP 안의 첫 XML 을 풀어 돌려준다', async () => {
    const zip = buildZip([
      { name: 'readme.txt', data: 'x' },
      { name: '20260101000001.xml', data: '<DOCUMENT>본문</DOCUMENT>' },
    ]);
    const { calls, client } = setup(() => new Response(zip));

    const response = await client.publicDisclosure.disclosureDocumentFile({ rceptNo: '20260101000001' });

    expect(calls[0]?.url.pathname).toBe('/api/document.xml');
    expect(params(calls[0])).toEqual({ rcept_no: '20260101000001', crtfc_key: 'key' });
    expect(new TextDecoder().decode(response.body)).toBe('<DOCUMENT>본문</DOCUMENT>');
  });

  it('ZIP 이 아니면 받은 그대로 돌려준다', async () => {
    const { client } = setup(() => new Response('<DOCUMENT>raw</DOCUMENT>'));

    const response = await client.publicDisclosure.disclosureDocumentFile({ rceptNo: '1' });

    expect(new TextDecoder().decode(response.body)).toBe('<DOCUMENT>raw</DOCUMENT>');
  });

  it('XML 없는 ZIP 은 DartApiError', async () => {
    const { client } = setup(() => new Response(buildZip([{ name: 'a.txt', data: 'x' }])));

    await expect(client.publicDisclosure.disclosureDocumentFile({ rceptNo: '1' })).rejects.toBeInstanceOf(DartApiError);
  });

  it('에러 XML 은 DartApiError (errorCode 보존)', async () => {
    const { client } = setup(
      () => new Response('<result><status>014</status><message>파일이 존재하지 않습니다.</message></result>'),
    );

    await expect(client.publicDisclosure.disclosureDocumentFile({ rceptNo: '1' })).rejects.toMatchObject({
      errorCode: '014',
    });
  });
});

describe('publicDisclosure.corpCode', () => {
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<result>
  <list><corp_code>00126380</corp_code><corp_name>삼성전자</corp_name><corp_eng_name>SAMSUNG ELECTRONICS CO,.LTD</corp_eng_name><stock_code>005930</stock_code><modify_date>20240101</modify_date></list>
  <list><corp_code>00000001</corp_code><corp_name>비상장</corp_name><stock_code> </stock_code><modify_date>20230101</modify_date></list>
  <list><corp_code></corp_code><corp_name>코드없음</corp_name><modify_date>20230101</modify_date></list>
</result>`;

  it('ZIP→XML 을 파싱해 status/message/list 로 돌려주고 빈 값은 생략한다', async () => {
    const { calls, client } = setup(() => new Response(buildZip([{ name: 'CORPCODE.xml', data: xml }])));

    const response = await client.publicDisclosure.corpCode();

    expect(calls[0]?.url.pathname).toBe('/api/corpCode.xml');
    expect(params(calls[0])).toEqual({ crtfc_key: 'key' });
    expect(response.body).toEqual({
      status: '000',
      message: '정상',
      list: [
        {
          corpCode: '00126380',
          corpName: '삼성전자',
          corpEngName: 'SAMSUNG ELECTRONICS CO,.LTD',
          stockCode: '005930',
          modifyDate: '20240101',
        },
        { corpCode: '00000001', corpName: '비상장', modifyDate: '20230101' },
      ],
    });
  });

  it('ZIP 이 손상됐으면 DartApiError', async () => {
    const { client } = setup(() => new Response('<html>not a zip</html>'));

    await expect(client.publicDisclosure.corpCode()).rejects.toBeInstanceOf(DartApiError);
  });
});
