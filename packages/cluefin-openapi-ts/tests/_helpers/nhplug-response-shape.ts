import { readFileSync } from 'node:fs';
import { expect } from 'vitest';
import type { z } from 'zod';
import { toCamelCase } from '../../src/core/case-convert';

// `assertNhplugResponseShape` 는 최상위 키의 초과분만 본다. 그래서 블록 안 필드가 서버와 달라도 통과했다.
// 이 버전은 스키마를 따라 모든 배열·객체 블록을 내려가며 대조하고, 스펙 길이(`spec_lengths.json`)도 검사한다 —
// Python tests/nhplug/_response_shape.py 와 같은 규칙. `Output_N`·`message` 는 데이터가 있을 때만 오므로
// 최상위에서 빠진 것은 문제로 보지 않는다 (잘못된 이름의 블록은 extra 로 드러난다).

type Kind = 'object' | 'array' | 'scalar';
type ZodLike = { _zod: { def: Record<string, unknown> & { type: string } } };
type Shape = Record<string, ZodLike>;

const WRAPPERS = new Set(['optional', 'default', 'nullable', 'prefault', 'catch', 'readonly', 'nonoptional']);

/** Every (kind, nested shape) a schema accepts — unions (object | array) yield several. */
function candidates(schema: ZodLike): { kind: Kind; shape?: Shape }[] {
  let current = schema;
  for (;;) {
    const def = current._zod.def;
    if (WRAPPERS.has(def.type)) {
      current = def.innerType as ZodLike;
      continue;
    }
    if (def.type === 'pipe') {
      current = def.in as ZodLike;
      continue;
    }
    if (def.type === 'union') return (def.options as ZodLike[]).flatMap(candidates);
    if (def.type === 'array') {
      return candidates(def.element as ZodLike).map((item) => ({
        kind: 'array' as const,
        shape: item.shape,
      }));
    }
    if (def.type === 'object') return [{ kind: 'object', shape: def.shape as Shape }];
    return [{ kind: 'scalar' }];
  }
}

const rawKind = (value: unknown): Kind =>
  Array.isArray(value) ? 'array' : value && typeof value === 'object' ? 'object' : 'scalar';

const OPTIONAL_TOP = (wireKey: string): boolean => wireKey.startsWith('Output_') || wireKey === 'message';

/** Every difference between a camelCased NH PLUG body and its (wire-keyed) schema; empty means exact match. */
export function nhplugResponseShapeDiff(body: Record<string, unknown>, shape: Shape, path = ''): string[] {
  const problems: string[] = [];
  const claimed = new Set<string>();

  for (const [wireKey, fieldSchema] of Object.entries(shape)) {
    const key = toCamelCase(wireKey);
    claimed.add(key);
    const label = `${path}${wireKey}`;
    if (!(key in body)) {
      if (!(path === '' && OPTIONAL_TOP(wireKey))) {
        problems.push(`missing: ${label} (schema declares it, server did not send it)`);
      }
      continue;
    }
    const value = body[key];
    const nested = candidates(fieldSchema).filter((c) => c.shape);
    if (nested.length === 0 || value === null || value === undefined) continue;
    const match = nested.find((c) => c.kind === rawKind(value));
    if (!match?.shape) {
      const expected = [...new Set(nested.map((c) => c.kind))].sort().join('/');
      problems.push(`kind: ${label} is ${rawKind(value)} on the server, schema expects ${expected}`);
      continue;
    }
    // 배열은 모든 행의 키 합집합으로 본다 (행마다 빠지는 키가 있다)
    const rows = (match.kind === 'array' ? value : [value]) as Record<string, unknown>[];
    const keys = Object.fromEntries(rows.flatMap((row) => Object.keys(row ?? {})).map((k) => [k, null]));
    if (Object.keys(keys).length === 0) continue; // 빈 배열·빈 객체는 키를 판정할 수 없다
    problems.push(...nhplugResponseShapeDiff(keys, match.shape, `${label}.`));
  }

  for (const key of Object.keys(body).sort()) {
    if (!claimed.has(key)) problems.push(`extra: ${path}${key} (server sent it, schema does not declare it)`);
  }
  return problems;
}

type SpecLengths = {
  known_exceed: Record<string, Record<string, string>>;
  lengths: Record<string, { req: Record<string, string>; res: Record<string, string> }>;
};

// Python 스위트와 같은 스냅샷을 쓴다 (generate:metadata 가 Python 소스를 읽는 것과 같은 결합).
const SPEC: SpecLengths = JSON.parse(
  readFileSync(new URL('../../../cluefin-openapi/tests/nhplug/spec_lengths.json', import.meta.url), 'utf8'),
);

/**
 * How `value` exceeds `spec` ("N" or "N.M"), or null if it fits. Same rule as the Python helper:
 * numbers ignore the sign, "N.M" = N-M integer digits + M fraction digits, strings count CP949 bytes
 * (non-ASCII = 2 — Node has no CP949 encoder; Korean text, the case that matters, is exact).
 */
export function valueLength(value: unknown, spec: string): string | null {
  if (value === null || value === undefined || value === '' || typeof value === 'boolean') return null;
  if (spec.includes('.')) {
    const [total, frac] = spec.split('.').map(Number) as [number, number];
    const [wholeRaw = '', fraction = ''] = String(value).replace(/^[+-]/, '').split('.');
    const whole = wholeRaw.replace(/^0+/, '') || '0';
    return whole.length > total - frac || fraction.length > frac ? `${whole.length}.${fraction.length}` : null;
  }
  let size: number;
  if (typeof value === 'number') {
    size = String(Math.abs(value)).replace('.', '').length;
  } else {
    size = [...String(value)].reduce((n, ch) => n + ((ch.codePointAt(0) ?? 0) > 0x7f ? 2 : 1), 0);
  }
  return size > Number(spec) ? String(size) : null;
}

const sizeOf = (length: string): number[] => length.split('.').map(Number);
const larger = (a: string, b: string): boolean => {
  const [x, y] = [sizeOf(a), sizeOf(b)];
  return (x[0] ?? 0) !== (y[0] ?? 0) ? (x[0] ?? 0) > (y[0] ?? 0) : (x[1] ?? 0) > (y[1] ?? 0);
};

/** Every response value longer than the spec says, minus `known_exceed`. */
export function nhplugLengthViolations(
  apiPath: string,
  body: Record<string, unknown>,
  spec: SpecLengths = SPEC,
): string[] {
  const rules = spec.lengths[apiPath];
  if (!rules) return [];
  const known = spec.known_exceed[apiPath] ?? {};
  const worst: Record<string, string> = {};
  for (const [wireKey, length] of Object.entries(rules.res)) {
    if (wireKey in known) continue;
    const [block = '', field = ''] = wireKey.split('.');
    const value = body[toCamelCase(block)];
    const rows = (Array.isArray(value) ? value : value && typeof value === 'object' ? [value] : []) as Record<
      string,
      unknown
    >[];
    for (const row of rows) {
      const over = valueLength(row?.[toCamelCase(field)], length);
      if (over && (!(wireKey in worst) || larger(over, worst[wireKey] as string))) worst[wireKey] = over;
    }
  }
  return Object.entries(worst).map(([key, over]) => `length: ${key} is up to ${over}, spec says ${rules.res[key]}`);
}

/**
 * Fail unless an NH PLUG body matches its response schema at every level and fits the spec lengths.
 * `ignore` takes dotted wire paths (`'Output_0.iem_nm'`) for key divergences already measured and
 * recorded in the errata — justify each one at the call site. Length exceptions live in
 * `spec_lengths.json` `known_exceed`, shared with the Python suite. Request lengths are checked
 * on the Python side only (both suites send the same test inputs through the same body map).
 */
export function assertNhplugMatchesSpec(
  apiPath: string,
  body: unknown,
  responseSchema: z.ZodObject<z.ZodRawShape>,
  ignore: readonly string[] = [],
): void {
  const ignored = new Set(ignore);
  const record = body as Record<string, unknown>;
  const problems = nhplugResponseShapeDiff(record, responseSchema.shape as unknown as Shape).filter(
    (p) => !ignored.has(p.split(' ')[1] ?? ''),
  );
  problems.push(...nhplugLengthViolations(apiPath, record));
  expect(problems).toEqual([]);
}
