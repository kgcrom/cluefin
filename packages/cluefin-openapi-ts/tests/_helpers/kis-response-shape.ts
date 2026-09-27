import { expect } from 'vitest';
import type { z } from 'zod';
import { toCamelCase } from '../../src/core/case-convert';

// `assertResponseShape` 는 최상위 키와, 호출부가 넘긴 블록 하나만 본다. 그래서 넘기지 않은 배열 항목의
// 필드가 서버와 달라도 통과했다 (2026-09-27: 업종기간별시세 output1, 시황/공시 output).
// 이 버전은 스키마를 따라 모든 배열·객체 블록을 내려가며 대조한다 — Python tests/kis/_response_shape.py 와 같은 규칙.

type Kind = 'object' | 'array' | 'scalar';
type ZodLike = { _zod: { def: Record<string, unknown> & { type: string } } };

const WRAPPERS = new Set(['optional', 'default', 'nullable', 'prefault', 'catch', 'readonly', 'nonoptional']);

function unwrap(schema: ZodLike): { kind: Kind; shape?: Record<string, ZodLike> } {
  let current = schema;
  for (;;) {
    const def = current._zod.def;
    if (WRAPPERS.has(def.type)) {
      current = def.innerType as ZodLike;
      continue;
    }
    if (def.type === 'array') {
      const item = unwrap(def.element as ZodLike);
      return { kind: 'array', shape: item.shape };
    }
    if (def.type === 'object') {
      return { kind: 'object', shape: def.shape as Record<string, ZodLike> };
    }
    return { kind: 'scalar' };
  }
}

const rawKind = (value: unknown): Kind =>
  Array.isArray(value) ? 'array' : value && typeof value === 'object' ? 'object' : 'scalar';

/** An object as-is, or an array's rows merged (rows can omit keys); keeps the first non-empty value per key. */
function mergeRows(value: unknown): Record<string, unknown> {
  const rows = Array.isArray(value) ? value : [value];
  const merged: Record<string, unknown> = {};
  for (const row of rows) {
    if (!row || typeof row !== 'object' || Array.isArray(row)) continue;
    for (const [key, item] of Object.entries(row)) {
      const prev = merged[key];
      const empty =
        prev === undefined ||
        prev === null ||
        prev === '' ||
        (typeof prev === 'object' && Object.keys(prev).length === 0);
      if (empty) merged[key] = item;
    }
  }
  return merged;
}

/** Every difference between a camelCased KIS body and its (snake_case) schema; empty means exact match. */
export function kisResponseShapeDiff(
  body: Record<string, unknown>,
  shape: Record<string, ZodLike>,
  path = '',
): string[] {
  const problems: string[] = [];
  const claimed = new Set<string>();

  for (const [wireKey, fieldSchema] of Object.entries(shape)) {
    const key = toCamelCase(wireKey);
    claimed.add(key);
    const label = `${path}${wireKey}`;
    if (!(key in body)) {
      problems.push(`missing: ${label} (schema declares it, server did not send it)`);
      continue;
    }
    const { kind, shape: nested } = unwrap(fieldSchema);
    if (!nested) continue;
    const value = body[key];
    if (rawKind(value) !== kind) {
      problems.push(`kind: ${label} is ${rawKind(value)} on the server, schema expects ${kind}`);
      continue;
    }
    const merged = mergeRows(value);
    if (Object.keys(merged).length === 0) continue; // 빈 배열·빈 객체는 키를 판정할 수 없다
    problems.push(...kisResponseShapeDiff(merged, nested, `${label}.`));
  }

  for (const key of Object.keys(body).sort()) {
    if (!claimed.has(key)) problems.push(`extra: ${path}${key} (server sent it, schema does not declare it)`);
  }
  return problems;
}

/**
 * Fail unless a KIS body matches its response schema at every level.
 * `ignore` takes dotted wire paths (`'output.acml_vol'`) for divergences already measured and
 * recorded in the errata — justify each one at the call site.
 * `extra` keys are reported as the body has them (camelCased) — the wire name can't be recovered.
 */
export function assertKisResponseShapeDeep(
  body: Record<string, unknown>,
  responseSchema: z.ZodObject<z.ZodRawShape>,
  ignore: readonly string[] = [],
): void {
  const ignored = new Set(ignore);
  const problems = kisResponseShapeDiff(body, responseSchema.shape as unknown as Record<string, ZodLike>).filter(
    (p) => !ignored.has(p.split(' ')[1] ?? ''),
  );
  expect(problems).toEqual([]);

  // 빈 배열은 항목 키를 판정할 수 없다. 요청값이 스펙과 달라 빈 결과가 온 채로 통과하는 경우가 있어
  // (2026-09-27 시황·공시, 프로그램매매 일별) KIS_SHAPE_REPORT_EMPTY=1 로 어떤 블록이 비었는지 본다.
  if (process.env.KIS_SHAPE_REPORT_EMPTY === '1') {
    const empty = Object.entries(body)
      .filter(([, v]) => Array.isArray(v) && v.length === 0)
      .map(([k]) => k);
    if (empty.length > 0) console.warn(`[kis-shape] empty blocks: ${empty.join(', ')}`);
  }
}
