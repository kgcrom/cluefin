import { describe, expect, it } from 'vitest';

import { DartApiError } from '../../src/core/errors';
import { silentLogger } from '../../src/core/logger';
import { DartClient } from '../../src/dart/client';
import { majorShareholderDisclosureEndpoints } from '../../src/dart/metadata/major-shareholder-disclosure';

const INPUT = { corpCode: '00126380', bgnDe: '20250101', endDe: '20250131' };

const setup = (body: unknown = { status: '000', message: '정상', list: [] }) => {
  const urls: URL[] = [];
  const fetchMock: typeof fetch = async (input) => {
    urls.push(new URL(String(input)));
    return new Response(JSON.stringify(body));
  };
  const client = new DartClient({ authKey: 'key', fetchImpl: fetchMock, logger: silentLogger, maxRetries: 0 });
  return { urls, service: client.majorShareholderDisclosure };
};

describe('majorShareholderDisclosure', () => {
  it('36개 엔드포인트가 모두 도메인 메서드로 노출된다', () => {
    const { service } = setup();
    for (const endpoint of majorShareholderDisclosureEndpoints) {
      expect(typeof (service as unknown as Record<string, unknown>)[endpoint.methodName], endpoint.methodName).toBe(
        'function',
      );
    }
  });

  it.each(
    majorShareholderDisclosureEndpoints.map((endpoint) => [endpoint.methodName, endpoint.path] as const),
  )('%s 는 %s 를 corp_code·bgn_de·end_de 로 호출한다', async (methodName, path) => {
    const { urls, service } = setup();
    const method = (service as unknown as Record<string, (input: unknown) => Promise<unknown>>)[methodName];

    await method?.(INPUT);

    expect(urls[0]?.pathname).toBe(path);
    expect(Object.fromEntries(urls[0]?.searchParams ?? [])).toEqual({
      corp_code: '00126380',
      bgn_de: '20250101',
      end_de: '20250131',
      crtfc_key: 'key',
    });
  });

  it('유형자산 양도와 영업양도는 서로 다른 경로를 쓴다', () => {
    const byName = Object.fromEntries(majorShareholderDisclosureEndpoints.map((e) => [e.methodName, e.path]));
    expect(byName.tangibleAssetTransferDecision).toBe('/api/tgastTrfDecsn.json');
    expect(byName.businessTransferDecision).toBe('/api/bsnTrfDecsn.json');
  });

  it('응답을 camelCase 로 바꾼다', async () => {
    const { service } = setup({
      status: '000',
      message: '정상',
      list: [{ rcept_no: '20250331003652', ctr_prc: '1,000,000,000', od_a_at_t: '2' }],
    });

    const response = await service.treasuryStockTrustContractDecision(INPUT);

    expect(response.body.list?.[0]).toMatchObject({ rceptNo: '20250331003652', ctrPrc: '1,000,000,000', odAAtT: '2' });
  });

  it('필수 파라미터가 빠지면 요청 없이 실패한다', async () => {
    const { urls, service } = setup();

    await expect(service.corporateLawDecision({ corpCode: '00126380' })).rejects.toBeInstanceOf(DartApiError);
    expect(urls).toHaveLength(0);
  });
});
