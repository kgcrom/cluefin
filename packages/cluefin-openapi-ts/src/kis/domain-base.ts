import type { ApiResponse, KisEndpointDefinition } from '../core/types';
import type { KisHttpClient } from './http-client';

export class KisDomainBase {
  [key: string]: unknown;

  public constructor(
    protected readonly client: KisHttpClient,
    protected readonly endpoints: readonly KisEndpointDefinition[],
  ) {
    for (const endpoint of endpoints) {
      Object.defineProperty(this, endpoint.methodName, {
        value: async (input: Record<string, unknown>) => this.client.invokeEndpoint(endpoint, input),
        enumerable: true,
      });
    }
  }

  protected invoke(methodName: string, input: Record<string, unknown>): Promise<ApiResponse> {
    const endpoint = this.endpoints.find((item) => item.methodName === methodName);
    if (!endpoint) {
      throw new Error(`Unknown KIS endpoint: ${methodName}`);
    }
    return this.client.invokeEndpoint(endpoint, input);
  }
}
