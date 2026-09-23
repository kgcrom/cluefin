import { expect, test, vi } from 'vitest';

import { TokenBucket } from '../../src/core/rate-limiter';

test('TokenBucket allows burst then waits for refill', async () => {
  const bucket = new TokenBucket(1, 1);

  const first = await bucket.waitForToken(10);
  const second = await bucket.waitForToken(10);

  expect(first).toBe(true);
  expect(second).toBe(false);
});

test('TokenBucket grants a new token once enough time has passed to refill', async () => {
  vi.useFakeTimers();
  try {
    // 초당 10개 리필 => 100ms 마다 토큰 1개.
    const bucket = new TokenBucket(1, 10);

    const first = await bucket.waitForToken(1000);
    expect(first).toBe(true);

    const secondPromise = bucket.waitForToken(1000);
    // 즉시는 토큰이 없어 폴링(50ms 간격)에 들어간다 — 리필에 필요한 100ms만큼 진행시킨다.
    await vi.advanceTimersByTimeAsync(100);

    await expect(secondPromise).resolves.toBe(true);
  } finally {
    vi.useRealTimers();
  }
});

test('TokenBucket times out without refilling if not enough time has passed', async () => {
  vi.useFakeTimers();
  try {
    const bucket = new TokenBucket(1, 1);

    const first = await bucket.waitForToken(1000);
    expect(first).toBe(true);

    const secondPromise = bucket.waitForToken(40);
    // 폴링 간격(50ms)보다 짧은 timeoutMs 라도 한 번은 폴링을 기다려야 하므로 60ms 만큼 진행시킨다.
    await vi.advanceTimersByTimeAsync(60);

    await expect(secondPromise).resolves.toBe(false);
  } finally {
    vi.useRealTimers();
  }
});
