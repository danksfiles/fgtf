"""
Sentiment Engine for calculating the Fear & Greed Index.
"""
import numpy as np
import pandas as pd
from alpaca_trade_api.rest import TimeFrame
from datetime import datetime, timedelta
from ..data_ingestion.market_data_client import MarketDataClient
from ..logger import get_logger

logger = get_logger(__name__)

class SentimentAnalyzer:
    """
    Calculates the Fear & Greed Index based on market data.
    """
    def __init__(self, market_data_client: MarketDataClient):
        """
        Initializes the SentimentAnalyzer.

        Args:
            market_data_client (MarketDataClient): The client for fetching market data.
        """
        self.market_data_client = market_data_client
        self.volatility_weight = 0.40
        self.momentum_weight = 0.30
        self.social_sentiment_weight = 0.30

    def _get_volatility_score(self, symbol: str = 'SPY') -> float:
        """
        Calculates the volatility score.
        Higher volatility = lower score (more fear).
        """
        try:
            end_date = datetime.now()
            start_date_90 = end_date - timedelta(days=90)
            
            bars = self.market_data_client.get_historical_bars(
                symbol, TimeFrame.Day, start_date_90.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
            )
            
            if bars is None or bars.empty:
                logger.warning("Could not retrieve historical bars for volatility score.")
                return 50.0 # Return neutral score

            # Calculate 30-day rolling volatility using a more robust method
            log_returns = np.log(bars['close'] / bars['close'].shift(1))
            bars['volatility'] = log_returns.rolling(window=30).std() * np.sqrt(252)
            
            current_volatility = bars['volatility'].iloc[-1]
            
            # Higher volatility should correlate with more fear (lower score)
            # We can normalize this against the 90-day history
            historical_volatility = bars['volatility'].dropna()
            percentile = historical_volatility.rank(pct=True).iloc[-1]
            
            # Invert the percentile: high volatility (high percentile) should result in a low score
            score = (1 - percentile) * 100
            
            logger.info(f"Volatility score for {symbol}: {score:.2f} (current vol: {current_volatility:.3f})")
            return score
        except Exception as e:
            logger.error(f"Error calculating volatility score: {e}", exc_info=True)
            return 50.0 # Return neutral score on error

    def _get_momentum_score(self, symbol: str = 'SPY') -> float:
        """
        Calculates the market momentum score.
        Price above 125-day MA = higher score (more greed).
        """
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=200) # Need enough data for 125-day MA
            
            bars = self.market_data_client.get_historical_bars(
                symbol, TimeFrame.Day, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
            )

            if bars is None or bars.empty:
                logger.warning("Could not retrieve historical bars for momentum score.")
                return 50.0

            bars['ma_125'] = bars['close'].rolling(window=125).mean()
            
            current_price = bars['close'].iloc[-1]
            current_ma = bars['ma_125'].iloc[-1]
            
            # If price is above MA, score is > 50, otherwise < 50
            # The further away, the more extreme the score
            price_ma_ratio = current_price / current_ma
            score = min(max(50 * price_ma_ratio, 0), 100) # Scale and cap the score
            logger.info(f"Momentum score for {symbol}: {score:.2f}")
            return score
        except Exception as e:
            logger.error(f"Error calculating momentum score: {e}", exc_info=True)
            return 50.0

    def _get_social_sentiment_score(self) -> float:
        """
        Placeholder for social sentiment analysis.
        """
        logger.info("Social sentiment score is a placeholder, returning neutral (50.0).")
        return 50.0

    def calculate_fear_greed_index(self, symbol: str = 'SPY') -> float:
        """
        Calculates the final Fear & Greed Index.

        Args:
            symbol (str): The ticker symbol to analyze.

        Returns:
            float: The Fear & Greed Index value (0-100).
        """
        logger.info(f"Calculating Fear & Greed Index for {symbol}...")
        
        volatility_score = self._get_volatility_score(symbol)
        momentum_score = self._get_momentum_score(symbol)
        social_score = self._get_social_sentiment_score()

        fear_greed_index = (
            volatility_score * self.volatility_weight +
            momentum_score * self.momentum_weight +
            social_score * self.social_sentiment_weight
        )
        
        logger.info(f"--- Fear & Greed Index: {fear_greed_index:.2f} ---")
        return fear_greed_index

if __name__ == '__main__':
    from ..config import settings
    
    print("--- Sentiment Analyzer Test ---")
    if settings.EXCHANGE_API_KEY == "your_api_key_here":
        print("Please set your Alpaca paper trading keys in a .env file to run this test.")
    else:
        market_client = MarketDataClient()
        analyzer = SentimentAnalyzer(market_client)
        index_value = analyzer.calculate_fear_greed_index('SPY')
        print(f"Current Fear & Greed Index for SPY: {index_value:.2f}")
    print("-----------------------------")
