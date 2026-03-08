import type { DomainMethods } from '../core/types';
import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import {
  overseasMarketAnalysisEndpoints,
  type OverseasMarketAnalysisMethodName,
} from './metadata/overseas-market-analysis';

export interface OverseasMarketAnalysis extends DomainMethods<OverseasMarketAnalysisMethodName> {}
export class OverseasMarketAnalysis extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, overseasMarketAnalysisEndpoints);
  }
}
