from crypto_analyst.sources import fetch_market_snapshot
from crypto_analyst.indicators import trend_score, momentum_score

cfg = {
    "crypto_assets": [{"label": "BTC", "product_id": "BTC-USD"}, {"label": "ETH", "product_id": "ETH-USD"}],
    "macro_assets": [{"symbol": "^TNX", "range": "3mo"}, {"symbol": "DX-Y.NYB", "range": "3mo"}]
}

snapshot = fetch_market_snapshot(cfg)

print("--- Market Analysis Report ---")
for asset in snapshot.crypto:
    t_score = trend_score(asset)
    m_score = momentum_score(asset)
    print(f"Asset: {asset.label} | Trend: {t_score:.2f} | Momentum: {m_score:.2f}")

for macro in snapshot.macro:
    t_score = trend_score(macro)
    print(f"Macro: {macro.label} | Trend: {t_score:.2f}")
