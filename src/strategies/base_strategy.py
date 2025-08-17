"""
Base class for all trading strategies.
"""
from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    """
    Abstract base class for trading strategies.
    """
    @abstractmethod
    def generate_signal(self, fear_greed_index: float) -> str:
        """
        Generates a trading signal based on the Fear & Greed Index.

        Args:
            fear_greed_index (float): The current Fear & Greed Index value.

        Returns:
            str: A trading signal ('BUY', 'SELL', or 'HOLD').
        """
        pass
