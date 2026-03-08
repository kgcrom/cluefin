import type { DomainMethods } from '../core/types';
import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { type DomesticThemeMethodName, domesticThemeEndpoints } from './metadata/domestic-theme';

export interface DomesticTheme extends DomainMethods<DomesticThemeMethodName> {}
export class DomesticTheme extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticThemeEndpoints);
  }
}
