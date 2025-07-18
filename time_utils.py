from datetime import datetime

def to_session_date(ts: datetime) -> str:
    return ts.strftime("%Y-%m-%d")
