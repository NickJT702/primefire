#!/usr/bin/env python
import time
from primefire.utils.env_loader import load_env
from primefire.utils.logging_setup import get_logger
from primefire.core.data_feed import LivePollingFeed
from primefire.core.strategy_orb import ORBStrategy
from primefire.core.strategy_router import StrategyRouter
from primefire.core.risk_engine import RiskEngine
from primefire.core.order_manager import OrderManager
from primefire.core.position_tracker import PositionTracker
from primefire.core.execution_pipeline import ExecutionPipeline
from primefire.storage.db import init_db
from primefire.storage.persistence import TradeRecorder

def main():
    load_env()
    log = get_logger("live")

    init_db()
    symbol = "SPY"  # Adjust
    strategy = ORBStrategy(symbol=symbol, opening_range_minutes=30)
    router = StrategyRouter([strategy])
    risk = RiskEngine()
    order_manager = OrderManager(
        paper=(str(strategy.env("BROKER_PAPER_MODE", "true")).lower() == "true")
    )
    tracker = PositionTracker()
    recorder = TradeRecorder()

    feed = LivePollingFeed(symbols=[symbol], interval_seconds=15)

    pipeline = ExecutionPipeline(
        feed=feed,
        router=router,
        risk=risk,
        order_manager=order_manager,
        tracker=tracker,
        recorder=recorder,
        logger=log,
        live=True,
    )

    while True:
        pipeline.step()
        time.sleep(feed.interval_seconds)

if __name__ == "__main__":
    main()
