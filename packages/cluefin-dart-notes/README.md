# cluefin-dart-notes

DART 공시 원문(`document.xml`, dart4 XML)을 직접 파싱하는 패키지입니다. 정기보고서(사업·반기·분기)와 첨부
감사보고서의 서술형 주석, "사업의 내용"처럼 XBRL에 없는 내용을 다루는 것이 목표입니다.

지금은 원문 정리, 문서 메타, 섹션 트리, 문단·표 블록까지 있습니다. 주석을 노트 단위로 나누는 기능은 이어서 추가합니다.

## 문서와 섹션

```python
from cluefin_dart_notes import business_description, find_section, find_sections, load_document

doc = load_document("docs/20260814000000.xml")
print(doc.document_name, doc.document_code, doc.company_name, doc.rcept_no)  # 반기보고서 11012 …

for section in doc.iter_sections():  # 문서 순서, 장 → 절 → 항
    print("  " * (section.level - 1), section.title, section.assoc_code)

business = business_description(doc)  # II. 사업의 내용 (정기보고서만)
notes = find_section(doc, assoc_code="D-0-3-3-0")  # 연결재무제표 주석
overview_parts = find_sections(doc, assoc_code="D-0-1-*")  # glob 패턴
same_notes = find_section(doc, title="연결재무제표 주석")  # 번호·공백 무시
```

## 문단과 표

`Section.blocks`는 섹션 본문을 문서 순서의 `Paragraph`·`Heading`·`Table`로 돌려줍니다(하위 섹션 내용 제외).

```python
import pandas as pd

from cluefin_dart_notes import Heading, Paragraph, Table, parse_amount

for block in notes.blocks:
    if isinstance(block, Heading):  # 2024년 이후 상장사 주석은 노트마다 소제목이 붙는다
        print("##", block.text)
    elif isinstance(block, Paragraph):
        print(block.text)
    elif isinstance(block, Table) and block.bordered:
        rows = block.to_rows()  # 병합 셀은 펼쳐서 반복
        frame = pd.DataFrame(rows[1:], columns=rows[0])
        print(block.caption, block.unit)  # "… (단위 : 백만원)", "백만원"

parse_amount("(23,593,369)")  # Decimal('-23593369'). △·▲·- 도 음수, "-"·빈 셀은 None
```

- 레이아웃용 표(1×1 상자, 실제 표를 셀 안에 담은 래퍼)는 풀어서 안의 문단·표를 블록으로 꺼냅니다.
- 단위는 바로 앞 캡션 표(기준일·단위가 적힌 작은 테두리 없는 표), 짧은 단위 문단, 표의 첫 행 순서로 찾습니다.
  값을 환산하지는 않습니다.
- 문단 텍스트의 줄바꿈은 원문의 `&cr;`·`BR`에서 온 것만 남고, 나머지 공백은 한 칸으로 줄입니다.
  `Paragraph.bold_starts`는 굵은 글씨가 시작하는 위치입니다.

섹션 코드(`AASSOCNOTE`)는 문서 종류마다 뜻이 다릅니다. 감사보고서의 `D-0-2-0-0`은 "외부감사 실시내용"입니다.
그래서 `business_description`·`company_overview`는 정기보고서에서만 값을 돌려줍니다. 감사보고서는 `doc.summary`에
감사인·감사의견·자산총액 같은 요약값(`SUMMARY/EXTRACTION`)이 있습니다.

## 원문 정리

DART 원문은 그대로 넣으면 XML 파서가 거부합니다. 인코딩 선언이 틀리고, `R&D`처럼 escape되지 않은 `&`와
`<시장 동향>`처럼 본문에 쓰인 꺾쇠가 있습니다. `DartXmlRepairer`가 이런 곳을 고쳐 표준 라이브러리 파서가 받는
XML을 만들고, 무엇을 고쳤는지 기록을 남깁니다.

```python
from pathlib import Path

from cluefin_dart_notes import DartXmlRepairer

root, result = DartXmlRepairer().parse(Path("20260814000000.xml").read_bytes())

print(root.findtext(".//DOCUMENT-NAME"), result.encoding)
for report in result.reports:
    print(report.rule, report.count, report.samples[:1])
print(result.warnings)  # 허용 목록 밖의 태그가 여닫는 짝으로 나온 경우 등
print(result.used_fallback)  # 규칙이 모르는 오류를 위치 기반으로 고쳤는지
```

원문 파일은 `cluefin-openapi`로 받습니다. ZIP에 든 본문과 첨부 감사보고서를 모두 저장합니다.

```python
from cluefin_openapi.dart._client import Client
from cluefin_openapi.dart._public_disclosure import PublicDisclosure

paths = PublicDisclosure(Client(auth_key="…")).disclosure_document_files("20260814000000", destination="docs")
```

### 규칙 바꾸기

정리는 순서가 있는 규칙 목록입니다. 새로 깨지는 유형이 나오면 규칙을 하나 만들어 끼워 넣습니다.

```python
from cluefin_dart_notes import DartXmlRepairer, RuleOutcome


class StripZeroWidthSpace:
    name = "zero-width-space"

    def apply(self, text: str) -> RuleOutcome:
        return RuleOutcome(text=text.replace("​", ""), count=text.count("​"))


repairer = DartXmlRepairer().with_rule(StripZeroWidthSpace(), before="unknown-tags")
strict = DartXmlRepairer(strict=True)  # 위치 기반 수리 없이 첫 오류에서 예외
```

기본 규칙 (`DEFAULT_RULES`, 이 순서로 적용):

| 이름 | 고치는 것 |
|---|---|
| `dart-entities` | DART 고유 엔티티 `&cr;` → 줄바꿈 표식 U+2028 (블록 텍스트에서 `\n`이 됨) |
| `bare-ampersand` | 엔티티가 아닌 `&` → `&amp;` |
| `unknown-tags` | 허용 목록(`KNOWN_TAGS`) 밖의 `<` → `&lt;` |
| `attributes` | 여는 태그 속성의 여분 따옴표·중복 이름 |

인코딩은 규칙 앞의 `Decoder`가 판정합니다(utf-8 → cp949). 규칙을 다 거쳐도 파싱이 실패하면
`PositionalRepair`가 파서 오류 위치 근처의 `<`·`&`를 escape합니다. 이 경우는 `positional` 보고와 경고 로그가
남으니, 견본을 보고 새 규칙으로 옮기세요.
