from datetime import datetime
from pathlib import Path

def write_heartbeat(path: str = "state/heartbeat.txt"):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(datetime.utcnow().isoformat())
