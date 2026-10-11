"""파싱된 XML 요소의 타입.

파싱은 `defusedxml`로 하지만 `defusedxml`은 요소 클래스를 내보내지 않는다. 표준 `xml` 모듈을 import하면
(타입 힌트용이라도) 보안 정적 분석이 XXE 위험으로 지적하므로, 이 모듈이 쓰는 부분만 Protocol로 둔다.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Protocol


class Element(Protocol):
    tag: str
    text: str | None

    def get(self, key: str, default: None = None) -> str | None: ...

    def __iter__(self) -> Iterator[Element]: ...

    def find(self, path: str) -> Element | None: ...

    def findall(self, path: str) -> list[Element]: ...

    def findtext(self, path: str, default: None = None) -> str | None: ...

    def clear(self) -> None: ...
