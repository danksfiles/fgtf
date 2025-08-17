"""
Main application entry point for the Fear & Greed Trading Framework.

This script initializes the necessary components and runs the main trading loop.
"""
import time
from src.logger import get_logger
from src.config import settings
from src.execution.alpaca_client import AlpacaClient
from src.data_ingestion.market_data_client import MarketDataClient
from src.sentiment_engine.sentiment_analyzer import SentimentAnalyzer
from src.strategies.fear_greed_strategy import FearGreedStrategy

# Initialize logger
logger = get_logger(__name__)

def main():
    """
    The main function that runs the trading framework.
    """
    logger.info("--- Starting Fear & Greed Trading Framework ---")
    logger.info(f"Log Level set to: {settings.LOG_LEVEL}")

    # --- Initialize API Clients ---
    if settings.EXCHANGE_API_KEY == "your_api_key_here":
        logger.error("Alpaca API keys are not set. Please update your .env file.")
        return

    alpaca_client = AlpacaClient()
    if not alpaca_client.check_connection():
        logger.error("Failed to connect to Alpaca. Exiting.")
        return
    logger.info("Successfully connected to Alpaca paper trading.")

    market_data_client = MarketDataClient()
    logger.info("Market data client initialized.")

    # --- Initialize Core Components ---
    sentiment_analyzer = SentimentAnalyzer(market_data_client)
    strategy = FearGreedStrategy(buy_threshold=30, sell_threshold=70)
    logger.info("Core components initialized.")

    # --- Main Application Loop ---
    try:
        while True:
            # 1. Calculate the Fear & Greed index.
            fear_greed_index = sentiment_analyzer.calculate_fear_greed_index('SPY')

            # 2. Generate a trade signal using the strategy module.
            signal = strategy.generate_signal(fear_greed_index)
            
            logger.info(f"Generated Signal: {signal}")

            # 3. Execute the trade based on the signal.
            if signal == "BUY":
                logger.info("Executing BUY order.")
                # alpaca_client.place_order(symbol='SPY', qty=1, side='buy')
            elif signal == "SELL":
                logger.info("Executing SELL order.")
                # alpaca_client.place_order(symbol='SPY', qty=1, side='sell')
            else:
                logger.info("No action taken for HOLD signal.")

            # Sleep for a defined interval (e.g., 5 minutes)
            logger.info("--- Loop finished, sleeping for 5 minutes ---")
            time.sleep(300)

    except KeyboardInterrupt:
        logger.info("--- Shutting down framework ---")
    except Exception as e:
        logger.error(f"An unexpected error occurred in the main loop: {e}", exc_info=True)

if __name__ == "__main__":
    main()
