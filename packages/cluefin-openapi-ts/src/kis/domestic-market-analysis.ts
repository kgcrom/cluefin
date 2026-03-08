import type { DomainMethods } from '../core/types';
import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import {
  type DomesticMarketAnalysisMethodName,
  domesticMarketAnalysisEndpoints,
} from './metadata/domestic-market-analysis';

export interface DomesticMarketAnalysis extends DomainMethods<DomesticMarketAnalysisMethodName> {}
export class DomesticMarketAnalysis extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, domesticMarketAnalysisEndpoints);
  }
}
