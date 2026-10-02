import { describe, expect, test } from 'vitest';
import type { z } from 'zod';

import { periodicReportKeyInformationEndpoints } from '../../src/dart/metadata/periodic-report-key-information';
import * as schemas from '../../src/dart/schemas/periodic-report-key-information';
import {
  DART_SAMSUNG_CORP_CODE,
  getDartClient,
  runDartIntegration,
  setupDartRateLimit,
} from '../_helpers/integration-setup';

const it = runDartIntegration ? test : test.skip;

const INPUT = { corpCode: DART_SAMSUNG_CORP_CODE, bsnsYear: '2023', reprtCode: '11011' };

// `getFooBar` → `fooBarResponseSchema` (생성기의 명명 규칙)
const schemaFor = (methodName: string): z.ZodTypeAny => {
  const base = methodName.replace(/^get/, '');
  const name = `${base.charAt(0).toLowerCase()}${base.slice(1)}ResponseSchema`;
  const schema = (schemas as unknown as Record<string, z.ZodTypeAny | undefined>)[name];
  if (!schema) throw new Error(`schema not found: ${name}`);
  return schema;
};

// 삼성전자 2023 사업보고서는 28개 모두 데이터가 있다 (2026-10 실측) — 013 을 허용하면 파라미터 오류가 가려진다.
describe('Dart PeriodicReportKeyInformation', () => {
  setupDartRateLimit();

  it.each(periodicReportKeyInformationEndpoints.map((endpoint) => endpoint.methodName))('%s', async (methodName) => {
    const endpoint = periodicReportKeyInformationEndpoints.find((item) => item.methodName === methodName);
    if (!endpoint) throw new Error(methodName);

    // responseSchema 를 붙여 호출하면 클라이언트가 실응답을 생성된 zod 스키마로 검증한다.
    const res = await getDartClient().invokeEndpoint({ ...endpoint, responseSchema: schemaFor(methodName) }, INPUT);

    expect(res.body.status).toBe('000');
    expect((res.body.list as unknown[]).length).toBeGreaterThan(0);
  });
});
