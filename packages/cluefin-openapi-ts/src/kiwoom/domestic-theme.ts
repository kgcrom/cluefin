import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { domesticThemeEndpoints } from './metadata/domestic-theme';

export class DomesticTheme extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticThemeEndpoints);
  }
}
