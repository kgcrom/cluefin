import type { DomainMethods } from '../core/types.js';
import { KisDomainBase } from './domain-base.js';
import type { KisHttpClient } from './http-client.js';
import {
  type DomesticMarketAnalysisMethodName,
  domesticMarketAnalysisEndpoints,
} from './metadata/domestic-market-analysis.js';

export type DomesticMarketAnalysis = KisDomainBase & DomainMethods<DomesticMarketAnalysisMethodName>;
export const DomesticMarketAnalysis = class DomesticMarketAnalysis extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, domesticMarketAnalysisEndpoints);
  }
} as {
  new (client: KisHttpClient): DomesticMarketAnalysis;
};
