import type { DomainMethods } from '../core/types';
import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import {
  type DomesticRankingAnalysisMethodName,
  domesticRankingAnalysisEndpoints,
} from './metadata/domestic-ranking-analysis';

export type DomesticRankingAnalysis = KisDomainBase & DomainMethods<DomesticRankingAnalysisMethodName>;
export const DomesticRankingAnalysis = class DomesticRankingAnalysis extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, domesticRankingAnalysisEndpoints);
  }
} as {
  new (client: KisHttpClient): DomesticRankingAnalysis;
};
