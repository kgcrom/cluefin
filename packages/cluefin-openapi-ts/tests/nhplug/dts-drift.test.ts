import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { expect, test } from 'vitest';

// @ts-expect-error - 생성 스크립트는 타입 선언이 없는 .mjs 다.
import { typesContent } from '../../scripts/generate-types.mjs';
import * as Nhplug from '../../src/nhplug';

const packageRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

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

test('every nhplug runtime export has a declaration in the generated index.d.ts', () => {
  // 값(런타임) export 만 열거된다 — `export type` 은 여기에 나타나지 않는다.
  const runtimeExports = Object.keys(Nhplug).sort();
  expect(runtimeExports.length).toBeGreaterThan(0);

  const missing = runtimeExports.filter((name) => !declared.has(name));
  expect(missing).toEqual([]);
});

test('nhplug type-only exports are declared too', () => {
  // 타입 export 는 런타임에 열거되지 않으므로 목록을 고정해 회귀를 잡는다.
  const typeExports = [
    'NhplugAuthOptions',
    'NhplugTokenResponse',
    'NhplugTokenRevokeResponse',
    'NhplugTokenCacheEntry',
    'NhplugTokenCacheStore',
    'NhplugClientOptions',
    'NhplugEndpointDefinition',
    'NhplugMarket',
    'NhplugSocketClientOptions',
  ];

  const missing = typeExports.filter((name) => !declared.has(name));
  expect(missing).toEqual([]);
});

test('the built index.d.ts matches the generator output', () => {
  const builtPath = path.join(packageRoot, 'dist', 'types', 'index.d.ts');
  if (!fs.existsSync(builtPath)) {
    // 아직 빌드 전이면 검사할 대상이 없다.
    return;
  }
  expect(fs.readFileSync(builtPath, 'utf8')).toBe(typesContent);
});
