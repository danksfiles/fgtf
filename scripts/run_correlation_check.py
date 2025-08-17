import sys
sys.path.append('.')

from chunks.chunk4_risk_management.correlation.matrix_calculator import calculate_correlation_matrix
from src.database import SessionLocal
from src.models.market_data import MarketData
from datetime import datetime, timedelta
import random

def run():
    db = SessionLocal()
    try:
        # Create dummy market data for two assets
        for i in range(30):
            db.add(MarketData(
                asset_id=1,
                timestamp=datetime.now() - timedelta(days=i),
                open=100 + i,
                high=100 + i + 1,
                low=100 + i - 1,
                close=100 + i + random.uniform(-1, 1),
                volume=1000
            ))
            db.add(MarketData(
                asset_id=2,
                timestamp=datetime.now() - timedelta(days=i),
                open=200 + i,
                high=200 + i + 1,
                low=200 + i - 1,
                close=200 + i + random.uniform(-1, 1),
                volume=1000
            ))
        db.commit()

        print("Dummy market data created.")

        # Run correlation check
        correlation_matrix = calculate_correlation_matrix(asset_ids=[1, 2])

        if correlation_matrix is not None:
            print("Correlation matrix calculated:")
            print(correlation_matrix)
        else:
            print("No correlation matrix created.")

    finally:
        db.close()

if __name__ == "__main__":
    run()
