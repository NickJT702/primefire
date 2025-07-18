from sqlalchemy import create_engine, text
import os

_engine = None

def get_engine():
    global _engine
    if _engine is None:
        url = os.getenv("PF_DB_URL", "sqlite:///primefire.db")
        _engine = create_engine(url, future=True)
    return _engine

def init_db():
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            symbol TEXT,
            side TEXT,
            quantity REAL,
            price REAL,
            reason TEXT,
            pnl_pct REAL,
            equity REAL
        );
        """))
        conn.commit()
