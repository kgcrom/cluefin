import type { DomainMethods } from '../core/types.js';
import { KisDomainBase } from './domain-base.js';
import type { KisHttpClient } from './http-client.js';
import { type DomesticIssueOtherMethodName, domesticIssueOtherEndpoints } from './metadata/domestic-issue-other.js';

export type DomesticIssueOther = KisDomainBase & DomainMethods<DomesticIssueOtherMethodName>;
export const DomesticIssueOther = class DomesticIssueOther extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, domesticIssueOtherEndpoints);
  }
} as {
  new (client: KisHttpClient): DomesticIssueOther;
};
