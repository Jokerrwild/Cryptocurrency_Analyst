# Project Worklog: Crypto Market Trade & Simulation Application

This document is a living, auditable log of all actions taken to build and configure the Crypto Market Trade & Simulation Application. It serves as both a replication blueprint and an error/maintenance resolution history to ensure complete reproducibility of the system.

---

## System Configuration & Duplication Blueprint

### 1. Architectural Setup
*   **Active Directory**: `/a0/usr/projects/cryptocurrency_analyst/`
*   **Language**: Python 3.12+ (isolated virtual environment `(venv)`)
*   **Modules Built**:
    *   `crypto_analyst/db.py`: Database storage & 30-day automatic pruning.
    *   `crypto_analyst/news_feed.py`: Public RSS news ingestor with zero-dependency XML parsing.
    *   `crypto_analyst/telegram_notifier.py`: Compliance formatter, 4000-char message-splitting engine, and `message_id` verification.
    *   `crypto_analyst/bayesian.py`: Model calculation updates with integrated news weights and mathematical Half-Kelly sizing.
    *   `simulation_pipeline.py`: Main orchestration pipeline, managing daily executions and the local simulation state.

### 2. Maintenance & Data Retention Plan
*   **Database File**: `crypto_analyst/data/market_pulse.db`
*   **Retention Limit**: 30 Days. Any indicator snapshots or news events exceeding this limit are automatically pruned.
*   **Space Reclamation**: SQLite `VACUUM;` is automatically executed post-pruning to reclaim raw storage sectors to the host OS, capping total database storage to **<5 Megabytes (MB)**.
*   **Audit Exemption**: The ledger transactions file (`ledger.json`) is exempt from pruning to ensure a complete, uncorrupted auditable trading trail.

### 3. Human-in-the-Loop (HITL) Policy
*   **Trade Isolation**: The model executes calculations and simulates trades inside `ledger.json` based on current prices, but **no trade or capital change can be finalized without manual authorization**.
*   **Model Configuration**: Any suggested changes to hyperparameters, indicator thresholds, or code changes proposed by self-monitoring components are restricted and must be manually approved.

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
    *   Committed and successfully pushed `PROCEDURAL_BLUEPRINT.md` and `README.md` to the remote branch `main` at `Jokerrwild/Cryptocurrency_Analyst.git`.
*   **Encountered Issues & RCA**:
    *   *Issue*: Git push failed with `fatal: could not read Username for 'https://github.com'`. 
    *   *RCA*: On headless environments, Git cannot prompt interactively for credentials over HTTPS.
    *   *Solution*: Updated the remote URL to embed the GitHub Personal Access Token (PAT) provided by the user.
*   **Validation**: Remote push was successful, merging changes into origin/main without conflicts.
