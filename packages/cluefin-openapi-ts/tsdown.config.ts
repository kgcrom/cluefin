import { defineConfig } from 'tsdown';

// zod and ws are declared as runtime dependencies, so tsdown externalizes them
// automatically (it keeps `dependencies` / `peerDependencies` unbundled by default).
const baseConfig = {
  entry: ['src/index.ts'],
  platform: 'node' as const,
  target: 'node20',
  sourcemap: true,
  clean: false,
  dts: false,
};

export default defineConfig([
  {
    ...baseConfig,
    format: ['esm'],
    outDir: 'dist/esm',
    outExtensions: () => ({ js: '.js' }),
  },
  {
    ...baseConfig,
    format: ['cjs'],
    outDir: 'dist/cjs',
    outExtensions: () => ({ js: '.cjs' }),
  },
]);
