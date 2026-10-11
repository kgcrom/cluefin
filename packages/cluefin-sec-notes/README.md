# cluefin-sec-notes

SEC EDGAR 공시 주 문서(10-K·10-Q·8-K HTML)에서 Item 단위 본문을 뽑는 패키지입니다. 네트워크를 쓰지 않고
로컬 파일만 읽습니다. 원문은 `cluefin-openapi`의 `sec` 모듈로 받습니다. 의존성은 없습니다(stdlib `html.parser`).

경계를 확신하지 못하면 조용히 틀리지 않고 `findings`로 알리는 것이 목표입니다. Item마다 어떤 방식으로
찾았는지(`method`)와 신뢰도(`confidence`)가 붙습니다.

## 원문 받기

```python
from cluefin_openapi.sec import Client

client = Client("Your Name your@email.com")  # SEC는 키 대신 User-Agent로 호출자를 밝히게 한다
filing = client.submissions.filings(cik, forms=["10-K"])[0]
path = client.archives.download_filing_document(
    cik, filing.accession_number, filing.primary_document, destination="filings"
)
```

## Item 추출

```python
from cluefin_sec_notes import extract_items, load_filing

document = load_filing(path)  # 서식은 인라인 XBRL dei → EDGAR SGML <TYPE> → 표지 순으로 정한다
result = extract_items(document)  # 서식을 알면 load_filing(path, form="10-K")

for item in result:  # 문서 순서
    print(item.key, item.method, item.confidence, len(item.text))

risk = result.item("1A")
print(risk.heading)  # "Item 1A. Risk Factors"
print(risk.text[:500])

for finding in result.warnings:  # 결과를 의심해야 할 때만 warning
    print(finding.code, finding.message)
```

- `Item.text`는 헤딩을 포함한 구간 텍스트입니다. 표는 행마다 칸을 탭으로 잇습니다.
- `Item.ranges`는 블록 구간 `[start, end)`들입니다. 본문이 같은 문서의 다른 쪽에 있는 Item은 구간이 여럿입니다
  (Item 8 "See pages F-1 through F-30" → 서명란 뒤 F-쪽, 교차참조 색인의 "4–36, 121–127").
- `Item.incorporated_by_reference`: 본문이 다른 문서(위임장, Exhibit 13 연차보고서, 8-K 첨부 보도자료)를 참조로
  편입한다는 문장뿐입니다. Part III처럼 이게 정상인 Item이 있습니다.
- `Item.shared_with`: 결합 헤딩("Items 1 and 2. Business and Properties")으로 같은 구간을 가리키는 다른 Item입니다.
- `result.missing`은 카탈로그상 있어야 하는데 못 찾은 Item이고, 그중 문서에 표기조차 없거나 공시가 생략을 밝힌
  것은 `result.omitted`입니다.

## 지원 서식

| 서식 | Item 키 | 비고 |
| --- | --- | --- |
| 10-K (10-K405, 10-KT, 10-KSB) | `result.item("7")` | 1C(2023-12-15~), 9C 등은 보고 기간 말로 적용 여부를 판단 |
| 10-Q (10-QT, 10-QSB) | `result.item("1", "II")` | Part마다 번호가 다시 시작한다. Part I Item 1·2·4는 생략할 수 없다 |
| 8-K | `result.item("2.02")` | 2004-08-23 전 번호 체계(Item 1–12)도 읽는다. 전부 optional |

정정 공시(`/A`)는 일부 Item만 담는 것이 정상이라 누락 경고를 내지 않습니다. 2001년 이전의 텍스트(.txt) 공시와
20-F 등 다른 서식은 범위 밖입니다(`extract_items`가 `ValueError`).

## 탐지 방식

신뢰도 높은 후보부터 채택합니다. 신뢰도가 낮은 후보는 이미 정한 Item 사이의 빈자리만 채웁니다.

| 방식(`method`) | 신뢰도 | 대응하는 경우 |
| --- | --- | --- |
| `cross_reference` | 0.97 | "Form 10-K Cross-Reference Index" 표의 쪽 범위(본문에 Item 헤딩이 없는 은행·대기업) |
| `toc_anchor` | 0.95 | 목차의 문서 안 링크(Workiva·DFIN 공시 대부분) |
| `heading_style` | 0.7 | "Item" 표기 없이 제목만 있는 헤딩(이미 찾은 Item 헤딩과 굵기·글자 크기가 같을 때) |
| `pattern` | 0.6 | 문단·표 맨 앞의 "Item 1A." 표기 |
| `toc_anchor_unverified` | 0.5 | 링크가 가리키는 블록이 그 Item 헤딩이 아닌 목차 링크 |
| `statements_after_toc` | 0.45 | 목차 바로 뒤 헤딩 없이 시작하는 10-Q 재무제표 |

머리말·꼬리말과 쪽 번호는 본문에서 뺍니다. 꼬리말의 쪽 번호(`document.pages`의 `Page.label`)로 "pages 46–160"
같은 쪽 참조와 교차참조 색인을 블록 구간으로 바꿉니다.

## 표

```python
from cluefin_sec_notes import parse_amount

statements = result.item("8")
for table in statements.tables:
    for row in table.grid():  # ('Products', '$307,003', '$294,866', '$298,085')
        print(row)

parse_amount("$(1,234)")  # Decimal('-1234'). 쉼표·통화 기호·퍼센트·끝의 각주 표시를 떼고, 대시·글자는 None
```

`Table.grid()`는 열을 맞춘 문자열 행렬입니다. 병합 칸(`colspan`·`rowspan`)을 펴고, 옆 칸에 따로 있는 `$`·`)`·`%`와
각주 표시를 값에 붙이고, 금액 칸이 덮는 열끼리 하나로 묶은 뒤 빈 행·열을 지웁니다. 원문 칸 그대로는
`Table.rows`(`Cell.text`·`col_span`·`row_span`)입니다. 표 머리의 단위("in millions")는 곱하지 않습니다.

## Finding 코드

| 코드 | 뜻 |
| --- | --- |
| `missing_item` | 있어야 할 Item을 못 찾았는데 문서에 그 표기나 제목이 있다(탐지 실패 의심) |
| `omitted_item` (info) | 문서에 표기가 없거나 공시가 생략을 밝혔다 |
| `unknown_item` | 카탈로그에 없는 Item 번호의 헤딩 |
| `empty_item` | 헤딩 뒤에 본문이 없다 |
| `non_sequential_layout` | Item이 카탈로그 순서대로 놓이지 않았다(구간 끝을 의심) |
| `page_reference_unresolved` | 같은 문서의 쪽을 참조하는데 그 쪽 번호를 찾지 못했다 |
| `toc_target_missing` | 목차 링크가 가리키는 앵커가 없다 |
| `toc_not_found`, `out_of_order`, `conflicting_candidate` (info) | 탐지 과정의 정보 |

읽으며 고친 HTML 결함(닫히지 않은 태그, 숨긴 내용, 머리말 제거 등)은 `document.report`에 위치와 함께 남습니다.
