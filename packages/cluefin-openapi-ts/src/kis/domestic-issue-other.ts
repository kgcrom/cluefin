import type { DomainMethods } from '../core/types';
import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import { type DomesticIssueOtherMethodName, domesticIssueOtherEndpoints } from './metadata/domestic-issue-other';

export type DomesticIssueOther = KisDomainBase & DomainMethods<DomesticIssueOtherMethodName>;
export const DomesticIssueOther = class DomesticIssueOther extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, domesticIssueOtherEndpoints);
  }
} as {
  new (client: KisHttpClient): DomesticIssueOther;
};
