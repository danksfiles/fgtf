from sqlalchemy.orm import Session
from src.database import get_db
from src.models.sentiment import MarketSentiment
from src.models.regime import MarketRegime, SentimentZone
from chunks.chunk2_sentiment_engine.classifiers.dynamic_zones import get_sentiment_zone, get_default_thresholds

def get_latest_market_sentiment(db: Session) -> MarketSentiment:
    """Fetches the most recent market sentiment record from the database."""
    return db.query(MarketSentiment).order_by(MarketSentiment.timestamp.desc()).first()

def determine_and_store_regime(db: Session):
    """
    Determines the current market regime based on the latest sentiment data
    and stores it in the database.
    """
    latest_sentiment = get_latest_market_sentiment(db)
    if not latest_sentiment:
        print("No market sentiment data found. Cannot determine regime.")
        return

    thresholds = get_default_thresholds()
    current_zone = get_sentiment_zone(latest_sentiment.composite_score, thresholds)

    # For now, we'll do a simple direct insertion.
    # Hysteresis and transition logic will be added later.
    new_regime = MarketRegime(
        sentiment_id=latest_sentiment.id,
        zone=current_zone,
        transition_strength=1.0,  # Placeholder
        is_transitioning=False  # Placeholder
    )

    db.add(new_regime)
    db.commit()
    print(f"Successfully stored new regime: {current_zone.value}")

def main():
    """Main function to run the regime change process."""
    db_session_gen = get_db()
    db: Session = next(db_session_gen)
    try:
        determine_and_store_regime(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()