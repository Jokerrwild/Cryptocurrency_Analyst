import json
from crypto_analyst.sources import fetch_market_snapshot

cfg = {
    "crypto_assets": [{"label": "BTC", "product_id": "BTC-USD"}, {"label": "ETH", "product_id": "ETH-USD"}],
    "macro_assets": [{"symbol": "^TNX", "range": "3mo"}, {"symbol": "DX-Y.NYB", "range": "3mo"}]
}

snapshot = fetch_market_snapshot(cfg)
print(f"Collected data for {len(snapshot.crypto)} crypto assets and {len(snapshot.macro)} macro assets.")
# Print a summary of the first crypto asset to verify data
if snapshot.crypto:
    print(f"Sample: {snapshot.crypto[0].label} - {len(snapshot.crypto[0].closes)} data points")
