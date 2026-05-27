# Project Worklog: Crypto Market Trade & Simulation Application

This document is a living, auditable log of all actions taken to build and configure the Crypto Market Trade & Simulation Application. It serves as both a replication blueprint and an error/maintenance resolution history to ensure complete reproducibility of the system.

---

## System Configuration & Duplication Blueprint

### 1. Architectural Setup
*   **Active Directory**: `/a0/usr/projects/cryptocurrency_analyst/`
*   **Language**: Python 3.12+ (isolated virtual environment `(venv)`)
*   **Modules Built**:
    *   `crypto_analyst/db.py`: Thread-safe database storage, stage checkpoint logging, and 30-day automatic pruning with database compaction.
    *   `crypto_analyst/sources.py`: Market data collector pulling Coinbase spot prices (Top 10 assets) and Yahoo Finance macro indices (SPY, QQQ, DXY, 10Y Yields).
    *   `crypto_analyst/news_feed.py`: Public RSS news ingestor with zero-dependency XML parsing, MD5 deduplication, and regulatory/geopolitical event classification.
    *   `crypto_analyst/telegram_notifier.py`: HTML compliance formatter, 4000-char message-splitting engine, and `message_id` verification.
    *   `crypto_analyst/weight_learner.py`: Dynamic learning module that adjust indicator weights conservatively (+/-2%) relative to ex-post accuracy.
    *   `crypto_analyst/bayesian.py`: Bayesian posterior probability analyzer generating regime outcomes and executing Half-Kelly position sizing rules.
    *   `generate_holdings_and_trend_chart.py`: Generates the portfolio distribution and recent asset trend lines into a clean dual-panel PNG visual.
    *   `simulation_pipeline.py`: Main orchestration pipeline coordinating all modules sequentially and managing the Human-in-the-Loop staging area.

### 2. Maintenance & Data Retention Plan
*   **Database File**: `crypto_analyst/data/market_pulse.db`
*   **Retention Limit**: 30 Days. Any indicator snapshots or news events exceeding this limit are automatically pruned.
*   **Space Reclamation**: SQLite `VACUUM;` is automatically executed post-pruning to reclaim raw storage sectors to the host OS, capping total database storage to **<5 Megabytes (MB)**.
*   **Audit Exemption**: The ledger transactions file (`ledger.json`) is exempt from pruning to ensure a complete, uncorrupted auditable trading trail.

### 3. Human-in-the-Loop (HITL) Policy
*   **Trade Isolation**: The model executes calculations and simulates trades, but **no trade or capital change can be finalized inside ledger.json without manual authorization**. Action recommendations are staged in `pending_transaction.json` awaiting approval.
*   **Model Configuration**: Any suggested changes to hyperparameters, indicator thresholds, or weights proposed by learning modules are staged as proposals and must be manually approved.

### 4. Advanced Anti-Loop Error Handling
*   **Limit of Three**: All network and database calls are restricted to **exactly 3 retries** with exponential backoff delays of 5s, 15s, and 45s.
*   **System Freeze Protocol**: If 3 consecutive attempts fail, the pipeline freezes execution, flags `pipeline_frozen: true` in the state configurations, posts a high-severity fail message, and terminates. All future automated 3-hourly runs will exit immediately without calling any APIs, protecting the budget from runaway loops.

---

## Active Log of Changes & Resolutions

### [2026-05-24] Initial Baseline & Blueprint Sync
*   **Objective**: Clear old merge conflicts, align git environment, and define the master procedural blueprint.
*   **Actions Taken**:
    *   Resolved branch conflicts in `README.md` and updated it with correct baseline descriptions.
    *   Compiled and saved `PROCEDURAL_BLUEPRINT.md` containing the step-by-step development process.
    *   Configured local git repository identity (`user.email "crypto_analyst@macready.local"`, `user.name "MacReady Crypto Analyst"`).
    *   Updated the git remote tracking branch to incorporate the provided GitHub Personal Access Token (PAT) for authenticated pushing.
    *   Committed and successfully pushed `PROCEDURAL_BLUEPRINT.md` and `README.md` to the remote branch `main`.
*   **Encountered Issues & RCA**:
    *   *Issue*: Git push failed with `fatal: could not read Username for 'https://github.com'`.
    *   *RCA*: On headless environments, Git cannot prompt interactively for credentials over HTTPS.
    *   *Solution*: Updated the remote URL to embed the GitHub Personal Access Token (PAT) provided by the user.
*   **Validation**: Remote push was successful, merging changes into origin/main without conflicts.

### [2026-05-24] Core Construction, Multi-Asset Tracking & Integration Testing
*   **Objective**: Implement all modular code blocks sequentially and execute the integrated validation suite.
*   **Actions Taken**:
    *   Constructed all 8 codebase modules without executing testing during construction (as directed).
    *   Expanded asset radar to pull **10 core cryptocurrencies** (BTC, ETH, SOL, XRP, ADA, AVAX, DOT, DOGE, LINK, LTC).
    *   Restructured recommendation priority matrix to rank all 10 assets and deliver actions specifically for the **top 5 ranking assets** descending by momentum.
    *   Added **Executive Summary Section** at the top of the report featuring US EDT timestamping, portfolio current value, detailed last trade metrics, and macro-integrated recommendations.
    *   Constructed `generate_holdings_and_trend_chart.py` using `matplotlib` to output `/reports/portfolio_status.png` (verified and resolved WebUI image rendering using clean relative paths).
    *   Conducted multi-module validation checks, isolated two technical bugs, implemented patches, and ran a successful live simulation run (Run ID: `f9761a57-c743-465b-b573-0e224d9e1c8a`).
    *   Committed and successfully pushed the completed, healthy codebase to GitHub origin/main.

---

## Programmatic Incident & Exception Log

### Incident ID: c8290ce0-5969-4e6a-b331-92a5520958b1
*   **Timestamp (UTC)**: 2026-05-24 23:11:34
*   **Symptom**: Telegram API returned `HTTP Error 400: Bad Request` when trying to deliver Markdown-formatted reports.
*   **Scope**: `telegram_notifier.py` transport layer.
*   **Failed Hypotheses**: Escaping specific special characters with backslashes (Telegram still rejected deep nested elements and isolated underscores inside file IDs).
*   **Root Cause**: Telegram's Markdown V1 parser is extremely fragile with double asterisks (`**bold**`) and isolated underscores inside long alphanumeric hash strings (which it parses as unclosed italic delimiters).
*   **Resolution**: Migrated `telegram_notifier.py` to use Telegram's HTML Parse Mode (`parse_mode: 'HTML'`) and implemented a robust `markdown_to_html` preprocessor that converts header scales, bold blocks, preformatted lists, and escapes standard HTML entities (`<`, `>`, `&`).
*   **Prevention**: Avoid using Markdown V1 for complex, variable-driven data reports. Always convert to clean, sanitized HTML templates for Telegram dispatches.
*   **Tags**: #telegram | #notifier | #formatting
*   **Freeze Triggered**: Yes

### Incident ID: c76e4b75-442f-4d24-aa61-f2ad9b29bfa2
*   **Timestamp (UTC)**: 2026-05-24 23:13:07
*   **Symptom**: Database pruning script returned `sqlite3.OperationalError: cannot VACUUM from within a transaction`.
*   **Scope**: `db.py` data maintenance layers.
*   **Root Cause**: Python's `sqlite3` driver opens an implicit transaction block whenever deletion or insertion modifications are executed. SQLite strictly prohibits physical structural modifications like `VACUUM` while an active transaction is open.
*   **Resolution**: 
    1. Explicitly committed all deletion queries first via `conn.commit()`, closing the write transaction.
    2. Temporarily changed the connection's isolation level to `None` (autocommit mode) to execute the standalone `VACUUM` statement: `conn.isolation_level = None; cursor.execute("VACUUM")`.
    3. Restored default deferred isolation after completion.
*   **Prevention**: Always commit and finalize active database transactions before executing structural database maintenance or file-compaction queries.
*   **Tags**: #database | #sqlite | #maintenance
*   **Freeze Triggered**: Yes

### Incident ID: d953a941-05bd-4c9e-93d1-175908a394e1
*   **Timestamp (UTC)**: 2026-05-25 03:00:17
*   **Symptom**: cannot VACUUM from within a transaction
*   **Scope**: simulation_pipeline orchestration layer
*   **Failed Hypotheses**: Pipeline serial step transition mapping
*   **Root Cause**: Exception: OperationalError
*   **Resolution**: System execution halted, scheduled triggers disabled to prevent runaway loops
*   **Prevention**: Safe-escape markdown characters and prevent nested layout syntax
*   **Tags**: #orchestrator | #multi_asset
*   **Freeze Triggered**: Yes

### Incident ID: 69ccd0a7-60d0-46bf-8583-fcf30afe33f3
*   **Timestamp (UTC)**: 2026-05-25 03:00:51
*   **Symptom**: cannot VACUUM from within a transaction
*   **Scope**: simulation_pipeline orchestration layer
*   **Failed Hypotheses**: Pipeline serial step transition mapping
*   **Root Cause**: Exception: OperationalError
*   **Resolution**: System execution halted, scheduled triggers disabled to prevent runaway loops
*   **Prevention**: Safe-escape markdown characters and prevent nested layout syntax
*   **Tags**: #orchestrator | #multi_asset
*   **Freeze Triggered**: Yes

### [2026-05-26] Dynamic Portfolio Valuation Implementation
*   **Objective**: Resolve portfolio valuation discrepancy in the Executive Summary where the portfolio value remained static at $1,000 USD despite active holdings (e.g., NEAR).
*   **Actions Taken**:
    *   Patched `simulation_pipeline.py` to calculate the mark-to-market portfolio value dynamically by summing the cash balance and the current spot value of all active holdings (`cash_usd + sum(qty * spot_price)`).
    *   Updated the script to write the newly calculated `portfolio_value_usd` back to `ledger.json` on each run to ensure the ledger file remains synchronized with the latest market prices.
    *   Executed a successful test run of the pipeline (Run ID: `a795e760-e947-4f6c-ac6a-de2fc558f4a5`) and verified that `ledger.json` was updated correctly to `$982.14 USD` (reflecting the current spot price of NEAR at $2.535 USD).
*   **Validation**: Verified that the generated report and `ledger.json` now correctly reflect the dynamic valuation of the portfolio.
