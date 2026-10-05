"""원문 정리: dart4 원문 바이트를 `xml.etree`가 받는 XML로 만든다.

원문 정리(bytes → 올바른 XML)와 구조 해석(섹션·표·노트)을 분리하고, 정리 단계는 바꾸거나 더할 수 있는
규칙 목록으로 둔다. 깨지는 유형은 계속 늘어난다는 전제다. 규칙이 모르는 오류는 `PositionalRepair`가 일단
고치되 반드시 보고서에 남겨, 새 규칙을 만들 근거로 삼는다.
"""

from cluefin_dart_notes.repair._decoder import Decoder, DecodeResult
from cluefin_dart_notes.repair._positional import PositionalRepair
from cluefin_dart_notes.repair._repairer import DartXmlRepairer
from cluefin_dart_notes.repair._report import (
    DartXmlRepairError,
    RepairReport,
    RepairResult,
    RepairSample,
    RuleOutcome,
)
from cluefin_dart_notes.repair._rules import (
    DEFAULT_RULES,
    EscapeBareAmpersand,
    EscapeUnknownTags,
    NormalizeAttributes,
    RepairRule,
    ReplaceDartEntities,
)
from cluefin_dart_notes.repair._tags import KNOWN_TAGS

__all__ = [
    "DEFAULT_RULES",
    "KNOWN_TAGS",
    "DartXmlRepairError",
    "DartXmlRepairer",
    "DecodeResult",
    "Decoder",
    "EscapeBareAmpersand",
    "EscapeUnknownTags",
    "NormalizeAttributes",
    "PositionalRepair",
    "RepairReport",
    "RepairResult",
    "RepairRule",
    "RepairSample",
    "ReplaceDartEntities",
    "RuleOutcome",
]
