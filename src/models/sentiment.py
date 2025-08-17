from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Float, UniqueConstraint
from src.database import Base

class SentimentSource(str, Enum):
    FEAR_GREED = "fear_greed"
    ON_CHAIN = "on_chain"
    SOCIAL = "social"
    OPTIONS = "options"

class MarketSentiment(Base):
    __tablename__ = 'market_sentiment'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, unique=True, nullable=False)
    fear_greed_value = Column(Integer)
    fear_greed_weight = Column(Float)
    on_chain_score = Column(Float)
    on_chain_weight = Column(Float)
    social_score = Column(Float)
    social_weight = Column(Float)
    options_score = Column(Float)
    options_weight = Column(Float)
    composite_score = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False)

    __table_args__ = (UniqueConstraint('timestamp', name='uq_market_sentiment_timestamp'),)

class MarketSentimentSchema(BaseModel):
    id: Optional[int] = None
    timestamp: datetime
    fear_greed_value: Optional[int] = Field(None, ge=0, le=100)
    fear_greed_weight: Optional[float] = Field(None, ge=0, le=1)
    on_chain_score: Optional[float] = Field(None, ge=-1, le=1)
    on_chain_weight: Optional[float] = Field(None, ge=0, le=1)
    social_score: Optional[float] = Field(None, ge=-1, le=1)
    social_weight: Optional[float] = Field(None, ge=0, le=1)
    options_score: Optional[float] = Field(None, ge=-1, le=1)
    options_weight: Optional[float] = Field(None, ge=0, le=1)
    composite_score: float = Field(..., ge=-1, le=1)
    confidence_score: float = Field(..., ge=0, le=1)

    class Config:
        orm_mode = True