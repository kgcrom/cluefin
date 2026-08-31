import type { DomainMethods } from '../core/types.js';
import type { KiwoomClient } from './client.js';
import { KiwoomDomainBase } from './domain-base.js';
import { type DomesticChartMethodName, domesticChartEndpoints } from './metadata/domestic-chart.js';
import type { DomesticChartResponseMap } from './schemas/domestic-chart.js';

export type DomesticChart = KiwoomDomainBase & DomainMethods<DomesticChartMethodName, DomesticChartResponseMap>;
export const DomesticChart = class DomesticChart extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticChartEndpoints);
  }
} as {
  new (client: KiwoomClient): DomesticChart;
};
