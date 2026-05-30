### **System Analysis Report**
*   **Report ID**: `5dda3c0b-62c6-4d8a-a3f0-0d9023eca6e8`
*   **Generated Timestamp (UTC)**: 2026-05-25T22:15:03.116679+00:00Z
*   **Interval Label**: 3-Hourly Scheduled Pulse
*   **BTC Spot Price**: $77,324.91 USD
*   **ETH Spot Price**: $2,111.94 USD
*   **SOL Spot Price**: $85.40 USD
*   **XRP Spot Price**: $1.35 USD
*   **NEAR Spot Price**: $2.77 USD
*   **USD1 Spot Price**: $1.00 USD
*   **BNB Spot Price**: $662.00 USD
*   **HYPE Spot Price**: $61.64 USD
*   **ZEC Spot Price**: $651.69 USD
*   **SUI Spot Price**: $1.05 USD

### **Executive Summary**
*   **Date/Time (US EDT) of the analysis**: 2026-05-25 06:15:03 PM EDT
*   **Portfolio Current Value**: $1,000.00 USD
*   **The Last Trade**: None (Initial Capital Staging)
*   **Recommendation (HOLD / BUY / SELL) currency**: <b>RULE-BASED HOLD (Conviction below threshold)</b>
    *   *Key Macro Indicators*: SPY=$745.64, QQQ=$717.54, DXY=99.24, US10Y=4.56%
    *   *Market Trend Probability*: Neutral consolidation (31.4% probability)


### **Market Thesis**
Leading regime is classified as *Neutral consolidation* with a posterior probability weight of *31.4%*.

### **Probability Table**
```text
Market Regime                  | Probability | Confidence
----------------------------------------------------------
Neutral consolidation          | 31.4%       | Medium    
Bullish accumulation           | 14.1%       | Low       
Bullish continuation           | 12.3%       | Low       
High-volatility transition     | 11.4%       | Low       
Macro-driven risk-off          | 11.0%       | Low       
Bearish continuation           | 10.2%       | Low       
Bearish distribution           | 9.5%        | Low       
```

### **Quantitative Evidence**
* BTC latest close: $77,324.91
* Trend score: +0.043 (positive = above EMA-50)
* Momentum score: +0.018 (EMA-12 vs EMA-26 spread)
* Volatility score: 0.019 (0=calm, 1=extreme)
* Volume score: 0.156 (0.5=avg, 1.0=2x avg)
* Macro support: +0.090 (equity trend minus DXY drag)
*   Momentum [NEAR]: +0.403
*   Momentum [SUI]: +0.021
*   Momentum [BNB]: +0.020
*   Momentum [BTC]: +0.018
*   Momentum [ETH]: +0.016
*   Momentum [XRP]: +0.007
*   Momentum [ZEC]: +0.004
*   Momentum [SOL]: +0.002
*   Momentum [USD1]: -0.001
*   Momentum [HYPE]: -0.017
* BTC Indicators: RSI=48.7, EMA20=$77,289.04, EMA50=$76,993.50, 24h=+0.04%, 5d=-0.20%, VolConf=0.16
* ETH Indicators: RSI=48.1, EMA20=$2,113.86, EMA50=$2,107.47, 24h=+0.15%, 5d=-0.61%, VolConf=1.00
* SOL Indicators: RSI=37.7, EMA20=$85.66, EMA50=$85.54, 24h=+0.13%, 5d=-0.51%, VolConf=0.21
* XRP Indicators: RSI=43.2, EMA20=$1.36, EMA50=$1.35, 24h=+0.06%, 5d=-0.25%, VolConf=0.23
* NEAR Indicators: RSI=82.7, EMA20=$2.62, EMA50=$2.47, 24h=-0.65%, 5d=+1.69%, VolConf=0.20
* USD1 Indicators: RSI=20.0, EMA20=$1.00, EMA50=$1.00, 24h=+0.00%, 5d=-0.02%, VolConf=0.15
* BNB Indicators: RSI=51.3, EMA20=$662.01, EMA50=$658.95, 24h=+0.14%, 5d=-0.03%, VolConf=0.03
* HYPE Indicators: RSI=30.1, EMA20=$62.17, EMA50=$61.45, 24h=+0.29%, 5d=-0.10%, VolConf=0.06
* ZEC Indicators: RSI=38.4, EMA20=$659.15, EMA50=$651.86, 24h=+0.25%, 5d=-1.28%, VolConf=0.08
* SUI Indicators: RSI=56.2, EMA20=$1.05, EMA50=$1.05, 24h=-0.09%, 5d=-0.56%, VolConf=0.08

### **Qualitative Evidence**
* No recent high-impact geopolitical or economic headlines parsed in this interval.
* Aggregate News Sentiment Score: +0.00 (Weights: Clear/Threat ±0.18, Easing/Tightening ±0.15)
* Regulatory Sentiment Bias: +0.10

### **Interpretation**
Leading regime is 'Neutral consolidation' with posterior probability 31.4% (confidence: Medium). Trend signal is positive (+0.04) and momentum is building (+0.02). Treat this as a probabilistic belief state, not a deterministic prediction.

### **Invalidation Conditions**
* Regime velocity exceeds 5% shift toward Bullish or Bearish
* Volume breakout above 1.5x average

### **Risk-Aware Decision Support**
**Global Thesis Action Strategy**: Guided by Bayesian Regime *Neutral consolidation*.

**Top 5 Currencies Priority List**:
```text
Rank | Asset  | Spot Price   | Momentum   | Rec Allocation 
----------------------------------------------------------
1    | NEAR   | $2.77        | +0.403     | 0.0% (HOLD)    
2    | SUI    | $1.05        | +0.021     | 0.0% (HOLD)    
3    | BNB    | $662.00      | +0.020     | 0.0% (HOLD)    
4    | BTC    | $77,324.91   | +0.018     | 0.0% (HOLD)    
5    | ETH    | $2,111.94    | +0.016     | 0.0% (HOLD)    
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