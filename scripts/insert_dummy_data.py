import sys
sys.path.append('.')

from src.database import get_db
from src.models.sentiment import MarketSentiment
from datetime import datetime

def insert_dummy_data():
    db = next(get_db())
    try:
        print("Inserting dummy data...")
        dummy_sentiment = MarketSentiment(
            timestamp=datetime.now(),
            fear_greed_value=50,
            fear_greed_weight=0.5,
            on_chain_score=0.5,
            on_chain_weight=0.25,
            social_score=0.5,
            social_weight=0.15,
            options_score=0.5,
            options_weight=0.1,
            composite_score=0.5,
            confidence_score=0.8
        )
        db.add(dummy_sentiment)
        db.commit()
        print("Dummy data inserted successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    insert_dummy_data()
