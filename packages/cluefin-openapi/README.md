# cluefin-openapi

> **cluefin-openapi**: 주식 투자 OpenAPI를 위한 Python 클라이언트

![Python](https://img.shields.io/badge/Python-3.10%2B-green)
![Pydantic](https://img.shields.io/badge/Pydantic-Type%20Safe-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🚀 주요 기능

- **계좌 정보 조회**: 잔고, 보유종목, 수익률 등 계좌 관련 정보
- **국내/해외 주식 정보**: 실시간 시세, 종목 정보, 기업 정보
- **차트 데이터 및 분석**: 일/주/월 차트, 기술적 지표, 시계열 데이터
- **ETF, 섹터, 테마**: ETF 정보, 업종별 정보, 테마별 종목 분류
- **시장 상황 모니터링**: 시장 지수, 거래량, 시장 동향
- **기업 공시 분석 (DART)**: 공시 원문, 재무제표, 대량보유상황 등 공시 데이터

## ⚡ 빠른 시작

### 설치

```bash
# 워크스페이스 설치 (권장)
git clone https://github.com/kgcrom/cluefin
cd cluefin
uv venv --python 3.10
uv sync --all-packages

# 패키지만 단독 설치
pip install cluefin-openapi
```

## 🎯 왜 cluefin-openapi인가요?

### 통합된 인터페이스
키움증권, 한국투자증권(KIS), DART 등 여러 금융 OpenAPI를 하나의 Python 인터페이스로 통합하여 제공합니다.

### 개발 시간 단축
복잡한 금융 API 통합 작업을 대신 처리하여, 투자 도구 개발에 집중할 수 있습니다.

### 타입 안전성
Pydantic을 활용한 강력한 타입 검증으로 런타임 에러를 방지합니다.

### 풍부한 기능
- 실시간 데이터 스트리밍
- 자동 토큰 갱신
- 요청 제한 관리
- 포괄적인 에러 처리

## 📖 시작하기

### 1. 키움증권 API 신청

1. [키움증권 OpenAPI 사이트](https://apiportal.kiwoom.com/)에서 계정 생성
2. API 사용 신청 및 승인 대기
3. APP_KEY 및 SECRET_KEY 발급 받기

### 2. 한국투자증권 API 신청

1. [한국투자증권 OpenAPI 사이트](https://apiportal.koreainvestment.com/)에서 계정 생성
2. API 사용 신청 및 승인 대기
3. APP_KEY 및 SECRET_KEY 발급 받기

### 3. 환경 변수 설정

```bash
# 워크스페이스 루트 디렉토리에서
cp apps/cluefin-cli/.env.sample .env

# .env 파일 수정 (워크스페이스 루트에 생성)

# 키움증권 API 키 설정 (OAuth2-style 인증)
KIWOOM_APP_KEY=your_app_key_here
KIWOOM_SECRET_KEY=your_secret_key_here
KIWOOM_ENV=dev # options: prod | dev(default)

# 한국투자증권 API 키 설정 (토큰 기반 인증)
KIS_APP_KEY=your_kis_app_key_here
KIS_SECRET_KEY=your_kis_secret_key_here
KIS_ENV=dev # options: prod | dev(default)

# 금융감독원 DART API 키 설정
DART_AUTH_KEY=your_dart_auth_key_here
```

### 기본 사용법

```python
from loguru import logger
from pydantic import SecretStr
import os
from cluefin_openapi.kiwoom._auth import Auth
from cluefin_openapi.kiwoom._client import Client
import dotenv

# 인증 설정
dotenv.load_dotenv(dotenv_path=".env")
auth = Auth(
    app_key=os.getenv("KIWOOM_APP_KEY"),
    secret_key=SecretStr(os.getenv("KIWOOM_SECRET_KEY")),
    env="dev",  # 개발환경: "dev", 운영환경: "prod"
)

# 토큰 생성 및 클라이언트 초기화
token = auth.generate_token()
client = Client(token=token.get_token(), env="dev")

# 삼성전자(005930) 일별 실현손익 조회
response = client.account.get_daily_stock_realized_profit_loss_by_date("005930", "20250630")
logger.info(f"응답 헤더: ${response.headers}")
logger.info(f"응답 데이터: ${response.body}")
```

## 📚 API 문서

### 인증

```python
# 키움증권
from loguru import logger
import os
from pydantic import SecretStr
import dotenv
from cluefin_openapi.kiwoom._auth import Auth

# 인증 설정
dotenv.load_dotenv(dotenv_path=".env")

auth = Auth(
    app_key=os.getenv("KIWOOM_APP_KEY"),
    secret_key=SecretStr(os.getenv("KIWOOM_SECRET_KEY")),
    env="dev",  # 개발환경: "dev", 운영환경: "prod"
)

# 토큰 생성
token = auth.generate_token()
logger.info(f"token => ${token}")
```

### 클라이언트 초기화

```python
# 키움증권
from cluefin_openapi.kiwoom._client import Client

client = Client(
    token=token.get_token(),
    env="dev",
)
```

```python
# 한국투자증권
from loguru import logger
import os
from pydantic import SecretStr
import dotenv
from cluefin_openapi.kis._auth import Auth
from cluefin_openapi.kis._client import Client as KISClient

# 인증 설정
dotenv.load_dotenv(dotenv_path=".env")

# 토큰 생성
auth = Auth(
    app_key=os.getenv("KIS_APP_KEY"),
    secret_key=SecretStr(os.getenv("KIS_SECRET_KEY")),
    env="dev",
)
token = auth.generate()

# 클라이언트 초기화
kis_client = KISClient(
    app_key=os.getenv("KIS_APP_KEY"),
    secret_key=SecretStr(os.getenv("KIS_SECRET_KEY")),
    token=token,
    env="dev",
)
logger.info(f"kis_client => ${kis_client}")
```

## 📊 KIS API 사용 예제

### 국내 주식 시세 조회

```python
from loguru import logger
from cluefin_openapi.kis._client import Client as KISClient

# 주식 현재가 시세 조회
current_price = kis_client.domestic_basic_quote.get_inquire_price(
    fid_cond_mrkt_div_code="J",  # 시장 분류 코드 (J: 주식)
    fid_input_iscd="005930"      # 종목 코드 (삼성전자)
)
logger.info(f"현재가: {current_price}")

# 주식 일별 시세 조회
daily_price = kis_client.domestic_basic_quote.get_inquire_daily_itemchartprice(
    fid_cond_mrkt_div_code="J",
    fid_input_iscd="005930",
    fid_input_date_1="20250101",  # 조회 시작일
    fid_input_date_2="20250131",  # 조회 종료일
    fid_period_div_code="D"        # 기간 분류 코드 (D: 일)
)
logger.info(f"일별 시세: {daily_price}")
```

### 국내 계좌 조회

```python
# 주식 잔고 조회
balance = kis_client.domestic_account.get_inquire_balance(
    cano="12345678",      # 종합계좌번호
    acnt_prdt_cd="01",    # 계좌상품코드
    afhr_flpr_yn="N",     # 시간외단일가여부
    ofl_yn="N",           # 오프라인여부
    inqr_dvsn="01",       # 조회구분
    unpr_dvsn="01",       # 단가구분
    fund_sttl_icld_yn="N", # 펀드결제분포함여부
    fncg_amt_auto_rdpt_yn="N", # 융자금액자동상환여부
    prcs_dvsn="00",       # 처리구분
    ctx_area_fk100="",    # 연속조회검색조건100
    ctx_area_nk100=""     # 연속조회키100
)
logger.info(f"잔고: {balance}")
```

### 해외 주식 시세 조회

```python
# 해외 주식 현재가 조회 (미국 주식)
overseas_price = kis_client.overseas_basic_quote.get_inquire_price(
    exch="NAS",           # 거래소 코드 (NAS: 나스닥)
    symb="AAPL"           # 종목 코드 (애플)
)
logger.info(f"해외 주식 현재가: {overseas_price}")
```

## 🔧 구성 옵션

### 로깅 설정

```python
import logging
from loguru import logger

# 로그 레벨 설정
logger.add("kiwoom_api.log", level="INFO", rotation="10 MB")
```

### 요청 제한 관리

라이브러리는 자동으로 API 요청 제한을 관리합니다:

- 초당 요청 수 제한
- 일일 요청 수 제한
- 자동 재시도 메커니즘

## ⚠️ 에러 처리

### 키움증권 API 에러 처리

```python
from loguru import logger
from cluefin_openapi.kiwoom._exceptions import KiwoomAPIError

try:
    response = client.account.get_inquire_balance()
except KiwoomAPIError as e:
    logger.info(f"API 에러: {e.message}")
    logger.info(f"에러 코드: {e.error_code}")
except Exception as e:
    logger.info(f"일반 에러: {str(e)}")
```

### 한국투자증권 API 에러 처리

```python
from loguru import logger
from cluefin_openapi.kis._exceptions import KISAPIError

try:
    response = kis_client.domestic_basic_quote.get_inquire_price(
        fid_cond_mrkt_div_code="J",
        fid_input_iscd="005930"
    )
except KISAPIError as e:
    logger.error(f"KIS API 에러: {e.message}")
    logger.error(f"에러 코드: {e.error_code}")
except Exception as e:
    logger.error(f"일반 에러: {str(e)}")
```

### 일반적인 에러 시나리오

**키움증권 API 에러 코드:**
- `40010000`: 잘못된 요청 형식
- `40080000`: 토큰 만료
- `50010000`: 서버 내부 오류

**한국투자증권 API 에러 코드:**
- `EGW00001`: 잘못된 요청 형식
- `EGW00123`: API 키 오류
- `EGW00201`: 토큰 만료 - 토큰 재생성 필요 (1분 간격 제한)
- `40000000`: 서버 내부 오류

## 🧪 테스트

```bash
# 워크스페이스 루트에서 실행

# 단위 테스트만 실행 (통합 테스트 제외)
uv run pytest -m "not integration"

# 통합 테스트만 실행 (API 키 필요)
uv run pytest -m "integration"

# KIS integration 테스트 실패 시 마지막 raw 응답 출력
# 기본값은 조용함. 필요할 때만 켜서 사용
KIS_DEBUG_ON_FAILURE=1 uv run pytest packages/cluefin-openapi/tests/kis/ -m "integration"

# Kiwoom 통합 테스트는 .env.test의 KIWOOM_ENV(dev|prod)를 사용
# - KIWOOM_ENV=dev  -> mockapi 키 사용
# - KIWOOM_ENV=prod -> 실서버 키 사용

# 권한/샌드박스 환경에서 uv 캐시 접근 오류가 나면
# (예: ".../.cache/uv/... Operation not permitted")
# 워크스페이스 내부 캐시 경로를 지정해서 실행
mkdir -p .uv-cache
UV_CACHE_DIR=.uv-cache uv run pytest packages/cluefin-openapi/tests/kiwoom/test_domestic_chart_integration.py -q

# cluefin-openapi 패키지 테스트만 실행
uv run pytest packages/cluefin-openapi/tests/ -v

# 특정 모듈 테스트 실행
uv run pytest packages/cluefin-openapi/tests/kiwoom/test_auth_unit.py -v

# 코드 커버리지 확인
uv run pytest --cov=cluefin_openapi --cov-report=html
```

### KIS 통합 테스트 디버깅

- 기본적으로 KIS integration 테스트 실패 시 raw 응답을 출력하지 않습니다.
- 필요할 때만 `KIS_DEBUG_ON_FAILURE=1` 를 주면 실패한 테스트의 마지막 KIS 응답이 같이 출력됩니다.
- 출력에는 `status_code`, `tr_id`, `path`, 요청 파라미터 요약, `response_preview`, `artifact_path` 가 포함됩니다.
- 전체 payload는 `artifact_path` 로 표시된 `/tmp/cluefin-kis-debug/*.json` 파일에서 확인할 수 있습니다.

```bash
# KIS integration 실패 시 마지막 raw 응답 보기
KIS_DEBUG_ON_FAILURE=1 uv run pytest packages/cluefin-openapi/tests/kis/test_domestic_market_analysis_integration.py -m "integration"
```

### 통합 테스트 실행 이슈 (uv 캐시 권한)

- 증상: `uv run pytest ...` 실행 시 `.../.cache/uv/... Operation not permitted`
- 원인: 실행 환경(샌드박스/권한 정책)에서 기본 uv 캐시 경로 접근이 제한됨
- 해결:
  1. 워크스페이스 내부 캐시 디렉터리 생성: `mkdir -p .uv-cache`
  2. 실행 시 캐시 경로 지정: `UV_CACHE_DIR=.uv-cache uv run pytest <file_or_args>`
  3. 필요하면 동일 세션에서 `export UV_CACHE_DIR=.uv-cache` 후 반복 실행

## 🏗️ 프로젝트 구조

```
packages/cluefin-openapi/
├── src/cluefin_openapi/
│   ├── dart/                      # 금융감독원 DART 공시 클라이언트
│   ├── kiwoom/                    # 키움증권 API 클라이언트
│   ├── kis/                       # 한국투자증권 API 클라이언트
│   └── __init__.py
├── tests/                        # 테스트 스위트
│   ├── kiwoom/                   # 키움증권 API 테스트
│   │   ├── test_*_unit.py        # 단위 테스트 (requests_mock 사용)
│   │   └── test_*_integration.py # 통합 테스트 (@pytest.mark.integration)
│   ├── kis/                       # 한국투자증권 API 테스트
│   │   ├── test_*_unit.py        # 단위 테스트 (Mock 사용, JSON 테스트 케이스)
│   │   └── test_*_integration.py # 통합 테스트 (@pytest.mark.integration)
│   └── dart/                      # Dart API 테스트
│       ├── test_*_unit.py        # 단위 테스트
│       └── test_*_integration.py # 통합 테스트
├── pyproject.toml               # 패키지 의존성 및 설정
└── README.md                    # 이 문서
```

### 핵심 설계 패턴

**응답 래퍼 패턴**: 모든 API 응답을 구조화된 형태로 반환
```python
@dataclass
class KiwoomHttpResponse(Generic[T]):
    headers: KiwoomHttpHeader  # 헤더 정보 (연속조회키 등)
    body: T                    # 응답 데이터 (Pydantic 모델)
```

**한국 금융 API 특화 기능**:
- 한국 시장 시간대(KST) 처리
- 한국 주식 코드 형식 (6자리, 예: "005930")
- 한국어 필드명에 대한 영어 별칭: `cont_yn: Literal["Y", "N"] = Field(..., alias="cont-yn")`

## 🛠️ 개발 가이드

프로젝트는 다음 도구들을 사용합니다:

- **Uv**: Rust로 만들어진 Python 패키지 메니저
- **Ruff**: 코드 포맷팅 및 린팅
- **pytest**: 테스트 프레임워크
- **Pydantic**: 데이터 검증 및 타입 안전성
- **requests**: HTTP 클라이언트
- **loguru**: 구조화된 로깅

```bash
# 워크스페이스 루트에서 실행

# 코드 포맷팅 (전체 프로젝트)
uv run ruff format .

# 린팅 확인 및 자동 수정
uv run ruff check . --fix

# cluefin-openapi만 포맷팅
uv run ruff format packages/cluefin-openapi/

# cluefin-openapi만 린팅
uv run ruff check packages/cluefin-openapi/
```

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](../../LICENSE) 파일을 참조하세요.

## 🔗 관련 링크

- [키움증권 OpenAPI 포털](https://openapi.kiwoom.com/)
- [한국투자증권 OpenAPI 포털](https://apiportal.koreainvestment.com/)
- [금융감독원 OpenAPI 포털](https://opendart.fss.or.kr/)

---

> ⚠️ **투자 주의사항**: 이 프로젝트는 키움증권, 한국투자증권과 공식적으로 연관되지 않습니다.
> 투자는 신중하게 하시고, 모든 투자 손실에 대한 책임은 투자자 본인에게 있습니다.
