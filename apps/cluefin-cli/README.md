# Cluefin CLI

기술적 지표, 터미널 차트 및 **머신러닝 기반 가격 예측**을 제공하는 한국 주식 시장 분석용 강력한 명령줄 인터페이스입니다.

![CLI Demo](https://img.shields.io/badge/CLI-Korean%20Stock%20Analysis-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-green)
![ML](https://img.shields.io/badge/ML-LightGBM%20%2B%20SHAP-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ 주요 기능

### **포괄적 주식 분석**
- 실시간 한국 주식 데이터 분석 (KOSPI, KOSDAQ)
- 외국인 거래량 분석 (매수/매도 흐름)
- 시장 지수 모니터링 (KOSPI, KOSDAQ)
- 다중 기간 분석 (1개월, 3개월, 6개월, 1년)
- DART 공시 기반 펀더멘털 데이터 (배당, 재무지표, 주요 주주)

### **기술적 지표**
- **RSI (상대강도지수)** - 과매수/과매도 상황을 위한 모멘텀 오실레이터
- **MACD (이동평균수렴확산)** - 추세 추종 모멘텀 지표
- **이동평균선** - SMA(5, 20, 50) 및 EMA(12, 26)
- **볼린저 밴드** - 변동성 및 추세 분석
- **스토캐스틱 오실레이터** - 종가와 가격대를 비교하는 모멘텀 지표
- **지지/저항 레벨** - 주요 가격대 식별

### **터미널 시각화**
- 터미널에서 직접 렌더링되는 아름다운 ASCII 차트
- 이동평균선 오버레이가 포함된 가격 차트
- 거래량 분석 차트
- 과매수/과매도 구간이 포함된 RSI 오실레이터 시각화
- MACD 히스토그램 및 시그널 라인 차트
- 색상으로 구분된 데이터가 포함된 풍부한 형식의 테이블


### **🤖 머신러닝 예측**
- **LightGBM 기반 분류** - 익일 가격 움직임에 대한 이진 예측
- **150개 이상의 기술적 지표** - cluefin-ta를 사용한 향상된 피처 엔지니어링
- **SHAP 모델 해석가능성** - 예측을 주도하는 피처 이해
- **피처 중요도 분석** - 가격 움직임에 영향을 미치는 주요 요소 식별
- **시계열 교차검증** - 시계열 데이터를 위한 적절한 검증
- **성능 메트릭** - 정확도, 정밀도, 재현율, F1-score, AUC

## 🚀 빠른 시작

### 사전 요구사항
- Python 3.10 이상
- uv 패키지 매니저
- **LightGBM 시스템 의존성** (ML 기능용)

### 설치

1. **저장소 클론 및 워크스페이스 설정:**
```bash
git clone https://github.com/kgcrom/cluefin
cd cluefin
uv venv --python 3.10
```

2. **시스템 의존성 설치:**
```bash
# macOS
brew install lightgbm
```

3. **모든 워크스페이스 의존성 설치:**
```bash
uv sync --all-packages
```

4. **환경 설정 (선택사항):**
```bash
cp apps/cluefin-cli/.env.sample .env
# .env 파일에 API 키 설정 (KIWOOM_APP_KEY, KIWOOM_SECRET_KEY, KIWOOM_ENV, KRX_AUTH_KEY, DART_AUTH_KEY)
```

### 기본 사용법

```bash
# 기본 주식 분석
cluefin-cli ta 005930

# 터미널 차트 포함
cluefin-cli ta 005930 --chart

# 🤖 ML 예측 포함
cluefin-cli ta 005930 --ml-predict

# 📊 기본 피처 중요도 포함
cluefin-cli ta 005930 --ml-predict --feature-importance

# 🔍 상세 SHAP 분석 포함
cluefin-cli ta 005930 --ml-predict --shap-analysis

# 🚀 전체 분석 (모든 기능)
cluefin-cli ta 005930 --chart --ml-predict --shap-analysis

# 📘 펀더멘털 분석 (DART)
cluefin-cli fa 005930

# 📘 2023 사업보고서 기준 펀더멘털 분석 (상위 3명 주주)
cluefin-cli fa 005930 --year 2023 --report annual --max-shareholders 3
```

## 명령어 참조

### `ta` 명령어

포괄적인 기술적 지표 및 시장 데이터로 한국 주식을 분석합니다.

```bash
cluefin-cli ta [OPTIONS] STOCK_CODE
```

#### 인수
- `STOCK_CODE` - 한국 주식 코드 (예: 삼성전자는 `005930`)

#### 옵션
- `-c, --chart` - 터미널에서 대화형 차트 표시
- `-m, --ml-predict` - ML 기반 가격 예측 포함 🤖
- `-f, --feature-importance` - 기본 피처 중요도 표시 (--ml-predict 필요) 📊
- `-s, --shap-analysis` - 설명이 포함된 상세 SHAP 분석 표시 (--ml-predict 필요) 🔍
- `--help` - 명령어 도움말 표시

#### 예제

```bash
# 삼성전자 기본 분석
cluefin-cli ta 005930

# SK하이닉스 차트 포함
cluefin-cli ta 000660 --chart

# 삼성전자 ML 예측 포함
cluefin-cli ta 005930 --ml-predict

# LG화학 ML + 기본 피처 중요도
cluefin-cli ta 051910 --ml-predict --feature-importance

# 삼성바이오로직스 ML + 상세 SHAP 분석
cluefin-cli ta 207940 --ml-predict --shap-analysis

# LG에너지솔루션 - 전체 분석
cluefin-cli ta 373220 --chart --ml-predict --shap-analysis
```

### `fa` 명령어

DART 공시 데이터를 기반으로 기업의 펀더멘털 정보를 조회합니다.

```bash
cluefin-cli fa [OPTIONS] STOCK_CODE
```

#### 인수
- `STOCK_CODE` - 한국 주식 코드 (예: 삼성전자는 `005930`)

#### 옵션
- `--year` - 조회할 사업연도 (기본값: 전년도)
- `--report` - 공시 보고서 구분 (`annual`, `q1`, `half`, `q3`)
- `--max-shareholders` - 출력할 주요 주주 수 (기본값: 5)
- `--help` - 명령어 도움말 표시

#### 예제

```bash
# 2023 사업보고서를 기준으로 삼성전자 기본적 분석
cluefin-cli fa 005930 --year 2023 --report annual

# 상위 3명의 주요 주주만 확인
cluefin-cli fa 005930 --max-shareholders 3
```

## 📈 지원 종목

CLI는 KOSPI와 KOSDAQ에서 거래되는 모든 한국 주식을 지원합니다. 다음은 인기 종목 예시입니다:

| 종목 코드 | 회사명 | 시장 |
|----------|--------|------|
| `005930` | 삼성전자 | KOSPI |
| `000660` | SK하이닉스 | KOSPI |
| `035420` | NAVER | KOSPI |
| `051910` | LG화학 | KOSPI |
| `207940` | 삼성바이오로직스 | KOSPI |
| `373220` | LG에너지솔루션 | KOSPI |

## 설정

### 환경 변수

**워크스페이스 루트** 디렉토리에 `.env` 파일을 생성하세요:

```env
# 키움증권 API (실시간 한국 주식 데이터용)
KIWOOM_APP_KEY=your_app_key_here
KIWOOM_SECRET_KEY=your_secret_key_here
KIWOOM_ENV=prod # 옵션: prod | dev(기본값)

# 한국거래소(KRX) API
KRX_AUTH_KEY=your_auth_key_here

# 금융감독원 DART API
DART_AUTH_KEY=your_dart_auth_key_here

# ML 모델 설정 (선택사항)
ML_MODEL_PATH=models/
ML_CACHE_DIR=.ml_cache/
```

### API 연동

CLI는 `cluefin-openapi` 패키지를 통해 한국 금융 API와 연동됩니다:

1. **키움증권 API**: 실시간 주식 데이터, 주문, 계좌 정보를 위한 OAuth2 스타일 인증
2. **한국거래소(KRX)**: 시장 데이터, 지수, 섹터 정보를 위한 단순 auth_key 인증
3. **금융감독원(DART)**: 기업 공시, 정기 보고서, 배당, 주주 데이터

**참고**: API 키 없이도 데모용 목업 데이터를 사용하여 제한된 기능으로 CLI를 사용할 수 있습니다.

## 출력 예시

### 기본 분석 출력

Stock Information - 005930

| Metric        | Value            |
|---------------|------------------|
| Current Price | 64,775          |
| Change        | -1,300 (-1.97%) |
| Volume        | 7,544,353        |

Technical Indicators

| Indicator | Value    | Signal     |
|-----------|----------|------------|
| RSI (14)  | 57.60    | Neutral    |
| MACD      | 429.71   | Bullish    |
| SMA (20)  | 63,110  | Above MA20 |

### 🤖 ML 예측 출력

```
==================================================
🎯 ML Prediction Results
┌─────────────────────────────────────────────────┐
│ Signal: 📈 BUY (67.3%)                         │
│ Confidence: 67.3%                              │
│ Up Probability: 67.3%                          │
│ Down Probability: 32.7%                        │
└─────────────────────────────────────────────────┘

📊 Model Performance
┌─────────────────────────────────────────────────┐
│ Validation Accuracy: 64.2%                     │
│ Validation F1-Score: 0.638                     │
│ Validation AUC: 0.721                          │
└─────────────────────────────────────────────────┘
```

### 🔍 SHAP 분석 출력

```
🔍 Top 15 Feature Importance (SHAP)
┌──────┬─────────────────────┬────────────┬────────────┬────────────┐
│ Rank │ Feature             │ Importance │ Mean SHAP  │ Impact     │
├──────┼─────────────────────┼────────────┼────────────┼────────────┤
│  1   │ rsi_14             │   0.0234   │  +0.0156   │ 📈 UP     │
│  2   │ macd_signal        │   0.0198   │  -0.0087   │ 📉 DOWN   │
│  3   │ bb_position        │   0.0167   │  +0.0123   │ 📈 UP     │
│  4   │ volume_ratio       │   0.0142   │  +0.0089   │ 📈 UP     │
│  5   │ sma_20             │   0.0134   │  -0.0067   │ 📉 DOWN   │
└──────┴─────────────────────┴────────────┴────────────┴────────────┘
```

### 차트 시각화
`--chart` 옵션은 터미널에서 직접 아름다운 ASCII 차트를 표시합니다:
- 이동평균선이 포함된 가격 차트
- 거래량 분석
- 주요 레벨이 포함된 RSI 오실레이터
- 시그널 라인과 히스토그램이 포함된 MACD


## 개발

### 프로젝트 구조
```
apps/cluefin-cli/
├── src/cluefin_cli/              # 메인 애플리케이션 코드
│   ├── commands/                 # CLI 명령어 구현
│   │   ├── analysis/             # 기술적 분석 모듈
│   │   │   └── indicators.py     # 기술적 지표 계산
│   │   ├── technical_analysis.py # 메인 TA 명령어 (Click 기반)
│   │   ├── fundamental_analysis.py # 펀더멘털 분석 명령어
│   │   └── import_cmd.py         # 데이터 임포트 명령어
│   ├── config/                   # 애플리케이션 설정
│   │   └── settings.py           # Pydantic 설정 관리
│   ├── data/                     # 데이터 레이어 추상화
│   │   ├── duckdb_manager.py     # DuckDB 데이터베이스 관리
│   │   ├── fetcher.py            # cluefin-openapi에서 데이터 조회
│   │   ├── importer.py           # 주식 차트 데이터 임포터
│   │   ├── industry_importer.py  # 업종 코드 임포터
│   │   └── industry_chart_importer.py # 업종 차트 데이터 임포터
│   ├── display/                  # 터미널 시각화
│   │   └── charts.py             # ASCII 차트 렌더링 (plotext)
│   ├── ml/                       # 🤖 머신러닝 파이프라인
│   │   ├── diagnostics.py        # 모델 성능 평가
│   │   ├── explainer.py          # SHAP 기반 모델 해석가능성
│   │   ├── feature_engineering.py  # cluefin-ta 피처 생성 (150+ 지표)
│   │   ├── models.py             # LightGBM 분류기 구현
│   │   └── predictor.py          # 완전한 ML 예측 파이프라인
│   ├── utils/                    # 공유 유틸리티
│   │   └── formatters.py         # 한국 통화 및 텍스트 포맷팅
│   └── main.py                   # CLI 진입점 및 Click 앱
├── tests/unit/                   # 단위 테스트 모음
│   ├── commands/                 # 명령어 테스트
│   └── ml/                       # ML 파이프라인 및 모델 테스트
├── pyproject.toml               # 패키지 의존성 및 설정
└── README.md                    # 이 문서
```

### 새 기능 추가

1. **새 기술적 지표**: `src/cluefin_cli/commands/analysis/indicators.py` 또는 `src/cluefin_cli/ml/feature_engineering.py`에 추가
2. **차트 유형**: `src/cluefin_cli/display/charts.py` 확장
3. **데이터 소스**: `src/cluefin_cli/data/fetcher.py` 수정
4. **CLI 명령어**: `src/cluefin_cli/commands/`에 새 명령어 추가
5. **ML 모델**: `src/cluefin_cli/ml/models.py` 확장 또는 새 모델 클래스 추가
6. **SHAP 시각화**: `src/cluefin_cli/ml/explainer.py` 개선
7. **유틸리티 함수**: `src/cluefin_cli/utils/formatters.py`에 추가

### 테스트 실행

```bash
# 워크스페이스 루트 디렉토리에서
cd cluefin

# 모든 CLI 테스트 실행
uv run pytest apps/cluefin-cli/tests/ -v

# 단위 테스트만 실행 (통합 테스트 제외)
uv run pytest -m "not integration"

# 특정 테스트 모듈 실행
uv run pytest apps/cluefin-cli/tests/unit/ml/test_ml_pipeline.py -v

# 코드 품질 검사
uv run ruff check . --fix
uv run ruff format .

# 실제 예제로 ML 파이프라인 테스트
cluefin-cli ta 005930 --ml-predict --shap-analysis
```

### 🤖 ML 모델 아키텍처

ML 예측 시스템은 정교한 파이프라인을 사용합니다:

1. **피처 엔지니어링** (150+ 피처)
   - cluefin-ta 기술적 지표 (RSI, MACD, 볼린저 밴드 등)
   - 커스텀 가격 기반 피처 (비율, 변동성, 모멘텀)
   - 시간적 패턴을 위한 래그 피처
   - 거래량 기반 지표

2. **모델 학습**
   - **LightGBM 분류기**: 상승/하락 이진 예측
   - **시계열 분할**: 데이터 누수 방지
   - **조기 중단**: 과적합 방지
   - **교차 검증**: 적절한 시간 순서 유지

3. **모델 해석**
   - **SHAP TreeExplainer**: 피처 중요도
   - **개별 예측 설명**
   - **전역 피처 순위**
   - **방향성 영향 분석** (긍정/부정 기여도)

### ML 성능 가이드라인

- **정확도 > 60%**: 좋은 예측 성능
- **AUC > 0.7**: 상승/하락 움직임 간 우수한 구별력
- **F1-Score > 0.6**: 균형 잡힌 정밀도와 재현율
- **최소 30일**: 학습에 필요한 과거 데이터
- **권장 100일 이상**: 신뢰할 수 있는 모델 성능을 위해

**⚠️ 중요**: 주가 예측은 본질적으로 불확실합니다. ML 예측을 투자 결정 시 여러 요소 중 하나로 활용하세요.

## 기여하기

1. 저장소 포크
2. 피처 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 푸시 (`git push origin feature/amazing-feature`)
5. Pull Request 열기

## 라이선스

이 프로젝트는 MIT 라이선스에 따라 라이선스가 부여됩니다. 자세한 내용은 [LICENSE](../../LICENSE) 파일을 참조하세요.

## 지원

- **문서**: 메인 [Cluefin 문서](../../README.md) 확인
- **이슈**: [GitHub Issues](https://github.com/kgcrom/cluefin/issues)에서 버그 신고 또는 기능 요청
- **토론**: [GitHub Discussions](https://github.com/kgcrom/cluefin/discussions)에서 커뮤니티 토론 참여

## 관련 프로젝트

- **[cluefin-openapi](../../packages/cluefin-openapi/)** - 한국 금융 API 클라이언트
- **[cluefin-ta](../../packages/cluefin-ta/)** - 순수 Python 기술적 분석 라이브러리

---

**한국 금융 시장을 위해 정성을 담아 만들었습니다**

*"Clearly Looking U Entered Financial Information"*
