import type { DomainMethods } from '../core/types.js';
import type { DartClient } from './client.js';
import { DartDomainBase } from './domain-base.js';
import {
  type PeriodicReportKeyInformationMethodName,
  periodicReportKeyInformationEndpoints,
} from './metadata/periodic-report-key-information.js';
import type { PeriodicReportKeyInformationResponseMap } from './schemas/periodic-report-key-information.js';

/** 정기보고서 주요정보 (증자·배당·주주·임원·보수·채무증권·감사·자금사용 등) */
export type PeriodicReportKeyInformation = DartDomainBase &
  DomainMethods<PeriodicReportKeyInformationMethodName, PeriodicReportKeyInformationResponseMap>;
export const PeriodicReportKeyInformation = class PeriodicReportKeyInformation extends DartDomainBase {
  public constructor(client: DartClient) {
    super(client, periodicReportKeyInformationEndpoints);
  }
} as {
  new (client: DartClient): PeriodicReportKeyInformation;
};
