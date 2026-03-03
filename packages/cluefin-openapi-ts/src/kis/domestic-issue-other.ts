import type { DomainMethods } from '../core/types';
import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import { domesticIssueOtherEndpoints, type DomesticIssueOtherMethodName } from './metadata/domestic-issue-other';

export interface DomesticIssueOther extends DomainMethods<DomesticIssueOtherMethodName> {}
export class DomesticIssueOther extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, domesticIssueOtherEndpoints);
  }
}
