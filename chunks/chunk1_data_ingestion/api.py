import json
import psycopg2
import redis
from fastapi import FastAPI, HTTPException
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

# Pydantic Models - A simplified version for API responses
class FearGreedResponse(BaseModel):
    timestamp: datetime
    value: int
    value_classification: str

class MarketDataResponse(BaseModel):
    asset_id: int
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float

class SentimentResponse(BaseModel):
    asset_id: int
    timestamp: datetime
    source: str
    sentiment_score: float
    volume: int
    mentions: int

# --- Database and Cache Connections ---
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="trading_framework",
        user="user",
        password="password"
    )

def get_redis_connection():
    return redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


app = FastAPI()

@app.get("/latest/fear_greed", response_model=FearGreedResponse)
def get_latest_fear_greed():
    redis_key = "fear_greed_index:latest"
    try:
        redis_conn = get_redis_connection()
        cached_data = redis_conn.get(redis_key)
        if cached_data:
            data = json.loads(cached_data)
            data['timestamp'] = datetime.fromtimestamp(int(data['timestamp']))
            return data
    except redis.RedisError as e:
        print(f"Redis error: {e}") # Log error but proceed to DB

    db_conn = None
    try:
        db_conn = get_db_connection()
        with db_conn.cursor() as cur:
            cur.execute("SELECT timestamp, value, value_classification FROM trading_framework.fear_greed_index ORDER BY timestamp DESC LIMIT 1")
            record = cur.fetchone()
            if not record:
                raise HTTPException(status_code=404, detail="Fear & Greed data not found.")
            return {"timestamp": record[0], "value": record[1], "value_classification": record[2]}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        if db_conn:
            db_conn.close()

@app.get("/latest/prices", response_model=List[MarketDataResponse])
def get_latest_prices(asset_id: int = 1, limit: int = 100):
    db_conn = None
    try:
        db_conn = get_db_connection()
        with db_conn.cursor() as cur:
            cur.execute("SELECT asset_id, timestamp, open, high, low, close FROM trading_framework.market_data WHERE asset_id = %s ORDER BY timestamp DESC LIMIT %s", (asset_id, limit))
            records = cur.fetchall()
            if not records:
                raise HTTPException(status_code=404, detail=f"Price data not found for asset_id {asset_id}.")
            return [{"asset_id": r[0], "timestamp": r[1], "open": r[2], "high": r[3], "low": r[4], "close": r[5]} for r in records]
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        if db_conn:
            db_conn.close()

@app.get("/latest/sentiment", response_model=SentimentResponse)
def get_latest_sentiment(asset_id: int = 1, source: str = 'simulated_twitter'):
    redis_key = f"social_sentiment:{asset_id}:{source}:latest"
    try:
        redis_conn = get_redis_connection()
        cached_data = redis_conn.get(redis_key)
        if cached_data:
            data = json.loads(cached_data)
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
            return data
    except redis.RedisError as e:
        print(f"Redis error: {e}")

    db_conn = None
    try:
        db_conn = get_db_connection()
        with db_conn.cursor() as cur:
            cur.execute("SELECT asset_id, timestamp, source, sentiment_score, volume, mentions FROM trading_framework.social_sentiment WHERE asset_id = %s AND source = %s ORDER BY timestamp DESC LIMIT 1", (asset_id, source))
            record = cur.fetchone()
            if not record:
                raise HTTPException(status_code=404, detail=f"Sentiment data not found for asset_id {asset_id} and source {source}.")
            return {"asset_id": record[0], "timestamp": record[1], "source": record[2], "sentiment_score": record[3], "volume": record[4], "mentions": record[5]}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        if db_conn:
            db_conn.close()
