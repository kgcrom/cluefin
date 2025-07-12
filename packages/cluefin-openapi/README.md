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

## ⚡ Quick Start

### 설치

```bash
# 기본 설치
pip install cluefin-openapi

# 키움증권 종속성 포함 설치
pip install "cluefin-openapi[kiwoom]"

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

### 2. 환경 변수 설정

```bash
# .env 파일 생성
KIWOOM_APP_KEY=your_app_key_here
KIWOOM_SECRET_KEY=your_secret_key_here
```


## 📚 API 문서

### 인증 (Authentication)

```python
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
from cluefin_openapi.kiwoom._client import Client

client = Client(
    token=token.token,
    env="dev",
)
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

### 일반적인 에러 코드

- `40010000`: 잘못된 요청 형식
- `40080000`: 토큰 만료
- `50010000`: 서버 내부 오류

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

### 코드 스타일

프로젝트는 다음 도구들을 사용합니다:

- **Ruff**: 코드 포맷팅 및 린팅
- **pytest**: 테스트 프레임워크
- **Pydantic**: 데이터 검증

```bash
# 코드 포맷팅
ruff format packages/cluefin-openapi/

# 린팅 확인
ruff check packages/cluefin-openapi/
```

### 브랜치 전략

1. `main` 브랜치에서 새 브랜치 생성
2. 기능 개발 후 Pull Request 생성
3. 코드 리뷰 완료 후 머지

## 🤝 기여하기

프로젝트에 기여하는 방법:

1. **이슈 보고**: 버그나 개선사항을 [GitHub Issues](https://github.com/kgcrom/cluefin/issues)에 등록
2. **풀 리퀘스트**: 코드 개선이나 새 기능 추가
3. **문서 개선**: README나 코드 주석 개선
4. **테스트 추가**: 테스트 커버리지 향상

자세한 내용은 [CONTRIBUTING.md](../CONTRIBUTING.md)를 참조하세요.

### 기여 가이드라인

- 코드 스타일 가이드 준수
- 적절한 테스트 코드 작성
- 명확한 커밋 메시지 작성
- 문서 업데이트 (필요시)

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](../../LICENSE) 파일을 참조하세요.

## 📞 지원 및 문의

- **이슈 및 버그 리포트**: [GitHub Issues](https://github.com/kgcrom/cluefin/issues)
- **기능 요청**: [GitHub Discussions](https://github.com/kgcrom/cluefin/discussions)

## 🔗 관련 링크

- [키움증권 OpenAPI 포털](https://openapi.kiwoom.com/)
- [한국거래서 OpenAPI 포털](http://openapi.krx.co.kr)
- [Cluefin 메인 프로젝트](https://github.com/kgcrom/cluefin)

---

> ⚠️ **투자 주의사항**: 이 프로젝트는 키움증권과 공식적으로 연관되지 않습니다. 
> 투자는 신중하게 하시고, 모든 투자 손실에 대한 책임은 투자자 본인에게 있습니다.
