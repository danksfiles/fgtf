
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float
from src.database import Base
from uuid import UUID

class Slippage(Base):
    __tablename__ = 'slippage'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, nullable=False)
    expected_price = Column(Float, nullable=False)
    actual_price = Column(Float, nullable=False)
    slippage = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
