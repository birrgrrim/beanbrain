from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Origin
from ..schemas import OriginOut

router = APIRouter(prefix="/origins", tags=["origins"])


@router.get("/", response_model=list[OriginOut])
def list_origins(db: Session = Depends(get_db)):
    return db.query(Origin).order_by(Origin.name_en).all()
