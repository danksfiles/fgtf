import requests
import json
import psycopg2
import redis
import os
from datetime import datetime

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

def fetch_fear_greed_index():
    """
    Fetches the latest Fear & Greed Index data from alternative.me,
    stores it in PostgreSQL, and caches it in Redis.
    """
    api_url = "https://api.alternative.me/fng/?limit=1"
    redis_key = "fear_greed_index:latest"
    
    db_conn = None
    try:
        # Fetch data from API
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()['data'][0]
        
        # Connect to databases
        db_conn = get_db_connection()
        redis_conn = get_redis_connection()
        
        # Prepare data for insertion
        timestamp = datetime.fromtimestamp(int(data['timestamp']))
        value = int(data['value'])
        value_classification = data['value_classification']
        
        # Store in PostgreSQL
        with db_conn.cursor() as cur:
            cur.execute(
                """INSERT INTO trading_framework.fear_greed_index (timestamp, value, value_classification)
                   VALUES (%s, %s, %s)
                   ON CONFLICT (timestamp) DO NOTHING;""",
                (timestamp, value, value_classification)
            )
            db_conn.commit()
            print(f"Successfully stored value {value} from {timestamp.isoformat()} in PostgreSQL.")

        # Cache in Redis
        redis_conn.set(redis_key, json.dumps(data), ex=3600) # Cache for 1 hour
        print(f"Successfully cached data in Redis under key '{redis_key}'.")
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None
    except (psycopg2.Error, redis.RedisError) as e:
        print(f"Database or cache error: {e}")
        return None
    finally:
        if db_conn:
            db_conn.close()

if __name__ == "__main__":
    fetch_fear_greed_index()