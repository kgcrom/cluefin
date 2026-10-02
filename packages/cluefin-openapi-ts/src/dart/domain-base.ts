import type { ApiResponse, DartEndpointDefinition } from '../core/types.js';
import type { DartBinaryResponse, DartClient } from './client.js';

export class DartDomainBase {
  public constructor(
    protected readonly client: DartClient,
    protected readonly endpoints: readonly DartEndpointDefinition[],
  ) {
    for (const endpoint of endpoints) {
      Object.defineProperty(this, endpoint.methodName, {
        value: async (input: Record<string, unknown> = {}) => this.dispatch(endpoint, input),
        enumerable: true,
      });
    }
  }

  private dispatch(
    endpoint: DartEndpointDefinition,
    input: Record<string, unknown>,
  ): Promise<ApiResponse | DartBinaryResponse> {
    return endpoint.responseKind === 'binary'
      ? this.client.invokeBinaryEndpoint(endpoint, input)
      : this.client.invokeEndpoint(endpoint, input);
  }
}
