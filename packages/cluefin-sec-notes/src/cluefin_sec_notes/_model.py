"""Item 추출 결과 모델과 Finding 코드."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cluefin_sec_notes._document import SecDocument

# Finding 코드. 코퍼스 리포트가 이 코드로 실패 양상을 묶는다. 새 양상을 감지하게 되면 코드를 더하고 설명을 단다.
MISSING_ITEM = "missing_item"
"""카탈로그상 이 공시에 있어야 할 Item을 어느 탐지기도 찾지 못했다."""
UNKNOWN_ITEM = "unknown_item"
"""Item 표기는 있는데 카탈로그에 없는 번호다. 새 Item이면 카탈로그에 더한다."""
OUT_OF_ORDER = "out_of_order"
"""후보 위치가 이미 정한 Item들과 카탈로그 순서가 어긋나 버렸다."""
CONFLICTING_CANDIDATE = "conflicting_candidate"
"""이미 정한 Item에 신뢰도가 낮은 탐지기가 다른 위치를 냈다(버렸다)."""
NON_SEQUENTIAL_LAYOUT = "non_sequential_layout"
"""채택한 Item들의 문서 위치가 카탈로그 순서와 다르다(연차보고서 형식 10-K). 구간 끝이 틀렸을 수 있다."""
TOC_TARGET_MISSING = "toc_target_missing"
"""목차 링크가 가리키는 앵커가 문서에 없다."""
TOC_NOT_FOUND = "toc_not_found"
"""Item 링크가 모인 목차를 찾지 못했다(목차 앵커 방식을 쓰지 못함)."""
EMPTY_ITEM = "empty_item"
"""Item 제목 뒤에 본문이 없다. 참조 편입이 정상인 Item(Part III)은 제외."""

WARNING = "warning"
INFO = "info"


@dataclass(frozen=True, order=True)
class ItemKey:
    """Item 식별자. 10-K처럼 번호만으로 유일한 서식도 Part를 채워 둔다(카탈로그 값)."""

    part: str | None
    number: str

    def __str__(self) -> str:
        return f"Part {self.part} Item {self.number}" if self.part else f"Item {self.number}"


@dataclass(frozen=True)
class Candidate:
    """탐지기가 낸 Item 시작 위치 후보.

    Attributes:
        block: Item이 시작하는 블록 위치(`SecDocument.blocks`의 인덱스).
        method: 낸 탐지기 이름.
        confidence: 탐지기의 신뢰도(0–1). 높은 것부터 채택한다.
        evidence: 사람이 읽을 근거(목차 행, 헤딩 텍스트 등).
    """

    key: ItemKey
    block: int
    method: str
    confidence: float
    evidence: str = ""


@dataclass(frozen=True)
class Finding:
    """추출 중 알게 된 문제나 사실. `severity`는 `warning`(결과를 의심하라) 또는 `info`."""

    code: str
    message: str
    severity: str = WARNING
    key: ItemKey | None = None
    block: int | None = None
    method: str | None = None


@dataclass(frozen=True, eq=False)
class Item:
    """Item 하나의 구간. `start`(제목 블록)부터 `end` 직전 블록까지.

    Attributes:
        title: 카탈로그의 표준 제목.
        shared_with: 같은 구간을 가리키는 다른 Item("Items 1 and 2. Business and Properties").
        incorporated_by_reference: 본문이 다른 문서(위임장 등)를 참조로 편입한다는 문장뿐이다.
    """

    key: ItemKey
    title: str
    start: int
    end: int
    method: str
    confidence: float
    document: SecDocument
    evidence: str = ""
    shared_with: tuple[ItemKey, ...] = ()
    incorporated_by_reference: bool = False

    @property
    def blocks(self):
        return self.document.blocks[self.start : self.end]

    @property
    def text(self) -> str:
        """제목 블록을 포함한 구간 텍스트(제목과 본문이 한 문단에 붙은 공시가 있어 제목을 따로 떼지 않는다)."""
        return self.document.text(self.start, self.end)

    @property
    def heading(self) -> str:
        from cluefin_sec_notes._document import block_text

        """구간에서 글자가 있는 첫 줄(빈 칸만 있는 표는 건너뛴다)."""
        for block in self.document.blocks[self.start : self.end]:
            line = next((line.strip() for line in block_text(block).split("\n") if line.strip()), "")
            if line:
                return line
        return ""


@dataclass(frozen=True, eq=False)
class ItemExtraction:
    """공시 하나의 Item 추출 결과.

    Attributes:
        items: 문서 순서.
        missing: 카탈로그상 있어야 하는데 못 찾은 Item.
        findings: 문제와 사실. `warnings`는 그중 `warning`만.
        candidates: 탐지기들이 낸 후보 전부(채택 여부와 무관). 경계가 이상할 때 원인을 보는 용도.
    """

    document: SecDocument
    catalog: str
    items: tuple[Item, ...]
    missing: tuple[ItemKey, ...]
    findings: tuple[Finding, ...]
    candidates: tuple[Candidate, ...]

    @property
    def warnings(self) -> tuple[Finding, ...]:
        return tuple(finding for finding in self.findings if finding.severity == WARNING)

    def item(self, number: str, part: str | None = None) -> Item | None:
        """번호로 찾는다. 10-Q처럼 Part마다 번호가 다시 시작하는 서식은 `part`를 준다."""
        number = number.upper()
        part = part.upper() if part else None
        return next(
            (item for item in self.items if item.key.number == number and (part is None or item.key.part == part)),
            None,
        )

    def __iter__(self):
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)
