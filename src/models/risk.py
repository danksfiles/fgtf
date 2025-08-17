
from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, validator


class RiskMetrics(BaseModel):
    timestamp: datetime
    portfolio_value: float = Field(..., gt=0)
    daily_pnl: float
    daily_pnl_pct: float
    unrealized_pnl: float
    unrealized_pnl_pct: float
    max_drawdown: float = Field(..., le=0)
    sharpe_ratio: Optional[float] = None
    sortino_ratio: Optional[float] = None
    var_95: Optional[float] = None
    exposure_pct: float = Field(..., ge=0, le=1)
    leverage: float = Field(..., ge=0)


from sqlalchemy import Column, Integer, DateTime, Float
from src.database import Base
from sqlalchemy.dialects.postgresql import JSONB

class RiskMetrics(Base):
    __tablename__ = 'risk_metrics'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    portfolio_value = Column(Float, nullable=False)
    daily_pnl = Column(Float, nullable=False)
    daily_pnl_pct = Column(Float, nullable=False)
    unrealized_pnl = Column(Float, nullable=False)
    unrealized_pnl_pct = Column(Float, nullable=False)
    max_drawdown = Column(Float, nullable=False)
    sharpe_ratio = Column(Float)
    sortino_ratio = Column(Float)
    var_95 = Column(Float)
    exposure_pct = Column(Float, nullable=False)
    leverage = Column(Float, nullable=False)

class RiskMetricsSchema(BaseModel):
    id: Optional[int] = None
    timestamp: datetime
    portfolio_value: float = Field(..., gt=0)
    daily_pnl: float
    daily_pnl_pct: float
    unrealized_pnl: float
    unrealized_pnl_pct: float
    max_drawdown: float = Field(..., le=0)
    sharpe_ratio: Optional[float] = None
    sortino_ratio: Optional[float] = None
    var_95: Optional[float] = None
    exposure_pct: float = Field(..., ge=0, le=1)
    leverage: float = Field(..., ge=0)

    class Config:
        orm_mode = True

class CorrelationMatrix(Base):
    __tablename__ = 'correlation_matrix'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    period_days = Column(Integer, nullable=False)
    matrix = Column(JSONB, nullable=False)

class CorrelationMatrixSchema(BaseModel):
    id: Optional[int] = None
    timestamp: datetime
    period_days: int
    matrix: Dict[str, Dict[str, float]]

    class Config:
        orm_mode = True

class CorrelationMatrixSchema(BaseModel):
    id: Optional[int] = None
    timestamp: datetime
    period_days: int
    matrix: Dict[str, Dict[str, float]]

    class Config:
        orm_mode = True

    @validator('matrix')
    def validate_matrix(cls, v):
        # Validate that the matrix is square and symmetric
        assets = list(v.keys())
        for asset in assets:
            if asset not in v or len(v[asset]) != len(assets):
                raise ValueError('Correlation matrix must be square')
            for other_asset in assets:
                if other_asset not in v[asset]:
                    raise ValueError(f'Missing correlation value for {asset} -> {other_asset}')
                if abs(v[asset][other_asset] - v[other_asset][asset]) > 0.001:
                    raise ValueError(f'Correlation matrix must be symmetric: {asset} -> {other_asset}')
                if not -1 <= v[asset][other_asset] <= 1:
                    raise ValueError(f'Correlation must be between -1 and 1: {asset} -> {other_asset}')
        return v
