---
name: perform-ledger-commit
description: Sync and commit the active state ledger file (ledger.json) to the remote GitHub repository whenever the user says "perform a ledger commit".
---

# Perform Ledger Commit

This skill provides the procedural sequence for committing and synchronizing the simulation's asset ledger (`ledger.json`) with the remote GitHub repository. This serves as an auditable trail and disaster recovery backup for the current portfolio allocation.

## When to Use
Trigger this workflow immediately whenever the user says **"perform a ledger commit"** or explicitly asks to synchronize, back up, or push the simulation ledger to GitHub.

## Core Steps

### 1. Validate local file integrity
Prior to committing, read `/a0/usr/projects/cryptocurrency_analyst/ledger.json` and ensure it is parseable and valid JSON. If the file is missing or corrupted, fail fast and do not commit a corrupt state.

### 2. Check Git status
Check if there are modified or untracked changes on `ledger.json` using the local command:
```bash
git status ledger.json
```
If there are no changes to the file, notify the user that the ledger is already fully up to date and synchronized with remote.

### 3. Stage, Commit and Push
If modifications exist, execute the Git synchronization sequence directly inside `/a0/usr/projects/cryptocurrency_analyst/`:
```bash
git add ledger.json
git commit -m "trade: synchronize simulation ledger state"
git push
```

### 4. Verification
Verify that the remote push was completed successfully and report the new commit hash and portfolio valuation from the ledger directly to the user.
