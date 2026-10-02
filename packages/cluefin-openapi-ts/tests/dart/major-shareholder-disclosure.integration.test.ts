import { describe, expect, test } from 'vitest';
import type { z } from 'zod';

import { majorShareholderDisclosureEndpoints } from '../../src/dart/metadata/major-shareholder-disclosure';
import * as schemas from '../../src/dart/schemas/major-shareholder-disclosure';
import { getDartClient, runDartIntegration, setupDartRateLimit } from '../_helpers/integration-setup';
import { majorShareholderSamples } from './fixtures/major-shareholder-samples';

const it = runDartIntegration ? test : test.skip;

// 생성기의 명명 규칙: 메서드 `fooBar` → 스키마 `fooBarResponseSchema`
const schemaFor = (methodName: string): z.ZodTypeAny => {
  const schema = (schemas as unknown as Record<string, z.ZodTypeAny | undefined>)[`${methodName}ResponseSchema`];
  if (!schema) throw new Error(`schema not found: ${methodName}`);
  return schema;
};

// 주요사항보고서는 사건성 공시라 해당 연도에 샘플이 없을 수 있다 — 실패가 아니라 skip 으로 남긴다.
describe('Dart MajorShareholderDisclosure', () => {
  setupDartRateLimit();

  for (const endpoint of majorShareholderDisclosureEndpoints) {
    const sample = majorShareholderSamples[endpoint.methodName];
    const run = sample ? it : test.skip;

    run(endpoint.methodName, async () => {
      if (!sample) return;
      // responseSchema 를 붙여 호출하면 클라이언트가 실응답을 생성된 zod 스키마로 검증한다.
      const res = await getDartClient().invokeEndpoint(
        { ...endpoint, responseSchema: schemaFor(endpoint.methodName) },
        { corpCode: sample.corpCode, bgnDe: sample.rceptDt, endDe: sample.rceptDt },
      );

      expect(res.body.status, sample.reportName).toBe('000');
      expect((res.body.list as unknown[]).length).toBeGreaterThan(0);
    });
  }
});
