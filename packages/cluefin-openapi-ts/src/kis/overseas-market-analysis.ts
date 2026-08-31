import type { DomainMethods } from '../core/types.js';
import { KisDomainBase } from './domain-base.js';
import type { KisHttpClient } from './http-client.js';
import {
  type OverseasMarketAnalysisMethodName,
  overseasMarketAnalysisEndpoints,
} from './metadata/overseas-market-analysis.js';

export type OverseasMarketAnalysis = KisDomainBase & DomainMethods<OverseasMarketAnalysisMethodName>;
export const OverseasMarketAnalysis = class OverseasMarketAnalysis extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, overseasMarketAnalysisEndpoints);
  }
} as {
  new (client: KisHttpClient): OverseasMarketAnalysis;
};
