-- PostgreSQL Database Schema for Fear & Greed Adaptive Trading Framework

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create the main schema
CREATE SCHEMA IF NOT EXISTS trading_framework;

-- Set search path to our schema
SET search_path TO trading_framework, public;

-- Create enum types
CREATE TYPE sentiment_zone AS ENUM ('extreme_fear', 'fear', 'neutral', 'greed', 'extreme_greed');
CREATE TYPE strategy_type AS ENUM ('trend_following', 'mean_reversion', 'defensive', 'range_trading', 'hedged_positions');
CREATE TYPE order_status AS ENUM ('pending', 'open', 'filled', 'cancelled', 'rejected');
CREATE TYPE order_type AS ENUM ('market', 'limit', 'stop_limit', 'stop_market');
CREATE TYPE trade_side AS ENUM ('buy', 'sell');
CREATE TYPE alert_severity AS ENUM ('info', 'warning', 'critical');

-- Market Data Tables
CREATE TABLE assets (
    asset_id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    base_currency VARCHAR(10) NOT NULL,
    quote_currency VARCHAR(10) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE market_data (
    data_id SERIAL PRIMARY KEY,
    asset_id INTEGER REFERENCES assets(asset_id),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    open NUMERIC(20, 8) NOT NULL,
    high NUMERIC(20, 8) NOT NULL,
    low NUMERIC(20, 8) NOT NULL,
    close NUMERIC(20, 8) NOT NULL,
    volume NUMERIC(30, 8) NOT NULL,
    quote_volume NUMERIC(30, 8),
    trades_count INTEGER,
    UNIQUE(asset_id, timestamp)
);

-- Sentiment Data Tables
CREATE TABLE fear_greed_index (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    value INTEGER NOT NULL CHECK (value BETWEEN 0 AND 100),
    value_classification VARCHAR(50),
    timestamp_until TIMESTAMP WITH TIME ZONE,
    UNIQUE(timestamp)
);

CREATE TABLE on_chain_metrics (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    asset_id INTEGER REFERENCES assets(asset_id),
    transaction_volume NUMERIC(30, 2),
    active_addresses INTEGER,
    exchange_netflow NUMERIC(20, 8),
    nupl NUMERIC(10, 4),
    UNIQUE(timestamp, asset_id)
);

CREATE TABLE social_sentiment (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    asset_id INTEGER REFERENCES assets(asset_id),
    source VARCHAR(50) NOT NULL,
    sentiment_score NUMERIC(5, 4) CHECK (sentiment_score BETWEEN -1 AND 1),
    volume INTEGER,
    mentions INTEGER,
    UNIQUE(timestamp, asset_id, source)
);

CREATE TABLE options_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    asset_id INTEGER REFERENCES assets(asset_id),
    implied_volatility NUMERIC(10, 4),
    put_call_ratio NUMERIC(10, 4),
    skew NUMERIC(10, 4),
    term_structure NUMERIC(10, 4),
    UNIQUE(timestamp, asset_id)
);

-- Aggregated Sentiment and Regime Tables
CREATE TABLE market_sentiment (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    fear_greed_value INTEGER,
    fear_greed_weight NUMERIC(5, 4),
    on_chain_score NUMERIC(5, 4),
    on_chain_weight NUMERIC(5, 4),
    social_score NUMERIC(5, 4),
    social_weight NUMERIC(5, 4),
    options_score NUMERIC(5, 4),
    options_weight NUMERIC(5, 4),
    composite_score NUMERIC(5, 4),
    confidence_score NUMERIC(5, 4) CHECK (confidence_score BETWEEN 0 AND 1),
    UNIQUE(timestamp)
);

CREATE TABLE market_regime (
    id SERIAL PRIMARY KEY,
    sentiment_id INTEGER REFERENCES market_sentiment(id),
    zone sentiment_zone NOT NULL,
    transition_strength NUMERIC(5, 4),
    is_transitioning BOOLEAN DEFAULT FALSE,
    previous_zone sentiment_zone,
    next_zone sentiment_zone,
    transition_start TIMESTAMP WITH TIME ZONE,
    transition_end TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Strategy and Signal Tables
CREATE TABLE strategies (
    strategy_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type strategy_type NOT NULL,
    description TEXT,
    parameters JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE strategy_signals (
    signal_id SERIAL PRIMARY KEY,
    strategy_id INTEGER REFERENCES strategies(strategy_id),
    asset_id INTEGER REFERENCES assets(asset_id),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    signal_type VARCHAR(50) NOT NULL,
    strength NUMERIC(5, 4) CHECK (strength BETWEEN 0 AND 1),
    direction VARCHAR(10) NOT NULL, -- 'long', 'short'
    price NUMERIC(20, 8),
    stop_loss NUMERIC(20, 8),
    take_profit NUMERIC(20, 8),
    ttl TIMESTAMP WITH TIME ZONE,
    is_executed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Risk Management Tables
CREATE TABLE correlation_matrix (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    asset_1_id INTEGER REFERENCES assets(asset_id),
    asset_2_id INTEGER REFERENCES assets(asset_id),
    correlation NUMERIC(10, 4) CHECK (correlation BETWEEN -1 AND 1),
    period_days INTEGER NOT NULL,
    UNIQUE(timestamp, asset_1_id, asset_2_id, period_days)
);

CREATE TABLE contagion_events (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    source_asset_id INTEGER REFERENCES assets(asset_id),
    affected_asset_id INTEGER REFERENCES assets(asset_id),
    strength NUMERIC(5, 4) CHECK (strength BETWEEN 0 AND 1),
    direction VARCHAR(20), -- 'spillover', 'contagion', 'flight_to_safety'
    detection_method VARCHAR(50),
    UNIQUE(timestamp, source_asset_id, affected_asset_id)
);

CREATE TABLE circuit_breakers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'portfolio', 'strategy', 'asset'
    threshold NUMERIC(20, 8) NOT NULL,
    threshold_type VARCHAR(20) NOT NULL, -- 'percentage', 'absolute', 'volatility'
    is_active BOOLEAN DEFAULT TRUE,
    triggered_at TIMESTAMP WITH TIME ZONE,
    reset_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Execution Tables
CREATE TABLE orders (
    order_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    signal_id INTEGER REFERENCES strategy_signals(signal_id),
    exchange VARCHAR(50) NOT NULL,
    exchange_order_id VARCHAR(100),
    asset_id INTEGER REFERENCES assets(asset_id),
    order_type order_type NOT NULL,
    side trade_side NOT NULL,
    quantity NUMERIC(20, 8) NOT NULL,
    price NUMERIC(20, 8),
    stop_price NUMERIC(20, 8),
    status order_status NOT NULL,
    filled_quantity NUMERIC(20, 8) DEFAULT 0,
    filled_price NUMERIC(20, 8),
    fee NUMERIC(20, 8),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    executed_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE trades (
    trade_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID REFERENCES orders(order_id),
    asset_id INTEGER REFERENCES assets(asset_id),
    side trade_side NOT NULL,
    quantity NUMERIC(20, 8) NOT NULL,
    price NUMERIC(20, 8) NOT NULL,
    fee NUMERIC(20, 8),
    fee_currency VARCHAR(10),
    executed_at TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE positions (
    position_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id INTEGER REFERENCES assets(asset_id),
    quantity NUMERIC(20, 8) NOT NULL,
    average_entry_price NUMERIC(20, 8),
    unrealized_pnl NUMERIC(20, 8),
    realized_pnl NUMERIC(20, 8),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Monitoring and Governance Tables
CREATE TABLE performance_metrics (
    id SERIAL PRIMARY KEY,
    strategy_id INTEGER REFERENCES strategies(strategy_id),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    period VARCHAR(20) NOT NULL, -- 'daily', 'weekly', 'monthly'
    return_percentage NUMERIC(10, 4),
    sharpe_ratio NUMERIC(10, 4),
    sortino_ratio NUMERIC(10, 4),
    max_drawdown NUMERIC(10, 4),
    win_rate NUMERIC(10, 4),
    profit_factor NUMERIC(10, 4),
    total_trades INTEGER,
    UNIQUE(strategy_id, timestamp, period)
);

CREATE TABLE system_health (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    component VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL, -- 'healthy', 'warning', 'critical'
    cpu_usage NUMERIC(5, 2),
    memory_usage NUMERIC(5, 2),
    disk_usage NUMERIC(5, 2),
    api_latency_ms INTEGER,
    error_rate NUMERIC(5, 4),
    UNIQUE(timestamp, component)
);

CREATE TABLE alerts (
    alert_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    severity alert_severity NOT NULL,
    component VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    is_resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_market_data_asset_time ON market_data(asset_id, timestamp DESC);
CREATE INDEX idx_market_sentiment_time ON market_sentiment(timestamp DESC);
CREATE INDEX idx_market_regime_time ON market_regime(created_at DESC);
CREATE INDEX idx_strategy_signals_time ON strategy_signals(timestamp DESC);
CREATE INDEX idx_orders_status_time ON orders(status, created_at DESC);
CREATE INDEX idx_trades_asset_time ON trades(asset_id, executed_at DESC);
CREATE INDEX idx_system_health_time ON system_health(timestamp DESC);
CREATE INDEX idx_alerts_severity_time ON alerts(severity, timestamp DESC);

-- Create views for common queries
CREATE VIEW latest_market_data AS
SELECT DISTINCT ON (asset_id) 
    asset_id, symbol, name, timestamp, open, high, low, close, volume
FROM market_data
JOIN assets USING(asset_id)
ORDER BY asset_id, timestamp DESC;

CREATE VIEW latest_market_sentiment AS
SELECT * FROM market_sentiment
ORDER BY timestamp DESC
LIMIT 1;

CREATE VIEW current_regime AS
SELECT * FROM market_regime
WHERE is_transitioning = FALSE
ORDER BY created_at DESC
LIMIT 1;

CREATE VIEW open_positions AS
SELECT * FROM positions WHERE quantity != 0;

CREATE VIEW pending_orders AS
SELECT * FROM orders WHERE status = 'pending' OR status = 'open';
