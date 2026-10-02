import type { DomainMethods } from '../core/types.js';
import type { DartClient } from './client.js';
import { DartDomainBase } from './domain-base.js';
import {
  type MajorShareholderDisclosureMethodName,
  majorShareholderDisclosureEndpoints,
} from './metadata/major-shareholder-disclosure.js';
import type { MajorShareholderDisclosureResponseMap } from './schemas/major-shareholder-disclosure.js';

/** 주요사항보고서 주요정보 (자기주식·증자·감자·사채 발행·합병/분할·영업/자산 양수도 결정 등) */
export type MajorShareholderDisclosure = DartDomainBase &
  DomainMethods<MajorShareholderDisclosureMethodName, MajorShareholderDisclosureResponseMap>;
export const MajorShareholderDisclosure = class MajorShareholderDisclosure extends DartDomainBase {
  public constructor(client: DartClient) {
    super(client, majorShareholderDisclosureEndpoints);
  }
} as {
  new (client: DartClient): MajorShareholderDisclosure;
};
