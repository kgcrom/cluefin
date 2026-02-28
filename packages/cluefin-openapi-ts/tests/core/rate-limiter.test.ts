import { expect, test } from 'bun:test';

import { TokenBucket } from '../../src/core/rate-limiter';

test('TokenBucket allows burst then waits for refill', async () => {
  const bucket = new TokenBucket(1, 1);

  const first = await bucket.waitForToken(10);
  const second = await bucket.waitForToken(10);

  expect(first).toBeTrue();
  expect(second).toBeFalse();
});
