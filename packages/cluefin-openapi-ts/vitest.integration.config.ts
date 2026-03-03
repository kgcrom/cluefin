import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'node',
    include: ['tests/**/*.integration.test.ts'],
    setupFiles: ['./tests/setup-integration-env.ts'],
    testTimeout: 180_000,
    fileParallelism: false,
    pool: 'forks',
    poolOptions: {
      forks: { singleFork: true },
    },
  },
});
