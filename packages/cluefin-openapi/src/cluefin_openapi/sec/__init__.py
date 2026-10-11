"""SEC EDGAR client (www.sec.gov, data.sec.gov).

SEC has no API key: every request declares its caller in the User-Agent header
("Name email@example.com"). See https://www.sec.gov/os/accessing-edgar-data
"""

from cluefin_openapi.sec._client import Client
from cluefin_openapi.sec._exceptions import (
    SecAPIError,
    SecAuthorizationError,
    SecClientError,
    SecNetworkError,
    SecNotFoundError,
    SecRateLimitError,
    SecServerError,
    SecTimeoutError,
)
from cluefin_openapi.sec._reference import Reference
from cluefin_openapi.sec._reference_types import CompanyTicker, CompanyTickerExchange
from cluefin_openapi.sec._submissions import Submissions
from cluefin_openapi.sec._submissions_types import CompanySubmissions, FilingEntry, FormerName, SubmissionsFile
from cluefin_openapi.sec._xbrl_api import XbrlApi
from cluefin_openapi.sec._xbrl_api_types import (
    CompanyConcept,
    CompanyFacts,
    ConceptFacts,
    FactValue,
    Frame,
    FrameValue,
)

__all__ = [
    "Client",
    "CompanyConcept",
    "CompanyFacts",
    "CompanySubmissions",
    "CompanyTicker",
    "CompanyTickerExchange",
    "ConceptFacts",
    "FactValue",
    "FilingEntry",
    "FormerName",
    "Frame",
    "FrameValue",
    "Reference",
    "Submissions",
    "SubmissionsFile",
    "XbrlApi",
    "SecAPIError",
    "SecAuthorizationError",
    "SecClientError",
    "SecNetworkError",
    "SecNotFoundError",
    "SecRateLimitError",
    "SecServerError",
    "SecTimeoutError",
]
