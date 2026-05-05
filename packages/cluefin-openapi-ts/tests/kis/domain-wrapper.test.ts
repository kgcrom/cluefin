import { describe, expect, test } from 'vitest';

import type { ApiResponse, KisEndpointDefinition } from '../../src/core/types';
import { KisDomainBase } from '../../src/kis/domain-base';
import { DomesticAccount } from '../../src/kis/domestic-account';
import { DomesticIssueOther } from '../../src/kis/domestic-issue-other';
import { DomesticMarketAnalysis } from '../../src/kis/domestic-market-analysis';
import { DomesticRankingAnalysis } from '../../src/kis/domestic-ranking-analysis';
import type { KisHttpClient } from '../../src/kis/http-client';
import { domesticAccountEndpoints } from '../../src/kis/metadata/domestic-account';
import { domesticIssueOtherEndpoints } from '../../src/kis/metadata/domestic-issue-other';
import { domesticMarketAnalysisEndpoints } from '../../src/kis/metadata/domestic-market-analysis';
import { domesticRankingAnalysisEndpoints } from '../../src/kis/metadata/domestic-ranking-analysis';

const response: ApiResponse = { headers: {}, body: { ok: true } };

class TestKisDomainBase extends KisDomainBase {
  public async callInvoke(methodName: string): Promise<ApiResponse> {
    return await this.invoke(methodName, { sample: 'value' });
  }
}

describe('KIS domain wrappers', () => {
  test('generated domain methods delegate to the client endpoint invoker', async () => {
    const calls: Array<{ endpoint: KisEndpointDefinition; input: Record<string, unknown> }> = [];
    const client = {
      invokeEndpoint: async (endpoint: KisEndpointDefinition, input: Record<string, unknown>) => {
        calls.push({ endpoint, input });
        return response;
      },
    } as unknown as KisHttpClient;

    const wrappers = [
      { instance: new DomesticAccount(client), endpoint: domesticAccountEndpoints[0] },
      { instance: new DomesticIssueOther(client), endpoint: domesticIssueOtherEndpoints[0] },
      { instance: new DomesticMarketAnalysis(client), endpoint: domesticMarketAnalysisEndpoints[0] },
      { instance: new DomesticRankingAnalysis(client), endpoint: domesticRankingAnalysisEndpoints[0] },
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
    } as unknown as KisHttpClient;
    const domain = new TestKisDomainBase(client, domesticAccountEndpoints);

    await expect(domain.callInvoke(domesticAccountEndpoints[0]?.methodName ?? '')).resolves.toBe(response);
    await expect(domain.callInvoke('missingMethod')).rejects.toThrow('Unknown KIS endpoint');
  });
});
