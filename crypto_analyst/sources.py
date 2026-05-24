import urllib.request
import json
import logging
from datetime import datetime
from typing import Dict, Any, List

from .models import MarketSnapshot, SeriesSummary

logger = logging.getLogger("crypto_analyst.sources")

def fetch_coinbase_candles(product_id: str, granularity: int = 3600, limit: int = 24) -> SeriesSummary:
    """Fetches recent candle data from Coinbase Public REST API using urllib."""
    logger.info(f"Fetching Coinbase candles for {product_id} (granularity: {granularity}s)")
    url = f"https://api.exchange.coinbase.com/products/{product_id}/candles?granularity={granularity}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'CryptoAnalystSources/1.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            # Coinbase returns: [[time, low, high, open, close, volume], ...]
            # Sort ascending by timestamp
            sorted_data = sorted(data, key=lambda x: x[0])
            
            # Truncate to limit
            if len(sorted_data) > limit:
                sorted_data = sorted_data[-limit:]
                
            timestamps = [int(item[0]) for item in sorted_data]
            closes = [float(item[4]) for item in sorted_data]
            volumes = [float(item[5]) for item in sorted_data]
            
            label = product_id.split('-')[0]
            return SeriesSummary(label=label, closes=closes, volumes=volumes, timestamps=timestamps)
    except Exception as e:
        logger.warning(f"Failed to fetch Coinbase data for {product_id}: {e}")
        # Fallback empty summary to prevent complete pipeline crash
        return SeriesSummary(label=product_id.split('-')[0])

def fetch_yahoo_finance_candles(symbol: str, range_val: str = "3mo", interval_val: str = "1d") -> SeriesSummary:
    """Fetches recent price history from Yahoo Finance Public Query API using urllib."""
    logger.info(f"Fetching Yahoo Finance data for {symbol} (range: {range_val}, interval: {interval_val})")
    # Encode symbol to safely handle characters like ^ in ^TNX
    safe_symbol = urllib.parse.quote(symbol)
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{safe_symbol}?range={range_val}&interval={interval_val}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            result = data["chart"]["result"][0]
            timestamps = result["timestamp"]
            closes = result["indicators"]["quote"][0]["close"]
            volumes = result["indicators"]["quote"][0].get("volume", [0] * len(timestamps))
            
            # Filter out null values
            clean_timestamps = []
            clean_closes = []
            clean_volumes = []
            for t, c, v in zip(timestamps, closes, volumes):
                if c is not None and t is not None:
                    clean_timestamps.append(int(t))
                    clean_closes.append(float(c))
                    clean_volumes.append(float(v or 0))
                    
            label = "10Y" if symbol == "^TNX" else ("DXY" if symbol == "DX-Y.NYB" else symbol)
            return SeriesSummary(label=label, closes=clean_closes, volumes=clean_volumes, timestamps=clean_timestamps)
    except Exception as e:
        logger.warning(f"Failed to fetch Yahoo Finance data for {symbol}: {e}")
        # Fallback empty summary
        label = "10Y" if symbol == "^TNX" else ("DXY" if symbol == "DX-Y.NYB" else symbol)
        return SeriesSummary(label=label)

def fetch_market_snapshot(cfg: Dict[str, Any]) -> MarketSnapshot:
    """Compiles all configured crypto and macro data streams into a single UTC MarketSnapshot."""
    logger.info("Starting market snapshot data collection.")
    utc_now = datetime.utcnow().isoformat() + "Z"
    
    crypto_series = []
    for asset in cfg.get("crypto_assets", []):
        product_id = asset.get("product_id", f"{asset['label']}-USD")
        granularity = asset.get("granularity_seconds", 3600)
        crypto_series.append(fetch_coinbase_candles(product_id, granularity=granularity))
        
    macro_series = []
    for asset in cfg.get("macro_assets", []):
        symbol = asset.get("symbol")
        range_val = asset.get("range", "3mo")
        interval_val = asset.get("interval", "1d")
        macro_series.append(fetch_yahoo_finance_candles(symbol, range_val=range_val, interval_val=interval_val))
        
    return MarketSnapshot(
        crypto=crypto_series,
        macro=macro_series,
        timestamp_utc=utc_now
    )
