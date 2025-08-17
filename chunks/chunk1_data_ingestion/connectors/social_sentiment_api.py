import json
import psycopg2
import redis
import os
from datetime import datetime
import random

def get_db_connection():
    """Establishes connection to the PostgreSQL database."""
    return psycopg2.connect(
        host="localhost",
        database="trading_framework",
        user="user",
        password="password"
    )

def get_redis_connection():
    """Establishes connection to the Redis server."""
    return redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def fetch_simulated_social_sentiment(asset_id=1, source="simulated_twitter"):
    """
    Generates simulated social sentiment data, stores it in PostgreSQL,
    and caches it in Redis.
    """
    redis_key = f"social_sentiment:{asset_id}:{source}:latest"
    
    db_conn = None
    try:
        # Generate simulated data
        simulated_data = {
            "timestamp": datetime.now(),
            "asset_id": asset_id,
            "source": source,
            "sentiment_score": round(random.uniform(-1, 1), 4),
            "volume": random.randint(100, 10000),
            "mentions": random.randint(50, 5000)
        }
        
        # Connect to databases
        db_conn = get_db_connection()
        redis_conn = get_redis_connection()
        
        # Store in PostgreSQL
        with db_conn.cursor() as cur:
            cur.execute(
                """INSERT INTO trading_framework.social_sentiment (timestamp, asset_id, source, sentiment_score, volume, mentions)
                   VALUES (%s, %s, %s, %s, %s, %s)
                   ON CONFLICT (timestamp, asset_id, source) DO NOTHING;""",
                (
                    simulated_data["timestamp"],
                    simulated_data["asset_id"],
                    simulated_data["source"],
                    simulated_data["sentiment_score"],
                    simulated_data["volume"],
                    simulated_data["mentions"]
                )
            )
            db_conn.commit()
            print(f"Successfully stored simulated sentiment from {simulated_data['timestamp'].isoformat()} in PostgreSQL.")

        # Cache in Redis (serializing datetime for JSON)
        cached_data = simulated_data.copy()
        cached_data['timestamp'] = simulated_data['timestamp'].isoformat()
        redis_conn.set(redis_key, json.dumps(cached_data), ex=3600) # Cache for 1 hour
        print(f"Successfully cached data in Redis under key '{redis_key}'.")
        
        return simulated_data
        
    except (psycopg2.Error, redis.RedisError) as e:
        print(f"Database or cache error: {e}")
        return None
    finally:
        if db_conn:
            db_conn.close()

if __name__ == "__main__":
    fetch_simulated_social_sentiment()
