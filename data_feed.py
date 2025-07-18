import pandas as pd
import time
from datetime import datetime
from pathlib import Path
import random
from typing import Iterable, List

class CSVFeed:
    def __init__(self, path: str, symbol: str):
        self.df = pd.read_csv(path, parse_dates=["timestamp"])
        self.symbol = symbol
        self.pointer = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.pointer >= len(self.df):
            raise StopIteration
        row = self.df.iloc[self.pointer]
        self.pointer += 1
        return {
            "timestamp": row["timestamp"],
            "symbol": self.symbol,
            "open": row["open"],
            "high": row["high"],
            "low": row["low"],
            "close": row["close"],
            "volume": row.get("volume", 0),
        }

class LivePollingFeed:
    """
    Stub polling feed. Replace with real broker or market data API.
    """
    def __init__(self, symbols: List[str], interval_seconds: int = 15):
        self.symbols = symbols
        self.interval_seconds = interval_seconds

    def fetch(self) -> Iterable[dict]:
        # Simulated random-walk close price for demonstration
        now = datetime.utcnow()
        for s in self.symbols:
            price = 500 + random.uniform(-2, 2)
            yield {
                "timestamp": now,
                "symbol": s,
                "open": price,
                "high": price * (1 + random.uniform(0, 0.001)),
                "low": price * (1 - random.uniform(0, 0.001)),
                "close": price,
                "volume": random.randint(10_000, 50_000),
            }
