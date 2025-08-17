"""
Market data client for fetching asset prices using the Alpaca API.
"""
from alpaca_trade_api.rest import REST, TimeFrame
from ..config import settings
from ..logger import get_logger

logger = get_logger(__name__)

class MarketDataClient:
    """
    A client for fetching market data from Alpaca.
    """
    def __init__(self):
        """
        Initializes the MarketDataClient.
        """
        self.api = None
        try:
            # The same API keys can be used for market data
            self.api = REST(
                key_id=settings.EXCHANGE_API_KEY,
                secret_key=settings.EXCHANGE_API_SECRET,
                base_url='https://paper-api.alpaca.markets'
            )
            logger.info("MarketDataClient initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize MarketDataClient: {e}")
            raise

    def get_latest_quote(self, symbol: str):
        """
        Fetches the latest quote for a given symbol.

        Args:
            symbol (str): The ticker symbol (e.g., 'SPY').

        Returns:
            dict: The latest quote data, or None if an error occurs.
        """
        try:
            quote = self.api.get_latest_quote(symbol)
            logger.debug(f"Fetched latest quote for {symbol}: {quote}")
            return quote._raw
        except Exception as e:
            logger.error(f"Failed to get latest quote for {symbol}: {e}")
            return None

    def get_historical_bars(self, symbol: str, timeframe: TimeFrame, start_date: str, end_date: str):
        """
        Fetches historical bar data for a given symbol.

        Args:
            symbol (str): The ticker symbol.
            timeframe (TimeFrame): The timeframe for the bars (e.g., TimeFrame.Day).
            start_date (str): The start date in ISO format (YYYY-MM-DD).
            end_date (str): The end date in ISO format (YYYY-MM-DD).

        Returns:
            list: A list of bar objects, or None if an error occurs.
        """
        try:
            bars = self.api.get_bars(symbol, timeframe, start_date, end_date).df
            logger.debug(f"Fetched {len(bars)} historical bars for {symbol} from {start_date} to {end_date}.")
            return bars
        except Exception as e:
            logger.error(f"Failed to get historical bars for {symbol}: {e}")
            return None

if __name__ == '__main__':
    # Example usage:
    # Ensure your .env file has valid Alpaca API keys.
    print("--- Market Data Client Test ---")
    if settings.EXCHANGE_API_KEY == "your_api_key_here":
        print("Please set your Alpaca paper trading keys in a .env file to run this test.")
    else:
        client = MarketDataClient()
        
        # Test fetching latest quote
        spy_quote = client.get_latest_quote('SPY')
        if spy_quote:
            print(f"Latest SPY Quote: {spy_quote}")

        # Test fetching historical data
        from datetime import datetime, timedelta
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        spy_bars = client.get_historical_bars('SPY', TimeFrame.Day, start_date, end_date)
        if spy_bars is not None:
            print(f"Successfully fetched {len(spy_bars)} daily bars for SPY.")
            print(spy_bars.head())
    print("-----------------------------")
