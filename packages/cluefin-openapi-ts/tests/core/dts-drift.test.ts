import fs from 'node:fs';
import { describe, expect, test } from 'vitest';

// @ts-expect-error - 생성 스크립트는 타입 선언이 없는 .mjs 다.
import { typesContent } from '../../scripts/generate-types.mjs';
import * as Kis from '../../src/kis';
import * as Kiwoom from '../../src/kiwoom';
import * as Nhplug from '../../src/nhplug';

// vitest 는 패키지 루트를 cwd 로 실행한다. 경로를 조립하지 않고 리터럴로 둔다.
const BUILT_DTS = 'dist/types/index.d.ts';

const declaredNames = (source: string): Set<string> => {
  const names = new Set<string>();
  const pattern =
    /^export\s+(?:declare\s+)?(?:abstract\s+)?(?:class|const|function|interface|type|enum)\s+([A-Za-z0-9_$]+)/gm;
  for (const [, name] of source.matchAll(pattern)) {
    if (name) {
      names.add(name);
    }
  }
  return names;
};

const declared = declaredNames(typesContent as string);

/**
 * `dist/types/index.d.ts` 는 tsc 산출물이 아니라 `scripts/generate-types.mjs` 가
 * 문자열로 찍어 내는 파일이다. 배럴에 export 를 추가해도 생성기를 고치지 않으면
 * 런타임에는 동작하지만 소비자의 TypeScript 에는 "그런 export 없음" 으로 보인다.
 * 벤더별 배럴의 런타임 export 를 생성기 출력과 대조해 그 누락을 잡는다.
 */
const vendors: Array<{
  name: string;
  barrel: Record<string, unknown>;
  /** 런타임에 열거되지 않는 `export type` 은 목록을 고정해 회귀를 잡는다. */
  typeExports: string[];
}> = [
  {
    name: 'kis',
    barrel: Kis,
    typeExports: [
      'KisApprovalResponse',
      'KisAuthOptions',
      'KisTokenResponse',
      'KisHttpClientOptions',
      'KisSocketClientOptions',
      'TokenCacheEntry',
      'TokenCacheStore',
      'DomesticRealtimeExecutionItem',
      'DomesticRealtimeExecutionNotificationItem',
      'DomesticRealtimeOrderbookItem',
      'BondRealtimeExecutionItem',
      'BondRealtimeIndexExecutionItem',
      'BondRealtimeOrderbookItem',
      'OverseasRealtimeDelayedOrderbookItem',
      'OverseasRealtimeExecutionItem',
      'OverseasRealtimeExecutionNotificationItem',
      'OverseasRealtimeOrderbookItem',
      'OverseasAccountMethodName',
      'OverseasMarketAnalysisMethodName',
    ],
  },
  {
    name: 'kiwoom',
    barrel: Kiwoom,
    // `schemas/*` 의 응답 타입(200여 개)은 아직 선언되지 않는다 — 별도 과제.
    typeExports: ['KiwoomAuthOptions', 'KiwoomTokenResponse', 'KiwoomClientOptions'],
  },
  {
    name: 'nhplug',
    barrel: Nhplug,
    typeExports: [
      'NhplugAuthOptions',
      'NhplugTokenResponse',
      'NhplugTokenRevokeResponse',
      'NhplugTokenCacheEntry',
      'NhplugTokenCacheStore',
      'NhplugClientOptions',
      'NhplugEndpointDefinition',
      'NhplugMarket',
      'NhplugSocketClientOptions',
    ],
  },
];

describe.each(vendors)('$name barrel vs. generated index.d.ts', ({ barrel, typeExports }) => {
  test('every runtime export has a declaration', () => {
    // 값(런타임) export 만 열거된다 — `export type` 은 여기에 나타나지 않는다.
    const runtimeExports = Object.keys(barrel).sort();
    expect(runtimeExports.length).toBeGreaterThan(0);

    const missing = runtimeExports.filter((name) => !declared.has(name));
    expect(missing, `선언 누락 ${missing.length}건: ${missing.join(', ')}`).toEqual([]);
  });

  test('listed type-only exports are declared too', () => {
    const missing = typeExports.filter((name) => !declared.has(name));
    expect(missing, `타입 선언 누락 ${missing.length}건: ${missing.join(', ')}`).toEqual([]);
  });
});

test('declared *_FIELD_NAMES literal tuples match the runtime arrays', () => {
  // 리터럴 튜플로 선언하는 이상, 런타임 배열과 어긋나면 소비자 쪽에서만 조용히 틀어진다.
  const fieldNameConsts = Object.entries(Kis).filter(([name]) => name.endsWith('_FIELD_NAMES'));
  expect(fieldNameConsts.length).toBeGreaterThan(0);

  const source = typesContent as string;
  for (const [name, value] of fieldNameConsts) {
    // 정규식을 조립하지 않고 문자열로 찾는다 — 동적 RegExp 는 정적분석이 걸고 넘어진다.
    const prefix = `export declare const ${name}: readonly [`;
    const start = source.indexOf(prefix);
    expect(start, `${name} 이 리터럴 튜플로 선언되지 않았다.`).toBeGreaterThanOrEqual(0);
    const end = source.indexOf('];', start);
    const declaredFields = source
      .slice(start + prefix.length, end)
      .split(', ')
      .map((f) => f.slice(1, -1));
    expect(declaredFields, name).toEqual(value as readonly string[]);
  }
});

test('the built index.d.ts matches the generator output', () => {
  if (!fs.existsSync(BUILT_DTS)) {
    // 아직 빌드 전이면 검사할 대상이 없다.
    return;
  }
  expect(fs.readFileSync(BUILT_DTS, 'utf8')).toBe(typesContent);
});
