import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import ts from 'typescript';
import { beforeAll, describe, expect, test } from 'vitest';

import * as Kis from '../../src/kis';
import * as Kiwoom from '../../src/kiwoom';
import * as Nhplug from '../../src/nhplug';

/**
 * `dist/types` 는 이제 `tsc -p tsconfig.build.json` 산출물이다(수기 템플릿 폐지).
 * 그래서 "선언을 빠뜨렸는가" 는 구조적으로 불가능해졌고, 대신 확인할 것이 바뀌었다:
 * 배포되는 선언이 **소비자 쪽에서 실제로 해석·컴파일되는가**.
 *
 * 두 가지를 본다.
 *   1. `package.json` 의 `exports["."].types` 로 import 하는 픽스처가 `tsc` 를 통과하는가.
 *      — **moduleResolution 두 가지 모두**로 본다. Bundler 만 보면 확장자 없는 상대
 *      지정자가 통과해 버려서, node16/nodenext 소비자에서만 터지는 회귀(TS2834 →
 *      전 export TS2305)를 놓친다. 실제로 그렇게 한 번 놓쳤다.
 *   2. 벤더 배럴의 런타임 export 가 선언 표면에 전부 있는가(엔트리 배럴 누락 방지).
 */

const packageRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const declarationEntry = path.join(packageRoot, 'dist', 'types', 'index.d.ts');
const consumerDir = path.join(packageRoot, 'tests', 'fixtures', 'dts-consumer');
const consumerProjects = [
  { mode: 'Bundler', project: path.join(consumerDir, 'tsconfig.json') },
  { mode: 'NodeNext', project: path.join(consumerDir, 'tsconfig.nodenext.json') },
] as const;

const buildDeclarations = (): void => {
  execFileSync('npx', ['tsc', '-p', 'tsconfig.build.json'], { cwd: packageRoot, stdio: 'pipe' });
};

const exportedNames = (entry: string): Set<string> => {
  const program = ts.createProgram([entry], {
    skipLibCheck: true,
    moduleResolution: ts.ModuleResolutionKind.Bundler,
    target: ts.ScriptTarget.ES2022,
    strict: true,
  });
  const source = program.getSourceFile(entry);
  const moduleSymbol = source && program.getTypeChecker().getSymbolAtLocation(source);
  if (!moduleSymbol) {
    throw new Error(`선언 엔트리를 모듈로 해석하지 못했다: ${entry}`);
  }
  return new Set(
    program
      .getTypeChecker()
      .getExportsOfModule(moduleSymbol)
      .map((symbol) => symbol.getName()),
  );
};

beforeAll(() => {
  // 빌드 산출물이 없으면 검사할 대상이 없다 — 스킵하지 말고 직접 뽑는다(1~2초).
  if (!fs.existsSync(declarationEntry)) {
    buildDeclarations();
  }
}, 120_000);

test('package.json 의 types 엔트리가 실제로 존재한다', () => {
  const pkg = JSON.parse(fs.readFileSync(path.join(packageRoot, 'package.json'), 'utf8'));
  expect(pkg.types).toBe('./dist/types/index.d.ts');
  expect(pkg.exports['.'].types).toBe('./dist/types/index.d.ts');
  expect(fs.existsSync(declarationEntry)).toBe(true);
});

test.each(consumerProjects)('소비자 픽스처가 배포될 선언만으로 컴파일된다 — moduleResolution $mode', ({ project }) => {
  let output = '';
  let failed = false;
  try {
    execFileSync('npx', ['tsc', '-p', project], { cwd: packageRoot, stdio: 'pipe' });
  } catch (error) {
    failed = true;
    const err = error as { stdout?: Buffer; stderr?: Buffer };
    output = `${err.stdout?.toString() ?? ''}${err.stderr?.toString() ?? ''}`;
  }
  expect(failed, output).toBe(false);
}, 120_000);

test('두 소비자 프로젝트가 서로 다른 moduleResolution 을 쓴다', () => {
  const modes = consumerProjects.map(({ project }) => {
    const config = ts.parseConfigFileTextToJson(project, fs.readFileSync(project, 'utf8'));
    return String(config.config.compilerOptions.moduleResolution).toLowerCase();
  });
  // 한쪽이 조용히 다른 쪽 설정을 베끼면 두 모드 검사가 무의미해진다.
  expect(new Set(modes).size).toBe(2);
  expect(modes).toContain('nodenext');
});

describe.each([
  { name: 'kis', barrel: Kis as Record<string, unknown> },
  { name: 'kiwoom', barrel: Kiwoom as Record<string, unknown> },
  { name: 'nhplug', barrel: Nhplug as Record<string, unknown> },
])('$name barrel', ({ barrel }) => {
  test('런타임 export 가 전부 선언 표면에 있다', () => {
    const declared = exportedNames(declarationEntry);
    const runtimeExports = Object.keys(barrel).sort();
    expect(runtimeExports.length).toBeGreaterThan(0);

    const missing = runtimeExports.filter((name) => !declared.has(name));
    expect(missing, `선언 누락 ${missing.length}건: ${missing.join(', ')}`).toEqual([]);
  });
}, 120_000);
