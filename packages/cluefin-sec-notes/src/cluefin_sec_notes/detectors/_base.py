"""탐지기 규약. 새 탐지 방식은 `Detector`를 구현해 `DEFAULT_DETECTORS`에 넣으면 캐스케이드에 들어간다."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from cluefin_sec_notes._catalog import FormCatalog
from cluefin_sec_notes._document import SecDocument
from cluefin_sec_notes._model import Candidate, Finding, ItemKey


@dataclass
class DetectionContext:
    """탐지기들이 공유하는 상태. 앞 탐지기가 알아낸 것을 뒤 탐지기가 쓴다.

    Attributes:
        excluded: Item 본문 탐색에서 뺄 블록 구간 `[start, end)`. 목차 탐지기가 목차 구간을 넣는다
            (목차 안의 "Item 1A. Risk Factors"를 본문 헤딩으로 잡지 않게).
        previous: 앞 탐지기들이 낸 후보. 신뢰도 낮은 탐지기는 이걸 보고 빈자리만 채운다.
        absent: 공시가 이 문서에 본문이 없다고 밝힌 Item → 근거(교차참조 색인의 "Not Applicable", 위임장 각주).
            못 찾아도 `missing_item`이 아니라 생략(`omitted`)으로 본다.
    """

    document: SecDocument
    catalog: FormCatalog
    excluded: list[tuple[int, int]] = field(default_factory=list)
    previous: list[Candidate] = field(default_factory=list)
    absent: dict[ItemKey, str] = field(default_factory=dict)

    def is_excluded(self, block: int) -> bool:
        return any(start <= block < end for start, end in self.excluded)


@dataclass(frozen=True)
class Detection:
    candidates: tuple[Candidate, ...] = ()
    findings: tuple[Finding, ...] = ()


class Detector(Protocol):
    """Item 시작 위치 후보를 내는 방식 하나.

    `name`은 `Item.method`로 드러나고, `confidence`가 높은 탐지기의 후보부터 채택된다. 탐지기는 후보만 내고
    채택·충돌 판단은 하지 않는다(`extract_items`가 한다).
    """

    name: str
    confidence: float

    def detect(self, context: DetectionContext) -> Detection: ...
