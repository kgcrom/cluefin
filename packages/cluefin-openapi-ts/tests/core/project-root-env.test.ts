import { afterEach, expect, test } from 'bun:test';
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

import { loadProjectRootEnv } from '../setup-env';

const TEST_KEY = 'CLUEFIN_OPENAPI_TS_TEST_ENV_KEY';
const KEEP_KEY = 'CLUEFIN_OPENAPI_TS_TEST_KEEP_KEY';
const ORDER_KEY = 'CLUEFIN_OPENAPI_TS_TEST_ORDER_KEY';
const FALLBACK_KEY = 'CLUEFIN_OPENAPI_TS_TEST_FALLBACK_KEY';

const createProjectRootWithFiles = (files: Record<string, string>): string => {
  const rootDir = mkdtempSync(join(tmpdir(), 'cluefin-openapi-env-'));
  for (const [name, content] of Object.entries(files)) {
    writeFileSync(join(rootDir, name), content, 'utf8');
  }
  return rootDir;
};

afterEach(() => {
  delete process.env.PROJECT_ROOT_DIR;
  delete process.env[TEST_KEY];
  delete process.env[KEEP_KEY];
  delete process.env[ORDER_KEY];
  delete process.env[FALLBACK_KEY];
});

test('loadProjectRootEnv reads .env from PROJECT_ROOT_DIR', () => {
  const rootDir = createProjectRootWithFiles({
    '.env': `${TEST_KEY}=loaded-from-project-root\n`,
  });

  try {
    process.env.PROJECT_ROOT_DIR = rootDir;

    const loadedKeys = loadProjectRootEnv();

    expect(loadedKeys).toContain(TEST_KEY);
    expect(process.env[TEST_KEY]).toBe('loaded-from-project-root');
  } finally {
    rmSync(rootDir, { recursive: true, force: true });
  }
});

test('loadProjectRootEnv does not overwrite existing environment variables', () => {
  const rootDir = createProjectRootWithFiles({
    '.env': `${KEEP_KEY}=from-dotenv\n`,
  });

  try {
    process.env.PROJECT_ROOT_DIR = rootDir;
    process.env[KEEP_KEY] = 'already-set';

    const loadedKeys = loadProjectRootEnv();

    expect(loadedKeys).not.toContain(KEEP_KEY);
    expect(process.env[KEEP_KEY]).toBe('already-set');
  } finally {
    rmSync(rootDir, { recursive: true, force: true });
  }
});

test('loadProjectRootEnv prefers earlier env files when ordered list is provided', () => {
  const rootDir = createProjectRootWithFiles({
    '.env.test': `${ORDER_KEY}=from-dotenv-test\n`,
    '.env': `${ORDER_KEY}=from-dotenv\n`,
  });

  try {
    process.env.PROJECT_ROOT_DIR = rootDir;

    const loadedKeys = loadProjectRootEnv(process.env, {
      envFiles: ['.env.test', '.env'],
    });

    expect(loadedKeys).toContain(ORDER_KEY);
    expect(process.env[ORDER_KEY]).toBe('from-dotenv-test');
  } finally {
    rmSync(rootDir, { recursive: true, force: true });
  }
});

test('loadProjectRootEnv falls back to .env when preferred file does not exist', () => {
  const rootDir = createProjectRootWithFiles({
    '.env': `${FALLBACK_KEY}=from-dotenv\n`,
  });

  try {
    process.env.PROJECT_ROOT_DIR = rootDir;

    const loadedKeys = loadProjectRootEnv(process.env, {
      envFiles: ['.env.test', '.env'],
    });

    expect(loadedKeys).toContain(FALLBACK_KEY);
    expect(process.env[FALLBACK_KEY]).toBe('from-dotenv');
  } finally {
    rmSync(rootDir, { recursive: true, force: true });
  }
});
