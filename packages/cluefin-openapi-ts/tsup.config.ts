import { defineConfig } from 'tsup';

const baseConfig = {
  entry: ['src/index.ts'],
  platform: 'node' as const,
  target: 'node20',
  sourcemap: true,
  clean: false,
  dts: false,
  external: ['zod'],
};

export default defineConfig([
  {
    ...baseConfig,
    format: ['esm'],
    outDir: 'dist/esm',
  },
  {
    ...baseConfig,
    format: ['cjs'],
    outDir: 'dist/cjs',
    outExtension() {
      return {
        js: '.cjs',
      };
    },
  },
]);
