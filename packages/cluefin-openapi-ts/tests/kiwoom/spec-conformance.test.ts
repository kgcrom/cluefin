import { afterEach, describe, expect, test, vi } from 'vitest';
import { z } from 'zod';

import {
  assertKiwoomSpecConformance,
  kiwoomLengthDiff,
  kiwoomRecordingFetch,
  kiwoomShapeDiff,
  setLastKiwoomExchangeForTest,
} from '../_helpers/kiwoom-spec-conformance';

// 헬퍼가 느슨하면 통합테스트가 스키마 회귀를 못 잡는다 — Python test_spec_conformance_unit.py 와 같은 사례.

const s = () => z.string().default('');
const rowSchema = z.object({ dt: s(), name: s() }).passthrough();
const bodySchema = z
  .object({
    return_code: z.union([z.string(), z.number()]).optional(),
    return_msg: z.string().optional(),
    cur_prc: s(),
    rows: z.array(rowSchema).default([]),
  })
  .passthrough();
type Shape = Parameters<typeof kiwoomShapeDiff>[1];
const shape = bodySchema.shape as unknown as Shape;

const raw = (overrides: Record<string, unknown> = {}) => ({
  return_code: 0,
  return_msg: '정상적으로 처리되었습니다',
  cur_prc: '+1000',
  rows: [
    { dt: '20260925', name: '삼성전자' },
    { dt: '20260924', name: '삼성전자' },
  ],
  ...overrides,
});

afterEach(() => {
  setLastKiwoomExchangeForTest(undefined);
  vi.restoreAllMocks();
});

describe('kiwoomShapeDiff', () => {
  test('exact match ignores the envelope', () => {
    expect(kiwoomShapeDiff(raw(), shape)).toEqual([]);
  });

  test('reports missing, extra and keys from any row', () => {
    const r: Record<string, unknown> = raw({
      rows: [
        { dt: '1', name: 'x' },
        { dt: '2', name: 'y', pipe1: 'z' },
      ],
      acc_trde_qty: '1',
    });
    delete r.cur_prc;
    expect(kiwoomShapeDiff(r, shape)).toEqual([
      'missing: cur_prc (schema declares it, server did not send it)',
      'extra: rows.pipe1 (server sent it, schema does not declare it)',
      'extra: acc_trde_qty (server sent it, schema does not declare it)',
    ]);
  });

  test('reports kind mismatch', () => {
    expect(kiwoomShapeDiff(raw({ rows: { dt: '1', name: 'x' } }), shape)).toEqual([
      'kind: rows is object on the server, schema expects array',
    ]);
  });

  test('collects empty arrays', () => {
    const empty: string[] = [];
    expect(kiwoomShapeDiff(raw({ rows: [] }), shape, '', empty)).toEqual([]);
    expect(empty).toEqual(['rows']);
  });
});

describe('kiwoomLengthDiff', () => {
  test('uses the longest row and counts signs', () => {
    const data = { cur_prc: '--1000', rows: [{ dt: '20260925' }, { dt: '2026092512' }] };
    expect(kiwoomLengthDiff(data, { cur_prc: 5, 'rows.dt': 8 }, 'response')).toEqual([
      'length: response cur_prc is 6 chars, spec Length is 5',
      'length: response rows.dt is 10 chars, spec Length is 8',
    ]);
  });

  test('counts characters, not bytes', () => {
    expect(kiwoomLengthDiff({ name: '가'.repeat(20) }, { name: 20 }, 'response')).toEqual([]);
  });

  test('checks request lists of scalars', () => {
    expect(kiwoomLengthDiff({ stk_cd: ['AAPL', 'TOOLONGTICKER'] }, { stk_cd: 12 }, 'request')).toEqual([
      'length: request stk_cd is 13 chars, spec Length is 12',
    ]);
  });
});

describe('assertKiwoomSpecConformance', () => {
  test('passes on a real TR within spec lengths', () => {
    setLastKiwoomExchangeForTest({ apiId: 'ka10008', body: { stk_cd: '005930' }, raw: raw() });
    assertKiwoomSpecConformance(bodySchema);
  });

  test('fails on request length from spec_lengths.json without leaking values', () => {
    setLastKiwoomExchangeForTest({ apiId: 'ka10008', body: { stk_cd: '1234567890123456789012' }, raw: raw() });
    let message = '';
    try {
      assertKiwoomSpecConformance(bodySchema);
    } catch (e) {
      message = String(e);
    }
    expect(message).toContain('length: request stk_cd is 22 chars, spec Length is 20');
    expect(message).not.toContain('1234567890123456789012');
  });

  test('ignore lists are separate', () => {
    setLastKiwoomExchangeForTest({ apiId: 'ka10008', body: { stk_cd: 'x'.repeat(21) }, raw: raw({ pipe1: 'x' }) });
    assertKiwoomSpecConformance(bodySchema, { ignore: ['pipe1'], ignoreLength: ['stk_cd'] });
    expect(() => assertKiwoomSpecConformance(bodySchema, { ignore: ['pipe1', 'stk_cd'] })).toThrow();
  });

  test('warns on empty blocks', () => {
    const warn = vi.spyOn(console, 'warn').mockImplementation(() => {});
    setLastKiwoomExchangeForTest({ apiId: 'ka99999', body: {}, raw: raw({ rows: [] }) });
    assertKiwoomSpecConformance(bodySchema);
    expect(warn).toHaveBeenCalledWith(expect.stringContaining('rows'));
  });

  test('requires a recorded exchange', () => {
    expect(() => assertKiwoomSpecConformance(bodySchema)).toThrow(/kiwoomRecordingFetch/);
  });
});

test('kiwoomRecordingFetch records api-id, request body and raw JSON', async () => {
  const body = raw();
  vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(JSON.stringify(body)));
  const res = await kiwoomRecordingFetch('https://mockapi.kiwoom.com/api/dostk/stkinfo', {
    method: 'POST',
    headers: { 'api-id': 'ka10001' },
    body: JSON.stringify({ stk_cd: '005930' }),
  });
  expect(await res.json()).toEqual(body); // 원 응답 body 를 소비하지 않는다
  setLastKiwoomExchangeForTest(undefined);
  vi.spyOn(globalThis, 'fetch').mockRejectedValue(new Error('network'));
  await expect(kiwoomRecordingFetch('https://x', {})).rejects.toThrow('network');
  expect(() => assertKiwoomSpecConformance(bodySchema)).toThrow(/kiwoomRecordingFetch/);
});
