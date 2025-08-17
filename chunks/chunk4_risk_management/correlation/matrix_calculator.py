import sys
sys.path.append('.')

from src.database import SessionLocal
from src.models.market_data import MarketData
from src.models.risk import CorrelationMatrix
from sqlalchemy import desc
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

def calculate_correlation_matrix(asset_ids: list[int]):
    """
    Calculates the correlation matrix for a given list of assets.
    """
    db = SessionLocal()
    try:
        # Fetch the last 30 days of market data for each asset
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        all_market_data = db.query(MarketData).filter(
            MarketData.asset_id.in_(asset_ids),
            MarketData.timestamp >= start_date,
            MarketData.timestamp <= end_date
        ).order_by(MarketData.timestamp).all()

        if not all_market_data:
            return None

        # Create a list of dictionaries from the market data
        data = [{'timestamp': md.timestamp, 'asset_id': md.asset_id, 'close': md.close} for md in all_market_data]
        df = pd.DataFrame(data)
        df = df.pivot(index='timestamp', columns='asset_id', values='close')

        # Forward-fill missing values
        df.fillna(method='ffill', inplace=True)
        df.fillna(method='bfill', inplace=True) # Also backfill for safety

        # Calculate daily returns
        returns = df.pct_change().dropna()

        # Calculate correlation matrix
        correlation_matrix = returns.corr()

        # Save the entire matrix to the database
        new_correlation_matrix = CorrelationMatrix(
            timestamp=datetime.now(),
            period_days=30,
            matrix=correlation_matrix.to_dict()
        )
        db.add(new_correlation_matrix)
        db.commit()

        return correlation_matrix
    finally:
        db.close()
