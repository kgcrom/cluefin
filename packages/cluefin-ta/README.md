# cluefin-ta

TA-Lib 호환 API를 제공하는 순수 Python 기술적 분석 라이브러리입니다.

![Python](https://img.shields.io/badge/Python-3.10%2B-green)
![NumPy](https://img.shields.io/badge/NumPy-Pure%20Python-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 특징

- **간편한 설치**: `pip install`만으로 설치 가능 (brew/apt 시스템 의존성 불필요)
- **TA-Lib 호환 API**: 기존 TA-Lib 코드를 최소한의 변경으로 마이그레이션
- **선택적 Numba 가속**: Numba 설치 시 평균 ~238배 성능 향상
- **포트폴리오 메트릭**: TA-Lib에 없는 MDD, Sharpe, Sortino 등 추가 제공
- **시장 레짐 감지**: 이동평균, 변동성, HMM 기반 시장 상태 분류

## 설치

```bash
# 기본 설치 (NumPy만 의존)
pip install cluefin-ta

# Numba 가속 포함 설치 (선택)
pip install cluefin-ta[numba]
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
from cluefin_ta import MDD, CAGR, SHARPE, SORTINO, CALMAR, VOLATILITY

returns = np.array([...])  # 일별 수익률

mdd = MDD(returns)                          # 최대 낙폭
cagr = CAGR(returns, periods_per_year=252)  # 연평균수익률
sharpe = SHARPE(returns, risk_free=0)       # 샤프비율
sortino = SORTINO(returns, risk_free=0)     # 소르티노비율
calmar = CALMAR(returns)                    # 칼마비율
vol = VOLATILITY(returns)                   # 연환산변동성
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
# states: 0=약세, 1=중립, 2=강세
```

## 지원 함수

총 **39개** 기술 분석 함수 지원

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

### Candlestick Patterns (캔들패턴) - 10개

| 함수 | 설명 | 신호 |
|------|------|--------|
| `CDLDOJI` | 도지 | +100 |
| `CDLHAMMER` | 해머 | +100 |
| `CDLENGULFING` | 장악형 | +100/-100 |
| `CDLSHOOTINGSTAR` | 유성형 | -100 |
| `CDLHANGINGMAN` | 교수형 | -100 |
| `CDLHARAMI` | 하라미 | +100/-100 |
| `CDLPIERCING` | 관통형 | +100 |
| `CDLMORNINGSTAR` | 샛별 (3봉) | +100 |
| `CDLEVENINGSTAR` | 저녁별 (3봉) | -100 |
| `CDLDARKCLOUDCOVER` | 먹구름 | -100 |

### Portfolio Metrics (포트폴리오) - 6개

| 함수 | 설명 |
|------|------|
| `MDD(returns)` | 최대 낙폭 |
| `CAGR(returns, periods_per_year=252)` | 연평균수익률 |
| `SHARPE(returns, risk_free=0, periods_per_year=252)` | 샤프비율 |
| `SORTINO(returns, risk_free=0, periods_per_year=252)` | 소르티노비율 |
| `CALMAR(returns, periods_per_year=252)` | 칼마비율 |
| `VOLATILITY(returns, periods_per_year=252)` | 연환산변동성 |

### Regime Detection (시장 레짐 감지) - 6개

| 함수 | 설명 |
|------|------|
| `REGIME_MA(close, fast_period=20, slow_period=50, sideways_threshold=0.02)` | 이동평균 기반 레짐 감지 (0=하락, 1=횡보, 2=상승) |
| `REGIME_MA_DURATION(regime_states)` | 현재 레짐 지속 기간 계산 |
| `REGIME_VOLATILITY(high, low, close, atr_period=14, threshold_percentile=66)` | 변동성 기반 레짐 감지 (0=저변동성, 1=고변동성) |
| `REGIME_COMBINED(high, low, close, ...)` | 추세+변동성 결합 레짐 (0-5: 6가지 시장 상태) |
| `REGIME_HMM_RETURNS(close)` | HMM 레짐 감지용 수익률 계산 |
| `REGIME_HMM(returns, n_states=3, ...)` | 은닉 마르코프 모델 기반 레짐 감지 |

## 성능

Numba 설치 시 루프 기반 함수가 JIT 컴파일되어 성능 향상:

| 함수 | NumPy (ms) | Numba (ms) | 성능 향상 |
|------|-----------|-----------|----------|
| EMA Loop | 1.506 | 0.015 | 101x |
| Rolling Std | 44.574 | 0.144 | 310x |
| Rolling MinMax | 20.467 | 0.061 | 333x |
| True Range | 3.635 | 0.012 | 310x |
| OBV | 2.187 | 0.009 | 254x |
| A/D | 4.067 | 0.034 | 120x |

*n=10,000 데이터 기준, 평균 238배 성능 향상*

## 요구사항

- **필수**: `numpy>=1.20.0`
- **선택**: `numba>=0.56.0` (성능 향상)
- **선택**: `hmmlearn` (HMM 레짐 감지용, `uv add --optional hmm hmmlearn`)
