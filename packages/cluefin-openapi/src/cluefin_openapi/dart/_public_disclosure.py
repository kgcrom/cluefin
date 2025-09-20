"""공시정보 (Public Disclosure Information) API client."""

from ._client import Client


class PublicDisclosure:
    def __init__(self, client: Client):
        self.client = client

    def public_disclosure_search(self):
        """공시검색 - 공시 유형별, 회사별, 날짜별 등 여러가지 조건으로 공시보고서 검색기능을 제공합니다."""
        # TODO: implement 공시검색 API
        pass

    def company_overview(self):
        """기업개황 - DART에 등록되어있는 기업의 개황정보를 제공합니다."""
        # TODO: implement 기업개황 API
        pass

    def disclosure_document_file(self):
        """공시서류원본파일 - 공시보고서 원본파일을 제공합니다."""
        # TODO: implement 공시서류원본파일 API
        pass

    def unique_number(self):
        """고유번호 - DART에 등록되어있는 공시대상회사의 고유번호,회사명,종목코드, 최근변경일자를 파일로 제공합니다."""
        # TODO: implement 고유번호 API
        pass
