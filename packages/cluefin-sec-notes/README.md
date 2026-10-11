# cluefin-sec-notes

SEC EDGAR 공시 주 문서(10-K·10-Q·8-K HTML)에서 Item 단위 본문을 뽑는 패키지입니다. 내부자 소유 신고
(Form 3·4·5 XML)를 읽는 하위 패키지 `cluefin_sec_notes.ownership`도 있습니다([아래](#내부자-소유-신고-form-345)).
네트워크를 쓰지 않고 로컬 파일만 읽습니다. 원문은 `cluefin-openapi`의 `sec` 모듈로 받습니다. HTML은 stdlib
`html.parser`로, XML은 `defusedxml`로 읽습니다.

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

risk = result.item("1A")  # 구간을 믿을 수 없으면 예외(아래)
print(risk.heading)  # "Item 1A. Risk Factors"
print(risk.text[:500])

for finding in result.warnings:  # 결과를 의심해야 할 때만 warning
    print(finding.code, finding.message)
```

`item()`은 조용히 틀린 구간을 내주지 않습니다.

```python
from cluefin_sec_notes import MissingItemError, UncertainItemError

try:
    statements = result.item("8")
except UncertainItemError as error:  # 찾았지만 경계가 의심스럽다(아래 표의 "예외" 열)
    print([finding.code for finding in error.findings])  # ['statements_not_found']
    statements = error.item  # 그래도 쓰려면. result.item("8", strict=False)와 같다
except MissingItemError as error:  # 문서에 표기는 있는데 구간을 못 찾았다
    print(error.key, error)
```

- 문서가 생략한 Item(`omitted`)과 카탈로그에 없는 번호는 예외 없이 None입니다.
- `for item in result` 순회는 예외를 내지 않습니다. Item마다 `item.warnings`(그 Item의 warning Finding)를 보세요.
- `strict=False`면 경고와 무관하게 찾은 것을 그대로(없으면 None) 돌려줍니다.

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

| 코드 | 뜻 | `item()` 예외 |
| --- | --- | --- |
| `missing_item` | 있어야 할 Item을 못 찾았는데 문서에 그 표기나 제목이 있다(탐지 실패 의심) | `MissingItemError` |
| `empty_item` | 헤딩 뒤에 본문이 없다 | `UncertainItemError` |
| `page_reference_unresolved` | 같은 문서의 쪽을 참조하는데 그 쪽 번호를 찾지 못했다 | `UncertainItemError` |
| `statements_not_found` | 재무제표 Item(10-K 8, 10-Q I:1)이 재무제표라기엔 짧다(다른 곳을 가리키는 참조만 남음) | `UncertainItemError` |
| `implausible_length` | Item 길이가 그 Item에 그럴듯한 범위를 벗어났다(10-K 7·7A, 10-Q I:3·I:4. 앞뒤 경계가 틀림) | `UncertainItemError` |
| `non_sequential_layout` | Item이 카탈로그 순서대로 놓이지 않았다(구간 끝을 의심) | 없음(`item.warnings`에만) |
| `toc_target_missing` | 목차 링크가 가리키는 앵커가 없다(Item은 헤딩으로 찾았을 수 있다) | 없음(`item.warnings`에만) |
| `unknown_item` | 카탈로그에 없는 Item 번호의 헤딩 | 없음(공시 단위) |
| `omitted_item` (info) | 문서에 표기가 없거나 공시가 생략을 밝혔다 | 없음(None) |
| `toc_not_found`, `out_of_order`, `conflicting_candidate` (info) | 탐지 과정의 정보 | 없음 |

예외를 내는 코드는 `UNCERTAIN_CODES`입니다. 목차·배치 경고는 맞게 찾은 Item에도 붙어서 예외에서 뺐습니다.
다음 쪽 머리말이 구간 끝에 남은 Item 목록("Item 9, 9A")은 경고 없이 잘라 냅니다.

읽으며 고친 HTML 결함(닫히지 않은 태그, 숨긴 내용, 머리말 제거 등)은 `document.report`에 위치와 함께 남습니다.

## 내부자 소유 신고 (Form 3·4·5)

임원·이사·10% 주주가 회사 주식을 사고팔거나(Form 4, 2영업일 안), 처음 보유를 신고하거나(Form 3), 연간 신고(Form 5)할 때
내는 XML(`ownershipDocument`)입니다. 정정(`/A`)도 같은 형식입니다.

```python
from cluefin_openapi.sec import Client
from cluefin_sec_notes.ownership import load_ownership

client = Client("Your Name your@email.com")
filing = client.submissions.filings(cik, forms=["4"])[0]
# 주 문서명은 SEC가 XSL로 렌더링한 경로(xslF345X05/form4.xml)다. 파일명만 떼면 원본 XML이다
name = filing.primary_document.rsplit("/", 1)[-1]
path = client.archives.download_filing_document(cik, filing.accession_number, name, destination="ownership")

doc = load_ownership(path)
doc.issuer.trading_symbol, [owner.officer_title for owner in doc.reporting_owners]
for t in doc.non_derivative_transactions:
    print(t.date, t.code, t.shares, t.price, t.acquired_disposed, t.shares_owned_after)
    for field, ids in t.footnote_ids.items():  # 예: {"price": ("F2",)} — "가중평균, 범위 $262.00–$262.67"
        print(" ", field, [doc.footnotes[i] for i in ids])
```

- 표는 넷입니다: `non_derivative_transactions`·`non_derivative_holdings`(주식), `derivative_transactions`·
  `derivative_holdings`(옵션·RSU 등, 행사가·만기·기초자산 칸이 더 있음). `doc.transactions`·`doc.holdings`는 둘을 이어 줍니다.
- `code`는 SEC 거래 코드입니다. P 장내 매수, S 장내 매도, A 보상 지급, M 옵션 행사, F 세금 원천징수분, G 증여 등.
  매수 신호로 쓸 만한 P는 드뭅니다(표본 거래 1,035건 중 32건).
- 값이 없으면 None입니다. 옵션 행사(M) 가격처럼 값 대신 각주만 있는 칸이 흔해서, 각주는 필드별 `footnote_ids`로 남깁니다.
- `aff10b5_one`(사전 매매 계획 10b5-1에 따른 거래인지)은 2023년부터 있는 칸이라 그전 공시는 None입니다.
- 예상 밖의 불리언·숫자·날짜, 3·4·5가 아닌 서식은 `ValueError`입니다.
