# Fear & Greed Trading Framework (fgtf)

This project is a production-grade, adaptive trading framework. The system automatically selects and executes strategies based on real-time market sentiment, with a primary focus on capital preservation and risk management.

## Vision & Guiding Principles

- **Risk-First**: The system's first priority is to survive extreme market events. Risk controls are not an afterthought; they are central to the architecture.
- **Adaptive Strategy**: No single strategy works in all market regimes. The framework must be able to identify the prevailing sentiment (e.g., fear, greed, neutrality) and deploy the appropriate strategy.
- **Simulate First**: All components and strategies must be validated through rigorous backtesting and paper-trading simulation before any live capital is deployed.
- **Test the Thesis, Not the Tech**: Prove the predictive power of signals before scaling infrastructure.
- **Start Small**: Test with a single asset and a minimal set of indicators first. Avoid premature complexity.

## Current Status: Phase 4 - Iteration

The project has a complete, end-to-end simulation pipeline. All core components (execution, data ingestion, sentiment engine, and strategies) are built and integrated. The framework is now in an iterative loop of backtesting, analysis, and refinement.

## Features

- **Modular Architecture**: Each component is a standalone module, making the system easy to maintain and extend.
- **Data Ingestion**: A client for fetching market data from Alpaca.
- **Sentiment Engine**: Calculates a proprietary "Fear & Greed" index based on volatility and market momentum.
- **Strategy Engine**: A modular system for defining and executing trading strategies. Comes with a baseline `FearGreedStrategy`.
- **Execution Client**: A client for placing paper trades via the Alpaca API.
- **Configuration-Driven**: All settings are managed via a `.env` file using `pydantic-settings`.
- **Backtesting Notebook**: A comprehensive Jupyter notebook for analyzing strategy performance.

## Getting Started

### Prerequisites
- Python 3.10+
- An Alpaca paper trading account (for API keys).

### Setup & Configuration
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/danksfiles/fgtf.git
    cd fgtf
    ```
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure your environment**:
    - Copy the example `.env.example` file to `.env`:
      ```bash
      cp .env.example .env
      ```
    - Edit the `.env` file and add your Alpaca paper trading API key and secret:
      ```
      EXCHANGE_API_KEY=YOUR_ALPACA_PAPER_KEY
      EXCHANGE_API_SECRET=YOUR_ALPACA_PAPER_SECRET
      ```

### Running the Live Simulation

The main application will run a continuous loop that calculates the Fear & Greed index and generates trading signals. **Note: By default, the lines that place actual paper trades are commented out in `src/main.py` for safety.**

To run the simulation:
```bash
python -m src.main
```
You will see logs in your console as the application runs its cycle.

### Running the Backtest

The backtesting notebook allows you to test the `FearGreedStrategy` on historical data and analyze its performance.

1.  **Start the Jupyter Notebook server**:
    ```bash
    jupyter notebook
    ```
2.  **Open the notebook**:
    Navigate to `notebooks/backtesting/initial_spy_vix_backtest.ipynb` in the Jupyter interface.
3.  **Run the cells**:
    Execute the cells in the notebook to fetch data, run the backtest, and visualize the results.

## Project Structure

```
├── notebooks/
│   └── backtesting/
│       └── initial_spy_vix_backtest.ipynb  # Main backtesting and analysis tool
├── src/
│   ├── data_ingestion/   # Clients for fetching data
│   ├── execution/        # Clients for executing trades
│   ├── sentiment_engine/ # Logic for calculating the F&G index
│   ├── strategies/       # Trading strategy definitions
│   ├── config.py         # Configuration management
│   ├── logger.py         # Logging setup
│   └── main.py           # Main application entry point
├── .env.example          # Example environment file
├── forward.md            # The project's development roadmap
├── NOTES.md              # Details on the F&G formula
├── README.md             # This file
└── requirements.txt      # Python dependencies
```