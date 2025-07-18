# PRIMEFIRE

Autonomous trading framework focused on ORB (Opening Range Breakout) and extensible AI-driven enhancements.

## Quick Start

```bash
git clone <your_private_repo_url> primefire
cd primefire
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with real values (DO NOT COMMIT)
python scripts/run_backtest.py --data tests/data/sample_5min.csv
```

## Running Live (High-Level)

1. Ensure broker automation complies with current Terms of Service.
2. Populate required environment variables (`BROKER_*`).
3. `python scripts/run_live.py`

## Architecture

- `core`: deterministic trading pipeline (data → strategy → orders → risk → execution → tracking).
- `ai`: optional ML / reinforcement components augmenting signals.
- `orchestration`: uptime, scheduling, heartbeat.
- `storage`: persistence (SQLite / file).
- `interfaces`: CLI / (future) FastAPI web.
- `tests`: unit tests (sample data).

## Risk Controls

- Max position size per symbol (% of equity).
- Max daily loss (absolute / %).
- Circuit breakers for volatility / slippage.
- Kill switch file in `state/stop.flag`.

## Disclaimer

Educational framework. You are solely responsible for regulatory compliance and broker ToS adherence. Remove or adapt components as necessary.
