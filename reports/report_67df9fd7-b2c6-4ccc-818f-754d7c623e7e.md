### **System Analysis Report**
*   **Report ID**: `67df9fd7-b2c6-4ccc-818f-754d7c623e7e`
*   **Generated Timestamp (UTC)**: 2026-05-26T22:50:07.576905+00:00Z
*   **Interval Label**: 3-Hourly Scheduled Pulse
*   **BTC Spot Price**: $75,618.05 USD
*   **ETH Spot Price**: $2,064.03 USD
*   **SOL Spot Price**: $83.48 USD
*   **XRP Spot Price**: $1.33 USD
*   **USD1 Spot Price**: $1.00 USD
*   **NEAR Spot Price**: $2.62 USD
*   **HYPE Spot Price**: $59.28 USD
*   **BNB Spot Price**: $654.59 USD
*   **ZEC Spot Price**: $573.53 USD
*   **DOGE Spot Price**: $0.10 USD

### **Executive Summary**
*   **Date/Time (US EDT) of the analysis**: 2026-05-26 06:50:07 PM EDT
*   **Portfolio Current Value**: $990.38 USD ($750.00 Cash / $240.38 Holdings)
*   **The Last Trade**: [2026-05-26T16:38:55.139395+00:00] BUY 91.575092 NEAR @ $2.73 USD (Total: $250.00 USD)
*   **Recommendation (HOLD / BUY / SELL) currency**: <b>RULE-BASED HOLD (Conviction below threshold)</b>
    *   *Key Macro Indicators*: SPY=$750.59, QQQ=$730.28, DXY=99.14, US10Y=4.49%
    *   *Market Trend Probability*: Neutral consolidation (29.5% probability)


### **Market Thesis**
Leading regime is classified as *Neutral consolidation* with a posterior probability weight of *29.5%*.

### **Probability Table**
```text
Market Regime                  | Probability | Confidence
----------------------------------------------------------
Neutral consolidation          | 29.5%       | Medium    
Bullish accumulation           | 17.3%       | Low       
Bullish continuation           | 13.5%       | Low       
High-volatility transition     | 12.3%       | Low       
Macro-driven risk-off          | 11.8%       | Low       
Bearish continuation           | 8.1%        | Low       
Bearish distribution           | 7.6%        | Low       
```

### **Quantitative Evidence**
* BTC latest close: $75,618.05
* Trend score: -0.135 (positive = above EMA-50)
* Momentum score: -0.043 (EMA-12 vs EMA-26 spread)
* Volatility score: 0.036 (0=calm, 1=extreme)
* Volume score: 0.241 (0.5=avg, 1.0=2x avg)
* Macro support: +0.262 (equity trend minus DXY drag)
*   Momentum [USD1]: -0.001
*   Momentum [BNB]: -0.018
*   Momentum [NEAR]: -0.023
*   Momentum [DOGE]: -0.031
*   Momentum [XRP]: -0.040
*   Momentum [BTC]: -0.043
*   Momentum [SOL]: -0.047
*   Momentum [ETH]: -0.048
*   Momentum [HYPE]: -0.053
*   Momentum [ZEC]: -0.264
* BTC Indicators: RSI=35.1, EMA20=$76,382.56, EMA50=$76,656.23, 24h=-0.22%, 5d=-0.12%, VolConf=0.24
* ETH Indicators: RSI=37.6, EMA20=$2,087.61, EMA50=$2,096.49, 24h=-0.29%, 5d=-0.06%, VolConf=0.15
* SOL Indicators: RSI=39.9, EMA20=$84.26, EMA50=$84.75, 24h=-0.11%, 5d=+0.01%, VolConf=0.23
* XRP Indicators: RSI=39.7, EMA20=$1.34, EMA50=$1.35, 24h=-0.18%, 5d=-0.05%, VolConf=0.49
* USD1 Indicators: RSI=50.0, EMA20=$1.00, EMA50=$1.00, 24h=+0.00%, 5d=+0.03%, VolConf=0.93
* NEAR Indicators: RSI=41.7, EMA20=$2.70, EMA50=$2.63, 24h=+0.81%, 5d=+0.27%, VolConf=0.27
* HYPE Indicators: RSI=48.9, EMA20=$60.92, EMA50=$61.06, 24h=+0.44%, 5d=-3.83%, VolConf=0.23
* BNB Indicators: RSI=45.3, EMA20=$657.98, EMA50=$658.39, 24h=-0.17%, 5d=-0.03%, VolConf=0.16
* ZEC Indicators: RSI=31.6, EMA20=$605.27, EMA50=$624.21, 24h=-0.43%, 5d=-2.18%, VolConf=0.42
* DOGE Indicators: RSI=45.4, EMA20=$0.10, EMA50=$0.10, 24h=+0.03%, 5d=+0.02%, VolConf=0.19

### **Qualitative Evidence**
* Trump praises prediction markets, defends CFTC as court cases compound
* Bitcoin mining stocks jump as AI infrastructure boom boosts sector outlook
* Aggregate News Sentiment Score: +0.00 (Weights: Clear/Threat ±0.18, Easing/Tightening ±0.15)
* Regulatory Sentiment Bias: +0.10

### **Interpretation**
Leading regime is 'Neutral consolidation' with posterior probability 29.5% (confidence: Medium). Trend signal is negative (-0.14) and momentum is waning (-0.04). Treat this as a probabilistic belief state, not a deterministic prediction.

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
2    | BNB    | $654.59      | -0.018     | 0.0% (HOLD)    
3    | NEAR   | $2.62        | -0.023     | 0.0% (HOLD)    
4    | DOGE   | $0.10        | -0.031     | 0.0% (HOLD)    
5    | XRP    | $1.33        | -0.040     | 0.0% (HOLD)    
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