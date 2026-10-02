import { DartApiError } from '../core/errors.js';
import type { ApiResponse, DomainMethods } from '../core/types.js';
import { isZip, readZip, ZipError } from '../core/zip.js';
import type { DartClient } from './client.js';
import { DartDomainBase } from './domain-base.js';
import {
  type PeriodicReportFinancialStatementMethodName,
  periodicReportFinancialStatementEndpoints,
} from './metadata/periodic-report-financial-statement.js';
import type { PeriodicReportFinancialStatementResponseMap } from './schemas/periodic-report-financial-statement.js';

/** XBRL 패키지에서 푼 파일들 (파일명 → 내용). `.xbrl`·`.xsd`·`_lab-ko.xml` 등이 들어 있다. */
export type DartXbrlFiles = Map<string, Uint8Array>;

export interface PeriodicReportFinancialStatement
  extends DomainMethods<
    Exclude<PeriodicReportFinancialStatementMethodName, 'downloadFinancialStatementXbrl'>,
    PeriodicReportFinancialStatementResponseMap
  > {}

/** 정기보고서 재무정보 */
export class PeriodicReportFinancialStatement extends DartDomainBase {
  public constructor(client: DartClient) {
    super(client, periodicReportFinancialStatementEndpoints, { custom: ['downloadFinancialStatementXbrl'] });
  }

  /**
   * 재무제표 원본파일(XBRL) — ZIP 을 풀어 파일명 → 바이트 맵으로 돌려준다.
   * 디스크에 쓰지는 않는다 (파이썬은 `destination` 에 압축을 푼다).
   */
  public async downloadFinancialStatementXbrl(input: Record<string, unknown>): Promise<ApiResponse<DartXbrlFiles>> {
    const response = await this.invokeBinary('downloadFinancialStatementXbrl', input);
    if (!isZip(response.body)) {
      throw new DartApiError('응답이 ZIP 파일 형식이 아닙니다.');
    }
    try {
      return { headers: response.headers, body: readZip(response.body) };
    } catch (error) {
      if (error instanceof ZipError) {
        throw new DartApiError(`XBRL ZIP 파일을 읽을 수 없습니다: ${error.message}`);
      }
      throw error;
    }
  }
}
