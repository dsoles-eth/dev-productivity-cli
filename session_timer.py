import datetime
import os

def start_session(project_name=""):
    """Start a new session record."""
    start_time = datetime.datetime.now()
    record = {
        "project": project_name,
        "start_time": start_time.isoformat(),
        "status": "active"
    }
    return record

def parse_shell_history(lines):
    """Parse shell history lines."""
    if not lines:
        return []
    
    parsed = []
    for line in lines:
        if line and line.strip():
            parsed.append(line.strip())
    return parsed