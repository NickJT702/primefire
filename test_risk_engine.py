from primefire.core.risk_engine import RiskEngine
from primefire.config.schema import Signal
from datetime import datetime

def test_risk_position_cap():
    re = RiskEngine()
    sig = Signal(symbol="TEST", side="LONG", confidence=0.9, reason="t", timestamp=datetime.utcnow().isoformat(), price=500, size_pct=0.50)
    vetted = re.evaluate_signal(sig, 100_000, 0)
    assert vetted.size_pct <= re.max_position_pct/100
