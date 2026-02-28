import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const outDir = path.join(root, '.typecheck');

fs.rmSync(outDir, { recursive: true, force: true });
fs.mkdirSync(outDir, { recursive: true });

const entries = [
  { input: './src/index.ts', output: 'index.js' },
  { input: './src/kis/index.ts', output: 'kis-index.js' },
  { input: './src/kiwoom/index.ts', output: 'kiwoom-index.js' },
];

for (const entry of entries) {
  const outfile = path.join(outDir, entry.output);
  const proc = Bun.spawnSync([
    'bun',
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
  ]);

  if (proc.exitCode !== 0) {
    process.stdout.write(proc.stdout);
    process.stderr.write(proc.stderr);
    process.exit(proc.exitCode ?? 1);
  }
}

fs.rmSync(outDir, { recursive: true, force: true });
console.log('Typecheck (Bun compile check) completed successfully.');
