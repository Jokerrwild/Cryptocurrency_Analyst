# Master Procedural Blueprint: Crypto Market Trade & Simulation Application

**Author**: Senior Cryptocurrency Market & Macro-Statistical Analyst  
**Version**: 1.1.0  
**Date**: May 2026  
**Target Environment**: Agent Zero / Debian Linux VPS / Docker (Python 3.12+)  

---

## 1. Executive Summary & Core Objective

### Core Objective
"The objective of this application is to produce disciplined, repeatable, probability-based market analysis and maintain an auditable simulated investment ledger under strict Human-in-the-Loop approval. The system is not permitted to optimize toward a fixed profit target or alter its behavior to chase a portfolio outcome."

### System Nature
The application is built as a **probabilistic market analysis and simulation engine**, not a profit-seeking optimizer. Its job is to collect evidence, score regimes, generate risk-aware recommendations, and preserve a faithful simulation ledger under strict Human-in-the-Loop (HITL) control.

### Temporal Alignment
Use UTC (Coordinated Universal Time) exclusively for all scheduler triggers, database timestamps, report timestamps, worklog timestamps, and ledger events. Local display time conversion is only permitted in user-facing delivery if explicitly requested.

---

## 2. System Architecture & Modular Topology

The application consists of the following explicit modules. No behavior may be inferred loosely or self-modified:

*   **`simulation_pipeline.py`**: The sole orchestrator of the scheduled runs. Coordinates all other modules sequentially and manages checkpoint persistence.
*   **`sources.py`**: Handles raw crypto spot price ingestion (Coinbase or equivalent) and macroeconomic indices (Yahoo Finance or equivalent for SPY, QQQ, DXY, 10Y yields).
*   **`news_feed.py`**: Ingests public RSS feeds from CoinDesk, CoinTelegraph, and The Block. Performs XML parsing, keyword-based classification, hash-based deduplication, and scores interval news sentiment.
*   **`bayesian.py`**: Evaluates technical and macro signals, computes posterior probability distributions across 7 core market regimes, assigns confidence labels, and generates position-sizing suggestions.
*   **`weight_learner.py`**: Dedicated learning module. Records predictions, resolves outcomes relative to actual market structures, and updates learned weights conservatively over time.
*   **`db.py`**: Coordinates database schemas, execution inserts, data retrieval, 30-day automatic pruning, and checkpoint/delivery audit persistence.
*   **`telegram_notifier.py`**: Formats the report schema, manages clean section-boundary splitting for message size compliance, and handles message dispatch and validation.
*   **`worklog_util.py`**: Standardized utility layer for programmatically updating the persistent `WORKLOG.md` on system events or errors.

---

## 3. Mandatory Persistence & Database Schema

The SQLite database `market_pulse.db` will enforce the following strict tables:

1.  **`snapshots`**: Stores raw interval market state indicators (timestamp, ticker spot prices, RSI, trend/momentum metrics, volume indicators, raw macro inputs).
2.  **`news_events`**: Stores unique cryptographic MD5 hashes of parsed headlines, source labels, classifications, and individual sentiment scores for deduplication.
3.  **`regime_outcomes`**: Records predicted regime profiles, probability weights, and actual resolved market regimes for weight calibration.
4.  **`weight_priors`**: Maintains the persistent states of learned regime-feature weights, means, and mathematical uncertainty bands.
5.  **`delivery_audit`**: Logs each Telegram transmission attempt, HTTP response code, response body hash, and the successfully confirmed `message_id` on delivery completion.
6.  **`pipeline_runs`** (or `checkpoint_events`): Implements stage-by-stage boundary checkpoint observability for each scheduled execution (fired, fetched, computed, completed, sent).
7.  **`system_state`**: Stores persistent freeze-state settings (e.g. `pipeline_frozen: true`) ensuring it survives process restarts and stops further network operations on failure.

---

## 4. Operational Control & Risk Guardrails

*   **Human-In-The-Loop (HITL) Control**: No trade, allocation change, ledger mutation, or transaction commit may occur in `ledger.json` without explicit, validated human approval. Recommendations may be rendered and staged in the DB or Telegram, but the ledger remains unchanged until sign-off is committed.
*   **Kelly Sizing Limitations**: Full Kelly sizing is strictly prohibited. The system must utilize **Half-Kelly sizing only**, bounded by absolute safety limits (default: max 25% single-asset exposure, 0% below the conviction threshold).
*   **Minimum Conviction Threshold**: If the leading regime's posterior probability is below **55%** (action threshold), the system defaults to a **HOLD** recommendation, regardless of whether that regime technically leads the table.
*   **News Scoring Boundaries**: Qualitative news scores are supportive evidence only. They may adjust regime scoring weights, but they are not permitted to dominate price and macro-economic trends.
*   **Volume Confirmation**: Crypto-native volume indicators must remain part of the core technical trend verification path. Unconfirmed price breakouts on low relative volume must weaken the resulting bullish regime weights.
*   **Simulation-First Execution**: The system is simulation-first. It recommends, simulates, and records, but does not execute real asset trades.

---

## 5. Strict Reporting & Telegram splitting

### Verbatim Reporting Rule
"Every scheduled run must generate the same report schema in the same order: Header, Market Thesis, Probability Table, Quantitative Evidence, Qualitative Evidence, Interpretation, Invalidation Conditions, Risk-Aware Decision Support, What To Monitor Next, Learning Notes."

*   **Tone**: Strict probabilistic, objective, and quantitative tone. Deterministic buy/sell language is prohibited.
*   **Sizing**: Suggested trade adjustments must be clearly presented as proposed recommendations awaiting human signature.
*   **Smart Splitting**: If a message exceeds 4,000 characters, it must split **only at section headers**. Splitting mid-table, mid-bullet, or inside code blocks is strictly prohibited.

---

## 6. Implementation & Adaptive Weighting Rules

### Verbatim Adaptive Weighting Rule
"Adaptive weighting requires a dedicated `weight_learner.py` module and persistent `weight_priors` storage. Adaptive learning must be conservative in early cycles and must never bypass volume confirmation or other existing invalidation safeguards."

### Verbatim Diagnostics Rule
"Every scheduled run must persist checkpoint status for each pipeline boundary. Delivery is not considered successful unless Telegram returns a valid `message_id` and that value is recorded in persistence."

### Scheduled Execution Behavior
Scheduled runs must only execute the defined sequential pipeline steps. They are strictly prohibited from self-modifying code, patching source modules, or attempting autonomous error remediation. On any failure, the application must **fail loudly, log, write `pipeline_frozen: true` to the state, notify the user, and immediately stop.**

---

## 7. Programmatic `WORKLOG.md` Schema

To ensure auditability, any logged entries (especially incidents and fixes) must be appended according to this strict format:

```markdown
### Incident ID: <UUID>
*   **Timestamp (UTC)**: YYYY-MM-DD HH:MM:SS
*   **Symptom**: Precise error traceback or system behavioral anomaly.
*   **Scope**: Affected modules, tables, or integration boundaries.
*   **Failed Hypotheses**: Paths investigated that did not resolve the issue.
*   **Root Cause**: Underlying trigger of the failure.
*   **Resolution**: Exact code modification or configuration change applied.
*   **Prevention**: Architectural safeguards implemented to prevent regression.
*   **Tags**: #database | #network | #math
*   **Freeze Triggered**: Yes/No
```