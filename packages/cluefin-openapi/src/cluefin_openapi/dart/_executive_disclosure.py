"""증권신고서 주요정보 (Executive Disclosure Main Information) API client."""

from ._client import Client


class ExecutiveDisclosure:
    def __init__(self, client: Client):
        self.client = client

    def public_disclosure_search(self):
        """공시검색 정보를 조회합니다.

        공시 유형별, 회사별, 날짜별 등 여러가지 조건으로 공시보고서 검색기능을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def company_overview(self):
        """기업개황 정보를 조회합니다.

        DART에 등록되어있는 기업의 개황정보를 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def public_disclosure_document_file(self):
        """공시서류원본파일을 조회합니다.

        공시보고서 원본파일을 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def unique_number(self):
        """고유번호 정보를 조회합니다.

        DART에 등록되어있는 공시대상회사의 고유번호,회사명,종목코드, 최근변경일자를 파일로 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass
