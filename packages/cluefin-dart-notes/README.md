# cluefin-dart-notes

DART 공시 원문(`document.xml`, dart4 XML)을 직접 읽는 패키지입니다. 재무제표 주석의 서술과 표, "사업의 내용"처럼
XBRL에 없는 내용을 문서 → 섹션 → 문단·표 → 주석 노트 순서로 꺼냅니다. 네트워크를 쓰지 않고 로컬 파일만 읽으며,
원문은 `cluefin-openapi`로 받습니다.

지원 범위는 2017년 이후 제출된 정기보고서(사업·반기·분기)와 그 첨부 감사보고서, 감사보고서 단독 공시입니다.

## 사용

```python
from cluefin_dart_notes import Table, extract_notes, find_section, load_document
from cluefin_openapi.dart import Client

# ZIP에 든 본문과 첨부 감사보고서를 모두 저장한다. 본문이 있으면 첫 번째다(감사보고서만 든 ZIP도 있다)
dart = Client(auth_key="…").public_disclosure
paths = dart.disclosure_document_files("20260814000000", destination="docs")

doc = load_document(paths[0])
print(doc.document_name, doc.document_code, doc.rcept_no)  # 반기보고서 11012 20260814000000

for note in extract_notes(doc):  # 연결 주석 다음 별도 주석
    print(note.basis, note.number, note.title)  # consolidated 7 유형자산
    for block in note.blocks:
        if isinstance(block, Table) and block.bordered:  # 테두리 있는 표가 데이터 표
            print(block.caption, block.unit, block.to_rows()[:2])  # 병합 셀은 펼쳐서 반복

business = find_section(doc, assoc_code="D-0-2-0-0")  # II. 사업의 내용. title="사업의 내용"으로도 찾는다
```

처음부터 따라 해 보려면 [examples/dart_notes_analysis.ipynb](examples/dart_notes_analysis.ipynb)를 여세요
(`DART_AUTH_KEY`와 분석할 회사의 고유번호 `DART_CORP_CODE`가 필요합니다).

## 걸리기 쉬운 곳

- **섹션 코드(`AASSOCNOTE`)는 문서 종류마다 뜻이 다릅니다.** `D-0-2-0-0`은 정기보고서에서 "II. 사업의 내용"이지만
  감사보고서에서는 "외부감사 실시내용"입니다. `business_description`·`company_overview`는 그래서 정기보고서에서만
  값을 돌려줍니다. 감사보고서의 감사인·감사의견·자산총액은 `doc.summary`에 있습니다.
- `Section.blocks`에는 하위 섹션의 내용이 들어가지 않습니다. 최근 공시의 "사업의 내용"은 본문이 하위 섹션에 있고,
  여러 업종을 함께 하는 회사는 "사업의 개요"가 업종마다 따로 있습니다. `business_overviews(doc)`가 전부 돌려줍니다.
- **값은 환산하지 않습니다.** `Table.unit`("백만원")과 `parse_amount("(23,593,369)")`(괄호·△·▲·`-`는 음수, `-`만
  있거나 빈 셀은 None)를 함께 씁니다. 단위를 찾지 못한 표는 `unit`이 None입니다.
- 주석을 나누는 방식은 둘입니다. 2024년 이후 상장사 본문은 노트마다 소제목이 있어 그것으로 나누고, 소제목이 없는
  문서(오래된 공시, 비상장사, 감사보고서)는 문단의 번호를 1, 2, 3… 순서로 따라갑니다. 뒤쪽은 번호가 하나 빠지면
  경고만 남기고 계속하지만 둘 이상 빠지면 거기서 멈춥니다. `extract_notes`는 경고를 로그로만 남기므로, 노트 수가
  적어 보이면 `notes_sections(doc)`와 `split_notes(section, basis).warnings`로 확인하세요.
- 노트 번호는 문자열입니다(`"9-1"`, `"6-A"`, `"9&10"`).
- DART 원문은 XML 파서가 그대로 받지 못합니다(틀린 인코딩 선언, escape되지 않은 `R&D`의 `&`, 본문에 쓰인
  `<시장 동향>` 같은 꺾쇠). `load_document`가 고쳐서 읽고 무엇을 고쳤는지 `doc.repair`에 남깁니다.
  `doc.repair.used_fallback`이 참이거나 `doc.repair.warnings`가 있으면 아직 규칙이 없는 결함이니 텍스트를
  의심하세요. 새 규칙은 `DartXmlRepairer().with_rule(규칙, before="unknown-tags")`로 끼워
  `load_document(path, repairer=…)`에 넘깁니다. 지금까지 본 결함 유형은 [AGENTS.md](AGENTS.md)에 있습니다.
- dart4 XML이 아닌 원문은 `DartXmlRepairError`입니다. 본문이 HTML로 오는 거래소 공시가 그렇습니다.
- `[기재정정]` 보고서 맨 앞의 정정신고는 `is_correction=True`인 섹션으로 따로 나옵니다.
- 문단 텍스트의 줄바꿈은 원문의 `&cr;`·`BR`에서 온 것만 남고, 나머지 공백은 한 칸으로 줄어듭니다.
