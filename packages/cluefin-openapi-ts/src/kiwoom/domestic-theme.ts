import type { DomainMethods } from '../core/types';
import type { KiwoomClient } from './client';
import { KiwoomDomainBase } from './domain-base';
import { type DomesticThemeMethodName, domesticThemeEndpoints } from './metadata/domestic-theme';
import type { DomesticThemeResponseMap } from './schemas/domestic-theme';

export type DomesticTheme = KiwoomDomainBase & DomainMethods<DomesticThemeMethodName, DomesticThemeResponseMap>;
export const DomesticTheme = class DomesticTheme extends KiwoomDomainBase {
  public constructor(client: KiwoomClient) {
    super(client, domesticThemeEndpoints);
  }
} as {
  new (client: KiwoomClient): DomesticTheme;
};
