# cluefin-desk

Interactive TUI dashboard for Korean stock market analysis, built with [Textual](https://textual.textualize.io/).

## Features

- Stock screening: top gainers, trading volume, transaction value
- Market overview: KOSPI/KOSDAQ index summary
- Stock detail: price chart, technical indicators (RSI, MACD, Bollinger Bands)
- Company info: market cap, PER, PBR, ROE, EPS

## Usage

```bash
# Run the TUI dashboard
cluefin-desk
```

## Requirements

- Kiwoom API keys (`KIWOOM_APP_KEY`, `KIWOOM_SECRET_KEY`)
- KRX API key (`KRX_AUTH_KEY`) for market index data
