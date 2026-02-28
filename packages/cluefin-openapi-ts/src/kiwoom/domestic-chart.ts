import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { domesticChartEndpoints } from './metadata/domestic-chart';

export class DomesticChart extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticChartEndpoints);
  }
}
