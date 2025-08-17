import sys
sys.path.append('.')

from src.database import SessionLocal
from src.models.risk import RiskMetrics
from sqlalchemy import desc

def check_portfolio_drawdown(portfolio_value: float, drawdown_threshold: float):
    """
    Checks the portfolio drawdown and triggers a circuit breaker if it exceeds the threshold.
    """
    db = SessionLocal()
    try:
        # Fetch the last 30 days of risk metrics
        historical_metrics = db.query(RiskMetrics).order_by(desc(RiskMetrics.timestamp)).limit(30).all()

        if not historical_metrics:
            return False

        # Calculate the peak portfolio value
        peak_value = max([m.portfolio_value for m in historical_metrics])

        # Calculate the current drawdown
        drawdown = (peak_value - portfolio_value) / peak_value

        if drawdown > drawdown_threshold:
            print(f"CIRCUIT BREAKER TRIPPED: Portfolio drawdown ({drawdown:.2%}) exceeds threshold ({drawdown_threshold:.2%}). ALL SELL.")
            return True
        else:
            return False
    finally:
        db.close()
