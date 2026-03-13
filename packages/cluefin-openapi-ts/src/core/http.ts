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
        const timeout = setTimeout(() => {
          controller.abort();
        }, this.options.timeoutMs);

        try {
          const url = new URL(request.url);
          if (request.query) {
            for (const [key, value] of Object.entries(request.query)) {
              url.searchParams.set(key, value);
            }
          }

          const fetchInit: RequestInit = {
            method: request.method,
            headers: request.headers,
            signal: controller.signal,
          };
          if (request.body) {
            fetchInit.body = JSON.stringify(request.body);
          }

          const response = await this.fetchImpl(url.toString(), fetchInit);

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
            const rateLimitDetails: import('./errors').ApiErrorDetails = {
              statusCode: response.status,
              responseData: await this.safeJson(response),
            };
            const retryAfter = getRetryAfter(response);
            if (retryAfter !== undefined) {
              rateLimitDetails.retryAfter = retryAfter;
            }
            throw new ApiRateLimitError('Rate limit exceeded', rateLimitDetails);
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
        if (error instanceof ApiRateLimitError || error instanceof ApiServerError || error instanceof ApiTimeoutError) {
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
