from typing import List
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.signals import TradeSignal
from .conflict_resolver import resolve_conflicts

def generate_master_signal(db: Session) -> None:
    """
    Generates a master signal by fetching all recent signals for each asset
    and resolving conflicts.
    """
    print("Generating master signal...")
    # Get all unique asset_ids from recent signals
    asset_ids = db.query(TradeSignal.asset_id).distinct().all()
    asset_ids = [a[0] for a in asset_ids]

    for asset_id in asset_ids:
        # Fetch all signals for the current asset that have not been executed
        signals = db.query(TradeSignal).filter(
            TradeSignal.asset_id == asset_id,
            TradeSignal.is_executed == False
        ).all()

        if signals:
            master_signal = resolve_conflicts(signals)
            if master_signal:
                # In a real scenario, we would store the master signal in a new table.
                # For now, we just print it.
                print(f"Master signal for asset {asset_id}: {master_signal.direction.value}")
            else:
                print(f"No consensus for asset {asset_id}.")

    print("Master signal generation complete.")

def main():
    db: Session = next(get_db())
    try:
        generate_master_signal(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
