from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from enum import Enum
from uuid import UUID, uuid4
from sqlalchemy import Column, Integer, String, DateTime, Float, Enum as SQLAlchemyEnum
from src.database import Base

class OrderStatus(str, Enum):
    PENDING = "pending"
    OPEN = "open"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP_LIMIT = "stop_limit"
    STOP_MARKET = "stop_market"


class TradeSide(str, Enum):
    BUY = "buy"
    SELL = "sell"


class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    signal_id = Column(Integer, nullable=True)
    exchange = Column(String, nullable=False)
    exchange_order_id = Column(String, nullable=True)
    asset_id = Column(Integer, nullable=False)
    order_type = Column(SQLAlchemyEnum(OrderType), nullable=False)
    side = Column(SQLAlchemyEnum(TradeSide), nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=True)
    stop_price = Column(Float, nullable=True)
    status = Column(SQLAlchemyEnum(OrderStatus), nullable=False)
    filled_quantity = Column(Float, default=0)
    filled_price = Column(Float, nullable=True)
    fee = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    executed_at = Column(DateTime, nullable=True)


class OrderSchema(BaseModel):
    order_id: UUID = Field(default_factory=uuid4)
    signal_id: Optional[int] = None
    exchange: str
    exchange_order_id: Optional[str] = None
    asset_id: int
    order_type: OrderType
    side: TradeSide
    quantity: float = Field(..., gt=0)
    price: Optional[float] = Field(None, gt=0)
    stop_price: Optional[float] = Field(None, gt=0)
    status: OrderStatus
    filled_quantity: float = Field(0, ge=0)
    filled_price: Optional[float] = Field(None, gt=0)
    fee: Optional[float] = Field(None, ge=0)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    executed_at: Optional[datetime] = None

    @validator('price')
    def validate_price(cls, v, values):
        if v is None and values.get('order_type') in [OrderType.LIMIT, OrderType.STOP_LIMIT]:
            raise ValueError('Price is required for limit and stop-limit orders')
        return v

    @validator('stop_price')
    def validate_stop_price(cls, v, values):
        if v is None and values.get('order_type') in [OrderType.STOP_LIMIT, OrderType.STOP_MARKET]:
            raise ValueError('Stop price is required for stop orders')
        return v

    @validator('filled_quantity')
    def validate_filled_quantity(cls, v, values):
        if 'quantity' in values and v > values['quantity']:
            raise ValueError('Filled quantity cannot exceed order quantity')
        return v

    class Config:
        from_attributes = True