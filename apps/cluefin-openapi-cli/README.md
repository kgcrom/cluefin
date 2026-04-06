# cluefin-openapi-cli

Agent-friendly CLI surface for `cluefin-openapi`.

This app exposes the current broker RPC surface as a broker-first CLI:

- `list` for registry discovery
- `describe` for command metadata
- `kis`, `kiwoom`, `dart` command trees
- `--params-json` plus schema-derived CLI options
- JSON and TTY-aware output plumbing

Examples:

```bash
cluefin-openapi-cli list --json
cluefin-openapi-cli describe kis stock current-price --json
cluefin-openapi-cli kis stock current-price --stock-code 005930 --json
cluefin-openapi-cli dart company-overview --corp-code 00126380 --json
```

The CLI consumes the shared registry from `cluefin-rpc` and creates broker
clients through `cluefin_openapi.client_factory`, so command metadata and
executor behavior stay aligned with the existing RPC handlers.
