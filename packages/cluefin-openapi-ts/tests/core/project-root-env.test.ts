import { afterEach, expect, test } from 'bun:test';
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

import { loadProjectRootEnv } from '../setup-env';

const TEST_KEY = 'CLUEFIN_OPENAPI_TS_TEST_ENV_KEY';
const KEEP_KEY = 'CLUEFIN_OPENAPI_TS_TEST_KEEP_KEY';

const createProjectRootWithEnv = (content: string): string => {
  const rootDir = mkdtempSync(join(tmpdir(), 'cluefin-openapi-env-'));
  writeFileSync(join(rootDir, '.env'), content, 'utf8');
  return rootDir;
};

afterEach(() => {
  delete process.env.PROJECT_ROOT_DIR;
  delete process.env[TEST_KEY];
  delete process.env[KEEP_KEY];
});

test('loadProjectRootEnv reads .env from PROJECT_ROOT_DIR', () => {
  const rootDir = createProjectRootWithEnv(`${TEST_KEY}=loaded-from-project-root\n`);

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
  const rootDir = createProjectRootWithEnv(`${KEEP_KEY}=from-dotenv\n`);

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
