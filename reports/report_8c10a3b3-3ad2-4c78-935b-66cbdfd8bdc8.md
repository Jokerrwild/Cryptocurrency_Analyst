### **System Analysis Report**
*   **Report ID**: `8c10a3b3-3ad2-4c78-935b-66cbdfd8bdc8`
*   **Generated Timestamp (UTC)**: 2026-05-26T21:08:08.608156+00:00Z
*   **Interval Label**: 3-Hourly Scheduled Pulse
*   **BTC Spot Price**: $75,898.00 USD
*   **ETH Spot Price**: $2,072.84 USD
*   **SOL Spot Price**: $83.67 USD
*   **XRP Spot Price**: $1.33 USD
*   **USD1 Spot Price**: $1.00 USD
*   **NEAR Spot Price**: $2.64 USD
*   **HYPE Spot Price**: $59.72 USD
*   **BNB Spot Price**: $655.94 USD
*   **ZEC Spot Price**: $589.04 USD
*   **DOGE Spot Price**: $0.10 USD

### **Executive Summary**
*   **Date/Time (US EDT) of the analysis**: 2026-05-26 05:08:08 PM EDT
*   **Portfolio Current Value**: $991.48 USD ($750.00 Cash / $241.48 Holdings)
*   **The Last Trade**: [2026-05-26T16:38:55.139395+00:00] BUY 91.575092 NEAR @ $2.73 USD (Total: $250.00 USD)
*   **Recommendation (HOLD / BUY / SELL) currency**: <b>RULE-BASED HOLD (Conviction below threshold)</b>
    *   *Key Macro Indicators*: SPY=$750.59, QQQ=$730.28, DXY=99.15, US10Y=4.49%
    *   *Market Trend Probability*: Neutral consolidation (30.6% probability)


### **Market Thesis**
Leading regime is classified as *Neutral consolidation* with a posterior probability weight of *30.6%*.

### **Probability Table**
```text
Market Regime                  | Probability | Confidence
----------------------------------------------------------
Neutral consolidation          | 30.6%       | Medium    
Bullish accumulation           | 14.4%       | Low       
Bullish continuation           | 12.6%       | Low       
High-volatility transition     | 12.3%       | Low       
Macro-driven risk-off          | 11.9%       | Low       
Bearish continuation           | 9.3%        | Low       
Bearish distribution           | 8.9%        | Low       
```

### **Quantitative Evidence**
* BTC latest close: $75,898.00
* Trend score: -0.105 (positive = above EMA-50)
* Momentum score: -0.038 (EMA-12 vs EMA-26 spread)
* Volatility score: 0.035 (0=calm, 1=extreme)
* Volume score: 0.016 (0.5=avg, 1.0=2x avg)
* Macro support: +0.261 (equity trend minus DXY drag)
*   Momentum [NEAR]: +0.008
*   Momentum [USD1]: -0.001
*   Momentum [BNB]: -0.015
*   Momentum [HYPE]: -0.025
*   Momentum [DOGE]: -0.026
*   Momentum [XRP]: -0.037
*   Momentum [BTC]: -0.038
*   Momentum [ETH]: -0.043
*   Momentum [SOL]: -0.044
*   Momentum [ZEC]: -0.230
* BTC Indicators: RSI=38.4, EMA20=$76,473.54, EMA50=$76,702.52, 24h=-0.13%, 5d=+0.11%, VolConf=0.02
* ETH Indicators: RSI=41.4, EMA20=$2,090.35, EMA50=$2,097.91, 24h=-0.13%, 5d=+0.26%, VolConf=0.02
* SOL Indicators: RSI=43.1, EMA20=$84.36, EMA50=$84.80, 24h=-0.17%, 5d=+0.24%, VolConf=0.01
* XRP Indicators: RSI=41.4, EMA20=$1.34, EMA50=$1.35, 24h=-0.15%, 5d=-0.14%, VolConf=0.09
* USD1 Indicators: RSI=53.8, EMA20=$1.00, EMA50=$1.00, 24h=+0.00%, 5d=+0.02%, VolConf=0.31
* NEAR Indicators: RSI=43.5, EMA20=$2.71, EMA50=$2.63, 24h=-0.49%, 5d=-1.93%, VolConf=0.01
* HYPE Indicators: RSI=49.8, EMA20=$61.16, EMA50=$61.16, 24h=+0.12%, 5d=-2.88%, VolConf=0.01
* BNB Indicators: RSI=47.1, EMA20=$658.35, EMA50=$658.55, 24h=-0.08%, 5d=+0.20%, VolConf=0.05
* ZEC Indicators: RSI=36.0, EMA20=$609.85, EMA50=$626.76, 24h=-0.04%, 5d=-1.30%, VolConf=0.02
* DOGE Indicators: RSI=48.1, EMA20=$0.10, EMA50=$0.10, 24h=-0.21%, 5d=-0.04%, VolConf=0.01

### **Qualitative Evidence**
* No recent high-impact geopolitical or economic headlines parsed in this interval.
* Aggregate News Sentiment Score: +0.00 (Weights: Clear/Threat ±0.18, Easing/Tightening ±0.15)
* Regulatory Sentiment Bias: +0.10

### **Interpretation**
Leading regime is 'Neutral consolidation' with posterior probability 30.6% (confidence: Medium). Trend signal is negative (-0.10) and momentum is waning (-0.04). Treat this as a probabilistic belief state, not a deterministic prediction.

### **Invalidation Conditions**
* Regime velocity exceeds 5% shift toward Bullish or Bearish
* Volume breakout above 1.5x average

### **Risk-Aware Decision Support**
**Global Thesis Action Strategy**: Guided by Bayesian Regime *Neutral consolidation*.

**Top 5 Currencies Priority List**:
```text
Rank | Asset  | Spot Price   | Momentum   | Rec Allocation 
----------------------------------------------------------
1    | NEAR   | $2.64        | +0.008     | 0.0% (HOLD)    
2    | USD1   | $1.00        | -0.001     | 0.0% (HOLD)    
3    | BNB    | $655.94      | -0.015     | 0.0% (HOLD)    
4    | HYPE   | $59.72       | -0.025     | 0.0% (HOLD)    
5    | DOGE   | $0.10        | -0.026     | 0.0% (HOLD)    
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