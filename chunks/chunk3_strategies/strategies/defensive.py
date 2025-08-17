from .base_strategy import BaseStrategy
from src.models.signals import TradeSignal

class DefensiveStrategy(BaseStrategy):
    """A defensive strategy."""

    def generate_signals(self) -> list[TradeSignal]:
        """Generates signals for the defensive strategy."""
        # Placeholder implementation
        print("Generating signals for DefensiveStrategy...")
        return []
