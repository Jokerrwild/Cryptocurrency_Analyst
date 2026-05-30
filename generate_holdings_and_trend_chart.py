import os
import json
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# State files
LEDGER_PATH = "/a0/usr/projects/cryptocurrency_analyst/ledger.json"
DB_PATH = "/a0/usr/projects/cryptocurrency_analyst/crypto_analyst/data/market_pulse.db"
OUTPUT_IMAGE = "/a0/usr/projects/cryptocurrency_analyst/reports/portfolio_status.png"

def main():
    # Set style for presentation-grade charts
    plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available else 'default')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Portfolio Allocation & Market Trend Analysis', fontsize=16, fontweight='bold', color='#1e293b', y=0.98)

    # 1. Parse Portfolio Holdings from ledger.json
    portfolio_value = 1000.00
    cash_usd = 1000.00
    holdings = {}
    
    if os.path.exists(LEDGER_PATH):
        with open(LEDGER_PATH, "r") as f:
            ledger = json.load(f)
            portfolio_value = ledger.get("portfolio_value_usd", 1000.0) 
            cash_usd = ledger.get("cash_usd", 1000.0)
            holdings = ledger.get("holdings", {})

    # Compile labels and sizes for the pie chart
    labels = ['Cash USD']
    sizes = [cash_usd]
    colors = ['#10b981']  # Green for Cash
    
    for asset, qty in holdings.items():
        # Just a placeholder for value since currently holdings are empty
        if qty > 0:
            labels.append(asset)
            # Mock asset value for rendering if it were to have holdings
            sizes.append(qty * 1.0) 
            colors.append('#3b82f6')
            
    # Plot Portfolio Allocation Pie Chart
    wedges, texts, autotexts = ax1.pie(
        sizes, 
        labels=labels, 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=colors, 
        textprops=dict(color='#1e293b', fontweight='bold'),
        wedgeprops=dict(width=0.4, edgecolor='w') # Donut shape
    )
    ax1.set_title(f'Portfolio Allocation (Total: ${portfolio_value:,.2f})', fontsize=12, fontweight='semibold', pad=15)

    # 2. Parse Market Trend from database
    timestamps = []
    btc_prices = []
    eth_prices = []
    
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp, btc_price, eth_price FROM snapshots ORDER BY timestamp ASC")
            rows = cursor.fetchall()
            conn.close()
            
            for row in rows:
                # Parse raw timestamp and keep time part
                dt_str = row[0].split('T')[-1].split('.')[0] if 'T' in row[0] else row[0]
                timestamps.append(dt_str)
                btc_prices.append(row[1])
                eth_prices.append(row[2])
        except Exception as e:
            print(f"Database read error: {e}")

    if len(btc_prices) > 1:
        # Dual axes plotting
        color = '#f59e0b' # Gold for BTC
        ax2.set_xlabel('Snapshot Time (Intervals)', fontweight='bold', color='#475569')
        ax2.set_ylabel('BTC Spot Price ($)', color=color, fontweight='bold')
        line1, = ax2.plot(timestamps, btc_prices, color=color, marker='o', linewidth=2, label='BTC-USD')
        ax2.tick_params(axis='y', labelcolor=color)
        
        # Twin axis for ETH
        ax2_twin = ax2.twinx()
        color_eth = '#6366f1' # Purple-blue for ETH
        ax2_twin.set_ylabel('ETH Spot Price ($)', color=color_eth, fontweight='bold')
        line2, = ax2_twin.plot(timestamps, eth_prices, color=color_eth, marker='s', linestyle='--', linewidth=2, label='ETH-USD')
        ax2_twin.tick_params(axis='y', labelcolor=color_eth)
        
        # Title and legends
        ax2.set_title('Recent Crypto Market Trend (BTC & ETH Spot Closes)', fontsize=12, fontweight='semibold', pad=15)
        ax2.legend([line1, line2], ['BTC-USD', 'ETH-USD'], loc='upper left')
        
        # Rotate x-axis labels slightly for clean layout
        plt.setp(ax2.get_xticklabels(), rotation=30, ha='right')
    else:
        # Fallback empty line if database was empty
        ax2.text(0.5, 0.5, 'No Trend Data Registered Yet', horizontalalignment='center', verticalalignment='center', fontsize=12, color='#64748b')
        ax2.set_title('Crypto Market Trend', fontsize=12, fontweight='semibold')

    plt.tight_layout()
    os.makedirs(os.path.dirname(OUTPUT_IMAGE), exist_ok=True)
    plt.savefig(OUTPUT_IMAGE, dpi=150, bbox_inches='tight')
    print(f"Successfully compiled and generated holdings graph: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
