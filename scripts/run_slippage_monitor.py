
import sys
sys.path.append('.')

from chunks.chunk5_execution.slippage_monitor import calculate_and_store_slippage
from src.models.orders import Order, OrderStatus, OrderType, TradeSide
from datetime import datetime
from uuid import uuid4

def run():
    """
    Runs the slippage monitor verification script.
    """
    print("Creating dummy order...")
    dummy_order = Order(
        order_id=str(uuid4()),
        signal_id=1,
        exchange="binance_testnet",
        asset_id=1,
        order_type=OrderType.MARKET,
        side=TradeSide.BUY,
        quantity=1.0,
        status=OrderStatus.FILLED,
        filled_quantity=1.0,
        filled_price=101.0,
        created_at=datetime.now(),
        executed_at=datetime.now()
    )

    print("Calculating and storing slippage...")
    slippage = calculate_and_store_slippage(order=dummy_order)

    print("Slippage calculated and stored:")
    print(f"  Order ID: {slippage.order_id}")
    print(f"  Expected Price: {slippage.expected_price}")
    print(f"  Actual Price: {slippage.actual_price}")
    print(f"  Slippage: {slippage.slippage}")

if __name__ == "__main__":
    run()
