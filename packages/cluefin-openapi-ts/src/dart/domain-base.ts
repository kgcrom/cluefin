import type { ApiResponse, DartEndpointDefinition } from '../core/types.js';
import type { DartBinaryResponse, DartClient } from './client.js';

export interface DartDomainBaseOptions {
  /** 도메인 클래스가 직접 구현하는 메서드 — 자동 생성 대상에서 뺀다. */
  custom?: readonly string[];
}

export class DartDomainBase {
  public constructor(
    protected readonly client: DartClient,
    protected readonly endpoints: readonly DartEndpointDefinition[],
    options: DartDomainBaseOptions = {},
  ) {
    const custom = new Set(options.custom ?? []);
    for (const endpoint of endpoints) {
      if (custom.has(endpoint.methodName)) {
        continue;
      }
      Object.defineProperty(this, endpoint.methodName, {
        value: async (input: Record<string, unknown> = {}) => this.dispatch(endpoint, input),
        enumerable: true,
      });
    }
  }

  protected invokeJson(methodName: string, input: Record<string, unknown>): Promise<ApiResponse> {
    return this.client.invokeEndpoint(this.endpointOf(methodName), input);
  }

  protected invokeBinary(methodName: string, input: Record<string, unknown>): Promise<DartBinaryResponse> {
    return this.client.invokeBinaryEndpoint(this.endpointOf(methodName), input);
  }

  private endpointOf(methodName: string): DartEndpointDefinition {
    const endpoint = this.endpoints.find((item) => item.methodName === methodName);
    if (!endpoint) {
      throw new Error(`Unknown DART endpoint: ${methodName}`);
    }
    return endpoint;
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
