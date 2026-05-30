### **System Analysis Report**
*   **Report ID**: `c08fe698-1a6c-4b2f-b16d-df615e420dad`
*   **Generated Timestamp (UTC)**: 2026-05-27T15:01:47.840558+00:00Z
*   **Interval Label**: 3-Hourly Scheduled Pulse
*   **BTC Spot Price**: $74,896.28 USD
*   **ETH Spot Price**: $2,058.09 USD
*   **SOL Spot Price**: $83.78 USD
*   **XRP Spot Price**: $1.33 USD
*   **USD1 Spot Price**: $1.00 USD
*   **HYPE Spot Price**: $59.92 USD
*   **BNB Spot Price**: $652.81 USD
*   **NEAR Spot Price**: $2.55 USD
*   **ZEC Spot Price**: $566.89 USD
*   **DOGE Spot Price**: $0.10 USD

### **Executive Summary**
*   **Date/Time (US EDT) of the analysis**: 2026-05-27 11:01:47 AM EDT
*   **Portfolio Current Value**: $983.79 USD
*   **The Last Trade**: [2026-05-26T16:38:55.139395+00:00] BUY 91.575092 NEAR @ $2.73 USD (Total: $250.00 USD)
*   **Recommendation (HOLD / BUY / SELL) currency**: <b>RULE-BASED HOLD (Conviction below threshold)</b>
    *   *Key Macro Indicators*: SPY=$749.76, QQQ=$726.94, DXY=99.12, US10Y=4.47%
    *   *Market Trend Probability*: Bullish accumulation (36.5% probability)


### **Market Thesis**
Leading regime is classified as *Bullish accumulation* with a posterior probability weight of *36.5%*.

### **Probability Table**
```text
Market Regime                  | Probability | Confidence
----------------------------------------------------------
Bullish accumulation           | 36.5%       | Medium    
Neutral consolidation          | 22.7%       | Low       
Bullish continuation           | 12.5%       | Low       
Macro-driven risk-off          | 10.1%       | Low       
High-volatility transition     | 9.6%        | Low       
Bearish continuation           | 4.7%        | Low       
Bearish distribution           | 3.9%        | Low       
```

### **Quantitative Evidence**
* BTC latest close: $74,896.28
* Trend score: -0.165 (positive = above EMA-50)
* Momentum score: -0.042 (EMA-12 vs EMA-26 spread)
* Volatility score: 0.025 (0=calm, 1=extreme)
* Volume score: 1.000 (0.5=avg, 1.0=2x avg)
* Macro support: -0.053 (equity trend minus DXY drag)
*   Momentum [DOGE]: -0.002
*   Momentum [USD1]: -0.002
*   Momentum [HYPE]: -0.007
*   Momentum [SOL]: -0.020
*   Momentum [BNB]: -0.021
*   Momentum [XRP]: -0.027
*   Momentum [ETH]: -0.029
*   Momentum [BTC]: -0.042
*   Momentum [NEAR]: -0.145
*   Momentum [ZEC]: -0.174
* BTC Indicators: RSI=22.3, EMA20=$75,691.74, EMA50=$76,150.03, 24h=-0.03%, 5d=-1.16%, VolConf=1.00
* ETH Indicators: RSI=30.8, EMA20=$2,075.43, EMA50=$2,085.61, 24h=-0.11%, 5d=-0.89%, VolConf=1.00
* SOL Indicators: RSI=50.7, EMA20=$83.85, EMA50=$84.27, 24h=+0.01%, 5d=-0.04%, VolConf=0.00
* XRP Indicators: RSI=46.6, EMA20=$1.33, EMA50=$1.34, 24h=+0.45%, 5d=-0.08%, VolConf=0.80
* USD1 Indicators: RSI=33.3, EMA20=$1.00, EMA50=$1.00, 24h=+0.04%, 5d=-0.04%, VolConf=0.58
* HYPE Indicators: RSI=49.1, EMA20=$61.20, EMA50=$61.18, 24h=-0.10%, 5d=-3.79%, VolConf=0.01
* BNB Indicators: RSI=36.3, EMA20=$654.14, EMA50=$656.04, 24h=-0.03%, 5d=+0.00%, VolConf=0.04
* NEAR Indicators: RSI=47.9, EMA20=$2.56, EMA50=$2.58, 24h=+0.59%, 5d=+2.49%, VolConf=0.69
* ZEC Indicators: RSI=39.0, EMA20=$577.73, EMA50=$599.06, 24h=-1.49%, 5d=-0.57%, VolConf=0.49
* DOGE Indicators: RSI=49.8, EMA20=$0.10, EMA50=$0.10, 24h=+0.00%, 5d=-0.12%, VolConf=0.00

### **Qualitative Evidence**
* No recent high-impact geopolitical or economic headlines parsed in this interval.
* Aggregate News Sentiment Score: +0.00 (Weights: Clear/Threat ±0.18, Easing/Tightening ±0.15)
* Regulatory Sentiment Bias: +0.10

### **Interpretation**
Leading regime is 'Bullish accumulation' with posterior probability 36.5% (confidence: Medium). Trend signal is negative (-0.16) and momentum is waning (-0.04). Treat this as a probabilistic belief state, not a deterministic prediction.

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
1    | DOGE   | $0.10        | -0.002     | 0.0% (HOLD)    
2    | USD1   | $1.00        | -0.002     | 0.0% (HOLD)    
3    | HYPE   | $59.92       | -0.007     | 0.0% (HOLD)    
4    | SOL    | $83.78       | -0.020     | 0.0% (HOLD)    
5    | BNB    | $652.81      | -0.021     | 0.0% (HOLD)    
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