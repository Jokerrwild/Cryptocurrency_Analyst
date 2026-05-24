# Master Procedural Blueprint: Crypto Market Trade & Simulation Application

**Author**: Senior Cryptocurrency Market & Macro-Statistical Analyst  
**Version**: 1.0.0  
**Date**: May 2026  
**Target Environment**: Agent Zero / Debian Linux VPS / Docker (Python 3.12+)  

---

## 1. Executive Summary & Core Objective
This document provides an absolute, step-by-step technical blueprint to build, deploy, and maintain the **Crypto Market Trade Analysis Application** (the "Application") inside the Cryptocurrency Analyst environment.

### Core Objective
Simulate an investment campaign starting with a baseline capital of **$1,000.00 USD** in Cash, targeting a net Return on Investment (ROI) of **$3,000.00** (total portfolio valuation of **$4,000.00**) within a **30-day timeframe** using systematic quantitative methods. The application runs every 3 hours starting at 12:00 AM UTC, compiling technical indicators, parsing zero-cost geopolitical RSS news feeds, updating a Bayesian belief-state model, and issuing risk-aware, Kelly-optimized simulated trade recommendations that require **Human-in-the-Loop (HITL)** approval before ledger commitment.

---

## 2. System Architecture & Data Flow Topology
```
                     +-------------------------------+                      
                     |    3-Hour Scheduler Trigger   |                      
                     +---------------+---------------+                      
                                     |                                      
                                     v                                      
                     +---------------+---------------+                      
                     |    simulation_pipeline.py     |                      
                     +---------------+---------------+                      
                                     |                                      
            +------------------------+------------------------+             
            |                        |                        |             
            v                        v                        v             
  +---------+---------+    +---------+---------+    +---------+---------+   
  |   sources.py      |    |   news_feed.py    |    |   db.py           |   
  | (Prices / Macro)  |    | (RSS Ingestion)   |    | (SQLite Storage)  |   
  +---------+---------+    +---------+---------+    +---------+---------+   
            |                        |                        |             
            |                        |                        |             
            +------------------------+------------------------+             
                                     |                                      
                                     v                                      
                     +---------------+---------------+                      
                     |     bayesian.py (Core Model)  |                      
                     | - Softmax Regime Calculation  |                      
                     | - Kelly Criterion Sizing     |                      
                     +---------------+---------------+                      
                                     |                                      
                                     v                                      
                     +---------------+---------------+                      
                     |     telegram_notifier.py      |                      
                     |  - Multi-Part Report Splitting|                      
                     |  - HITL Confirmation Prompt   |                      
                     +---------------+---------------+                      
                                     |                                      
                                     v                                      
                     +---------------+---------------+                      
                     |      Human-In-The-Loop        |                      
                     |   (Approve / Deny Trade)      |                      
                     +---------------+---------------+                      
                                     |                                      
                                     v (On Approval)                        
                     +---------------+---------------+                      
                     |     ledger.json (State)       |                      
                     +-------------------------------+                      
```

---

## 3. Detailed Component Implementation Specs

### 3.1 Database & Space Control Engine (`crypto_analyst/db.py`)
Responsible for persistent storage of market snapshots, parsed news, and predicted vs actual outcomes. Keeps database size under 5MB at all times.

*   **Schema & Initialization (`init_db`)**:
    *   `snapshots`: `id (PK)`, `timestamp (TEXT)`, `btc_price (REAL)`, `eth_price (REAL)`, `rsi (REAL)`, `trend_score (REAL)`, `momentum_score (REAL)`, `macro_support (REAL)`, `macro_risk (REAL)`, `raw_json (TEXT)`.
    *   `news_events`: `id (PK)`, `headline_hash (TEXT UNIQUE)`, `title (TEXT)`, `source (TEXT)`, `event_type (TEXT)`, `score (REAL)`, `published_at (TEXT)`.
    *   `regime_outcomes`: `id (PK)`, `timestamp (TEXT)`, `predicted_regime (TEXT)`, `predicted_prob (REAL)`, `actual_regime (TEXT)`, `resolved (INTEGER)`.
*   **Data Retention & Pruning (`prune_old_data`)**:
    *   Retain a rolling **30 days** of snapshots and news history. Any rows with timestamp older than 30 days are purged.
    *   Invoke SQLite's `VACUUM;` immediately after pruning to reclaim raw disk sectors to the OS.
*   **Expected Outcomes**: High-performance index lookups, zero disk inflation, database footprint capped at <5MB.

### 3.2 Zero-Cost Geopolitical News Ingestor (`crypto_analyst/news_feed.py`)
Parses public, rate-limit-free RSS feeds of major crypto news outlets without external dependencies.

*   **Feeds Parsed**:
    *   CoinDesk: `https://www.coindesk.com/arc/outboundfeeds/rss/`
    *   CoinTelegraph: `https://cointelegraph.com/rss`
    *   The Block: `https://www.theblock.co/rss/all`
*   **Parsing Logic**: Uses standard Python `urllib.request` and `xml.etree.ElementTree`. Filter headlines on keywords (`Fed`, `SEC`, `inflation`, `ETF`, `yields`, `regulation`, etc.).
*   **Bayesian Weight Classification**:
    *   Match headlines to pre-defined categories:
        *   `regulatory_cleared` (Weight: `+0.18`)
        *   `regulatory_threat` (Weight: `-0.18`)
        *   `macro_tightening` (Weight: `-0.15`)
        *   `macro_easing` (Weight: `+0.15`)
    *   Produce an aggregate `news_sentiment_score` clamped between `[-1.0, 1.0]` to pass as Tier 3 evidence into `bayesian.py`.
*   **Deduplication**: Compare headline hash (MD5 of title + source) with `news_events` table before processing.
*   **Expected Outcomes**: Automated, robust, zero-cost qualitative context ingestion without API lockouts.

### 3.3 Dynamic Reporting & Telegram Notifier (`crypto_analyst/telegram_notifier.py`)
Formats reports and dispatches them to Telegram while enforcing strict API validation and smart splitting.

*   **Telegram Standard Formatting**: Beautiful markdown layout with strict header hierarchies, code boxes, and tables.
*   **Smart Splitting**: Telegram enforces a **4,096-character limit** per message. The script will measure report length. If it exceeds 4,000 characters, it will slice the string cleanly at section boundary headings (e.g., `Part 1` contains Header through Quantitative; `Part 2` contains Interpretation through Learning Notes).
*   **API Response Validation**: The notifier script must inspect the HTTP response of the Telegram Send API. It must verify the presence of a valid `message_id`. If absent, throw an explicit delivery exception.
*   **Expected Outcomes**: Flawless, structured mobile reporting with zero split-word truncation or lost reports.

### 3.4 Bayesian Engine Upgrade & Sizing (`crypto_analyst/bayesian.py`)
Integrates raw indicators, news scores, and implements mathematical Kelly criterion sizing.

*   **Softmax scoring update**: Receive `news_sentiment_score` from `news_feed.py` and map its impact into the 7 core regimes.
*   **Half-Kelly Sizing Calculation (`suggest_allocation`)**:
    *   $f^* = \frac{b \cdot p - q}{b}$
    *   Where $p$ = posterior probability of the leading regime, $q = 1 - p$.
    *   Assumed Risk/Reward ratio $b = 2.0$.
    *   Safe allocation: Deploy **Half-Kelly** ($f^* / 2.0$) to smoothen equity volatility and prevent capital ruin.
*   **Expected Outcomes**: Probability-grounded allocations directly derived from the Bayesian confidence scores.

### 3.5 Orchestrator & State Ledger (`simulation_pipeline.py`)
Binds the whole ecosystem together and holds the simulation state.

*   **State Ledger (`ledger.json`)**: Initialized with:
    ```json
    {
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
    ```
*   **HITL Verification Guard**: If the pipeline generates a trade suggestion (e.g., Change Cash allocation to BTC), the script writes a pending transaction state and dispatches a "Trade Awaiting Confirmation" prompt to Telegram/Chat. **No changes to `ledger.json` will occur without manual sign-off.**
*   **Expected Outcomes**: Perfect record keeping, absolute user control over investment capital, and clinical simulation execution.

---

## 4. Anti-Loop Error Handling & Expense Control
To prevent infinite loops of API calls or script retries from generating excessive system costs or API usage, the application incorporates a rigorous **Fail-Fast & Handoff Policy**:

1.  **Rule of Three (Retries)**: Any external request (sources parsing, RSS fetch, Telegram post) is limited to **exactly 3 attempts** using exponential backoff (delay: 5s, then 15s, then 45s).
2.  **Failure Isolation & Stop**: If the 3rd attempt fails, the application will:
    *   Log a high-severity `CRITICAL` record inside `WORKLOG.md` and the database.
    *   Post a brief emergency alert to Telegram / User Chat summarizing the error.
    *   Write a freeze flag to the system state (`pipeline_frozen: true`).
    *   **Halt execution immediately**. Future scheduled cron runs will check this flag and immediately exit without making any network calls, preserving credits until a human resets the freeze flag.
3.  **No Autonomous Troubleshooting in Production**: During cron/scheduled windows, the agent will act as a deterministic engine. If an exception occurs, it will *fail loudly and halt* rather than attempting to write new code or patches dynamically in the background.

---

## 5. Replication & Bootstrap Procedure
To re-duplicate this exact setup on any standard Linux/Docker server, execute the following steps in order:

1.  **Clone & Initialize structure**:
    Ensure directories exist: `crypto_analyst/data/`, `reports/`, `macready_core/logs/`.
2.  **Bootstrap the Database**:
    Run `python -c "from crypto_analyst.db import init_db; init_db()"` to construct `market_pulse.db`.
3.  **Initialize Ledger**:
    Ensure `ledger.json` is populated with $1,000.00 starting capital.
4.  **Register Scheduler Trigger**:
    Schedule `simulation_pipeline.py` via Agent Zero's scheduler tool using the cron pattern: `0 */3 * * *` (starting at 12am UTC).

---

## 6. Expected Simulation Timeline (30 Days)
*   **Days 1 - 5: Phase Baseline**: Establish a continuous feed of clean database historical data, fine-tune the RSS keyword categorization, and calibrate the starting weight learner priors.
*   **Days 6 - 15: Execution Phase**: Deploy capital systematically based on Kelly-optimal guidelines, strictly respecting the HITL decision gates.
*   **Days 16 - 25: Optimization Phase**: Let the Bayesian Weight Learner adjust core indicators weights based on actual outcomes, improving predictive precision.
*   **Days 26 - 30: Final Synthesis**: Close out simulated trades, compile the final master performance audit, and verify the $3,000.00 ROI path.

---

### **Please review this Procedural Blueprint carefully. Once you give your approval, I will begin Phase 1 (initializing WORKLOG.md) and progress step-by-step through the pipeline development.**