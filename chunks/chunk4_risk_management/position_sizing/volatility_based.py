import sys
sys.path.append('.')

from src.database import SessionLocal
from src.models.market_data import MarketData
from src.models.position_size import PositionSize
from sqlalchemy import desc
from datetime import datetime, timedelta
import numpy as np

def calculate_volatility_based_position_size(asset_id: int):
    """
    Calculates the position size for a given asset based on its volatility.
    """
    db = SessionLocal()
    try:
        # Fetch the last 30 days of market data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        market_data = db.query(MarketData).filter(
            MarketData.asset_id == asset_id,
            MarketData.timestamp >= start_date,
            MarketData.timestamp <= end_date
        ).order_by(MarketData.timestamp).all()

        if len(market_data) < 2:
            return None

        # Calculate daily returns
        prices = [md.close for md in market_data]
        returns = np.diff(prices) / prices[:-1]

        # Calculate volatility (standard deviation of returns)
        volatility = np.std(returns)

        if volatility == 0:
            return None

        # Calculate position size (inverse of volatility)
        position_size = 1 / volatility

        # Save to the database
        new_position_size = PositionSize(
            asset_id=asset_id,
            timestamp=datetime.now(),
            volatility=float(volatility),
            position_size=float(position_size)
        )
        db.add(new_position_size)
        db.commit()
        db.refresh(new_position_size)

        return new_position_size
    finally:
        db.close()
