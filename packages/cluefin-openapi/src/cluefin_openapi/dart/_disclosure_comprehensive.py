"""지분공시 종합정보 (Disclosure Comprehensive Information) API client."""

from ._client import Client


class DisclosureComprehensive:
    def __init__(self, client: Client):
        self.client = client

    def large_holdings_report(self):
        """대량보유 상황보고 정보를 조회합니다.

        주식등의 대량보유상황보고서 내에 대량보유 상황보고 정보를 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass

    def executive_major_shareholder_ownership_report(self):
        """임원·주요주주 소유보고 정보를 조회합니다.

        임원·주요주주특정증권등 소유상황보고서 내에 임원·주요주주 소유보고
        정보를 제공합니다.
        """
        # TODO: Implement API call with parameters and response handling
        pass
