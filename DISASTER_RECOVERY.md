# Disaster Recovery & Restoration Procedure

**Author**: Senior Cryptocurrency Market & Macro-Statistical Analyst  
**Version**: 1.0.1  
**Date**: May 2026  
**Scope**: Crypto Market Trade & Simulation Application  

---

## 1. Overview & Objectives

This manual outlines the step-by-step procedure required to recover and restore the **Crypto Market Trade & Simulation Application** from a catastrophic failure (e.g., VPS crash, cloud provider termination, database corruption, or local file deletion). 

By following these instructions, any qualified systems administrator or AI agent can reconstruct the application, restore the transaction history, and resume background scheduled runs within **under 10 minutes**.

---

## 2. Disaster Scenarios & Mitigation

| Disaster Event | Impacted Files | Recovery Time Objective (RTO) | Mitigation Action |
| :--- | :--- | :---: | :--- |
| **VPS Host Termination** | Local DB, local files. | <10 Minutes | Clone remote Git mirror; re-seed local secrets; launch scheduler. |
| **Database File Corruption** | `market_pulse.db` | <2 Minutes | Delete corrupt `.db` file; run pipeline to auto-initialize clean schemas. |
| **Ledger Accidental Deletion** | `ledger.json` | <3 Minutes | Pull the latest transaction state directly from remote Git. |
| **Runaway Failure / Freeze** | Execution halt. | <1 Minute | Inspect `WORKLOG.md` incident; clear issue; write `pipeline_frozen = False` in DB. |

---

## 3. Pre-Requisites for Restoration

Before initiating restoration, ensure you have the following credentials and tools:
1.  **Git Access**: The project URL (e.g., `https://github.com/Jokerrwild/Cryptocurrency_Analyst.git`).
2.  **GitHub PAT**: Your personal access token (e.g., `ghp_...`).
3.  **Telegram Bot Credentials**: 
    *   Bot Token (e.g., `TELEGRAM_BOT_TOKEN`)
    *   Chat ID (e.g., `TELEGRAM_CHAT_ID`)
4.  **Runtime**: Python 3.12+ in a Linux (Debian/Ubuntu/Kali) virtualenv.

---

## 4. Step-by-Step Restoration Sequence

### **Step 1: Clone the Application Repository**
On your fresh host or VPS, open a terminal, navigate to your active projects root, and clone the repository. Use your personal access token (PAT) to authorize the headless operation:
```bash
cd /a0/usr/projects/
git clone https://<YOUR_GITHUB_PAT>@github.com/Jokerrwild/Cryptocurrency_Analyst.git cryptocurrency_analyst
cd cryptocurrency_analyst
```

### **Step 2: Activate Virtual Environment & Install Dependencies**
Initialize the isolated Python virtual environment and verify dependency requirements:
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install matplotlib
```
*(Note: All other modules use standard zero-dependency libraries: urllib, sqlite3, xml, json, datetime, ssl)*

### **Step 3: Restore Local Environment Secrets**
Create the project-scoped local secrets files. **These files are excluded from Git tracking for security and must be written manually**:
1.  Create `/a0/usr/projects/cryptocurrency_analyst/.a0proj/secrets.env`
2.  Write the following lines into the file (replacing placeholders with your active tokens):
    ```env
    GITHUB_PAT=<YOUR_GITHUB_PAT>
    TELEGRAM_BOT_TOKEN=<YOUR_TELEGRAM_BOT_TOKEN>
    TELEGRAM_CHAT_ID=<YOUR_TELEGRAM_CHAT_ID>
    ```
3.  *(Optional Mirror)* Create identical variables inside `/a0/usr/projects/cryptocurrency_analyst/mac_os/configs/projects/crptocurrency_analyst/secrets.env`.

### **Step 4: Re-Compile and Initialize Database Tables**
Run a quick Python command to re-compile the local SQLite file structures and seed the default indicator weighting tables:
```bash
python -c "from crypto_analyst.db import init_db; init_db()"
```
*This will create `crypto_analyst/data/market_pulse.db` containing all 7 blank tables.*

### **Step 5: Restore Ledger State**
Your current ledger status (`ledger.json`) is tracked directly on your remote repository. Cloning in **Step 1** has already restored your exact historical transaction ledger, cash USD balance, and holding balances. Verify the file is active on disk:
```bash
cat ledger.json
```

### **Step 6: Execute a Manual Dry-Run Verification**
Run the orchestration pipeline manually once to ensure that all networks, feeds, data ingestion queries, database writes, and Telegram delivery configurations are operating correctly:
```bash
python simulation_pipeline.py
```
*   Check that your Telegram bot successfully receives the compiled 10-section report.
*   Verify that `reports/portfolio_status.png` was successfully generated.
*   Check that a temporary staging transaction is saved to `pending_transaction.json`.

### **Step 7: Re-Schedule the Background Loop**
Once the dry-run is complete, re-register the background loop within the scheduling daemon using the Agent Zero scheduler tool or system crontab to execute every 3 hours:
*   **Command**: `python simulation_pipeline.py`
*   **Schedule**: `0 */3 * * *` (Runs on minute 0 of every 3rd hour UTC)
*   **Timezone**: `UTC`

---

## 5. Post-Recovery Checklist

- [ ] Git branch clean and tracking `origin/main`?
- [ ] `market_pulse.db` successfully initialized with 7 tables?
- [ ] `ledger.json` present with starting cash/history?
- [ ] Manual execution of `simulation_pipeline.py` returned success?
- [ ] Telegram report received on your Bot (Message ID validated)?
- [ ] `reports/portfolio_status.png` generated and visible in WebUI?
- [ ] Scheduler task successfully registered?

**Restoration Complete. System is active.**
