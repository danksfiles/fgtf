from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from src.models.signals import TradeSignal

class BaseStrategy(ABC):
    """Abstract base class for all trading strategies."""

    def __init__(self, db: Session):
        self.db = db

    @abstractmethod
    def generate_signals(self) -> list[TradeSignal]:
        """Generates a list of trading signals based on the strategy's logic."""
        pass
