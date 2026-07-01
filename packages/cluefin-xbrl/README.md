# cluefin-xbrl

DART(전자공시시스템)가 제공하는 한국 기업 재무제표 XBRL 문서를 파싱하는 순수 Python 라이브러리입니다.

## 특징

- XBRL 파일/디렉터리 파싱 (`parse_xbrl_file`, `parse_xbrl_directory`)
- 재무상태표·손익계산서 등 재무제표 구조화 추출 (`extract_financial_statements`)
- 재무제표를 dict 리스트로 변환 (`statement_to_dicts`)
- 프레젠테이션 택소노미 정보 추출 (`extract_taxonomy`)
- Pydantic 기반 타입 모델 (`XbrlDocument`, `FinancialStatement`, `ParsedFinancialStatements` 등)

## 설치

uv 워크스페이스 멤버로, 저장소 루트에서 설치합니다.

```bash
uv sync --all-packages
```

**요구사항**: Python 3.10+

## 사용

```python
from cluefin_xbrl import (
    parse_xbrl_file,
    extract_financial_statements,
    statement_to_dicts,
)

# XBRL 파일 파싱 (디렉터리는 parse_xbrl_directory 사용)
doc = parse_xbrl_file("path/to/filing.xbrl")

# 재무제표 추출
parsed = extract_financial_statements(doc)

# 재무제표 유형별 접근 (BS, IS, CIS, CF, SCE)
for statement_type, statement in parsed.statements.items():
    print(statement_type, len(statement.line_items), "line items")
    rows = statement_to_dicts(statement)  # list[dict]
```

## 주요 API

| 함수 | 설명 |
|------|------|
| `parse_xbrl_file(path, *, include_taxonomy=False)` | 단일 XBRL 파일을 파싱해 `XbrlDocument` 반환 |
| `parse_xbrl_directory(directory, *, include_taxonomy=False)` | 디렉터리 내 XBRL 문서를 파싱 |
| `extract_financial_statements(doc)` | `XbrlDocument`에서 재무제표를 구조화해 `ParsedFinancialStatements` 반환 |
| `statement_to_dicts(statement)` | `FinancialStatement`을 `list[dict]`로 변환 |
| `extract_taxonomy(model_xbrl)` | 프레젠테이션 택소노미 정보(`TaxonomyInfo`) 추출 |
