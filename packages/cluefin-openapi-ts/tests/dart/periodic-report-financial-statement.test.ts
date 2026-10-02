import { describe, expect, it } from 'vitest';

import { DartApiError } from '../../src/core/errors';
import { silentLogger } from '../../src/core/logger';
import { DartClient } from '../../src/dart/client';
import { buildZip } from '../_helpers/zip-builder';

const setup = (responder: (url: URL) => Response) => {
  const urls: URL[] = [];
  const fetchMock: typeof fetch = async (input) => {
    const url = new URL(String(input));
    urls.push(url);
    return responder(url);
  };
  const client = new DartClient({ authKey: 'key', fetchImpl: fetchMock, logger: silentLogger, maxRetries: 0 });
  return { urls, service: client.periodicReportFinancialStatement };
};

const json = (body: unknown): Response => new Response(JSON.stringify(body));
const query = (url: URL | undefined): Record<string, string> => Object.fromEntries(url?.searchParams ?? []);

const ACCOUNT = { corpCode: '00126380', bsnsYear: '2024', reprtCode: '11011' };
const ACCOUNT_WIRE = { corp_code: '00126380', bsns_year: '2024', reprt_code: '11011' };

describe('periodicReportFinancialStatement JSON endpoints', () => {
  type Service = ReturnType<typeof setup>['service'];

  it.each([
    [
      'getSingleCompanyMajorAccounts',
      '/api/fnlttSinglAcnt.json',
      (s: Service) => s.getSingleCompanyMajorAccounts(ACCOUNT),
      ACCOUNT_WIRE,
    ],
    [
      'getMultiCompanyMajorAccounts',
      '/api/fnlttMultiAcnt.json',
      (s: Service) => s.getMultiCompanyMajorAccounts(ACCOUNT),
      ACCOUNT_WIRE,
    ],
    [
      'getSingleCompanyFullStatements',
      '/api/fnlttSinglAcntAll.json',
      (s: Service) => s.getSingleCompanyFullStatements({ ...ACCOUNT, fsDiv: 'OFS' }),
      { ...ACCOUNT_WIRE, fs_div: 'OFS' },
    ],
    [
      'getSingleCompanyMajorIndicators',
      '/api/fnlttSinglIndx.json',
      (s: Service) => s.getSingleCompanyMajorIndicators({ ...ACCOUNT, idxClCode: 'M210000' }),
      { ...ACCOUNT_WIRE, idx_cl_code: 'M210000' },
    ],
    [
      'getMultiCompanyMajorIndicators',
      '/api/fnlttCmpnyIndx.json',
      (s: Service) => s.getMultiCompanyMajorIndicators({ ...ACCOUNT, idxClCode: 'M220000' }),
      { ...ACCOUNT_WIRE, idx_cl_code: 'M220000' },
    ],
    [
      'getXbrlTaxonomy',
      '/api/xbrlTaxonomy.json',
      (s: Service) => s.getXbrlTaxonomy({ sjDiv: 'BS1' }),
      { sj_div: 'BS1' },
    ],
  ] as const)('%s → %s', async (_method, path, call, wire) => {
    const { urls, service } = setup(() =>
      json({ status: '000', message: '정상', list: [{ account_nm: '매출액', thstrm_amount: '1,000', ord: 1 }] }),
    );

    const response = await call(service);

    expect(urls[0]?.pathname).toBe(path);
    expect(query(urls[0])).toEqual({ ...wire, crtfc_key: 'key' });
    expect(response.body.list?.[0]).toMatchObject({ accountNm: '매출액', thstrmAmount: '1,000', ord: 1 });
  });

  it('전체 재무제표는 fsDiv 를 생략하면 CFS(연결)로 보낸다', async () => {
    const { urls, service } = setup(() => json({ status: '000', message: '정상' }));

    await service.getSingleCompanyFullStatements(ACCOUNT);

    expect(query(urls[0]).fs_div).toBe('CFS');
  });

  it('필수 파라미터가 빠지면 요청 없이 실패한다', async () => {
    const { urls, service } = setup(() => json({}));

    await expect(service.getSingleCompanyMajorAccounts({ corpCode: '00126380' })).rejects.toBeInstanceOf(DartApiError);
    expect(urls).toHaveLength(0);
  });

  it('조회 결과 없음(013)은 throw 하지 않는다', async () => {
    const { service } = setup(() => json({ status: '013', message: '조회된 데이타가 없습니다.' }));

    const response = await service.getSingleCompanyMajorAccounts(ACCOUNT);

    expect(response.body.status).toBe('013');
  });
});

describe('periodicReportFinancialStatement.downloadFinancialStatementXbrl', () => {
  const input = { rceptNo: '20240101000000', reprtCode: '11011' };

  it('ZIP 을 풀어 파일명 → 바이트 맵으로 돌려준다', async () => {
    const zip = buildZip([
      { name: 'entity00126380_2024-12-31.xbrl', data: '<xbrl>값</xbrl>' },
      { name: 'entity00126380_2024-12-31.xsd', data: '<schema/>' },
      { name: 'entity00126380_2024-12-31_lab-ko.xml', data: '<lab/>' },
    ]);
    const { urls, service } = setup(() => new Response(zip));

    const response = await service.downloadFinancialStatementXbrl(input);

    expect(urls[0]?.pathname).toBe('/api/fnlttXbrl.xml');
    expect(query(urls[0])).toEqual({ rcept_no: '20240101000000', reprt_code: '11011', crtfc_key: 'key' });
    expect([...response.body.keys()]).toEqual([
      'entity00126380_2024-12-31.xbrl',
      'entity00126380_2024-12-31.xsd',
      'entity00126380_2024-12-31_lab-ko.xml',
    ]);
    expect(new TextDecoder().decode(response.body.get('entity00126380_2024-12-31.xbrl'))).toBe('<xbrl>값</xbrl>');
  });

  it('ZIP 이 아니면 DartApiError', async () => {
    const { service } = setup(() => new Response('plain text'));

    await expect(service.downloadFinancialStatementXbrl(input)).rejects.toThrow('ZIP 파일 형식이 아닙니다');
  });

  it('에러 XML 은 status 를 errorCode 로 보존한 DartApiError', async () => {
    const { service } = setup(
      () => new Response('<result><status>012</status><message>접근할 수 없는 IP입니다.</message></result>'),
    );

    await expect(service.downloadFinancialStatementXbrl(input)).rejects.toMatchObject({
      message: '접근할 수 없는 IP입니다.',
      errorCode: '012',
    });
  });

  it('잘린 ZIP 은 DartApiError', async () => {
    const zip = buildZip([{ name: 'a.xbrl', data: 'x'.repeat(500) }]);
    const { service } = setup(() => new Response(zip.subarray(0, zip.length - 40)));

    await expect(service.downloadFinancialStatementXbrl(input)).rejects.toBeInstanceOf(DartApiError);
  });
});
