from collections import defaultdict

class PositionTracker:
    def __init__(self):
        self.positions = defaultdict(float)

    def update_from_fill(self, fill):
        qty = fill.quantity if fill.side == "BUY" else -fill.quantity
        self.positions[fill.symbol] += qty

    def get_position(self, symbol: str) -> float:
        return self.positions.get(symbol, 0.0)
