import json
import os
import subprocess
from datetime import datetime, timezone

LEDGER_PATH = "/a0/usr/projects/cryptocurrency_analyst/ledger.json"

def backup_ledger():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{LEDGER_PATH}.{timestamp}.bak"
    with open(LEDGER_PATH, 'r') as f:
        data = f.read()
    with open(backup_path, 'w') as f:
        f.write(data)
    print(f"Backup created: {backup_path}")

def execute_trade(asset, amount_usd, price):
    backup_ledger()
    
    with open(LEDGER_PATH, 'r') as f:
        ledger = json.load(f)
    
    cash = ledger.get("cash_usd", 0.0)
    if cash < amount_usd:
        print("Insufficient cash.")
        return False

    bought_units = amount_usd / price
    ledger["cash_usd"] -= amount_usd
    ledger["holdings"][asset] = ledger["holdings"].get(asset, 0.0) + bought_units
    
    new_tx = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "action": "BUY",
        "asset": asset,
        "quantity": bought_units,
        "price": price,
        "total_usd": amount_usd
    }
    ledger["transaction_history"].append(new_tx)
    
    with open(LEDGER_PATH, 'w') as f:
        json.dump(ledger, f, indent=2)
    
    # Git commit and push
    subprocess.run(["git", "add", "ledger.json"], cwd="/a0/usr/projects/cryptocurrency_analyst")
    subprocess.run(["git", "commit", "-m", f"trade: execute BUY of {bought_units} {asset} @ ${price}"], cwd="/a0/usr/projects/cryptocurrency_analyst")
    subprocess.run(["git", "push"], cwd="/a0/usr/projects/cryptocurrency_analyst")
    
    print(f"Trade executed and pushed: {asset}")
    return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--asset", required=True)
    parser.add_argument("--amount", type=float, required=True)
    parser.add_argument("--price", type=float, required=True)
    args = parser.parse_args()
    execute_trade(args.asset, args.amount, args.price)