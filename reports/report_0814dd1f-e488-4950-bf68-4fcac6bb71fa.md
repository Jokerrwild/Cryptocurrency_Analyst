### **System Analysis Report**
*   **Report ID**: `0814dd1f-e488-4950-bf68-4fcac6bb71fa`
*   **Generated Timestamp (UTC)**: 2026-05-27T00:38:12.135900+00:00Z
*   **Interval Label**: 3-Hourly Scheduled Pulse
*   **BTC Spot Price**: $75,855.60 USD
*   **ETH Spot Price**: $2,076.60 USD
*   **SOL Spot Price**: $83.93 USD
*   **XRP Spot Price**: $1.33 USD
*   **USD1 Spot Price**: $1.00 USD
*   **NEAR Spot Price**: $2.59 USD
*   **HYPE Spot Price**: $60.29 USD
*   **BNB Spot Price**: $656.80 USD
*   **ZEC Spot Price**: $577.50 USD
*   **DOGE Spot Price**: $0.10 USD

### **Executive Summary**
*   **Date/Time (US EDT) of the analysis**: 2026-05-26 08:38:12 PM EDT
*   **Portfolio Current Value**: $987.09 USD ($750.00 Cash / $237.09 Holdings)
*   **The Last Trade**: [2026-05-26T16:38:55.139395+00:00] BUY 91.575092 NEAR @ $2.73 USD (Total: $250.00 USD)
*   **Recommendation (HOLD / BUY / SELL) currency**: <b>RULE-BASED HOLD (Conviction below threshold)</b>
    *   *Key Macro Indicators*: SPY=$750.59, QQQ=$730.28, DXY=99.08, US10Y=4.49%
    *   *Market Trend Probability*: Neutral consolidation (30.5% probability)


### **Market Thesis**
Leading regime is classified as *Neutral consolidation* with a posterior probability weight of *30.5%*.

### **Probability Table**
```text
Market Regime                  | Probability | Confidence
----------------------------------------------------------
Neutral consolidation          | 30.5%       | Medium    
Bullish accumulation           | 15.1%       | Low       
Bullish continuation           | 12.6%       | Low       
High-volatility transition     | 12.3%       | Low       
Macro-driven risk-off          | 11.8%       | Low       
Bearish continuation           | 9.1%        | Low       
Bearish distribution           | 8.7%        | Low       
```

### **Quantitative Evidence**
* BTC latest close: $75,855.60
* Trend score: -0.097 (positive = above EMA-50)
* Momentum score: -0.042 (EMA-12 vs EMA-26 spread)
* Volatility score: 0.036 (0=calm, 1=extreme)
* Volume score: 0.071 (0.5=avg, 1.0=2x avg)
* Macro support: +0.251 (equity trend minus DXY drag)
*   Momentum [USD1]: -0.001
*   Momentum [BNB]: -0.017
*   Momentum [DOGE]: -0.026
*   Momentum [XRP]: -0.042
*   Momentum [BTC]: -0.042
*   Momentum [SOL]: -0.044
*   Momentum [ETH]: -0.046
*   Momentum [HYPE]: -0.060
*   Momentum [NEAR]: -0.079
*   Momentum [ZEC]: -0.281
* BTC Indicators: RSI=23.6, EMA20=$76,285.45, EMA50=$76,595.08, 24h=+0.04%, 5d=-0.19%, VolConf=0.07
* ETH Indicators: RSI=26.0, EMA20=$2,085.26, EMA50=$2,094.85, 24h=+0.28%, 5d=+0.05%, VolConf=0.12
* SOL Indicators: RSI=28.4, EMA20=$84.18, EMA50=$84.68, 24h=+0.41%, 5d=+0.14%, VolConf=0.23
* XRP Indicators: RSI=20.5, EMA20=$1.34, EMA50=$1.34, 24h=+0.15%, 5d=-0.17%, VolConf=0.22
* USD1 Indicators: RSI=50.0, EMA20=$1.00, EMA50=$1.00, 24h=+0.00%, 5d=-0.01%, VolConf=0.40
* NEAR Indicators: RSI=24.8, EMA20=$2.68, EMA50=$2.62, 24h=+1.57%, 5d=-2.30%, VolConf=0.19
* HYPE Indicators: RSI=44.1, EMA20=$60.77, EMA50=$60.99, 24h=+1.31%, 5d=+1.07%, VolConf=0.17
* BNB Indicators: RSI=30.5, EMA20=$657.71, EMA50=$658.25, 24h=+0.18%, 5d=+0.05%, VolConf=0.18
* ZEC Indicators: RSI=27.0, EMA20=$599.21, EMA50=$620.21, 24h=+1.64%, 5d=-2.00%, VolConf=0.23
* DOGE Indicators: RSI=40.3, EMA20=$0.10, EMA50=$0.10, 24h=+0.49%, 5d=+0.31%, VolConf=0.25

### **Qualitative Evidence**
* No recent high-impact geopolitical or economic headlines parsed in this interval.
* Aggregate News Sentiment Score: +0.00 (Weights: Clear/Threat ±0.18, Easing/Tightening ±0.15)
* Regulatory Sentiment Bias: +0.10

### **Interpretation**
Leading regime is 'Neutral consolidation' with posterior probability 30.5% (confidence: Medium). Trend signal is negative (-0.10) and momentum is waning (-0.04). Treat this as a probabilistic belief state, not a deterministic prediction.

### **Invalidation Conditions**
* Regime velocity exceeds 5% shift toward Bullish or Bearish
* Volume breakout above 1.5x average

### **Risk-Aware Decision Support**
**Global Thesis Action Strategy**: Guided by Bayesian Regime *Neutral consolidation*.

**Top 5 Currencies Priority List**:
```text
Rank | Asset  | Spot Price   | Momentum   | Rec Allocation 
----------------------------------------------------------
1    | USD1   | $1.00        | -0.001     | 0.0% (HOLD)    
2    | BNB    | $656.80      | -0.017     | 0.0% (HOLD)    
3    | DOGE   | $0.10        | -0.026     | 0.0% (HOLD)    
4    | XRP    | $1.33        | -0.042     | 0.0% (HOLD)    
5    | BTC    | $75,855.60   | -0.042     | 0.0% (HOLD)    
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