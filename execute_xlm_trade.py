import json
import os
from datetime import datetime, timezone

LEDGER_PATH = "/a0/usr/projects/cryptocurrency_analyst/ledger.json"

def main():
    if not os.path.exists(LEDGER_PATH):
        print("Ledger file not found!")
        return
    with open(LEDGER_PATH, 'r') as f:
        ledger = json.load(f)

    # Define trade parameters
    asset = "XLM"
    price = 0.19
    amount_usd = 250.00

    cash = ledger.get("cash_usd", 1000.0)
    holdings = ledger.get("holdings", {})
    current_holding = holdings.get(asset, 0.0)

    print("\n--- PRE-TRADE VERIFICATION ---")
    print(f"Action: BUY | Asset: {asset} | Price: ${price:.4f}")
    print(f"Starting Cash: ${cash:.2f} | Starting {asset} Balance: {current_holding:.6f} units")

    if cash < amount_usd:
        print("Insufficient cash for BUY order. Aborting.")
        return

    # Execute trade
    bought_units = amount_usd / price
    new_cash = cash - amount_usd
    new_holding = current_holding + bought_units
    holdings[asset] = new_holding

    # Update ledger fields
    ledger["cash_usd"] = new_cash
    ledger["holdings"] = holdings
    
    # Calculate total portfolio value dynamically using current spot prices
    # NEAR spot price: $2.29, XLM spot price: $0.19
    spot_prices = {
        "NEAR": 2.29,
        "XLM": 0.19
    }
    holdings_val = 0.0
    for ast, qty in holdings.items():
        spot = spot_prices.get(ast, 0.0)
        holdings_val += float(qty) * spot
        
    ledger["portfolio_value_usd"] = new_cash + holdings_val

    # Update performance metrics
    ledger["performance_metrics"]["roi_percent"] = ((ledger["portfolio_value_usd"] - 1000.0) / 1000.0) * 100.0

    # Add transaction to history
    new_tx = {
        "action": "BUY",
        "asset": asset,
        "total_usd": amount_usd,
        "quantity": bought_units,
        "price": price,
        "timestamp_utc": datetime.now(timezone.utc).isoformat()
    }
    if "transaction_history" not in ledger:
        ledger["transaction_history"] = []
    ledger["transaction_history"].append(new_tx)

    # Save ledger
    with open(LEDGER_PATH, 'w') as f:
        json.dump(ledger, f, indent=2)

    print("\n--- POST-TRADE SUMMARY ---")
    print(f"Final Cash: ${ledger['cash_usd']:.2f} | Final {asset}: {ledger['holdings'].get(asset, 0):.6f} units")
    print(f"Final Portfolio Value: ${ledger['portfolio_value_usd']:.2f}")
    print("Ledger updated successfully.\n")

if __name__ == "__main__":
    main()
