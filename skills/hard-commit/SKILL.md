---
name: "hard-commit"
description: "Automates the Git commit process for the cryptocurrency_analyst project, bypassing gitignores and setting identity."
version: "1.0.0"
author: "Agent Zero"
tags: ["git", "version-control", "commit", "automation"]
trigger_patterns:
  - "hard commit"
  - "commit project"
  - "save to git"
  - "push changes"
  - "commit changes"
---

# Hard Commit Automation Skill

## Purpose
This skill automates the process of saving the `cryptocurrency_analyst` project state to the Git repository. It bypasses the global `.gitignore` (which normally ignores `/a0/usr/projects`), automatically configures the necessary Git identity for the container environment, and executes the commit in a single, efficient step.

## When to Use
Activate this skill whenever the user asks to perform a "hard commit", save the project, or commit changes to Git.

## Execution Instructions

When triggered, do **not** manually run individual `git add`, `git config`, or `git commit` commands. 

Instead, immediately use the `code_execution_tool` (with `runtime: terminal`) to execute the dedicated bash script:

```bash
bash /a0/usr/projects/cryptocurrency_analyst/scripts/hard_commit.sh "[Optional commit message based on user context]"
```

### Example Context
If the user says: *"Hard commit the new skill we just added."*

You execute:
```bash
bash /a0/usr/projects/cryptocurrency_analyst/scripts/hard_commit.sh "Add hard-commit skill and update guidelines"
```

If the user does not provide context for a message, you can omit the message argument, and the script will use its default message.
