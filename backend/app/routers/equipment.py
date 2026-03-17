from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import BrewMethod, Equipment
from ..schemas import BrewMethodOut, EquipmentOut

router = APIRouter(tags=["equipment"])


@router.get("/equipment", response_model=list[EquipmentOut])
def list_equipment(db: Session = Depends(get_db)):
    return db.query(Equipment).filter(Equipment.is_active == True).all()


@router.get("/brew-methods", response_model=list[BrewMethodOut])
def list_brew_methods(db: Session = Depends(get_db)):
    return db.query(BrewMethod).all()
