import { KisDomainBase } from './domain-base';
import type { KisHttpClient } from './http-client';
import { domesticIssueOtherEndpoints } from './metadata/domestic-issue-other';

export class DomesticIssueOther extends KisDomainBase {
  public constructor(client: KisHttpClient) {
    super(client, domesticIssueOtherEndpoints);
  }
}
