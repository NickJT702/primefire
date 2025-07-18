import logging
import os
from pathlib import Path

def get_logger(name: str):
    level = os.getenv("PF_LOG_LEVEL", "INFO").upper()
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(level)
    Path("logs").mkdir(exist_ok=True)
    fh = logging.FileHandler(f"logs/{name}.log")
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
