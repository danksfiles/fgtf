from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, DateTime, Float, ARRAY
from src.database import Base
from .signals import SignalDirection

class MasterSignal(Base):
    __tablename__ = 'master_signals'

    master_signal_id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    signal_type = Column(String, nullable=False)
    strength = Column(Float, nullable=False)
    direction = Column(String, nullable=False)
    price = Column(Float)
    stop_loss = Column(Float)
    take_profit = Column(Float)
    conflicting_signals = Column(ARRAY(Integer))
    created_at = Column(DateTime, default=datetime.now)

class MasterSignalSchema(BaseModel):
    master_signal_id: Optional[int] = None
    asset_id: int
    timestamp: datetime
    signal_type: str
    strength: float = Field(..., ge=0, le=1)
    direction: SignalDirection
    price: Optional[float] = Field(None, gt=0)
    stop_loss: Optional[float] = Field(None, gt=0)
    take_profit: Optional[float] = Field(None, gt=0)
    conflicting_signals: Optional[List[int]] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
