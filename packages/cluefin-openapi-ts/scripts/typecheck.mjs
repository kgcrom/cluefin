import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptPath = fileURLToPath(import.meta.url);
const scriptDir = path.dirname(scriptPath);
const packageRoot = path.resolve(scriptDir, '..');
const outDir = path.join(packageRoot, '.typecheck');

fs.rmSync(outDir, { recursive: true, force: true });
fs.mkdirSync(outDir, { recursive: true });

const entries = [
  { input: './src/index.ts', output: 'index.js' },
  { input: './src/kis/index.ts', output: 'kis-index.js' },
  { input: './src/kiwoom/index.ts', output: 'kiwoom-index.js' },
];

for (const entry of entries) {
  const outfile = path.join(outDir, entry.output);
  const proc = spawnSync(
    'bun',
    [
      'build',
      entry.input,
      '--outfile',
      outfile,
      '--target',
      'node',
      '--format',
      'esm',
      '--packages',
      'external',
      '--no-bundle',
    ],
    { cwd: packageRoot },
  );

  if (proc.status !== 0) {
    if (proc.stdout) {
      process.stdout.write(proc.stdout);
    }
    if (proc.stderr) {
      process.stderr.write(proc.stderr);
    }
    if (proc.error) {
      console.error(proc.error.message);
    }
    process.exit(proc.status ?? 1);
  }
}

fs.rmSync(outDir, { recursive: true, force: true });
console.log('Typecheck (Bun compile check) completed successfully.');
