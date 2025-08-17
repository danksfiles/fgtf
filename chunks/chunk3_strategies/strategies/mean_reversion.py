from .base_strategy import BaseStrategy
from src.models.signals import TradeSignal

class MeanReversionStrategy(BaseStrategy):
    """A mean-reversion strategy."""

    def generate_signals(self) -> list[TradeSignal]:
        """Generates signals for the mean-reversion strategy."""
        # Placeholder implementation
        print("Generating signals for MeanReversionStrategy...")
        return []
