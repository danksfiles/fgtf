from typing import List
from src.models.signals import TradeSignal, SignalDirection
from src.models.master_signal import MasterSignal
from src.database import SessionLocal
from sqlalchemy import desc
from datetime import datetime

def resolve_conflicts(asset_id: int) -> MasterSignal:
    """
    Resolves conflicts between signals from different strategies for a given asset
    using a majority vote and saves the result to the master_signals table.
    """
    db = SessionLocal()
    try:
        # Fetch the last 3 signals for the given asset
        signals = db.query(TradeSignal).filter(TradeSignal.asset_id == asset_id).order_by(desc(TradeSignal.timestamp)).limit(3).all()

        if len(signals) < 3:
            return None

        longs = [s for s in signals if s.direction == SignalDirection.LONG]
        shorts = [s for s in signals if s.direction == SignalDirection.SHORT]

        if len(longs) >= 2 or len(shorts) >= 2:
            if len(longs) > len(shorts):
                winning_direction = SignalDirection.LONG
                winning_signals = longs
            else:
                winning_direction = SignalDirection.SHORT
                winning_signals = shorts

            # Create a consolidated signal
            # For simplicity, we'll use the data from the latest winning signal
            latest_winning_signal = sorted(winning_signals, key=lambda x: x.timestamp, reverse=True)[0]

            master_signal = MasterSignal(
                asset_id=asset_id,
                timestamp=datetime.now(),
                signal_type="consolidated",
                strength=latest_winning_signal.strength,
                direction=winning_direction.value,
                price=latest_winning_signal.price,
                stop_loss=latest_winning_signal.stop_loss,
                take_profit=latest_winning_signal.take_profit,
                conflicting_signals=[s.signal_id for s in signals]
            )

            db.add(master_signal)
            db.commit()
            db.refresh(master_signal)

            return master_signal
        else:
            # No clear majority
            return None
    finally:
        db.close()
