import type { DomainMethods } from '../core/types';
import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { type DomesticChartMethodName, domesticChartEndpoints } from './metadata/domestic-chart';
import type { DomesticChartResponseMap } from './schemas/domestic-chart';

export type DomesticChart = KiwoomDomainBase & DomainMethods<DomesticChartMethodName, DomesticChartResponseMap>;
export const DomesticChart = class DomesticChart extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticChartEndpoints);
  }
} as {
  new (client: KiwoomClient): DomesticChart;
};
