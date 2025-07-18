from typing import List
from primefire.config.schema import Signal

class StrategyRouter:
    def __init__(self, strategies: List):
        self.strategies = strategies

    def process_bar(self, bar: dict) -> list[Signal]:
        signals = []
        for strat in self.strategies:
            sig = strat.on_bar(bar)
            if sig:
                signals.append(sig)
        return signals
