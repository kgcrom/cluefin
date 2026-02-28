import {
  ApiAuthenticationError,
  ApiAuthorizationError,
  ApiError,
  ApiNetworkError,
  ApiRateLimitError,
  ApiServerError,
  ApiTimeoutError,
  ApiValidationError,
} from './errors';
import { TokenBucket } from './rate-limiter';
import { isRetryableError, withRetry } from './retry';
import type { FetchLike, HttpClientOptions, HttpRequestOptions } from './types';

const getRetryAfter = (response: Response): number | undefined => {
  const raw = response.headers.get('retry-after');
  if (!raw) {
    return undefined;
  }
  const parsed = Number.parseInt(raw, 10);
  return Number.isFinite(parsed) ? parsed : undefined;
};

export class BaseHttpClient {
  private readonly limiter: TokenBucket;
  private readonly fetchImpl: FetchLike;

  public constructor(
    private readonly options: HttpClientOptions,
    fetchImpl?: FetchLike,
  ) {
    this.fetchImpl = fetchImpl ?? globalThis.fetch;
    this.limiter = new TokenBucket(options.rateLimit.burst, options.rateLimit.requestsPerSecond);
  }

  public async request(request: HttpRequestOptions): Promise<Response> {
    const acquired = await this.limiter.waitForToken(this.options.timeoutMs);
    if (!acquired) {
      throw new ApiRateLimitError('Rate limit timeout');
    }

    return withRetry(
      async () => {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), this.options.timeoutMs);

        try {
          const url = new URL(request.url);
          if (request.query) {
            for (const [key, value] of Object.entries(request.query)) {
              url.searchParams.set(key, value);
            }
          }

          const response = await this.fetchImpl(url.toString(), {
            method: request.method,
            headers: request.headers,
            body: request.body ? JSON.stringify(request.body) : undefined,
            signal: controller.signal,
          });

          if (response.status === 400) {
            throw new ApiValidationError('Bad request', {
              statusCode: response.status,
              responseData: await this.safeJson(response),
            });
          }
          if (response.status === 401) {
            throw new ApiAuthenticationError('Authentication failed', {
              statusCode: response.status,
              responseData: await this.safeJson(response),
            });
          }
          if (response.status === 403) {
            throw new ApiAuthorizationError('Authorization failed', {
              statusCode: response.status,
              responseData: await this.safeJson(response),
            });
          }
          if (response.status === 429) {
            throw new ApiRateLimitError('Rate limit exceeded', {
              statusCode: response.status,
              responseData: await this.safeJson(response),
              retryAfter: getRetryAfter(response),
            });
          }
          if (response.status >= 500) {
            throw new ApiServerError('Server error', {
              statusCode: response.status,
              responseData: await this.safeJson(response),
            });
          }
          if (!response.ok) {
            throw new ApiError(`Unexpected status code ${response.status}`, {
              statusCode: response.status,
              responseData: await this.safeJson(response),
            });
          }

          return response;
        } catch (error) {
          if (error instanceof ApiError) {
            throw error;
          }
          if (error instanceof DOMException && error.name === 'AbortError') {
            throw new ApiTimeoutError('Request timeout');
          }
          throw new ApiNetworkError(error instanceof Error ? error.message : 'Unknown network error');
        } finally {
          clearTimeout(timeout);
        }
      },
      this.options.retry,
      (error) => {
        if (error instanceof ApiRateLimitError || error instanceof ApiServerError) {
          return true;
        }
        if (error instanceof ApiError) {
          return false;
        }
        return isRetryableError(error);
      },
    );
  }

  private async safeJson(response: Response): Promise<unknown> {
    try {
      const clone = response.clone();
      return await clone.json();
    } catch {
      return undefined;
    }
  }
}
