# ML 적용 계획서 (scikit-learn + LightGBM + SHAP)

## 전체 구현 계획

### 1. 프로젝트 종속성 추가
- [x] 1.1 pyproject.toml에 ML 라이브러리 추가
  - lightgbm
  - scikit-learn 
  - shap
  - ta (기술적 지표 라이브러리)

### 2. ML 모듈 구조 설계 및 디렉터리 생성
- [x] 2.1 `apps/cluefin-cli/src/cluefin_cli/ml/` 디렉터리 생성
- [x] 2.2 ML 모듈 파일들 생성:
  - `__init__.py`
  - `feature_engineering.py` (피처 엔지니어링)
  - `models.py` (ML 모델들) 
  - `explainer.py` (SHAP 해석)
  - `predictor.py` (예측 파이프라인)

### 3. 피처 엔지니어링을 위한 데이터 전처리기 클래스 생성
- [x] 3.1 `FeatureEngineer` 클래스 구현
  - 기존 기술적 지표 데이터를 ML 피처로 변환
  - `ta` 라이브러리를 사용한 추가 기술적 지표 생성
  - 타겟 변수 생성 (다음날 상승/하락 예측)
  - 데이터 정규화 및 결측치 처리

### 4. ML 모델 클래스 구현
- [x] 4.1 `StockPredictor` 클래스 구현
  - LightGBM 모델 설정 및 학습
  - Scikit-learn의 교차검증 활용
  - 모델 성능 평가 (정확도, precision, recall, F1-score)
  - 시계열 데이터 특성 고려한 train/test split

### 5. SHAP 기반 모델 해석 클래스 구현  
- [x] 5.1 `SHAPExplainer` 클래스 구현
  - TreeExplainer로 피처 중요도 분석
  - Summary plot 생성
  - Force plot 생성 (개별 예측 해석)
  - 결과를 Rich 테이블로 출력

### 6. 기존 analyze.py에 ML 기능 통합
- [x] 6.1 ML 관련 import 추가
- [x] 6.2 `_analyze_stock` 함수에 ML 예측 로직 추가
- [x] 6.3 기존 데이터 수집 로직과 ML 파이프라인 연결

### 7. ML 결과 표시를 위한 디스플레이 함수 추가
- [x] 7.1 `_display_ml_prediction` 함수 구현
  - 예측 결과 (상승/하락 확률)
  - 모델 성능 지표
- [x] 7.2 `_display_shap_analysis` 함수 구현  
  - 피처 중요도 테이블
  - 주요 영향 요인 설명

### 8. CLI 옵션 추가
- [x] 8.1 `--ml-predict` 옵션 추가
- [x] 8.2 `--shap-analysis` 옵션 추가
- [x] 8.3 기존 옵션들과 조합 가능하도록 구현

### 9. 테스트 및 검증
- [x] 9.1 샘플 데이터로 ML 파이프라인 테스트
- [ ] 9.2 실제 주식 데이터로 예측 성능 검증 (종속성 설치 후)
- [ ] 9.3 SHAP 분석 결과 검토 (종속성 설치 후)

## 주요 구현 포인트

### 데이터 처리
- 기존의 `stock_data`와 `indicators`를 ML 피처로 변환
- 시계열 특성을 고려한 데이터 분할 (앞 80% 학습, 뒤 20% 테스트)
- 결측치 처리 및 피처 정규화

### 모델 설계
- **타겟**: 다음날 종가가 오늘 종가보다 상승할지 예측 (이진 분류)
- **피처**: 기존 기술적 지표 + ta 라이브러리 추가 지표
- **모델**: LightGBM (트리 기반, 빠른 학습, 피처 중요도 제공)

### SHAP 활용
- **TreeExplainer**: LightGBM 모델에 최적화된 explainer
- **Summary Plot**: 전체적인 피처 중요도 시각화
- **Force Plot**: 개별 예측에 대한 상세 분석
- CLI 환경에서의 결과 표시를 위해 matplotlib 대신 텍스트 기반 출력

### 기존 코드와의 통합
- 기존의 데이터 수집 및 기술적 지표 계산 로직 재활용
- Rich 라이브러리를 활용한 일관된 출력 스타일 유지
- 비동기 함수 구조 유지

## 예상 CLI 사용법

```bash
# 기본 분석 + ML 예측
cluefin-cli analyze 005930 --ml-predict

# ML 예측 + SHAP 분석
cluefin-cli analyze 005930 --ml-predict --shap-analysis

# 전체 기능 활용
cluefin-cli analyze 005930 --chart --ai-analysis --ml-predict --shap-analysis
```