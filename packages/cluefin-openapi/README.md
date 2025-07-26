# cluefin-openapi

> **cluefin-openapi**: 투자 OpenAPI를 위한 Python 클라이언트

---

## 🚀 주요 기능

- **계좌 정보 조회**: 잔고, 보유종목, 수익률 등 계좌 관련 정보
- **국내/해외 주식 정보**: 실시간 시세, 종목 정보, 기업 정보
- **차트 데이터 및 분석**: 일/주/월 차트, 기술적 지표, 시계열 데이터
- **ETF, 섹터, 테마**: ETF 정보, 업종별 정보, 테마별 종목 분류
- **시장 상황 모니터링**: 시장 지수, 거래량, 시장 동향
- **주문 관리**: 매수/매도 주문, 주문 조회, 실시간 체결 알림
- **KRX 시장 데이터**: KOSPI/KOSDAQ/KONEX 일별매매정보, 시장지수, 종목 기본정보
- **채권 시장 정보**: 국고채, 일반채권, 소액채권 시장 데이터
- **파생상품 정보**: 선물/옵션 거래정보, KOSPI/KOSDAQ 파생상품 데이터
- **상장 상품 정보**: ETF, ETN, ELW 등 거래소 상장 상품 데이터
- **ESG 및 원자재**: ESG 채권, 유가, 금, 배출권 시장 정보

## ⚡ Quick Start

### 설치

```bash
# 기본 설치
pip install cluefin-openapi

# 개발 환경에서 설치
git clone https://github.com/kgcrom/cluefin
cd cluefin
pip install -e .
```

### 기본 사용법

```python
import os
from cluefin_openapi.kiwoom._auth import Auth
from cluefin_openapi.kiwoom._client import Client

# 인증 설정
auth = Auth(
    app_key=os.getenv("KIWOOM_APP_KEY"),
    secret_key=os.getenv("KIWOOM_SECRET_KEY"),
    env="dev",  # 개발환경: "dev", 운영환경: "prod"
)

# 토큰 생성 및 클라이언트 초기화
token = auth.generate_token()
client = Client(token=token.token, env="dev")

# 삼성전자(005930) 일별 실현손익 조회
response = client.account.get_daily_stock_realized_profit_loss_by_date("005930", "20250630")
print("응답 헤더:", response.headers)
print("응답 데이터:", response.body)
```


## 🎯 왜 cluefin-openapi인가요?

### 통합된 인터페이스
키움증권, DART, KRX 등 여러 금융 OpenAPI를 하나의 Python 인터페이스로 통합하여 제공합니다.

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


### 2. 한국거래소 OpenAPI 신청

1. [한국거래소 OpenAPI 사이트](http://openapi.krx.co.kr/contents/OPP/MAIN/main/index.cmd)에서 계정 생성
2. API 인증키 신청 및 승인 대기
3. 사용할 API 마다 신청 및 승인 대기

### 3. 환경 변수 설정

```bash
$> cp .env.sample .env

# .env 파일 수정

# 키움증권 API 키 설정
KIWOOM_APP_KEY=your_app_key_here
KIWOOM_SECRET_KEY=your_secret_key_here

# 한국거래소 API 키 설정
KRX_AUTH_KEY=your_krx_auth_key_here
```

## 📚 API 문서

### 인증 (Authentication)

```python
# 키움증권
from cluefin_openapi.kiwoom._auth import Auth

auth = Auth(
    app_key="your_app_key",
    secret_key="your_secret_key",
    env="dev"  # "dev" 또는 "prod"
)

# 토큰 생성
token = auth.generate_token()
```

### 클라이언트 초기화

```python
# 키움증권
from cluefin_openapi.kiwoom._client import Client

client = Client(
    token=token.token,
    env="dev",
)

# 한국거래소
from cluefin_openapi.krx._client import Client as KRXClient

# 기본 설정
krx_client = KRXClient(auth_key="your_krx_auth_key", timeout=30)

# 커스텀 타임아웃 설정 (대용량 데이터 조회시)
krx_client = KRXClient(auth_key="your_krx_auth_key", timeout=60)
```

## 📊 KRX API 사용 예제

### 주식 시장 데이터

```python
from cluefin_openapi.krx._client import Client as KRXClient

# KRX 클라이언트 초기화
krx_client = KRXClient(auth_key="your_krx_auth_key")

# KOSPI 일별매매정보 조회
kospi_data = krx_client.stock.get_kospi("20250721")
print("KOSPI 데이터:", kospi_data.body)

# KOSDAQ 일별매매정보 조회
kosdaq_data = krx_client.stock.get_kosdaq("20250721")
print("KOSDAQ 데이터:", kosdaq_data.body)

# KONEX 일별매매정보 조회
konex_data = krx_client.stock.get_konex("20250721")
print("KONEX 데이터:", konex_data.body)

# 워런트 및 신주인수권증서 조회
warrant_data = krx_client.stock.get_warrant("20250721")
subscription_warrant_data = krx_client.stock.get_subscription_warrant("20250721")

# 종목 기본정보 조회
kospi_base_info = krx_client.stock.get_kospi_base_info("20250721")
kosdaq_base_info = krx_client.stock.get_kosdaq_base_info("20250721")
konex_base_info = krx_client.stock.get_konex_base_info("20250721")
```

### 시장 지수 정보

```python
# KRX 종합지수 조회
krx_index = krx_client.index.get_krx("20250721")
print("KRX 종합지수:", krx_index.body)

# KOSPI 지수 조회
kospi_index = krx_client.index.get_kospi("20250721")
print("KOSPI 지수:", kospi_index.body)

# KOSDAQ 지수 조회
kosdaq_index = krx_client.index.get_kosdaq("20250721")
print("KOSDAQ 지수:", kosdaq_index.body)

# 채권 지수 조회
bond_index = krx_client.index.get_bond("20250721")

# 파생상품 지수 조회
derivatives_index = krx_client.index.get_derivatives("20250721")
```

### 일괄 데이터 조회 예제

```python
import asyncio
from datetime import datetime, timedelta

# 특정 날짜의 주요 시장 데이터 일괄 조회
def get_market_overview(date: str):
    """특정 날짜의 시장 개요 데이터를 조회합니다."""
    try:
        # 주식 시장 데이터
        kospi = krx_client.stock.get_kospi(date)
        kosdaq = krx_client.stock.get_kosdaq(date)
        
        # 지수 데이터
        krx_index = krx_client.index.get_krx(date)
        
        # ETF 데이터
        etf = krx_client.exchange_traded_product.get_etf(date)
        
        return {
            "date": date,
            "kospi": kospi.body,
            "kosdaq": kosdaq.body,
            "index": krx_index.body,
            "etf": etf.body
        }
    except Exception as e:
        print(f"데이터 조회 중 오류 발생: {e}")
        return None

# 사용 예제
market_data = get_market_overview("20250721")
if market_data:
    print("시장 개요 데이터 조회 완료")
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
from cluefin_openapi.kiwoom._exceptions import KiwoomAPIError

try:
    response = client.account.get_inquire_balance()
except KiwoomAPIError as e:
    print(f"API 에러: {e.message}")
    print(f"에러 코드: {e.error_code}")
except Exception as e:
    print(f"일반 에러: {str(e)}")
```

### 일반적인 에러 시나리오

**키움증권 API 에러 코드:**
- `40010000`: 잘못된 요청 형식
- `40080000`: 토큰 만료
- `50010000`: 서버 내부 오류

**KRX API 에러 시나리오:**
- `401`: 인증 실패 - AUTH_KEY 확인 필요
- `403`: 접근 권한 없음 - API 사용 신청 상태 확인 필요
- `400`: 잘못된 요청 - 날짜 형식(YYYYMMDD) 등 파라미터 확인 필요
- `500`: 서버 오류 - 네트워크 상태 확인 및 재시도 필요

## 🧪 테스트

```bash
# 단위 테스트 실행
pytest packages/cluefin-openapi/tests/unit/ -v

# 통합 테스트 실행 (API 키 필요)
pytest packages/cluefin-openapi/tests/integration/ -v

# 코드 커버리지 확인
pytest --cov=cluefin_openapi --cov-report=html
```

## 🛠️ 개발 가이드

프로젝트는 다음 도구들을 사용합니다:

- **Uv**: Rust로 만들어진 Python 패키지 메니저
- **Ruff**: 코드 포맷팅 및 린팅
- **pytest**: 테스트 프레임워크
- **Pydantic**: 데이터 검증

```bash
# 코드 포맷팅
ruff format packages/cluefin-openapi/

# 린팅 확인
ruff check packages/cluefin-openapi/
```

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](../../LICENSE) 파일을 참조하세요.

## 📞 지원 및 문의

- **이슈 및 버그 리포트**: [GitHub Issues](https://github.com/kgcrom/cluefin/issues)
- **기능 요청**: [GitHub Discussions](https://github.com/kgcrom/cluefin/discussions)

## 🔗 관련 링크

- [키움증권 OpenAPI 포털](https://openapi.kiwoom.com/)
- [한국거래소 OpenAPI 포털](http://openapi.krx.co.kr)
- [Cluefin 메인 프로젝트](https://github.com/kgcrom/cluefin)

---

> ⚠️ **투자 주의사항**: 이 프로젝트는 키움증권과 공식적으로 연관되지 않습니다. 
> 투자는 신중하게 하시고, 모든 투자 손실에 대한 책임은 투자자 본인에게 있습니다.
