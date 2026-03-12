import type { DomainMethods } from '../core/types';
import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { type DomesticSectorMethodName, domesticSectorEndpoints } from './metadata/domestic-sector';
import type { DomesticSectorResponseMap } from './schemas/domestic-sector';

export interface DomesticSector extends DomainMethods<DomesticSectorMethodName, DomesticSectorResponseMap> {}
export class DomesticSector extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticSectorEndpoints);
  }
}
