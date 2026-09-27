import { readFileSync } from 'node:fs';
import { expect } from 'vitest';
import type { z } from 'zod';

// 키움 통합테스트용 스펙 대조 — Python tests/kiwoom/_spec_conformance.py 와 같은 규칙.
// `assertResponseShape` 는 최상위 키와 호출부가 넘긴 블록 하나의 **첫 행**만 봐서, 다른 블록·다른 행의 차이와
// 요청·응답 길이를 못 잡았다. 여기선 fetch 를 감싸 wire 원문(snake_case)을 잡아 스키마 전체와 대조하고,
// 포털 Length(cluefin-openapi/tests/kiwoom/spec_lengths.json — Python 과 같은 파일)와 비교한다.
// 실패 메시지엔 값을 넣지 않는다 (계좌 TR 원문엔 계좌번호가 섞인다).

type Kind = 'object' | 'array' | 'scalar';
type ZodLike = { _zod: { def: Record<string, unknown> & { type: string } } };
type Lengths = Record<string, number>;

const SPEC_LENGTHS: Record<string, { request?: Lengths; response?: Lengths }> = JSON.parse(
  readFileSync(new URL('../../../cluefin-openapi/tests/kiwoom/spec_lengths.json', import.meta.url), 'utf8'),
);

// 응답 봉투 — 스키마는 envelope 로 선언하지만 판정 대상이 아니다.
const ENVELOPE_KEYS = new Set(['return_code', 'return_msg']);

interface KiwoomExchange {
  apiId: string | undefined;
  body: Record<string, unknown>;
  raw: unknown;
}

let lastExchange: KiwoomExchange | undefined;

/** `KiwoomClient` 의 `fetchImpl` 로 넘긴다. 마지막 요청 body 와 응답 JSON 원문을 남긴다. */
export const kiwoomRecordingFetch: typeof fetch = async (input, init) => {
  lastExchange = undefined;
  const response = await globalThis.fetch(input, init);
  const headers = new Headers(init?.headers);
  let raw: unknown;
  try {
    raw = await response.clone().json();
  } catch {
    raw = undefined;
  }
  lastExchange = {
    apiId: headers.get('api-id') ?? undefined,
    body: typeof init?.body === 'string' ? JSON.parse(init.body) : {},
    raw,
  };
  return response;
};

const WRAPPERS = new Set(['optional', 'default', 'nullable', 'prefault', 'catch', 'readonly', 'nonoptional']);

function unwrap(schema: ZodLike): { kind: Kind; shape?: Record<string, ZodLike> } {
  let current = schema;
  for (;;) {
    const def = current._zod.def;
    if (WRAPPERS.has(def.type)) {
      current = def.innerType as ZodLike;
      continue;
    }
    if (def.type === 'array') return { kind: 'array', shape: unwrap(def.element as ZodLike).shape };
    if (def.type === 'object') return { kind: 'object', shape: def.shape as Record<string, ZodLike> };
    return { kind: 'scalar' };
  }
}

const rawKind = (value: unknown): Kind =>
  Array.isArray(value) ? 'array' : value && typeof value === 'object' ? 'object' : 'scalar';

/** Every difference between wire keys and a (snake_case) schema; `empty` collects empty array blocks. */
export function kiwoomShapeDiff(
  raw: Record<string, unknown>,
  shape: Record<string, ZodLike>,
  path = '',
  empty: string[] = [],
): string[] {
  const problems: string[] = [];
  const claimed = new Set<string>(path ? [] : ENVELOPE_KEYS);
  for (const [key, fieldSchema] of Object.entries(shape)) {
    claimed.add(key);
    if (!path && ENVELOPE_KEYS.has(key)) continue;
    const label = `${path}${key}`;
    if (!(key in raw)) {
      problems.push(`missing: ${label} (schema declares it, server did not send it)`);
      continue;
    }
    const { kind, shape: nested } = unwrap(fieldSchema);
    if (!nested) continue;
    const value = raw[key];
    if (rawKind(value) !== kind) {
      problems.push(`kind: ${label} is ${rawKind(value)} on the server, schema expects ${kind}`);
      continue;
    }
    const rows = (kind === 'array' ? value : [value]) as Record<string, unknown>[];
    const keys = Object.fromEntries(rows.flatMap((row) => Object.keys(row)).map((k) => [k, null]));
    if (Object.keys(keys).length === 0) {
      empty.push(label);
      continue;
    }
    problems.push(...kiwoomShapeDiff(keys, nested, `${label}.`, empty));
  }
  for (const key of Object.keys(raw).sort()) {
    if (!claimed.has(key)) problems.push(`extra: ${path}${key} (server sent it, schema does not declare it)`);
  }
  return problems;
}

const scalarLen = (v: unknown): number | undefined =>
  v === null || v === undefined || typeof v === 'object' ? undefined : [...String(v)].length;

/** Fields longer than the spec Length (character count). Array blocks use the longest value over all rows. */
export function kiwoomLengthDiff(data: Record<string, unknown>, lengths: Lengths, side: string): string[] {
  const observed = new Map<string, number>();
  const note = (label: string, v: unknown) => {
    const n = scalarLen(v);
    if (n !== undefined) observed.set(label, Math.max(observed.get(label) ?? 0, n));
  };
  for (const [key, value] of Object.entries(data)) {
    if (!Array.isArray(value)) {
      note(key, value);
      continue;
    }
    for (const row of value) {
      if (row && typeof row === 'object') {
        for (const [child, v] of Object.entries(row)) note(`${key}.${child}`, v);
      } else note(key, row);
    }
  }
  return [...observed.entries()]
    .filter(([label, n]) => lengths[label] !== undefined && n > (lengths[label] as number))
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([label, n]) => `length: ${side} ${label} is ${n} chars, spec Length is ${lengths[label]}`);
}

const problemKey = (p: string): string => {
  const parts = p.split(' ');
  return (parts[0] === 'length:' ? parts[2] : parts[1]) ?? '';
};

/**
 * 마지막 키움 호출의 원문이 스키마(키)·포털 스펙(Length)에 맞지 않으면 실패한다.
 * `ignore`(키)·`ignoreLength`(길이)는 wire 경로(`'stk_frgnr.dt'`) — 실측해 VENDOR_DOC_ERRATA.md 에 적은 건만,
 * 호출부에 근거 주석과 함께.
 */
export function assertKiwoomSpecConformance(
  responseSchema: z.ZodObject<z.ZodRawShape>,
  options: { ignore?: readonly string[]; ignoreLength?: readonly string[] } = {},
): void {
  const exchange = lastExchange;
  if (!exchange || !exchange.raw || typeof exchange.raw !== 'object') {
    throw new Error('no recorded Kiwoom exchange; was the client built with kiwoomRecordingFetch?');
  }
  const raw = exchange.raw as Record<string, unknown>;
  const spec = SPEC_LENGTHS[exchange.apiId ?? ''] ?? {};
  const empty: string[] = [];
  const ignored = new Set(options.ignore ?? []);
  const ignoredLength = new Set(options.ignoreLength ?? []);
  const shape = kiwoomShapeDiff(raw, responseSchema.shape as unknown as Record<string, ZodLike>, '', empty);
  const lengths = [
    ...kiwoomLengthDiff(exchange.body, spec.request ?? {}, 'request'),
    ...kiwoomLengthDiff(raw, spec.response ?? {}, 'response'),
  ];
  const problems = [
    ...shape.filter((p) => !ignored.has(problemKey(p))),
    ...lengths.filter((p) => !ignoredLength.has(problemKey(p))),
  ];
  if (empty.length > 0) {
    console.warn(`[kiwoom-spec] ${exchange.apiId}: empty blocks, item keys/lengths unchecked: ${empty.join(', ')}`);
  }
  // 목록을 메시지에 풀어 쓴다 — toEqual([]) 는 긴 배열을 `[ Array(n) ]` 로 줄여 무엇이 틀렸는지 안 보인다
  if (problems.length > 0) {
    expect.fail(`${exchange.apiId} does not match the spec:\n${problems.map((p) => `  - ${p}`).join('\n')}`);
  }
}

/** 단위 테스트 전용 — 기록된 교환을 직접 넣는다. */
export function setLastKiwoomExchangeForTest(exchange: KiwoomExchange | undefined): void {
  lastExchange = exchange;
}
