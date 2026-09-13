# cluefin-desk

Interactive TUI dashboard for Korean stock market analysis, built with [Textual](https://textual.textualize.io/).

## Screens

Top-level screens switch with keys `1`–`5`; `stock detail` and `financial analysis` are
pushed from a row selection (`escape` goes back).

| Key | Screen | Content |
|-----|--------|---------|
| `1` | Market overview | KOSPI/KOSDAQ index summary, movers |
| `2` | Screening | Top gainers, trading volume, transaction value |
| `3` | Theme / sector | Theme groups and sector constituents (Kiwoom) |
| `4` | ETF analysis | ETF ranking and composition |
| `5` | Investor flow | Institution/foreign net-buy trends |
| — | Stock detail | Price chart, RSI/MACD/Bollinger, investor·broker·supply, opinions, news, ML prediction (LightGBM + SHAP) |
| — | Financial analysis | KIS financials, XBRL statements, DART disclosures, dividends, major shareholders, share changes |

`r` refreshes the current screen.

## Usage

```bash
# Run the TUI dashboard
cluefin-desk
```

## Requirements

Keys are read from a `.env` in the **current working directory** — launching from the repo
root uses the production `.env`.

- Kiwoom API keys (`KIWOOM_APP_KEY`, `KIWOOM_SECRET_KEY`) — required; authentication runs at startup
- KIS API keys (`KIS_APP_KEY`, `KIS_SECRET_KEY`) — optional; KIS-backed panels are skipped without them
- DART API key (`DART_AUTH_KEY`) — optional; disclosure/financial tabs need it

The app is read-only — it contains no order or account-mutation code.
