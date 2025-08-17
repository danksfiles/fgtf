"""
Alpaca API Client for paper trading.

This module provides a client to connect to the Alpaca API, allowing
for paper trading execution and account information retrieval. It uses the
settings from src.config to configure the API connection.
"""
import alpaca_trade_api as tradeapi
from ..config import settings
from ..logger import get_logger

logger = get_logger(__name__)

class AlpacaClient:
    """
    A client for interacting with the Alpaca paper trading API.
    """
    def __init__(self):
        """
        Initializes the Alpaca API client.
        """
        self.api = None
        try:
            self.api = tradeapi.REST(
                key_id=settings.EXCHANGE_API_KEY,
                secret_key=settings.EXCHANGE_API_SECRET,
                base_url='https://paper-api.alpaca.markets',  # Ensure paper trading
                api_version='v2'
            )
            logger.info("Alpaca API client initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize Alpaca API client: {e}")
            raise

    def check_connection(self):
        """
        Checks the connection to the Alpaca API by fetching account info.

        Returns:
            dict: A dictionary with account information if successful.
            None: If the connection fails.
        """
        try:
            account = self.api.get_account()
            logger.info(f"Successfully connected to Alpaca. Account: {account.id}")
            return account._raw
        except Exception as e:
            logger.error(f"Failed to connect to Alpaca API: {e}")
            return None

    def place_order(self, symbol: str, qty: float, side: str, order_type: str = 'market', time_in_force: str = 'gtc'):
        """
        Places a paper trading order.

        Args:
            symbol (str): The ticker symbol to trade (e.g., 'SPY').
            qty (float): The number of shares to trade.
            side (str): 'buy' or 'sell'.
            order_type (str): 'market', 'limit', etc. Defaults to 'market'.
            time_in_force (str): 'gtc', 'day', etc. Defaults to 'gtc'.

        Returns:
            dict: The order object if successful.
            None: If the order placement fails.
        """
        try:
            logger.info(f"Placing {side} order for {qty} {symbol}...")
            order = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side=side,
                type=order_type,
                time_in_force=time_in_force
            )
            logger.info(f"Order placed successfully. Order ID: {order.id}")
            return order._raw
        except Exception as e:
            logger.error(f"Failed to place order: {e}")
            return None

if __name__ == '__main__':
    # Example usage:
    # To run this, you must have a .env file with your Alpaca paper trading keys:
    # EXCHANGE_API_KEY=your_paper_key
    # EXCHANGE_API_SECRET=your_paper_secret

    print("--- Alpaca Client Test ---")
    # Note: This will fail if API keys are not set in a .env file.
    if settings.EXCHANGE_API_KEY == "your_api_key_here":
        print("Please set your Alpaca paper trading keys in a .env file to run this test.")
    else:
        client = AlpacaClient()
        connection_status = client.check_connection()
        if connection_status:
            print("Connection successful.")
            # Example: Place a buy order for 1 share of SPY
            # client.place_order('SPY', 1, 'buy')
        else:
            print("Connection failed. Check your API keys and network.")
    print("--------------------------")
