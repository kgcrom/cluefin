import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import { domesticMarketAnalysisEndpoints } from './metadata/domestic-market-analysis';

export class DomesticMarketAnalysis extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, domesticMarketAnalysisEndpoints);
  }
}
