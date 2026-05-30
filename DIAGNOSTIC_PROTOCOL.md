# Root-Cause Analysis (RCA) and Troubleshooting Protocol

This document defines the strict, non-negotiable diagnostic protocol that must be followed by any automated quantitative agent to ensure absolute analytical rigor, prevent projection errors, eliminate confirmation bias, and verify root causes with primary empirical evidence before reporting.

## 1. The Core Failure Modes to Mitigate
Any troubleshooting process must actively guard against three primary failure modes:
* **Confirmation Bias**: Accepting a logical-sounding theory (e.g., outdated model names or API deprecations) without testing if it is the active cause of the current failure.
* **Projection/Isolation Failure**: Observing an error or warning in the manual terminal session (the active chat container) and falsely assuming it exists inside the background daemon's environment (Gunicorn/Uvicorn runtime).
* **The Narrative Trap**: Writing highly elaborate logical stories explaining why something failed rather than designing and executing physical, reproducible tests first.

## 2. The Four-Step Diagnostic Pipeline
Whenever a system failure, missed run, or anomalous state is detected, the agent **must** execute this pipeline in strict sequence:

```text
[ HYPOTHESIS ] ---> [ STRATIFICATION ] ---> [ FALSIFICATION ] ---> [ VERIFICATION ]
```

### Step 2.1: Hypothesis Formulation
* Formulate a clear, specific, and bounded hypothesis. 
* *Example*: "The background task failed because of an API rate-limit timeout on Coinbase."

### Step 2.2: Environment Stratification
* Explicitly separate the runtimes and determine which one is affected:
  * **Manual Session Environment** (the interactive container/shell).
  * **Background Daemon Environment** (the `/opt/venv-a0` Uvicorn orchestrator).
  * **Script Execution Environment** (the modular pipeline python scripts).
* Never assume code behavior in one environment matches another without a dedicated test.

### Step 2.3: Empirical Falsification (Disprove the Hypothesis First)
* The agent must design and execute a direct, manual terminal command or script inside the target environment to try to **disprove** the hypothesis.
* If the test completes successfully without the assumed error, the hypothesis is **rejected instantly**.
* *Example*: To test if a dependency is missing, run `/opt/venv-a0/bin/python -c "import <module>"`. If it imports with no error, the hypothesis is false. Discard it and start over.

### Step 2.4: Primary Source Verification
* Do not declare an RCA as correct unless it is backed by one of the following **primary source artifacts**:
  1. A verbatim, unedited traceback log from the active service stderr.
  2. A physical change in state variables inside persistent configuration files (e.g., `chat.json` or `tasks.json` timestamps/values).
  3. A direct database record discrepancy (e.g., `pipeline_runs` gaps).
* If logs are physically inaccessible, the agent must explicitly state:
  > *"I do not have access to the raw stderr logs of the background daemon, so the following is a hypothesis. Here is the empirical test we will use to verify or reject it: [...]"*

## 3. The Baseline Constraint Checklist
Before debugging complex logical loops, the agent must systematically audit these baseline constraints:
1. **State & Iteration Limits**: Check the `iteration_no` parameter inside the background's `chat.json` file. If it has reached the framework safety limit, the task will be silently skipped during initialization.
2. **Concurrency & File Locks**: Check for stale `.lock` files or tasks stuck in the `running` state in `tasks.json`.
3. **Schedules & Timezones**: Verify that UTC-to-local shifts align across the system cron daemon, Python localization, and the framework scheduler.
4. **Data Endpoints**: Verify that CoinGecko and Coinbase API endpoints are active and returning expected structures by executing dry-run curl requests.
