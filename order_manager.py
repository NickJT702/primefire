from primefire.config.schema import Order, Signal
from primefire.core.broker_interface import get_broker
from datetime import datetime
from primefire.utils.logging_setup import get_logger

log = get_logger("orders")

class OrderManager:
    def __init__(self, paper: bool = True):
        self.broker = get_broker(paper=paper)

    def signal_to_order(self, signal: Signal, account_equity: float) -> Order | None:
        if signal.side == "FLAT":
            return None
        # size_pct applies to equity
        target_notional = account_equity * signal.size_pct
        # naive assumption price will be provided or re-fetched
        est_price = signal.price if signal.price else 500.0
        quantity = max(1, int(target_notional / est_price))
        side = "BUY" if signal.side == "LONG" else "SELL"
        return Order(
            symbol=signal.symbol,
            side=side,
            quantity=quantity,
            reason=signal.reason,
            timestamp=datetime.utcnow().isoformat(),
        )

    def execute(self, order: Order):
        return self.broker.place_order(order)
