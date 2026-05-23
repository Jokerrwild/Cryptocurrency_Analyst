# Error Handling Protocol

- When a system warning or traceback occurs, do not display the full error message to the user.
- Summarize the error concisely (e.g., 'ValueError in memory system', 'API connection timeout').
- State the error type and the component affected.
- Proceed with the assigned task if possible, otherwise, initiate a Root Cause Analysis as per SOP.