from .base_strategy import BaseStrategy
from src.models.signals import TradeSignal

class TrendFollowingStrategy(BaseStrategy):
    """A trend-following strategy."""

    def generate_signals(self) -> list[TradeSignal]:
        """Generates signals for the trend-following strategy."""
        # Placeholder implementation
        print("Generating signals for TrendFollowingStrategy...")
        return []
