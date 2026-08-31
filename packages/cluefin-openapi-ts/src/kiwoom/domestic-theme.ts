import type { DomainMethods } from '../core/types.js';
import type { KiwoomClient } from './client.js';
import { KiwoomDomainBase } from './domain-base.js';
import { type DomesticThemeMethodName, domesticThemeEndpoints } from './metadata/domestic-theme.js';
import type { DomesticThemeResponseMap } from './schemas/domestic-theme.js';

export type DomesticTheme = KiwoomDomainBase & DomainMethods<DomesticThemeMethodName, DomesticThemeResponseMap>;
export const DomesticTheme = class DomesticTheme extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticThemeEndpoints);
  }
} as {
  new (client: KiwoomClient): DomesticTheme;
};
