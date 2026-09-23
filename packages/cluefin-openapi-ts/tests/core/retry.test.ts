import { expect, test, vi } from 'vitest';

import { computeBackoffMs, withRetry } from '../../src/core/retry';

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

test('withRetry throws the last error once maxRetries is exhausted', async () => {
  let attempts = 0;

  await expect(
    withRetry(
      async () => {
        attempts += 1;
        throw new Error(`failure-${attempts}`);
      },
      {
        maxRetries: 2,
        baseDelayMs: 1,
      },
      () => true,
    ),
  ).rejects.toThrow('failure-3');

  // maxRetries=2 는 최초 시도 + 2번 재시도 = 3회 호출을 의미한다.
  expect(attempts).toBe(3);
});

test('withRetry stops immediately when canRetry returns false', async () => {
  let attempts = 0;

  await expect(
    withRetry(
      async () => {
        attempts += 1;
        throw new Error('non-retryable');
      },
      {
        maxRetries: 5,
        baseDelayMs: 1,
      },
      () => false,
    ),
  ).rejects.toThrow('non-retryable');

  expect(attempts).toBe(1);
});

test('withRetry backs off with a growing delay between attempts', async () => {
  // 지터를 0으로 고정하고 setTimeout 호출에 넘어간 ms 값만 기록한다 —
  // 실제 대기를 없애 테스트를 빠르고 결정적으로 만든다.
  vi.spyOn(globalThis.crypto, 'getRandomValues').mockImplementation(((array: Uint32Array) => {
    array[0] = 0;
    return array;
  }) as typeof globalThis.crypto.getRandomValues);
  const recordedDelays: number[] = [];
  vi.spyOn(globalThis, 'setTimeout').mockImplementation(((fn: () => void, ms?: number) => {
    recordedDelays.push(ms ?? 0);
    fn();
    return 0 as unknown as ReturnType<typeof setTimeout>;
  }) as typeof setTimeout);

  try {
    let attempts = 0;
    await expect(
      withRetry(
        async () => {
          attempts += 1;
          throw new Error('transient');
        },
        {
          maxRetries: 2,
          baseDelayMs: 20,
        },
        () => true,
      ),
    ).rejects.toThrow('transient');

    expect(attempts).toBe(3);
    expect(recordedDelays).toEqual([20, 40]);
  } finally {
    vi.restoreAllMocks();
  }
});

test('computeBackoffMs grows exponentially with attempt number', () => {
  vi.spyOn(globalThis.crypto, 'getRandomValues').mockImplementation(((array: Uint32Array) => {
    array[0] = 0;
    return array;
  }) as typeof globalThis.crypto.getRandomValues);

  try {
    const delay0 = computeBackoffMs(0, 100);
    const delay1 = computeBackoffMs(1, 100);
    const delay2 = computeBackoffMs(2, 100);

    expect(delay0).toBe(100);
    expect(delay1).toBe(200);
    expect(delay2).toBe(400);
  } finally {
    vi.restoreAllMocks();
  }
});
