import sys
sys.path.append('.')

from chunks.chunk4_risk_management.circuit_breakers.portfolio_breaker import check_portfolio_drawdown
from src.database import SessionLocal
from src.models.risk import RiskMetrics
from datetime import datetime, timedelta

def run():
    db = SessionLocal()
    try:
        # Create dummy risk metrics
        for i in range(10):
            db.add(RiskMetrics(
                timestamp=datetime.now() - timedelta(days=i),
                portfolio_value=10000 - (i * 100),
                daily_pnl=0,
                daily_pnl_pct=0,
                unrealized_pnl=0,
                unrealized_pnl_pct=0,
                max_drawdown=0,
                exposure_pct=0,
                leverage=0
            ))
        db.commit()

        print("Dummy risk metrics created.")

        # Run portfolio breaker check
        check_portfolio_drawdown(portfolio_value=8000, drawdown_threshold=0.1)

    finally:
        db.close()

if __name__ == "__main__":
    run()
