import type { ApiResponse, KiwoomEndpointDefinition } from '../core/types';
import type { KiwoomClient } from './client';

export class KiwoomDomainBase {
  [key: string]: unknown;

  public constructor(
    protected readonly client: KiwoomClient,
    protected readonly endpoints: readonly KiwoomEndpointDefinition[],
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
      throw new Error(`Unknown Kiwoom endpoint: ${methodName}`);
    }
    return this.client.invokeEndpoint(endpoint, input);
  }
}
