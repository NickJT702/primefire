import time
from datetime import datetime

class SimpleScheduler:
    def __init__(self, interval_seconds: int, fn):
        self.interval_seconds = interval_seconds
        self.fn = fn

    def run_forever(self):
        while True:
            self.fn()
            time.sleep(self.interval_seconds)
