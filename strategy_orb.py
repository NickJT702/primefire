from datetime import timedelta
from primefire.config.schema import Signal
from primefire.utils.time_utils import to_session_date
from primefire.utils.logging_setup import get_logger
from dataclasses import dataclass
from datetime import datetime

log = get_logger("strategy_orb")

@dataclass
class ORBState:
    range_high: float | None = None
    range_low: float | None = None
    locked: bool = False
    session: str | None = None

class ORBStrategy:
    def __init__(self, symbol: str, opening_range_minutes: int = 30):
        self.symbol = symbol
        self.opening_range_minutes = opening_range_minutes
        self.state = ORBState()

    def env(self, key: str, default=None):
        import os
        return os.getenv(key, default)

    def on_bar(self, bar: dict) -> Signal | None:
        # Derive session
        session = to_session_date(bar["timestamp"])
        if self.state.session != session:
            self.state = ORBState(session=session)
        bar_time = bar["timestamp"]
        session_open = datetime(bar_time.year, bar_time.month, bar_time.day, 13, 30)  # 9:30 NY placeholder
        cutoff = session_open + timedelta(minutes=self.opening_range_minutes)

        if bar_time <= cutoff:
            # Build range
            if self.state.range_high is None:
                self.state.range_high = bar["high"]
                self.state.range_low = bar["low"]
            else:
                self.state.range_high = max(self.state.range_high, bar["high"])
                self.state.range_low = min(self.state.range_low, bar["low"])
            return None

        if not self.state.locked:
            self.state.locked = True
            log.info(f"ORB locked: high={self.state.range_high} low={self.state.range_low}")

        # Breakout logic
        price = bar["close"]
        reason = ""
        if price > self.state.range_high:
            reason = "ORB Long Breakout"
            return Signal(
                symbol=self.symbol,
                side="LONG",
                confidence=0.75,
                reason=reason,
                timestamp=bar_time.isoformat(),
                price=price,
                size_pct=0.05,
            )
        if price < self.state.range_low:
            reason = "ORB Short Breakdown"
            return Signal(
                symbol=self.symbol,
                side="SHORT",
                confidence=0.75,
                reason=reason,
                timestamp=bar_time.isoformat(),
                price=price,
                size_pct=0.05,
            )
        return None
