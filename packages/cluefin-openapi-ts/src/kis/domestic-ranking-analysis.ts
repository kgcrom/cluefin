import type { DomainMethods } from '../core/types.js';
import { KisDomainBase } from './domain-base.js';
import type { KisHttpClient } from './http-client.js';
import {
  type DomesticRankingAnalysisMethodName,
  domesticRankingAnalysisEndpoints,
} from './metadata/domestic-ranking-analysis.js';

export type DomesticRankingAnalysis = KisDomainBase & DomainMethods<DomesticRankingAnalysisMethodName>;
export const DomesticRankingAnalysis = class DomesticRankingAnalysis extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, domesticRankingAnalysisEndpoints);
  }
} as {
  new (client: KisHttpClient): DomesticRankingAnalysis;
};
