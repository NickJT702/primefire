from primefire.config.settings import SETTINGS
from primefire.config.schema import Signal
from primefire.utils.logging_setup import get_logger
import os
from pathlib import Path

log = get_logger("risk")

class RiskEngine:
    def __init__(self):
        self.daily_start_equity = None
        self.max_loss_pct = SETTINGS.max_daily_loss_pct
        self.max_position_pct = SETTINGS.max_position_pct
        self.kill_flag_path = Path("state/stop.flag")

    def check_kill_switch(self) -> bool:
        return self.kill_flag_path.exists()

    def evaluate_signal(self, signal: Signal, account_equity: float, current_pnl_pct: float) -> Signal | None:
        if self.check_kill_switch():
            log.warning("Kill switch active; rejecting signal.")
            return None
        if current_pnl_pct <= -self.max_loss_pct:
            log.warning("Daily loss limit exceeded; rejecting signal.")
            return None
        # Enforce position sizing cap
        if signal.size_pct * 100 > self.max_position_pct:
            signal.size_pct = self.max_position_pct / 100
        return signal
