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

def fetch_market_ohlcv(coin_id="bitcoin", vs_currency="usd", days="1"):
    """
    Fetches market OHLCV data from CoinGecko, stores it in PostgreSQL,
    and caches the latest entry in Redis.
    """
    api_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc?vs_currency={vs_currency}&days={days}"
    redis_key = f"market_ohlcv:{coin_id}:{vs_currency}:latest"
    
    db_conn = None
    try:
        # Fetch data from API
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        
        if not data:
            print("No data returned from API.")
            return None

        # Connect to databases
        db_conn = get_db_connection()
        redis_conn = get_redis_connection()
        
        # The kickstart context has an 'assets' table. We should have a way to link this data to an asset.
        # For now, we'll assume a static asset_id for simplicity, e.g., 1 for bitcoin.
        # A real implementation would look up the asset_id from the 'assets' table.
        asset_id = 1 # Static asset_id for bitcoin

        # Store in PostgreSQL
        with db_conn.cursor() as cur:
            # Using executemany for bulk insertion
            insert_query = """INSERT INTO trading_framework.market_data (asset_id, timestamp, open, high, low, close, volume)
                              VALUES (%s, %s, %s, %s, %s, %s, %s) -- Volume is not provided by this endpoint, so we use 0
                              ON CONFLICT (asset_id, timestamp) DO NOTHING;"""
            
            # CoinGecko OHLC data format: [timestamp, open, high, low, close]
            # We add asset_id and a placeholder for volume
            records_to_insert = [
                (asset_id, datetime.fromtimestamp(d[0] / 1000), d[1], d[2], d[3], d[4], 0) for d in data
            ]
            
            cur.executemany(insert_query, records_to_insert)
            db_conn.commit()
            print(f"Attempted to store {len(records_to_insert)} OHLCV records in PostgreSQL.")

        # Cache the latest entry in Redis
        latest_record = data[-1]
        redis_conn.set(redis_key, json.dumps(latest_record), ex=3600) # Cache for 1 hour
        print(f"Successfully cached latest OHLCV data in Redis under key '{redis_key}'.")
        
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
    # Before running, we should ensure the asset exists in the 'assets' table.
    # For this test, we'll manually insert it.
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO trading_framework.assets (asset_id, symbol, name, base_currency, quote_currency)
                           VALUES (1, 'btc', 'Bitcoin', 'btc', 'usd')
                           ON CONFLICT (asset_id) DO NOTHING;""")
            conn.commit()
    except psycopg2.Error as e:
        print(f"Could not pre-insert asset: {e}")
    finally:
        if conn:
            conn.close()
            
    fetch_market_ohlcv()