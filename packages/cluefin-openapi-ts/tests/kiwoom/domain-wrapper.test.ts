import { describe, expect, test } from 'vitest';

import type { ApiResponse, KiwoomEndpointDefinition } from '../../src/core/types';
import type { KiwoomClient } from '../../src/kiwoom/client';
import { KiwoomDomainBase } from '../../src/kiwoom/domain-base';
import { DomesticAccount } from '../../src/kiwoom/domestic-account';
import { DomesticETF } from '../../src/kiwoom/domestic-etf';
import { DomesticForeign } from '../../src/kiwoom/domestic-foreign';
import { DomesticMarketCondition } from '../../src/kiwoom/domestic-market-condition';
import { DomesticOrder } from '../../src/kiwoom/domestic-order';
import { DomesticSector } from '../../src/kiwoom/domestic-sector';
import { DomesticTheme } from '../../src/kiwoom/domestic-theme';
import { domesticAccountEndpoints } from '../../src/kiwoom/metadata/domestic-account';
import { domesticEtfEndpoints } from '../../src/kiwoom/metadata/domestic-etf';
import { domesticForeignEndpoints } from '../../src/kiwoom/metadata/domestic-foreign';
import { domesticMarketConditionEndpoints } from '../../src/kiwoom/metadata/domestic-market-condition';
import { domesticOrderEndpoints } from '../../src/kiwoom/metadata/domestic-order';
import { domesticSectorEndpoints } from '../../src/kiwoom/metadata/domestic-sector';
import { domesticThemeEndpoints } from '../../src/kiwoom/metadata/domestic-theme';

const response: ApiResponse = { headers: {}, body: { ok: true } };

class TestKiwoomDomainBase extends KiwoomDomainBase {
  public async callInvoke(methodName: string): Promise<ApiResponse> {
    return await this.invoke(methodName, { sample: 'value' });
  }
}

describe('Kiwoom domain wrappers', () => {
  test('generated domain methods delegate to the client endpoint invoker', async () => {
    const calls: Array<{ endpoint: KiwoomEndpointDefinition; input: Record<string, unknown> }> = [];
    const client = {
      invokeEndpoint: async (endpoint: KiwoomEndpointDefinition, input: Record<string, unknown>) => {
        calls.push({ endpoint, input });
        return response;
      },
    } as unknown as KiwoomClient;

    const wrappers = [
      { instance: new DomesticAccount(client), endpoint: domesticAccountEndpoints[0] },
      { instance: new DomesticETF(client), endpoint: domesticEtfEndpoints[0] },
      { instance: new DomesticForeign(client), endpoint: domesticForeignEndpoints[0] },
      { instance: new DomesticMarketCondition(client), endpoint: domesticMarketConditionEndpoints[0] },
      { instance: new DomesticOrder(client), endpoint: domesticOrderEndpoints[0] },
      { instance: new DomesticSector(client), endpoint: domesticSectorEndpoints[0] },
      { instance: new DomesticTheme(client), endpoint: domesticThemeEndpoints[0] },
    ];

    for (const { instance, endpoint } of wrappers) {
      const method = instance[endpoint.methodName as keyof typeof instance] as unknown as (
        input: Record<string, unknown>,
      ) => Promise<ApiResponse>;

      await expect(method({ sample: 'value' })).resolves.toBe(response);
    }

    expect(calls.map((call) => call.endpoint.methodName)).toEqual(wrappers.map(({ endpoint }) => endpoint.methodName));
  });

  test('protected invoke resolves known methods and rejects unknown methods', async () => {
    const client = {
      invokeEndpoint: async () => response,
    } as unknown as KiwoomClient;
    const domain = new TestKiwoomDomainBase(client, domesticAccountEndpoints);

    await expect(domain.callInvoke(domesticAccountEndpoints[0]?.methodName ?? '')).resolves.toBe(response);
    await expect(domain.callInvoke('missingMethod')).rejects.toThrow('Unknown Kiwoom endpoint');
  });
});
