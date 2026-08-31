import { describe, expect, it } from 'vitest';

import type { ApiResponse, NhplugEndpointDefinition } from '../../src/core/types';
import type { NhplugClient } from '../../src/nhplug/client';
import { NhplugDomainBase } from '../../src/nhplug/domain-base';

const response: ApiResponse = { headers: {}, body: { ok: true } };

const endpoints: NhplugEndpointDefinition[] = [
  {
    methodName: 'getAccountList',
    path: '/n2/acctinfo',
    bodyMap: {},
    supportsCts: true,
    params: [{ name: 'cts', required: false }],
  },
];

class TestNhplugDomainBase extends NhplugDomainBase {
  public async callInvoke(methodName: string): Promise<ApiResponse> {
    return await this.invoke(methodName, {});
  }
}

describe('NhplugDomainBase', () => {
  it('defines generated methods that delegate to the client endpoint invoker', async () => {
    const calls: NhplugEndpointDefinition[] = [];
    const client = {
      invokeEndpoint: async (endpoint: NhplugEndpointDefinition) => {
        calls.push(endpoint);
        return response;
      },
    } as unknown as NhplugClient;

    const domain = new TestNhplugDomainBase(client, endpoints);
    const methods = domain as unknown as Record<
      string,
      ((input: Record<string, unknown>) => Promise<ApiResponse>) | undefined
    >;
    const method = methods.getAccountList;

    expect(method).toBeTypeOf('function');
    await expect(method?.({})).resolves.toBe(response);
    await expect(domain.callInvoke('getAccountList')).resolves.toBe(response);
    await expect(domain.callInvoke('missingMethod')).rejects.toThrow('Unknown NH PLUG endpoint');
    expect(calls).toHaveLength(2);
  });
});
