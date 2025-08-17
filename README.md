# Fear & Greed Adaptive Crypto Trading Framework

This project is a production-grade algorithmic trading system that dynamically adapts its strategies based on market sentiment regimes. It is designed to be a modular, risk-first architecture for cryptocurrency markets.

## Current Development Focus: Phase 0 - End-to-End Simulation

The current focus is on building and validating the entire logical pipeline in a controlled, simulated environment before integrating with live exchange APIs. This ensures the core decision-making framework is sound.

**Current Goal**: Implement a master script that simulates the full trading lifecycle:
1.  Generate mock data (Fear & Greed, prices).
2.  Run a sentiment engine to determine the market "Regime".
3.  Execute a strategy based on the regime to generate a signal.
4.  Feed the signal into the order router.
5.  Calculate slippage and trigger alerts.

## System Architecture

The framework is composed of several interconnected modules that form a data-driven pipeline:

```
[Data Sources] -> [Sentiment Engine] -> [Strategy Engine] -> [Risk Management] -> [Execution Engine] -> [Monitoring]
```

## Granular Implementation Plan

The project is being built in chunks, with the current focus on simulating the interaction between them.

-   **✅ Chunk 1 & 2: Data & Sentiment (Simulation)**: Develop mock data sources and a basic sentiment engine.
-   **✅ Chunk 3: Strategy (Simulation)**: Implement a core trading strategy that reacts to the sentiment engine.
-   **✅ Chunk 4: Risk Management (Simulation)**: Integrate basic risk controls like position sizing.
-   **✅ Chunk 5: Execution**: The order router and slippage monitor are complete.
-   **✅ Chunk 6: Monitoring**: A basic Streamlit dashboard and an alerting module are complete.

## Getting Started

### Prerequisites
- Python 3.10+
- Podman & podman-compose (or Docker & Docker-Compose)
- PostgreSQL 14+
- Redis 7+

### Environment Setup
1.  **Clone the repository** (if you haven't already).
2.  **Configure Environment**:
    ```bash
    cp .env.example .env
    # Edit .env with your database credentials if necessary
    ```
3.  **Start Services**:
    ```bash
    podman-compose up -d
    ```
    This will start the PostgreSQL and Redis containers.
4.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application
-   **Run the Dashboard**:
    ```bash
    streamlit run dashboard.py
    ```
-   **Run Verification Scripts**:
    The `scripts/` directory contains individual scripts to test modules, such as `run_order_router.py`.

## Project Structure

```
├── chunks/             # Core logic for each architectural chunk
├── configs/            # YAML configuration files
├── containers/         # Podman/Docker container definitions
├── scripts/            # Standalone scripts for verification and simulation
├── src/                # Core source code (database, models, etc.)
├── tests/              # Unit and integration tests
├── dashboard.py        # The Streamlit monitoring dashboard
├── podman-compose.yml  # Service definitions for Podman
└── README.md           # This file
```

## Database Schema
The full database schema is defined in `containers/postgres/init.sql`. It includes tables for market data, sentiment, signals, orders, risk, and monitoring.

---
*This README was consolidated from multiple context files for clarity.*
