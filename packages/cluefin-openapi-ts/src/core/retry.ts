import type { RetryOptions } from './types';

export const isRetryableStatus = (status: number): boolean => status === 429 || (status >= 500 && status <= 599);

export const isRetryableError = (error: unknown): boolean => {
  if (!(error instanceof Error)) {
    return false;
  }
  return /network|timeout|abort|fetch/i.test(error.message);
};

const U32_RANGE = 0x1_0000_0000;
const secureRandomInt = (maxExclusive: number): number => {
  if (maxExclusive <= 1) {
    return 0;
  }

  const values = new Uint32Array(1);
  globalThis.crypto.getRandomValues(values);
  const randomValue = values[0];
  return Math.floor((randomValue / U32_RANGE) * maxExclusive);
};

export const computeBackoffMs = (attempt: number, baseDelayMs: number): number => {
  const exponential = baseDelayMs * 2 ** attempt;
  const jitterMax = Math.max(25, Math.floor(baseDelayMs / 2));
  const jitter = secureRandomInt(jitterMax);
  return exponential + jitter;
};

export const withRetry = async <T>(
  operation: (attempt: number) => Promise<T>,
  options: RetryOptions,
  canRetry: (error: unknown) => boolean,
): Promise<T> => {
  let lastError: unknown;

  for (let attempt = 0; attempt <= options.maxRetries; attempt += 1) {
    try {
      return await operation(attempt);
    } catch (error) {
      lastError = error;
      if (attempt >= options.maxRetries || !canRetry(error)) {
        throw error;
      }
      await new Promise((resolve) => setTimeout(resolve, computeBackoffMs(attempt, options.baseDelayMs)));
    }
  }

  throw lastError instanceof Error ? lastError : new Error('Unknown retry failure');
};
