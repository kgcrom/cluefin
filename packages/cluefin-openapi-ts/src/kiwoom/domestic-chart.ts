import type { DomainMethods } from '../core/types';
import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { type DomesticChartMethodName, domesticChartEndpoints } from './metadata/domestic-chart';

export interface DomesticChart extends DomainMethods<DomesticChartMethodName> {}
export class DomesticChart extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticChartEndpoints);
  }
}
