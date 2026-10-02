import type { DomainMethods } from '../core/types.js';
import type { DartClient } from './client.js';
import { DartDomainBase } from './domain-base.js';
import {
  type ShareDisclosureComprehensiveMethodName,
  shareDisclosureComprehensiveEndpoints,
} from './metadata/share-disclosure-comprehensive.js';
import type { ShareDisclosureComprehensiveResponseMap } from './schemas/share-disclosure-comprehensive.js';

/** 지분공시 종합정보 */
export type DartShareDisclosureComprehensive = DartDomainBase &
  DomainMethods<ShareDisclosureComprehensiveMethodName, ShareDisclosureComprehensiveResponseMap>;
export const DartShareDisclosureComprehensive = class DartShareDisclosureComprehensive extends DartDomainBase {
  public constructor(client: DartClient) {
    super(client, shareDisclosureComprehensiveEndpoints);
  }
} as {
  new (client: DartClient): DartShareDisclosureComprehensive;
};
