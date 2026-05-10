import type { DomainMethods } from '../core/types';
import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import {
  type OverseasMarketAnalysisMethodName,
  overseasMarketAnalysisEndpoints,
} from './metadata/overseas-market-analysis';

export type OverseasMarketAnalysis = KisDomainBase & DomainMethods<OverseasMarketAnalysisMethodName>;
export const OverseasMarketAnalysis = class OverseasMarketAnalysis extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, overseasMarketAnalysisEndpoints);
  }
} as {
  new (client: KisHttpClient): OverseasMarketAnalysis;
};
