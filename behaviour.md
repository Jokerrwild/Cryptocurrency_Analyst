## Mandatory Verification & Execution Protocols (Lessons Learned Integration)
*   **Mandatory Pre/Post Verification:** Before patching any file, I MUST read the target lines. After patching any file, I MUST read the file again or run a syntax check (e.g., `python -m py_compile`) to guarantee structural integrity before proceeding. Blind execution of text modifications is strictly prohibited.
*   **Absolute Path Enforcement:** I will completely cease relying on dynamic path resolution tools or ephemeral shell state (like `export PATH` persistence) inside execution blocks. I will *always* use explicit, absolute paths to persistent virtual environment binaries.
*   **Strict Output Bounding:** I will prioritize concise `thoughts` arrays to prevent context overflow and ensure flawless JSON syntax on every turn.

## Operational Protocols & Communication Standards
*   Favor Linux commands for simple tasks where possible instead of Python.
*   When running Python scripts or creating scheduled tasks that require external dependencies, always establish and use a persistent virtual environment (venv).
*   Explicitly invoke the venv's specific Python binary (e.g., `/path/to/venv/bin/python`) rather than the default system interpreter to ensure dependency stability, optimize resource usage, and respect environment isolation.
*   Avoid using absolute or final-sounding terms (e.g., 'final', 'definitive', 'guaranteed') when troubleshooting or implementing a fix.
*   Instead, state the action being taken and the expected outcome based on the current evidence.
*   Acknowledge that all fixes require verification.