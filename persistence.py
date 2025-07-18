from sqlalchemy import text
from primefire.storage.db import get_engine
from primefire.utils.logging_setup import get_logger

log = get_logger("persistence")

class TradeRecorder:
    def __init__(self):
        self.trades = []

    def record(self, fill, reason: str, pnl_pct: float, equity: float):
        entry = {
            "timestamp": fill.timestamp,
            "symbol": fill.symbol,
            "side": fill.side,
            "quantity": fill.quantity,
            "price": fill.price,
            "reason": reason,
            "pnl_pct": pnl_pct,
            "equity": equity,
            "cash_delta": (fill.price * fill.quantity) * (1 if fill.side == "SELL" else -1),
        }
        self.trades.append(entry)
        engine = get_engine()
        with engine.begin() as conn:
            conn.execute(
                text("""INSERT INTO trades(timestamp,symbol,side,quantity,price,reason,pnl_pct,equity)
                        VALUES(:timestamp,:symbol,:side,:quantity,:price,:reason,:pnl_pct,:equity)"""),
                entry,
            )
