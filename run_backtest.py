#!/usr/bin/env python
import argparse
from primefire.utils.env_loader import load_env
from primefire.utils.logging_setup import get_logger
from primefire.core.data_feed import CSVFeed
from primefire.core.strategy_router import StrategyRouter
from primefire.core.strategy_orb import ORBStrategy
from primefire.core.risk_engine import RiskEngine
from primefire.core.order_manager import OrderManager
from primefire.core.position_tracker import PositionTracker
from primefire.core.execution_pipeline import ExecutionPipeline
from primefire.storage.db import init_db
from primefire.portfolio_analyzer import analyze_results  # type: ignore
from primefire.storage.persistence import TradeRecorder

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="CSV OHLCV file (sample in tests/data)")
    parser.add_argument("--symbol", default="TEST")
    parser.add_argument("--opening-range-minutes", type=int, default=30)
    args = parser.parse_args()

    load_env()
    log = get_logger("backtest")

    init_db()
    feed = CSVFeed(args.data, symbol=args.symbol)
    strategy = ORBStrategy(symbol=args.symbol, opening_range_minutes=args.opening_range_minutes)
    router = StrategyRouter([strategy])
    risk = RiskEngine()
    order_manager = OrderManager(paper=True)
    tracker = PositionTracker()
    recorder = TradeRecorder()

    pipeline = ExecutionPipeline(
        feed=feed,
        router=router,
        risk=risk,
        order_manager=order_manager,
        tracker=tracker,
        recorder=recorder,
        logger=log,
        live=False,
    )
    pipeline.run()

    analyze_results(recorder.trades)

if __name__ == "__main__":
    main()
