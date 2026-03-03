import type { DomainMethods } from '../core/types';
import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import {
  domesticRankingAnalysisEndpoints,
  type DomesticRankingAnalysisMethodName,
} from './metadata/domestic-ranking-analysis';

export interface DomesticRankingAnalysis extends DomainMethods<DomesticRankingAnalysisMethodName> {}
export class DomesticRankingAnalysis extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, domesticRankingAnalysisEndpoints);
  }
}
