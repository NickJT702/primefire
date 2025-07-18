import os
from pydantic import BaseModel, Field

class Settings(BaseModel):
    max_daily_loss_pct: float = Field(default=2.5)
    max_position_pct: float = Field(default=10.0)
    risk_free_rate: float = Field(default=0.02)
    log_level: str = Field(default="INFO")

    @classmethod
    def load(cls):
        return cls(
            max_daily_loss_pct=float(os.getenv("PF_MAX_DAILY_LOSS_PCT", 2.5)),
            max_position_pct=float(os.getenv("PF_MAX_POSITION_PCT", 10.0)),
            risk_free_rate=float(os.getenv("PF_RISK_FREE_RATE", 0.02)),
            log_level=os.getenv("PF_LOG_LEVEL", "INFO"),
        )

SETTINGS = Settings.load()
