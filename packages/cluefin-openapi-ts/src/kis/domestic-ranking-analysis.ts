import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import { domesticRankingAnalysisEndpoints } from './metadata/domestic-ranking-analysis';

export class DomesticRankingAnalysis extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, domesticRankingAnalysisEndpoints);
  }
}
