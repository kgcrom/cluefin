import { describe, expect, it } from 'vitest';

import { DartApiError } from '../../src/core/errors';
import { silentLogger } from '../../src/core/logger';
import { DartClient } from '../../src/dart/client';
import { periodicReportKeyInformationEndpoints } from '../../src/dart/metadata/periodic-report-key-information';

const INPUT = { corpCode: '00126380', bsnsYear: '2024', reprtCode: '11011' };

const setup = (body: unknown = { status: '000', message: '정상', list: [] }) => {
  const urls: URL[] = [];
  const fetchMock: typeof fetch = async (input) => {
    urls.push(new URL(String(input)));
    return new Response(JSON.stringify(body));
  };
  const client = new DartClient({ authKey: 'key', fetchImpl: fetchMock, logger: silentLogger, maxRetries: 0 });
  return { urls, service: client.periodicReportKeyInformation };
};

describe('periodicReportKeyInformation', () => {
  it('메타데이터의 모든 엔드포인트가 도메인 메서드로 노출된다', () => {
    const { service } = setup();
    const methods = new Map(Object.entries(service));
    for (const endpoint of periodicReportKeyInformationEndpoints) {
      expect(typeof methods.get(endpoint.methodName), endpoint.methodName).toBe('function');
    }
  });

  it.each(
    periodicReportKeyInformationEndpoints.map((endpoint) => [endpoint.methodName, endpoint.path] as const),
  )('%s 는 %s 를 corp_code·bsns_year·reprt_code 로 호출한다', async (methodName, path) => {
    const { urls, service } = setup();
    const method = new Map(Object.entries(service)).get(methodName);

    await method?.(INPUT);

    expect(urls[0]?.pathname).toBe(path);
    expect(Object.fromEntries(urls[0]?.searchParams ?? [])).toEqual({
      corp_code: '00126380',
      bsns_year: '2024',
      reprt_code: '11011',
      crtfc_key: 'key',
    });
  });

  it('경로가 중복되지 않는다', () => {
    const paths = periodicReportKeyInformationEndpoints.map((endpoint) => endpoint.path);
    expect(new Set(paths).size).toBe(paths.length);
  });

  it('대표 경로가 DART 명세와 일치한다', () => {
    const byName = Object.fromEntries(
      periodicReportKeyInformationEndpoints.map((endpoint) => [endpoint.methodName, endpoint.path]),
    );
    expect(byName.getDividendInformation).toBe('/api/alotMatter.json');
    expect(byName.getTotalNumberOfShares).toBe('/api/stockTotqySttus.json');
    expect(byName.getAuditorNameAndOpinion).toBe('/api/accnutAdtorNmNdAdtOpinion.json');
  });

  it('응답을 camelCase 로 바꾸고 null 선택 필드를 보존한다', async () => {
    const { service } = setup({
      status: '000',
      message: '정상',
      list: [{ rcept_no: '20240101000001', stock_knd: null, thstrm: '10', stlm_dt: '2024-12-31' }],
    });

    const response = await service.getDividendInformation(INPUT);

    expect(response.body.list?.[0]).toEqual({
      rceptNo: '20240101000001',
      stockKnd: null,
      thstrm: '10',
      stlmDt: '2024-12-31',
    });
  });

  it('필수 파라미터가 빠지면 요청 없이 실패한다', async () => {
    const { urls, service } = setup();

    await expect(service.getDividendInformation({ corpCode: '00126380' })).rejects.toBeInstanceOf(DartApiError);
    expect(urls).toHaveLength(0);
  });
});
