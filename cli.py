import argparse

def parse():
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["backtest", "live"], default="backtest")
    return p.parse_args()
