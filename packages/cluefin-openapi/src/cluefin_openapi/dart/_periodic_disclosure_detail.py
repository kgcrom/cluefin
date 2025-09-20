"""정기보고서 재무정보 (Periodic Disclosure Detail Information) API client."""

from ._client import Client


class PeriodicDisclosureDetail:
    def __init__(self, client: Client):
        self.client = client

    def capital_increase_decrease_current_state(self):
        """증자(감자) 현황 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 증자(감자) 현황을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def dividend_related_matters(self):
        """배당에 관한 사항 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 배당에 관한 사항을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def treasury_stock_acquisition_disposal_current_state(self):
        """자기주식 취득 및 처분 현황 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 자기주식 취득 및 처분 현황을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def largest_shareholder_current_state(self):
        """최대주주 현황 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 최대주주 현황을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def largest_shareholder_change_current_state(self):
        """최대주주 변동현황 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 최대주주 변동현황을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def minority_shareholder_current_state(self):
        """소액주주 현황 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 소액주주 현황을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def executive_current_state(self):
        """임원 현황 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 임원 현황을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def employee_current_state(self):
        """직원 현황 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 직원 현황을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def director_auditor_individual_remuneration_5_or_more(self):
        """이사·감사의 개인별 보수현황(5억원 이상) 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 이사·감사의 개인별 보수현황(5억원 이상)을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def director_auditor_total_remuneration_by_group(self):
        """이사·감사 전체의 보수현황(보수지급금액 - 이사·감사 전체) 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 이사·감사 전체의 보수현황(보수지급금액 - 이사·감사 전체)을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def individual_remuneration_top5_or_more(self):
        """개인별 보수지급 금액(5억이상 상위5인) 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 개인별 보수지급 금액(5억이상 상위5인)을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def retirement_pension_operation(self):
        """타법인 출자현황 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 타법인 출자현황을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def stock_acquisition_current_state(self):
        """주식의 총수 현황 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 주식의총수현황을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def financial_management_disclosure(self):
        """재무충건 발행실적 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 재무충건 발행실적을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def business_merger_related_outstanding_plans(self):
        """기업어음증권 미상환 잔액 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 기업어음증권 미상환 잔액을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def short_term_financing_outstanding_balance(self):
        """단기사채 미상환 잔액 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 단기사채 미상환 잔액을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def corporate_bonds_outstanding_balance(self):
        """회사채 미상환 잔액 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 회사채 미상환 잔액을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def new_stock_related_outstanding_balance(self):
        """신종자본증권 미상환 잔액 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 신종자본증권 미상환 잔액을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def early_redemption_related_outstanding_balance(self):
        """조건부 자본증권 미상환 잔액 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 조건부 자본증권 미상환 잔액을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def foreign_auditor_name_and_audit_opinion(self):
        """회계감사인의 명칭 및 감사의견 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 회계감사인의 명칭 및 감사의견을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def audit_fee_evaluation_plan(self):
        """감사용역체결현황 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 감사용역체결현황을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def non_audit_service_contract_plan_for_accounting_auditor(self):
        """회계감사인과의 비감사용역 계약체결 현황 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 회계감사인과의 비감사용역 계약체결 현황을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def external_auditor_and_change_current_state(self):
        """사외이사 및 그 변동현황 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 사외이사 및 그 변동현황을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def non_registered_executive_remuneration(self):
        """미등기임원 보수현황 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 미등기임원 보수현황을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def director_auditor_total_remuneration_general_meeting(self):
        """이사·감사 전체의 보수현황(주주총회 승인금액) 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 이사·감사 전체의 보수현황(주주총회 승인금액)을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def director_auditor_total_remuneration_payment_type(self):
        """이사·감사 전체의 보수현황(보수지급금액 - 유형별) 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 이사·감사 전체의 보수현황(보수지급금액 - 유형별)을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def public_fund_usage_details(self):
        """공모자금의 사용내역 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 공모자금의 사용내역을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def private_fund_usage_details(self):
        """사모자금의 사용내역 정보를 조회합니다.

        정기보고서(사업, 분기, 반기보고서) 내에 사모자금의 사용내역을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    # XBRL 재무제표 관련 API
    def single_company_main_financial_statement(self):
        """단일회사 주요계정 정보를 조회합니다.

        상장법인(유가증권, 코스닥) 및 주요 비상장법인(사업보고서 제출대상 & IFRS 적용)이 제출한 정기보고서 내에 XBRL재무제표의 주요계정과목(재무상태표, 손익계산서)을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def multi_company_main_financial_statement(self):
        """다중회사 주요계정 정보를 조회합니다.

        상장법인(유가증권, 코스닥) 및 주요 비상장법인(사업보고서 제출대상 & IFRS 적용)이 제출한 정기보고서 내에 XBRL재무제표의 주요계정과목(재무상태표, 손익계산서)을 제공합니다. (대상법인 복수조회 복수조회 가능)
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def xbrl_financial_statement_original(self):
        """재무제표 원본파일(XBRL) 정보를 조회합니다.

        상장법인(유가증권, 코스닥) 및 주요 비상장법인(사업보고서 제출대상 & IFRS 적용)이 제출한 정기보고서 내에 XBRL재무제표의 원본파일(XBRL)을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def single_company_all_financial_statements(self):
        """단일회사 전체 재무제표 정보를 조회합니다.

        상장법인(유가증권, 코스닥) 및 주요 비상장법인(사업보고서 제출대상 & IFRS 적용)이 제출한 정기보고서 내에 XBRL재무제표의 모든계정과목을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def xbrl_taxonomy_financial_statement_concept(self):
        """XBRL택사노미재무제표양식 정보를 조회합니다.

        금융감독원 회계포탈에서 제공하는 IFRS 기반 XBRL 재무제표 공시용 표준계정과목체계(계정과목) 을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def single_company_main_financial_statement_summary(self):
        """단일회사 주요 재무제표 요약 정보를 조회합니다.

        상장법인(유가증권, 코스닥) 및 주요 비상장법인(사업보고서 제출대상 & IFRS 적용)이 제출한 정기보고서 내에 XBRL재무제표의 주요 재무제표를 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def multi_company_main_financial_statement_summary(self):
        """다중회사 주요 재무제표 요약 정보를 조회합니다.

        상장법인(유가증권, 코스닥) 및 주요 비상장법인(사업보고서 제출대상 & IFRS 적용)이 제출한 정기보고서 내에 XBRL재무제표의 주요 재무제표를 제공합니다.(대상법인 복수조회 가능)
        """
        # TODO: Implement API call with parameters and response handling
        pass
