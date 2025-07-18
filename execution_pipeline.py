from primefire.utils.logging_setup import get_logger
from primefire.config.schema import Signal
from primefire.core.broker_interface import BrokerInterface
from primefire.core.order_manager import OrderManager
from primefire.core.position_tracker import PositionTracker
from primefire.core.risk_engine import RiskEngine
from primefire.core.data_feed import CSVFeed, LivePollingFeed
from primefire.storage.persistence import TradeRecorder

class ExecutionPipeline:
    def __init__(
        self,
        feed,
        router,
        risk: RiskEngine,
        order_manager: OrderManager,
        tracker: PositionTracker,
        recorder: TradeRecorder,
        logger,
        live: bool = False,
    ):
        self.feed = feed
        self.router = router
        self.risk = risk
        self.order_manager = order_manager
        self.tracker = tracker
        self.recorder = recorder
        self.logger = logger
        self.live = live
        self._equity_cache = None

    def account_equity(self):
        eq = self.order_manager.broker.total_equity()
        return eq

    def current_pnl_pct(self):
        if self._equity_cache is None:
            self._equity_cache = self.account_equity()
            return 0.0
        now_equity = self.account_equity()
        return (now_equity - self._equity_cache) / self._equity_cache * 100

    def handle_signals(self, signals: list[Signal], bar):
        pnl_pct = self.current_pnl_pct()
        eq = self.account_equity()
        for sig in signals:
            vetted = self.risk.evaluate_signal(sig, eq, pnl_pct)
            if not vetted:
                continue
            order = self.order_manager.signal_to_order(vetted, eq)
            if not order:
                continue
            fill = self.order_manager.execute(order)
            self.tracker.update_from_fill(fill)
            self.recorder.record(fill, order.reason, pnl_pct, eq)

    def step(self):
        if isinstance(self.feed, LivePollingFeed):
            bars = list(self.feed.fetch())
            for bar in bars:
                signals = self.router.process_bar(bar)
                self.handle_signals(signals, bar)
        else:
            raise NotImplementedError

    def run(self):
        if isinstance(self.feed, CSVFeed):
            for bar in self.feed:
                signals = self.router.process_bar(bar)
                self.handle_signals(signals, bar)
        else:
            raise NotImplementedError("Use step() loop for live feeds.")
