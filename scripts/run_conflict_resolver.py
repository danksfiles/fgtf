import sys
sys.path.append('.')

from chunks.chunk3_strategies.signals.conflict_resolver import resolve_conflicts
from src.database import SessionLocal
from src.models.signals import TradeSignal, SignalDirection
from datetime import datetime

def run():
    db = SessionLocal()
    try:
        # Create dummy signals
        signal1 = TradeSignal(strategy_id=1, asset_id=1, timestamp=datetime.now(), signal_type="test", strength=0.8, direction=SignalDirection.LONG, price=100)
        signal2 = TradeSignal(strategy_id=2, asset_id=1, timestamp=datetime.now(), signal_type="test", strength=0.7, direction=SignalDirection.LONG, price=101)
        signal3 = TradeSignal(strategy_id=3, asset_id=1, timestamp=datetime.now(), signal_type="test", strength=0.9, direction=SignalDirection.SHORT, price=99)

        db.add_all([signal1, signal2, signal3])
        db.commit()

        print("Dummy signals created.")

        # Run conflict resolver
        master_signal = resolve_conflicts(asset_id=1)

        if master_signal:
            print("Conflict resolved. Master signal created:")
            print(f"  ID: {master_signal.master_signal_id}")
            print(f"  Asset ID: {master_signal.asset_id}")
            print(f"  Direction: {master_signal.direction}")
            print(f"  Conflicting signals: {master_signal.conflicting_signals}")
        else:
            print("No master signal created.")

    finally:
        db.close()

if __name__ == "__main__":
    run()
