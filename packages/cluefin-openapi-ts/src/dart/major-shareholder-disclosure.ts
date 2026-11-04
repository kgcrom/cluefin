import type { ApiResponse, DomainMethods } from '../core/types.js';
import type { DartClient } from './client.js';
import { DartDomainBase } from './domain-base.js';
import {
  type MajorMattersReportMethodName,
  majorMattersReportEndpoints,
} from './metadata/major-shareholder-disclosure.js';
import type { MajorMattersReportResponseMap } from './schemas/major-shareholder-disclosure.js';

type MajorMattersReportMethods = DomainMethods<MajorMattersReportMethodName, MajorMattersReportResponseMap>;

/**
 * 2026-11-04 (B-13): 엔드포인트와 맞지 않던 옛 메서드 이름이다. 지우지 않고 새 이름에 위임하는
 * 별칭으로 둔다 — 외부 사용자 호환.
 */
interface DeprecatedMajorMattersReportMethods {
  /** @deprecated assetTransferPutbackOption() 의 옛 이름. Use assetTransferPutbackOption() instead. */
  treasuryStockAcquisitionDisposalPlan: MajorMattersReportMethods['assetTransferPutbackOption'];
  /** @deprecated defaultOccurrence() 의 옛 이름. Use defaultOccurrence() instead. */
  realEstateDevelopment: MajorMattersReportMethods['defaultOccurrence'];
  /** @deprecated businessSuspension() 의 옛 이름. Use businessSuspension() instead. */
  businessLetter: MajorMattersReportMethods['businessSuspension'];
  /** @deprecated paidInCapitalIncreaseDecision() 의 옛 이름. Use paidInCapitalIncreaseDecision() instead. */
  securitiesGrantedDecision: MajorMattersReportMethods['paidInCapitalIncreaseDecision'];
  /** @deprecated freeCapitalIncreaseDecision() 의 옛 이름. Use freeCapitalIncreaseDecision() instead. */
  freeSecuritiesDecision: MajorMattersReportMethods['freeCapitalIncreaseDecision'];
  /** @deprecated paidInAndFreeCapitalIncreaseDecision() 의 옛 이름. Use paidInAndFreeCapitalIncreaseDecision() instead. */
  paidInCapitalReductionDecision: MajorMattersReportMethods['paidInAndFreeCapitalIncreaseDecision'];
  /** @deprecated creditorBankManagementProcedureCommencement() 의 옛 이름. Use creditorBankManagementProcedureCommencement() instead. */
  governmentBondManagerReplacement: MajorMattersReportMethods['creditorBankManagementProcedureCommencement'];
  /** @deprecated lawsuitFiling() 의 옛 이름. Use lawsuitFiling() instead. */
  profitRevocation: MajorMattersReportMethods['lawsuitFiling'];
  /** @deprecated overseasSecuritiesMarketListingDecision() 의 옛 이름. Use overseasSecuritiesMarketListingDecision() instead. */
  overseasSecuritiesTradingResolution: MajorMattersReportMethods['overseasSecuritiesMarketListingDecision'];
  /** @deprecated overseasSecuritiesMarketDelistingDecision() 의 옛 이름. Use overseasSecuritiesMarketDelistingDecision() instead. */
  overseasSecuritiesTradingDelistingResolution: MajorMattersReportMethods['overseasSecuritiesMarketDelistingDecision'];
  /** @deprecated overseasSecuritiesMarketListingStatus() 의 옛 이름. Use overseasSecuritiesMarketListingStatus() instead. */
  overseasSecuritiesTradingStatus: MajorMattersReportMethods['overseasSecuritiesMarketListingStatus'];
  /** @deprecated overseasSecuritiesMarketDelistingStatus() 의 옛 이름. Use overseasSecuritiesMarketDelistingStatus() instead. */
  overseasSecuritiesTradingStatusDelisting: MajorMattersReportMethods['overseasSecuritiesMarketDelistingStatus'];
  /** @deprecated exchangeableBondIssuanceDecision() 의 옛 이름. Use exchangeableBondIssuanceDecision() instead. */
  corporateBondIssuanceDecision: MajorMattersReportMethods['exchangeableBondIssuanceDecision'];
  /** @deprecated creditorBankManagementProcedureTermination() 의 옛 이름. Use creditorBankManagementProcedureTermination() instead. */
  governmentBondManagerTransferTermination: MajorMattersReportMethods['creditorBankManagementProcedureTermination'];
  /** @deprecated writeDownContingentCapitalSecuritiesIssuanceDecision() 의 옛 이름. Use writeDownContingentCapitalSecuritiesIssuanceDecision() instead. */
  reorganizationPlanApprovedRuling: MajorMattersReportMethods['writeDownContingentCapitalSecuritiesIssuanceDecision'];
  /** @deprecated businessAcquisitionDecision() 의 옛 이름. Use businessAcquisitionDecision() instead. */
  businessPlanDecision: MajorMattersReportMethods['businessAcquisitionDecision'];
  /** @deprecated tangibleAssetAcquisitionDecision() 의 옛 이름. Use tangibleAssetAcquisitionDecision() instead. */
  tangibleAssetPlanDecision: MajorMattersReportMethods['tangibleAssetAcquisitionDecision'];
  /** @deprecated otherCorporationSecuritiesAcquisitionDecision() 의 옛 이름. Use otherCorporationSecuritiesAcquisitionDecision() instead. */
  retirementStockInvestmentPlanDecision: MajorMattersReportMethods['otherCorporationSecuritiesAcquisitionDecision'];
  /** @deprecated otherCorporationSecuritiesTransferDecision() 의 옛 이름. Use otherCorporationSecuritiesTransferDecision() instead. */
  retirementStockInvestmentTransferDecision: MajorMattersReportMethods['otherCorporationSecuritiesTransferDecision'];
  /** @deprecated stockRelatedBondAcquisitionDecision() 의 옛 이름. Use stockRelatedBondAcquisitionDecision() instead. */
  stockRelatedBondPlanDecision: MajorMattersReportMethods['stockRelatedBondAcquisitionDecision'];
  /** @deprecated companyMergerDecision() 의 옛 이름. Use companyMergerDecision() instead. */
  corporateLawDecision: MajorMattersReportMethods['companyMergerDecision'];
  /** @deprecated companyDivisionMergerDecision() 의 옛 이름. Use companyDivisionMergerDecision() instead. */
  corporateLawMethodDecision: MajorMattersReportMethods['companyDivisionMergerDecision'];
  /** @deprecated stockExchangeTransferDecision() 의 옛 이름. Use stockExchangeTransferDecision() instead. */
  stockTradingOtherDecision: MajorMattersReportMethods['stockExchangeTransferDecision'];
}

/** 옛 메서드 이름 → 새 메서드 이름. 생성자가 각 옛 이름을 새 이름에 위임하는 메서드로 정의한다. */
const DEPRECATED_METHOD_ALIASES: ReadonlyArray<
  readonly [keyof DeprecatedMajorMattersReportMethods, MajorMattersReportMethodName]
> = [
  ['treasuryStockAcquisitionDisposalPlan', 'assetTransferPutbackOption'],
  ['realEstateDevelopment', 'defaultOccurrence'],
  ['businessLetter', 'businessSuspension'],
  ['securitiesGrantedDecision', 'paidInCapitalIncreaseDecision'],
  ['freeSecuritiesDecision', 'freeCapitalIncreaseDecision'],
  ['paidInCapitalReductionDecision', 'paidInAndFreeCapitalIncreaseDecision'],
  ['governmentBondManagerReplacement', 'creditorBankManagementProcedureCommencement'],
  ['profitRevocation', 'lawsuitFiling'],
  ['overseasSecuritiesTradingResolution', 'overseasSecuritiesMarketListingDecision'],
  ['overseasSecuritiesTradingDelistingResolution', 'overseasSecuritiesMarketDelistingDecision'],
  ['overseasSecuritiesTradingStatus', 'overseasSecuritiesMarketListingStatus'],
  ['overseasSecuritiesTradingStatusDelisting', 'overseasSecuritiesMarketDelistingStatus'],
  ['corporateBondIssuanceDecision', 'exchangeableBondIssuanceDecision'],
  ['governmentBondManagerTransferTermination', 'creditorBankManagementProcedureTermination'],
  ['reorganizationPlanApprovedRuling', 'writeDownContingentCapitalSecuritiesIssuanceDecision'],
  ['businessPlanDecision', 'businessAcquisitionDecision'],
  ['tangibleAssetPlanDecision', 'tangibleAssetAcquisitionDecision'],
  ['retirementStockInvestmentPlanDecision', 'otherCorporationSecuritiesAcquisitionDecision'],
  ['retirementStockInvestmentTransferDecision', 'otherCorporationSecuritiesTransferDecision'],
  ['stockRelatedBondPlanDecision', 'stockRelatedBondAcquisitionDecision'],
  ['corporateLawDecision', 'companyMergerDecision'],
  ['corporateLawMethodDecision', 'companyDivisionMergerDecision'],
  ['stockTradingOtherDecision', 'stockExchangeTransferDecision'],
];

/** 주요사항보고서 주요정보 (자기주식·증자·감자·사채 발행·합병/분할·영업/자산 양수도 결정 등) */
export type MajorMattersReport = DartDomainBase & MajorMattersReportMethods & DeprecatedMajorMattersReportMethods;
export const MajorMattersReport = class MajorMattersReport extends DartDomainBase {
  public constructor(client: DartClient) {
    super(client, majorMattersReportEndpoints);
    const self = this as unknown as Record<string, (input: Record<string, unknown>) => Promise<ApiResponse>>;
    for (const [oldName, newName] of DEPRECATED_METHOD_ALIASES) {
      Object.defineProperty(this, oldName, {
        // eslint-disable-next-line security/detect-object-injection -- newName comes from internal endpoint metadata.
        value: (input: Record<string, unknown> = {}) => self[newName](input),
        enumerable: true,
      });
    }
  }
} as {
  new (client: DartClient): MajorMattersReport;
};

/**
 * `MajorMattersReport` 의 옛 이름이다 (주요사항보고서는 주요주주 공시가 아니다).
 *
 * @deprecated Use {@link MajorMattersReport} instead (2026-11-04, B-13).
 */
export type MajorShareholderDisclosure = MajorMattersReport;
/** @deprecated Use {@link MajorMattersReport} instead (2026-11-04, B-13). */
export const MajorShareholderDisclosure = MajorMattersReport as unknown as {
  new (client: DartClient): MajorShareholderDisclosure;
};
