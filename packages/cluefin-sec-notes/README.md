# cluefin-sec-notes

SEC EDGAR 공시 주 문서(10-K·10-Q·8-K HTML)에서 Item 단위 본문을 뽑고 재무제표 Item을 주석으로 나누는 패키지입니다.
내부자 소유 신고(Form 3·4·5 XML)와 13F 기관 보유 보고를 읽는 하위 패키지 `cluefin_sec_notes.ownership`도 있습니다.
네트워크를 쓰지 않고 로컬 파일만 읽습니다. 원문은 `cluefin-openapi`의 `sec` 모듈로 받습니다.

경계를 확신하지 못하면 조용히 틀리지 않고 알리는 것이 목표입니다. Item마다 어떤 방식으로 찾았는지(`method`)와
신뢰도(`confidence`)가 붙고, 믿을 수 없는 구간은 `item()`이 예외로 막습니다.

## Item 추출

```python
import os

from cluefin_openapi.sec import Client
from cluefin_sec_notes import MissingItemError, UncertainItemError, extract_items, load_filing

# SEC는 키 대신 User-Agent("이름 이메일")로 호출자를 밝히게 한다. 이 저장소는 환경변수 SEC_USER_AGENT에 둔다
client = Client(os.environ["SEC_USER_AGENT"])
filing = client.submissions.filings(cik, forms=["10-K"])[0]
path = client.archives.download_filing_document(
    cik, filing.accession_number, filing.primary_document, destination="filings"
)

result = extract_items(load_filing(path))  # 서식을 알면 load_filing(path, form="10-K")
for item in result:  # 문서 순서. 순회는 예외를 내지 않는다
    print(item.key, item.method, item.confidence, len(item.text), [w.code for w in item.warnings])

risk = result.item("1A")  # 10-Q는 Part마다 번호가 다시 시작한다: result.item("1", "II"). 8-K는 result.item("2.02")
print(risk.heading, risk.text[:500])

try:
    statements = result.item("8")
except UncertainItemError as error:  # 찾았지만 경계가 의심스럽다
    print([finding.code for finding in error.findings])  # ['statements_not_found']
    statements = error.item  # 그래도 쓰려면. result.item("8", strict=False)와 같다
except MissingItemError as error:  # 문서에 표기는 있는데 구간을 못 찾았다
    print(error.key, error)
```

- **None은 실패가 아니라 "없음"입니다.** 문서가 생략한 Item(`result.omitted`)과 카탈로그에 없는 번호는 예외 없이
  None입니다. 정정 공시(`/A`)는 일부 Item만 담는 것이 정상이라 누락 경고도 내지 않습니다.
- 예외가 없어도 `item.warnings`를 보세요. 목차·배치 경고(`toc_target_missing`, `non_sequential_layout`)는 맞게 찾은
  Item에도 붙어서 예외에서 뺐습니다. 공시 전체의 경고는 `result.warnings`입니다.
- 본문이 "위임장을 참조로 편입한다"는 문장뿐인 Item이 있습니다(`item.incorporated_by_reference`). Part III는 그게
  정상입니다. 8-K 첨부 보도자료(EX-99.1)처럼 다른 파일에 있는 내용은 읽지 않습니다.
- 본문이 같은 문서의 다른 쪽에 있으면 `item.ranges`가 여럿입니다(Item 8 "See pages F-1 through F-30" → 서명란 뒤
  F-쪽). 결합 헤딩("Items 1 and 2. Business and Properties")은 두 Item이 같은 구간을 가리킵니다(`item.shared_with`).
- 20-F 등 다른 서식은 `extract_items`가 `ValueError`를 내고, 2001년 이전의 텍스트(.txt) 공시는 범위 밖입니다.
- 읽으며 고친 HTML 결함(닫히지 않은 태그, 숨긴 내용, 머리말 제거)은 `result.document.report`에 위치와 함께 남습니다.

## 표와 주석

```python
from cluefin_sec_notes import parse_amount, split_notes, unit_scale

split = split_notes(result.item("8"))  # 10-Q는 result.item("1", part="I")
for note in split:  # 첫 원소는 첫 주석 앞의 감사보고서·본표(number=None, title="statements")
    print(note.number, note.title, len(note.text))
    for table in note.tables:
        print(table.unit, unit_scale(table.unit), table.grid()[:2])  # 'in thousands, except per share amounts' 1000 …

parse_amount("$(1,234)")  # Decimal('-1234'). "(35)"는 각주 표시가 아니라 -35, 대시·글자는 None
```

- **값은 곱하지 않습니다.** `Table.unit`은 표 머리나 바로 앞 문단의 단위 문구 그대로이고, 배수는 `unit_scale`이 줍니다.
  "except per share amounts"가 붙은 표의 주당 값에는 곱하면 안 됩니다.
- `split`의 원소가 하나뿐이면 주석 헤딩을 하나도 찾지 못한 것입니다. `split.findings`의 `note_sequence_gap`은 번호가
  건너뛰었다는 뜻이고, 대개 읽지 못한 모양의 헤딩이 그 사이에 있습니다.
- 문자 번호("Note C")는 `number`가 A=1부터 센 값(3)이고 적힌 표기는 `label`("C")입니다.

## 내부자 소유 신고 (Form 3·4·5)

임원·이사·10% 주주가 회사 주식을 사고팔거나(Form 4, 2영업일 안), 처음 보유를 신고하거나(Form 3), 연간 신고(Form 5)할 때
내는 XML입니다. 정정(`/A`)도 같은 형식입니다.

```python
from cluefin_sec_notes.ownership import load_ownership

filing = client.submissions.filings(cik, forms=["4"])[0]
# 주 문서명은 SEC가 XSL로 렌더링한 경로(xslF345X05/form4.xml)다. 파일명만 떼면 원본 XML이다
name = filing.primary_document.rsplit("/", 1)[-1]
path = client.archives.download_filing_document(cik, filing.accession_number, name, destination="ownership")

doc = load_ownership(path)
print(doc.issuer.trading_symbol, [owner.officer_title for owner in doc.reporting_owners])
for t in doc.non_derivative_transactions:
    print(t.date, t.code, t.shares, t.price, t.acquired_disposed, t.shares_owned_after)
    for field, ids in t.footnote_ids.items():  # 예: {"price": ("F2",)} — "가중평균, 범위 $262.00–$262.67"
        print(" ", field, [doc.footnotes[i] for i in ids])
```

- `code`는 SEC 거래 코드입니다. P 장내 매수, S 장내 매도, A 보상 지급, M 옵션 행사, F 세금 원천징수분, G 증여 등.
  매수 신호로 쓸 만한 P는 드뭅니다(표본 거래 1,035건 중 32건, 2026-10-12).
- 값이 없으면 None입니다. 옵션 행사(M) 가격처럼 값 대신 각주만 있는 칸이 흔해서, 각주는 필드별 `footnote_ids`로 남깁니다.
- 발행사(`doc.issuer`)가 제출 이력을 조회한 회사가 아닐 수 있습니다. 그 회사가 다른 회사 지분을 신고한 경우입니다.
- `aff10b5_one`(사전 매매 계획 10b5-1에 따른 거래인지)은 2023년부터 있는 칸이라 그전 공시는 None입니다.
- 정정은 원본과 합치지 않습니다. 서명·비고만 고쳐 행이 없는 정정도 있습니다.

## 기관 보유 보고 (13F)

운용자산 1억 달러 이상 운용사가 분기 말 보유 미국 상장 증권을 45일 안에 내는 보고입니다. 공시 폴더에 표지
`primary_doc.xml`과 보유 목록인 정보표 XML이 있고, 13F-NT(통지)는 다른 운용사가 대신 보고한다는 표지뿐입니다.
2013년 상반기 이전 공시는 XML이 아닌 텍스트라 읽지 않습니다.

```python
from cluefin_sec_notes.ownership import load_13f

filing = client.submissions.filings(cik, forms=["13F-HR"])[0]
# 정보표 파일명은 공시마다 다르다. download_13f_files가 표지가 아닌 XML 하나를 골라 준다
files = client.archives.download_13f_files(cik, filing.accession_number, destination="13f")

doc = load_13f(files.cover, files.information_table, filed=filing.filing_date)
print(doc.cover.period_of_report, doc.cover.report_type, doc.table.value_unit_suspect)
for row in doc.holdings:
    print(row.cusip, row.name_of_issuer, row.value, row.shares, row.shares_type, row.put_call, row.other_managers)
```

- **`value`는 달러로 맞춰 줍니다.** 2023-01-03 이후 제출분은 달러, 그전은 천 달러로 적혀 있어 제출일(`filed`)이
  필요합니다. 보고 기준일이 아니라 제출일 기준입니다(2023년에 낸 2020년 기간 정정분도 달러). 규칙과 다른 단위로 낸
  공시가 있어(표본 약 5%, 2026-10-12) 주당 금액 중앙값이 1–5,000달러 밖이면 `table.value_unit_suspect`가 True입니다.
  값은 고치지 않습니다.
- 정보표에는 티커가 없습니다. CUSIP(대문자로만 맞춤)과 발행사명, 일부 공시의 FIGI뿐입니다.
- 한 종목이 여러 행일 수 있습니다. 투자 재량(`investment_discretion`)·함께 보고하는 운용사(`other_managers`, 표지
  `included_managers`의 순번)·풋/콜마다 행이 나뉩니다.
- 정정(`/A`)의 `amendment_type`은 RESTATEMENT(전체 재작성)·NEW HOLDINGS(보유 추가)입니다. 원본과 합치지 않습니다.
- 표지의 합계(`table_entry_total`·`table_value_total`)는 적힌 그대로입니다. 실제 행·금액과 다른 공시가 있습니다.
