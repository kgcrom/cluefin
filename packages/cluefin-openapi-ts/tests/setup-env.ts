import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';

type EnvMap = Record<string, string | undefined>;
interface LoadProjectRootEnvOptions {
  envFiles?: string[];
}

const parseEnvContent = (content: string): Record<string, string> => {
  const parsed: Record<string, string> = {};

  for (const rawLine of content.split(/\r?\n/u)) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#')) {
      continue;
    }

    const lineWithoutExport = line.startsWith('export ') ? line.slice(7).trim() : line;
    const equalsIndex = lineWithoutExport.indexOf('=');
    if (equalsIndex <= 0) {
      continue;
    }

    const key = lineWithoutExport.slice(0, equalsIndex).trim();
    if (!/^[A-Za-z_][A-Za-z0-9_]*$/u.test(key)) {
      continue;
    }

    let value = lineWithoutExport.slice(equalsIndex + 1).trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }

    parsed[key] = value;
  }

  return parsed;
};

const resolveProjectRootDir = (): string => {
  if (process.env.PROJECT_ROOT_DIR) {
    return process.env.PROJECT_ROOT_DIR;
  }

  const packageRootDir = resolve(import.meta.dir, '..');
  return resolve(packageRootDir, '..', '..');
};

export const loadProjectRootEnv = (
  targetEnv: EnvMap = process.env,
  options: LoadProjectRootEnvOptions = {},
): string[] => {
  const projectRootDir = resolveProjectRootDir();
  targetEnv.PROJECT_ROOT_DIR ??= projectRootDir;
  const loadedKeys: string[] = [];
  const envFiles = options.envFiles ?? ['.env'];

  for (const envFile of envFiles) {
    const envPath = resolve(projectRootDir, envFile);
    if (!existsSync(envPath)) {
      continue;
    }

    const parsed = parseEnvContent(readFileSync(envPath, 'utf8'));
    for (const [key, value] of Object.entries(parsed)) {
      if (value === undefined || targetEnv[key] !== undefined) {
        continue;
      }

      targetEnv[key] = value;
      loadedKeys.push(key);
    }
  }

  return loadedKeys;
};

loadProjectRootEnv();
