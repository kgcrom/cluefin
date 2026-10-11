# cluefin-xbrl

DART(전자공시시스템)와 SEC EDGAR의 재무제표 XBRL 문서를 파싱하는 Python 라이브러리입니다. 받아 오기는
`cluefin-openapi`(DART `dart`, SEC `sec` 모듈)가 맡고, 이 패키지는 받은 파일만 읽습니다.

## 특징

- XBRL 파일/디렉터리 파싱 (`parse_xbrl_file`, `parse_xbrl_directory`) — DART `.xbrl`, SEC `*_htm.xml`(인라인 XBRL에서 뽑은 인스턴스)·2019년 이전 `*.xml`
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

# XBRL 파일 파싱 (디렉터리는 parse_xbrl_directory 사용). 재무제표 추출에는 택소노미가 필요하다
doc = parse_xbrl_file("path/to/filing.xbrl", include_taxonomy=True)

# 재무제표 추출
parsed = extract_financial_statements(doc)

# 재무제표 유형별 접근 (BS, IS, CIS, CF, SCE)
for statement_type, statement in parsed.statements.items():
    print(statement_type, len(statement.line_items), "line items")
    rows = statement_to_dicts(statement)  # list[dict]
```

### SEC 공시

```python
import os

from cluefin_openapi.sec import Client
from cluefin_xbrl import extract_financial_statements, parse_xbrl_directory

user_agent = os.environ["SEC_USER_AGENT"]  # "이름 이메일"
Client(user_agent=user_agent).archives.download_xbrl_files(320193, "0000320193-23-000106", destination="aapl-fy2023")

# Arelle 이 US-GAAP·DEI 택소노미를 처음 한 번 웹에서 받아 캐시한다. http_user_agent 로 SEC 정책대로 신원을 밝힌다
doc = parse_xbrl_directory("aapl-fy2023", include_taxonomy=True, http_user_agent=user_agent)
parsed = extract_financial_statements(doc)  # statements: BS, IS, CIS, CF, SCE (미국 공시는 연결만)
```

## 예제 노트북

`examples/` 에 DART 에서 사업보고서 XBRL 을 내려받아 삼성전자·현대차의 본표와 주석을 분석하는 Jupyter 노트북이 있습니다.

```bash
# 워크스페이스 루트에서 실행 — .env.test 의 DART_AUTH_KEY 를 사용합니다
uv run --with jupyter jupyter lab packages/cluefin-xbrl/examples/xbrl_analysis.ipynb
```

## 주요 API

| 함수 | 설명 |
|------|------|
| `parse_xbrl_file(path, *, include_taxonomy=False, http_user_agent=None)` | 단일 XBRL 파일을 파싱해 `XbrlDocument` 반환 |
| `parse_xbrl_directory(directory, *, include_taxonomy=False, http_user_agent=None)` | 디렉터리 내 XBRL 인스턴스(DART `.xbrl`, SEC `*_htm.xml` 등)를 찾아 파싱 |
| `extract_financial_statements(doc)` | `XbrlDocument`에서 재무제표를 구조화해 `ParsedFinancialStatements` 반환 |
| `statement_to_dicts(statement)` | `FinancialStatement`을 `list[dict]`로 변환 |
| `extract_taxonomy(model_xbrl)` | 프레젠테이션 택소노미 정보(`TaxonomyInfo`) 추출 |
