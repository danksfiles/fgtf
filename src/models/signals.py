from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, Field, validator
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Enum as SQLAlchemyEnum
from src.database import Base

class SignalDirection(str, Enum):
    LONG = "long"
    SHORT = "short"

class TradeSignal(Base):
    __tablename__ = 'strategy_signals'

    signal_id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, nullable=False)
    asset_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    signal_type = Column(String, nullable=False)
    strength = Column(Float, nullable=False)
    direction = Column(SQLAlchemyEnum(SignalDirection), nullable=False)
    price = Column(Float)
    stop_loss = Column(Float)
    take_profit = Column(Float)
    ttl = Column(DateTime)
    is_executed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)

class TradeSignalSchema(BaseModel):
    signal_id: Optional[int] = None
    strategy_id: int
    asset_id: int
    timestamp: datetime
    signal_type: str
    strength: float = Field(..., ge=0, le=1)
    direction: SignalDirection
    price: Optional[float] = Field(None, gt=0)
    stop_loss: Optional[float] = Field(None, gt=0)
    take_profit: Optional[float] = Field(None, gt=0)
    ttl: Optional[datetime] = None
    is_executed: bool = False
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True