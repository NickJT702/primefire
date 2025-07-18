from datetime import datetime, timedelta
from pathlib import Path

def stale_heartbeat(path: str = "state/heartbeat.txt", max_age_sec: int = 120) -> bool:
    p = Path(path)
    if not p.exists():
        return True
    ts = datetime.fromisoformat(p.read_text().strip())
    return (datetime.utcnow() - ts) > timedelta(seconds=max_age_sec)
