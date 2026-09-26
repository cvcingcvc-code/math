# Binance public market-data forward/shadow validation

This isolated directory records a research-only forward validation for the frozen historical transfer model.

- Endpoint: `https://data-api.binance.vision/api/v3/klines` (public GET only)
- Symbol: `BTCUSDT`
- No API key, secret, account, balance, order, margin, futures, transfer, or withdrawal interface
- Safety gate: `LIVE_ORDERING_ENABLED` must be explicitly set to exactly `false`
- Frozen parameters: 7-day momentum; reliability weights 0.30/0.30/0.20/0.20; abstain threshold 0.65
- Future returns are backfilled only after the target time; current features are not recomputed from future outcomes.

Run from the project root:

```powershell
$env:LIVE_ORDERING_ENABLED = 'false'
python experiments/transfer_finance/live_shadow/run_live_shadow.py
```

Outputs are `live_shadow_log.csv`, `live_shadow_state.json`, and `live_shadow_summary.json`.
