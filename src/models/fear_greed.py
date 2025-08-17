
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator


class FearGreedIndex(BaseModel):
    timestamp: datetime
    value: int = Field(..., ge=0, le=100)
    value_classification: Optional[str] = None
    timestamp_until: Optional[datetime] = None

    @validator('value')
    def validate_value(cls, v):
        if not 0 <= v <= 100:
            raise ValueError('Fear & Greed value must be between 0 and 100')
        return v


class FearGreedHistory(BaseModel):
    data: List[FearGreedIndex]
    count: int

    @validator('count')
    def validate_count(cls, v, values):
        if 'data' in values and v != len(values['data']):
            raise ValueError('Count must match length of data')
        return v
