### **System Analysis Report**
*   **Report ID**: `b2f04cc7-4faa-4e0e-a548-bfe67f32ac10`
*   **Generated Timestamp (UTC)**: 2026-05-27T00:01:01.288174+00:00Z
*   **Interval Label**: 3-Hourly Scheduled Pulse
*   **BTC Spot Price**: $75,813.60 USD
*   **ETH Spot Price**: $2,070.16 USD
*   **SOL Spot Price**: $83.68 USD
*   **XRP Spot Price**: $1.33 USD
*   **USD1 Spot Price**: $1.00 USD
*   **NEAR Spot Price**: $2.54 USD
*   **HYPE Spot Price**: $59.39 USD
*   **BNB Spot Price**: $655.68 USD
*   **ZEC Spot Price**: $567.99 USD
*   **DOGE Spot Price**: $0.10 USD

### **Executive Summary**
*   **Date/Time (US EDT) of the analysis**: 2026-05-26 08:01:01 PM EDT
*   **Portfolio Current Value**: $982.42 USD ($750.00 Cash / $232.42 Holdings)
*   **The Last Trade**: [2026-05-26T16:38:55.139395+00:00] BUY 91.575092 NEAR @ $2.73 USD (Total: $250.00 USD)
*   **Recommendation (HOLD / BUY / SELL) currency**: <b>RULE-BASED HOLD (Conviction below threshold)</b>
    *   *Key Macro Indicators*: SPY=$750.59, QQQ=$730.28, DXY=99.09, US10Y=4.49%
    *   *Market Trend Probability*: Neutral consolidation (30.1% probability)


### **Market Thesis**
Leading regime is classified as *Neutral consolidation* with a posterior probability weight of *30.1%*.

### **Probability Table**
```text
Market Regime                  | Probability | Confidence
----------------------------------------------------------
Neutral consolidation          | 30.1%       | Medium    
Bullish accumulation           | 16.0%       | Low       
Bullish continuation           | 13.0%       | Low       
High-volatility transition     | 12.2%       | Low       
Macro-driven risk-off          | 11.7%       | Low       
Bearish continuation           | 8.6%        | Low       
Bearish distribution           | 8.2%        | Low       
```

### **Quantitative Evidence**
* BTC latest close: $75,813.60
* Trend score: -0.106 (positive = above EMA-50)
* Momentum score: -0.043 (EMA-12 vs EMA-26 spread)
* Volatility score: 0.036 (0=calm, 1=extreme)
* Volume score: 0.145 (0.5=avg, 1.0=2x avg)
* Macro support: +0.267 (equity trend minus DXY drag)
*   Momentum [USD1]: -0.001
*   Momentum [BNB]: -0.018
*   Momentum [DOGE]: -0.030
*   Momentum [XRP]: -0.042
*   Momentum [BTC]: -0.043
*   Momentum [SOL]: -0.046
*   Momentum [ETH]: -0.048
*   Momentum [NEAR]: -0.063
*   Momentum [HYPE]: -0.072
*   Momentum [ZEC]: -0.284
* BTC Indicators: RSI=39.1, EMA20=$76,329.50, EMA50=$76,624.22, 24h=+0.24%, 5d=-0.14%, VolConf=0.15
* ETH Indicators: RSI=40.5, EMA20=$2,086.10, EMA50=$2,095.54, 24h=+0.21%, 5d=-0.03%, VolConf=0.13
* SOL Indicators: RSI=23.0, EMA20=$84.16, EMA50=$84.67, 24h=+0.11%, 5d=-0.16%, VolConf=0.00
* XRP Indicators: RSI=38.1, EMA20=$1.34, EMA50=$1.34, 24h=-0.07%, 5d=-0.24%, VolConf=0.36
* USD1 Indicators: RSI=53.3, EMA20=$1.00, EMA50=$1.00, 24h=+0.01%, 5d=+0.01%, VolConf=0.55
* NEAR Indicators: RSI=38.4, EMA20=$2.68, EMA50=$2.62, 24h=-3.61%, 5d=-4.15%, VolConf=0.18
* HYPE Indicators: RSI=38.7, EMA20=$60.69, EMA50=$60.96, 24h=-0.20%, 5d=-0.44%, VolConf=0.00
* BNB Indicators: RSI=24.3, EMA20=$657.60, EMA50=$658.21, 24h=+0.01%, 5d=-0.12%, VolConf=0.01
* ZEC Indicators: RSI=32.1, EMA20=$601.48, EMA50=$621.92, 24h=-0.49%, 5d=-2.57%, VolConf=0.45
* DOGE Indicators: RSI=48.8, EMA20=$0.10, EMA50=$0.10, 24h=+0.02%, 5d=-0.07%, VolConf=0.20

### **Qualitative Evidence**
* HYPE chases new highs as ETF inflows, institutional adoption accelerate
* Crypto advocacy group challenges Senator Warren's claims on OCC charters
* Aggregate News Sentiment Score: +0.00 (Weights: Clear/Threat ±0.18, Easing/Tightening ±0.15)
* Regulatory Sentiment Bias: +0.10

### **Interpretation**
Leading regime is 'Neutral consolidation' with posterior probability 30.2% (confidence: Medium). Trend signal is negative (-0.11) and momentum is waning (-0.04). Treat this as a probabilistic belief state, not a deterministic prediction.

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
2    | BNB    | $655.68      | -0.018     | 0.0% (HOLD)    
3    | DOGE   | $0.10        | -0.030     | 0.0% (HOLD)    
4    | XRP    | $1.33        | -0.042     | 0.0% (HOLD)    
5    | BTC    | $75,813.60   | -0.043     | 0.0% (HOLD)    
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