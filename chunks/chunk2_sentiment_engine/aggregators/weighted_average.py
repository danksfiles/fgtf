import psycopg2
from datetime import datetime, timedelta

def get_db_connection():
    """Establishes connection to the PostgreSQL database."""
    return psycopg2.connect(
        host="localhost",
        database="trading_framework",
        user="user",
        password="password"
    )

def aggregate_sentiment():
    """ 
    Pulls the latest fear/greed and social sentiment data, calculates a 
    weighted average, and stores it in the market_sentiment table.
    """
    db_conn = None
    try:
        db_conn = get_db_connection()
        with db_conn.cursor() as cur:
            # Get latest Fear & Greed value (normalized to -1 to 1 range)
            cur.execute("SELECT value, timestamp FROM trading_framework.fear_greed_index ORDER BY timestamp DESC LIMIT 1")
            fg_record = cur.fetchone()
            if not fg_record:
                print("No Fear & Greed data found.")
                return
            
            fg_value, fg_timestamp = fg_record
            # Normalize F&G from [0, 100] to [-1, 1]
            # (value / 50) - 1
            fg_score = (fg_value / 50.0) - 1.0

            # Get latest social sentiment score
            cur.execute("SELECT sentiment_score, timestamp FROM trading_framework.social_sentiment ORDER BY timestamp DESC LIMIT 1")
            social_record = cur.fetchone()
            if not social_record:
                print("No social sentiment data found.")
                return

            social_score = float(social_record[0])
            social_timestamp = social_record[1]

            # --- Simple Aggregation Logic ---
            # Define weights
            fg_weight = 0.6
            social_weight = 0.4

            # Calculate composite score
            composite_score = (fg_score * fg_weight) + (social_score * social_weight)

            # Calculate confidence score (simple version based on data freshness)
            now = datetime.now(fg_timestamp.tzinfo) # Use timezone from DB
            fg_age = (now - fg_timestamp).total_seconds()
            social_age = (now - social_timestamp).total_seconds()
            
            # Confidence decays as data gets older (e.g., max confidence if < 1 hour old)
            fg_confidence = max(0, 1 - (fg_age / (3600 * 4)))
            social_confidence = max(0, 1 - (social_age / 3600))
            confidence_score = (fg_confidence * fg_weight) + (social_confidence * social_weight)

            # Insert aggregated data into the market_sentiment table
            insert_query = """INSERT INTO trading_framework.market_sentiment 
                               (timestamp, fear_greed_value, fear_greed_weight, social_score, social_weight, composite_score, confidence_score)
                               VALUES (%s, %s, %s, %s, %s, %s, %s);"""
            
            cur.execute(insert_query, (
                now,
                fg_value,
                fg_weight,
                social_score,
                social_weight,
                composite_score,
                confidence_score
            ))
            db_conn.commit()

            print("Successfully calculated and stored aggregated sentiment.")
            print(f"  Composite Score: {composite_score:.4f}")
            print(f"  Confidence Score: {confidence_score:.4f}")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    finally:
        if db_conn:
            db_conn.close()

if __name__ == "__main__":
    aggregate_sentiment()
