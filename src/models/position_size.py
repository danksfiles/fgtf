from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, DateTime, Float
from src.database import Base

class PositionSize(Base):
    __tablename__ = 'position_sizes'

    position_size_id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    volatility = Column(Float, nullable=False)
    position_size = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

class PositionSizeSchema(BaseModel):
    position_size_id: Optional[int] = None
    asset_id: int
    timestamp: datetime
    volatility: float = Field(..., gt=0)
    position_size: float = Field(..., gt=0)
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
