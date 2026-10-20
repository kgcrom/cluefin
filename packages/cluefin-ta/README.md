# cluefin-ta

TA-Lib 호환 API를 제공하는 순수 Python 기술적 분석 라이브러리입니다.

![Python](https://img.shields.io/badge/Python-3.10%2B-green)
![NumPy](https://img.shields.io/badge/NumPy-Pure%20Python-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 특징

- **간편한 설치**: NumPy만 의존 (C TA-Lib 같은 brew/apt 시스템 의존성 불필요)
- **TA-Lib 호환 API**: 기존 TA-Lib 코드를 최소한의 변경으로 마이그레이션
- **포트폴리오 메트릭**: TA-Lib에 없는 MDD, Sharpe, Sortino 등 추가 제공
- **시장 레짐 감지**: 이동평균, 변동성, HMM 기반 시장 상태 분류

## 설치

PyPI에 배포하지 않는 uv 워크스페이스 멤버로, 저장소 루트에서 설치합니다.

```bash
uv sync --all-packages
```

## 사용법

### 기본 사용

```python
import numpy as np
from cluefin_ta import SMA, EMA, RSI, MACD, BBANDS

close = np.array([...])  # 종가 데이터

# 이동평균
sma = SMA(close, timeperiod=20)
ema = EMA(close, timeperiod=20)

# RSI
rsi = RSI(close, timeperiod=14)

# MACD
macd, signal, hist = MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)

# 볼린저 밴드
upper, middle, lower = BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)
```

### ta-lib 대체 사용

```python
# Before (ta-lib)
import talib
sma = talib.SMA(close, timeperiod=20)

# After (cluefin-ta) - import만 변경
import cluefin_ta as talib
sma = talib.SMA(close, timeperiod=20)
```

### 포트폴리오 메트릭

```python
from cluefin_ta import MDD, CAGR, SHARPE, SORTINO, CALMAR, VOLATILITY, BETA, ALPHA

returns = np.array([...])  # 일별 수익률

mdd = MDD(returns)                          # 최대 낙폭
cagr = CAGR(returns, periods_per_year=252)  # 연평균수익률
sharpe = SHARPE(returns, risk_free=0)       # 샤프비율
sortino = SORTINO(returns, risk_free=0)     # 소르티노비율
calmar = CALMAR(returns)                    # 칼마비율
vol = VOLATILITY(returns)                   # 연환산변동성
beta = BETA(returns, kospi_returns)         # 베타 (같은 날짜로 정렬한 벤치마크 수익률)
alpha = ALPHA(returns, kospi_returns)       # 젠센 알파 (연율)
```

### 시장 레짐 감지

```python
from cluefin_ta import REGIME_MA, REGIME_COMBINED, REGIME_HMM, REGIME_HMM_RETURNS

# 이동평균 기반 레짐 감지
regime = REGIME_MA(close, fast_period=20, slow_period=50)
# 0=하락장, 1=횡보장, 2=상승장

# 추세+변동성 결합 레짐
trend, vol, combined = REGIME_COMBINED(high, low, close)
# combined: 0-5 (6가지 시장 상태)

# HMM 기반 레짐 감지 (선택적 의존성 필요)
returns = REGIME_HMM_RETURNS(close)
states, trans_probs, means = REGIME_HMM(returns, n_states=3)
# states: 0=약세, 1=중립, 2=강세 (봉마다 하나)
# trans_probs: (n, 3, 3), means: (n, 3) — 봉마다 그 시점의 모델 값
```

레짐 함수는 모든 봉을 **그 봉까지의 데이터만으로** 판정합니다. 변동성 기준선은 그 시점까지의
NATR 퍼센타일이고, HMM은 그 시점까지의 수익률로 학습(`refit_every`마다 재학습)한 모델의
필터링 확률을 씁니다. 그래서 ML 피처나 백테스트에 그대로 넣어도 미래 정보가 섞이지 않습니다.

## 예제 노트북

`examples/` 에 실제 시세로 지표·차트·해석·ML 피처 흐름을 따라가는 Jupyter 노트북이 있습니다.

```bash
# 워크스페이스 루트에서 실행 — .env.test 의 KIS 자격증명을 사용합니다
uv run --with jupyter jupyter lab packages/cluefin-ta/examples/ta_quickstart.ipynb
```

## 지원 함수

총 **40개** 기술 분석 함수 지원

### Overlap Studies (이동평균) - 7개

| 함수 | 설명 |
|------|------|
| `SMA(close, timeperiod=30)` | 단순이동평균 |
| `EMA(close, timeperiod=30)` | 지수이동평균 |
| `WMA(close, timeperiod=30)` | 가중이동평균 |
| `DEMA(close, timeperiod=30)` | 이중지수이동평균 |
| `TEMA(close, timeperiod=30)` | 삼중지수이동평균 |
| `KAMA(close, timeperiod=30)` | 카우프만 적응 이동평균 |
| `BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2)` | 볼린저 밴드 |

### Momentum Indicators (모멘텀지표) - 10개

| 함수 | 설명 |
|------|------|
| `RSI(close, timeperiod=14)` | 상대강도지수 |
| `MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)` | MACD |
| `STOCH(high, low, close, ...)` | 스토캐스틱 |
| `STOCHF(high, low, close, ...)` | 빠른 스토캐스틱 |
| `WILLR(high, low, close, timeperiod=14)` | 윌리엄스 %R |
| `MOM(close, timeperiod=10)` | 모멘텀 |
| `ROC(close, timeperiod=10)` | 변화율 |
| `CCI(high, low, close, timeperiod=14)` | 상품채널지수 |
| `MFI(high, low, close, volume, timeperiod=14)` | 자금흐름지수 |
| `ADX(high, low, close, timeperiod=14)` | 평균방향지수 |

### Volatility Indicators (변동성) - 3개

| 함수 | 설명 |
|------|------|
| `TRANGE(high, low, close)` | 실제범위 |
| `ATR(high, low, close, timeperiod=14)` | 평균실제범위 |
| `NATR(high, low, close, timeperiod=14)` | 정규화 ATR |

### Volume Indicators (거래량) - 3개

| 함수 | 설명 |
|------|------|
| `OBV(close, volume)` | 거래량잔고 |
| `AD(high, low, close, volume)` | 축적/분산 |
| `ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)` | A/D 오실레이터 |

### Candlestick Patterns (캔들패턴) - 3개

TA-Lib C 소스와 같은 알고리즘(직전 봉들의 평균 몸통·고저폭 기준)이라 결과가 정확히 같습니다.

| 함수 | 설명 | 신호 |
|------|------|--------|
| `CDLDOJI` | 도지 | +100 |
| `CDLHAMMER` | 해머 | +100 |
| `CDLENGULFING` | 장악형 | ±100 (한쪽 끝이 겹치면 ±80) |

### Portfolio Metrics (포트폴리오) - 8개

| 함수 | 설명 |
|------|------|
| `MDD(returns)` | 최대 낙폭 |
| `CAGR(returns, periods_per_year=252)` | 연평균수익률 |
| `SHARPE(returns, risk_free=0, periods_per_year=252)` | 샤프비율 |
| `SORTINO(returns, risk_free=0, periods_per_year=252)` | 소르티노비율 |
| `CALMAR(returns, periods_per_year=252)` | 칼마비율 |
| `VOLATILITY(returns, periods_per_year=252)` | 연환산변동성 |
| `BETA(returns, benchmark_returns)` | 베타 (공분산/분산, 날짜 정렬된 같은 길이 배열) |
| `ALPHA(returns, benchmark_returns, risk_free=0, periods_per_year=252)` | 젠센 알파 (연율) |

### Regime Detection (시장 레짐 감지) - 6개

| 함수 | 설명 |
|------|------|
| `REGIME_MA(close, fast_period=20, slow_period=50, sideways_threshold=0.02)` | 이동평균 기반 레짐 감지 (0=하락, 1=횡보, 2=상승) |
| `REGIME_MA_DURATION(regime_states)` | 현재 레짐 지속 기간 계산 |
| `REGIME_VOLATILITY(high, low, close, atr_period=14, threshold_percentile=66, min_periods=1)` | 변동성 기반 레짐 감지 (0=저변동성, 1=고변동성, 기준선은 그 시점까지의 퍼센타일) |
| `REGIME_COMBINED(high, low, close, ...)` | 추세+변동성 결합 레짐 (0-5: 6가지 시장 상태) |
| `REGIME_HMM_RETURNS(close)` | HMM 레짐 감지용 수익률 계산 |
| `REGIME_HMM(returns, n_states=3, ..., min_periods=60, refit_every=20)` | 은닉 마르코프 모델 기반 레짐 감지 (확장 창 재학습 + 필터링) |

## 요구사항

- **필수**: `numpy>=1.20.0`
- **선택**: `hmmlearn` (HMM 레짐 감지용, `hmm` extra. 워크스페이스에서는 dev 그룹으로 함께 설치됨)
