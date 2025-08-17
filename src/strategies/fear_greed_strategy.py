"""
A simple strategy based on the Fear & Greed Index.
"""
from .base_strategy import BaseStrategy
from ..logger import get_logger

logger = get_logger(__name__)

class FearGreedStrategy(BaseStrategy):
    """
    A strategy that generates signals based on Fear & Greed thresholds.
    """
    def __init__(self, buy_threshold: float = 30.0, sell_threshold: float = 70.0):
        """
        Initializes the FearGreedStrategy.

        Args:
            buy_threshold (float): The F&G index value below which a BUY signal is generated.
            sell_threshold (float): The F&G index value above which a SELL signal is generated.
        """
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        logger.info(f"FearGreedStrategy initialized with buy threshold < {buy_threshold} and sell threshold > {sell_threshold}.")

    def generate_signal(self, fear_greed_index: float) -> str:
        """
        Generates a trading signal based on the Fear & Greed Index.

        Args:
            fear_greed_index (float): The current Fear & Greed Index value.

        Returns:
            str: A trading signal ('BUY', 'SELL', or 'HOLD').
        """
        if fear_greed_index < self.buy_threshold:
            logger.info(f"F&G index ({fear_greed_index:.2f}) is below buy threshold ({self.buy_threshold}). Signal: BUY")
            return "BUY"
        elif fear_greed_index > self.sell_threshold:
            logger.info(f"F&G index ({fear_greed_index:.2f}) is above sell threshold ({self.sell_threshold}). Signal: SELL")
            return "SELL"
        else:
            logger.info(f"F&G index ({fear_greed_index:.2f}) is within neutral zone. Signal: HOLD")
            return "HOLD"
