
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from src.database import Base

class MarketData(Base):
    __tablename__ = 'market_data'

    data_id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    quote_volume = Column(Float)
    trades_count = Column(Integer)

class MarketDataSchema(BaseModel):
    data_id: Optional[int] = None
    asset_id: int
    timestamp: datetime
    open: float = Field(..., gt=0)
    high: float = Field(..., gt=0)
    low: float = Field(..., gt=0)
    close: float = Field(..., gt=0)
    volume: float = Field(..., ge=0)
    quote_volume: Optional[float] = None
    trades_count: Optional[int] = None

    class Config:
        orm_mode = True

class Asset(Base):
    __tablename__ = 'assets'

    asset_id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    base_currency = Column(String, nullable=False)
    quote_currency = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

class AssetSchema(BaseModel):
    asset_id: Optional[int] = None
    symbol: str = Field(..., max_length=20)
    name: str = Field(..., max_length=100)
    base_currency: str = Field(..., max_length=10)
    quote_currency: str = Field(..., max_length=10)
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
