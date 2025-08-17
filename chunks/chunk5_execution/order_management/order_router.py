import sys
from datetime import datetime
sys.path.append('.')

from src.database import SessionLocal
from src.models.orders import Order, OrderSchema, TradeSide
from src.models.signals import TradeSignal, SignalDirection

def place_order(signal: TradeSignal, size: float) -> OrderSchema:
    """
    Places an order based on a trade signal and logs it to the database.
    """
    db = SessionLocal()
    try:
        side = TradeSide.BUY if signal.direction == SignalDirection.LONG else TradeSide.SELL

        new_order = Order(
            signal_id=signal.signal_id,
            exchange="binance_testnet",
            asset_id=signal.asset_id,
            order_type="market",
            side=side,
            quantity=size,
            status="filled", # Assume immediate fill for now
            created_at=datetime.now(),
            executed_at=datetime.now()
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        return OrderSchema.from_orm(new_order)
    finally:
        db.close()
