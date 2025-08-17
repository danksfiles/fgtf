from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Enum as SQLAlchemyEnum
from src.database import Base

class SentimentZone(str, Enum):
    EXTREME_FEAR = "extreme_fear"
    FEAR = "fear"
    NEUTRAL = "neutral"
    GREED = "greed"
    EXTREME_GREED = "extreme_greed"

class MarketRegime(Base):
    __tablename__ = 'market_regime'

    id = Column(Integer, primary_key=True, index=True)
    sentiment_id = Column(Integer, nullable=False)
    zone = Column(SQLAlchemyEnum(SentimentZone), nullable=False)
    transition_strength = Column(Float, nullable=False)
    is_transitioning = Column(Boolean, default=False)
    previous_zone = Column(SQLAlchemyEnum(SentimentZone))
    next_zone = Column(SQLAlchemyEnum(SentimentZone))
    transition_start = Column(DateTime)
    transition_end = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)

class MarketRegimeSchema(BaseModel):
    id: Optional[int] = None
    sentiment_id: int
    zone: SentimentZone
    transition_strength: float = Field(..., ge=0, le=1)
    is_transitioning: bool = False
    previous_zone: Optional[SentimentZone] = None
    next_zone: Optional[SentimentZone] = None
    transition_start: Optional[datetime] = None
    transition_end: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True