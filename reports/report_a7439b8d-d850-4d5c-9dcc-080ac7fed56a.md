### **System Analysis Report**
*   **Report ID**: `a7439b8d-d850-4d5c-9dcc-080ac7fed56a`
*   **Generated Timestamp (UTC)**: 2026-05-31T06:13:53.488517+00:00Z
*   **Interval Label**: 3-Hourly Scheduled Pulse
*   **BTC Spot Price**: $73,901.17 USD
*   **ETH Spot Price**: $2,026.26 USD
*   **BNB Spot Price**: $734.97 USD
*   **SOL Spot Price**: $82.79 USD
*   **HYPE Spot Price**: $69.64 USD
*   **XLM Spot Price**: $0.24 USD
*   **XRP Spot Price**: $1.34 USD
*   **USD1 Spot Price**: $1.00 USD
*   **NEAR Spot Price**: $2.32 USD
*   **DOGE Spot Price**: $0.10 USD

### **Executive Summary**
*   **Date/Time (US EDT) of the analysis**: 2026-05-31 02:13:53 AM EDT
*   **Portfolio Current Value**: $1,028.11 USD
*   **The Last Trade**: [2026-05-28T17:48:57.677132+00:00] BUY 1315.789474 XLM @ $0.19 USD (Total: $250.00 USD)
*   **Recommendation (HOLD / BUY / SELL) currency**: <b>RULE-BASED HOLD (Conviction below threshold)</b>
    *   *Key Macro Indicators*: SPY=$756.48, QQQ=$738.31, DXY=98.91, US10Y=4.45%
    *   *Market Trend Probability*: Neutral consolidation (31.9% probability)


### **Market Thesis**
Leading regime is classified as *Neutral consolidation* with a posterior probability weight of *31.9%*.

### **Probability Table**
```text
Market Regime                  | Probability | Confidence
----------------------------------------------------------
Neutral consolidation          | 31.9%       | Medium    
Bullish accumulation           | 14.2%       | Low       
Bullish continuation           | 11.5%       | Low       
High-volatility transition     | 11.1%       | Low       
Macro-driven risk-off          | 10.9%       | Low       
Bearish continuation           | 10.5%       | Low       
Bearish distribution           | 9.9%        | Low       
```

### **Quantitative Evidence**
* BTC latest close: $73,901.17
* Trend score: +0.016 (positive = above EMA-50)
* Momentum score: +0.014 (EMA-12 vs EMA-26 spread)
* Volatility score: 0.009 (0=calm, 1=extreme)
* Volume score: 0.043 (0.5=avg, 1.0=2x avg)
* Macro support: +0.073 (equity trend minus DXY drag)
*   Momentum [BNB]: +0.263
*   Momentum [HYPE]: +0.151
*   Momentum [SOL]: +0.020
*   Momentum [ETH]: +0.017
*   Momentum [BTC]: +0.014
*   Momentum [XRP]: +0.012
*   Momentum [DOGE]: +0.009
*   Momentum [USD1]: +0.000
*   Momentum [XLM]: -0.048
*   Momentum [NEAR]: -0.117
* BTC Indicators: RSI=55.5, EMA20=$73,844.04, EMA50=$73,782.68, 24h=-0.06%, 5d=-0.11%, VolConf=0.04
* ETH Indicators: RSI=54.1, EMA20=$2,023.94, EMA50=$2,020.86, 24h=-0.04%, 5d=-0.24%, VolConf=0.07
* BNB Indicators: RSI=76.5, EMA20=$713.83, EMA50=$686.54, 24h=-0.14%, 5d=-0.44%, VolConf=0.02
* SOL Indicators: RSI=50.3, EMA20=$82.75, EMA50=$82.54, 24h=-0.13%, 5d=-0.29%, VolConf=0.14
* HYPE Indicators: RSI=70.9, EMA20=$68.15, EMA50=$66.16, 24h=+0.26%, 5d=+1.62%, VolConf=0.02
* XLM Indicators: RSI=36.7, EMA20=$0.24, EMA50=$0.23, 24h=+0.05%, 5d=-0.76%, VolConf=0.10
* XRP Indicators: RSI=39.7, EMA20=$1.34, EMA50=$1.34, 24h=-0.13%, 5d=-0.07%, VolConf=0.10
* USD1 Indicators: RSI=50.0, EMA20=$1.00, EMA50=$1.00, 24h=+0.00%, 5d=+0.01%, VolConf=0.07
* NEAR Indicators: RSI=45.9, EMA20=$2.32, EMA50=$2.37, 24h=+0.30%, 5d=+2.88%, VolConf=0.09
* DOGE Indicators: RSI=34.3, EMA20=$0.10, EMA50=$0.10, 24h=-0.06%, 5d=-0.32%, VolConf=0.49

### **Qualitative Evidence**
* No recent high-impact geopolitical or economic headlines parsed in this interval.
* Aggregate News Sentiment Score: +0.00 (Weights: Clear/Threat ±0.18, Easing/Tightening ±0.15)
* Regulatory Sentiment Bias: +0.10

### **Interpretation**
Leading regime is 'Neutral consolidation' with posterior probability 31.9% (confidence: Medium). Trend signal is positive (+0.02) and momentum is building (+0.01). Treat this as a probabilistic belief state, not a deterministic prediction.

### **Invalidation Conditions**
* Regime velocity exceeds 5% shift toward Bullish or Bearish
* Volume breakout above 1.5x average

### **Risk-Aware Decision Support**
**Global Thesis Action Strategy**: Guided by Bayesian Regime *Neutral consolidation*.

**Top 5 Currencies Priority List**:
```text
Rank | Asset  | Spot Price   | Momentum   | Rec Allocation 
----------------------------------------------------------
1    | BNB    | $734.97      | +0.263     | 0.0% (HOLD)    
2    | HYPE   | $69.64       | +0.151     | 0.0% (HOLD)    
3    | SOL    | $82.79       | +0.020     | 0.0% (HOLD)    
4    | ETH    | $2,026.26    | +0.017     | 0.0% (HOLD)    
5    | BTC    | $73,901.17   | +0.014     | 0.0% (HOLD)    
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