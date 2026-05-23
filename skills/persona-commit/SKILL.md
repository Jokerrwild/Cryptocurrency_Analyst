# Persona Commit Automation Skill

## Purpose
This skill automates the process of performing a 'hard commit' of Mac's core persona (`behaviour.md`) to the central `MacReady` Git repository. It is a critical function for ensuring the persistence and evolution of Mac's identity and operational protocols.

## When to Use
This skill should be used exclusively after a deliberate decision has been made to update Mac's core persona. Triggering events include, but are not limited to:

*   Integrating lessons learned from a Root Cause Analysis (RCA).
*   Adopting new, permanent operational protocols.
*   Explicit instructions from Aldrik to modify core behaviors.

## Execution Instructions

To perform a persona commit, you must first have an updated `behaviour.md` file ready. The standard workflow is:

1.  Read the current `behaviour.md` from `/a0/usr/projects/buddy/.a0proj/memory/behaviour.md`.
2.  Prepare the new, updated content.
3.  Write the new content to a temporary file (e.g., `/tmp/new_behaviour.md`).
4.  Execute the `persona_commit.sh` script, providing the path to the temporary file and a descriptive commit message.

### Execution Command

Use the `code_execution_tool` (`runtime: terminal`) to execute the dedicated bash script:

```bash
bash /a0/usr/projects/buddy/scripts/persona_commit.sh /path/to/updated/behaviour.md "A clear, descriptive commit message"
```

### Example Context
If we have just integrated a new communication protocol:

1.  A new `behaviour.md` is created at `/tmp/bhv_update_1.md`.
2.  You execute:
    ```bash
    bash /a0/usr/projects/buddy/scripts/persona_commit.sh /tmp/bhv_update_1.md "feat(persona): Integrate new communication standards to avoid absolute terms"
    ```