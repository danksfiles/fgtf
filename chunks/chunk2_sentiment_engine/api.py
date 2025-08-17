from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.regime import MarketRegimeSchema, MarketRegime

router = APIRouter()

@router.get("/regime/current", response_model=MarketRegimeSchema)
def get_current_regime(db: Session = Depends(get_db)):
    """Returns the most recent market regime."""
    return db.query(MarketRegime).order_by(MarketRegime.created_at.desc()).first()
