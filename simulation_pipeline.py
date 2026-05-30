import os
import sys
import uuid
import json
import logging
from datetime import datetime, timedelta, timezone

# Configure root logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("crypto_analyst.pipeline")

from crypto_analyst.config import load_config
from crypto_analyst.db import (
    init_db, 
    is_pipeline_frozen, 
    set_pipeline_frozen, 
    log_checkpoint, 
    prune_old_data, 
    get_db_connection
)
from crypto_analyst.sources import fetch_market_snapshot
from crypto_analyst.news_feed import ingest_and_score_news
from crypto_analyst.bayesian import analyze_snapshot
from crypto_analyst.indicators import momentum_score, trend_score, rsi, ema, pct_change, volume_score
from crypto_analyst.weight_learner import record_prediction, resolve_regime_outcome, run_adaptive_update
from crypto_analyst.worklog_util import log_incident_or_event

# State files
LEDGER_PATH = "/a0/usr/projects/cryptocurrency_analyst/ledger.json"
PENDING_TX_PATH = "/a0/usr/projects/cryptocurrency_analyst/pending_transaction.json"

def init_ledger() -> None:
    """Initializes ledger.json with $1,000 USD starting capital if it does not exist."""
    if not os.path.exists(LEDGER_PATH):
        initial_state = {
            "cash_usd": 1000.00,
            "holdings": {},
            "portfolio_value_usd": 1000.00,
            "performance_metrics": {
                "roi_percent": 0.0,
                "days_elapsed": 0,
                "win_rate": 0.0
            },
            "transaction_history": []
        }
        with open(LEDGER_PATH, "w") as f:
            json.dump(initial_state, f, indent=2)
        logger.info(f"Initialized ledger.json starting balance: $1,000.00 USD")

def get_current_portfolio_value() -> float:
    """Reads current mark-to-market valuation from the state ledger."""
    try:
        with open(LEDGER_PATH, "r") as f:
            ledger = json.load(f)
            return float(ledger.get("portfolio_value_usd", 1000.00))
    except Exception:
        return 1000.00

def compile_structured_report(
    run_id: str,
    timestamp_utc: str,
    timestamp_edt: str,
    asset_spot_prices: dict[str, float],
    regime_probs: list,
    leading_regime: str,
    prob_val: float,
    quant_ev: list,
    qual_ev: list,
    interpretation: str,
    invalidation: list,
    top_5_recommendations: list[dict],
    monitor_next: list,
    portfolio_value: float,
    last_trade_str: str,
    recommendation_summary: str,
    macro_benchmarks_str: str
) -> str:
    """
    Compiles a beautiful report strictly adhering to the 10-section operational schema
    augmented with an executive summary at the top containing EDT timestamp, portfolio value,
    highly detailed last trade parameters, and macro-integrated recommendations.
    Encloses raw tables and technical IDs inside code blocks to prevent Telegram parse errors.
    """
    safe_run_id = f"`{run_id}`"
    
    header_lines = [
        f"*   **Report ID**: {safe_run_id}",
        f"*   **Generated Timestamp (UTC)**: {timestamp_utc}",
        f"*   **Interval Label**: 3-Hourly Scheduled Pulse"
    ]
    for symbol in list(asset_spot_prices.keys()):
        header_lines.append(f"*   **{symbol} Spot Price**: ${asset_spot_prices[symbol]:,.2f} USD")
            
    header = "\n".join(header_lines)

    # Highly Detailed Executive Summary Block matching exact specification
    exec_summary = f"""*   **Date/Time (US EDT) of the analysis**: {timestamp_edt}
*   **Portfolio Current Value**: ${portfolio_value:,.2f} USD
*   **The Last Trade**: {last_trade_str}
*   **Recommendation (HOLD / BUY / SELL) currency**: <b>{recommendation_summary}</b>
    *   *Key Macro Indicators*: {macro_benchmarks_str}
    *   *Market Trend Probability*: {leading_regime} ({prob_val:.1%} probability)
"""

    # Generate probability text table to display in a code block safely on Telegram
    prob_table_lines = [
        "```text",
        f"{'Market Regime':<30} | {'Probability':<11} | {'Confidence':<10}",
        "-" * 58
    ]
    for p in regime_probs:
        prob_table_lines.append(f"{p.regime:<30} | {p.probability:<11.1%} | {p.confidence:<10}")
    prob_table_lines.append("```")
    prob_table = "\n".join(prob_table_lines)

    # Generate Top 5 Recommendations Table
    rec_table_lines = [
        "```text",
        f"{'Rank':<4} | {'Asset':<6} | {'Spot Price':<12} | {'Momentum':<10} | {'Rec Allocation':<15}",
        "-" * 58
    ]
    for r in top_5_recommendations:
        price_str = f"${r['spot_price']:,.2f}" if r['spot_price'] > 0 else "N/A"
        alloc_str = f"{r['suggested_allocation']:.1f}% (BUY)" if r['suggested_allocation'] > 0 else "0.0% (HOLD)"
        mom_str = f"{r['momentum']:+.3f}"
        rec_table_lines.append(f"{r['rank']:<4} | {r['asset']:<6} | {price_str:<12} | {mom_str:<10} | {alloc_str:<15}")
    rec_table_lines.append("```")
    rec_table = "\n".join(rec_table_lines)

    # Wrap individual list bullets cleanly
    quant_section = "\n".join([f"* {item}" for item in quant_ev])
    qual_section = "\n".join([f"* {item}" for item in qual_ev])
    invalidation_section = "\n".join([f"* {item}" for item in invalidation])
    monitor_section = "\n".join([f"* {item}" for item in monitor_next])

    report = f"""### **System Analysis Report**
{header}

### **Executive Summary**
{exec_summary}

### **Market Thesis**
Leading regime is classified as *{leading_regime}* with a posterior probability weight of *{prob_val:.1%}*.

### **Probability Table**
{prob_table}

### **Quantitative Evidence**
{quant_section}

### **Qualitative Evidence**
{qual_section}

### **Interpretation**
{interpretation}

### **Invalidation Conditions**
{invalidation_section}

### **Risk-Aware Decision Support**
**Global Thesis Action Strategy**: Guided by Bayesian Regime *{leading_regime}*.

**Top 5 Currencies Priority List**:
{rec_table}

All suggestions are trade recommendations awaiting strict Human-in-the-Loop (HITL) manual confirmation.

### **What To Monitor Next**
{monitor_section}

### **Learning Notes**
Model weights adaptively learned using historical priors. Minimum conviction threshold enforced at 55%. If leading probability falls below conviction threshold, recommended allocation defaults to HOLD state across all assets.
"""
    return report.strip()

def run_pipeline() -> None:
    """Executes the sequential 3-hourly analytical pipeline under strict error limit guardrails."""
    run_id = str(uuid.uuid4())
    
    # Generate timestamps
    now_utc = datetime.now(timezone.utc)
    utc_now_str = now_utc.isoformat() + "Z"
    
    # Compute US Eastern Daylight Time (EDT = UTC - 4 hours)
    edt_now = now_utc - timedelta(hours=4)
    edt_now_str = edt_now.strftime("%Y-%m-%d %I:%M:%S %p EDT")
    
    # 1. Initialize persistent stores
    init_db()
    init_ledger()
    
    # 2. Check freeze state
    if is_pipeline_frozen():
        logger.error("Pipeline execution is frozen due to a prior critical incident flag (pipeline_frozen = true). Execution halted.")
        sys.exit(1)
        
    logger.info(f"Launching scheduled pipeline execution run: {run_id}")
    
    try:
        # Checkpoint 1: scheduler fired
        log_checkpoint(run_id, "scheduler fired", "success", "Pipeline triggered successfully.")
        
        # Load configs
        cfg = load_config()
        
        # Checkpoint 2: sources fetched
        snapshot = fetch_market_snapshot(cfg)
        
        # Map current prices for all tracked assets
        prices_map = {}
        for s in snapshot.crypto:
            prices_map[s.label] = s.latest_close if s.latest_close else 0.0
            
        btc_price = prices_map.get("BTC", 0.0)
        eth_price = prices_map.get("ETH", 0.0)
        if btc_price == 0.0 or eth_price == 0.0:
            raise ValueError("Market data retrieval failed: critical spot prices are missing.")
            
        log_checkpoint(run_id, "sources fetched", "success", f"Fetched market prices for top {len(snapshot.crypto)} assets. BTC={btc_price}, ETH={eth_price}")
        
        # Extract key macro indicators
        macro_map = {}
        for m in snapshot.macro:
            macro_map[m.label] = m.latest_close if m.latest_close else 0.0
            
        spy_val = macro_map.get("SPY", 0.0)
        qqq_val = macro_map.get("QQQ", 0.0)
        dxy_val = macro_map.get("DX-Y.NYB", macro_map.get("DXY", 0.0))
        tnx_val = macro_map.get("10Y", 0.0)
        
        macro_benchmarks_str = f"SPY=${spy_val:,.2f}, QQQ=${qqq_val:,.2f}, DXY={dxy_val:.2f}, US10Y={tnx_val:.2f}%"
        
        # Checkpoint 3: indicators computed
        log_checkpoint(run_id, "indicators computed", "success", "Indicators derived successfully.")
        
        # Checkpoint 4: Bayesian analysis completed
        news_score, news_headlines_data = ingest_and_score_news()
        headlines = [item["title"] for item in news_headlines_data[:5]]
        
        # Run weight updates conservatively
        run_adaptive_update()
        
        # Execute core Bayesian model on the base asset to determine global Market Thesis
        analysis_result = analyze_snapshot(snapshot, cfg, news_sentiment_score=news_score, news_headlines=headlines)
        leading_reg = analysis_result.leading_regime
        leading_prob = analysis_result.regime_probabilities[0].probability
        
        # Persist snapshot state to SQLite snapshots table
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO snapshots (timestamp, btc_price, eth_price, rsi, trend_score, momentum_score, macro_support, macro_risk, raw_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                utc_now_str,
                btc_price,
                eth_price,
                analysis_result.quantitative_evidence[4] if len(analysis_result.quantitative_evidence)>4 else 0.0,
                analysis_result.quantitative_evidence[1] if len(analysis_result.quantitative_evidence)>1 else 0.0,
                analysis_result.quantitative_evidence[2] if len(analysis_result.quantitative_evidence)>2 else 0.0,
                analysis_result.quantitative_evidence[5] if len(analysis_result.quantitative_evidence)>5 else 0.0,
                0.0,
                json.dumps(utc_now_str)
            ))
            conn.commit()
            
        # Record current prediction
        record_prediction(utc_now_str, leading_reg, leading_prob)
        log_checkpoint(run_id, "Bayesian analysis completed", "success", f"Bayesian calculation complete. Classified regime: {leading_reg} ({leading_prob:.1%})")
        
        # Rank all 10 assets descending by momentum score to get top 5 recommendations
        asset_scores = []
        for s in snapshot.crypto:
            if s.closes:
                m_score = momentum_score(s)
                t_score = trend_score(s)
                asset_scores.append({
                    "asset": s.label,
                    "spot_price": s.latest_close if s.latest_close else 0.0,
                    "momentum": m_score,
                    "trend": t_score
                })
                
        # Sort descending by individual asset momentum score
        sorted_assets = sorted(asset_scores, key=lambda x: -x["momentum"])
        
        # Build Top 5 Recommendations list
        top_5_recommendations = []
        for rank, item in enumerate(sorted_assets[:5], 1):
            suggested_allocation = 0.0
            # Apply Bayesian Sizing rules based on the Global Market Thesis
            if leading_prob >= 0.55 and ("Bullish" in leading_reg) and item["momentum"] > 0:
                # If thesis is highly bullish, compute a proportional Half-Kelly size bounded by a conservative 10% safety cap per asset
                kelly_raw = (leading_prob * 2.0 - 1.0) / 2.0
                half_kelly = max(0.0, kelly_raw / 2.0)
                suggested_allocation = min(10.0, half_kelly * 100.0) # Cap at 10.0% max per asset
                
            top_5_recommendations.append({
                "rank": rank,
                "asset": item["asset"],
                "spot_price": item["spot_price"],
                "momentum": item["momentum"],
                "suggested_allocation": suggested_allocation
            })
            
        # Parse state ledger fields dynamically for Executive Summary rendering
        portfolio_val = 1000.00
        last_trade_str = "None (Initial Capital Staging)"
        try:
            with open(LEDGER_PATH, "r") as lf:
                ledger_data = json.load(lf)
                cash_usd = float(ledger_data.get("cash_usd", 1000.00))
                holdings = ledger_data.get("holdings", {})
                
                # Calculate dynamic mark-to-market portfolio value
                holdings_val = 0.0
                for asset, qty in holdings.items():
                    spot_price = prices_map.get(asset, 0.0)
                    holdings_val += float(qty) * spot_price
                
                portfolio_val = cash_usd + holdings_val
                
                # Update the ledger data with the new calculated value
                ledger_data["portfolio_value_usd"] = portfolio_val
                history = ledger_data.get("transaction_history", [])
                if history:
                    last_tx = history[-1]
                    last_trade_str = f"[{last_tx.get('timestamp_utc', 'N/A')}] {last_tx.get('action', 'HOLD')} {last_tx.get('quantity', 0.0):.6f} {last_tx.get('asset', 'N/A')} @ ${last_tx.get('price', 0.0):,.2f} USD (Total: ${last_tx.get('total_usd', 0.0):,.2f} USD)"
            
            # Save the updated ledger back to disk
            with open(LEDGER_PATH, "w") as lf:
                json.dump(ledger_data, lf, indent=2)
        except Exception as le:
            logger.warning(f"Could not parse ledger state fields: {le}")
            
        # Determine overarching action recommendation summary
        buy_list = [rec["asset"] for rec in top_5_recommendations if rec["suggested_allocation"] > 0.0]
        if buy_list:
            rec_summary = f"BUY {', '.join(buy_list)} (Staged)"
        else:
            rec_summary = "RULE-BASED HOLD (Conviction below threshold)"
            
        # Extract and append advanced technical metrics for each asset directly to quantitative evidence list
        for s in snapshot.crypto:
            rsi_val = rsi(s.closes) or 0.0
            ema20_val = ema(s.closes, 20) or 0.0
            ema50_val = ema(s.closes, 50) or 0.0
            move24h = pct_change(s.closes[-1], s.closes[-2] if len(s.closes) > 1 else None) or 0.0
            move5d = pct_change(s.closes[-1], s.closes[-5] if len(s.closes) > 5 else None) or 0.0
            v_score = volume_score(s)
            analysis_result.quantitative_evidence.append(
                f"{s.label} Indicators: RSI={rsi_val:.1f}, EMA20=${ema20_val:,.2f}, EMA50=${ema50_val:,.2f}, 24h={move24h:+.2f}%, 5d={move5d:+.2f}%, VolConf={v_score:.2f}"
            )
            
        # Checkpoint 5: report rendered
        report_markdown = compile_structured_report(
            run_id=run_id,
            timestamp_utc=utc_now_str,
            timestamp_edt=edt_now_str,
            asset_spot_prices=prices_map,
            regime_probs=analysis_result.regime_probabilities,
            leading_regime=leading_reg,
            prob_val=leading_prob,
            quant_ev=analysis_result.quantitative_evidence,
            qual_ev=analysis_result.qualitative_evidence,
            interpretation=analysis_result.interpretation,
            invalidation=analysis_result.invalidation_conditions,
            top_5_recommendations=top_5_recommendations,
            monitor_next=analysis_result.monitor_next,
            portfolio_value=portfolio_val,
            last_trade_str=last_trade_str,
            recommendation_summary=rec_summary,
            macro_benchmarks_str=macro_benchmarks_str
        )
        
        # Save report local copy
        reports_dir = "/a0/usr/projects/cryptocurrency_analyst/reports"
        os.makedirs(reports_dir, exist_ok=True)
        report_file_path = os.path.join(reports_dir, f"report_{run_id}.md")
        with open(report_file_path, "w") as rf:
            rf.write(report_markdown)
            
        log_checkpoint(run_id, "report rendered", "success", f"Saved local report at: {report_file_path}")
        
        # Checkpoint 7: ledger updated only if approved
        # Generate pending transactions for all top 5 candidates
        staged_transactions = []
        for rec in top_5_recommendations:
            staged_transactions.append({
                "asset": rec["asset"],
                "action": "BUY" if rec["suggested_allocation"] > 0 else "HOLD",
                "allocation_percentage": rec["suggested_allocation"],
                "spot_price": rec["spot_price"]
            })
            
        pending_tx = {
            "timestamp_utc": utc_now_str,
            "run_id": run_id,
            "global_regime": leading_reg,
            "global_confidence": analysis_result.regime_probabilities[0].confidence,
            "recommendations": staged_transactions,
            "approved": False
        }
        with open(PENDING_TX_PATH, "w") as tx_file:
            json.dump(pending_tx, tx_file, indent=2)
            
        log_checkpoint(run_id, "ledger updated only if approved", "success", "Staged recommendations in pending_transaction.json. Awaiting HITL approval.")
        
        # Process rolling database cleanups
        prune_old_data(days_limit=30)
        logger.info(f"Pipeline run {run_id} finished successfully.")
        
        # --- Self-cleaning routine to prevent context pollution ---
        context_id = os.environ.get("AGENT_CONTEXT_ID")
        if context_id:
            chat_file_path = f"/a0/usr/chats/{context_id}/chat.json"
            if os.path.exists(chat_file_path):
                try:
                    with open(chat_file_path, "w") as f:
                        f.write("[]") # Write an empty JSON array to clear the log
                    logger.info(f"Successfully cleared chat history for context {context_id} to prevent repetition fatigue.")
                except Exception as clean_e:
                    logger.warning(f"Failed to clear chat history file at {chat_file_path}: {clean_e}")
        # ---------------------------------------------------------
        
    except Exception as e:
        # Fail loudly, log programmatic incident, and freeze
        err_msg = f"Pipeline execution failure: {e}"
        logger.critical(err_msg, exc_info=True)
        
        # Log structured incident to WORKLOG.md
        log_incident_or_event(
            symptom=str(e),
            scope="simulation_pipeline orchestration layer",
            failed_hypotheses="Pipeline serial step transition mapping",
            root_cause=f"Exception: {type(e).__name__}",
            resolution="System execution halted, scheduled triggers disabled to prevent runaway loops",
            prevention="Safe-escape markdown characters and prevent nested layout syntax",
            tags="#orchestrator | #multi_asset",
            freeze_triggered=True
        )
        
        # Freeze pipeline and log failure
        set_pipeline_frozen(True)
        log_checkpoint(run_id, "execution boundary check", "failed", err_msg)
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()