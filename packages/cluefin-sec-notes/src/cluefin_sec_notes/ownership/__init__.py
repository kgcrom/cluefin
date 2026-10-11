"""SEC Form 3·4·5 내부자 소유 신고(`ownershipDocument` XML) 파서.

Item 본문 추출(`cluefin_sec_notes`)과 따로 쓰는 하위 패키지다. 공유하는 코드가 없다.
"""

from cluefin_sec_notes.ownership._model import (
    DOCUMENT_TYPES,
    Holding,
    Issuer,
    OwnershipDocument,
    ReportingOwner,
    Signature,
    Transaction,
)
from cluefin_sec_notes.ownership._parse import load_ownership, parse_ownership

__all__ = [
    "DOCUMENT_TYPES",
    "Holding",
    "Issuer",
    "OwnershipDocument",
    "ReportingOwner",
    "Signature",
    "Transaction",
    "load_ownership",
    "parse_ownership",
]
