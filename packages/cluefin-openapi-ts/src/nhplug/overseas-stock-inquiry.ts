import type { DomainMethods } from '../core/types';
import type { NhplugClient } from './client';
import { NhplugDomainBase } from './domain-base';
import { type OverseasStockInquiryMethodName, overseasStockInquiryEndpoints } from './metadata/overseas-stock-inquiry';
import type { OverseasStockInquiryResponseMap } from './schemas/overseas-stock-inquiry';

/** NH PLUG 해외주식(gbstock) 조회 API (`/gbstock/inquiry/v1/*`). */
export type NhplugOverseasStockInquiry = NhplugDomainBase &
  DomainMethods<OverseasStockInquiryMethodName, OverseasStockInquiryResponseMap>;
export const NhplugOverseasStockInquiry = class NhplugOverseasStockInquiry extends NhplugDomainBase {
  public constructor(client: NhplugClient) {
    super(client, overseasStockInquiryEndpoints);
  }
} as {
  new (client: NhplugClient): NhplugOverseasStockInquiry;
};
