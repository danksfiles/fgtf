import sys
sys.path.append('.')

from chunks.chunk5_execution.order_management.order_router import place_order
from src.database import SessionLocal
from src.models.signals import TradeSignal, SignalDirection
from datetime import datetime

def run():
    db = SessionLocal()
    try:
        # Create a dummy signal
        signal = TradeSignal(
            strategy_id=1,
            asset_id=1,
            timestamp=datetime.now(),
            signal_type="test",
            strength=0.8,
            direction=SignalDirection.LONG,
            price=100
        )
        db.add(signal)
        db.commit()
        db.refresh(signal)

        print("Dummy signal created.")

        # Run order router
        order = place_order(signal=signal, size=1.0)

        if order:
            print("Order placed:")
            print(f"  ID: {order.order_id}")
            print(f"  Asset ID: {order.asset_id}")
            print(f"  Side: {order.side}")
            print(f"  Quantity: {order.quantity}")
        else:
            print("No order placed.")

    finally:
        db.close()

if __name__ == "__main__":
    run()
