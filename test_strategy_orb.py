from primefire.core.strategy_orb import ORBStrategy
from datetime import datetime, timedelta

def test_orb_basic():
    strat = ORBStrategy(symbol="TEST", opening_range_minutes=15)
    base = datetime(2025, 7, 17, 13, 30)
    # Build range bars
    for i in range(3):
        strat.on_bar({"timestamp": base + timedelta(minutes=5*i), "symbol":"TEST",
                      "open":500,"high":501+i*0.1,"low":499.5,"close":500.5,"volume":1000})
    # After cutoff
    sig = strat.on_bar({"timestamp": base + timedelta(minutes=20),
                        "symbol":"TEST","open":501,"high":505,"low":500,"close":505,"volume":2000})
    assert sig is not None
    assert sig.side == "LONG"
