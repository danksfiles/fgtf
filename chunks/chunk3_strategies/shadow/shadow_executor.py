from sqlalchemy.orm import Session
from src.database import get_db
from chunks.chunk3_strategies.strategies.trend_following import TrendFollowingStrategy
from chunks.chunk3_strategies.strategies.mean_reversion import MeanReversionStrategy
from chunks.chunk3_strategies.strategies.defensive import DefensiveStrategy

def run_shadow_execution():
    """ 
    Runs all strategies in shadow mode and stores the generated signals in the database.
    """
    db: Session = next(get_db())
    try:
        print("Running shadow execution...")
        strategies = [
            TrendFollowingStrategy(db),
            MeanReversionStrategy(db),
            DefensiveStrategy(db),
        ]

        for strategy in strategies:
            signals = strategy.generate_signals()
            for signal in signals:
                db.add(signal)
            db.commit()
        print("Shadow execution completed successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    run_shadow_execution()
