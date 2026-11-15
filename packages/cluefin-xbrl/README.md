# cluefin-xbrl

DART(전자공시시스템)와 SEC EDGAR의 재무제표 XBRL을 읽어 본표(재무상태표·손익계산서·포괄손익계산서·현금흐름표·자본변동표)와
DART 주석을 행 단위로 꺼내는 패키지입니다. 받아 오기는 `cluefin-openapi`(DART `dart`, SEC `sec` 모듈)가 맡고, 이
패키지는 받은 파일만 읽습니다. uv 워크스페이스 멤버라 저장소 루트에서 `uv sync --all-packages`로 설치합니다.

## 사용

```python
from cluefin_openapi.dart import Client
from cluefin_xbrl import extract_financial_statements, extract_notes, parse_xbrl_directory, statement_to_dicts

# rcept_no: 정기보고서 접수번호(14자리). ZIP을 풀어 놓은 폴더 경로를 돌려준다
dart = Client(auth_key="…").periodic_report_financial_statement
folder = dart.download_financial_statement_xbrl(rcept_no, "11011", destination="xbrl")

doc = parse_xbrl_directory(folder, include_taxonomy=True)  # 본표·주석 추출에는 택소노미가 필요하다
parsed = extract_financial_statements(doc)

# 연결은 statements, 별도는 separate_statements. 키는 BS·IS·CIS·CF·SCE 가운데 그 공시에 있는 것만
for key, statement in parsed.statements.items():
    rows = statement_to_dicts(statement)  # list[dict]. value는 float이다(정확한 값은 line_items의 Decimal)
    print(key, statement.is_consolidated, len(statement.line_items))
separate_bs = parsed.separate_statements.get("BS")

notes = extract_notes(doc)  # DART 전용. SEC 공시는 빈 결과
for role_code, section in notes.notes.items():  # D8xxxxx(금융업은 DB8xxxxx 등). 끝자리 0은 연결, 5는 별도
    print(role_code, section.title, section.is_consolidated, len(section.line_items))
```

### SEC 공시

```python
import os

from cluefin_openapi.sec import Client
from cluefin_xbrl import extract_financial_statements, parse_xbrl_directory

user_agent = os.environ["SEC_USER_AGENT"]  # "이름 이메일"
Client(user_agent=user_agent).archives.download_xbrl_files(320193, "0000320193-23-000106", destination="aapl-fy2023")

# SEC 공시는 http_user_agent가 필수다. 없거나 이메일이 빠지면 택소노미 캐시가 차 있어도 ValueError
doc = parse_xbrl_directory("aapl-fy2023", include_taxonomy=True, http_user_agent=user_agent)
parsed = extract_financial_statements(doc)  # 미국 공시는 연결(statements)만

# 자본변동표의 자본, 현금흐름표의 현금은 기초·기말 두 행으로 나온다. 행마다 preferred_label 로 구분하고,
# 기초 행(…/periodStartLabel)에는 기간 시작 전날, 기말 행(…/periodEndLabel)에는 기간 종료일 시점 값만 있다
equity = [i for i in parsed.statements["SCE"].line_items if i.concept_local_name == "StockholdersEquity"]
```

## 걸리기 쉬운 곳

- **IS가 없는 공시가 있습니다.** 단일 포괄손익계산서를 내는 회사와 은행·보험·증권·금융지주는 손익이 CIS에만 있어
  `parsed.statements["IS"]`가 `KeyError`입니다. 종속회사가 없는 회사는 `statements`가 비고 `separate_statements`만 있습니다.
- **첫 파싱은 느립니다.** Arelle이 공시가 참조하는 택소노미를 웹에서 받아 캐시합니다(macOS는 `~/Library/Caches/Arelle`).
  빈 캐시에서 DART 공시 하나에 최대 약 76초가 걸렸습니다(2026-09-30). 오프라인에 캐시도 비어 있으면 `XbrlParseError`입니다.
- DART ZIP을 직접 풀지 마세요. FY2022 이전 ZIP은 링크베이스가 하위 폴더에 있어서, 폴더 없이 풀면 `XbrlParseError`입니다.
  `download_financial_statement_xbrl`이 맞게 풉니다.
- Arelle은 `[info] loaded …`를 stdout에 찍습니다. stdout으로 결과를 내보내는 프로그램은 파싱 호출을
  `contextlib.redirect_stdout`으로 감싸야 합니다.
- 주석은 DART만 됩니다. 금융업 공시의 주석은 FY2025부터 XBRL에 있습니다.
- `examples/` 에 DART 에서 사업보고서 XBRL 을 내려받아 삼성전자·현대차의 본표와 주석을 분석하는 노트북이 있습니다.
  저장소 루트에서 `uv run --with jupyter jupyter lab packages/cluefin-xbrl/examples/xbrl_analysis.ipynb`
  (`.env.test`의 `DART_AUTH_KEY`를 씁니다).
