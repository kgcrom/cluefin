import type { ApiResponse, NhplugEndpointDefinition } from '../core/types.js';
import type { NhplugClient } from './client.js';

export class NhplugDomainBase {
  public constructor(
    protected readonly client: NhplugClient,
    protected readonly endpoints: readonly NhplugEndpointDefinition[],
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
      throw new Error(`Unknown NH PLUG endpoint: ${methodName}`);
    }
    return this.client.invokeEndpoint(endpoint, input);
  }
}
