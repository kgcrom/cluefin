import type { DomainMethods } from '../core/types';
import type { NhplugClient } from './client';
import { NhplugDomainBase } from './domain-base';
import { type KrstockInquiryMethodName, krstockInquiryEndpoints } from './metadata/krstock-inquiry';
import type { KrstockInquiryResponseMap } from './schemas/krstock-inquiry';

export type NhplugKrstockInquiry = NhplugDomainBase &
  DomainMethods<KrstockInquiryMethodName, KrstockInquiryResponseMap>;
export const NhplugKrstockInquiry = class NhplugKrstockInquiry extends NhplugDomainBase {
  public constructor(client: NhplugClient) {
    super(client, krstockInquiryEndpoints);
  }
} as {
  new (client: NhplugClient): NhplugKrstockInquiry;
};
