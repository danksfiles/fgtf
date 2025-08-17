import streamlit as st
import pandas as pd
import sys
sys.path.append('.')

from src.database import SessionLocal
from src.models.signals import TradeSignal
from src.models.orders import Order

def get_latest_signals():
    db = SessionLocal()
    try:
        return db.query(TradeSignal).order_by(TradeSignal.timestamp.desc()).limit(10).all()
    finally:
        db.close()

def get_latest_orders():
    db = SessionLocal()
    try:
        return db.query(Order).order_by(Order.created_at.desc()).limit(10).all()
    finally:
        db.close()

def main():
    st.title("Fear & Greed Adaptive Trading Framework")

    # --- Current Regime ---
    st.header("Current Regime")
    st.write("Euphoric") # Placeholder

    # --- Latest Signals ---
    st.header("Latest Signals")
    signals = get_latest_signals()
    if signals:
        signals_data = {
            "Timestamp": [s.timestamp for s in signals],
            "Strategy ID": [s.strategy_id for s in signals],
            "Asset ID": [s.asset_id for s in signals],
            "Direction": [s.direction for s in signals],
            "Price": [s.price for s in signals],
        }
        signals_df = pd.DataFrame(signals_data)
        st.table(signals_df)
    else:
        st.write("No signals found.")

    # --- Latest Orders ---
    st.header("Latest Orders")
    orders = get_latest_orders()
    if orders:
        orders_data = {
            "Timestamp": [o.created_at for o in orders],
            "Asset ID": [o.asset_id for o in orders],
            "Side": [o.side for o in orders],
            "Quantity": [o.quantity for o in orders],
            "Status": [o.status for o in orders],
        }
        orders_df = pd.DataFrame(orders_data)
        st.table(orders_df)
    else:
        st.write("No orders found.")


if __name__ == "__main__":
    main()