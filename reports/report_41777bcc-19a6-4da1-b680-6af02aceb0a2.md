### **System Analysis Report**
*   **Report ID**: `41777bcc-19a6-4da1-b680-6af02aceb0a2`
*   **Generated Timestamp (UTC)**: 2026-06-01T01:00:42.766258+00:00Z
*   **Interval Label**: 3-Hourly Scheduled Pulse
*   **BTC Spot Price**: $73,786.89 USD
*   **ETH Spot Price**: $2,012.27 USD
*   **BNB Spot Price**: $710.46 USD
*   **SOL Spot Price**: $82.71 USD
*   **HYPE Spot Price**: $73.35 USD
*   **XRP Spot Price**: $1.34 USD
*   **XLM Spot Price**: $0.26 USD
*   **USD1 Spot Price**: $1.00 USD
*   **NEAR Spot Price**: $2.32 USD
*   **ZEC Spot Price**: $593.94 USD

### **Executive Summary**
*   **Date/Time (US EDT) of the analysis**: 2026-05-31 09:00:42 PM EDT
*   **Portfolio Current Value**: $1,093.76 USD
*   **The Last Trade**: [2026-05-31T19:42:24+00:00] BUY 0.458362 ZEC @ $545.42 USD (Total: $250.00 USD)
*   **Recommendation (HOLD / BUY / SELL) currency**: <b>RULE-BASED HOLD (Conviction below threshold)</b>
    *   *Key Macro Indicators*: SPY=$756.48, QQQ=$738.31, DXY=99.05, US10Y=4.45%
    *   *Market Trend Probability*: Bullish accumulation (29.0% probability)


### **Market Thesis**
Leading regime is classified as *Bullish accumulation* with a posterior probability weight of *29.0%*.

### **Probability Table**
```text
Market Regime                  | Probability | Confidence
----------------------------------------------------------
Bullish accumulation           | 29.0%       | Low       
Neutral consolidation          | 27.2%       | Low       
Bullish continuation           | 11.2%       | Low       
High-volatility transition     | 9.4%        | Low       
Macro-driven risk-off          | 9.2%        | Low       
Bearish continuation           | 7.4%        | Low       
Bearish distribution           | 6.6%        | Low       
```

### **Quantitative Evidence**
* BTC latest close: $73,786.89
* Trend score: +0.008 (positive = above EMA-50)
* Momentum score: -0.003 (EMA-12 vs EMA-26 spread)
* Volatility score: 0.019 (0=calm, 1=extreme)
* Volume score: 0.558 (0.5=avg, 1.0=2x avg)
* Macro support: +0.048 (equity trend minus DXY drag)
*   Momentum [HYPE]: +0.169
*   Momentum [ZEC]: +0.161
*   Momentum [XLM]: +0.159
*   Momentum [BNB]: +0.011
*   Momentum [USD1]: +0.001
*   Momentum [BTC]: -0.003
*   Momentum [SOL]: -0.005
*   Momentum [XRP]: -0.013
*   Momentum [NEAR]: -0.014
*   Momentum [ETH]: -0.019
* BTC Indicators: RSI=49.9, EMA20=$73,694.03, EMA50=$73,725.54, 24h=+0.29%, 5d=+0.20%, VolConf=0.56
* ETH Indicators: RSI=46.2, EMA20=$2,010.75, EMA50=$2,014.99, 24h=+0.41%, 5d=+0.40%, VolConf=0.86
* BNB Indicators: RSI=38.4, EMA20=$713.30, EMA50=$700.93, 24h=+0.12%, 5d=+0.13%, VolConf=0.64
* SOL Indicators: RSI=50.9, EMA20=$82.30, EMA50=$82.37, 24h=+0.01%, 5d=+0.63%, VolConf=0.01
* HYPE Indicators: RSI=79.5, EMA20=$69.82, EMA50=$67.96, 24h=+1.83%, 5d=+4.62%, VolConf=0.96
* XRP Indicators: RSI=50.5, EMA20=$1.33, EMA50=$1.33, 24h=+0.33%, 5d=+0.51%, VolConf=0.95
* XLM Indicators: RSI=59.3, EMA20=$0.25, EMA50=$0.24, 24h=-0.26%, 5d=+3.58%, VolConf=0.57
* USD1 Indicators: RSI=71.4, EMA20=$1.00, EMA50=$1.00, 24h=+0.02%, 5d=+0.02%, VolConf=0.48
* NEAR Indicators: RSI=57.9, EMA20=$2.30, EMA50=$2.33, 24h=+0.09%, 5d=+2.97%, VolConf=0.59
* ZEC Indicators: RSI=73.4, EMA20=$554.35, EMA50=$545.90, 24h=+4.47%, 5d=+8.07%, VolConf=1.00

### **Qualitative Evidence**
* Coinbase makes a major play for India’s booming $3 billion crypto market with local currency launch
* US, UK central bankers offer contrary views on stablecoins
* Aggregate News Sentiment Score: +0.00 (Weights: Clear/Threat ±0.18, Easing/Tightening ±0.15)
* Regulatory Sentiment Bias: +0.10

### **Interpretation**
Leading regime is 'Bullish accumulation' with posterior probability 29.0% (confidence: Low). Trend signal is positive (+0.01) and momentum is waning (-0.00). Treat this as a probabilistic belief state, not a deterministic prediction.

### **Invalidation Conditions**
* Trend flips negative (close drops below EMA-50)
* Momentum turns sharply negative over 2+ intervals
* Volume collapses below 50% of 20-period average

### **Risk-Aware Decision Support**
**Global Thesis Action Strategy**: Guided by Bayesian Regime *Bullish accumulation*.

**Top 5 Currencies Priority List**:
```text
Rank | Asset  | Spot Price   | Momentum   | Rec Allocation 
----------------------------------------------------------
1    | HYPE   | $73.35       | +0.169     | 0.0% (HOLD)    
2    | ZEC    | $593.94      | +0.161     | 0.0% (HOLD)    
3    | XLM    | $0.26        | +0.159     | 0.0% (HOLD)    
4    | BNB    | $710.46      | +0.011     | 0.0% (HOLD)    
5    | USD1   | $1.00        | +0.001     | 0.0% (HOLD)    
```

All suggestions are trade recommendations awaiting strict Human-in-the-Loop (HITL) manual confirmation.

### **What To Monitor Next**
* BTC close relative to EMA-50
* DXY trend continuation or reversal
* SPY/QQQ session volume
* Regulatory headlines for tracked assets
* Regime velocity (probability shift >5% vs last interval)

### **Learning Notes**
Model weights adaptively learned using historical priors. Minimum conviction threshold enforced at 55%. If leading probability falls below conviction threshold, recommended allocation defaults to HOLD state across all assets.