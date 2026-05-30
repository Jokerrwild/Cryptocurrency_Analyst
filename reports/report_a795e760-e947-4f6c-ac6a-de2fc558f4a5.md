### **System Analysis Report**
*   **Report ID**: `a795e760-e947-4f6c-ac6a-de2fc558f4a5`
*   **Generated Timestamp (UTC)**: 2026-05-27T01:44:31.138928+00:00Z
*   **Interval Label**: 3-Hourly Scheduled Pulse
*   **BTC Spot Price**: $75,793.91 USD
*   **ETH Spot Price**: $2,072.11 USD
*   **SOL Spot Price**: $83.79 USD
*   **USD1 Spot Price**: $1.00 USD
*   **XRP Spot Price**: $1.33 USD
*   **NEAR Spot Price**: $2.54 USD
*   **HYPE Spot Price**: $60.19 USD
*   **BNB Spot Price**: $656.60 USD
*   **ZEC Spot Price**: $574.63 USD
*   **WLD Spot Price**: $0.37 USD

### **Executive Summary**
*   **Date/Time (US EDT) of the analysis**: 2026-05-26 09:44:31 PM EDT
*   **Portfolio Current Value**: $982.14 USD
*   **The Last Trade**: [2026-05-26T16:38:55.139395+00:00] BUY 91.575092 NEAR @ $2.73 USD (Total: $250.00 USD)
*   **Recommendation (HOLD / BUY / SELL) currency**: <b>RULE-BASED HOLD (Conviction below threshold)</b>
    *   *Key Macro Indicators*: SPY=$750.59, QQQ=$730.28, DXY=99.11, US10Y=4.49%
    *   *Market Trend Probability*: Neutral consolidation (29.7% probability)


### **Market Thesis**
Leading regime is classified as *Neutral consolidation* with a posterior probability weight of *29.7%*.

### **Probability Table**
```text
Market Regime                  | Probability | Confidence
----------------------------------------------------------
Neutral consolidation          | 29.7%       | Medium    
Bullish accumulation           | 17.8%       | Low       
Bullish continuation           | 13.2%       | Low       
High-volatility transition     | 12.0%       | Low       
Macro-driven risk-off          | 11.5%       | Low       
Bearish continuation           | 8.1%        | Low       
Bearish distribution           | 7.6%        | Low       
```

### **Quantitative Evidence**
* BTC latest close: $75,793.91
* Trend score: -0.101 (positive = above EMA-50)
* Momentum score: -0.041 (EMA-12 vs EMA-26 spread)
* Volatility score: 0.036 (0=calm, 1=extreme)
* Volume score: 0.260 (0.5=avg, 1.0=2x avg)
* Macro support: +0.248 (equity trend minus DXY drag)
*   Momentum [WLD]: +0.253
*   Momentum [USD1]: -0.001
*   Momentum [BNB]: -0.015
*   Momentum [XRP]: -0.040
*   Momentum [BTC]: -0.041
*   Momentum [SOL]: -0.042
*   Momentum [ETH]: -0.044
*   Momentum [HYPE]: -0.055
*   Momentum [NEAR]: -0.114
*   Momentum [ZEC]: -0.276
* BTC Indicators: RSI=27.2, EMA20=$76,248.56, EMA50=$76,568.41, 24h=-0.23%, 5d=+0.01%, VolConf=0.26
* ETH Indicators: RSI=28.3, EMA20=$2,084.34, EMA50=$2,094.11, 24h=-0.40%, 5d=+0.10%, VolConf=0.08
* SOL Indicators: RSI=31.2, EMA20=$84.15, EMA50=$84.65, 24h=-0.29%, 5d=+0.26%, VolConf=0.16
* USD1 Indicators: RSI=46.7, EMA20=$1.00, EMA50=$1.00, 24h=+0.01%, 5d=+0.00%, VolConf=0.40
* XRP Indicators: RSI=25.4, EMA20=$1.34, EMA50=$1.34, 24h=-0.05%, 5d=+0.02%, VolConf=0.42
* NEAR Indicators: RSI=22.4, EMA20=$2.66, EMA50=$2.62, 24h=-1.17%, 5d=-2.65%, VolConf=0.10
* HYPE Indicators: RSI=45.3, EMA20=$60.76, EMA50=$60.98, 24h=-0.89%, 5d=+1.98%, VolConf=0.19
* BNB Indicators: RSI=32.5, EMA20=$657.68, EMA50=$658.22, 24h=-0.17%, 5d=+0.14%, VolConf=0.30
* ZEC Indicators: RSI=28.1, EMA20=$597.10, EMA50=$618.53, 24h=-0.94%, 5d=-0.24%, VolConf=0.24
* WLD Indicators: RSI=34.4, EMA20=$0.37, EMA50=$0.35, 24h=-1.26%, 5d=-2.26%, VolConf=0.15

### **Qualitative Evidence**
* No recent high-impact geopolitical or economic headlines parsed in this interval.
* Aggregate News Sentiment Score: +0.00 (Weights: Clear/Threat ±0.18, Easing/Tightening ±0.15)
* Regulatory Sentiment Bias: +0.10

### **Interpretation**
Leading regime is 'Neutral consolidation' with posterior probability 29.7% (confidence: Medium). Trend signal is negative (-0.10) and momentum is waning (-0.04). Treat this as a probabilistic belief state, not a deterministic prediction.

### **Invalidation Conditions**
* Regime velocity exceeds 5% shift toward Bullish or Bearish
* Volume breakout above 1.5x average

### **Risk-Aware Decision Support**
**Global Thesis Action Strategy**: Guided by Bayesian Regime *Neutral consolidation*.

**Top 5 Currencies Priority List**:
```text
Rank | Asset  | Spot Price   | Momentum   | Rec Allocation 
----------------------------------------------------------
1    | WLD    | $0.37        | +0.253     | 0.0% (HOLD)    
2    | USD1   | $1.00        | -0.001     | 0.0% (HOLD)    
3    | BNB    | $656.60      | -0.015     | 0.0% (HOLD)    
4    | XRP    | $1.33        | -0.040     | 0.0% (HOLD)    
5    | BTC    | $75,793.91   | -0.041     | 0.0% (HOLD)    
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