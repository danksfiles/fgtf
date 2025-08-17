from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from uuid import UUID, uuid4


class Trade(BaseModel):
    trade_id: UUID = Field(default_factory=uuid4)
    order_id: UUID
    asset_id: int
    side: str = Field(..., pattern=r'^(buy|sell)$')
    quantity: float = Field(..., gt=0)
    price: float = Field(..., gt=0)
    fee: Optional[float] = Field(None, ge=0)
    fee_currency: Optional[str] = None
    executed_at: datetime = Field(default_factory=datetime.now)


class Position(BaseModel):
    position_id: UUID = Field(default_factory=uuid4)
    asset_id: int
    quantity: float
    average_entry_price: Optional[float] = Field(None, gt=0)
    unrealized_pnl: float = 0
    realized_pnl: float = 0
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @validator('quantity')
    def validate_quantity(cls, v):
        if v == 0:
            raise ValueError('Position quantity cannot be zero')
        return v