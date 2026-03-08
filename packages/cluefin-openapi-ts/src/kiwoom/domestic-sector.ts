import type { DomainMethods } from '../core/types';
import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { domesticSectorEndpoints, type DomesticSectorMethodName } from './metadata/domestic-sector';

export interface DomesticSector extends DomainMethods<DomesticSectorMethodName> {}
export class DomesticSector extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticSectorEndpoints);
  }
}
