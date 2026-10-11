import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import { beforeAll, expect, test } from 'vitest';

import * as Root from '../../src';

/**
 * 배포되는 JS(`dist/esm`, `dist/cjs`)를 소비자처럼 연다. `dts-consumer.test.ts` 는 선언만 보고,
 * 다른 단위 테스트는 vitest 가 `src` 를 변환해 돌리므로, tsdown 설정이 바뀌어 번들에서만
 * export 가 빠지거나 CJS 가 깨지는 회귀는 여기서만 보인다.
 *
 * 별도 node 프로세스에서 패키지 이름(`cluefin-openapi`)으로 자기참조해 연다 — vitest 의
 * 모듈 변환을 거치지 않고, `package.json` 의 `exports` import/require 조건을 그대로 탄다.
 */

// vitest 는 패키지 루트를 cwd 로 실행한다. 경로를 조립하지 않고 리터럴로 둔다.
const ESM_ENTRY = 'dist/esm/index.js';
const CJS_ENTRY = 'dist/cjs/index.cjs';

const DESCRIBE_EXPORTS = 'JSON.stringify(Object.entries(m).map(([name, value]) => [name, typeof value]))';
const ESM_SCRIPT = `const m = await import('cluefin-openapi'); console.log(${DESCRIBE_EXPORTS});`;
const CJS_SCRIPT = `const m = require('cluefin-openapi'); console.log(${DESCRIBE_EXPORTS});`;

const loadExports = (args: string[]): Map<string, string> => {
  const output = execFileSync('node', args, { encoding: 'utf8', stdio: 'pipe' });
  return new Map(JSON.parse(output) as Array<[string, string]>);
};

const sortedNames = (exports: Map<string, string>): string[] => [...exports.keys()].sort();

let esmExports: Map<string, string>;
let cjsExports: Map<string, string>;

beforeAll(() => {
  // 빌드 산출물이 없으면 검사할 대상이 없다 — 스킵하지 말고 직접 뽑는다(tsdown 은 clean:false).
  if (!fs.existsSync(ESM_ENTRY) || !fs.existsSync(CJS_ENTRY)) {
    execFileSync('npx', ['tsdown', '--config', './tsdown.config.ts', '--silent'], { stdio: 'pipe' });
  }
  esmExports = loadExports(['--input-type=module', '-e', ESM_SCRIPT]);
  cjsExports = loadExports(['-e', CJS_SCRIPT]);
}, 120_000);

test('package.json 의 import/require 엔트리가 빌드 산출물을 가리킨다', () => {
  const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
  expect(pkg.exports['.'].import).toBe(`./${ESM_ENTRY}`);
  expect(pkg.exports['.'].require).toBe(`./${CJS_ENTRY}`);
  expect(pkg.main).toBe(`./${CJS_ENTRY}`);
  expect(pkg.module).toBe(`./${ESM_ENTRY}`);
});

test('ESM 과 CJS 번들이 src 배럴과 같은 이름을 export 한다', () => {
  // 다르면 dist 가 낡았거나(npm run build 후 다시 실행) 번들 설정이 export 를 떨어뜨린 것이다.
  const sourceNames = Object.keys(Root).sort();
  expect(sortedNames(esmExports)).toEqual(sourceNames);
  expect(sortedNames(cjsExports)).toEqual(sourceNames);
});

test('ESM 과 CJS 번들의 export 종류가 같다', () => {
  expect([...cjsExports.entries()].sort()).toEqual([...esmExports.entries()].sort());
});

test.each([
  'KisAuth',
  'KisHttpClient',
  'KiwoomAuth',
  'KiwoomClient',
  'NhplugAuth',
  'NhplugClient',
  'DartClient',
  'BaseWebSocketClient',
  'ApiError',
])('%s 가 번들에서 클래스(함수)로 열린다', (name) => {
  expect(esmExports.get(name)).toBe('function');
  expect(cjsExports.get(name)).toBe('function');
});
