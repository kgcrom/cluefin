import type { DomainMethods } from '../core/types.js';
import type { KiwoomClient } from './client.js';
import { KiwoomDomainBase } from './domain-base.js';
import { type DomesticSectorMethodName, domesticSectorEndpoints } from './metadata/domestic-sector.js';
import type { DomesticSectorResponseMap } from './schemas/domestic-sector.js';

export type DomesticSector = KiwoomDomainBase & DomainMethods<DomesticSectorMethodName, DomesticSectorResponseMap>;
export const DomesticSector = class DomesticSector extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticSectorEndpoints);
  }
} as {
  new (client: KiwoomClient): DomesticSector;
};
