import os
import uuid
from datetime import datetime

WORKLOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "WORKLOG.md")

def log_incident_or_event(
    symptom: str,
    scope: str,
    failed_hypotheses: str = "None",
    root_cause: str = "N/A",
    resolution: str = "N/A",
    prevention: str = "N/A",
    tags: str = "#system",
    freeze_triggered: bool = False
) -> str:
    """
    Programmatically appends a highly structured, audit-grade incident log to WORKLOG.md.
    Returns the generated unique Incident UUID string.
    """
    incident_id = str(uuid.uuid4())
    timestamp_utc = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    freeze_str = "Yes" if freeze_triggered else "No"
    
    entry_block = f"""
### Incident ID: {incident_id}
*   **Timestamp (UTC)**: {timestamp_utc}
*   **Symptom**: {symptom.strip()}
*   **Scope**: {scope.strip()}
*   **Failed Hypotheses**: {failed_hypotheses.strip()}
*   **Root Cause**: {root_cause.strip()}
*   **Resolution**: {resolution.strip()}
*   **Prevention**: {prevention.strip()}
*   **Tags**: {tags.strip()}
*   **Freeze Triggered**: {freeze_str}
"""
    
    # Ensure file ends in a newline before appending to keep it readable
    has_newline = True
    if os.path.exists(WORKLOG_PATH):
        try:
            with open(WORKLOG_PATH, "rb") as f:
                f.seek(-1, os.SEEK_END)
                last_char = f.read(1)
                has_newline = (last_char == b'\n')
        except Exception:
            pass
            
    with open(WORKLOG_PATH, "a", encoding="utf-8") as f:
        if not has_newline:
            f.write("\n")
        f.write(entry_block)
        
    return incident_id
