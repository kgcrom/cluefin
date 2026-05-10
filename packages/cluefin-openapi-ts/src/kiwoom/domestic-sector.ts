import type { DomainMethods } from '../core/types';
import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { type DomesticSectorMethodName, domesticSectorEndpoints } from './metadata/domestic-sector';
import type { DomesticSectorResponseMap } from './schemas/domestic-sector';

export type DomesticSector = KiwoomDomainBase & DomainMethods<DomesticSectorMethodName, DomesticSectorResponseMap>;
export const DomesticSector = class DomesticSector extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticSectorEndpoints);
  }
} as {
  new (client: KiwoomClient): DomesticSector;
};
