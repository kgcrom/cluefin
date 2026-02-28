import { expect, test } from 'bun:test';

import { withRetry } from '../../src/core/retry';

test('withRetry retries until success', async () => {
  let attempts = 0;

  const result = await withRetry(
    async () => {
      attempts += 1;
      if (attempts < 3) {
        throw new Error('transient');
      }
      return 'ok';
    },
    {
      maxRetries: 3,
      baseDelayMs: 1,
    },
    () => true,
  );

  expect(result).toBe('ok');
  expect(attempts).toBe(3);
});
