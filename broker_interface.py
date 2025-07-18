import os
from datetime import datetime
from primefire.config.schema import Order, Fill
from primefire.utils.logging_setup import get_logger
import uuid
import random

log = get_logger("broker")

class BrokerInterface:
    """
    Abstract interface; here a paper & mock live combined.
    Replace with actual broker API integration (respecting ToS).
    """
    def __init__(self, paper: bool = True):
        self.paper = paper
        self.cash = 100_000.0
        self.positions = {}  # symbol -> quantity
        self._fills = []

    def place_order(self, order: Order) -> Fill:
        # Simple immediate execution
        price = order.limit_price if order.limit_price else self._simulate_price(order.symbol)
        qty = order.quantity
        cost = price * qty
        if order.side == "BUY":
            if cost > self.cash:
                raise ValueError("Insufficient cash")
            self.cash -= cost
            self.positions[order.symbol] = self.positions.get(order.symbol, 0) + qty
        else:  # SELL
            if self.positions.get(order.symbol, 0) < qty:
                qty = self.positions.get(order.symbol, 0)
            self.positions[order.symbol] -= qty
            self.cash += price * qty
        fill = Fill(
            symbol=order.symbol,
            side=order.side,
            quantity=qty,
            price=price,
            timestamp=datetime.utcnow().isoformat(),
            order_id=str(uuid.uuid4()),
        )
        self._fills.append(fill)
        log.info(f"Filled {fill.side} {fill.quantity} {fill.symbol} @ {fill.price:.2f}")
        return fill

    def _simulate_price(self, symbol: str) -> float:
        return 500 + random.uniform(-3, 3)

    def total_equity(self) -> float:
        marked_positions = sum(self._simulate_price(s) * q for s, q in self.positions.items())
        return self.cash + marked_positions

def get_broker(paper: bool) -> BrokerInterface:
    return BrokerInterface(paper=paper)
