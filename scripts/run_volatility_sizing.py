import sys
sys.path.append('.')

from chunks.chunk4_risk_management.position_sizing.volatility_based import calculate_volatility_based_position_size
from src.database import SessionLocal
from src.models.market_data import MarketData
from datetime import datetime, timedelta
import random

def run():
    db = SessionLocal()
    try:
        # Create dummy market data
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
        db.commit()

        print("Dummy market data created.")

        # Run volatility sizing
        position_size = calculate_volatility_based_position_size(asset_id=1)

        if position_size:
            print("Volatility sizing calculated. Position size created:")
            print(f"  ID: {position_size.position_size_id}")
            print(f"  Asset ID: {position_size.asset_id}")
            print(f"  Volatility: {position_size.volatility}")
            print(f"  Position Size: {position_size.position_size}")
        else:
            print("No position size created.")

    finally:
        db.close()

if __name__ == "__main__":
    run()
