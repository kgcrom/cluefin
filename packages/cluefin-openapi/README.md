# cluefin-openapi

> **cluefin-openapi**: A Python client for Kiwoom Securities investment REST API.

---

## Features
- Account information retrieval
- Domestic/foreign stock info
- Chart data and analytics
- ETF, sector, theme, and market condition support
- Order management and real-time updates

## Quickstart
```bash
$> pip install cluefin-openapi
or
$> pip install cluefin-openapi[kiwoom]
```

```python
from cluefin_openapi.kiwoom._auth import Auth
from cluefin_openapi.kiwoom._client import Client

auth = Auth(
    app_key=os.getenv("APP_KEY"),
    secret_key=os.getenv("SECRET_KEY"),
    env="dev",
)

token = auth.generate_token()
client = Client(token=token.token, env="dev")

response = client.account.get_daily_stock_realized_profit_loss_by_date("005930", "20250630")
print(response.headers)
print(response.body)
```

## Why cluefin-openapi?
Easily access investment data and trading features from Kiwoom Securities, DART, KRX, and more—all through a unified Python interface.
Save time integrating with multiple financial APIs and focus on building your investment tools.

## Getting Started
1. Install via pip
2. Obtain your Kiwoom REST API credentials
3. See [examples](./test/integration/kiwoom/) for more usage

## Contributing
See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

*Invest responsibly. This project is not affiliated with Kiwoom Securities.*
