
import sys
sys.path.append('.')

from src.database import SessionLocal
from src.models.orders import Order
from src.models.slippage import Slippage

def calculate_and_store_slippage(order: Order):
    """
    Calculates the slippage for an order and stores it in the database.
    """
    db = SessionLocal()
    try:
        # For now, we'll assume a fixed expected price.
        # In a real-world scenario, this would be fetched from a price feed.
        expected_price = 100.0

        slippage = order.filled_price - expected_price

        new_slippage = Slippage(
            order_id=order.order_id,
            expected_price=expected_price,
            actual_price=order.filled_price,
            slippage=slippage
        )
        db.add(new_slippage)
        db.commit()
        db.refresh(new_slippage)

        return new_slippage
    finally:
        db.close()
