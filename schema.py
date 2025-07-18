from pydantic import BaseModel
from typing import Literal

class Signal(BaseModel):
    symbol: str
    side: Literal["LONG", "SHORT", "FLAT"]
    confidence: float
    reason: str
    timestamp: str
    price: float | None = None
    size_pct: float = 1.0

class Order(BaseModel):
    symbol: str
    side: Literal["BUY", "SELL"]
    quantity: float
    order_type: Literal["MKT", "LMT"] = "MKT"
    limit_price: float | None = None
    reason: str
    timestamp: str

class Fill(BaseModel):
    symbol: str
    side: Literal["BUY", "SELL"]
    quantity: float
    price: float
    timestamp: str
    order_id: str
