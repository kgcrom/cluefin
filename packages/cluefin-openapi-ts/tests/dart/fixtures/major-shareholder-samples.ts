/**
 * 주요사항보고서 엔드포인트별 실제 공시 샘플 (2025, DART 목록 API 에서 수집).
 *
 * 통합 테스트가 이 샘플의 회사·접수일로 각 엔드포인트를 호출해 생성된 zod 스키마를 실응답으로 검증한다.
 * 샘플이 없는 엔드포인트(해외증권시장 상장결정·상장폐지결정, 채권은행 관리절차 개시·중단)는 2025년에
 * 원본 공시가 없었거나 정정공시뿐이라 조회되지 않았다 — 통합 테스트에서 skip 된다.
 */
export interface MajorShareholderSample {
  reportName: string;
  corpCode: string;
  rceptDt: string;
}

export const majorShareholderSamples: Record<string, MajorShareholderSample> = {
  treasuryStockAcquisitionDisposalPlan: {
    reportName: '주요사항보고서(중요한자산양수도결정(기타))',
    corpCode: '01409095',
    rceptDt: '20250324',
  },
  realEstateDevelopment: { reportName: '주요사항보고서(부도발생)', corpCode: '00116268', rceptDt: '20250618' },
  businessLetter: { reportName: '주요사항보고서(영업정지)', corpCode: '01035289', rceptDt: '20250318' },
  corporateRehabilitationProceedings: {
    reportName: '주요사항보고서(회생절차개시신청)',
    corpCode: '00408956',
    rceptDt: '20250326',
  },
  dissolutionOccurrence: { reportName: '주요사항보고서(해산사유발생)', corpCode: '01497771', rceptDt: '20250321' },
  securitiesGrantedDecision: { reportName: '주요사항보고서(유상증자결정)', corpCode: '01575839', rceptDt: '20250331' },
  freeSecuritiesDecision: { reportName: '주요사항보고서(무상증자결정)', corpCode: '00332927', rceptDt: '20250319' },
  paidInCapitalReductionDecision: {
    reportName: '주요사항보고서(유무상증자결정)',
    corpCode: '01135084',
    rceptDt: '20250627',
  },
  capitalReductionDecision: { reportName: '주요사항보고서(감자결정)', corpCode: '00258102', rceptDt: '20250314' },
  profitRevocation: { reportName: '주요사항보고서(소송등의제기)', corpCode: '00364254', rceptDt: '20250331' },
  overseasSecuritiesTradingStatus: {
    reportName: '주요사항보고서(해외증권시장주권등상장)',
    corpCode: '00126380',
    rceptDt: '20250213',
  },
  overseasSecuritiesTradingStatusDelisting: {
    reportName: '주요사항보고서(해외증권시장주권등상장폐지)',
    corpCode: '00126380',
    rceptDt: '20250213',
  },
  convertibleBondIssuanceDecision: {
    reportName: '주요사항보고서(전환사채권발행결정)',
    corpCode: '01070149',
    rceptDt: '20250331',
  },
  newStockWarrantBondIssuanceDecision: {
    reportName: '주요사항보고서(신주인수권부사채권발행결정)',
    corpCode: '00910840',
    rceptDt: '20250225',
  },
  corporateBondIssuanceDecision: {
    reportName: '주요사항보고서(교환사채권발행결정)',
    corpCode: '00159795',
    rceptDt: '20250331',
  },
  reorganizationPlanApprovedRuling: {
    reportName: '주요사항보고서(상각형조건부자본증권발행결정)',
    corpCode: '00149646',
    rceptDt: '20250227',
  },
  treasuryStockAcquisitionDecision: {
    reportName: '주요사항보고서(자기주식취득결정)',
    corpCode: '00603278',
    rceptDt: '20250331',
  },
  treasuryStockDisposalDecision: {
    reportName: '주요사항보고서(자기주식처분결정)',
    corpCode: '00159795',
    rceptDt: '20250331',
  },
  treasuryStockTrustContractDecision: {
    reportName: '주요사항보고서(자기주식취득신탁계약체결결정)',
    corpCode: '00446901',
    rceptDt: '20250331',
  },
  treasuryStockTrustContractTerminationDecision: {
    reportName: '주요사항보고서(자기주식취득신탁계약해지결정)',
    corpCode: '00860332',
    rceptDt: '20250328',
  },
  businessPlanDecision: { reportName: '주요사항보고서(영업양수결정)', corpCode: '00118965', rceptDt: '20250331' },
  businessTransferDecision: { reportName: '주요사항보고서(영업양도결정)', corpCode: '00274933', rceptDt: '20250828' },
  tangibleAssetPlanDecision: {
    reportName: '주요사항보고서(유형자산양수결정)',
    corpCode: '00642541',
    rceptDt: '20250327',
  },
  tangibleAssetTransferDecision: {
    reportName: '주요사항보고서(유형자산양도결정)',
    corpCode: '00132725',
    rceptDt: '20250325',
  },
  retirementStockInvestmentPlanDecision: {
    reportName: '주요사항보고서(타법인주식및출자증권양수결정)',
    corpCode: '00347716',
    rceptDt: '20250331',
  },
  retirementStockInvestmentTransferDecision: {
    reportName: '주요사항보고서(타법인주식및출자증권양도결정)',
    corpCode: '00112004',
    rceptDt: '20250326',
  },
  stockRelatedBondPlanDecision: {
    reportName: '주요사항보고서(주권관련사채권양수결정)',
    corpCode: '00407975',
    rceptDt: '20250604',
  },
  stockRelatedBondTransferDecision: {
    reportName: '주요사항보고서(주권관련사채권양도결정)',
    corpCode: '00642541',
    rceptDt: '20250325',
  },
  corporateLawDecision: { reportName: '주요사항보고서(회사합병결정)', corpCode: '01204056', rceptDt: '20250331' },
  corporateDivisionDecision: { reportName: '주요사항보고서(회사분할결정)', corpCode: '00106623', rceptDt: '20250318' },
  corporateLawMethodDecision: {
    reportName: '주요사항보고서(회사분할합병결정)',
    corpCode: '00138792',
    rceptDt: '20250116',
  },
  stockTradingOtherDecision: {
    reportName: '주요사항보고서(주식교환ㆍ이전결정)',
    corpCode: '00197476',
    rceptDt: '20250318',
  },
};
